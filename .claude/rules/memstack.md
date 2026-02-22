# MemStack Global Rules

## Commit Format
All git commits must follow this format:
```
[ProjectName] Brief description of change

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

## Build Before Push
Always run `npm run build` (or equivalent) and verify it passes before any `git push`. If the build fails, fix the errors before pushing. Never use `--no-verify` to skip checks.

## No Secrets in Git
Never commit:
- `.env`, `.env.local`, or any environment files with secrets
- `node_modules/`
- Build output (`dist/`, `.next/`, `out/`)
- API keys, tokens, or passwords in source code

## Document Decisions
When making architectural decisions or non-obvious choices, update the project's `CLAUDE.md` with the rationale. Future sessions depend on this context.

## One Task at a Time
Complete the current task fully before starting a new one. If a task reveals sub-tasks, finish the original first or explicitly save state before switching.

## Skill Chain
When finishing a task: commit (Seal) → log session (Diary) → report status (Monitor). Each step should complete before the next begins.
