#!/usr/bin/env bash
# MemStack v3.3.2 — SessionStart Context Loader
# Injects a brief context summary from recent diary + observation files
# into .claude/session-context.md for CC to read at session start
# Always exit 0 — must never block session startup
#
# Triggered by: SessionStart hook event

set -uo pipefail

# --- Config ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PROJECT_DIR="$(cd "$CLAUDE_DIR/.." && pwd)"
DIARY_DIR="$CLAUDE_DIR/diary"
OBS_DIR="$CLAUDE_DIR/observations"
SESSIONS_DIR="$PROJECT_DIR/memory/sessions"
OUTFILE="$CLAUDE_DIR/session-context.md"
MAX_LINES=200
TODAY=$(date "+%Y-%m-%d %H:%M:%S" 2>/dev/null || echo "unknown")

# --- Collect diary entries (last 3, newest first) ---
# Check .claude/diary/ first, fall back to memory/sessions/
DIARY_CONTENT=""
DIARY_COUNT=0

get_recent_files() {
    local dir="$1"
    local count="$2"
    if [ -d "$dir" ]; then
        ls -t "$dir"/*.md 2>/dev/null | head -"$count"
    fi
}

# Try .claude/diary/ first, then memory/sessions/
DIARY_FILES=$(get_recent_files "$DIARY_DIR" 3)
if [ -z "$DIARY_FILES" ]; then
    DIARY_FILES=$(get_recent_files "$SESSIONS_DIR" 3)
fi

if [ -n "$DIARY_FILES" ]; then
    while IFS= read -r file; do
        [ -z "$file" ] && continue
        FNAME=$(basename "$file" 2>/dev/null || echo "unknown")
        DIARY_CONTENT="${DIARY_CONTENT}
- ${FNAME}"
        DIARY_COUNT=$((DIARY_COUNT + 1))
    done <<< "$DIARY_FILES"
    DIARY_CONTENT="${DIARY_CONTENT}

> Diary entries available. Use \`cat .claude/diary/<filename>\` to read if needed."
fi

# --- Collect observation files (last 3, newest first) ---
OBS_CONTENT=""
OBS_COUNT=0

OBS_FILES=$(get_recent_files "$OBS_DIR" 3)

if [ -n "$OBS_FILES" ]; then
    while IFS= read -r file; do
        [ -z "$file" ] && continue
        FNAME=$(basename "$file" 2>/dev/null || echo "unknown")
        # Extract last 20 entries (tail of file — most recent observations)
        EXCERPT=$(tail -60 "$file" 2>/dev/null || echo "(unreadable)")
        OBS_CONTENT="${OBS_CONTENT}
#### ${FNAME}
\`\`\`
${EXCERPT}
\`\`\`

"
        OBS_COUNT=$((OBS_COUNT + 1))
    done <<< "$OBS_FILES"
fi

# --- Assemble context summary ---
# Write to temp file first, then move (atomic-ish on most systems)
TMPFILE="${OUTFILE}.tmp.$$"

cat > "$TMPFILE" <<HEADER
# Session Context — Auto-Generated
> Injected by session-context-load.sh at ${TODAY}
> Sources: ${DIARY_COUNT} diary entries, ${OBS_COUNT} observation files

---

HEADER

# --- Diary section ---
if [ -n "$DIARY_CONTENT" ]; then
    cat >> "$TMPFILE" <<SECTION
## Recent Diary Entries (last ${DIARY_COUNT})

${DIARY_CONTENT}
---

SECTION
else
    cat >> "$TMPFILE" <<SECTION
## Recent Diary Entries

> No diary entries found in .claude/diary/ or memory/sessions/

---

SECTION
fi

# --- Observations section ---
if [ -n "$OBS_CONTENT" ]; then
    cat >> "$TMPFILE" <<SECTION
## Recent Observations (last ${OBS_COUNT})

${OBS_CONTENT}
SECTION
else
    cat >> "$TMPFILE" <<SECTION
## Recent Observations

> No observation files found in .claude/observations/

SECTION
fi

# --- Enforce max line limit ---
TOTAL_LINES=$(wc -l < "$TMPFILE" 2>/dev/null || echo "0")
if [ "$TOTAL_LINES" -gt "$MAX_LINES" ] 2>/dev/null; then
    head -$((MAX_LINES - 2)) "$TMPFILE" > "${TMPFILE}.trimmed"
    echo "" >> "${TMPFILE}.trimmed"
    echo "> (Truncated to ${MAX_LINES} lines)" >> "${TMPFILE}.trimmed"
    mv "${TMPFILE}.trimmed" "$TMPFILE" 2>/dev/null || true
fi

# --- Move into place (idempotent — overwrites previous) ---
mv "$TMPFILE" "$OUTFILE" 2>/dev/null || {
    # Fallback: direct copy if mv fails
    cp "$TMPFILE" "$OUTFILE" 2>/dev/null || true
    rm -f "$TMPFILE" 2>/dev/null || true
}

exit 0
