---
name: memstack-security-csp-headers
description: "Use this skill when the user says 'CSP', 'Content-Security-Policy', 'security headers', 'HSTS', 'X-Frame-Options', 'clickjacking', 'unsafe-inline', 'unsafe-eval', or needs to audit, generate, or fix HTTP security headers for a web application. Do NOT use for API route audits or dependency scanning."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# 🛡️ CSP Headers — Security Headers Auditor & Generator
*Audit existing security headers, identify overly permissive directives, and generate a production-ready Content-Security-Policy with companion headers.*

## Activation

When this skill activates, output:

`🛡️ CSP Headers — Auditing your security headers...`

| Context | Status |
|---------|--------|
| **User says "CSP", "security headers", "Content-Security-Policy"** | ACTIVE |
| **User wants to fix unsafe-inline, unsafe-eval, or wildcard directives** | ACTIVE |
| **User mentions HSTS, X-Frame-Options, or Permissions-Policy** | ACTIVE |
| **User wants a full OWASP security audit (not just headers)** | DORMANT — see owasp-top10 |
| **User wants to scan for secrets in code** | DORMANT — see secrets-scanner |
| **User wants API-level security (auth, rate limiting)** | DORMANT — see api-audit |

## Protocol

### Step 1: Gather Inputs

Ask the user for:
- **Framework**: Next.js, Express, Fastify, Nginx, Caddy, static hosting?
- **CDN/hosting**: Vercel, Netlify, Cloudflare, self-hosted?
- **External resources**: Which third-party scripts, fonts, images, or APIs are loaded? (analytics, payment widgets, CDNs)
- **Inline scripts**: Does the app use inline `<script>` tags or inline styles?
- **Iframes**: Does the app embed iframes or get embedded by others?

### Step 2: Scan Existing Headers

Check for CSP and security headers in all possible locations:

**Where to look:**
1. **Middleware** — Express/Next.js middleware setting response headers
2. **Config files** — `next.config.js` (`headers()` function), `nginx.conf`, `Caddyfile`
3. **Meta tags** — `<meta http-equiv="Content-Security-Policy" content="...">` in HTML
4. **Hosting config** — `vercel.json`, `netlify.toml`, `_headers` file
5. **Reverse proxy** — Nginx/Caddy/Apache header directives

```
── EXISTING HEADERS FOUND ─────────────────

Location: [file:line or "not found"]

Content-Security-Policy:
  [current policy or "MISSING"]

Strict-Transport-Security:
  [current value or "MISSING"]

X-Content-Type-Options:
  [current value or "MISSING"]

X-Frame-Options:
  [current value or "MISSING"]

Referrer-Policy:
  [current value or "MISSING"]

Permissions-Policy:
  [current value or "MISSING"]

X-XSS-Protection:
  [current value or "MISSING — deprecated but still useful for older browsers"]
```

### Step 3: Audit CSP Directives

If a CSP exists, audit each directive for security issues:

| Directive | Current Value | Issue | Severity | Fix |
|-----------|--------------|-------|----------|-----|
| `default-src` | `*` | Allows loading from any origin | 🔴 Critical | Restrict to known origins |
| `script-src` | `'unsafe-inline'` | Allows inline scripts — XSS vector | 🔴 Critical | Use nonces or hashes |
| `script-src` | `'unsafe-eval'` | Allows dynamic code execution — injection risk | 🟡 High | Remove, refactor code |
| `style-src` | `'unsafe-inline'` | Allows inline styles — less severe | 🟠 Medium | Use nonces if feasible |
| `img-src` | `*` | Allows images from any origin | 🟠 Medium | Restrict to known CDNs |
| `frame-ancestors` | missing | No clickjacking protection | 🟡 High | Add `'self'` or `'none'` |
| `connect-src` | missing | No restriction on fetch/XHR targets | 🟠 Medium | Restrict to API origins |
| `base-uri` | missing | Base tag injection possible | 🟡 High | Add `'self'` |
| `form-action` | missing | Forms can submit to any origin | 🟠 Medium | Add `'self'` |
| `object-src` | missing | Plugin content allowed | 🟡 High | Add `'none'` |

