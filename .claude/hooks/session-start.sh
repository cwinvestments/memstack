#!/usr/bin/env bash
# MemStack v3.9.6: Session Start Hook, side effects only.
#
# This script writes NOTHING to stdout. It injects no session context.
#
# Why, 2026-09-03: the plugin's own hooks/session-start is the single source of
# SessionStart context injection. Until this release both hooks were registered
# at once and both emitted an additionalContext payload, and the skill-loader
# block inside them was byte identical: 1,370 bytes delivered twice, plus a
# project-detection line restating the same fact in different words, for 1,462
# bytes of duplicated context per session. The plugin's copy also carries the
# secrets policy, living memory, the update-staleness advisory and the
# core.hooksPath check, none of which existed here, so this copy was the one to
# stop emitting.
#
# What this script still owns, because the plugin hook does not do it:
#   1. Auto-indexes CLAUDE.md into the SQLite project_context table.
#   2. Prints the Pro nudge on stderr when no license key is set.
#
# The personal blog-queue webhook ping was removed in 3.9.6. It was a personal
# automation that should never have shipped; its poster script now lives outside
# every repo, under the user's own ~/.memstack/tools directory.
#
# Note: the TokenStack proxy is started on demand via
#       'python -m memstack_skill_loader dashboard --with-proxy', not by this hook.
# Always exit 0: should never block work
#
# Triggered by: SessionStart hook event

set -uo pipefail

# --- Find MemStack root ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MEMSTACK_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

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

# Pro info (stderr: this hook writes nothing to stdout at all)
if [ -z "${MEMSTACK_PRO_LICENSE_KEY:-}" ]; then
  echo "MemStack Pro: 44 additional skills available. Details at memstack.pro" >&2
fi

exit 0
