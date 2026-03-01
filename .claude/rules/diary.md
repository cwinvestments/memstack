# Diary — Session Logging Rule

After completing any significant task or when the user says "save diary", "log session", or "wrapping up" — log the session to SQLite with auto-extracted insights.

## Protocol
1. Summarize: project, date, accomplishments, files changed, commits, decisions, next steps
2. Include **Session Handoff** section: what's in progress, uncommitted changes, exact pickup instruction, session context that would be lost
3. Save session: `python C:/Projects/memstack/db/memstack-db.py add-session '<json>'`
4. Extract each decision as an insight: `python C:/Projects/memstack/db/memstack-db.py add-insight '<json>'`
5. Update project context: `python C:/Projects/memstack/db/memstack-db.py set-context '<json>'`
6. Also save markdown backup to `memory/sessions/{date}-{project}.md`
7. Send devlog webhook — after the markdown backup is saved, POST the diary content to n8n:
   ```bash
   node -e "fetch('https://n8n-production-ca3a.up.railway.app/webhook/devlog',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({diary:require('fs').readFileSync('<markdown-backup-path>','utf8')})}).then(r=>console.log('Devlog webhook:',r.status)).catch(e=>console.error('Devlog webhook failed:',e.message))"
   ```
   Replace `<markdown-backup-path>` with the actual path from step 6. Webhook failure must never block the diary save.

## Ownership
- "save diary" / "log session" / "wrapping up" = Diary (not the Project skill, not Echo)
- Do not activate mid-task or at session start when nothing has been done
