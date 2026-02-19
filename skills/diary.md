# Diary — MemStack Skill

## Trigger Keywords
- save diary, write diary, log session (auto-activates at session end if auto_diary is true)

## Purpose
Document what was accomplished in each CC session. Creates a searchable log that Echo can reference later.

## Instructions

1. **Summarize the session:**
   - Project name and working directory
   - Date and approximate duration
   - What was built or changed
   - Files created or modified (list key ones)
   - Commits made (hashes and messages)
   - Decisions made and why
   - Problems encountered and how they were solved

2. **Check git log** for commits made this session:
   ```bash
   git log --oneline -10
   ```

3. **Format the diary entry** as markdown:
   ```markdown
   # Session Diary — {project} — {date}

   ## Accomplished
   - Item 1
   - Item 2

   ## Files Changed
   - path/to/file.ts — description

   ## Commits
   - abc1234 Commit message

   ## Decisions
   - Decision: reason

   ## Next Steps
   - What to do next
   ```

4. **Save to** `memory/sessions/{date}-{project}.md`

5. **Confirm** — show the user a brief summary of what was logged

## Inputs
- Current session context (CC tracks this naturally)
- Project name from working directory or config.json
- Git log for commit history

## Outputs
- Session diary file in memory/sessions/
- Brief confirmation summary

## Example Usage

**User prompt:** "save diary" (at end of session)

**Diary activates:**

```
Session Diary saved: memory/sessions/2026-02-18-adminstack.md

Summary:
  Project: AdminStack
  Duration: ~2 hours
  Accomplished: Built CC Monitor page, API routes, setup guide
  Commits: 4 (45b4c42, d1c7e11, f6c8e18, f0e793f)
  Files changed: 8

This session is now searchable via Echo.
```
