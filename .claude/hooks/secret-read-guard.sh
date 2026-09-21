#!/usr/bin/env bash
# MemStack: secret-read guard (PreToolUse)
#
# THE DEFECT CLASS
#
# Sessions leak secret values into the terminal by reading or grepping the
# files that hold them. Prose rules against printing secrets have failed
# repeatedly, because the rule is consulted after the intent to look at the
# file has already formed. This gate removes the discretion: a whole-file read
# of a secret-bearing path is refused mechanically, and the block message
# carries the safe alternative so the session is not left guessing.
#
# WHAT IT SEES
#
# Claude Code delivers hook input as one JSON document on stdin:
#
#   {"hook_event_name":"PreToolUse",
#    "tool_name":"Read",
#    "tool_input":{"file_path":"C:/x/.env"},
#    "cwd":"...","session_id":"..."}
#
# tool_name selects the rule. Read is judged on tool_input.file_path, Bash on
# tool_input.command, and Grep on tool_input.path and tool_input.glob together
# with tool_input.output_mode. Any other tool is allowed untouched.
#
# The Grep field names were captured from a real payload with a temporary probe
# hook rather than assumed, because the tool's parameter names are what the
# payload carries and a wrong guess here is a gate that never fires. What the
# probe showed:
#
#   tool_input keys, content mode:  -n, head_limit, output_mode, path, pattern
#   tool_input keys, default mode:  glob, pattern
#
# path and glob are strings and both are present only when the caller passed
# them. The load-bearing finding is the second line: output_mode is ABSENT from
# the payload when the caller does not pass it, rather than arriving as its
# default value. So absence has to be read as files_with_matches, and a rule
# written as output_mode == "content" is correct only because absence is
# handled first. The payload also carries a top-level scratchpad_dir.
#
# WHAT IT NEVER DOES
#
# It never emits, logs, or stores the command text or one byte of any file's
# contents. The only identifier that leaves this script is the BASENAME of the
# matched path, which is a filename and not a value. The recipes in the block
# messages use SRC and DST placeholders rather than the caller's own path for
# the same reason.
#
# POSTURE: FAIL OPEN, LOUDLY
#
# No python, or a payload that will not parse, means the gate cannot make a
# decision. It then says so on stderr and exits 0. A broken guard must never
# brick a session; a silent broken guard must never be mistaken for a working
# one. This is the same posture as the --critical notify gates.
#
# Exit codes: 2 blocks the tool call and shows stderr to the session. Every
# other path exits 0.
#
# Registered twice in .claude/settings.json, matcher Read and matcher Bash.
# This is a local dogfood: promotion into the shipped plugin is a separate
# task and no version surface moves for it.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$SCRIPT_DIR/../observations"

