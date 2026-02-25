# Work — Task Planning Rule

When the user says "plan", "task", "todo", "priorities", "what's next", "copy plan", "append plan", or "resume plan" — activate structured planning with per-task status tracking in SQLite.

## Protocol
- **Step 0 (silent)**: Before any plan operation, read `STATE.md`, `CLAUDE.md`, recent diary entries, and git state to compile context. Do not show this step to the user.
- **New plan / "copy plan"**: Parse tasks, save each via `python C:/Projects/memstack/db/memstack-db.py add-plan-task '<json>'`
- **Update / "append plan"**: Update task status via `python C:/Projects/memstack/db/memstack-db.py update-task '<json>'`
- **Resume / "resume plan"**: Load plan via `python C:/Projects/memstack/db/memstack-db.py get-plan <project>`, show status summary
- **Quick query / "todo"**: Show all pending and in-progress tasks with status indicators

## Status Values
`pending` | `in_progress` | `completed` | `blocked`

## Ownership
- "plan" / "todo" / "task" / "priorities" = Work only
- Do not activate when the user is executing a task (not managing the list)
