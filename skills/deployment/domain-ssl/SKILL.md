---
name: memstack-deployment-domain-ssl
description: "Use this skill when the user says 'setup domain', 'configure DNS', 'SSL certificate', 'domain-ssl', 'custom domain', 'HTTPS setup', or needs to configure DNS records, SSL certificates, and custom domains for any hosting provider. Do NOT use for full deployment workflows."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# 🔒 Domain & SSL — Verifying domain, DNS, and certificate configuration...
*Validates DNS records, SSL certificates, redirects, HSTS, and domain health across all managed properties.*

## Activation

When this skill activates, output:

`🔒 Domain & SSL — Running domain health checks...`

Then execute the protocol below.

| Context | Status |
|---------|--------|
| User says "check domain" or "setup domain" | ACTIVE |
| User says "SSL certificate" or "fix SSL" or "check DNS" | ACTIVE |
| Setting up a new domain for a deployed project | ACTIVE |
| Checking domain expiration or renewal status | ACTIVE |
| User is writing code, not managing infrastructure | DORMANT |
| Discussing domain names abstractly (brainstorming names) | DORMANT |

### Anti-patterns

| Trap | Reality Check |
|------|---------------|
| "SSL auto-renews, I don't need to check it" | Auto-renewal fails silently when DNS changes. Verify quarterly. |
| "DNS propagation takes 48 hours" | Most propagation happens in minutes. If it's been 2+ hours, something is misconfigured. |
| "www and non-www both work, that's fine" | Pick one canonical URL and redirect the other. Duplicate content hurts SEO and splits analytics. |
| "HTTPS is enough for security" | Without HSTS, the first request can still be intercepted. HSTS tells browsers to never try HTTP. |
| "I'll check the domain when it stops working" | By then, your site is down. Monitor expiration, SSL, and DNS proactively. |

## Protocol

### Step 1: Verify DNS Records

Check that DNS records are correctly configured for the target domain:

```bash
# A records (points domain to IP)
dig +short A example.com

# CNAME records (points subdomain to another domain)
dig +short CNAME www.example.com

# TXT records (verification, SPF, DKIM)
dig +short TXT example.com

# MX records (email routing — check for conflicts)
dig +short MX example.com

# NS records (authoritative nameservers)
dig +short NS example.com
```

**Expected patterns by hosting provider:**

| Provider | Record Type | Value |
|----------|------------|-------|
| Railway | CNAME | `*.up.railway.app` |
| Netlify | CNAME | `*.netlify.app` or A record to `75.2.60.5` |
| Vercel | CNAME | `cname.vercel-dns.com` or A record to `76.76.21.21` |
| Cloudflare (proxied) | A | Cloudflare IPs (check dashboard) |

**Check for conflicts:**
- ❌ A record AND CNAME on the same subdomain — CNAME takes precedence, A is ignored
- ❌ Multiple A records pointing to different providers — causes random routing
- ❌ Missing TXT record for domain verification — some providers require this

**Flag if:** DNS records don't match the expected hosting provider configuration.

### Step 2: Check SSL Certificate Status

```bash
# Check SSL certificate details
echo | openssl s_client -connect example.com:443 -servername example.com 2>/dev/null | openssl x509 -noout -dates -subject -issuer

# Check certificate chain
echo | openssl s_client -connect example.com:443 -servername example.com 2>/dev/null | openssl x509 -noout -text | grep -E "Issuer:|Not Before:|Not After:|Subject:"

# Quick expiration check
echo | openssl s_client -connect example.com:443 -servername example.com 2>/dev/null | openssl x509 -noout -enddate
```

