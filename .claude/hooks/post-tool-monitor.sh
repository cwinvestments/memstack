#!/usr/bin/env bash
# MemStack: PostToolUse Observation Monitor
# Captures lightweight observations after Write/Edit/MultiEdit/Bash calls
# Appends to .claude/observations/YYYY-MM-DD.md (daily file)
# Always exit 0, must never block tool completion
#
# Triggered by: PostToolUse hook event (matcher: Write|Edit|MultiEdit|Bash)
#
# Input contract: Claude Code delivers hook input as a single JSON document on
# this process's STDIN. CLAUDE_TOOL_NAME and CLAUDE_TOOL_INPUT do not exist.
# This script previously read those two variables, so both expanded empty and
# every entry it wrote recorded "unknown" and "unknown call": 1053 of them
# between 2026-06-02 and 2026-08-05. The payload's shape is:
#
#   {"hook_event_name":"PostToolUse",
#    "tool_name":"Bash",
#    "tool_input":{"command":"...","description":"..."},
#    "tool_response":{...}, "session_id":"...", "cwd":"..."}
#
# tool_name is a top-level string; tool_input is the tool's own parameter
# object, so for Bash the command text is tool_input.command.
#
# Secrets: a command or an edited string can contain a credential. Only
# tool_input is ever summarised, never tool_response, and every extracted
# value is whitespace-collapsed and clipped to 120 characters (40 for an edit
# fragment) before it reaches the observation file.

set -uo pipefail

# --- Config ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
OBS_DIR="$SCRIPT_DIR/../observations"
TODAY=$(date +%Y-%m-%d 2>/dev/null || echo "unknown-date")
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S" 2>/dev/null || echo "unknown-time")
OUTFILE="$OBS_DIR/${TODAY}.md"
WORKING_DIR=$(pwd 2>/dev/null || echo "unknown")

# --- Read the hook payload from stdin ---
PAYLOAD="$(cat)"

# --- Ensure observations directory exists ---
mkdir -p "$OBS_DIR" 2>/dev/null || true

# --- Locate a JSON parser ---
PY=""
for candidate in python3 python py; do
    if command -v "$candidate" >/dev/null 2>&1; then
        PY="$candidate"
        break
    fi
done

# --- Parse the payload: line 1 is the tool name, line 2 is the summary ---
TOOL_NAME=""
SUMMARY=""

if [ -n "$PAYLOAD" ] && [ -n "$PY" ]; then
    PARSED=$(printf '%s' "$PAYLOAD" | "$PY" -c '
import json, sys


def clip(value, limit=120):
    text = " ".join(str(value or "").split())
    if len(text) > limit:
        text = text[:limit - 3] + "..."
    return text


try:
    payload = json.load(sys.stdin)
except Exception:
    sys.exit(3)

tool = payload.get("tool_name")
if not isinstance(tool, str) or not tool:
    tool = "unknown"

tool_input = payload.get("tool_input")
if not isinstance(tool_input, dict):
    tool_input = {}

if tool == "Bash":
    summary = "Command: " + clip(tool_input.get("command"))
elif tool == "Write":
    summary = "Write: " + clip(tool_input.get("file_path"))
elif tool == "Edit":
    old = clip(tool_input.get("old_string"), 40)
    summary = "Edit: " + clip(tool_input.get("file_path")) + " (changed: \"" + old + "...\")"
elif tool == "MultiEdit":
    edits = tool_input.get("edits")
    count = len(edits) if isinstance(edits, list) else 0
    summary = "MultiEdit: " + clip(tool_input.get("file_path")) + " (" + str(count) + " edits)"
else:
    summary = tool + " call"

sys.stdout.write(tool + "\n" + summary + "\n")
' 2>/dev/null) || true

    TOOL_NAME=$(printf '%s\n' "$PARSED" | sed -n '1p')
    SUMMARY=$(printf '%s\n' "$PARSED" | sed -n '2p')
fi

# Fallback when no parser is available or the payload did not parse. The tool
# name is a bounded top-level field and is safe to lift with a regex; the
# input is NOT, because without a parser there is no way to tell a key inside
# tool_input from one inside tool_response, so no value is extracted here.
if [ -z "$TOOL_NAME" ]; then
    TOOL_NAME=$(printf '%s' "$PAYLOAD" \
        | grep -oE '"tool_name"[[:space:]]*:[[:space:]]*"[A-Za-z_][A-Za-z0-9_]{0,63}"' 2>/dev/null \
        | head -1 | sed -E 's/.*"([A-Za-z_][A-Za-z0-9_]*)"$/\1/')
fi
if [ -z "$TOOL_NAME" ]; then
    TOOL_NAME="unknown"
fi
if [ -z "$SUMMARY" ]; then
    SUMMARY="$TOOL_NAME call (no parser)"
fi

# --- Append observation entry ---
# Add header if new file
if [ ! -f "$OUTFILE" ]; then
    cat >> "$OUTFILE" <<HEADER
# Observations: ${TODAY}

HEADER
fi

cat >> "$OUTFILE" <<ENTRY
### ${TIMESTAMP}: ${TOOL_NAME}
- **Summary:** ${SUMMARY}
- **Working dir:** ${WORKING_DIR}

ENTRY

exit 0
