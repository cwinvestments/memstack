---
name: seal
description: "MUST use when committing code, pushing to git, or completing any task. Also triggers on 'commit', 'push', 'ship it', 'task done'. Auto-activates before any git push. Enforces build verification and clean commit hygiene."
---

# 🔒 Seal — Clean Commits, Every Time
*The guardian that ensures every push is build-verified and properly formatted.*

## Activation

When this skill activates, output:

`🔒 Seal — Clean commits, every time.`

Then execute the protocol below.

## Context Guard

| Context | Status |
|---------|--------|
| **User says "commit" or "push"** | ACTIVE — full protocol |
| **Task completion detected** | ACTIVE — full protocol |
| **About to run git push** | ACTIVE — full protocol |
| **Discussing git concepts theoretically** | DORMANT — do not activate |
| **Reading git logs or history** | DORMANT — do not activate |
| **User explicitly says "skip build check"** | ACTIVE — skip step 1 only |

## Protocol

1. **Run build check:**
   ```bash
   npm run build 2>&1 | tail -20
   ```
   If build fails — STOP. Fix errors before proceeding.

2. **Check git status:**
   ```bash
   git status
   git diff --stat
   ```

3. **Stage only relevant files.** Never `git add .` blindly. Exclude:
   - `node_modules/`, `.env`, `.env.local`, any secrets
   - Build output (`dist/`, `.next/`, `out/`)
   - OS files (`.DS_Store`, `Thumbs.db`)

4. **Generate commit message** using config.json format:
   - Default: `[ProjectName] Brief description of change`
   - Be specific — describe WHAT changed and WHY
   - Add `Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>`

5. **Commit and push:**
   ```bash
   git add <specific files>
   git commit -m "[Project] Message

   Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
   git push
   ```

6. **Verify push succeeded** — run `git status` after push.

## Mandatory Rules
- NEVER commit with `--no-verify`
- NEVER force push to main/master
- NEVER amend published commits without explicit user request
- Always create NEW commits after hook failures

## Example Usage

**User:** "commit this"

```
🔒 Seal — Clean commits, every time.

Build check:  ✓ passed
Staging:      3 files (page.tsx, route.ts, migration.sql)
Commit:       [AdminStack] Add CC Monitor page for session tracking
Push:         main → origin/main ✓
```

## Level History

- **Lv.1** — Base: Build check, staged commits, descriptive messages. (Origin: MemStack v1.0, Feb 2026)
- **Lv.2** — Enhanced: Added YAML frontmatter, context guard, mandatory rules, activation message. (Origin: MemStack v2.0 MemoryCore merge, Feb 2026)
