---
description: Standards for Builder agent execution
globs: ["**/*"]
---

# Builder Agent Standards

## Before Reporting Counts or Claims
- Use shell commands (grep, find, wc) for all counts. Never estimate or eyeball.
- Report the exact command you ran and its output.
- Check ALL relevant directories before claiming something doesn't exist (e.g. both database/ AND migrations/).

## Before Starting Any Task
- Read all files specified in the prompt FIRST. Do not start coding until you've read everything.
- Never assume file contents, API shapes, column names, or path structures.
- Run `find` or `ls` to confirm directory structure before modifying files.

## Before Reporting Back
- Re-read your own output. Would a skeptical Reviewer find errors?
- Verify counts match reality by re-running the command.
- If you created/modified files, re-read them to confirm correctness.

## Shell Commands Over Eyeballing
- Count routes: `find src/app/api -name "route.ts" | wc -l`
- Count pages: `find src/app -name "page.tsx" | wc -l`
- Find a string: `grep -rn "searchterm" src/`
- Check table usage: `grep -rn "table_name" src/`
- List migrations: `ls -la database/ migrations/`

## Never
- Never report a count without running a command to verify
- Never claim a file or directory doesn't exist without searching for it
- Never skip reading files the prompt told you to read
- Never modify files outside the scope specified in the prompt
