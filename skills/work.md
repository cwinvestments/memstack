---
name: work
description: "MUST use when managing task lists, tracking plan progress, or resuming work after a session reset. Triggers on 'copy plan', 'append plan', 'resume plan', 'what's next', 'todo', 'priorities'. Supports three modes: copy (full plan capture), append (incremental updates), resume (restore after compact)."
---

# 📋 Work — Plan Execution Engaged
*Track tasks, manage plans, and survive CC compacts with three operating modes.*

## Activation

When this skill activates, output:

`📋 Work — Plan execution engaged.`

Then determine which mode to use based on the trigger.

## Context Guard

| Context | Status |
|---------|--------|
| **User says "copy plan", "append plan", "resume plan"** | ACTIVE — use matching mode |
| **User says "what's next", "todo", "priorities"** | ACTIVE — quick query mode |
| **User provides a task list or plan** | ACTIVE — copy mode |
| **General discussion about planning concepts** | DORMANT — do not activate |
| **User is executing a task (not managing the list)** | DORMANT — do not activate |

## Mode 1: Copy Plan

**Trigger:** "copy plan" or when a new plan is provided

1. Parse the entire plan into individual tasks
2. Create a numbered checklist with status markers
3. Write the full plan to `memory/projects/{project}-plan.md`
4. Confirm with task count

**Status markers:**
- `[ ]` — pending
- `[~]` — in progress
- `[x]` — completed
- `[!]` — blocked (include reason)

## Mode 2: Append Plan

**Trigger:** "append plan"

1. Read existing `memory/projects/{project}-plan.md`
2. Append a new progress section with timestamp:
   ```
   ## Update — {date} {time}
   - Completed: {what was done}
   - Next: {what's coming}
   ```
3. **Size check:** If file exceeds 1,000 lines:
   - Summarize the oldest entries into a `## Recap` block (10-15 lines)
   - Remove the detailed old entries
   - Keep the recap + recent entries under 1,000 lines
4. Save the updated file

## Mode 3: Resume Plan

**Trigger:** "resume plan" — use after CC compact or new session

1. Read `memory/projects/{project}-plan.md`
2. Parse current status: what's done, what's pending, what's blocked
3. Output a summary:
   ```
   Plan: {project} ({done}/{total} complete)

   Completed: [list]
   In Progress: [list]
   Pending: [list]
   Blocked: [list with reasons]

   Recommended next: {first pending task}
   ```
4. Continue from the first incomplete task

## Quick Commands

- **"what's next"** — reads plan, returns the single next uncompleted task
- **"priorities"** — shows top 3 pending items from the plan
- **"todo"** — shows all pending and in-progress items with status

## Inputs
- Plan text (copy mode) or project name (append/resume)
- Memory directory: `C:\Projects\memstack\memory\projects\`
- Plan max lines from config.json: `session_limits.plan_max_lines` (default 1000)

## Outputs
- Formatted task list with status indicators
- Updated plan file in memory
- Next recommended action

## Example Usage

**User:** "resume plan for AdminStack"

```
📋 Work — Plan execution engaged.

Plan: AdminStack (5/9 complete)

[x] 1. Build CC Monitor page
[x] 2. Add setup guide
[x] 3. Fix API key validation
[x] 4. Add refresh feedback
[x] 5. Update guide with curl snippet
[ ] 6. Build cc-reporter.js Node script
[ ] 7. Add WebSocket real-time updates
[ ] 8. Session grouping by project
[!] 9. Mobile polish (blocked: waiting for design specs)

Recommended next: Task 6 — Build cc-reporter.js
```

## Level History

- **Lv.1** — Base: Single-mode TODO tracking. (Origin: MemStack v1.0, Feb 2026)
- **Lv.2** — Enhanced: Three modes (copy/append/resume), 1K-line limit with auto-summarize, context guard, YAML frontmatter. (Origin: MemStack v2.0 MemoryCore merge, Feb 2026)
