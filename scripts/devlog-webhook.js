#!/usr/bin/env node
'use strict';

// devlog-webhook.js — fire-and-forget DevLog webhook for the Diary skill.
//
// WHY THIS FILE EXISTS
// --------------------
// The webhook used to be fired with an inline one-liner:
//
//   node -e "fetch(URL,{...}).then(r=>console.log('Devlog webhook:',r.status))
//                            .catch(e=>console.error('Devlog webhook failed:',e.message))"
//
// On Windows CMD that one-liner is unsafe. When the command is wrapped inside
// another double-quoted context (e.g. cmd.exe /c "node -e "..."") CMD pairs the
// outer quote with the FIRST inner quote, which terminates the -e argument's
// quoting early. CMD then parses the rest unquoted and treats the ">" inside the
// "=>" fat-arrow as an output-redirection operator. The token right after ">"
// becomes the redirect target, so CMD creates a 0-byte file literally named
//   console.error('Devlog
// in whatever directory the diary was saved from — one junk file per save.
//
// Moving the JS into a real file run BY PATH removes every inline quoting and
// redirection hazard: there are no quotes for the shell to mis-pair and no ">"
// on the command line. Invoke it as:
//
//   node scripts/devlog-webhook.js <markdown-backup-path>
//
// CONTRACT (intentional, do not "improve" away)
// ---------------------------------------------
// The webhook is fire-and-forget: it must NEVER block, fail, or delay a diary
// save, and must NEVER create a file on disk. Exit code is ALWAYS 0, in every
// path below.
//
// What is NOT swallowed is visibility: each outcome prints exactly one line to
// stderr (prefixed "devlog-webhook:") so a broken pipeline is distinguishable
// from a working one in the Diary hook output. Behavior is unchanged — only
// diagnostics were added.
//   * MEMSTACK_DEVLOG_WEBHOOK not set      -> stderr line, exit 0, nothing sent.
//   * DEVLOG_KEY not set                   -> stderr line, exit 0, nothing sent.
//   * `fetch` unavailable (Node < 18)      -> stderr line, exit 0, nothing sent.
//   * Missing/unreadable/empty markdown    -> stderr line, exit 0, nothing sent.
//   * Network error / timeout              -> stderr line, exit 0.
//   * Non-2xx response                     -> stderr line (status + body), exit 0.
//   * 2xx response                         -> stderr line confirming, exit 0.

// One diagnostic line to stderr. Prefixed so it's greppable in Diary hook output.
function log(msg) {
  console.error('devlog-webhook: ' + msg);
}

async function main() {
  const url = process.env.MEMSTACK_DEVLOG_WEBHOOK;
  if (!url) {
    log('MEMSTACK_DEVLOG_WEBHOOK is not set — nothing sent.');
    return;
  }

  const key = process.env.DEVLOG_KEY;
  if (!key) {
    log('DEVLOG_KEY is not set — nothing sent.');
    return;
  }

  // Global fetch requires Node 18+. If it's missing, no-op rather than crash.
  if (typeof fetch !== 'function') {
    log('global fetch unavailable (needs Node 18+) — nothing sent.');
    return;
  }

  // Read the diary markdown that was just written.
  const mdPath = process.argv[2];
  if (!mdPath) {
    log('no diary path argument given — nothing sent.');
    return;
  }
  let diary;
  try {
    diary = require('fs').readFileSync(mdPath, 'utf8');
  } catch (err) {
    log('could not read diary at ' + mdPath + ': ' + err.message + ' — nothing sent.');
    return;
  }
  if (!diary || !diary.trim()) {
    log('diary at ' + mdPath + ' is empty — nothing sent.');
    return;
  }

  // Bound the request so an unreachable webhook can never hang the diary save.
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 5000); // ~5s, like `curl -m 5`
  try {
    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'x-devlog-key': key },
      body: JSON.stringify({ diary }),
      signal: controller.signal,
    });
    if (res.ok) {
      log('sent OK (HTTP ' + res.status + ').');
    } else {
      let body = '';
      try { body = (await res.text()).slice(0, 200); } catch { /* body unreadable */ }
      log('webhook returned HTTP ' + res.status + ' — treated as NOT sent. Body: ' + body);
    }
  } catch (err) {
    log('network error: ' + err.message + ' — nothing sent.');
  } finally {
    clearTimeout(timer);
  }
}

// Top-level guard: nothing escapes. Process ends with the default exit code 0.
main().catch(() => {});
