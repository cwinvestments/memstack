---
name: echo
description: "MUST use when the user asks about past sessions, wants to recall previous work, or references earlier context. Triggers on 'recall', 'last session', 'do you remember', 'what did we', 'continue from'. Searches memory/sessions/ and memory/projects/ for matching context."
---

# 🔊 Echo — Searching the Archives...
*Recall information from past CC sessions stored in memory.*

## Activation

When this skill activates, output:

`🔊 Echo — Searching the archives...`

Then execute the protocol below.

## Context Guard

| Context | Status |
|---------|--------|
| **User asks about past work or sessions** | ACTIVE — search memory |
| **User says "recall", "remember", "last session"** | ACTIVE — search memory |
| **User mentions a project by name in past tense** | ACTIVE — search memory |
| **General conversation about memory concepts** | DORMANT — do not activate |
| **User is describing NEW work to do** | DORMANT — do not activate |

## Protocol

1. **Search memory/sessions/** — look for files matching the topic or project name
2. **Search memory/projects/** — check for project state snapshots and plans
3. **Read the most recent matching files** — extract relevant context
4. **Present findings** in a summary format:
   - Date and project name
   - What was accomplished
   - What was left pending
   - Any decisions or notes recorded
5. **If nothing found** — say clearly: "No session logs found for [topic]. Use Diary to save future sessions."

## Inputs
- Keywords from the user's prompt (project name, feature name, date range)
- Memory directory: `C:\Projects\memstack\memory\`

## Outputs
- Summary of relevant past session context
- File paths to the source logs for reference

## Example Usage

**User:** "Do you remember what we did on AdminStack last session?"

```
🔊 Echo — Searching the archives...

Found: memory/sessions/2026-02-18-adminstack.md
  - Built CC Monitor page with session cards, auto-refresh, notifications
  - Created /api/cc-sessions CRUD + public report endpoint
  - 4 commits pushed to main
  - Status: Completed, no pending items
```

## Level History

- **Lv.1** — Base: Session log search and recall. (Origin: MemStack v1.0, Feb 2026)
- **Lv.2** — Enhanced: Added YAML frontmatter, context guard, activation message. (Origin: MemStack v2.0 MemoryCore merge, Feb 2026)
