# Echo — MemStack Skill

## Trigger Keywords
- do you remember, recall, last session, what did we, continue from

## Purpose
Recall information from past CC sessions by searching session logs stored in memory.

## Instructions

1. **Search memory/sessions/** — look for files matching the topic or project name
2. **Search memory/projects/** — check for project state snapshots
3. **Read the most recent matching files** — extract relevant context
4. **Present findings** in a summary format:
   - Date and project name
   - What was accomplished
   - What was left pending
   - Any decisions or notes recorded
5. **If nothing found** — tell the user clearly: "No session logs found for [topic]. Start a Diary to save future sessions."

## Inputs
- Keywords from the user's prompt (project name, feature name, date range)
- Memory directory: `C:\Projects\memstack\memory\`

## Outputs
- Summary of relevant past session context
- File paths to the source logs for reference
- Suggestions for what to do next based on past state

## Example Usage

**User prompt:** "Do you remember what we did on the AdminStack CC Monitor last session?"

**Echo activates:**

```
Found 2 session logs matching "AdminStack CC Monitor":

1. memory/sessions/2026-02-18-adminstack-cc-monitor.md
   - Built CC Monitor page with session cards, auto-refresh, notifications
   - Created /api/cc-sessions CRUD routes
   - Added setup guide with auto-report curl snippet
   - Status: Completed and pushed to main

2. memory/sessions/2026-02-17-adminstack-infrastructure.md
   - Added Headroom proxy monitoring tab
   - Relevant: CC Monitor uses similar card patterns

Pending items from last session: None — all tasks completed.
```
