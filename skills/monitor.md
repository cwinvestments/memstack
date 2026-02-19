# Monitor — MemStack Skill

## Trigger Keywords
- Auto-activates on every session if `cc_monitor.api_key` is set in config.json

## Purpose
Auto-report CC session status to AdminStack CC Monitor dashboard throughout each session.

## Instructions

### On session start:

1. **Read config.json** — get `cc_monitor.api_url` and `cc_monitor.api_key`
2. **If api_key is empty** — skip silently, do not prompt the user
3. **Report "working" status:**
   ```bash
   curl -s -X POST {api_url} \
     -H "Content-Type: application/json" \
     -d '{
       "api_key": "{api_key}",
       "session_name": "{task_name}",
       "project": "{project_name}",
       "status": "working",
       "last_output": "Starting task"
     }'
   ```

### During the session:

4. **When waiting for user input** — report "waiting_input":
   ```bash
   curl -s -X POST {api_url} \
     -H "Content-Type: application/json" \
     -d '{
       "api_key": "{api_key}",
       "session_name": "{task_name}",
       "project": "{project_name}",
       "status": "waiting_input",
       "last_output": "{what you need from the user}"
     }'
   ```

### On session end:

5. **Report "completed" or "error":**
   ```bash
   curl -s -X POST {api_url} \
     -H "Content-Type: application/json" \
     -d '{
       "api_key": "{api_key}",
       "session_name": "{task_name}",
       "project": "{project_name}",
       "status": "completed",
       "last_output": "{brief summary of what was accomplished}"
     }'
   ```

### Rules:
- Keep `last_output` under 500 characters
- Use the task name from the user's prompt as `session_name`
- Use the project name from config.json or the working directory name as `project`
- Do not report on trivial questions — only report on actual task sessions

## Inputs
- config.json: `cc_monitor.api_url`, `cc_monitor.api_key`
- Task name from user prompt
- Project name from config.json or working directory

## Outputs
- HTTP POST requests to CC Monitor API (silent — don't show output to user unless error)

## Example Usage

**Session starts with:** "Build the analytics dashboard for AdminStack"

**Monitor auto-activates (silently):**

```bash
# Sent automatically at start:
curl -s -X POST https://admin.cwaffiliateinvestments.com/api/cc-sessions/report \
  -H "Content-Type: application/json" \
  -d '{"api_key":"...","session_name":"Analytics Dashboard","project":"AdminStack","status":"working","last_output":"Starting task"}'

# Sent automatically at completion:
curl -s -X POST ... -d '{"status":"completed","last_output":"Built analytics page with charts, filters, and export"}'
```

The user sees nothing — Monitor works silently in the background.
