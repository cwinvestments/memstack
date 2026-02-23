---
name: echo
description: "Memory recall from past sessions. Uses MemSearch vector-powered semantic search with SQLite fallback. Triggers on recall, last session, do you remember."
---


# 🔊 Echo — Searching the Archives...
*Recall information from past CC sessions using semantic vector search.*

## Activation

When this skill activates, output:

`🔊 Echo — Searching the archives...`

Then execute the protocol below.

## Context Guard

| Context | Status | Priority |
|---------|--------|----------|
| **User says "recall", "remember", "last session", "what did we"** | ACTIVE — search memory | P1 |
| **User asks about past work explicitly ("did we build X?")** | ACTIVE — search memory | P1 |
| **User says "continue from" or "resume" a past topic** | ACTIVE — search memory | P2 |
| **User is describing NEW work to do ("build X", "add Y")** | DORMANT — this is new work, not recall | — |
| **User mentions "memory" in code context (RAM, variables)** | DORMANT — technical term, not MemStack recall | — |
| **User mentions a project name in present tense ("work on X")** | DORMANT — forward-looking, not recall | — |
| **User says "save" or "log" (Diary/Project territory)** | DORMANT — Diary or Project skill handles writing | — |

## Protocol

### Step 1: Semantic Vector Search (primary)

Try MemSearch first for best-quality results:
```bash
python C:/Projects/memstack/skills/echo/search.py "<keywords>" --top-k 5
```

If this returns results, present them with scores, dates, and source files.

### Step 2: SQLite Keyword Search (augment or fallback)

Always run SQLite search to supplement vector results or as fallback if Step 1 fails:
```bash
python C:/Projects/memstack/db/memstack-db.py search "<keywords>" --project <project>
```

### Step 3: Recent Sessions and Insights

For additional context:
```bash
python C:/Projects/memstack/db/memstack-db.py get-sessions <project> --limit 5
python C:/Projects/memstack/db/memstack-db.py get-insights <project>
```

### Step 4: Markdown Fallback

If both vector and SQLite return nothing, check `memory/sessions/` and `memory/projects/` for markdown files.

### Step 5: Present Findings

Combine and deduplicate results from all sources:
- **Vector results**: Show with similarity scores and section headings
- **SQLite results**: Show with dates and accomplishment summaries
- **Source attribution**: Always show which source (vector/SQLite/markdown) each result came from
- Date and project name
- What was accomplished
- What was left pending
- Key decisions and insights

### Step 6: No Results

If nothing found across all sources — say clearly: "No session logs found for [topic]. Use Diary to save future sessions."

## Indexing

To re-index sessions after new diary entries (normally done automatically):
```bash
python C:/Projects/memstack/skills/echo/index-sessions.py
```

Use `--force` to re-embed all content (e.g., after changing embedding model):
```bash
python C:/Projects/memstack/skills/echo/index-sessions.py --force
```

## Inputs
- Keywords from the user's prompt (project name, feature name, date range)
- Vector DB: `C:\Projects\memstack\memory\vectors\memsearch.db` (via MemSearch)
- Database: `C:\Projects\memstack\db\memstack.db` (via memstack-db.py)
- Fallback: `C:\Projects\memstack\memory\` (legacy markdown files)

## Outputs
- Ranked results with semantic similarity scores
- Source type attribution (vector, database, or markdown fallback)
- Summary of relevant past session context

## Example Usage

**User:** "Do you remember what we did on AdminStack last session?"

```
🔊 Echo — Searching the archives...

Vector search (top 3):
  [1] AdminStack — 2026-02-18 (session)
      Section: Accomplished
      Score: 0.912
      Built CC Monitor page with session cards, auto-refresh, notifications.
      Created /api/cc-sessions CRUD + public report endpoint.

  [2] AdminStack — 2026-02-17 (session)
      Section: Decisions
      Score: 0.847
      Used SWR for auto-refresh instead of polling. API key via HMAC-SHA256.

  [3] AdminStack — 2026-02-18 (session)
      Section: Next Steps
      Score: 0.791
      Deploy dashboard, add notification preferences, test mobile view.

SQLite insights (3):
  - [decision] Used SWR for auto-refresh instead of polling
  - [decision] API key validation via HMAC-SHA256
  - [pattern] Next.js App Router + SWR for all dashboard pages
```

## Level History

- **Lv.1** — Base: Session log search and recall. (Origin: MemStack v1.0, Feb 2026)
- **Lv.2** — Enhanced: Added YAML frontmatter, context guard, activation message. (Origin: MemStack v2.0 MemoryCore merge, Feb 2026)
- **Lv.3** — Advanced: SQLite backend as primary source, markdown as fallback, insight search. (Origin: MemStack v2.1 Accomplish-inspired upgrade, Feb 2026)
- **Lv.4** — Native: CC rules integration (`.claude/rules/echo.md`), `/memstack-search` slash command, auto-indexed CLAUDE.md context. (Origin: MemStack v3.0-beta, Feb 2026)
- **Lv.5** — Semantic: MemSearch vector-powered recall with hybrid search (dense + BM25 + RRF). Auto-indexes sessions/plans, semantic similarity across all logs, SQLite fallback. (Origin: MemStack v3.1, Feb 2026)
