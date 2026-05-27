---
name: diary
trigger: "save diary" | "log session" | "wrapping up" | "end of session"
---

# Diary -- Save Session Log

When triggered, follow these steps exactly.

## Step 1: Gather Session Data

Summarize the current session: project name, date (YYYY-MM-DD), what was accomplished, files changed, commits made, decisions and rationale, problems encountered, next steps.

## Step 2: Save to Database

Use Bash to call memstack-db.py. ALL field values must be plain strings, never arrays or objects.

Command: python C:/Projects/memstack/db/memstack-db.py add-session '<JSON>'

Required JSON fields:
- project (string): project name
- date (string): YYYY-MM-DD
- summary (string): one-line summary

Optional JSON fields (all strings, comma-separated if multiple):
- accomplished (string): what was done
- files_changed (string): "file1.py, file2.py, file3.py"
- commits (string): "abc1234 commit msg, def5678 commit msg"
- decisions (string): "Decision 1. Decision 2."
- problems (string): any issues encountered
- next_steps (string): what to do next
- duration (string): "Xm Ys"

## Step 3: Save Insights

For each significant decision, run:

Command: python C:/Projects/memstack/db/memstack-db.py add-insight '<JSON>'

Required JSON fields:
- content (string): the decision or insight text

CRITICAL: The field name is "content", NOT "insight". Using "insight" will error.

Optional JSON fields:
- project (string): project name
- type (string): defaults to "decision"
- context (string): why this decision was made
- tags (string): comma-separated tags

## Step 4: Save Markdown Backup

Write a markdown summary to memory/sessions/<date>-<project>.md

## Step 5: Webhook

If MEMSTACK_DEVLOG_WEBHOOK env var is set, POST the session JSON to that URL.

## Rules
- All JSON values must be strings. Never pass arrays or objects.
- Use Bash for all commands.
- If a command fails, read the error message carefully and fix the JSON before retrying. Do not guess.