**Common dangerous patterns:**
```
BAD:  default-src *                    → Defeats the entire purpose of CSP
BAD:  script-src 'unsafe-inline'       → XSS protection nullified
BAD:  script-src 'unsafe-eval'         → Dynamic code execution permitted
BAD:  script-src https:                → Any HTTPS origin can serve scripts
BAD:  script-src *.googleapis.com      → JSONP endpoints can bypass CSP
BAD:  connect-src *                    → Data exfiltration unrestricted
BAD:  frame-ancestors not set          → Clickjacking possible
```

### Step 4: Inventory External Resources

Identify all external resources the application loads:

```
── RESOURCE INVENTORY ─────────────────────

Scripts (script-src):
  - https://www.googletagmanager.com    — Google Tag Manager
  - https://js.stripe.com               — Stripe.js
  - https://cdn.jsdelivr.net             — jsDelivr CDN
  - 'self'                               — Own domain scripts

Styles (style-src):
  - https://fonts.googleapis.com         — Google Fonts CSS
  - 'self'                               — Own stylesheets
  - 'unsafe-inline'                      — Needed for: [reason]

Fonts (font-src):
  - https://fonts.gstatic.com            — Google Fonts files
  - 'self'                               — Self-hosted fonts

Images (img-src):
  - https://res.cloudinary.com           — Cloudinary images
  - https://*.githubusercontent.com      — GitHub avatars
  - data:                                — Data URI images
  - 'self'                               — Own images

Connections (connect-src):
  - https://api.example.com              — Own API
  - https://api.stripe.com               — Stripe API
  - https://www.google-analytics.com     — Analytics
  - 'self'                               — Same-origin requests

Frames (frame-src):
  - https://js.stripe.com                — Stripe checkout iframe
  - https://www.youtube.com              — Embedded videos
  - 'none'                               — If no iframes needed
```

### Step 5: Generate Recommended CSP

Build a CSP policy based on actual resource usage:

```
── RECOMMENDED CSP ────────────────────────

Content-Security-Policy:
  default-src 'self';
  script-src 'self' 'nonce-{SERVER_GENERATED}' https://www.googletagmanager.com https://js.stripe.com;
  style-src 'self' 'nonce-{SERVER_GENERATED}' https://fonts.googleapis.com;
  font-src 'self' https://fonts.gstatic.com;
  img-src 'self' https://res.cloudinary.com data:;
  connect-src 'self' https://api.stripe.com https://www.google-analytics.com;
  frame-src https://js.stripe.com https://www.youtube.com;
  frame-ancestors 'self';
  base-uri 'self';
  form-action 'self';
  object-src 'none';
  upgrade-insecure-requests;
```

**Nonce-based script loading (recommended over 'unsafe-inline'):**

```javascript
// Express/Next.js middleware example
const crypto = require('crypto');

function cspMiddleware(req, res, next) {
  const nonce = crypto.randomBytes(16).toString('base64');
  res.locals.cspNonce = nonce;

  res.setHeader('Content-Security-Policy', [
    "default-src 'self'",
    `script-src 'self' 'nonce-${nonce}'`,
    `style-src 'self' 'nonce-${nonce}'`,
    "font-src 'self' https://fonts.gstatic.com",
    "img-src 'self' data:",
    "connect-src 'self'",
    "frame-ancestors 'self'",
    "base-uri 'self'",
    "form-action 'self'",
    "object-src 'none'",
    "upgrade-insecure-requests",
  ].join('; '));

  next();
}
```

```html
<!-- Use nonce in script/style tags -->
<script nonce="<%= cspNonce %>">
  // Inline script allowed by nonce
</script>
```

