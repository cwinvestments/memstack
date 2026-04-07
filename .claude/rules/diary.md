# Diary — Session Logging Rule

After completing any significant task or when the user says "save diary", "log session", or "wrapping up" — log the session to SQLite with auto-extracted insights.

## Protocol
1. Summarize: project, date, accomplishments, files changed, commits, decisions, next steps
2. Include **Session Handoff** section: what's in progress, uncommitted changes, exact pickup instruction, session context that would be lost
3. Save session: `python db/memstack-db.py add-session '<json>'`
4. Extract each decision as an insight: `python db/memstack-db.py add-insight '<json>'`
5. Update project context: `python db/memstack-db.py set-context '<json>'`
6. Also save markdown backup to `memory/sessions/{date}-{project}.md`
7. If `MEMSTACK_DEVLOG_WEBHOOK` env var is set, POST diary content to the webhook URL. Webhook failure must never block the diary save.

## Ownership
- "save diary" / "log session" / "wrapping up" = Diary (not the Project skill, not Echo)
- Do not activate mid-task or at session start when nothing has been done
