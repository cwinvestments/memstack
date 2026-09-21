#!/usr/bin/env bash
# MemStack: junk-write guard (PreToolUse, matcher Bash)
#
# THE DEFECT CLASS
#
# A redirection operator turns into a file write. When the token after it is a
# code fragment rather than a filename, the shell silently creates a 0-byte
# file named after that fragment. Nothing errors, nothing is reported, and the
# file sits in the repo root until somebody runs git add -A and commits it.
#
# Every 0-byte junk file in this repository's ledger came from that mechanism:
#
#   client/green-acres-client@1.0.0, client/npm, client/react-scripts
#       npm prints a lifecycle banner whose every line begins with a redirect
#       operator followed by a token. That output was re-executed as shell
#       input, so the banner's own tokens became filenames. Committed
#       2025-11-02, not removed until 46cff0d on 2026-08-19.
#   console.error, s.category
#       identifiers that had just been written inside a quoted code fragment.
#   a file named with a single backtick
#       authored prose containing a backtick.
#
# HOW IT DECIDES
#
# It parses the command the way a shell does, tracking single quotes, double
# quotes and backslash escapes, and considers only the redirection operators
# that are at the top level. Each one's target token is classified: a filename
# shape is allowed, a code-fragment shape is blocked.
#
# It then adds the one case where quoting cannot be trusted. A command whose
# quotes do not balance is the precondition for the whole defect class: that is
# when an operator inside what looked like an argument is reinterpreted as a
# redirect. Unbalanced quotes plus a redirection operator anywhere in the text
# is therefore blocked on its own.
#
# WHAT IT DOES NOT SCAN
#
# Heredoc bodies, which are blanked before parsing. A heredoc body is never
# parsed by the shell for redirections, which is why the standing rule names it
# as the safe way to pass multi-line text, and its contents routinely carry
# both unbalanced apostrophes and operators. Scanning it would block the recipe
# this guard exists to teach.
#
# WHAT IT NEVER DOES
#
# It never emits, logs or stores the command text. The block message names the
# offending target token and nothing else. That token is the filename that was
# about to be created, so it is the one thing the session needs back.
#
# POSTURE: FAIL OPEN, LOUDLY. No python, or a payload that will not parse,
# prints a DEGRADED line and exits 0. Exit 2 blocks; everything else is 0.
#
# CALIBRATION, AND WHAT IT BOUGHT
#
# The rules were not chosen by eye. They were replayed offline over 3087 real
# Bash commands drawn from this project's 151 session transcripts and 18
# observation logs, 995 of which contain a redirection character. The first
# rule set blocked 63 of them. Every one was a false block, and they are the
# reason for three loosenings recorded on the rules below:
#
#   1. Only top-level operators count. The first set inspected every
#      greater-than sign in the text, which flagged sed expressions, inline
#      python slices, curl format strings and quoted comparisons. A shell does
#      not redirect on those, so neither does this.
#   2. A token may carry a variable reference. Redirecting into "$SP/out.txt"
#      is a path the author computed, not a fragment.
#   3. A leading-dot name with no second dot is a config file, not an
#      unrecognised extension. This is what .secretpaths and .gitignore are.
#
# Plus two tokenizer repairs, which were bugs rather than policy: a trailing
# bracket from a subshell such as (cmd 2>/dev/null) is stripped, and a quoted
# target is read to its closing quote instead of being cut at the first one.
#
# The final rule set blocks 0 of the 3087. The loosening is real coverage
# given up: a well-formed, correctly quoted inline fragment containing an
# arrow is allowed here, though the standing prose rule still forbids it,
# because blocking that shape false-blocks more than forty real commands.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$SCRIPT_DIR/../observations"

note() {
    printf 'junk-write-guard: %s\n' "$1" >&2
    local stamp day
    stamp="$(date -u '+%Y-%m-%dT%H:%M:%SZ' 2>/dev/null || echo unknown-time)"
    day="$(date -u '+%Y-%m-%d' 2>/dev/null || echo unknown-date)"
    if mkdir -p "$LOG_DIR" 2>/dev/null; then
        printf '%s  %s\n' "$stamp" "$1" >> "$LOG_DIR/junk-write-guard-${day}.log" 2>/dev/null
    fi
    return 0
}

PAYLOAD="$(cat)"

PY=""
for candidate in python3 python py; do
    if command -v "$candidate" >/dev/null 2>&1; then
        PY="$candidate"
        break
    fi
done

if [ -z "$PY" ]; then
    note "DEGRADED: no python interpreter, so hook input cannot be parsed and this junk-write guard did NOT run for this call"
    exit 0
fi

# The classifier source is split at the REPLAY_SPLIT marker by replay.py,
# which execs the half above it to replay the exact shipped rules over the
# historical corpus. Keep the marker, and keep every decision function above
# it, or the replay stops testing what ships.
PYSRC="$(cat <<'PYEOF'
import json
import os
import re
import sys

