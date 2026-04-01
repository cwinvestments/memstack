---
name: memstack-security-owasp-top10
description: "Use this skill when the user says 'OWASP audit', 'OWASP top 10', 'security audit', 'vulnerability assessment', 'full security check', or needs a comprehensive web application security review against OWASP Top 10 categories. Do NOT use for dependency audits or secret scanning alone."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---


# 🛡️ OWASP Top 10 — Running Full Vulnerability Assessment...
*Audit a web application against the OWASP Top 10 (2021) vulnerability categories with actionable findings and remediation.*

## Activation

When this skill activates, output:

`🛡️ OWASP Top 10 — Running Full Vulnerability Assessment...`

Then execute the protocol below.

## Context Guard

| Context | Status |
|---------|--------|
| **User asks for OWASP/security audit** | ACTIVE — full assessment |
| **User asks for vulnerability check** | ACTIVE — full assessment |
| **Pre-launch security review** | ACTIVE — full assessment |
| **User asks about a specific OWASP category** | ACTIVE — targeted check for that category |
| **User is actively fixing a vulnerability** | DORMANT — let them work |

## Scan Modes

This skill supports two modes. Default to **deep scan** unless the user specifies otherwise.

| Mode | Scope | When to use |
|------|-------|-------------|
| **Quick scan** | A01 (auth), A05 (headers + config), A06 (deps) | Fast pre-deploy check, CI pipeline gate, or first-pass triage |
| **Deep scan** | All 10 categories | Pre-launch review, security audit, compliance check |

If the user says "quick OWASP", "quick security check", or "fast scan", run only A01 + A05 + A06 and output the scorecard with the other 7 categories marked as "⏭️ SKIPPED (quick mode)".

## Protocol

Run each of the 10 checks below (or A01 + A05 + A06 only in quick mode). For each, search the codebase for vulnerability patterns, classify findings, and record results for the final scorecard.

**Finding format:** Every finding MUST include a file path and line number in the format `file:line`. If a finding is project-wide (e.g., "no rate limiting anywhere"), reference the most relevant file where the fix would be applied. Vague findings like "missing HSTS" without pointing to the middleware or config file are not actionable.

---

### A01: Broken Access Control

**Risk:** Users acting beyond their intended permissions — accessing other users' data, elevating privileges, or bypassing access restrictions.

**Detection:**

1. **Missing auth on routes:**
   Find all API route files, then check each for authentication patterns (`getAuthContext`, `getSession`, `auth()`, or equivalent).

2. **Insecure Direct Object References (IDOR):**
   Search for routes that take an ID parameter (`params.id`, `params.userId`, `params.orgId`) and fetch data without verifying the authenticated user owns or has access to the referenced resource.

3. **Privilege escalation:**
   Search for role checks (`role.*admin`, `isAdmin`, `requireRole`). Verify admin-only operations actually enforce role checks, not just rely on route naming.

4. **CORS bypass:**
   Search for `Access-Control-Allow-Origin` headers. Flag wildcard (`*`) with credentials enabled.

**Cross-reference:** Run `api-audit` (Checks 1-2) for detailed route-by-route auth analysis.

**Remediation:**
- Add auth middleware to all non-public routes
- Always derive user/org context from session, never from request parameters
- Implement RBAC (Role-Based Access Control) for admin operations
- Deny by default — explicitly allow, don't explicitly deny

---

### A02: Cryptographic Failures

**Risk:** Exposure of sensitive data due to weak or missing encryption.

**Detection:**

1. **Weak hashing:**
   Search for `md5`, `sha1`, `createHash('md5')`, `createHash('sha1')` in source files.
   MD5/SHA1 for passwords is CRITICAL. For checksums/cache keys it's acceptable (INFO).

2. **Unencrypted sensitive data:**
   Search for password assignment patterns. Verify passwords use bcrypt/argon2/scrypt, not plaintext or weak hashing.

3. **No HTTPS enforcement:**
   Check `next.config.js` or middleware for HTTPS redirect, `x-forwarded-proto` checks, `Strict-Transport-Security` header.

