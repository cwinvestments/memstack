# Project — MemStack Skill

## Trigger Keywords
- save project, load project, handoff, session ending, context running low

## Purpose
Save and restore project state between CC sessions. Generates handoff documents so the next session can pick up exactly where this one left off.

## Instructions

### Saving (handoff):

1. **Capture current state:**
   - What was accomplished this session
   - What's currently in progress (uncommitted changes, partial work)
   - Open questions or decisions pending
   - Next steps in priority order
   - Key file paths that were modified

2. **Run git status** to capture uncommitted state

3. **Generate handoff document** using `templates/handoff.md`:
   - Save to `memory/projects/{project}-{date}.md`
   - Include a ready-to-paste prompt for the next CC session

4. **Present the handoff prompt** — the user copies this into their next CC session

### Loading (restore):

1. **Find the most recent handoff** in `memory/projects/` for the requested project
2. **Read and present** the saved state
3. **Show the next steps** so CC can continue immediately

## Inputs
- Project name
- Current session context (what was done, what's pending)

## Outputs
- Handoff document saved to memory
- Ready-to-paste prompt for next CC session

## Example Usage

**User prompt:** "context is running low — save project"

**Project activates:**

```
Saving AdminStack session state...

Handoff saved: memory/projects/adminstack-2026-02-18.md

--- PASTE THIS INTO YOUR NEXT CC SESSION ---

Working directory: C:\Projects\AdminStack
Read C:\Projects\memstack\MEMSTACK.md

Resume AdminStack work. Last session (2026-02-18) completed:
- Built CC Monitor page with auto-refresh and notifications
- Added /api/cc-sessions CRUD + public report endpoint
- Fixed API key validation with .trim()

Next steps:
1. Build cc-reporter.js Node script
2. Add WebSocket real-time updates
3. Mobile responsive polish

Uncommitted changes: None (all pushed to main)

--- END HANDOFF ---
```
