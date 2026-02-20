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

| Context | Status | Priority |
|---------|--------|----------|
| **User says "save diary", "log session", "write diary"** | ACTIVE — write diary | P1 |
| **User explicitly says they're done ("that's it", "wrapping up")** | ACTIVE — suggest diary if work was done | P2 |
| **Mid-session, user is actively coding** | DORMANT — don't interrupt flow | — |
| **Casual conversation, no code changes made** | DORMANT — nothing to log | — |
| **User asks to recall past sessions ("what did we do")** | DORMANT — Echo handles recall, not Diary | — |
| **User says "save project" or "handoff"** | DORMANT — Project skill handles this | — |
| **Session just started, no work yet** | DORMANT — nothing to log | — |

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

4. **Save to SQLite database** (primary storage):
   ```bash
   python C:/Projects/memstack/db/memstack-db.py add-session '{"project":"<name>","date":"<YYYY-MM-DD>","accomplished":"<bullets>","files_changed":"<bullets>","commits":"<bullets>","decisions":"<bullets>","problems":"<bullets>","next_steps":"<bullets>","duration":"<estimate>","raw_markdown":"<full text>"}'
   ```

5. **Also save decisions as insights** for cross-project search:
   ```bash
   python C:/Projects/memstack/db/memstack-db.py add-insight '{"project":"<name>","type":"decision","content":"<decision>","context":"Session <date>","tags":"<project>"}'
   ```

6. **Update project context** with last session date:
   ```bash
   python C:/Projects/memstack/db/memstack-db.py set-context '{"project":"<name>","last_session_date":"<YYYY-MM-DD>"}'
   ```

7. **Also save markdown copy** to `memory/sessions/{date}-{project}.md` (export format, human-readable backup)

## Session File Size Management

The 500-line limit on markdown files is no longer a concern since SQLite is the source of truth.
Markdown files in `memory/sessions/` are now just human-readable exports.
Old markdown files are preserved but not the primary storage.

## Inputs
- Current session context
- Project name from working directory or config.json
- Git log for commit history

## Outputs
- Session entry in SQLite database
- Insights extracted from decisions
- Markdown backup in memory/sessions/
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
- **Lv.3** — Advanced: SQLite as primary storage, auto-extract insights from decisions, markdown as backup export. (Origin: MemStack v2.1 Accomplish-inspired upgrade, Feb 2026)
