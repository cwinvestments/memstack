#!/usr/bin/env python3
"""The working-directory guard: refuse a prompt pasted into the wrong session.

A task prompt names its directory on a "Working directory:" line. Pasted into a
Claude Code window open on a different repository, the prompt runs anyway, in
the wrong tree, and nothing says so until the damage is done. This hook reads a
UserPromptSubmit payload on stdin and blocks that one case.

Contract, and every clause of it is deliberate:

- The directory line is read from one of two places, in this order. First,
  the first pasted block, the <pasted_content id="..."> ... </pasted_content
  id="..."> wrapper Claude Code puts around LONGER pasted text. Second, when
  no wrapped declaration exists, the prompt's first non-blank line, if that
  line is itself a "Working directory:" line: a probe on 2026-09-26 showed a
  short paste arrives as raw text with no wrapper, so this is where its
  routing line sits. A typed first line is indistinguishable from a short
  paste and is read the same way; a declaration contradicting cwd is wrong
  either way. A "Working directory:" line that is neither wrapped nor first
  is a reference in prose (a quoted diary, a path in a question) and is
  ignored.
- Inside a block, the FIRST "Working directory:" line is the declaration. A
  diary opens with one, and a pasted excerpt of it is exactly the real-world
  case, so a later line never overrides the first.
- It blocks only when the declared path and the payload cwd are both absolute,
  both parse cleanly, and neither contains the other. Equal passes, and so do
  a declared parent or child of cwd: a worktree, a monorepo subdirectory, and
  a prompt naming the repo root from a subdirectory are all legitimate.
- Everything else passes, silently. This gates every prompt of every session,
  and a false block teaches the user to stop reading blocks, which kills the
  guard more surely than any bug.
- A block is exit 0 with {"decision": "block", "reason": ...} as the ONLY
  stdout. Never exit 2: that erases the prompt, while the JSON block shows the
  user their prompt back, so a hard block here loses nothing.
- Fail open, loud. Any exception or unreadable payload prints nothing to
  stdout, so the prompt proceeds, and one line to stderr beginning
  "workdir-guard: DEGRADED", so a broken guard is never mistaken for a quiet
  one.

The report marker. verify.py's report-marker hook runs in PARALLEL with this
one on the same prompt, knows nothing about a block, and may arm
.memstack/report-required.json for a prompt that never ran. When this guard
blocks a prompt that would have armed it, it waits (bounded) for that
prompt's marker to land and puts back whatever was there before. See
neutralize_report_marker for the residual that parallel execution leaves.

Stdlib only. Local dogfood: registered in .claude/settings.local.json, not in
hooks/hooks.json.
"""

import json
import os
import re
import sys
import time
from pathlib import Path

PREFIX = "workdir-guard:"

_OPEN_RE = re.compile(r"^[ \t]*<pasted_content\b[^>\n]*>[ \t]*$", re.MULTILINE)
_CLOSE_RE = re.compile(r"^[ \t]*</pasted_content\b[^>\n]*>[ \t]*$", re.MULTILINE)
_LINE_RE = re.compile(r"^[ \t]*working directory:(.*)$",
                      re.IGNORECASE | re.MULTILINE)

# Characters no directory name on the declaring side should carry. Seeing one
# means the parse is not trustworthy, and doubt passes.
_BAD_CHARS = re.compile(r'[<>|?*"\x00-\x1f]')
_DRIVE_ABS = re.compile(r"^[a-z]:/")
_GITBASH_DRIVE = re.compile(r"^/([a-z])(?=/|$)")

# How long a block waits for the parallel report-marker to write, when the
# blocked prompt would have armed it. Far inside the 30s hook timeout.
MARKER_WAIT_S = 4.0
MARKER_POLL_S = 0.05
# A marker is this prompt's only if it was requested no earlier than this
# many seconds before the guard started. The two hooks start together.
MARKER_SLACK_S = 10.0


def first_pasted_block(prompt):
    """The text of the first complete pasted block, or None."""
    opened = _OPEN_RE.search(prompt)
    if opened is None:
        return None
    closed = _CLOSE_RE.search(prompt, opened.end())
    if closed is None:
        return None
    return prompt[opened.end():closed.start()]


def declared_line(block):
    """The remainder of the first "Working directory:" line, stripped, or
    None when the block has no such line."""
    found = _LINE_RE.search(block)
    if found is None:
        return None
    return found.group(1).strip()


def first_line_declaration(prompt):
    """The rest of the prompt's first non-blank line when that line is itself a
    "Working directory:" line, or None. A short paste arrives with no wrapper,
    and this is the only place its routing line can be; a line further down is
    a reference in prose, not a routing line, and is never read."""
    for line in prompt.splitlines():
        if not line.strip():
            continue
        found = _LINE_RE.fullmatch(line)
        return found.group(1).strip() if found else None
    return None


def _unwrap(text):
    """Strip matched wrapping quotes or backticks, and trailing punctuation."""
    text = text.strip()
    if len(text) >= 2 and text[0] == text[-1] and text[0] in "\"'`":
        text = text[1:-1].strip()
    return text.rstrip(".,;").strip()


