#!/usr/bin/env bash
# MemStack v3.0 — Seal Hook (replaces skills/seal.md)
# Deterministic pre-push check: build verification + commit format + secrets scan
# Exit 0 = allow, exit 2 = block
#
# Triggered by: PreToolUse on Bash commands matching "git push"

set -euo pipefail

# --- Config ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MEMSTACK_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Detect project name from git remote or directory
PROJECT_NAME=""
if git remote get-url origin &>/dev/null; then
    PROJECT_NAME=$(basename "$(git remote get-url origin)" .git)
else
    PROJECT_NAME=$(basename "$(pwd)")
fi

# --- Check 1: Uncommitted changes (modified/staged tracked files only) ---
# Filter out untracked files (??) — they don't affect the push
if git status --porcelain 2>/dev/null | grep -qE '^[^?]'; then
    echo "SEAL: Uncommitted changes detected. Commit before pushing."
    git status --short
    exit 2
fi

# --- Check 2: Build verification ---
if [ -f "package.json" ]; then
    # Check if build script exists
    if grep -q '"build"' package.json 2>/dev/null; then
        echo "SEAL: Running build check..."
        if ! npm run build --silent 2>&1 | tail -5; then
            echo "SEAL: Build failed. Fix errors before pushing."
            exit 2
        fi
        echo "SEAL: Build passed."
    fi
elif [ -f "Makefile" ]; then
    echo "SEAL: Running make build..."
    if ! make build 2>&1 | tail -5; then
        echo "SEAL: Build failed."
        exit 2
    fi
elif [ -f "pyproject.toml" ] || [ -f "setup.py" ]; then
    echo "SEAL: Python project detected — skipping build check."
fi

# --- Check 3: Commit message format ---
# Verify last commit follows [ProjectName] format
LAST_MSG=$(git log -1 --pretty=%s 2>/dev/null || echo "")
if [ -n "$LAST_MSG" ]; then
    if ! echo "$LAST_MSG" | grep -qE '^\[.+\]'; then
        echo "SEAL: Warning — last commit doesn't follow [ProjectName] format: $LAST_MSG"
        # Warning only, don't block
    fi
fi

# --- Check 4: Secrets scan on recent commits ---
# Use grep -P (Perl regex) for \s and \x27 support; fall back to -E with POSIX classes
SECRETS_PATTERN='(api_key|api_secret|password|token|secret)\s*[:=]\s*["\x27][^\s"'\'']{8,}'
if git diff HEAD~1..HEAD --unified=0 2>/dev/null | grep -iP "$SECRETS_PATTERN" 2>/dev/null | grep -v "config.json" | head -3; then
    echo "SEAL: Possible secrets detected in recent changes. Review before pushing."
    exit 2
fi
# Fallback: simpler pattern with grep -iE for systems without grep -P
if git diff HEAD~1..HEAD --unified=0 2>/dev/null | grep -iE "(api_key|api_secret|password|token|secret)[[:space:]]*[:=][[:space:]]*[\"'][A-Za-z0-9_-]{8,}" 2>/dev/null | grep -v "config.json" | head -3; then
    echo "SEAL: Possible secrets detected in recent changes. Review before pushing."
    exit 2
fi

# --- Check 5: No .env files staged ---
if git diff --cached --name-only 2>/dev/null | grep -E '\.env'; then
    echo "SEAL: .env file detected in staged changes. Remove before pushing."
    exit 2
fi

echo "SEAL: All pre-push checks passed."
exit 0