# One line to stderr, and the same line to the gate log when one can be
# written. Filenames and decisions only: never a command, never a value.
note() {
    printf 'secret-read-guard: %s\n' "$1" >&2
    local stamp day
    stamp="$(date -u '+%Y-%m-%dT%H:%M:%SZ' 2>/dev/null || echo unknown-time)"
    day="$(date -u '+%Y-%m-%d' 2>/dev/null || echo unknown-date)"
    if mkdir -p "$LOG_DIR" 2>/dev/null; then
        printf '%s  %s\n' "$stamp" "$1" >> "$LOG_DIR/secret-read-guard-${day}.log" 2>/dev/null
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
    note "DEGRADED: no python interpreter, so hook input cannot be parsed and this secret-read guard did NOT run for this call"
    exit 0
fi

PYSRC="$(cat <<'PYEOF'
import fnmatch
import json
import os
import shlex
import sys

# ---------------------------------------------------------------- patterns
#
# Conservative and exact. Every entry is a filename shape whose whole purpose
# is to hold credentials. Matching is on the path portion only: the basename
# for a bare pattern, the full normalised path for a pattern containing a
# slash. Case-insensitive throughout, because Windows is.

BUILTIN = [
    ".env",
    ".env.*",
    "config.local.json",
    ".npmrc",
    ".netrc",
    "*.pem",
    "*.pfx",
    "*.p12",
    "id_rsa",
    "id_ed25519",
    "*_rsa",
    "credentials*.json",
    "*.tfvars",
    "secrets.*",
    "*.secrets.*",
]

# Sample files are the documented counterpart of the real thing and hold
# placeholders by definition. Reading one is how a session learns which names
# exist without touching a value, so it must stay allowed.
NEVER = ["*.example", "*.sample", "*.example.*", "*.sample.*"]

# Verbs that print a file's bytes to the terminal. Blocking these is the whole
# mechanism. Known and deliberate gap: od, xxd, base64, nl, tac, and a python
# or node one-liner that opens the file, are not in this list, because the
# list is the spec's list. Widening it belongs to the promotion task.
BLOCKED_VERBS = {
    "cat", "type", "head", "tail", "more", "less", "strings",
    "sed", "awk", "gawk", "nawk",
}

# Searchers: allowed only in a form that cannot print a whole line.
GREP_VERBS = {"grep", "egrep", "fgrep", "rg", "ripgrep"}

# Verbs that report a property of the file and never its contents.
ALLOWED_VERBS = {"wc", "stat", "ls", "test", "[", "file", "du", "touch"}

# Once bytes have passed through a cryptographic hash, what can reach the
# terminal is a digest. This is the approved way to answer "are these two the
# same" without either value being emitted.
HASH_VERBS = {"sha256sum", "sha512sum", "sha1sum", "md5sum", "shasum", "cksum"}

# Wrappers to step over when looking for a stage's real verb.
WRAPPERS = {"sudo", "command", "env", "time", "nohup", "exec", "builtin"}

# Tools whose first positional argument is a pattern or a script, not a path.
# Without this, a perfectly ordinary "grep -rn \.env src/" would be read as a
# reference to .env and blocked.
PATTERN_FIRST = {
    "grep", "egrep", "fgrep", "rg", "ripgrep", "sed", "awk", "gawk", "nawk",
}
PATTERN_TAKING_FLAGS = {"-e", "--regexp", "-f", "--file", "--expression"}

REDIR_TOKENS = {">", ">>", "1>", "2>", "&>", "2>>", "1>>"}
REDIR_PREFIXES = ("&>", "1>>", "2>>", "1>", "2>", ">>", ">")


def repo_root(payload):
    return os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or os.getcwd()


def extra_patterns(payload):
    """Per-repo additions: one glob per line in .secretpaths at the repo root."""
    path = os.path.join(repo_root(payload), ".secretpaths")
    out = []
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if line and not line.startswith("#"):
                    out.append(line)
    except Exception:
        return []
    return out


def normalise(raw):
    s = raw.strip().strip('"').strip("'").strip()
    return s.replace("\\", "/").rstrip("/")


def matched_name(raw, patterns):
    """Return the basename when this path is secret-bearing, else None."""
    s = normalise(raw)
    if not s:
        return None
    base = s.split("/")[-1]
    if not base:
        return None
    low_base = base.lower()
    low_full = s.lower()
    # fnmatchcase, not fnmatch: fnmatch applies os.path.normcase, which on
    # Windows rewrites the separators of both sides. Both sides are already
    # lowercased here, so the case folding is done and normcase is only risk.
    for pat in NEVER:
        if fnmatch.fnmatchcase(low_base, pat.lower()):
            return None
    for pat in patterns:
        p = pat.strip().replace("\\", "/")
        if not p:
            continue
        target = low_full if "/" in p else low_base
        if fnmatch.fnmatchcase(target, p.lower()):
            return base
    return None


def glob_targets_secret(spec, patterns):
    """Does a Grep glob aim at a secret-bearing shape?

    A glob is itself a pattern, so the two are compared in both directions: a
    glob of **/.env has to match the .env rule, and a glob of *.pem has to
    match the *.pem rule. Only the last path segment is compared, which is the
    part naming the file.
    """
    s = normalise(spec)
    if not s:
        return None
    seg = s.split("/")[-1].lower()
    if not seg or seg in ("*", "**"):
        return None  # a glob that names no shape cannot be matched by name
    for pat in NEVER:
        if fnmatch.fnmatchcase(seg, pat.lower()):
            return None
    for pat in patterns:
        p = pat.strip().replace("\\", "/").split("/")[-1].lower()
        if not p:
            continue
        if fnmatch.fnmatchcase(seg, p) or fnmatch.fnmatchcase(p, seg):
            return seg
    return None


def verdict(state, name=None):
    if state == "BLOCK":
        sys.stdout.write("BLOCK\t%s\n" % (name or "the matched file"))
    else:
        sys.stdout.write("ALLOW\n")
    sys.exit(0)


# ------------------------------------------------------------- command scan

def split_top(text, seps):
    """Split on separators that are not inside quotes."""
    out, cur, i, quote = [], [], 0, None
    while i < len(text):
        ch = text[i]
        if quote:
            cur.append(ch)
            if ch == quote:
                quote = None
            i += 1
            continue
        if ch in ('"', "'"):
            quote = ch
            cur.append(ch)
            i += 1
            continue
        hit = None
        for sep in seps:
            if text.startswith(sep, i):
                hit = sep
                break
        if hit:
            out.append("".join(cur))
            cur = []
            i += len(hit)
            continue
        cur.append(ch)
        i += 1
    out.append("".join(cur))
    return out


def tokenise(stage):
    # posix=False on purpose. With posix=True shlex treats a backslash as an
    # escape character and eats it, so C:\Projects\app\.env tokenises as
    # C:Projectsapp.env, matches nothing, and a Windows-shaped path walks
    # straight through the gate. posix=False keeps the separators; the quotes
    # it leaves on a token are stripped in normalise().
    try:
        return shlex.split(stage, posix=False)
    except Exception:
        return stage.split()


def stage_verb(tokens):
    for tok in tokens:
        if "=" in tok and not tok.startswith("-") and "/" not in tok.split("=")[0]:
            continue  # leading VAR=value assignment
        base = tok.replace("\\", "/").split("/")[-1].lower()
        if base.endswith(".exe"):
            base = base[:-4]
        if base in WRAPPERS:
            continue
        return base
    return ""


def redirect_targets(tokens):
    """Tokens being written TO rather than read."""
    out, pending = set(), False
    for tok in tokens:
        if pending:
            out.add(normalise(tok))
            pending = False
            continue
        if tok in REDIR_TOKENS:
            pending = True
            continue
        for pref in REDIR_PREFIXES:
            if tok.startswith(pref) and len(tok) > len(pref):
                out.add(normalise(tok[len(pref):]))
                break
    return out


def has_only_matching(tokens):
    for tok in tokens:
        if tok == "--only-matching":
            return True
        if tok.startswith("--"):
            continue
        if tok.startswith("-") and len(tok) > 1 and "o" in tok[1:]:
            return True
    return False


def path_candidates(tokens, verb):
    """Argument tokens that could be paths, with pattern arguments removed."""
    skip_first = verb in PATTERN_FIRST and not any(
        t in PATTERN_TAKING_FLAGS for t in tokens
    )
    out, positional = [], 0
    for idx, tok in enumerate(tokens):
        if idx == 0:
            continue
        if tok.startswith("-") and tok != "-":
            continue
        if tok in REDIR_TOKENS or tok == "|":
            continue
        positional += 1
        if skip_first and positional == 1:
            continue
        out.append(tok)
    return out


def judge_bash(command, patterns):
    for segment in split_top(command, ["&&", "||", ";", "\n"]):
        if not segment.strip():
            continue
        parsed = []
        for stage in split_top(segment, ["|"]):
            if not stage.strip():
                continue
            tokens = tokenise(stage)
            if not tokens:
                continue
            verb = stage_verb(tokens)
            targets = redirect_targets(tokens)
            hits = []
            for tok in path_candidates(tokens, verb):
                if normalise(tok) in targets:
                    continue  # written TO, not read
                name = matched_name(tok, patterns)
                if name:
                    hits.append(name)
            parsed.append({"verb": verb, "tokens": tokens, "hits": hits})

        if not any(p["hits"] for p in parsed):
            continue  # nothing secret is read in this segment

        verbs = {p["verb"] for p in parsed}

        # A pipeline that passes the bytes through a hash emits a digest, not a
        # value. tee breaks that property by copying to stdout on the way, so a
        # pipeline containing tee gets no such allowance.
        if (verbs & HASH_VERBS) and "tee" not in verbs:
            continue

        for p in parsed:
            if not p["hits"]:
                continue
            name, verb = p["hits"][0], p["verb"]
            if verb in GREP_VERBS:
                if has_only_matching(p["tokens"]):
                    continue
                return ("BLOCK", name)
            if verb in BLOCKED_VERBS:
                return ("BLOCK", name)
            # ALLOWED_VERBS, and any verb this gate does not model, pass. The
            # gate blocks the known dump verbs; it is not a sandbox.
    return ("ALLOW", None)


# -------------------------------------------------------------------- main

mode = sys.argv[1] if len(sys.argv) > 1 else ""

try:
    payload = json.load(sys.stdin)
except Exception:
    sys.exit(3)
if not isinstance(payload, dict):
    sys.exit(3)

tool_input = payload.get("tool_input")
if not isinstance(tool_input, dict):
    sys.exit(3)

patterns = BUILTIN + extra_patterns(payload)

if mode == "read":
    target = tool_input.get("file_path")
    if not isinstance(target, str):
        verdict("ALLOW")
    name = matched_name(target, patterns)
    verdict("BLOCK", name) if name else verdict("ALLOW")

if mode == "bash":
    command = tool_input.get("command")
    if not isinstance(command, str):
        verdict("ALLOW")
    state, name = judge_bash(command, patterns)
    verdict(state, name)

if mode == "grep":
    # Absence first. The probe showed output_mode is simply not in the payload
    # when the caller omits it, and the tool's documented default is
    # files_with_matches, which prints paths and no line content.
    output_mode = tool_input.get("output_mode")
    if not isinstance(output_mode, str):
        output_mode = "files_with_matches"
    if output_mode != "content":
        # files_with_matches prints names, count prints numbers. Neither can
        # carry a value, so both stay allowed however they are aimed.
        verdict("ALLOW")
    target = tool_input.get("path")
    if isinstance(target, str):
        name = matched_name(target, patterns)
        if name:
            verdict("BLOCK", name)
    spec = tool_input.get("glob")
    if isinstance(spec, str):
        name = glob_targets_secret(spec, patterns)
        if name:
            verdict("BLOCK", name)
    verdict("ALLOW")

verdict("ALLOW")
PYEOF
)"

