---
name: deploy
description: "MUST use before any git push or deployment. Auto-activates before pushing code. Triggers on 'deploy', 'build', 'ship it', 'push'. Runs build verification, checks for debug artifacts, and confirms deployment safety."
---

# 🚀 Deploy — Pre-flight checks running...
*Verify builds pass and deployments are safe before shipping code.*

## Activation

When this skill activates, output:

`🚀 Deploy — Pre-flight checks running...`

Then execute the protocol below.

## Context Guard

| Context | Status | Priority |
|---------|--------|----------|
| **User says "deploy", "ship it", or "push" with intent to publish** | ACTIVE — run full checks | P1 |
| **About to run `git push` as part of a task** | ACTIVE — run full checks | P1 |
| **User says "build" to test locally (no push intent)** | DORMANT — just run `npm run build` directly | — |
| **Discussing deployment concepts ("how does Netlify work")** | DORMANT — do not activate | — |
| **Committing without pushing (user just said "commit")** | DORMANT — Seal handles commits | — |
| **Running tests or linting** | DORMANT — not a deploy action | — |
| **SSH-based server deploys (manual server work)** | DORMANT — user is handling deployment manually | — |

### Deconfliction with Seal
Deploy owns the **push**. If uncommitted changes exist, Deploy invokes Seal's commit protocol first, then runs its own pre-flight checks, then pushes. Seal does NOT independently activate on "push".

## Protocol

1. **Run the full build:**
   ```bash
   npm run build 2>&1 | tail -30
   ```

2. **Check for build errors** — if any, STOP and fix before proceeding

3. **Check for debug artifacts:**
   ```bash
   grep -rn "console.log\|console.warn\|console.error\|debugger" src/ --include="*.ts" --include="*.tsx" | grep -v "node_modules" | grep -v ".test." | head -20
   ```

4. **Check for .env or secrets in staged files:**
   ```bash
   git diff --cached --name-only | grep -E "\.env|secret|credential|password"
   ```

5. **Show deployment summary:**
   - Build status (pass/fail)
   - Warning count
   - Files changed (from git)
   - Deploy target (from project context)

6. **Ask user to confirm** before pushing

7. **Execute push** only after confirmation

## Inputs
- Project build command (from package.json)
- Git status and staged changes
- Deploy target (Netlify, Vercel, Railway, etc.)

## Outputs
- Build verification report (pass/fail)
- Debug artifact warnings
- Deployment confirmation

## Example Usage

**User:** "ship it"

```
🚀 Deploy — Pre-flight checks running...

Build:           ✓ passed (12.4s)
TypeScript:      ✓ no errors
Debug artifacts: ⚠ 3 console.log statements
Secrets check:   ✓ clean
Files changed:   8 files (+342, -56)
Deploy target:   Netlify (auto-deploy on push to main)

Warnings:
  - 3 console.log statements in production code — review before shipping

Proceed with push? [User confirms]
Pushing to main... ✓
Netlify deploy triggered. Check: https://app.netlify.com/sites/adminstack/deploys
```

## Level History

- **Lv.1** — Base: Build verification and push safety checks. (Origin: MemStack v1.0, Feb 2026)
- **Lv.2** — Enhanced: Added YAML frontmatter, context guard, activation message, secrets check step. (Origin: MemStack v2.0 MemoryCore merge, Feb 2026)
