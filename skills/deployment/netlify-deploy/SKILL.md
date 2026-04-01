---
name: memstack-deployment-netlify-deploy
description: "Use this skill when the user says 'deploy to Netlify', 'Netlify setup', 'netlify-deploy', or needs to deploy a static site or serverless functions to Netlify with build configuration and custom domains. Do NOT use for Railway, Vercel, or VPS deployments."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# 🌐 Netlify Deploy — Pre-flight check and deploy to Netlify...
*Validates build config, redirects, environment variables, and deployment readiness for Netlify static/SPA hosting.*

## Activation

When this skill activates, output:

`🌐 Netlify Deploy — Running pre-flight checks...`

Then execute the protocol below.

| Context | Status |
|---------|--------|
| User says "deploy to netlify" or "netlify deploy" | ACTIVE |
| User says "deploy frontend" or "deploy static site" | ACTIVE |
| Preparing a React/Vue/Svelte/Next.js static export for hosting | ACTIVE |
| Deploying a backend service or API server | DORMANT — use railway-deploy |
| Discussing Netlify pricing or features generally | DORMANT |

### Anti-patterns

| Trap | Reality Check |
|------|---------------|
| "I'll configure it in the Netlify UI" | `netlify.toml` is version-controlled and portable. UI settings get lost across teams. |
| "Redirects work fine without _redirects" | SPA routing breaks on refresh without `/* /index.html 200`. Every SPA needs this. |
| "Environment vars are the same everywhere" | Build-time vars (baked into JS bundle) vs runtime vars (Netlify Functions) are different. `NEXT_PUBLIC_` prefix exposes to client. |
| "The API proxy just works" | `/api/*` redirects must point to your actual backend URL. Forgetting to update after backend redeploy breaks the frontend. |
| "I'll check the deploy after pushing" | `netlify deploy --build` locally catches build failures before they hit production. Always build locally first. |

## Protocol

### Step 1: Check Build Configuration

Look for Netlify config and verify build settings:

```bash
# Check for Netlify configuration
ls netlify.toml _redirects _headers 2>/dev/null

# Check package.json for build script
cat package.json | grep -A2 '"scripts"' | grep '"build"'
```

If `netlify.toml` exists, verify it:

```toml
# Expected structure
[build]
  command = "npm run build"    # or "yarn build", "pnpm build"
  publish = "dist"             # or "build", "out", ".next" (varies by framework)

[build.environment]
  NODE_VERSION = "20"          # Pin Node version for reproducible builds
```

| Framework | Build Command | Publish Directory |
|-----------|--------------|-------------------|
| React (CRA) | `npm run build` | `build` |
| React (Vite) | `npm run build` | `dist` |
| Next.js (static) | `next build && next export` | `out` |
| Vue | `npm run build` | `dist` |
| Svelte/SvelteKit | `npm run build` | `build` |
| Astro | `npm run build` | `dist` |
| Plain HTML | — | `.` or `public` |

**Flag if:** `netlify.toml` missing or publish directory doesn't match framework default.

### Step 2: Verify Redirects and API Proxy

```bash
# Check redirect files
cat netlify.toml 2>/dev/null | grep -A5 '\[\[redirects\]\]'
cat _redirects 2>/dev/null
```

Check for the API proxy pattern (frontend → backend):

```toml
# netlify.toml — API proxy to Railway/external backend
[[redirects]]
  from = "/api/*"
  to = "https://your-backend.up.railway.app/api/:splat"
  status = 200
  force = true
```

Or in `_redirects`:
```
/api/*  https://your-backend.up.railway.app/api/:splat  200
```

**Verify:**
- ✅ Backend URL is the production URL (not localhost)
- ✅ `status = 200` (proxy, not redirect — preserves the URL for the client)
- ✅ `force = true` if the proxy should override static files at the same path
- ❌ Backend URL still points to `localhost:3000` — update to production

**Flag if:** Code references `/api/` paths but no proxy redirect is configured.

### Step 3: Verify SPA Routing

Single-page apps need a catch-all redirect so deep links and page refreshes work:

```bash
# Check for SPA redirect
grep -r "\/\*.*\/index\.html\|\/\*.*200" netlify.toml _redirects 2>/dev/null
```

Required for SPAs (React Router, Vue Router, etc.):

```
# In _redirects (must be LAST rule — order matters)
/*  /index.html  200
```

