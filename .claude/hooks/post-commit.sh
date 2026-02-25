#!/usr/bin/env bash
# MemStack v3.2 — Post-Commit Hook
# Post-commit verification: debug artifact scan + secrets check
# Exit 0 = allow, exit 1 = warning (non-blocking)
#
# Triggered by: PostToolUse on Bash commands matching "git commit"

set -uo pipefail

# --- Check 1: Debug artifacts in committed files ---
COMMITTED_FILES=$(git diff-tree --no-commit-id --name-only -r HEAD 2>/dev/null || echo "")
DEBUG_HITS=""

if [ -n "$COMMITTED_FILES" ]; then
    while IFS= read -r file; do
        if [[ "$file" =~ \.(ts|tsx|js|jsx)$ ]] && [ -f "$file" ]; then
            hits=$(grep -n 'console\.log\|debugger\b' "$file" 2>/dev/null | grep -v '// keep' | grep -v '.test.' | head -5)
            if [ -n "$hits" ]; then
                DEBUG_HITS="${DEBUG_HITS}\n  $file:\n$hits"
            fi
        fi
    done <<< "$COMMITTED_FILES"
fi

if [ -n "$DEBUG_HITS" ]; then
    echo "DEPLOY: Debug artifacts found in committed files:"
    printf '%b\n' "$DEBUG_HITS"
    echo "DEPLOY: Consider removing before pushing."
    # Non-blocking warning — exit 0
fi

# --- Check 2: Secrets in committed files ---
SECRETS_FOUND=""
while IFS= read -r file; do
    if [ -f "$file" ]; then
        hits=$(grep -inP '(api_key|api_secret|password|token|secret)\s*[:=]\s*["\x27][^\s"'\'']{8,}' "$file" 2>/dev/null || grep -inE '(api_key|api_secret|password|token|secret)[[:space:]]*[:=][[:space:]]*[\"'"'"'][A-Za-z0-9_-]{8,}' "$file" 2>/dev/null | head -3)
        if [ -n "$hits" ]; then
            SECRETS_FOUND="${SECRETS_FOUND}\n  $file:\n$hits"
        fi
    fi
done <<< "$COMMITTED_FILES"

if [ -n "$SECRETS_FOUND" ]; then
    echo "DEPLOY: Possible secrets in committed files:"
    printf '%b\n' "$SECRETS_FOUND"
    echo "DEPLOY: Review before pushing. Use git reset --soft HEAD~1 to undo."
    # Warning only — the commit already happened
fi

# --- Check 3: Commit message format validation ---
COMMIT_MSG=$(git log -1 --pretty=%s)
if echo "$COMMIT_MSG" | grep -qE '^\[.+\]|^(feat|fix|docs|refactor|style|test|chore)(\(.+\))?:'; then
    echo "DEPLOY: Commit format OK — $COMMIT_MSG"
else
    echo "DEPLOY: Commit message doesn't follow [Project] or conventional format: $COMMIT_MSG"
fi

exit 0
