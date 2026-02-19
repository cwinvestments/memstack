# Deploy — MemStack Skill

## Trigger Keywords
- deploy, build, ship it (auto-activates before any git push)

## Purpose
Verify builds pass and deployments are safe before shipping code.

## Instructions

1. **Run the full build:**
   ```bash
   npm run build 2>&1
   ```
   If it fails, STOP. Fix all errors before proceeding.

2. **Check for TypeScript errors:**
   ```bash
   npx tsc --noEmit 2>&1
   ```

3. **Scan for debug artifacts** — check for leftover console.logs in production code:
   ```bash
   grep -rn "console.log\|console.warn\|console.error\|debugger" src/ --include="*.ts" --include="*.tsx" | grep -v "node_modules" | grep -v ".test." | head -20
   ```
   Warn the user about any found (don't auto-remove — some may be intentional).

4. **Verify environment variables** — check that the deploy target has required env vars:
   - Read the project's `.env.example` or `.env.local` if they exist
   - List any vars that are referenced in code but might be missing on the deploy target

5. **Confirm deploy target** from config.json:
   - Netlify: check for `netlify.toml` or Netlify CLI config
   - Railway: check for `railway.toml` or Procfile
   - Vercel: check for `vercel.json`

6. **Execute deployment** based on target:
   - **Netlify:** `git push` triggers auto-deploy
   - **Railway:** `git push` triggers auto-deploy
   - **Vercel:** `vercel --prod` or `git push`

7. **Post-deploy verification:**
   - Wait 30 seconds for deployment to propagate
   - If a health check URL is known, ping it
   - Report success or failure

## Inputs
- Project name and deploy target from config.json
- Current branch and remote status

## Outputs
- Build verification report (pass/fail)
- Deployment status
- Any warnings (console.logs, missing env vars)

## Example Usage

**User prompt:** "ship it" (after completing a feature)

**Deploy activates:**

```
Deploy Guardian — AdminStack (Netlify)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Build check:     ✓ passed (47 routes compiled)
TypeScript:      ✓ no errors
Console.logs:    ⚠ 3 found (src/app/api/contacts/route.ts:24, ...)
Env vars:        ✓ all present on Netlify
Deploy target:   Netlify (auto-deploy on push to main)

Warnings:
  - 3 console.log statements in production code — review before shipping

Proceed with push? [User confirms]
Pushing to main... ✓
Netlify deploy triggered. Check: https://app.netlify.com/sites/adminstack/deploys
```
