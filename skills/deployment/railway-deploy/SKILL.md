---
name: memstack-deployment-railway-deploy
description: "Use this skill when the user says 'deploy to Railway', 'Railway setup', 'railway-deploy', or needs to deploy a Node.js, Python, or Docker application to Railway with environment variables, custom domains, and monitoring. Do NOT use for Netlify, Vercel, or Hetzner deployments."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# 🚂 Railway Deploy — Pre-flight check and deploy to Railway...
*Validates project configuration, environment variables, and deployment readiness before pushing to Railway.*

## Activation

When this skill activates, output:

`🚂 Railway Deploy — Running pre-flight checks...`

Then execute the protocol below.

| Context | Status |
|---------|--------|
| User says "deploy to railway" or "railway deploy" | ACTIVE |
| User says "ship it" or "deploy backend" with a Railway project | ACTIVE |
| Preparing a backend/fullstack app for production | ACTIVE |
| Deploying to Netlify, Vercel, or other non-Railway platform | DORMANT |
| Discussing Railway pricing or features generally | DORMANT |

### Anti-patterns

| Trap | Reality Check |
|------|---------------|
| "I'll just `railway up` and see what happens" | Pre-flight catches 90% of deploy failures. Check first. |
| "Environment vars are probably fine" | Missing vars are the #1 cause of Railway deploy failures. Verify every one. |
| "It works locally so it'll work on Railway" | localhost URLs, SQLite paths, and file:// references all break in production. |
| "I'll fix the Dockerfile later" | Railway's nixpacks auto-detect fails on monorepos and custom setups. Define build explicitly. |
| "The database connection works" | Railway internal networking uses `*.railway.internal` hostnames. External URLs add latency and cost. |

## Protocol

### Step 1: Detect Project Type

Identify the project framework and runtime:

```bash
# Check for framework indicators
ls package.json pyproject.toml requirements.txt Cargo.toml go.mod 2>/dev/null
```

| Indicator | Project Type |
|-----------|-------------|
| `package.json` with `next` | Next.js |
| `package.json` with `express`/`fastify`/`hono` | Node.js API |
| `pyproject.toml` or `requirements.txt` | Python (Django/Flask/FastAPI) |
| `Cargo.toml` | Rust |
| `go.mod` | Go |

Report: `Detected: [type] project`

### Step 2: Check Deployment Files

Verify Railway can build the project:

```bash
# Check for explicit build configuration
ls Dockerfile Procfile nixpacks.toml railway.toml 2>/dev/null
```

| File | Purpose | Required? |
|------|---------|-----------|
| `Dockerfile` | Explicit container build | Recommended for complex projects |
| `Procfile` | Process start command | Optional if start script exists |
| `nixpacks.toml` | Nixpacks build config | Optional — auto-detected |
| `railway.toml` | Railway-specific settings | Optional — build/deploy overrides |

If none exist, check that nixpacks can auto-detect:
- Node.js: `package.json` must have `start` script or `main` field
- Python: Must have `requirements.txt` or `pyproject.toml` with dependencies

**Flag if missing:** No build configuration found. Recommend adding `railway.toml` or `Dockerfile`.

### Step 3: Verify Environment Variables

Cross-reference what the app needs vs what Railway has:

```bash
# Find required env vars
cat .env.example .env.sample 2>/dev/null | grep -v '^#' | grep '=' | cut -d= -f1
```

Check for these common categories:

| Category | Variables to Verify |
|----------|-------------------|
| Database | `DATABASE_URL`, `POSTGRES_URL`, `REDIS_URL`, `MONGODB_URI` |
| Auth | `JWT_SECRET`, `SESSION_SECRET`, `NEXTAUTH_SECRET`, `NEXTAUTH_URL` |
| External APIs | `STRIPE_SECRET_KEY`, `SENDGRID_API_KEY`, `AWS_ACCESS_KEY_ID` |
| App Config | `NODE_ENV=production`, `PORT` (Railway sets this automatically) |
| URLs | `FRONTEND_URL`, `BACKEND_URL`, `CORS_ORIGIN` |

**Output:** List each variable with status:
- ✅ Set in `.env.example` — verify it's configured in Railway dashboard
- ⚠️ Referenced in code but not in `.env.example` — add to Railway
- ❌ Hardcoded value found — extract to environment variable