4. **Sensitive data in URLs:**
   Search for `token=`, `password=`, `secret=`, `key=` in URL/redirect/query string contexts.

**Remediation:**
- Use bcrypt/argon2 for password hashing (cost factor >= 10)
- Enforce HTTPS via HSTS header or middleware redirect
- Never pass secrets in query strings — use headers or POST body
- Encrypt sensitive data at rest (database-level or application-level)

---

### A03: Injection

**Risk:** Untrusted data sent to an interpreter as part of a command or query.

**Detection:**

1. **SQL injection:**
   Search for template literals with interpolated variables inside SQL query/execute calls. Search for string concatenation in SELECT/INSERT/UPDATE/DELETE statements.

2. **Cross-Site Scripting (XSS):**
   Search for `dangerouslySetInnerHTML`, `innerHTML`, `__html` in React/JSX files. Search for `v-html` in Vue files.

3. **Command injection:**
   Search for shell execution imports (`child_process`) and calls (`execSync`, `spawn`). Verify user input is never passed to shell commands. Use `execFile` with argument arrays instead.

4. **Dynamic code execution:**
   Search for `new Function(` with dynamic strings, `setTimeout`/`setInterval` with string arguments instead of function references. These allow arbitrary code execution if user input reaches them.

**Cross-reference:** Run `api-audit` (Check 5) for detailed SQL injection analysis.

**Remediation:**
- Use parameterized queries or ORM methods exclusively
- Use React's default JSX escaping — avoid `dangerouslySetInnerHTML`
- Sanitize HTML with DOMPurify if raw HTML rendering is required
- Never pass user input to shell execution — use `execFile()` with argument arrays

---

### A04: Insecure Design

**Risk:** Missing or ineffective security controls in the application's design.

**Detection:**

1. **Missing rate limits:**
   Search for `rateLimit`, `rateLimiter`, `@upstash/ratelimit` in source files. Flag login, registration, password reset, and public API routes with no rate limiting.

2. **No account lockout:**
   Search for login/signIn/authenticate handlers. Check if they track failed attempts.

3. **Predictable IDs:**
   Search for `autoIncrement`, `SERIAL`, `AUTO_INCREMENT` in SQL/migration files. Flag if sequential IDs are used for user-facing resources (IDOR enabler). UUIDs preferred.

4. **Missing CSRF protection:**
   Search for `csrf`, `csrfToken`, `x-csrf`, `SameSite` cookie attributes. Check if state-changing operations verify origin.

**Remediation:**
- Add rate limiting to auth endpoints (5 attempts/minute)
- Lock accounts after N failed login attempts with exponential backoff
- Use UUIDs for all user-facing resource IDs
- Enable CSRF protection via SameSite cookies and origin verification

---

### A05: Security Misconfiguration

**Risk:** Insecure default configs, debug mode in production, verbose error messages, missing security headers.

**Detection:**

1. **Debug mode / development settings:**
   Search for `debug.*true`, `DEBUG.*=.*1`, `NODE_ENV.*development` in source files, config, and env files (exclude `.example` files).

2. **Missing security headers:**
   Check `next.config.js` or middleware for these headers:
   - `X-Content-Type-Options: nosniff`
   - `X-Frame-Options: DENY` or `SAMEORIGIN`
   - `Strict-Transport-Security` (HSTS)
   - `Content-Security-Policy` (CSP)
   - `Referrer-Policy`
   - `Permissions-Policy`

3. **Default credentials:**
   Search for `admin:admin`, `root:root`, `password:password`, `default.*password` in source and config files.

4. **Verbose error responses:**
   Search for `.stack` or `.message` in response/return contexts. Verify stack traces are not sent to clients.

**Remediation:**
- Set security headers via `next.config.js` headers or middleware
- Never expose stack traces in production responses
- Remove default credentials from all configs
- Disable debug mode in production builds

---

### A06: Vulnerable and Outdated Components

