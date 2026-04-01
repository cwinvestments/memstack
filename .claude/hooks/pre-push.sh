#!/usr/bin/env bash
# MemStack v3.3.3 — Pre-Push Hook
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
# Verify last commit follows [ProjectName] or conventional commit format
# Valid: [ProjectName] description  OR  type(scope): description  OR  type: description
LAST_MSG=$(git log -1 --pretty=%s 2>/dev/null || echo "")
if [ -n "$LAST_MSG" ]; then
    if ! echo "$LAST_MSG" | grep -qE '^\[.+\]|^(feat|fix|docs|refactor|style|test|chore)(\(.+\))?:'; then
        echo "SEAL: Warning — last commit doesn't follow [ProjectName] or conventional format: $LAST_MSG"
        # Warning only, don't block
    fi
fi

# --- Check 4: Secrets scan (production-grade, 700+ patterns) ---
GITLEAKS_BIN=""
for candidate in \
    "gitleaks" \
    "$HOME/AppData/Local/Microsoft/WinGet/Packages/Gitleaks.Gitleaks_Microsoft.Winget.Source_8wekyb3d8bbwe/gitleaks.exe" \
    "$HOME/scoop/shims/gitleaks.exe" \
    "$HOME/go/bin/gitleaks.exe"; do
    if command -v "$candidate" &>/dev/null || [ -x "$candidate" ]; then
        GITLEAKS_BIN="$candidate"
        break
    fi
done

if [ -n "$GITLEAKS_BIN" ]; then
    GITLEAKS_OUTPUT=$("$GITLEAKS_BIN" detect --source . --no-git --redact --exit-code 1 2>&1) || {
        echo "SEAL: Secrets detected in working tree:"
        echo "$GITLEAKS_OUTPUT" | head -30
        echo "SEAL: Fix the above before pushing."
        exit 2
    }
else
    # Fallback: basic regex scan if production scanner not installed
    SECRETS_PATTERN='(api_key|api_secret|password|token|secret)\s*[:=]\s*["\x27][^\s"'\'']{8,}'
    if git diff HEAD~1..HEAD --unified=0 2>/dev/null | grep -iP "$SECRETS_PATTERN" 2>/dev/null | grep -v "config.json" | head -3; then
        echo "SEAL: Possible secrets detected in recent changes. Review before pushing."
        exit 2
    fi
    if git diff HEAD~1..HEAD --unified=0 2>/dev/null | grep -iE "(api_key|api_secret|password|token|secret)[[:space:]]*[:=][[:space:]]*[\"'][A-Za-z0-9_-]{8,}" 2>/dev/null | grep -v "config.json" | head -3; then
        echo "SEAL: Possible secrets detected in recent changes. Review before pushing."
        exit 2
    fi
fi

# --- Check 5: No .env files in unpushed commits ---
UPSTREAM=$(git rev-parse --abbrev-ref '@{upstream}' 2>/dev/null || echo "")
if [ -n "$UPSTREAM" ]; then
    if git diff "$UPSTREAM"..HEAD --name-only 2>/dev/null | grep -qE '(^|/)\.env'; then
        echo "SEAL: .env file detected in unpushed commits. Remove before pushing."
        exit 2
    fi
fi

echo "SEAL: All pre-push checks passed."
exit 0
