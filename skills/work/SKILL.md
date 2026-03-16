---
name: work
description: "Use when the user says 'plan', 'todo', 'copy plan', 'append plan', 'resume plan', 'priorities', or 'what's next'."
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

## Step 0: Silent Context Compilation (MANDATORY)

Before executing ANY mode, silently gather current state. Do NOT present findings. Do NOT ask questions. Just internalize:

1. Read the project's `STATE.md` (if it exists) — current task, blockers, next steps
2. Read the project's `CLAUDE.md` (if it exists) — conventions, architecture decisions
3. Check recent diary:
   ```bash
   python C:/Projects/memstack/db/memstack-db.py get-sessions <project> --limit 3
   ```
4. Check git state:
   ```bash
   git log --oneline -5
   git diff --stat
   ```

**This is silent.** Synthesize an internal understanding of where the project stands. Then proceed to the triggered mode with full context. The user already knows their project state — don't waste their time repeating it back.

## Mode 1: Copy Plan

**Trigger:** "copy plan" or when a new plan is provided

1. Parse the entire plan into individual numbered tasks
2. For each task, save to SQLite:
   ```bash
   python C:/Projects/memstack/db/memstack-db.py add-plan-task '{"project":"<name>","task_number":<n>,"description":"<task>","status":"pending"}'
   ```
3. Confirm with task count
4. Also write a markdown copy to `memory/projects/{project}-plan.md` for human readability

**Status values:** `pending`, `in_progress`, `completed`, `blocked`

## Mode 2: Append Plan (Update Tasks)

**Trigger:** "append plan" or when updating task statuses

1. Read current plan from SQLite:
   ```bash
   python C:/Projects/memstack/db/memstack-db.py get-plan <project>
   ```
2. Update individual task statuses:
   ```bash
   python C:/Projects/memstack/db/memstack-db.py update-task '{"project":"<name>","task_number":<n>,"status":"completed"}'
   ```
3. Add new tasks if needed via `add-plan-task`
4. No size limits needed — SQLite handles scale

## Mode 3: Resume Plan

**Trigger:** "resume plan" — use after CC compact or new session

1. Load plan from SQLite:
   ```bash
   python C:/Projects/memstack/db/memstack-db.py get-plan <project>
   ```
2. Parse the JSON output for task statuses
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

- **"what's next"** — queries plan, returns the single next pending task
- **"priorities"** — shows top 3 pending items from the plan
- **"todo"** — shows all pending and in-progress items with status

## Inputs
- Plan text (copy mode) or project name (append/resume)
- Database: `C:\Projects\memstack\db\memstack.db` (via memstack-db.py)
- Fallback: `C:\Projects\memstack\memory\projects\` (legacy markdown)

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
- **Lv.3** — Advanced: SQLite-backed plans with per-task status tracking, no size limits, structured queries. (Origin: MemStack v2.1 Accomplish-inspired upgrade, Feb 2026)
- **Lv.4** — Native: CC rules integration (`.claude/rules/work.md`), always-on task planning awareness without skill file read. (Origin: MemStack v3.0-beta, Feb 2026)
- **Lv.5** — Context-aware: Silent context compilation (Step 0) — reads STATE.md, CLAUDE.md, recent diary, and git state before any operation. Inspired by Intellegix silent pre-flight pattern. (Origin: MemStack v3.2, Feb 2026)

> 💎 Pro: SessionStart hook auto-injects your last 3 sessions of context.
