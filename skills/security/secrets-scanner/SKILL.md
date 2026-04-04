---
name: memstack-security-secrets-scanner
description: "Use this skill when the user says 'scan for secrets', 'check for leaked keys', 'secrets scanner', 'hardcoded credentials', 'API key leak', or needs to detect exposed secrets in source code. Do NOT use for dependency vulnerabilities or RLS auditing."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---


# 🔑 Secrets Scanner — Scanning for Exposed Credentials...
*Scan a codebase for hardcoded secrets, leaked API keys, and credential exposure across files and git history.*

## Activation

When this skill activates, output:

`🔑 Secrets Scanner — Scanning for Exposed Credentials...`

Then execute the protocol below.

## Context Guard

| Context | Status |
|---------|--------|
| **User asks to scan for secrets/keys** | ACTIVE — full scan |
| **User mentions credential exposure** | ACTIVE — full scan |
| **User asks about .env security** | ACTIVE — targeted .env audit |
| **Pre-deployment security review** | ACTIVE — full scan |
| **User is creating .env files** | DORMANT — let them work |

## Protocol

### Step 1: Scan for Hardcoded Secrets (Check 1)

Search all tracked files for strings matching known secret patterns:

**API Key Patterns:**
```bash
# Stripe
grep -rn "sk_live_[a-zA-Z0-9]\{20,\}\|sk_test_[a-zA-Z0-9]\{20,\}\|pk_live_[a-zA-Z0-9]\{20,\}" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.json" --include="*.md" --include="*.yaml" --include="*.yml" .

# Supabase
grep -rn "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9\." --include="*.ts" --include="*.tsx" --include="*.js" .

# AWS
grep -rn "AKIA[0-9A-Z]\{16\}" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.json" --include="*.env*" .

# GitHub tokens
grep -rn "ghp_[a-zA-Z0-9]\{36\}\|gho_[a-zA-Z0-9]\{36\}\|github_pat_[a-zA-Z0-9_]\{30,\}" .

# Slack tokens
grep -rn "xoxb-[0-9]\{10,\}\|xoxp-[0-9]\{10,\}\|xoxs-[0-9]\{10,\}" .

# Generic high-entropy strings assigned to obvious secret variables
grep -rn "api_key\s*=\s*['\"][a-zA-Z0-9]\{20,\}['\"]\|apiKey\s*[:=]\s*['\"][a-zA-Z0-9]\{20,\}['\"]" .
```

**Authentication Patterns:**
```bash
# Bearer tokens hardcoded
grep -rn "Bearer [a-zA-Z0-9_\-\.]\{20,\}" --include="*.ts" --include="*.tsx" --include="*.js" .

# Passwords in code
grep -rn "password\s*[:=]\s*['\"][^'\"]\{4,\}['\"]\|PASSWORD\s*=\s*['\"][^'\"]\{4,\}['\"]" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.json" .
```

**Private Keys:**
```bash
# RSA/EC/DSA/OpenSSH private keys
grep -rn "BEGIN.*PRIVATE KEY\|BEGIN RSA PRIVATE\|BEGIN EC PRIVATE\|BEGIN DSA PRIVATE\|BEGIN OPENSSH PRIVATE" \
  --include="*.ts" --include="*.tsx" --include="*.js" --include="*.json" --include="*.pem" --include="*.key" --include="*.yaml" --include="*.yml" --include="*.md" .
```
Flag as CRITICAL if found in any tracked file. Private keys should never be committed — use environment variables or secret managers.

**Base64-Encoded Secrets:**
```bash
# Look for base64-encoded strings assigned to secret-like variables
# These are often used to obfuscate secrets in source code
grep -rn "\(secret\|key\|token\|password\|credential\).*['\"][ ]*[A-Za-z0-9+/]\{40,\}=*['\"]" \
  --include="*.ts" --include="*.tsx" --include="*.js" --include="*.json" .

# Check for Buffer.from(... 'base64') with hardcoded strings
grep -rn "Buffer\.from(['\"][A-Za-z0-9+/]\{20,\}=*['\"].*base64\|atob(['\"][A-Za-z0-9+/]\{20,\}" \
  --include="*.ts" --include="*.tsx" --include="*.js" .
```
Flag as WARNING if a base64 string is assigned to a variable with `secret`, `key`, `token`, or `password` in its name. Developers sometimes base64-encode secrets thinking it hides them — it doesn't.