**Risk:** Using libraries with known security vulnerabilities.

**Detection:**

```bash
# npm audit for known CVEs
npm audit --json 2>/dev/null | head -100

# Check for outdated packages
npm outdated 2>/dev/null | head -30
```

**Cross-reference CVE databases** for key dependencies:
1. Read `package.json` and identify the framework (Next.js, React, Express, etc.) and its exact version
2. Search for known CVEs against the exact version: check the framework's GitHub security advisories, changelog, or release notes for security fixes in newer versions
3. For each HIGH/CRITICAL finding from `npm audit`, extract the CVE ID (e.g., `GHSA-xxxx-xxxx-xxxx`) and note:
   - The vulnerability description
   - The affected version range
   - The fixed version
   - Whether it affects production or dev only
4. Check if the vulnerability is actually reachable — a CVE in an image optimizer only matters if the app uses image optimization

**Classify:**
- Critical CVEs in production dependencies → CRITICAL
- High CVEs in production dependencies → WARNING
- CVEs in devDependencies only → INFO
- Outdated but no CVEs → INFO
- CVE present but feature not used (e.g., image optimizer CVE but no images) → INFO with note

**Report each finding with:** `package@version` → `file:line` (where it's imported or configured, e.g., `package.json:15`), CVE ID, severity, fixed version.

**Remediation:**
- Run `npm audit fix` for automatic patching
- Manually update packages with breaking changes
- Replace deprecated packages with maintained alternatives
- Set up Dependabot or Renovate for automated updates

---

### A07: Identification and Authentication Failures

**Risk:** Weak authentication mechanisms allowing account compromise.

**Detection:**

1. **Weak password policy:**
   Search for password length/minimum constraints. Flag if minimum length < 8 or no complexity requirements.

2. **Missing MFA/2FA:**
   Search for `mfa`, `2fa`, `two.factor`, `totp`, `authenticator` in source files. Flag if no MFA implementation found for admin or sensitive operations.

3. **Session management:**
   Search for `maxAge`, `expires`, `session.*timeout`, `cookie.*options`. Check session duration, secure/httpOnly flags, SameSite attribute.

4. **Credential recovery:**
   Search for password reset flow. Check if it uses time-limited, single-use tokens.

**Remediation:**
- Enforce minimum 8-character passwords with complexity rules
- Implement MFA for admin accounts at minimum
- Set session cookies: `httpOnly: true, secure: true, sameSite: 'lax'`
- Use time-limited (< 1 hour), single-use password reset tokens

---

### A08: Software and Data Integrity Failures

**Risk:** Code and infrastructure that doesn't verify integrity of updates, data, or CI/CD pipelines.

**Detection:**

1. **Unsigned JWTs:**
   Search for `jwt`, `jsonwebtoken`, `jose` imports. Verify JWTs use strong algorithms (RS256/ES256 preferred, HS256 acceptable). Flag `algorithm: 'none'` as CRITICAL.

2. **Missing Content Security Policy:**
   Check for CSP headers in config or middleware.

3. **No Subresource Integrity on CDN scripts:**
   Search for `<script src="http` or `<link href="http` in HTML/JSX. External scripts loaded without `integrity` attribute are vulnerable to CDN compromise.

4. **CI/CD pipeline security:**
   Check GitHub Actions for unpinned actions (`uses: action@main` or `@master` or `@latest`). Actions should reference specific commit SHAs, not branches.

**Remediation:**
- Sign JWTs with RS256 or ES256 and validate signatures
- Add CSP headers restricting script/style/connect sources
- Add SRI `integrity` attributes to all CDN-loaded resources
- Pin GitHub Actions to specific commit SHAs

---

### A09: Security Logging and Monitoring Failures

**Risk:** Insufficient logging prevents detection of breaches and forensic analysis.

**Detection:**

1. **Audit logging implementation:**
   Go beyond searching for service name strings — verify actual audit logging coverage:

   a. **Find the audit infrastructure:** Search for `audit_log`, `audit_logs`, `auditLog`, `logAction`, `logEvent`, `activity_log` in source files AND migration/schema SQL files. Identify the audit table schema (columns, what gets logged).

   b. **Verify critical event coverage.** For each of these events, search for audit log writes (INSERT into audit table, or audit helper function calls) in the relevant route handlers:

   | Event | Where to check | Risk if missing |
   |-------|---------------|-----------------|
   | Login success/failure | `auth/login`, `auth/verify-2fa` | Can't detect brute force |
   | Account creation | `auth/register`, `auth/setup` | Can't detect rogue accounts |
   | Password change | `account/password`, `auth/reset-password` | Can't detect account takeover |
   | Permission/role change | Admin routes, role update handlers | Can't detect privilege escalation |
   | Data deletion | All DELETE handlers | Can't investigate data loss |
   | Admin impersonation | Impersonation routes | Can't audit admin abuse |
   | Payment events | Webhook handlers, checkout routes | Can't investigate fraud |
   | Settings change | Org/account settings update routes | Can't track config drift |

   c. **Check what's logged:** Verify audit entries include `who` (user ID), `what` (action), `when` (timestamp), `where` (IP address), and `target` (affected resource ID). Missing any of these fields reduces forensic value.

   Flag as WARNING if audit table exists but critical events are not logged.
   Flag as CRITICAL if no audit logging infrastructure exists at all.

2. **Error monitoring service:**
   Search for actual SDK initialization, not just string mentions:
   - Sentry: `Sentry.init(`, `@sentry/nextjs`, `@sentry/node` in package.json
   - LogRocket: `LogRocket.init(`
   - Datadog: `dd-trace`, `@datadog/browser-rum`
   - New Relic: `newrelic` in package.json
   - Custom: structured logging to external service via HTTP
   Flag if no error monitoring service is initialized (not just imported). `console.error` alone is insufficient for production — errors disappear when the container restarts.

3. **Sensitive data in logs:**
   Search for `console.log` combined with `password`, `token`, `secret`, or `body`. Flag logging of passwords, tokens, or full request bodies.

**Remediation:**
- Log all authentication events (success and failure)
- Log all access control failures
- Log all admin/privileged operations
- Use structured logging with timestamps and request IDs
- Send logs to a monitoring service (Sentry, Datadog, etc.)
- Never log sensitive data (passwords, tokens, PII)

---

### A10: Server-Side Request Forgery (SSRF)

**Risk:** Application fetches URLs provided by users without validation, enabling access to internal services.

**Detection:**

1. **Unvalidated URL fetching:**
   Search for `fetch(`, `axios.get`, `axios.post`, `got(`, `request(` calls. For each, check if the URL comes from user input (query params, request body, database).

2. **User-controlled redirects:**
   Search for `redirect`, `res.redirect`, `window.location` assignments. Verify redirect URLs are validated against an allowlist.

3. **Image/file proxy endpoints:**
   Search for `imageUrl`, `fileUrl`, `proxyUrl`, `downloadUrl` patterns. Endpoints that fetch external resources based on user input are SSRF vectors.

**Remediation:**
- Validate and allowlist URLs before fetching
- Block requests to internal IP ranges (10.x, 172.16-31.x, 192.168.x, 127.x, 169.254.x)
- Use URL parsing to verify hostname before fetching
- Set timeouts on all outbound requests
- Don't expose raw fetch responses — filter and transform

---

### Generate Scorecard

```
🛡️ OWASP Top 10 Scorecard
Project: <project-name>
Assessment date: <date>
Framework: <Next.js / Express / etc.>

| # | Category | Status | Findings | Risk |
|---|----------|--------|----------|------|
| A01 | Broken Access Control | 🔴 FAIL | 3 | Critical |
| A02 | Cryptographic Failures | ✅ PASS | 0 | — |
| A03 | Injection | ⚠️ PARTIAL | 1 | Warning |
| A04 | Insecure Design | ⚠️ PARTIAL | 2 | Warning |
| A05 | Security Misconfiguration | 🔴 FAIL | 4 | Critical |
| A06 | Vulnerable Components | ⚠️ PARTIAL | 5 | Warning |
| A07 | Auth Failures | ✅ PASS | 0 | — |
| A08 | Data Integrity Failures | ⚠️ PARTIAL | 1 | Warning |
| A09 | Logging Failures | 🔴 FAIL | 2 | Critical |
| A10 | SSRF | ✅ PASS | 0 | — |

Score: 4/10 categories passing
Critical issues: <count>
Warnings: <count>

## Priority Fixes
1. [CRITICAL] A01 — Add authentication to unprotected API routes
2. [CRITICAL] A05 — Add security headers (CSP, HSTS, X-Frame-Options)
3. [CRITICAL] A09 — Set up error monitoring (Sentry recommended)
4. [WARNING] A03 — Remove dangerouslySetInnerHTML in user content component
5. [WARNING] A04 — Add rate limiting to login endpoint
6. [WARNING] A06 — Run npm audit fix for vulnerable packages

## Detailed Findings
[For each finding, include ALL of these fields:]
- **Category:** A0X name
- **Location:** `file/path:line_number` (REQUIRED — never omit)
- **Description:** What the vulnerability is
- **Risk:** CRITICAL/WARNING/INFO with exploitability × impact classification
- **Fix:** Specific code change or configuration update

## Related Audits
- Run `api-audit` for detailed route-by-route security analysis
- Run `rls-checker` for Supabase database-level access control
- Run `secrets-scanner` for credential exposure check
- Run `dependency-audit` for deep package vulnerability analysis
```

## Remediation Priority Matrix

After generating findings, assign each a priority using exploitability × impact:

| | **Low Impact** | **Medium Impact** | **High Impact** |
|---|---|---|---|
| **Easy to exploit** (no auth needed, public endpoint) | Medium | High | **Critical** |
| **Moderate to exploit** (requires auth, specific conditions) | Low | Medium | High |
| **Hard to exploit** (requires admin, chain of bugs) | Info | Low | Medium |

**Examples:**
- Unauthenticated API route exposing PII → Easy × High = **Critical**
- Missing HSTS header → Easy × Low = **Medium** (browser handles most cases)
- Admin route without role check → Moderate × High = **High** (attacker needs valid session)
- devDependency CVE → Hard × Low = **Info** (not in production bundle)
- XSS in admin-only page → Moderate × Medium = **Medium** (limited audience)

Include the matrix classification in the Priority Fixes section of the scorecard: `[CRITICAL/HIGH/MEDIUM/LOW] A0X — description (exploitability × impact)`.

## Scoring Criteria

| Status | Meaning |
|--------|---------|
| ✅ PASS | No findings, or only INFO-level observations |
| ⚠️ PARTIAL | WARNING-level findings but no critical vulnerabilities |
| 🔴 FAIL | One or more CRITICAL findings in this category |

## Related Skills

- **api-audit** — Detailed per-route authentication and authorization analysis
- **rls-checker** — Supabase Row Level Security policy audit
- **secrets-scanner** — Credential and API key exposure scan
- **dependency-audit** — npm package vulnerability assessment
- **csp-headers** — Content Security Policy configuration guide

## Level History

- **Lv.1** — Base: Full OWASP Top 10 (2021) assessment with per-category detection patterns, codebase search instructions, classification criteria, remediation guidance, scorecard output, and cross-references to api-audit, rls-checker, and secrets-scanner. Covers Next.js, React, and Node.js patterns. (Origin: MemStack Pro v1.0, Mar 2026)
- **Lv.2** — Audit feedback: Added quick/deep scan modes (quick = A01+A05+A06), mandatory file:line on all findings, CVE cross-referencing for A06 (verify reachability, extract CVE IDs, note fixed versions), deep A09 logging check (verify actual audit_log table coverage for 8 critical event types instead of string-matching service names), remediation priority matrix (exploitability × impact). (Origin: AdminStack audit, Mar 2026)
