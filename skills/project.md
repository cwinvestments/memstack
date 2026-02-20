---
name: project
description: "MUST use when saving project state for session handoff, restoring a previous session, or when context is running low. Triggers on 'save project', 'load project', 'handoff', 'session ending', 'context running low'. Generates ready-to-paste prompts for the next CC session."
---

# 💾 Project — Saving Project State...
*Save and restore project state between CC sessions for seamless handoffs.*

## Activation

When this skill activates, output:

`💾 Project — Saving project state...`

Then execute the protocol below.

## Protocol

### Saving (handoff):

1. **Capture current state:**
   - What was accomplished this session
   - What's currently in progress (uncommitted changes, partial work)
   - Open questions or decisions pending
   - Next steps in priority order
   - Key file paths that were modified
2. **Run git status** to capture uncommitted state
3. **Save project context to SQLite:**
   ```bash
   python C:/Projects/memstack/db/memstack-db.py set-context '{"project":"<name>","status":"active","current_branch":"<branch>","last_session_date":"<YYYY-MM-DD>","known_issues":"<issues>","backlog":"<next tasks>"}'
   ```
4. **Also save markdown handoff** to `memory/projects/{project}-{date}.md`
5. **Present the ready-to-paste prompt** for the next CC session

### Loading (restore):

1. **Load project context from SQLite:**
   ```bash
   python C:/Projects/memstack/db/memstack-db.py get-context <project>
   ```
2. **Load recent sessions:**
   ```bash
   python C:/Projects/memstack/db/memstack-db.py get-sessions <project> --limit 3
   ```
3. **Load plan if exists:**
   ```bash
   python C:/Projects/memstack/db/memstack-db.py get-plan <project>
   ```
4. **Fallback:** Check `memory/projects/` for markdown handoffs
5. **Present combined state** so CC can continue immediately

## Inputs
- Project name
- Current session context (what was done, what's pending)

## Outputs
- Project context saved to SQLite database
- Markdown handoff in memory/projects/ (backup)
- Ready-to-paste prompt for next CC session

## Example Usage

**User:** "context is running low — save project"

```
💾 Project — Saving project state...

Saved: memory/projects/adminstack-2026-02-18.md

--- PASTE INTO NEXT CC SESSION ---
Working directory: C:\Projects\AdminStack
Read C:\Projects\memstack\MEMSTACK.md

Resume AdminStack. Last session completed:
- Built CC Monitor page with auto-refresh
- Fixed API key validation

Next steps:
1. Build cc-reporter.js script
2. Add WebSocket updates
--- END HANDOFF ---
```

## Level History

- **Lv.1** — Base: Session state capture and handoff generation. (Origin: MemStack v1.0, Feb 2026)
- **Lv.2** — Enhanced: Added YAML frontmatter, activation message, template integration. (Origin: MemStack v2.0 MemoryCore merge, Feb 2026)
- **Lv.3** — Advanced: SQLite-backed project context, combined restore from DB + sessions + plan. (Origin: MemStack v2.1 Accomplish-inspired upgrade, Feb 2026)
