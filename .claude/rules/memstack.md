# MemStack Global Rules

## Commit Format
Git commits support two formats. Use whichever fits the context:

**Standard format** (default):
```
[ProjectName] Brief description of change

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

**Conventional format** (for phased projects or when type clarity helps):
```
type(scope): description

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

Types: `feat` (new feature), `fix` (bug fix), `docs` (documentation), `refactor` (restructure), `style` (formatting), `test` (tests), `chore` (maintenance)

Scope is optional — use project name, module, or phase-task number (e.g., `feat(03-02): add user registration`).

Auto-detect type from changes: new files = `feat`, modifications = `fix`/`refactor`, `.md` files = `docs`.

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

## Deprecated Skills — Do Not Activate
Skills marked `deprecated: true` (Seal, Deploy, Monitor) are replaced by deterministic hooks in `.claude/hooks/`. Never follow their protocols manually — the hooks fire automatically on the correct CC lifecycle events. Only read deprecated skill files if debugging hook behavior.

## Skill Chain
When finishing a task: commit (hook) → log session (Diary) → report status (hook). Hooks fire automatically; only Diary requires explicit activation.
