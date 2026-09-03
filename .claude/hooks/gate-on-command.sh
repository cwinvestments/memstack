#!/usr/bin/env bash
# MemStack: Hook command gate dispatcher
#
# Claude Code delivers hook input as a single JSON document on the hook
# process's STDIN. There is no CLAUDE_TOOL_INPUT environment variable: the
# registrations this script replaces gated on one, so they expanded to the
# empty string and never ran a single time. The payload's shape is:
#
#   {"hook_event_name":"PreToolUse",
#    "tool_name":"Bash",
#    "tool_input":{"command":"git push","description":"..."},
#    "session_id":"...","cwd":"...","tool_use_id":"..."}
#
# tool_name is a top-level string; tool_input is the tool's own parameter
# object, so for Bash the command text is tool_input.command.
#
# This script reads that payload, extracts tool_input.command, and runs the
# target script only when the command contains PATTERN as a literal substring,
# the semantics the previous grep-based registration intended.
#
# Usage:
#   gate-on-command.sh [--critical] PATTERN SCRIPT
#
#   PATTERN     literal substring to look for in the Bash command
#   SCRIPT      script to run on a match; a bare name resolves beside this
#               file, a name containing a slash is used as given
#   --critical  mark this gate as a security check: when the gate cannot run
#               (no python, unparseable payload) say so on stderr instead of
#               skipping silently, because a silent no-op is the exact defect
#               this script exists to repair
#
# Exit codes: on a match, the target script's own exit code, unchanged: 2
# blocks the tool call. Everything else exits 0, so a gate that cannot make a
# decision fails open and never blocks work on a parsing problem.
#
# stdin is consumable only once and this script consumes it. That is safe
# because none of the target scripts read stdin; they infer everything from
# git. The target is additionally run with stdin on /dev/null so no child of
# it can block waiting for input.
#
# The gate never logs the command text. A Bash command can contain a
# credential, and the secrets policy forbids emitting one. Only the pattern
# and the target script name are recorded.

set -uo pipefail

CRITICAL=0
if [ "${1:-}" = "--critical" ]; then
    CRITICAL=1
    shift
fi

PATTERN="${1:-}"
TARGET="${2:-}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$SCRIPT_DIR/../observations"

# One line to stderr, and the same line to the gate log when one can be
# written. The log is what makes a fired gate provable after the fact.
note() {
    printf 'gate-on-command: %s\n' "$1" >&2
    local stamp day
    stamp="$(date -u '+%Y-%m-%dT%H:%M:%SZ' 2>/dev/null || echo unknown-time)"
    day="$(date -u '+%Y-%m-%d' 2>/dev/null || echo unknown-date)"
    if mkdir -p "$LOG_DIR" 2>/dev/null; then
        printf '%s  %s\n' "$stamp" "$1" >> "$LOG_DIR/gates-${day}.log" 2>/dev/null
    fi
    return 0
}

if [ -z "$PATTERN" ] || [ -z "$TARGET" ]; then
    note "misconfigured registration: expected [--critical] PATTERN SCRIPT"
    exit 0
fi

case "$TARGET" in
    */*) TARGET_PATH="$TARGET" ;;
    *)   TARGET_PATH="$SCRIPT_DIR/$TARGET" ;;
esac

if [ ! -f "$TARGET_PATH" ]; then
    note "target script not found, [$PATTERN] gate did not run: $TARGET"
    exit 0
fi

PAYLOAD="$(cat)"

PY=""
for candidate in python3 python py; do
    if command -v "$candidate" >/dev/null 2>&1; then
        PY="$candidate"
        break
    fi
done

if [ -z "$PY" ]; then
    if [ "$CRITICAL" -eq 1 ]; then
        note "no python interpreter, so hook input cannot be parsed and the [$PATTERN] gate ($TARGET) did NOT run for this command"
    fi
    exit 0
fi

COMMAND="$(printf '%s' "$PAYLOAD" | "$PY" -c '
import json, sys
try:
    payload = json.load(sys.stdin)
except Exception:
    sys.exit(3)
tool_input = payload.get("tool_input")
if not isinstance(tool_input, dict):
    sys.exit(3)
command = tool_input.get("command")
sys.stdout.write(command if isinstance(command, str) else "")
' 2>/dev/null)"
PARSE_RC=$?

if [ "$PARSE_RC" -ne 0 ]; then
    if [ "$CRITICAL" -eq 1 ]; then
        note "hook input did not parse, so the [$PATTERN] gate ($TARGET) did NOT run for this command"
    fi
    exit 0
fi

# Literal substring test. A case pattern is used rather than grep so that no
# character in PATTERN is treated as a regular expression.
case "$COMMAND" in
    *"$PATTERN"*) ;;
    *) exit 0 ;;
esac

note "matched [$PATTERN], running $TARGET"

exec bash "$TARGET_PATH" < /dev/null
