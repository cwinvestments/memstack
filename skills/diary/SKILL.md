---
name: diary
description: "Use when the user says 'save diary', 'log session', 'wrapping up', or at end of a productive session."
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

## Anti-Rationalization

If you're thinking any of these, STOP — you're about to skip the protocol:

| You're thinking... | Reality |
|---|---|
| "Nothing important happened this session" | Every session has decisions, even small ones. Log them. |
| "I'll remember this for next time" | You won't. You don't persist. The database does. Write the diary. |
| "The user didn't ask me to log this" | The rule says log at session end. You don't need explicit permission. |
| "This was just a quick fix, not worth logging" | Quick fixes contain decisions ("why this approach?"). Future you needs that context. |
| "I already committed, so the work is saved" | Commits don't capture decisions, blockers, or next steps. The diary does. |
| "The Session Handoff section isn't needed" | Handoffs are the most valuable part. Always include in-progress work and pickup instructions. |

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

   ## Session Handoff
   **In Progress:** [what was actively being worked on when session ended]
   **Uncommitted Changes:** [list any unstaged/uncommitted work, or "None"]
   **Pick Up Here:** [exact instruction for next session — specific enough to start cold]
   **Session Context:** [anything important that isn't captured elsewhere — temp decisions, debugging state, gotchas discovered]
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
- **Lv.4** — Native: CC rules integration (`.claude/rules/diary.md`), always-on session logging awareness without skill file read. (Origin: MemStack v3.0-beta, Feb 2026)
- **Lv.5** — Handoff: Added structured Session Handoff section — in-progress work, uncommitted changes, exact pickup instructions, session context preservation. (Origin: MemStack v3.1, Feb 2026)

## Pro Feature: PreCompact Auto-Save

MemStack™ Pro includes a PreCompact hook that automatically saves a diary entry before Claude Code context compaction runs. Free version requires manual diary saves only.

Upgrade: memstack.pro
