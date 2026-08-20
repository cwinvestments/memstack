# Work — Task Planning Rule

When the user says "plan", "task", "todo", "priorities", "what's next", "copy plan", "append plan", or "resume plan" — activate structured planning with per-task status tracking in SQLite.

## Protocol
- **Step 0 (silent)**: Before any plan operation, read `STATE.md`, `CLAUDE.md`, recent diary entries, and git state to compile context. Do not show this step to the user.
- **New plan / "copy plan"**: Parse tasks, then save each one. Write the payload to a file and pipe it in with `-` as the argument: `cat task.json | python db/memstack-db.py add-plan-task -`
- **Update / "append plan"**: Same form: `cat task.json | python db/memstack-db.py update-task -`
- **Resume / "resume plan"**: Load plan via `python db/memstack-db.py get-plan <project>`, show status summary
- **Quick query / "todo"**: Show all pending and in-progress tasks with status indicators

A payload on stdin is never seen by the shell's parser, so a redirection operator inside a task description cannot be read as one.

## Status Values
`pending` | `in_progress` | `completed` | `blocked`

## Ownership
- "plan" / "todo" / "task" / "priorities" = Work only
- Do not activate when the user is executing a task (not managing the list)