**Hash-based alternative (for static inline scripts):**
```bash
# Generate hash for a known inline script
echo -n "console.log('hello')" | openssl dgst -sha256 -binary | openssl enc -base64
# Result: 'sha256-xxxxxxxxx'
# Add to CSP: script-src 'sha256-xxxxxxxxx'
```

### Step 6: Generate Companion Security Headers

CSP alone isn't enough. Generate the full security headers suite:

```
── COMPLETE SECURITY HEADERS ──────────────

# HSTS — Force HTTPS for all future visits
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload

# Prevent MIME type sniffing attacks
X-Content-Type-Options: nosniff

# Clickjacking protection (legacy — frame-ancestors in CSP is preferred)
X-Frame-Options: SAMEORIGIN

# Control referrer information leakage
Referrer-Policy: strict-origin-when-cross-origin

# Restrict browser features
Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=self

# Legacy XSS filter (deprecated but harmless)
X-XSS-Protection: 0
```

**Header explanations:**

| Header | Purpose | Recommended Value |
|--------|---------|-------------------|
| `Strict-Transport-Security` | Force HTTPS, prevent SSL stripping | `max-age=63072000; includeSubDomains; preload` |
| `X-Content-Type-Options` | Prevent MIME sniffing (serving JS as image) | `nosniff` |
| `X-Frame-Options` | Prevent clickjacking (legacy, CSP preferred) | `SAMEORIGIN` or `DENY` |
| `Referrer-Policy` | Control referer header leakage | `strict-origin-when-cross-origin` |
| `Permissions-Policy` | Disable unused browser APIs | Disable camera, mic, geo unless needed |
| `X-XSS-Protection` | Legacy XSS filter | `0` (disable — can cause issues, CSP is better) |

### Step 7: Report-Only Mode

Always deploy CSP in report-only mode first to avoid breaking production:

```
── DEPLOYMENT STRATEGY ────────────────────

Phase 1: REPORT-ONLY (1-2 weeks)
  Header: Content-Security-Policy-Report-Only
  Purpose: Collect violations without blocking anything
  Report endpoint: /api/csp-report

Phase 2: ENFORCE (after zero violations)
  Header: Content-Security-Policy
  Purpose: Block unauthorized resources
  Keep report-uri for ongoing monitoring
```

**Report-only header:**
```
Content-Security-Policy-Report-Only:
  [same policy as above];
  report-uri /api/csp-report;
  report-to csp-endpoint
```

**Violation report handler:**
```javascript
// POST /api/csp-report
app.post('/api/csp-report', express.json({ type: 'application/csp-report' }), (req, res) => {
  const report = req.body['csp-report'];
  console.warn('CSP Violation:', {
    blockedUri: report['blocked-uri'],
    directive: report['violated-directive'],
    documentUri: report['document-uri'],
    sourceFile: report['source-file'],
    lineNumber: report['line-number'],
  });
  res.status(204).end();
});
```

**Common violations to expect:**
- Browser extensions injecting scripts (ignore — not your code)
- Inline styles from third-party libraries (add nonce or hash)
- Data URIs for images (add `data:` to `img-src` if needed)
- Dynamic code execution in legacy libraries (refactor or whitelist as last resort)

### Step 8: Framework-Specific Implementation

**Next.js (`next.config.js`):**
```javascript
const securityHeaders = [
  { key: 'Content-Security-Policy', value: "default-src 'self'; ..." },
  { key: 'Strict-Transport-Security', value: 'max-age=63072000; includeSubDomains; preload' },
  { key: 'X-Content-Type-Options', value: 'nosniff' },
  { key: 'X-Frame-Options', value: 'SAMEORIGIN' },
  { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
  { key: 'Permissions-Policy', value: 'camera=(), microphone=(), geolocation=()' },
];

module.exports = {
  async headers() {
    return [{ source: '/(.*)', headers: securityHeaders }];
  },
};
```

