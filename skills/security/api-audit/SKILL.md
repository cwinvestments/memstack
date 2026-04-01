---
name: memstack-security-api-audit
description: "Use this skill when the user says 'audit API', 'check API security', 'API routes security', 'endpoint audit', 'check my routes', or needs to verify API route protection. Reviews API endpoints for authentication, authorization, and input validation gaps. Do NOT use for frontend security headers or dependency scanning."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---


# 🛡️ API Audit — Checking API Route Security...
*Audit Next.js API routes for authentication, authorization, validation, and common vulnerabilities.*

## Activation

When this skill activates, output:

`🛡️ API Audit — Checking API Route Security...`

Then execute the protocol below.

## Context Guard

| Context | Status |
|---------|--------|
| **User asks to audit/check API routes** | ACTIVE — full audit |
| **User mentions API security** | ACTIVE — full audit |
| **User asks about endpoint protection** | ACTIVE — full audit |
| **User is writing a new API route** | DORMANT — let them finish first |
| **Non-Next.js project** | DORMANT — not applicable (adapt if Express/Fastify detected) |

## Protocol

### Step 1: Discover API Routes

Find all API route files in the project:

1. **App Router (Next.js 13+):**
   ```bash
   find . -path "*/app/api/*/route.ts" -o -path "*/app/api/*/route.js"
   ```
   Each file exports named functions: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`.

2. **Pages Router (legacy):**
   ```bash
   find . -path "*/pages/api/*.ts" -o -path "*/pages/api/*.js"
   ```
   Each file exports a default handler.

3. **Middleware:**
   ```bash
   find . -name "middleware.ts" -o -name "middleware.js" | head -5
   ```
   Check if global auth middleware exists (reduces per-route auth requirements).

4. **Server Actions (Next.js 14+):**
   ```
   grep -r "'use server'" --include="*.ts" --include="*.tsx" -l
   ```
   Server actions are also attack surface — treat as API routes. For each server action function, verify it performs authentication before accessing data. Server actions are callable from any client component and receive no automatic auth — they are functionally identical to unauthenticated POST endpoints unless the function explicitly calls `getSession()`, `getAuthContext()`, or equivalent.

Compile a list of all routes with their HTTP methods and file paths.

### Step 2: Check Authentication (Check 1)

For each route, determine if it verifies the caller is authenticated:

**Search for auth patterns in each route file:**
- `getAuthContext` / `getSession` / `getServerSession` / `auth()` — framework auth
- `getToken` / `verifyToken` / `jwt.verify` — manual JWT
- `cookies().get` with session validation — cookie-based auth
- `headers().get('authorization')` with validation — bearer token
- `createRouteHandlerClient` / `createServerComponentClient` — Supabase auth

**Classify each route:**
| Status | Meaning |
|--------|---------|
| ✅ Authenticated | Auth check found before data access |
| 🔴 No Auth | No authentication pattern detected |
| ℹ️ Public | Route is intentionally public (webhooks, health checks, public data) |
| ⚠️ Middleware-only | Auth handled by middleware — verify matcher covers this route |

**Flag as CRITICAL** if a route performs database writes or returns user-specific data with no auth.

**Known public route patterns** (classify as ℹ️ INFO, not CRITICAL):
- `/api/health`, `/api/status` — health checks
- `/api/webhooks/*` — external webhooks (need signature verification instead)
- `/api/auth/*` — auth flow endpoints (login, callback, register)
- `/api/public/*` — explicitly named public routes
- `/api/cron/*` — cron jobs (need secret verification instead)

### Step 3: Check Authorization (Check 2)

For authenticated routes, verify they check *what* the user can access:

**Search for authorization patterns:**
- `verifyOrgAccess` / `checkOrgMembership` / `requireRole` — org-level authz
- Comparing `user.id` against resource `user_id` / `owner_id` — ownership check
- Role checks: `user.role === 'admin'` or similar
- Supabase RLS (may handle authz at database layer — note as INFO)

**Flag as WARNING if:**
- Route fetches data by ID from params without ownership verification
- Route accepts `organization_id` from request body instead of deriving from session
- Multi-tenant route returns data without org scope filter
- DELETE route has no ownership check

**Pattern to enforce:**
```typescript
// BAD — trusts client-provided org ID
const { orgId } = await req.json();
const data = await db.from('documents').select().eq('org_id', orgId);

// GOOD — derives org from authenticated session
const { orgId } = await getAuthContext(req);
const data = await db.from('documents').select().eq('org_id', orgId);
```

### Step 4: Check Input Validation (Check 3)

For routes that accept request body or query params:

**Search for validation patterns:**
- `z.object` / `z.string()` / `.parse(` / `.safeParse(` — Zod
- `Joi.object` / `.validate(` — Joi
- `yup.object` / `.validate(` — Yup
- `body.` or `req.json()` followed by manual type checks — weak validation

**Flag as WARNING if:**
- Route reads `req.json()` or `request.body` without schema validation
- Route uses query params in database queries without validation
- Route passes user input directly to external APIs

**Flag as CRITICAL if:**
- Route uses dynamic code execution with user input (see Check 5)
- Route constructs file paths from user input without sanitization

### Step 5: Check Rate Limiting (Check 4)

For public-facing routes:

**Search for rate limiting patterns:**
- `rateLimit` / `rateLimiter` / `limiter` imports
- `@upstash/ratelimit` — serverless rate limiting
- `X-RateLimit` header setting
- Middleware-level rate limiting (check `middleware.ts`)

**Flag as WARNING if:**
- Login/register routes have no rate limiting (brute force risk)
- Public data endpoints have no rate limiting (scraping/abuse risk)
- Webhook endpoints have no rate limiting (replay attack risk)

### Step 5b: Check Request Size Limits (Check 4b)

For POST/PUT/PATCH routes that accept request bodies:

**Search for size enforcement patterns:**
- `Content-Length` header checks before parsing body
- `bodyParser` config with `sizeLimit` option
- `export const config = { api: { bodyParser: { sizeLimit: '...' } } }` — Next.js Pages Router
- Next.js App Router: check if `request.text()` / `request.json()` is called without upstream size limits
- Middleware-level body size restrictions

**Flag as WARNING if:**
- Routes that accept file uploads, JSON bodies, or form data have no explicit size limit
- No global body size limit configured in middleware or framework config
- A route reads `await request.json()` on an unbounded body — a malicious client can send gigabytes of JSON, causing memory exhaustion (DoS)

**Note:** Next.js App Router does NOT enforce a default body size limit on route handlers. Unlike the Pages Router (which defaults to 1MB via `bodyParser`), App Router passes the raw request through. Projects must enforce limits explicitly.

**Correct pattern:**
```typescript
// Check Content-Length before parsing
const contentLength = parseInt(request.headers.get('content-length') || '0');
if (contentLength > 1_000_000) { // 1MB
  return NextResponse.json({ error: 'Request too large' }, { status: 413 });
}
const body = await request.json();
```

### Step 5c: Check Idempotency Keys (Check 4c)

For routes that create payments, charges, transfers, or financial transactions:

**Search for idempotency patterns:**
- `idempotencyKey` / `idempotency_key` / `Idempotency-Key` header
- Stripe: `stripe.paymentIntents.create({}, { idempotencyKey: ... })` — built-in support
- Square: `idempotency_key` field in request bodies — built-in support
- Custom: checking for duplicate request IDs before processing

**Identify payment mutation routes:**
Search for routes that call:
- `stripe.paymentIntents.create`, `stripe.charges.create`, `stripe.invoices.pay`
- `stripe.checkout.sessions.create`, `stripe.subscriptions.create`
- `squareClient.payments.create`, `squareClient.orders.create`
- Any route that inserts into `invoices`, `payments`, `orders`, or `transactions` tables

**Flag as WARNING if:**
- Payment-creating routes don't use idempotency keys — network retries can cause duplicate charges
- Routes that create financial records have no duplicate-request protection

**Correct pattern:**
```typescript
// Stripe — pass idempotency key from client or generate deterministically
const session = await stripe.checkout.sessions.create(
  { ... },
  { idempotencyKey: `order-${orderId}-${timestamp}` }
);
```

### Step 6: Check SQL Injection (Check 5)

**Search for dangerous query patterns:**
- Template literals in raw SQL strings with interpolated variables — CRITICAL
- String concatenation in queries: `"SELECT * FROM " + table` — CRITICAL
- `.rpc()` calls with unsanitized user input — WARNING
- Raw SQL via `prisma.$queryRawUnsafe` or `sql.unsafe` — CRITICAL

**Safe patterns** (do not flag):
- Parameterized queries with tagged templates (Prisma)
- Supabase client `.from().select().eq()` chain — safe by design
- Prepared statements with `$1, $2` placeholders

### Step 7: Check Data Exposure (Check 6)

**Search for sensitive data in responses:**
- Returning full user objects: `return NextResponse.json(user)` — may include password hash
- Returning `select('*')` results without column filtering — WARNING
- Logging request bodies that may contain passwords — WARNING
- Returning internal IDs, database errors, or stack traces — WARNING

**Fields that should never appear in API responses:**
`password`, `password_hash`, `hashed_password`, `secret`, `token`, `refresh_token`, `api_key`, `private_key`, `ssn`, `credit_card`

Search each route file for these field names, then check if they appear in return/response paths.

### Step 8: Check CORS Configuration (Check 7)

**Search for CORS patterns:**
- `Access-Control-Allow-Origin: *` — overly permissive (WARNING)
- `Access-Control-Allow-Credentials: true` with wildcard origin — CRITICAL
- Missing CORS headers on routes that need cross-origin access — INFO
- `next.config.js` headers configuration for CORS

**Check `next.config.js` or `next.config.mjs`:**
```
grep -A5 "Access-Control\|headers\(\)" next.config.*
```

### Step 9: Check Error Handling (Check 8)

**Search for error patterns in each route:**
- Bare `catch (e) { return NextResponse.json(e) }` — leaks stack traces (WARNING)
- `catch (e) { return NextResponse.json({ error: e.message }) }` — leaks internal errors (WARNING)
- No try/catch around database operations — unhandled errors become 500s with stack traces (WARNING)
- `console.error` with full error objects in production — log exposure (INFO)

**Correct pattern:**
```typescript
catch (error) {
  console.error('Route /api/items failed:', error);
  return NextResponse.json(
    { error: 'Internal server error' },
    { status: 500 }
  );
}
```

### Step 10: Check Webhook & Special Routes (Check 9)

**For webhook routes** (`/api/webhooks/*`):
- Stripe: must call `stripe.webhooks.constructEvent(body, sig, secret)` — CRITICAL if missing
- GitHub: must verify `X-Hub-Signature-256` header
- Generic: must verify shared secret or HMAC signature
- Must use raw body (`req.text()` not `req.json()`) for signature verification

**For file upload routes:**
- Must enforce file size limits — WARNING if missing
- Must validate file type / MIME type — WARNING if missing
- Must not store uploads in publicly accessible paths without auth — CRITICAL

**For DELETE routes:**
- Must verify resource ownership before deletion — CRITICAL if missing
- Should use soft delete pattern where appropriate — INFO

### Step 11: Generate Report

```
🛡️ API Security Audit Report
Project: <project-name>
Routes found: <count>
Server actions: <count>
Global middleware auth: <yes/no>

## Route Audit

| Route | Method | Auth | Authz | Validation | Risk | Issues |
|-------|--------|------|-------|------------|------|--------|
| /api/users | GET | ✅ | ✅ | ✅ | ✅ OK | — |
| /api/users | POST | ✅ | ✅ | 🔴 | ⚠️ WARN | No input validation |
| /api/items/[id] | DELETE | 🔴 | 🔴 | — | 🔴 CRIT | No auth, no ownership check |
| /api/webhooks/stripe | POST | ℹ️ | — | — | ✅ OK | Signature verified |
| /api/admin/users | GET | ✅ | ⚠️ | ✅ | ⚠️ WARN | No role check for admin route |

## Critical Issues
1. **DELETE /api/items/[id]** — No authentication. Any request can delete any item.
   → Fix: Add `getAuthContext(req)` and verify `item.user_id === user.id` before deleting.

2. **POST /api/upload** — No file size limit. Server vulnerable to resource exhaustion.
   → Fix: Add size limit config or check `Content-Length` header.

## Warnings
1. **POST /api/users** — Request body parsed without schema validation.
   → Fix: Add Zod schema and parse before processing.

2. **GET /api/admin/users** — Authenticated but no admin role verification.
   → Fix: Add role check before returning data.

## Info
1. **Supabase RLS active** — Authorization may be handled at database layer for some routes.
   Verify RLS policies cover the same access patterns. Run `rls-checker` for full RLS audit.

## Summary
- 🔴 Critical: <count>
- ⚠️ Warning: <count>
- ℹ️ Info: <count>
- ✅ OK: <count>
- Total routes: <count>

## Checklist
- [ ] All non-public routes authenticate callers
- [ ] All data-access routes verify ownership/org membership
- [ ] All POST/PUT/PATCH routes validate input with schema
- [ ] Login/register routes have rate limiting
- [ ] Webhook routes verify signatures
- [ ] No raw SQL with user input
- [ ] API responses exclude sensitive fields
- [ ] Error responses don't leak stack traces
- [ ] CORS configured for specific origins, not wildcard
- [ ] POST/PUT/PATCH routes enforce request body size limits
- [ ] Payment-creating routes use idempotency keys
- [ ] Server actions verify auth before data access
```

### Step 12: Suggest Fixes

For each CRITICAL and WARNING issue, provide:
1. The exact code fix with file path and line number
2. Any new dependencies needed (e.g., `@upstash/ratelimit` for rate limiting)
3. Whether the fix requires changes to other files (middleware, types, etc.)

Offer to apply fixes directly if the user approves.

## Risk Levels

| Level | Meaning | Action |
|-------|---------|--------|
| 🔴 CRITICAL | Active vulnerability exploitable without auth | Fix immediately |
| ⚠️ WARNING | Missing defense layer or weak pattern | Fix before production |
| ℹ️ INFO | Acceptable pattern worth verifying | Review and confirm intentional |
| ✅ OK | Properly secured | No action needed |

## Related Skills

- **rls-checker** — Audit Supabase RLS policies (database-level security)
- **secrets-scanner** — Find exposed API keys and credentials
- **owasp-top10** — Full OWASP Top 10 vulnerability assessment

## Level History

- **Lv.1** — Base: Route discovery (App Router, Pages Router, Server Actions, middleware), 9-point analysis (auth, authz, validation, rate limiting, SQLi, data exposure, CORS, error handling, webhooks/uploads/deletes), structured report with risk levels, inline fix suggestions. Patterns derived from AdminStack (getAuthContext, verifyOrgAccess) and 10+ production Next.js apps. (Origin: MemStack Pro v1.0, Mar 2026)
- **Lv.2** — Audit feedback: Added request body size limit check (App Router has no default limit), idempotency key check for payment mutations (Stripe/Square), Server Actions auth verification (callable from any client, no automatic auth). (Origin: AdminStack audit, Mar 2026)