Or in `netlify.toml`:
```toml
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

**Flag if:** Project uses client-side routing but no catch-all redirect exists. Symptoms: pages work when navigated to via links, but return 404 on direct URL access or refresh.

**Note:** Next.js static export handles this differently — each page is pre-rendered as its own HTML file. SPA redirect is NOT needed for static Next.js.

### Step 4: Verify Environment Variables

```bash
# Find env vars used in frontend code
grep -rn "process\.env\.\|import\.meta\.env\.\|VITE_\|NEXT_PUBLIC_\|REACT_APP_" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" . | grep -v node_modules
```

**Build-time vs runtime separation:**

| Prefix | Framework | When Available | Exposed to Client? |
|--------|-----------|---------------|-------------------|
| `REACT_APP_` | CRA | Build time | ⚠️ YES — baked into JS bundle |
| `NEXT_PUBLIC_` | Next.js | Build time | ⚠️ YES — baked into JS bundle |
| `VITE_` | Vite | Build time | ⚠️ YES — baked into JS bundle |
| No prefix | Any | Build time only | ❌ No — server-side/build scripts only |

**Critical security check:**
```bash
# Search for secrets that might be exposed to client
grep -rn "NEXT_PUBLIC_.*SECRET\|NEXT_PUBLIC_.*KEY\|VITE_.*SECRET\|REACT_APP_.*SECRET" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.env*" . | grep -v node_modules
```

**Flag if:** Any secret (API keys with write access, database URLs, auth secrets) uses a client-exposed prefix. These are baked into the JavaScript bundle and visible to anyone who opens DevTools.

**Output:** List each variable with where to set it:
- Netlify UI: Site Settings → Environment Variables (for secrets)
- `netlify.toml` `[build.environment]` (for non-sensitive build config like `NODE_VERSION`)

### Step 5: Check Custom Domain and SSL

```bash
# Check for domain configuration
cat netlify.toml 2>/dev/null | grep -A5 '\[context\]'
```

Verify in Netlify dashboard:
- ✅ Custom domain added (Domain Management → Add domain)
- ✅ DNS points to Netlify (CNAME to `*.netlify.app` or A record to Netlify load balancer)
- ✅ SSL certificate provisioned (automatic via Let's Encrypt — check HTTPS section)
- ✅ Force HTTPS enabled (redirects http → https)
- ✅ www redirect configured (www → apex or apex → www — pick one, be consistent)

**Flag if:** Domain is added but DNS hasn't propagated or SSL shows "Waiting for DNS verification."

### Step 6: Check for Netlify Functions

```bash
# Check for serverless functions
ls netlify/functions/ functions/ 2>/dev/null
cat netlify.toml 2>/dev/null | grep 'functions'
```

If functions exist, verify:
- Function directory is specified in `netlify.toml`: `[functions] directory = "netlify/functions"`
- Functions have correct export pattern: `export const handler = async (event, context) => { ... }`
- Environment variables needed by functions are set in Netlify dashboard (these are runtime, not build-time)
- Functions are not importing large dependencies that exceed Netlify's 50MB bundle limit

### Step 7: Check Headers Configuration

```bash
# Check for security headers
cat netlify.toml 2>/dev/null | grep -A10 '\[\[headers\]\]'
cat _headers 2>/dev/null
```

Recommended security headers:

```toml
# netlify.toml
[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
    Permissions-Policy = "camera=(), microphone=(), geolocation=()"
```

### Step 8: Pre-Deploy Checklist

Build locally to catch errors before Netlify builds:

```bash
# Local build test
npm run build

# Check output directory exists and has content
ls -la dist/  # or build/, out/, etc.

# Check for common issues
grep -rn "http://localhost\|http://127\.0\.0\.1" dist/ 2>/dev/null
```

| Check | Command | Pass Criteria |
|-------|---------|--------------|
| Build passes | `npm run build` | Exit code 0, no errors |
| Output directory exists | `ls dist/` | Has index.html and assets |
| No localhost in build | grep dist/ for localhost | Zero matches |
| _redirects in output | `ls dist/_redirects` | Exists if using _redirects approach |
| Env vars documented | Check .env.example | All client vars listed |
| No secrets in client code | grep for exposed secrets | Zero matches |
| Git clean | `git status` | All changes committed |

**Output pre-deploy summary:**

```
🌐 Netlify Deploy — Pre-flight Complete

Project: [name] ([framework])
Build: ✅ passes → [publish directory]
Redirects: ✅ SPA routing + API proxy configured
Env vars: ✅ 8 build-time vars, no secrets exposed
Domain: ✅ [domain] with SSL
Functions: ✅ 2 functions in netlify/functions/
Headers: ✅ security headers configured

Ready to deploy.
  Preview:    netlify deploy --build
  Production: netlify deploy --build --prod
```

### Step 9: Post-Deploy Verification

After deployment completes:

1. **Preview deploy:** Netlify generates a unique URL for every deploy — test there first
2. **Check build log:** Netlify dashboard → Deploys → click deploy → Build Log
3. **Test SPA routing:** Navigate directly to a deep route (e.g., `/dashboard/settings`) — should load, not 404
4. **Test API proxy:** Open DevTools Network tab, trigger an API call, verify it reaches backend
5. **Check SSL:** Visit `https://[domain]` — padlock should appear, no mixed content warnings
6. **Test redirects:** Visit `http://[domain]` — should redirect to `https://`

**Rollback plan:**
- Netlify keeps every deploy as an immutable snapshot
- Dashboard → Deploys → click any previous deploy → "Publish deploy"
- Instant rollback, no rebuild required

## Level History

- **Lv.1** — Base: Build config validation, redirect/proxy verification, SPA routing, env var security audit, domain/SSL checks, Netlify Functions, security headers, pre/post-deploy checklists. Based on AdminStack marketing site, GreenAcres frontend, and other Netlify deployments. (Origin: MemStack Pro v3.2, Mar 2026)