**Remind user:** "Set these in Railway dashboard → Variables tab. Never commit actual values."

### Step 4: Verify Build and Start Commands

```bash
# Node.js
cat package.json | grep -A2 '"scripts"' | grep -E '"(build|start|dev)"'

# Python
cat Procfile 2>/dev/null || cat pyproject.toml 2>/dev/null | grep -A5 '\[tool.poetry.scripts\]'
```

Verify:
- **Build command** exists and produces output (e.g., `npm run build` → `dist/` or `.next/`)
- **Start command** uses production mode (not `dev` or `nodemon`)
- **Port** reads from `process.env.PORT` or `os.environ["PORT"]` — Railway assigns this dynamically

**Flag if:** Start command uses hardcoded port (e.g., `app.listen(3000)` without PORT env fallback).

### Step 5: Verify Database Connection Strings

If the project uses a database:

```bash
# Search for connection patterns
grep -r "localhost:5432\|localhost:3306\|localhost:6379\|127.0.0.1" --include="*.ts" --include="*.js" --include="*.py" --include="*.env*" .
```

Railway internal networking rules:
- ✅ `${{Postgres.DATABASE_URL}}` — Railway reference variable
- ✅ `*.railway.internal:5432` — internal hostname (no egress cost)
- ❌ `localhost:5432` — won't resolve in Railway container
- ❌ Public Railway URL with port — adds latency, uses egress bandwidth

**Flag if:** Any hardcoded `localhost` or `127.0.0.1` database URLs found.

### Step 6: Check Health Check Endpoint

```bash
# Search for common health check patterns
grep -rn "\/health\|\/healthz\|\/api\/health\|\/readyz" --include="*.ts" --include="*.js" --include="*.py" .
```

If no health endpoint exists, recommend adding one:

```typescript
// Express/Fastify pattern
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'ok', timestamp: new Date().toISOString() });
});
```

Configure in Railway: Settings → Deploy → Health Check Path → `/health`

### Step 7: Pre-Deploy Checklist

Run the build locally to catch errors before deploying:

```bash
# Build test
npm run build  # or equivalent

# Search for localhost references
grep -rn "localhost\|127\.0\.0\.1" --include="*.ts" --include="*.js" --include="*.py" . | grep -v node_modules | grep -v .git
```

| Check | Command | Pass Criteria |
|-------|---------|--------------|
| Build passes | `npm run build` | Exit code 0, no errors |
| No hardcoded URLs | grep for localhost | Zero matches in source |
| Production env vars | Review .env.example | All vars documented |
| Port configuration | grep for PORT | Reads from env, not hardcoded |
| Node version | Check `engines` in package.json | Specified if needed |
| Git clean | `git status` | All changes committed |

**Output pre-deploy summary:**

```
🚂 Railway Deploy — Pre-flight Complete

Project: [name] ([type])
Build: ✅ passes
Env vars: ✅ 12 documented, verify in Railway dashboard
Database: ✅ uses Railway internal networking
Health check: ✅ /health endpoint configured
Localhost refs: ✅ none found
Port: ✅ reads from process.env.PORT

Ready to deploy. Run: railway up
```

### Step 8: Post-Deploy Verification

After deployment completes:

1. **Health check:** `curl https://[app].up.railway.app/health`
2. **Logs:** Check Railway dashboard → Deployments → View Logs for startup errors
3. **Database:** Verify migrations ran (check logs for migration output)
4. **Environment:** Confirm `NODE_ENV=production` is active

**Rollback plan:**
- Railway keeps previous deployments. Go to Deployments → click previous successful deploy → Rollback
- Or via CLI: `railway rollback`

**If deploy fails:**
1. Check build logs first — dependency or build script errors
2. Check runtime logs — missing env vars show as undefined/null errors
3. Check health check timeout — app may be starting slowly (increase timeout in Settings)
4. Verify Railway service is connected to correct GitHub branch

## Level History

- **Lv.1** — Base: Project detection, env var verification, build validation, database connection checks, health endpoint, pre/post-deploy checklists. Based on AdminStack, DeedStack, AlgoStack, and EpsteinScan Railway deployments. (Origin: MemStack Pro v3.2, Mar 2026)
