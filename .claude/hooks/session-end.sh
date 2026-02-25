#!/usr/bin/env bash
# MemStack v3.2 — Session End Hook
# Reports session completion to monitoring API
# Always exit 0 — monitoring should never block work
#
# Triggered by: Stop hook event

set -uo pipefail

# --- Find config ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MEMSTACK_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

CONFIG_FILE=""
if [ -f "$MEMSTACK_ROOT/config.local.json" ]; then
    CONFIG_FILE="$MEMSTACK_ROOT/config.local.json"
elif [ -f "$MEMSTACK_ROOT/config.json" ]; then
    CONFIG_FILE="$MEMSTACK_ROOT/config.json"
else
    exit 0
fi

# --- Read API config ---
# Convert MSYS paths to Windows paths for Python compatibility
PYTHON_CONFIG="$CONFIG_FILE"
if command -v cygpath &>/dev/null; then
    PYTHON_CONFIG=$(cygpath -w "$CONFIG_FILE")
fi
read -r API_URL API_KEY <<< $(python -c "
import json, sys
try:
    with open(r'$PYTHON_CONFIG') as f:
        cfg = json.load(f)
    m = cfg.get('cc_monitor', {})
    print(m.get('api_url', ''), m.get('api_key', ''))
except:
    print(' ')
" 2>/dev/null || echo " ")

if [ -z "$API_KEY" ] || [ "$API_KEY" = " " ]; then
    exit 0
fi

# --- Detect project ---
PROJECT_NAME=""
if git remote get-url origin &>/dev/null; then
    PROJECT_NAME=$(basename "$(git remote get-url origin)" .git)
else
    PROJECT_NAME=$(basename "$(pwd)")
fi

# --- Report session end ---
curl -s -m 5 -X POST "$API_URL" \
    -H "Content-Type: application/json" \
    -d "{
        \"api_key\": \"$API_KEY\",
        \"session_name\": \"CC Session\",
        \"project\": \"$PROJECT_NAME\",
        \"status\": \"completed\",
        \"last_output\": \"Session ended\"
    }" >/dev/null 2>&1 || true

exit 0