# Extensions that name a real output file. An unknown extension is not treated
# as an extension at all, which is what catches console.error and s.category:
# both have a dot, neither names a file anybody meant to write.
KNOWN_EXT = {
    "txt", "md", "markdown", "json", "jsonl", "ndjson", "log", "csv", "tsv",
    "html", "htm", "xml", "svg", "yml", "yaml", "toml", "ini", "cfg", "conf",
    "js", "mjs", "cjs", "ts", "tsx", "jsx", "py", "pyc", "sh", "bash", "zsh",
    "ps1", "cmd", "bat", "sql", "patch", "diff", "out", "err", "tmp", "temp",
    "bak", "orig", "rej", "lock", "sum", "sha256", "png", "jpg", "jpeg", "gif",
    "pdf", "zip", "gz", "tgz", "tar", "db", "sqlite", "bin", "exe", "dll",
    "map", "css", "scss", "less", "env", "example", "sample", "template",
    "dist", "snap", "list", "report", "receipt", "state", "cache", "pid",
    "url", "key", "pub", "crt", "pem", "resolved", "backup", "1", "2",
}

# Targets that are not files at all.
NOT_A_FILE = {
    "/dev/null", "/dev/stdout", "/dev/stderr", "/dev/tty", "/dev/fd/1",
    "/dev/fd/2", "nul", "con",
}

# Characters that mean the token is a code fragment rather than a filename.
# The equals sign is here because s.category=x shaped fragments are in the
# ledger, the parenthesis because console.error( is, the backtick because a
# file named with one is.
FRAGMENT_CHARS = set("()`;{}[]!*?<>|,'\"=")

SCRATCH_MARKERS = ("temp/claude/", "appdata/local/temp", "/tmp/", "temp\\claude\\")

TRAILING_STRIP = ")]},;:"


def blank_heredocs(text):
    """Replace heredoc bodies with spaces, preserving every character index.

    A heredoc body is not shell syntax, so its operators are not redirects and
    its apostrophes do not unbalance the command.
    """
    out = list(text)
    for match in re.finditer(r"<<-?\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1", text):
        delim = match.group(2)
        nl = text.find("\n", match.end())
        if nl == -1:
            start, end = match.end(), len(text)
        else:
            start = nl + 1
            end = len(text)
            closer = re.search(r"^[ \t]*" + re.escape(delim) + r"[ \t]*\r?$",
                               text[start:], re.MULTILINE)
            if closer:
                end = start + closer.start()
        for idx in range(start, min(end, len(out))):
            if out[idx] != "\n":
                out[idx] = " "
    return "".join(out)


def read_target(text, pos):
    """Read the redirect target token starting at pos. Returns (token, end)."""
    i = pos
    n = len(text)
    chars = []
    quote = None
    while i < n:
        ch = text[i]
        if quote:
            if ch == quote:
                quote = None
            else:
                chars.append(ch)
            i += 1
            continue
        if ch in ("'", '"'):
            quote = ch
            i += 1
            continue
        if ch == "\\" and i + 1 < n:
            chars.append(text[i + 1])
            i += 2
            continue
        if ch in " \t\n\r;|&<>":
            break
        chars.append(ch)
        i += 1
    return ("".join(chars), i)


def scan(command):
    """Top-level redirect targets, plus whether the command's quotes balance."""
    text = blank_heredocs(command)
    targets = []
    i = 0
    n = len(text)
    quote = None
    while i < n:
        ch = text[i]
        if quote == "'":
            if ch == "'":
                quote = None
            i += 1
            continue
        if quote == '"':
            if ch == "\\":
                i += 2
                continue
            if ch == '"':
                quote = None
            i += 1
            continue
        if ch == "\\":
            i += 2
            continue
        if ch in ("'", '"'):
            quote = ch
            i += 1
            continue
        if ch == ">":
            j = i + 1
            if j < n and text[j] == ">":
                j += 1
            while j < n and text[j] in " \t":
                j += 1
            if j < n and text[j] == "(":
                i = j + 1  # process substitution, not a file redirect
                continue
            if j < n and text[j] == "&":
                k = j + 1
                while k < n and (text[k].isdigit() or text[k] == "-"):
                    k += 1
                i = k
                continue
            token, end = read_target(command, j)
            targets.append(token)
            i = end if end > i else i + 1
            continue
        i += 1
    return targets, (quote is not None)


def extension(tok):
    base = tok.replace("\\", "/").split("/")[-1]
    # A leading-dot name with no second dot is a config file, not an extension.
    # LOOSENED BY CALIBRATION: .secretpaths was blocked as an unrecognised
    # extension, and .gitignore, .npmrc and .verify-required are the same shape.
    if base.startswith(".") and base.count(".") == 1:
        return "dotfile"
    if "." not in base:
        return None
    ext = base.rsplit(".", 1)[1].lower()
    return ext or None