def declared_candidates(rest):
    """(primary, all candidates) for the declared path, from the line's rest.

    The primary is the path shown in a block message: the whole rest when it
    is quoted or names a real directory, otherwise the text before the first
    space, which drops decoration such as "(dev branch)". The candidates are
    every space-bounded prefix too, so an unquoted path with a space in it can
    only ever be read as a match, never manufacture a mismatch.
    """
    rest = rest.strip()
    if not rest:
        return None, []
    if rest[0] in "\"'`":
        close = rest.find(rest[0], 1)
        if close > 1:
            quoted = rest[1:close].strip()
            return quoted, [quoted]
    whole = _unwrap(rest)
    candidates = []
    words = rest.split(" ")
    for n in range(1, len(words) + 1):
        piece = _unwrap(" ".join(words[:n]))
        if piece and piece not in candidates:
            candidates.append(piece)
    if whole and whole not in candidates:
        candidates.append(whole)
    try:
        whole_is_dir = bool(whole) and os.path.isdir(whole)
    except (OSError, ValueError):
        whole_is_dir = False
    primary = whole if whole_is_dir else (candidates[0] if candidates else None)
    return primary, candidates


def normalize(path):
    """One comparable shape for a Windows path, or None when in any doubt.

    Lowercase, forward slashes, the Git Bash /c/... form folded into c:/...,
    no repeated or trailing slash. Relative paths, UNC paths, dot segments and
    stray metacharacters all return None, which the caller reads as pass.
    """
    if not isinstance(path, str):
        return None
    text = path.strip()
    if not text or _BAD_CHARS.search(text):
        return None
    text = text.replace("\\", "/").lower()
    if text.startswith("//"):
        return None
    text = _GITBASH_DRIVE.sub(lambda m: m.group(1) + ":", text, count=1)
    text = re.sub(r"/{2,}", "/", text)
    if re.fullmatch(r"[a-z]:", text):
        text += "/"
    if not _DRIVE_ABS.match(text):
        return None
    if len(text) > 3:
        text = text.rstrip("/")
    parts = text[3:].split("/") if len(text) > 3 else []
    if any(part in (".", "..") or part != part.strip() for part in parts):
        return None
    return text


def related(a, b):
    """Equal, or one is an ancestor of the other."""
    if a == b:
        return True
    a_slash = a if a.endswith("/") else a + "/"
    b_slash = b if b.endswith("/") else b + "/"
    return b.startswith(a_slash) or a.startswith(b_slash)


def decide(payload):
    """The block reason, or None to pass. Pure: reads the payload only, plus
    one isdir probe that can only turn a mismatch into a pass."""
    if not isinstance(payload, dict):
        return None
    prompt = payload.get("prompt")
    cwd = payload.get("cwd")
    if not isinstance(prompt, str) or not isinstance(cwd, str):
        return None
    block = first_pasted_block(prompt)
    rest = declared_line(block) if block is not None else None
    if rest is None:
        rest = first_line_declaration(prompt)
    if rest is None:
        return None
    primary, candidates = declared_candidates(rest)
    if primary is None:
        return None
    cwd_norm = normalize(cwd)
    primary_norm = normalize(primary)
    if cwd_norm is None or primary_norm is None:
        return None
    for candidate in candidates:
        norm = normalize(candidate)
        if norm is not None and related(norm, cwd_norm):
            return None
    return ("Working-directory guard: the prompt declares " + primary
            + " but this session is in " + cwd.strip()
            + ". If this is the wrong window, paste it where it belongs.")


def _load_verify():
    """verify.py, imported from beside this file. It has no import-time side
    effects: everything it does sits behind its __main__ guard."""
    here = str(Path(__file__).resolve().parent)
    if here not in sys.path:
        sys.path.insert(0, here)
    import verify  # noqa: PLC0415 - only needed on the rare block path
    return verify


def _read_bytes(path):
    try:
        return path.read_bytes()
    except FileNotFoundError:
        return None


def early_marker_snapshot(payload):
    """(marker path, bytes) taken the moment a block is decided, or (None, None).

    This runs BEFORE verify.py is imported, because that import is slow enough
    for a parallel report-marker to write first, and a snapshot taken after
    that write has already lost the marker it replaced. verify.py finds the
    root with `git rev-parse`; this walks up for a .git entry instead, which
    agrees in every ordinary repo and worktree. Where the two disagree,
    neutralize_report_marker notices and snapshots late at verify's path.
    """
    try:
        start = Path(payload["cwd"])
        if not start.is_dir():
            return None, None
        start = start.resolve()
        root = start
        for candidate in (start,) + tuple(start.parents):
            if (candidate / ".git").exists():
                root = candidate
                break
        path = root / ".memstack" / "report-required.json"
        return path, _read_bytes(path)
    except Exception:  # noqa: BLE001 - a missed snapshot only means a late one
        return None, None