**Verify:**
- ✅ Certificate is valid (not expired)
- ✅ Certificate covers the correct domain(s) — check Subject Alternative Names
- ✅ Certificate chain is complete (no missing intermediates)
- ✅ Auto-renewal is configured (Let's Encrypt certs expire every 90 days)
- ✅ Certificate issuer matches expected provider (Let's Encrypt, Cloudflare, AWS ACM)

**Renewal timeline:**
| Days Until Expiry | Status | Action |
|-------------------|--------|--------|
| > 30 days | ✅ Healthy | No action |
| 15–30 days | ⚠️ Warning | Verify auto-renewal is working |
| < 15 days | ❌ Critical | Manually trigger renewal immediately |
| Expired | 🚨 Down | Site showing security warnings to visitors |

### Step 3: Verify www vs non-www Redirect

Pick one canonical form and redirect the other:

```bash
# Test non-www → www (or vice versa)
curl -sI http://example.com | grep -i "location"
curl -sI http://www.example.com | grep -i "location"
curl -sI https://example.com | grep -i "location"
curl -sI https://www.example.com | grep -i "location"
```

**Expected redirect chain (non-www canonical):**
```
http://www.example.com  → 301 → https://example.com
http://example.com      → 301 → https://example.com
https://www.example.com → 301 → https://example.com
https://example.com     → 200 (canonical)
```

**Verify:**
- ✅ Only ONE canonical URL returns 200 — all others 301 redirect to it
- ✅ Redirects use 301 (permanent), not 302 (temporary) — 301 is cacheable and SEO-friendly
- ✅ Redirect chain is at most 1 hop (http://www → https://apex, not http://www → https://www → https://apex)
- ❌ Both www and non-www return 200 — duplicate content, split SEO

### Step 4: Check HSTS Headers

HTTP Strict Transport Security prevents SSL stripping attacks:

```bash
# Check for HSTS header
curl -sI https://example.com | grep -i "strict-transport-security"
```

**Expected:**
```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

| Directive | Purpose |
|-----------|---------|
| `max-age=31536000` | Browser remembers to use HTTPS for 1 year |
| `includeSubDomains` | Applies to all subdomains too |
| `preload` | Eligible for browser HSTS preload list (permanent HTTPS) |

**Warning:** `preload` is hard to undo. Only add it if you're committed to HTTPS permanently. Removing it requires submitting to the [HSTS preload removal list](https://hstspreload.org/) and waiting for browser updates.

**Flag if:** No HSTS header present, or `max-age` is too short (< 6 months / 15768000).

### Step 5: Verify DNS Propagation

After making DNS changes, verify propagation across global nameservers:

```bash
# Check propagation from multiple DNS resolvers
for dns in 8.8.8.8 1.1.1.1 208.67.222.222 9.9.9.9; do
  echo "=== $dns ==="
  dig +short A example.com @$dns
done
```

| DNS Resolver | Provider |
|-------------|----------|
| `8.8.8.8` | Google |
| `1.1.1.1` | Cloudflare |
| `208.67.222.222` | OpenDNS |
| `9.9.9.9` | Quad9 |

**Also check:** [dnschecker.org](https://dnschecker.org) for worldwide propagation view.

**Propagation timeline:**
| Record Type | Typical Propagation | Max Propagation |
|-------------|-------------------|-----------------|
| A / AAAA | 5–30 minutes | 48 hours |
| CNAME | 5–30 minutes | 48 hours |
| TXT | 5–60 minutes | 48 hours |
| NS | 24–48 hours | 72 hours |
| MX | 1–4 hours | 48 hours |

**Flag if:** Different DNS resolvers return different values after 2+ hours — likely a TTL issue or misconfigured record.

### Step 6: Check for Mixed Content

Mixed content (HTTP resources loaded on HTTPS pages) triggers browser security warnings:

```bash
# Scan built output for http:// references
grep -rn "http://" dist/ build/ out/ public/ 2>/dev/null | grep -v "http://localhost\|http://127\|http://schemas\|http://www.w3.org\|http://xmlns" | head -20

# Check HTML for mixed content
grep -rn 'src="http://\|href="http://\|url("http://' dist/ build/ out/ public/ 2>/dev/null | head -20

# Check for hardcoded HTTP API endpoints
grep -rn "http://" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" . | grep -v node_modules | grep -v "localhost\|127\.0\.0\|schemas\|w3\.org\|xmlns" | head -20
```

**Common mixed content sources:**
- ❌ Hardcoded `http://` image URLs — change to `https://` or protocol-relative `//`
- ❌ Third-party scripts loaded over HTTP — update to HTTPS CDN URL
- ❌ API endpoints using `http://` — update to `https://`
- ❌ CSS `url()` references with `http://` — update to `https://`
- ✅ `http://localhost` in development code — acceptable, won't appear in production build

**Flag if:** Any `http://` references found in production build output (excluding localhost and XML namespaces).

### Step 7: Domain Monitoring Checklist

Proactive monitoring prevents surprise outages:

```bash
# Check WHOIS for expiration (if whois is available)
whois example.com | grep -i "expir"

# Quick SSL expiry check
echo | openssl s_client -connect example.com:443 -servername example.com 2>/dev/null | openssl x509 -noout -enddate
```

| Check | Frequency | What to Verify |
|-------|-----------|---------------|
| Domain expiration | Monthly | Auto-renew enabled, registrar payment method valid |
| SSL certificate | Monthly | Valid, auto-renewing, > 30 days until expiry |
| DNS records | After any change | Records match expected values, propagation complete |
| HSTS header | Quarterly | Present with adequate max-age |
| Mixed content | After deploys | No HTTP resources on HTTPS pages |
| Registrar access | Quarterly | Login works, 2FA enabled, recovery email current |
| Nameserver delegation | After registrar changes | NS records point to correct DNS provider |

**Domain inventory — track for each property:**
```
Domain:       example.com
Registrar:    [Namecheap / GoDaddy / Cloudflare / Google Domains]
Auto-renew:   [Yes / No]
Expires:      [YYYY-MM-DD]
DNS provider: [Cloudflare / Registrar / Route53]
SSL issuer:   [Let's Encrypt / Cloudflare / ACM]
Hosting:      [Railway / Netlify / Vercel]
Canonical:    [https://example.com]
```

### Step 8: Multi-Domain and Wildcard Setup

For projects with multiple domains or subdomains:

**Wildcard SSL:**
```bash
# Check if wildcard cert is installed
echo | openssl s_client -connect example.com:443 -servername example.com 2>/dev/null | openssl x509 -noout -text | grep "DNS:"
```

Wildcard certs (`*.example.com`) cover all subdomains at one level:
- ✅ Covers: `app.example.com`, `api.example.com`, `www.example.com`
- ❌ Does NOT cover: `example.com` (apex) — need separate SAN entry
- ❌ Does NOT cover: `staging.api.example.com` (two levels deep)

**Subdomain routing patterns:**

| Pattern | DNS Record | Points To |
|---------|-----------|-----------|
| `app.example.com` | CNAME | Frontend hosting (Netlify/Vercel) |
| `api.example.com` | CNAME | Backend hosting (Railway) |
| `docs.example.com` | CNAME | Docs hosting (GitBook/Notion) |
| `mail.example.com` | MX + CNAME | Email provider |
| `*.example.com` | CNAME | Catch-all (if needed) |

**Multi-domain for same project:**
When multiple domains point to the same app (e.g., `deedstack.com` and `www.deedstack.com`):
1. Set one as canonical (return 200)
2. All others 301 redirect to canonical
3. Each domain needs its own SSL certificate (or use a multi-SAN cert)
4. Update `Content-Security-Policy` and CORS origins to include all domains

**Output domain health report:**

```
🔒 Domain & SSL — Health Report

Domain: example.com
DNS:         ✅ A record → 76.76.21.21 (Vercel)
SSL:         ✅ Let's Encrypt, expires 2026-05-15 (75 days)
HSTS:        ✅ max-age=31536000; includeSubDomains
Redirect:    ✅ www → apex (301)
HTTPS force: ✅ http → https (301)
Mixed content: ✅ none detected
Registrar:   Cloudflare (auto-renew ON, expires 2027-01-20)

Subdomains:
  app.example.com  → ✅ Netlify (SSL valid)
  api.example.com  → ✅ Railway (SSL valid)

No issues found. Next check recommended: 2026-04-01
```

## Level History

- **Lv.1** — Base: DNS verification, SSL certificate checks, www/non-www redirects, HSTS validation, DNS propagation testing, mixed content scanning, domain monitoring checklist, multi-domain/wildcard setup. Based on managing adminstack.pro, epsteinscan.org, deedstack.com, and related properties. (Origin: MemStack Pro v3.2, Mar 2026)
