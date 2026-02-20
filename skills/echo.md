---
name: echo
description: "MUST use when the user asks about past sessions, wants to recall previous work, or references earlier context. Triggers on 'recall', 'last session', 'do you remember', 'what did we', 'continue from'. Searches SQLite database (primary) with markdown fallback."
---

# 🔊 Echo — Searching the Archives...
*Recall information from past CC sessions stored in memory.*

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

1. **Search SQLite database** (primary source of truth):
   ```bash
   python C:/Projects/memstack/db/memstack-db.py search "<keywords>" --project <project>
   ```
2. **Get recent sessions** for the specific project:
   ```bash
   python C:/Projects/memstack/db/memstack-db.py get-sessions <project> --limit 5
   ```
3. **Get relevant insights/decisions:**
   ```bash
   python C:/Projects/memstack/db/memstack-db.py get-insights <project>
   ```
4. **Fallback:** If SQLite returns no results, also check `memory/sessions/` and `memory/projects/` for markdown files
5. **Present findings** in a summary format:
   - Date and project name
   - What was accomplished
   - What was left pending
   - Key decisions and insights
6. **If nothing found** — say clearly: "No session logs found for [topic]. Use Diary to save future sessions."

## Inputs
- Keywords from the user's prompt (project name, feature name, date range)
- Database: `C:\Projects\memstack\db\memstack.db` (via memstack-db.py)
- Fallback: `C:\Projects\memstack\memory\` (legacy markdown files)

## Outputs
- Summary of relevant past session context
- Source type (database or markdown fallback)

## Example Usage

**User:** "Do you remember what we did on AdminStack last session?"

```
🔊 Echo — Searching the archives...

Found in DB: AdminStack session 2026-02-18
  - Built CC Monitor page with session cards, auto-refresh, notifications
  - Created /api/cc-sessions CRUD + public report endpoint
  - 4 commits pushed to main
  - Status: Completed, no pending items

Insights (3):
  - Used SWR for auto-refresh instead of polling
  - API key validation via HMAC-SHA256
```

## Level History

- **Lv.1** — Base: Session log search and recall. (Origin: MemStack v1.0, Feb 2026)
- **Lv.2** — Enhanced: Added YAML frontmatter, context guard, activation message. (Origin: MemStack v2.0 MemoryCore merge, Feb 2026)
- **Lv.3** — Advanced: SQLite backend as primary source, markdown as fallback, insight search. (Origin: MemStack v2.1 Accomplish-inspired upgrade, Feb 2026)
