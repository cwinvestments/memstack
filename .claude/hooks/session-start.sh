#!/usr/bin/env bash
# MemStack v3.0-rc — Session Start Hook
# 1. Headroom proxy auto-detection and auto-start
# 2. Auto-indexes CLAUDE.md into SQLite project_context
# 3. Reports session start to monitoring API
# Always exit 0 — should never block work
#
# Triggered by: SessionStart hook event

set -uo pipefail

# --- Find MemStack root ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MEMSTACK_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# --- Read Headroom config ---
HEADROOM_PORT=8787
HEADROOM_AUTO_START=true
CONFIG_FILE=""
if [ -f "$MEMSTACK_ROOT/config.local.json" ]; then
    CONFIG_FILE="$MEMSTACK_ROOT/config.local.json"
elif [ -f "$MEMSTACK_ROOT/config.json" ]; then
    CONFIG_FILE="$MEMSTACK_ROOT/config.json"
fi

if [ -n "$CONFIG_FILE" ]; then
    PYTHON_CONFIG="$CONFIG_FILE"
    if command -v cygpath &>/dev/null; then
        PYTHON_CONFIG=$(cygpath -w "$CONFIG_FILE")
    fi
    read -r HEADROOM_PORT HEADROOM_AUTO_START <<< $(python -c "
import json
try:
    with open(r'$PYTHON_CONFIG') as f:
        cfg = json.load(f)
    h = cfg.get('headroom', {})
    print(h.get('port', 8787), str(h.get('auto_start', True)).lower())
except:
    print('8787 true')
" 2>/dev/null || echo "8787 true")
fi

# --- Headroom proxy auto-detection ---
# Check if Headroom is already running, auto-start if installed and configured
if [ "$HEADROOM_AUTO_START" = "true" ]; then
    HEADROOM_URL="http://127.0.0.1:${HEADROOM_PORT}"

    if curl -s -m 2 "${HEADROOM_URL}/health" >/dev/null 2>&1; then
        # Headroom already running — nothing to do
        :
    elif command -v headroom &>/dev/null; then
        # Headroom installed but not running — auto-start
        headroom proxy --port "$HEADROOM_PORT" >/dev/null 2>&1 &
        sleep 2
        if curl -s -m 2 "${HEADROOM_URL}/health" >/dev/null 2>&1; then
            export ANTHROPIC_BASE_URL="${HEADROOM_URL}"
        fi
    fi
    # If headroom not installed, skip silently
fi

# --- Detect project ---
PROJECT_NAME=""
if git remote get-url origin &>/dev/null; then
    PROJECT_NAME=$(basename "$(git remote get-url origin)" .git)
else
    PROJECT_NAME=$(basename "$(pwd)")
fi

# --- Auto-index CLAUDE.md into SQLite ---
# If CLAUDE.md exists in the working directory, extract key facts and store in project_context
CLAUDE_MD=""
for candidate in "CLAUDE.md" "*-CLAUDE.md" "claude.md"; do
    found=$(ls $candidate 2>/dev/null | head -1)
    if [ -n "$found" ]; then
        CLAUDE_MD="$found"
        break
    fi
done

if [ -n "$CLAUDE_MD" ] && [ -n "$PROJECT_NAME" ]; then
    PYTHON_CLAUDE_MD="$CLAUDE_MD"
    PYTHON_DB_SCRIPT="$MEMSTACK_ROOT/db/memstack-db.py"
    if command -v cygpath &>/dev/null; then
        PYTHON_CLAUDE_MD=$(cygpath -w "$CLAUDE_MD")
        PYTHON_DB_SCRIPT=$(cygpath -w "$PYTHON_DB_SCRIPT")
    fi
    python -c "
import json, subprocess, sys, re

# Read and extract key facts from CLAUDE.md
try:
    with open(r'$PYTHON_CLAUDE_MD', encoding='utf-8') as f:
        content = f.read()
except:
    sys.exit(0)

# Extract headings and their first paragraph (max ~1500 chars total)
sections = []
for match in re.finditer(r'^#{1,3}\s+(.+?)$\n(.*?)(?=\n#{1,3}\s|\Z)', content, re.MULTILINE | re.DOTALL):
    heading = match.group(1).strip()
    body = match.group(2).strip()[:200]
    if body:
        sections.append(f'{heading}: {body}')
summary = '\n'.join(sections)[:1500] if sections else content[:1500]

# Store via memstack-db.py set-context
ctx = json.dumps({
    'project': '$PROJECT_NAME',
    'architecture_decisions': summary,
    'status': 'active'
})
subprocess.run(
    ['python', r'$PYTHON_DB_SCRIPT', 'set-context', ctx],
    capture_output=True, timeout=10
)
" 2>/dev/null || true
fi

# --- Report session start to monitoring API ---
if [ -n "$CONFIG_FILE" ]; then
    read -r API_URL API_KEY <<< $(python -c "
import json
try:
    with open(r'$PYTHON_CONFIG') as f:
        cfg = json.load(f)
    m = cfg.get('cc_monitor', {})
    print(m.get('api_url', ''), m.get('api_key', ''))
except:
    print(' ')
" 2>/dev/null || echo " ")

    if [ -n "$API_KEY" ] && [ "$API_KEY" != " " ]; then
        curl -s -m 5 -X POST "$API_URL" \
            -H "Content-Type: application/json" \
            -d "{
                \"api_key\": \"$API_KEY\",
                \"session_name\": \"CC Session\",
                \"project\": \"$PROJECT_NAME\",
                \"status\": \"working\",
                \"last_output\": \"Session started\"
            }" >/dev/null 2>&1 || true
    fi
fi

exit 0