**Connection Strings:**
```bash
# Database URLs with credentials
grep -rn "postgres://[^:]\+:[^@]\+@\|mysql://[^:]\+:[^@]\+@\|mongodb://[^:]\+:[^@]\+@\|redis://:[^@]\+@" .

# Supabase/Firebase URLs with keys inline
grep -rn "supabase\.co.*service_role\|firebaseio\.com.*AIza" --include="*.ts" --include="*.tsx" --include="*.js" .
```

**Exclude false positives:**
- Files in `node_modules/`, `.git/`, `dist/`, `.next/`
- Test fixtures with obviously fake values (e.g., `sk_test_fake123`)
- Environment variable references (`process.env.STRIPE_SECRET_KEY` is safe — the variable itself, not a value)
- Documentation showing example formats

### Step 2: Audit .env File Security (Check 2)

**Check if .env files are gitignored:**
```bash
# Are .env files in .gitignore?
grep -n "\.env" .gitignore

# Are any .env files currently tracked?
git ls-files | grep -i "\.env"

# Were .env files ever committed?
git log --all --diff-filter=A --name-only --pretty=format: | grep -i "\.env" | sort -u
```

**Flag as CRITICAL if:**
- `.env` or `.env.local` is currently tracked by git
- `.env` was previously committed (secrets in git history even if now removed)
- `.gitignore` does not contain `.env` patterns

**Check .env.example exists:**
- Should contain all required env var names with placeholder values
- Should NOT contain real secrets (scan for patterns from Check 1)

### Step 3: Scan Config and Documentation Files (Check 3)

Secrets often leak into files developers don't think about:

```bash
# Check CLAUDE.md, README, docs
grep -rn "sk_\|pk_\|AKIA\|ghp_\|password\s*[:=]" *.md docs/ CLAUDE.md README.md 2>/dev/null

# Check config files
grep -rn "sk_\|pk_\|AKIA\|secret\|password\|token" \
  --include="*.json" --include="*.yaml" --include="*.yml" --include="*.toml" \
  --exclude-dir=node_modules .

# Check CI/CD config files
grep -rn "sk_\|pk_\|AKIA\|password\|token" \
  .github/workflows/*.yml .gitlab-ci.yml Dockerfile docker-compose*.yml 2>/dev/null
```

**Flag as CRITICAL** if real secrets found in any committed documentation or config.

### Step 3b: Scan Deployment Platform Configs (Check 3b)

Secrets can leak into platform-specific deployment configurations:

```bash
# Netlify config
grep -rn "password\|secret\|token\|api_key\|AKIA\|sk_\|pk_" \
  netlify.toml netlify.yml 2>/dev/null

# Vercel config
grep -rn "password\|secret\|token\|api_key\|AKIA\|sk_\|pk_" \
  vercel.json .vercel/project.json 2>/dev/null

# Railway config
grep -rn "password\|secret\|token\|api_key" \
  railway.json railway.toml 2>/dev/null

# Render config
grep -rn "password\|secret\|token\|api_key" \
  render.yaml 2>/dev/null

# Fly.io config
grep -rn "password\|secret\|token\|api_key" \
  fly.toml 2>/dev/null
```

**Flag as CRITICAL if:**
- Real secret values are hardcoded in any deployment config file
- `netlify.toml` `[build.environment]` section contains secret values (these are committed to git — use Netlify UI environment variables instead)
- `vercel.json` contains environment variable values (use `vercel env` CLI or Dashboard instead)