def _is_this_prompts_marker(raw, session_id, prompt, started_at):
    """Did report-marker write this for the prompt being blocked?

    Matched on session, on the recorded prompt head being a prefix of this
    prompt with whitespace collapsed (a prefix rather than equality, so an
    installed verify.py with a different head cap still matches), and on a
    request time no earlier than the guard's own start less the slack.
    Unparsable bytes are a write in progress and read as not yet.
    """
    if raw is None:
        return False
    try:
        marker = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return False
    if not isinstance(marker, dict):
        return False
    head = marker.get("prompt_head")
    epoch = marker.get("requested_at_epoch")
    return (marker.get("session_id") == session_id
            and isinstance(head, str) and head
            and " ".join(prompt.split()).startswith(head)
            and isinstance(epoch, (int, float))
            and epoch >= started_at - MARKER_SLACK_S)


def neutralize_report_marker(payload, started_at, prior_path=None,
                             prior=None, wait_s=MARKER_WAIT_S):
    """Undo the report marker a blocked prompt would arm. Returns what it did.

    report-marker runs in parallel, so there is no ordering to lean on and no
    way to stop its write. What IS knowable: whether this prompt arms a marker
    at all (the same trigger function report-marker calls), and which marker
    it writes (this session, this prompt's head, requested now). So this
    waits, bounded, for that marker to appear, then restores the bytes that
    were there before this prompt, or removes the file when there were none.

    The residual, stated precisely rather than papered over:
    - If report-marker wrote BEFORE this guard took its snapshot, the snapshot
      already holds this prompt's marker and the earlier marker it replaced is
      gone. The guard can only delete, so a report still owed for an earlier
      prompt in this session stops being enforced. This needs report-marker to
      win a race it starts with a cmd.exe probe and an interpreter launch, so
      it should be rare; it is not impossible.
    - If report-marker takes longer than the wait, the marker lands after the
      guard has exited and stays armed for a prompt that never ran.
    - The cleaner point, for promotion into the plugin, is report_marker_decide
      in verify.py consulting decide() on the same payload before it writes.
      Both are pure functions of one payload, so that has no race at all. It
      is not done here because the local dogfood runs the INSTALLED plugin's
      verify.py, which this repo does not reach, and because shipping that
      check before this guard is registered would drop markers for prompts
      that were never blocked.
    """
    prompt = payload.get("prompt")
    verify = _load_verify()
    if not isinstance(prompt, str) or verify.report_trigger_match(prompt) is None:
        return "not-armed"
    session_id = verify._payload_session(payload)
    _, root = verify._payload_root(payload, None)
    marker_path = verify.report_marker_path(root)
    if prior_path is None or (Path(os.path.normcase(str(prior_path)))
                              != Path(os.path.normcase(str(marker_path)))):
        # No early snapshot, or it was of a different file: snapshot late.
        prior_path = marker_path
        prior = _read_bytes(prior_path)

    if _is_this_prompts_marker(prior, session_id, prompt, started_at):
        prior_path.unlink(missing_ok=True)
        return "removed-early"

    deadline = time.monotonic() + wait_s
    while time.monotonic() < deadline:
        now = _read_bytes(prior_path)
        if now != prior and _is_this_prompts_marker(now, session_id, prompt,
                                                    started_at):
            if prior is None:
                prior_path.unlink(missing_ok=True)
                return "removed"
            prior_path.write_bytes(prior)
            return "restored"
        time.sleep(MARKER_POLL_S)
    return "not-seen"


def run(raw, started_at=None):
    """(stdout text, stderr text) for one payload. Never raises."""
    started_at = time.time() if started_at is None else started_at
    try:
        try:
            payload = json.loads(raw)
        except ValueError as exc:
            return "", PREFIX + " DEGRADED (unreadable payload: " + str(exc) + ")"
        if not isinstance(payload, dict):
            return "", PREFIX + " DEGRADED (payload is not a JSON object)"
        reason = decide(payload)
        if reason is None:
            return "", ""
    except Exception as exc:  # noqa: BLE001 - fail open is the contract
        return "", (PREFIX + " DEGRADED (" + type(exc).__name__ + ": "
                    + str(exc) + ")")

    note = ""
    try:
        prior_path, prior = early_marker_snapshot(payload)
        neutralize_report_marker(payload, started_at, prior_path, prior)
    except Exception as exc:  # noqa: BLE001 - the block stands regardless
        note = (PREFIX + " report marker not neutralized ("
                + type(exc).__name__ + ": " + str(exc) + ")")
    return json.dumps({"decision": "block", "reason": reason}), note


def main():
    started_at = time.time()
    try:
        raw = sys.stdin.buffer.read().decode("utf-8")
    except Exception as exc:  # noqa: BLE001
        sys.stderr.write(PREFIX + " DEGRADED (stdin unreadable: "
                         + type(exc).__name__ + ")\n")
        return 0
    out, err = run(raw, started_at)
    if out:
        sys.stdout.write(out)
        sys.stdout.flush()
    if err:
        sys.stderr.write(err + "\n")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # noqa: BLE001 - last line of fail open
        try:
            sys.stderr.write(PREFIX + " DEGRADED (" + type(exc).__name__ + ")\n")
        except Exception:  # noqa: BLE001
            pass
        sys.exit(0)
