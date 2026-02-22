---
name: monitor
description: "DEPRECATED v3.0 — Replaced by native CC hooks at .claude/hooks/session-start.sh and session-end.sh. Kept as fallback for CC versions without hook support. Original: Auto-activates on every session if cc_monitor.api_key is set."
deprecated: true
replaced_by: ".claude/hooks/session-start.sh, .claude/hooks/session-end.sh"
---

# 📡 Monitor — Reporting Status...

> **DEPRECATED in MemStack v3.0** — This skill is now a pair of deterministic CC hooks.
> See `.claude/hooks/session-start.sh`, `.claude/hooks/session-end.sh`, and `.claude/settings.json`.
> This file is preserved as fallback for older CC versions without hook support.
*Auto-report CC session status to AdminStack CC Monitor dashboard throughout each session.*

## Activation

When this skill activates, output:

`📡 Monitor — Reporting to AdminStack...`

Then execute the protocol below silently (do not show curl output to user unless there's an error).

## Protocol

### On session start:

1. **Read config.json** to get `cc_monitor.api_url` and `cc_monitor.api_key`
2. **If no API key is set** — skip silently, do not activate
3. **Report "working" status:**
   ```bash
   curl -s -X POST {api_url} \
     -H "Content-Type: application/json" \
     -d '{
       "api_key": "{api_key}",
       "session_name": "{task_name}",
       "project": "{project}",
       "status": "working",
       "last_output": "Starting: {brief_description}"
     }'
   ```

### During the session:

4. **Report progress** at major milestones (file creation, build completion, etc.):
   ```bash
   curl -s -X POST {api_url} \
     -H "Content-Type: application/json" \
     -d '{
       "api_key": "{api_key}",
       "session_name": "{task_name}",
       "project": "{project}",
       "status": "working",
       "last_output": "{what_just_happened}"
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
       "project": "{project}",
       "status": "completed",
       "last_output": "{final_summary}"
     }'
   ```

## Rules

- Use the project name from config.json or the working directory name as `project`
- Use the task description from the user's first message as `session_name`
- Keep `last_output` under 200 characters — brief, informative summaries
- Run all curl commands silently (`-s` flag) — do not show output to user unless error
- If a curl fails, ignore it and continue — monitoring should never block work
- Report at natural breakpoints, not after every small action

## Inputs
- config.json cc_monitor settings (api_url, api_key)
- Current task context (project name, task description)

## Outputs
- HTTP POST requests to CC Monitor API (silent — don't show output to user unless error)

## Example Usage

```
📡 Monitor — Reporting to AdminStack...

# Sent automatically at session start:
curl -s -X POST {api_url} \
  -H "Content-Type: application/json" \
  -d '{"api_key":"...","session_name":"Analytics Dashboard","project":"MyProject","status":"working","last_output":"Starting task"}'

# Sent automatically at completion:
curl -s -X POST ... -d '{"status":"completed","last_output":"Built analytics page with charts, filters, and export"}'
```

The user sees nothing — Monitor works silently in the background.

## Level History

- **Lv.1** — Base: Silent CC Monitor reporting with curl. (Origin: MemStack v1.0, Feb 2026)
- **Lv.2** — Enhanced: Added YAML frontmatter, activation message, structured protocol sections. (Origin: MemStack v2.0 MemoryCore merge, Feb 2026)
- **Lv.3** — DEPRECATED: Replaced by deterministic CC hooks `session-start.sh` + `session-end.sh`. Skill preserved as fallback. (Origin: MemStack v3.0, Feb 2026)