TOOL_NAME="$(printf '%s' "$PAYLOAD" | "$PY" -c '
import json, sys
try:
    payload = json.load(sys.stdin)
except Exception:
    sys.exit(3)
name = payload.get("tool_name")
sys.stdout.write(name if isinstance(name, str) else "")
' 2>/dev/null)"

if [ $? -ne 0 ]; then
    note "DEGRADED: hook input did not parse, so this secret-read guard did NOT run for this call"
    exit 0
fi

case "$TOOL_NAME" in
    Read) MODE="read" ;;
    Bash) MODE="bash" ;;
    Grep) MODE="grep" ;;
    *)    exit 0 ;;
esac

DECISION="$(printf '%s' "$PAYLOAD" | "$PY" -c "$PYSRC" "$MODE" 2>/dev/null)"
PARSE_RC=$?

if [ "$PARSE_RC" -ne 0 ]; then
    note "DEGRADED: hook input did not parse, so this secret-read guard did NOT run for this ${TOOL_NAME} call"
    exit 0
fi

case "$DECISION" in
    BLOCK*) ;;
    *) exit 0 ;;
esac

MATCHED="$(printf '%s' "${DECISION#BLOCK}" | tr -d '\t\r\n')"
[ -n "$MATCHED" ] || MATCHED="the matched file"

note "BLOCKED ${TOOL_NAME} of ${MATCHED}"

# Both messages below are emitted through a quoted heredoc, so every character
# of the recipes reaches stderr exactly as written. No expansion, no printf
# format interpretation: an earlier draft passed the recipe through printf as a
# format string, where bash turned the \x22 inside the regex into a literal
# quote and broke it.

if [ "$MODE" = "read" ]; then
    printf 'BLOCKED: Read of %s\n\n' "$MATCHED" >&2
    cat >&2 <<'READ_MSG'
This file can hold secret values, so it is never read whole.
Make a redacted copy first and read that.

1. Copy it with every value destroyed. Each NAME=VALUE or NAME: VALUE line
   becomes NAME=[REDACTED]; comments and blank lines survive, so the structure
   and all of the variable names are still there to read. This destroys values
   by shape and is not a name denylist, which is what the secrets policy
   requires:

     python -c 'import re,sys;p=re.compile(r"^\s*(?:export\s+)?[\x22\x27]?([A-Za-z_][A-Za-z0-9_.-]*)[\x22\x27]?\s*[:=].*");o=open(sys.argv[2],"w",encoding="utf-8");[o.write(p.sub(lambda m:m.group(1)+"=[REDACTED]",l)) for l in open(sys.argv[1],encoding="utf-8",errors="replace")];o.close()' SRC DST

2. Then Read DST.

Name DST outside the guarded shapes, for example env-redacted.txt in the
scratchpad. A name like .env.redacted matches .env.* and this gate would
refuse the copy too.

If the file is opaque key material (.pem, .pfx, .p12, id_rsa, id_ed25519) it
has no NAME=VALUE lines and the copy would tell you nothing. Identify it by
property instead:  sha256sum SRC   or   wc -c SRC
READ_MSG
    exit 2
fi

if [ "$MODE" = "grep" ]; then
    printf 'BLOCKED: this Grep would print matching lines out of %s.\n\n' "$MATCHED" >&2
    cat >&2 <<'GREP_MSG'
Content output mode prints the matching line, and in that file the line IS the
value. The other two output modes are always allowed against it, because names
and counts cannot carry a secret:

     output_mode: "files_with_matches"   prints paths
     output_mode: "count"                prints numbers

If you need to see matched text rather than whole lines, the three recipes
below apply to Grep exactly as they do to a shell command.

GREP_MSG
else
    printf 'BLOCKED: this Bash command reads %s whole.\n\n' "$MATCHED" >&2
fi
cat >&2 <<'BASH_MSG'
That file can hold secret values, so its lines are never printed to the
terminal. Use one of these three instead.

A. Analysis, on a redacted copy. Each NAME=VALUE or NAME: VALUE line becomes
   NAME=[REDACTED]; comments, blanks and every variable name survive. Values
   are destroyed by shape, not matched against a name denylist. Read DST,
   never SRC:

     python -c 'import re,sys;p=re.compile(r"^\s*(?:export\s+)?[\x22\x27]?([A-Za-z_][A-Za-z0-9_.-]*)[\x22\x27]?\s*[:=].*");o=open(sys.argv[2],"w",encoding="utf-8");[o.write(p.sub(lambda m:m.group(1)+"=[REDACTED]",l)) for l in open(sys.argv[1],encoding="utf-8",errors="replace")];o.close()' SRC DST

   Name DST outside the guarded shapes, for example env-redacted.txt in the
   scratchpad. A name like .env.redacted matches .env.* and is refused too.

B. Presence check, which prints the match and not the line:

     grep -n -o PATTERN SRC

C. Value comparison, by fingerprint, never by the value:

     sha256sum SRC
     grep '^VAR=' SRC | cut -d= -f2- | tr -d '"' | sha256sum | cut -c1-8

   Two fingerprints answer "are these the same" across variables, hosts and
   environments without either value being emitted.

Names only is always safe:  cut -d= -f1 SRC | grep -vE '^#|^$' | sort
BASH_MSG
exit 2
