# Seal — MemStack Skill

## Trigger Keywords
- commit, push, task completion (auto-activates at end of any task)

## Purpose
Enforce consistent, clean git commits with build verification before pushing.

## Instructions

1. **Run build check:**
   ```bash
   npm run build 2>&1 | tail -20
   ```
   If the build fails, FIX the errors before proceeding. Never commit broken code.

2. **Check git status:**
   ```bash
   git status
   git diff --stat
   ```

3. **Stage only relevant files** — never use `git add .` blindly. Exclude:
   - `node_modules/`
   - `.env`, `.env.local`, any file with secrets
   - Build output (`dist/`, `.next/`, `out/`)
   - OS files (`.DS_Store`, `Thumbs.db`)

4. **Generate commit message** using the format from config.json:
   - Default: `[ProjectName] Brief description of change`
   - Be specific: "[AdminStack] Add CC Monitor page with session tracking" not "[AdminStack] Update code"
   - Add `Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>`

5. **Commit and push:**
   ```bash
   git add <specific files>
   git commit -m "[Project] Message\n\nCo-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
   git push
   ```

6. **Verify push succeeded** — run `git status` after push.

## Inputs
- Project name (from config.json or working directory)
- Files changed during the task

## Outputs
- Clean git commit with descriptive message
- Confirmation of successful push

## Example Usage

**User prompt:** "commit this" (after building a feature)

**Seal activates:**

```
Running build check... ✓ Build passed
Staging files:
  - src/app/(dashboard)/cc-monitor/page.tsx
  - src/app/api/cc-sessions/route.ts
  - database/020_cc_sessions.sql

Commit: [AdminStack] Add CC Monitor page for tracking Claude Code sessions
Push: main → origin/main ✓
```