**Express middleware:**
```javascript
app.use((req, res, next) => {
  res.setHeader('Content-Security-Policy', "default-src 'self'; ...");
  res.setHeader('Strict-Transport-Security', 'max-age=63072000; includeSubDomains; preload');
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'SAMEORIGIN');
  res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
  res.setHeader('Permissions-Policy', 'camera=(), microphone=(), geolocation=()');
  next();
});
```

**Nginx:**
```nginx
add_header Content-Security-Policy "default-src 'self'; ..." always;
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Permissions-Policy "camera=(), microphone=(), geolocation=()" always;
```

**Caddy:**
```
header {
    Content-Security-Policy "default-src 'self'; ..."
    Strict-Transport-Security "max-age=63072000; includeSubDomains; preload"
    X-Content-Type-Options "nosniff"
    X-Frame-Options "SAMEORIGIN"
    Referrer-Policy "strict-origin-when-cross-origin"
    Permissions-Policy "camera=(), microphone=(), geolocation=()"
}
```

**Vercel (`vercel.json`):**
```json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "Content-Security-Policy", "value": "default-src 'self'; ..." },
        { "key": "Strict-Transport-Security", "value": "max-age=63072000; includeSubDomains; preload" },
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "X-Frame-Options", "value": "SAMEORIGIN" },
        { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" },
        { "key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=()" }
      ]
    }
  ]
}
```

### Step 9: Output

Present the complete security headers audit and configuration:

```
━━━ SECURITY HEADERS REPORT ━━━━━━━━━━━━━━
Project: [name]
Framework: [framework]
Hosting: [platform]

── AUDIT RESULTS ──────────────────────────
Headers found: [X] of 6
Issues found: [count]
  🔴 Critical: [count]
  🟡 High:     [count]
  🟠 Medium:   [count]

── ISSUES ─────────────────────────────────
[directive-level audit table]

── RESOURCE INVENTORY ─────────────────────
[categorized external resources]

── RECOMMENDED CSP ────────────────────────
[complete CSP policy]

── COMPANION HEADERS ──────────────────────
[HSTS, X-Content-Type-Options, etc.]

── IMPLEMENTATION ─────────────────────────
[framework-specific config, copy-paste ready]

── DEPLOYMENT PLAN ────────────────────────
Phase 1: Report-only ([duration])
Phase 2: Enforce (after zero violations)
Report endpoint: [handler code]

── SECURITY SCORE ─────────────────────────
Score: [A+ / A / B / C / D / F]
  CSP:              [pass/fail]
  HSTS:             [pass/fail]
  X-Content-Type:   [pass/fail]
  X-Frame-Options:  [pass/fail]
  Referrer-Policy:  [pass/fail]
  Permissions:      [pass/fail]
```

**Grading:**
- A+: All headers present, CSP with nonces, no unsafe directives
- A: All headers present, minor CSP weaknesses
- B: Most headers present, some unsafe directives
- C: CSP present but overly permissive
- D: Missing critical headers
- F: No security headers at all

## Inputs
- Framework / hosting platform
- External resource list (scripts, fonts, APIs, CDNs)
- Inline script/style usage
- Iframe embedding requirements
- Existing CSP or security headers (auto-scanned)

## Outputs
- Existing headers audit with directive-level issues
- External resource inventory categorized by CSP directive
- Generated CSP policy based on actual resource usage
- Nonce-based inline script/style implementation
- Complete companion security headers suite
- Framework-specific implementation code (Next.js, Express, Nginx, Caddy, Vercel)
- Report-only deployment plan with violation handler
- Security headers grade (A+ through F)

## Level History

- **Lv.1** — Base: CSP directive audit with severity classification, external resource inventory, nonce/hash-based inline script handling, companion headers suite (HSTS, X-Content-Type-Options, X-Frame-Options, Referrer-Policy, Permissions-Policy), framework-specific implementations (Next.js, Express, Nginx, Caddy, Vercel), report-only deployment strategy, security grade. (Origin: MemStack v3.2, Mar 2026)
