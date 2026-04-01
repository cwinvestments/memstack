#!/usr/bin/env bash
# MemStack v3.3.3 — Pre-Commit Secrets Hook
# Scans staged files for secrets before any commit
# Exit 0 = allow, exit 2 = block
#
# Triggered by: PreToolUse on Bash commands matching "git commit"

set -uo pipefail

# --- Config ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# --- Locate secrets scanner ---
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
    GITLEAKS_OUTPUT=$("$GITLEAKS_BIN" protect --staged --redact --exit-code 1 2>&1) || {
        echo "SEAL: Secrets detected in staged files:"
        echo "$GITLEAKS_OUTPUT" | head -30
        echo "SEAL: Remove secrets before committing."
        exit 2
    }
else
    # Fallback: basic regex scan on staged diff
    STAGED_DIFF=$(git diff --cached --unified=0 2>/dev/null)
    if [ -n "$STAGED_DIFF" ]; then
        SECRETS_PATTERN='(api_key|api_secret|password|token|secret)\s*[:=]\s*["\x27][^\s"'\'']{8,}'
        if echo "$STAGED_DIFF" | grep -iP "$SECRETS_PATTERN" 2>/dev/null | grep -v "config.json" | head -3; then
            echo "SEAL: Possible secrets detected in staged changes. Review before committing."
            exit 2
        fi
        if echo "$STAGED_DIFF" | grep -iE "(api_key|api_secret|password|token|secret)[[:space:]]*[:=][[:space:]]*[\"'][A-Za-z0-9_-]{8,}" 2>/dev/null | grep -v "config.json" | head -3; then
            echo "SEAL: Possible secrets detected in staged changes. Review before committing."
            exit 2
        fi
    fi
fi

exit 0