def classify_target(tok, cwd, scratchpad=None):
    """None to allow, or a short reason to block."""
    tok = tok.strip()
    while tok and tok[-1] in TRAILING_STRIP and tok.count("(") == 0 and tok.count("[") == 0:
        # A trailing bracket from a subshell, as in (cmd 2>/dev/null), is
        # punctuation of the enclosing command, not part of the filename.
        tok = tok[:-1]
    if not tok:
        return None

    low = tok.replace("\\", "/").lower()

    if low in NOT_A_FILE:
        return None
    # The payload carries the session's scratchpad_dir at the top level, found
    # by probing a real payload. Prefer it over the path markers, which are a
    # fallback for a payload that does not carry it.
    if scratchpad:
        if low.startswith(scratchpad.replace("\\", "/").lower().rstrip("/")):
            return None
    for marker in SCRATCH_MARKERS:
        if marker in low:
            return None

    try:
        candidate = tok if os.path.isabs(tok) else os.path.join(cwd, tok)
        if os.path.exists(candidate):
            return None  # overwriting or appending to something already there
    except Exception:
        pass

    # LOOSENED BY CALIBRATION: a token carrying a variable reference is a path
    # the author computed. Every junk file in the ledger came from literal text.
    if "$" in tok:
        return None

    bad = sorted(set(c for c in tok if c in FRAGMENT_CHARS))
    if bad:
        return "a code fragment, not a filename: it contains %s" % " ".join(bad)

    ext = extension(tok)
    if ext == "dotfile":
        return None
    if ext is None:
        if "/" in tok or "\\" in tok:
            parent = os.path.dirname(tok if os.path.isabs(tok) else os.path.join(cwd, tok))
            try:
                if parent and os.path.isdir(parent):
                    return None
            except Exception:
                pass
        return "a bare word with no extension and no such file"
    if ext not in KNOWN_EXT:
        return "an unrecognised extension (.%s)" % ext
    return None


def judge_command(command, cwd, scratchpad=None):
    """(target, reason) for the first offending redirect, else (None, None)."""
    if not isinstance(command, str) or ">" not in command:
        return (None, None)
    targets, unbalanced = scan(command)
    for token in targets:
        reason = classify_target(token, cwd, scratchpad)
        if reason:
            return (token.strip() or "an empty target", reason)
    if unbalanced:
        return ("an unquoted fragment",
                "inside a command whose quotes do not balance, which is the "
                "precondition for an operator being reinterpreted as a redirect")
    return (None, None)


# REPLAY_SPLIT

try:
    payload = json.load(sys.stdin)
except Exception:
    sys.exit(3)
if not isinstance(payload, dict):
    sys.exit(3)
tool_input = payload.get("tool_input")
if not isinstance(tool_input, dict):
    sys.exit(3)

cwd = payload.get("cwd") or os.getcwd()
scratchpad = payload.get("scratchpad_dir")
target, reason = judge_command(tool_input.get("command"), cwd,
                               scratchpad if isinstance(scratchpad, str) else None)
if target:
    sys.stdout.write("BLOCK\t%s\t%s\n" % (target, reason))
else:
    sys.stdout.write("ALLOW\n")
sys.exit(0)
PYEOF
)"

DECISION="$(printf '%s' "$PAYLOAD" | "$PY" -c "$PYSRC" 2>/dev/null)"
PARSE_RC=$?

if [ "$PARSE_RC" -ne 0 ]; then
    note "DEGRADED: hook input did not parse, so this junk-write guard did NOT run for this call"
    exit 0
fi

case "$DECISION" in
    BLOCK*) ;;
    *) exit 0 ;;
esac

TARGET="$(printf '%s' "$DECISION" | cut -f2)"
REASON="$(printf '%s' "$DECISION" | cut -f3 | tr -d '\r\n')"
[ -n "$TARGET" ] || TARGET="the redirect target"

note "BLOCKED a redirect into [${TARGET}]"

printf 'BLOCKED: a redirection in this command targets [%s].\n\n' "$TARGET" >&2
printf 'That target is %s.\n\n' "$REASON" >&2
cat >&2 <<'JUNK_MSG'
A redirection operator turns into a file write. When the token after it is a
code fragment, the shell creates a 0-byte file named after that fragment,
reports nothing, and leaves it in the repo root for the next git add -A to
commit. Every junk file in this repository's ledger was created that way, one
of them from an arrow inside ordinary prose in a command that ran no code.

Two recipes, and between them they cover every case:

1. PROSE goes through the Write tool, never through a shell argument.
   Commit messages, PR and issue bodies, report text, diary entries: write the
   text to a file with the Write tool, then pass the path.

     git commit -F PATH
     gh pr create --body-file PATH
     gh issue comment --body-file PATH

   Rewriting the sentence also works: "maps to" instead of an arrow, "greater
   than" instead of the operator.

2. PAYLOADS go to a file first and are piped in through the stdin sentinel, so
   the shell never parses them:

     cat PATH | python db/memstack-db.py add-plan-task -

   The trailing dash is the sentinel: the command reads the document from
   stdin, which the shell does not look inside. Inline code follows the same
   rule, as a script invoked by path rather than through -c or -e.

If the redirect was deliberate and the target really is a file, give it a
directory and a known extension, or send it to the session scratchpad.
JUNK_MSG
exit 2
