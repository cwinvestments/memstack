#!/usr/bin/env bash
# MemStack v3.3.2 — PostToolUse Observation Monitor
# Captures lightweight observations after Write/Edit/MultiEdit/Bash calls
# Appends to .claude/observations/YYYY-MM-DD.md (daily file)
# Always exit 0 — must never block tool completion
#
# Triggered by: PostToolUse hook event (matcher: Write|Edit|MultiEdit|Bash)

set -uo pipefail

# --- Config ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
OBS_DIR="$SCRIPT_DIR/../observations"
TODAY=$(date +%Y-%m-%d 2>/dev/null || echo "unknown-date")
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S" 2>/dev/null || echo "unknown-time")
OUTFILE="$OBS_DIR/${TODAY}.md"
TOOL_NAME="${CLAUDE_TOOL_NAME:-unknown}"
TOOL_INPUT="${CLAUDE_TOOL_INPUT:-}"
WORKING_DIR=$(pwd 2>/dev/null || echo "unknown")

# --- Ensure observations directory exists ---
mkdir -p "$OBS_DIR" 2>/dev/null || true

# --- Parse tool input (JSON) for a brief summary ---
SUMMARY=""
if [ -n "$TOOL_INPUT" ]; then
    # Try python first for safe JSON parsing
    SUMMARY=$(TOOL_NAME="$TOOL_NAME" python -c "
import json, os, sys
try:
    data = json.loads(sys.stdin.read())
    tool = os.environ.get('TOOL_NAME', 'unknown')
    if tool == 'Bash':
        cmd = data.get('command', '')
        if len(cmd) > 120:
            cmd = cmd[:117] + '...'
        print(f'Command: {cmd}')
    elif tool in ('Write', 'Edit', 'MultiEdit'):
        fp = data.get('file_path', '')
        if tool == 'Write':
            print(f'Write: {fp}')
        elif tool == 'Edit':
            old = data.get('old_string', '')[:40]
            print(f'Edit: {fp} (changed: \"{old}...\")')
        elif tool == 'MultiEdit':
            fp = data.get('file_path', '')
            edits = data.get('edits', [])
            print(f'MultiEdit: {fp} ({len(edits)} edits)')
        else:
            print(f'{tool}: {fp}')
    else:
        print(f'{tool} call')
except Exception as e:
    tool = os.environ.get('TOOL_NAME', 'unknown')
    print(f'{tool} call (parse error)')
" <<< "$TOOL_INPUT" 2>/dev/null) || true

    # Fallback if python fails: extract file_path or command via grep
    if [ -z "$SUMMARY" ]; then
        SUMMARY=$(echo "$TOOL_INPUT" | grep -oP '"(?:file_path|command)"\s*:\s*"[^"]{0,120}' 2>/dev/null | head -1 || echo "$TOOL_NAME call")
    fi
fi

# Final fallback
if [ -z "$SUMMARY" ]; then
    SUMMARY="$TOOL_NAME call"
fi

# --- Append observation entry ---
# Add header if new file
if [ ! -f "$OUTFILE" ]; then
    cat >> "$OUTFILE" <<HEADER
# Observations — ${TODAY}

HEADER
fi

cat >> "$OUTFILE" <<ENTRY
### ${TIMESTAMP} — ${TOOL_NAME}
- **Summary:** ${SUMMARY}
- **Working dir:** ${WORKING_DIR}

ENTRY

exit 0
