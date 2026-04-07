#!/usr/bin/env bash
# MemStack v3.2 — Session End Hook
# Reports session completion to monitoring webhook
# Always exit 0 — monitoring should never block work
#
# Triggered by: Stop hook event

set -uo pipefail

# External webhook: opt-in only via MEMSTACK_DEVLOG_WEBHOOK env var
if [ -z "${MEMSTACK_DEVLOG_WEBHOOK:-}" ]; then
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
JSON_BODY=$(printf '{"session_name":"CC Session","project":"%s","status":"completed","last_output":"Session ended"}' \
    "$(printf '%s' "$PROJECT_NAME" | sed 's/["\]/\\&/g')")
curl -s -m 5 -X POST "$MEMSTACK_DEVLOG_WEBHOOK" \
    -H "Content-Type: application/json" \
    -d "$JSON_BODY" >/dev/null 2>&1 || true

exit 0