**Flag as WARNING if:**
- Deployment configs reference environment variable names without values (usually OK, but verify the names match what's configured in the platform)

### Step 4: Check Environment Variable Usage (Check 4)

Verify env vars are validated at application startup:

**Search for unvalidated env var usage:**
```bash
# Direct process.env usage without validation
grep -rn "process\.env\.\(.*SECRET\|.*KEY\|.*TOKEN\|.*PASSWORD\|.*DATABASE_URL\)" \
  --include="*.ts" --include="*.tsx" --include="*.js" .
```

**Flag as WARNING if:**
- `process.env.SECRET_NAME` used directly without checking if defined
- No env validation library (e.g., `@t3-oss/env-nextjs`, `envalid`, `zod` env schema)
- Missing env vars would cause runtime errors instead of startup errors

**Correct pattern:**
```typescript
// Good — validated at startup
import { z } from 'zod';
const env = z.object({
  DATABASE_URL: z.string().url(),
  STRIPE_SECRET_KEY: z.string().startsWith('sk_'),
}).parse(process.env);
```

### Step 5: Check Client-Side Secret Exposure (Check 5)

Server-only secrets must never reach the browser:

**Search for secrets in client code:**
```bash
# In React/Next.js, only NEXT_PUBLIC_ vars are safe for client
grep -rn "process\.env\." --include="*.tsx" --include="*.jsx" \
  src/app/ src/components/ src/pages/ app/ components/ pages/ 2>/dev/null \
  | grep -v "NEXT_PUBLIC_"
```

**Flag as CRITICAL if:**
- `SUPABASE_SERVICE_ROLE_KEY` referenced in client components
- `STRIPE_SECRET_KEY` (not `STRIPE_PUBLISHABLE_KEY`) in client code
- `DATABASE_URL` in client code
- Any non-`NEXT_PUBLIC_` env var in files under `app/`, `components/`, `pages/` (client-rendered paths)

**Flag as WARNING if:**
- API keys passed as props from server to client components
- Secrets embedded in client-side API calls via headers

### Step 6: Scan Git History (Check 6)

Previously committed secrets remain in git history even after removal:

```bash
# Search git history for known secret patterns
git log -p --all -S "sk_live" --oneline -- "*.ts" "*.tsx" "*.js" "*.json" "*.env" 2>/dev/null | head -20
git log -p --all -S "AKIA" --oneline 2>/dev/null | head -20
git log -p --all -S "ghp_" --oneline 2>/dev/null | head -20
git log -p --all -S "password" --oneline -- "*.env" "*.env.*" 2>/dev/null | head -20
```

**Flag as CRITICAL if:**
- Any real secret pattern found in git history
- .env files appear in historical commits

**Remediation for exposed history:**
1. Rotate the exposed credential immediately
2. Use `git filter-branch` or `BFG Repo-Cleaner` to purge from history
3. Force-push the cleaned history (coordinate with team)

### Step 7: Check Docker/Container Files (Check 7)

```bash
# Secrets in Dockerfiles
grep -rn "ENV.*SECRET\|ENV.*KEY\|ENV.*PASSWORD\|ENV.*TOKEN\|ARG.*SECRET" \
  Dockerfile* docker-compose*.yml 2>/dev/null

# Secrets passed as build args
grep -rn "build-arg.*secret\|build-arg.*key\|build-arg.*password" \
  Dockerfile* .github/workflows/*.yml 2>/dev/null
```

**Flag as CRITICAL if:**
- Secrets hardcoded in Dockerfile ENV instructions
- Secrets in docker-compose.yml without using Docker secrets or env_file

**Flag as WARNING if:**
- Secrets passed as Docker build args (visible in image layers)

### Step 8: Generate Report

```
🔑 Secrets Scanner Report
Project: <project-name>
Files scanned: <count>
Git history checked: <yes/no>

## Findings

| # | File | Line | Type | Pattern | Risk | Status |
|---|------|------|------|---------|------|--------|
| 1 | src/lib/stripe.ts | 14 | Stripe Secret Key | sk_live_... | 🔴 CRIT | Hardcoded |
| 2 | .env | — | Environment File | .env tracked | 🔴 CRIT | In git |
| 3 | docker-compose.yml | 23 | Database Password | password= | ⚠️ WARN | Inline |
| 4 | src/app/page.tsx | 8 | Server Env in Client | DATABASE_URL | 🔴 CRIT | Client-exposed |
| 5 | README.md | 45 | API Key Example | sk_test_... | ℹ️ INFO | Test key |

## Critical Issues
1. **Stripe secret key hardcoded** in `src/lib/stripe.ts:14`
   → Fix: Move to `.env.local` as `STRIPE_SECRET_KEY`, reference via `process.env.STRIPE_SECRET_KEY`
   → Then: Rotate the key in Stripe Dashboard immediately — it's been committed

2. **.env file tracked in git**
   → Fix: `git rm --cached .env && echo ".env" >> .gitignore && git commit`
   → Then: Rotate ALL credentials that were in the .env file

3. **DATABASE_URL in client component**
   → Fix: Move database access to server-side API route or Server Component

## Git History
- ⚠️ Found `sk_live_` pattern in commit `a1b2c3d` (2024-03-15)
  → Credential was removed but remains in history
  → Fix: Rotate the key, then clean history with BFG Repo-Cleaner

## Environment File Audit
- .gitignore: ✅ Contains .env patterns
- .env tracked: 🔴 Yes — remove immediately
- .env.example: ⚠️ Missing — create with placeholder values
- Env validation: ⚠️ No startup validation found

## Summary
- 🔴 Critical: <count>
- ⚠️ Warning: <count>
- ℹ️ Info: <count>
- Files with secrets: <count>
- Git history exposures: <count>
```

### Step 9: Generate .env.example

If no `.env.example` exists, offer to create one:

```bash
# Extract all env var names from the codebase
grep -roh "process\.env\.[A-Z_]\+" --include="*.ts" --include="*.tsx" --include="*.js" . \
  | sort -u \
  | sed 's/process\.env\.//' \
  > /tmp/env_vars.txt
```

Generate `.env.example` with all discovered variables and placeholder values:
```
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# Stripe
STRIPE_SECRET_KEY=sk_test_your-key
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_your-key
STRIPE_WEBHOOK_SECRET=whsec_your-secret
```

### Step 10: Pre-Rotation Checklist

Before rotating any exposed credential, verify:

1. **Is the secret actively used in production?** Check deployment environment variables (Vercel/Netlify/Railway dashboard) to see if the exposed value matches what's currently configured. If the production value is already different, the exposure is historical only — still rotate, but priority is lower.
2. **What services depend on this secret?** A Stripe key rotation affects webhook verification, payment processing, and customer portal links. Map all dependencies before rotating.
3. **Can you rotate without downtime?** Some services (Stripe, AWS) support rolling two active keys simultaneously. Others (single JWT secret) require coordinated deployment.
4. **Who else has access?** If the repo is public or shared with contractors, assume the secret is fully compromised regardless of git history depth.

**Rotation priority:**
| Secret Type | Urgency | Reason |
|-------------|---------|--------|
| Payment keys (Stripe, Square) | Immediate | Financial fraud risk |
| Database credentials | Immediate | Full data access |
| Auth secrets (JWT, session) | Immediate | Session hijacking |
| API keys (SendGrid, OpenAI) | High | Abuse/cost risk |
| Monitoring tokens (Sentry, Datadog) | Medium | Limited blast radius |
| Internal service keys | Medium | Depends on what they access |

### Step 11: Provide Recommendations

Always conclude with:

1. **Rotate** any exposed credentials immediately — assume they've been compromised (see pre-rotation checklist above)
2. **Add `.env` patterns to `.gitignore`** before any new commits
3. **Create `.env.example`** with placeholder values for onboarding
4. **Use env validation** (`@t3-oss/env-nextjs` or Zod schema) to catch missing vars at startup
5. **Store secrets in CI/CD** environment variables (Vercel, GitHub Actions secrets), never in code
6. **Use `NEXT_PUBLIC_` prefix** only for values safe to expose to browsers
7. **Clean git history** if secrets were previously committed (`BFG Repo-Cleaner`)

## Risk Levels

| Level | Meaning | Action |
|-------|---------|--------|
| 🔴 CRITICAL | Live secret exposed in code or git history | Rotate immediately, then fix |
| ⚠️ WARNING | Weak secret hygiene or missing safeguards | Fix before next deploy |
| ℹ️ INFO | Test/example keys or minor hygiene issue | Review and confirm acceptable |
| ✅ OK | Properly managed | No action needed |

## Secret Pattern Reference

| Pattern | Service | Example |
|---------|---------|---------|
| `sk_live_*` / `sk_test_*` | Stripe Secret | `sk_live_51J...` |
| `pk_live_*` / `pk_test_*` | Stripe Publishable | `pk_live_51J...` |
| `whsec_*` | Stripe Webhook | `whsec_abc...` |
| `AKIA*` (20 chars) | AWS Access Key | `AKIAIOSFODNN7EXAMPLE` |
| `ghp_*` (36 chars) | GitHub PAT | `ghp_xxxxxxxxxxxx` |
| `gho_*` | GitHub OAuth | `gho_xxxxxxxxxxxx` |
| `github_pat_*` | GitHub Fine-grained PAT | `github_pat_11A...` |
| `xoxb-*` | Slack Bot Token | `xoxb-123-456-abc` |
| `xoxp-*` | Slack User Token | `xoxp-123-456-abc` |
| `SG.*` (69 chars) | SendGrid | `SG.xxxxxxxxxx` |
| `eyJhbGci*` | JWT (Supabase/Auth) | `eyJhbGciOiJIUzI1...` |
| `sk-*` (48+ chars) | OpenAI API Key | `sk-abc123...` |
| `Bearer *` | Auth Header | `Bearer eyJ...` |
| `-----BEGIN RSA PRIVATE KEY-----` | RSA Private Key | PEM block |
| `-----BEGIN EC PRIVATE KEY-----` | EC Private Key | PEM block |
| `-----BEGIN OPENSSH PRIVATE KEY-----` | SSH Private Key | OpenSSH format |
| Base64 in secret var | Obfuscated secret | `c2VjcmV0X2tleQ==` |

## Automated Hook Coverage

The MemStack Pro hook system provides **automatic, production-grade secrets detection** before every commit and push — no manual invocation required.

**Pre-Commit Hook** — Scans all staged files before any `git commit`. Detects 700+ credential formats across every major cloud provider, SaaS API, private key format, and authentication token type. Blocks the commit if secrets are found, with redacted output showing what was detected and where.

**Pre-Push Hook** — Full working-tree scan before any `git push`. Catches secrets that may have been committed across multiple commits since the last push. Also detects `.env` files in unpushed commits.

**Coverage includes:**
- Cloud provider credentials (AWS, GCP, Azure, DigitalOcean, Hetzner, etc.)
- Payment platform keys (Stripe, Square, Braintree, PayPal)
- SaaS API tokens (GitHub, GitLab, Slack, Discord, Twilio, SendGrid, Mailchimp, etc.)
- Database connection strings with embedded credentials
- Private keys (RSA, EC, DSA, OpenSSH, PGP)
- JWT tokens, Bearer tokens, OAuth secrets
- Base64-encoded and obfuscated credentials
- CI/CD tokens, container registry credentials
- Custom high-entropy string detection

**Fallback behavior:** If the production scanner is not installed, hooks silently fall back to the built-in 5-keyword regex scan (Step 1 patterns). Scanning is never skipped — only the depth of detection changes.

This manual skill remains available for **deep audits** — git history analysis, client-side exposure checks, env validation, Docker inspection, and remediation planning that go beyond what automated hooks cover.

## Related Skills

- **api-audit** — Audit API routes for auth/authz vulnerabilities
- **rls-checker** — Audit Supabase RLS policies
- **dependency-audit** — Check for vulnerable npm packages

## Level History

- **Lv.1** — Base: 7-check scan (hardcoded secrets, .env audit, config/docs, env validation, client exposure, git history, Docker), pattern reference for 14+ secret formats, .env.example generation, remediation guide. Derived from real credential incidents across AdminStack, EpsteinScan, and 10+ production projects. (Origin: MemStack Pro v1.0, Mar 2026)
- **Lv.2** — Audit feedback: Added deployment platform config scan (Netlify, Vercel, Railway, Render, Fly.io), base64-encoded secret detection, private key block detection (RSA/EC/DSA/OpenSSH PEM), pre-rotation checklist with dependency mapping and priority matrix. (Origin: AdminStack audit, Mar 2026)
- **Lv.3** — Hook integration: Documented automated pre-commit and pre-push hook coverage (700+ credential formats), fallback behavior, and relationship between manual skill audits and automated hook scanning. (Origin: MemStack Pro v3.3.3, Mar 2026)

## Pro Feature

Pro: Secrets scanning hooks run automatically before every commit and push, covering 700+ credential formats across every major cloud provider and API service. Free version requires manual scanning only.
