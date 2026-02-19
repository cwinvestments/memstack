---
name: diary
description: "MUST use when documenting session accomplishments, logging what was built, or at the end of any productive session. Triggers on 'save diary', 'write diary', 'log session'. Auto-activates at session end if auto_diary is true in config.json. Creates searchable logs for Echo."
---

# 📓 Diary — Logging Session...
*Document what was accomplished in each CC session for future recall.*

## Activation

When this skill activates, output:

`📓 Diary — Logging session...`

Then execute the protocol below.

## Context Guard

| Context | Status |
|---------|--------|
| **User says "save diary" or "log session"** | ACTIVE — write diary |
| **Session ending with productive work done** | ACTIVE — auto-diary |
| **Task completed and user is wrapping up** | ACTIVE — suggest diary |
| **Mid-session, user is actively working** | DORMANT — do not interrupt |
| **Casual conversation, no work done** | DORMANT — nothing to log |

## Protocol

1. **Summarize the session:**
   - Project name and working directory
   - Date and approximate duration
   - What was built or changed
   - Key files created or modified
   - Commits made (hashes and messages)
   - Decisions made and why
   - Problems encountered and solutions

2. **Check git log** for commits:
   ```bash
   git log --oneline -10
   ```

3. **Format the diary entry:**
   ```markdown
   # Session Diary — {project} — {date}

   ## Accomplished
   - Item 1...

   ## Files Changed
   - path/to/file.ts — description

   ## Commits
   - abc1234 Message

   ## Decisions
   - Decision: reason

   ## Next Steps
   - What to do next
   ```

4. **Save to** `memory/sessions/{date}-{project}.md`

## Session File Size Management

Session logs in `memory/sessions/` have a **500-line limit** per file.

When a session log approaches 500 lines:
1. Create a recap summary (5-10 lines) capturing key accomplishments, decisions, and next steps
2. Move the full log to `memory/sessions/archive/{original-filename}`
3. Start a fresh log file with only the recap block for continuity

This prevents stale context from bloating the context window. The archive preserves full history for Echo to search later.

## Inputs
- Current session context
- Project name from working directory or config.json
- Git log for commit history

## Outputs
- Session diary file in memory/sessions/
- Brief confirmation summary

## Example Usage

**User:** "save diary"

```
📓 Diary — Logging session...

Saved: memory/sessions/2026-02-18-adminstack.md

Project: AdminStack | Duration: ~2 hours
Accomplished: Built CC Monitor page, API routes, setup guide
Commits: 4 (45b4c42, d1c7e11, f6c8e18, f0e793f)
Files changed: 8

This session is now searchable via Echo.
```

## Level History

- **Lv.1** — Base: Session logging with git integration. (Origin: MemStack v1.0, Feb 2026)
- **Lv.2** — Enhanced: Added YAML frontmatter, context guard, 500-line limit with archive, activation message. (Origin: MemStack v2.0 MemoryCore merge, Feb 2026)
