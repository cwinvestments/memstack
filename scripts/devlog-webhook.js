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
//   * MEMSTACK_DEVLOG_WEBHOOK not set      -> silent no-op, exit 0, no output.
//   * Missing/unreadable markdown path     -> swallowed, exit 0.
//   * Network error / timeout / non-2xx    -> swallowed, exit 0.
//   * `fetch` unavailable (Node < 18)      -> swallowed, exit 0.
// The webhook is fire-and-forget: it must NEVER block, fail, or delay a diary
// save, and must NEVER create a file on disk.

async function main() {
  const url = process.env.MEMSTACK_DEVLOG_WEBHOOK;
  if (!url) return; // not configured -> clean no-op (no error, no output)

  // Global fetch requires Node 18+. If it's missing, no-op rather than crash.
  if (typeof fetch !== 'function') return;

  // Read the diary markdown that was just written. If we can't read it, there
  // is nothing meaningful to send — swallow and return.
  const mdPath = process.argv[2];
  let diary;
  try {
    diary = require('fs').readFileSync(mdPath, 'utf8');
  } catch {
    return;
  }

  // Bound the request so an unreachable webhook can never hang the diary save.
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 5000); // ~5s, like `curl -m 5`
  try {
    await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ diary }),
      signal: controller.signal,
    });
    // Response status is intentionally ignored — fire-and-forget.
  } catch {
    // network failure / abort / anything -> swallow
  } finally {
    clearTimeout(timer);
  }
}

// Top-level guard: nothing escapes. Process ends with the default exit code 0.
main().catch(() => {});
