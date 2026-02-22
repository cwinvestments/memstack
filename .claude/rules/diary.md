# Diary — Session Logging Rule

After completing any significant task or when the user says "save diary", "log session", or "wrapping up" — log the session to SQLite with auto-extracted insights.

## Protocol
1. Summarize: project, date, accomplishments, files changed, commits, decisions, next steps
2. Save session: `python C:/Projects/memstack/db/memstack-db.py add-session '<json>'`
3. Extract each decision as an insight: `python C:/Projects/memstack/db/memstack-db.py add-insight '<json>'`
4. Update project context: `python C:/Projects/memstack/db/memstack-db.py set-context '<json>'`
5. Also save markdown backup to `memory/sessions/{date}-{project}.md`

## Ownership
- "save diary" / "log session" / "wrapping up" = Diary (not Project, not Echo)
- Do not activate mid-task or at session start when nothing has been done
