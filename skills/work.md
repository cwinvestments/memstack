# Work — MemStack Skill

## Trigger Keywords
- copy plan, resume plan, what's next, todo, priorities, task list

## Purpose
Manage task lists, track progress through plans, and keep work organized across sessions.

## Instructions

1. **If "copy plan" or new plan provided:**
   - Parse the plan into individual tasks
   - Create a numbered checklist
   - Save to `memory/projects/{project}-plan.md`
   - Present the plan with status indicators

2. **If "what's next" or "priorities":**
   - Read the current plan from `memory/projects/{project}-plan.md`
   - Show incomplete tasks in priority order
   - Recommend which task to tackle next

3. **If "resume plan":**
   - Read the saved plan
   - Show what's done vs pending
   - Pick up from the first incomplete task

4. **Track progress** — as tasks complete, update the plan file:
   - `[ ]` → pending
   - `[~]` → in progress
   - `[x]` → completed
   - `[!]` → blocked (include reason)

5. **At task completion** — update the plan file and show remaining items

## Inputs
- Plan text (if new) or project name (if resuming)
- Memory directory: `C:\Projects\memstack\memory\projects\`

## Outputs
- Formatted task list with status indicators
- Next recommended action
- Updated plan file in memory

## Example Usage

**User prompt:** "what's next on AdminStack?"

**Work activates:**

```
AdminStack Plan (3 of 7 complete):

[x] 1. Build CC Monitor page
[x] 2. Add setup guide
[x] 3. Fix API key validation
[ ] 4. Build cc-reporter.js Node script
[ ] 5. Add real-time WebSocket updates
[ ] 6. Session grouping by project
[!] 7. Mobile responsive polish (blocked: waiting for design specs)

Recommended next: Task 4 — Build cc-reporter.js Node script
```
