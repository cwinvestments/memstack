---
name: memstack-seo-site-audit
description: "Use this skill when the user says 'SEO audit', 'site audit', 'check SEO', 'audit my site', 'SEO check', 'technical SEO', or is evaluating a website's search engine optimization health, meta tags, performance, or structured data. Do NOT use for keyword research or schema markup generation alone."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# 🔎 Site Audit — Running comprehensive SEO audit...
*Scans every page for meta tags, heading hierarchy, broken links, image optimization, Core Web Vitals, robots/sitemap, performance, and structured data — producing a prioritized fix list.*

## Activation

When this skill activates, output:

`🔎 Site Audit — Scanning site for SEO issues...`

Then execute the protocol below.

| Context | Status |
|---------|--------|
| User says "SEO audit" or "site audit" or "check SEO" | ACTIVE |
| User says "technical SEO" or "audit my site" | ACTIVE |
| Evaluating a website's overall search health | ACTIVE |
| Optimizing specific meta tags (not full audit) | DORMANT — use meta-tag-optimizer |
| Adding schema markup (not auditing) | DORMANT — use schema-markup |
| Researching keywords (not auditing) | DORMANT — use keyword-research |

### Anti-patterns

| Trap | Reality Check |
|------|---------------|
| "The site looks fine in the browser" | Crawlers and users see different things. Missing meta tags, broken links, and slow JS are invisible to humans. |
| "We'll optimize after launch" | Technical debt compounds. Fixing 5 issues now prevents 50 issues later when Google has already indexed the problems. |
| "One audit is enough" | Sites change with every deploy. Audit after major content or code changes, minimum quarterly. |
| "Performance doesn't affect SEO" | Core Web Vitals are ranking signals. Slow sites rank lower regardless of content quality. |
| "Robots.txt is set and forget" | One wrong rule can deindex your entire site. Review after every major structural change. |

## Protocol

For how each AI search engine ranks and cites content (ChatGPT, Perplexity, Google AI Overview, Copilot, Claude, and Google traditional as baseline), see [`references/platform-ranking-factors.md`](./references/platform-ranking-factors.md). Use it to prioritize fixes — a client whose audience is primarily on Perplexity benefits most from FAQ schema and PDF-friendly pages, while a ChatGPT-first audience needs backlinks and 30-day-fresh content.

### Step 0: Live site snapshot (optional, for deployed URLs)

If the site is already deployed, run the bundled stdlib-only audit script for a one-shot snapshot before walking the source-tree checks below:

```bash
python scripts/live_audit.py https://example.com
```

No API keys, no pip installs, no external dependencies — pure Python 3 stdlib (`urllib`, `html.parser`, `json`). It fetches the page once and checks title, meta description, heading hierarchy, image alt attributes, JSON-LD structured data, canonical URL, Open Graph tags, robots meta, viewport, `robots.txt` (including AI bot rules), `sitemap.xml`, page load time, and internal vs. external link counts. Output uses the same severity format (🔴 Critical / 🟠 High / 🟡 Medium / 🔵 Low) as the scorecard in Step 9, and the script exit code reflects severity (`0` clean, `1` high, `2` critical) so it can also gate CI.

Use this for deployed-URL audits; use Steps 1-8 below for source-tree scans of unshipped code. The two are complementary — the live script confirms what actually reaches crawlers, the grep steps catch issues before they ship.

---

### Step 1: Check Meta Tags

Scan every page for required meta tags:

```bash
# Find all page files
find app/ pages/ src/ -name "*.tsx" -o -name "*.jsx" -o -name "*.html" | grep -v node_modules

# Search for meta tag patterns
grep -rn "title\|<meta\|og:title\|og:description\|og:image\|canonical" --include="*.tsx" --include="*.jsx" --include="*.html" . | grep -v node_modules
```

**Required meta tags per page:**

| Tag | Required | Rule |
|-----|----------|------|
| `<title>` | Yes | Unique per page, 50-60 chars, includes primary keyword |
| `<meta name="description">` | Yes | Unique per page, 150-155 chars, includes CTA |
| `<link rel="canonical">` | Yes | Points to the canonical URL (prevents duplicate content) |
| `<meta property="og:title">` | Yes | Social sharing title (can differ from page title) |
| `<meta property="og:description">` | Yes | Social sharing description |
| `<meta property="og:image">` | Yes | Social sharing image (1200x630px recommended) |
| `<meta property="og:url">` | Yes | Canonical URL |
| `<meta name="robots">` | Conditional | `noindex` on admin, auth, and internal pages |
| `<meta name="viewport">` | Yes | `width=device-width, initial-scale=1` |

**Score per page:**
- ✅ All required tags present and valid
- ⚠️ Missing optional tags
- ❌ Missing required tags or invalid values

### Step 2: Check Heading Hierarchy

```bash
# Find heading usage across all pages
grep -rn "<h[1-6]\|<H[1-6]" --include="*.tsx" --include="*.jsx" --include="*.html" . | grep -v node_modules
```

**Heading rules:**

| Rule | Check | Why |
|------|-------|-----|
| Single H1 per page | Count H1 tags | Multiple H1s confuse crawlers about the page topic |
| H1 matches page title (roughly) | Compare H1 to `<title>` | Consistency signals relevance |
| No skipped levels | H1 → H2 → H3, not H1 → H3 | Broken hierarchy hurts accessibility and SEO |
| Keywords in H1 and H2 | Check for target keyword | Headings are high-weight ranking signals |
| No empty headings | Check for `<h2></h2>` | Empty headings are wasted signals |
| Headings aren't used for styling | Check if headings are decorative | Use CSS for size, headings for structure |

### Step 3: Check for Broken Links

```bash
# Find all links in the codebase
grep -rn 'href="\|href={' --include="*.tsx" --include="*.jsx" --include="*.html" --include="*.md" . | grep -v node_modules | grep -v "mailto:\|tel:\|#"
```

**Check each link category:**

| Category | What to Check | Common Issues |
|----------|--------------|---------------|
| Internal links | Path exists in the app | Renamed pages, deleted routes |
| External links | URL returns 200 | Dead links, moved pages, domain expired |
| Anchor links | Target ID exists on page | Renamed sections, removed elements |
| Image links | Image file exists, loads | Wrong path, deleted assets |
| API endpoints | Endpoint is live | Changed API routes |

**Flag:** Any link returning 404, 500, or timeout. Prioritize fixing internal broken links (you control these).

### Step 4: Check Image Optimization

```bash
# Find all images
grep -rn '<img\|<Image\|background-image' --include="*.tsx" --include="*.jsx" --include="*.css" . | grep -v node_modules

# Check for alt text
grep -rn '<img\|<Image' --include="*.tsx" --include="*.jsx" . | grep -v 'alt=' | grep -v node_modules
```

**Image optimization checklist:**

| Check | Rule | Impact |
|-------|------|--------|
| Alt text present | Every `<img>` has `alt` attribute | Accessibility + image SEO |
| Alt text descriptive | Not empty, not "image", includes context | Screen readers and image search |
| File size | Under 200KB for standard images, under 100KB for thumbnails | Page speed |
| Modern format | WebP or AVIF preferred over PNG/JPG | 25-50% smaller file size |
| Lazy loading | `loading="lazy"` on below-fold images | Reduces initial page load |
| Dimensions | `width` and `height` attributes set | Prevents Cumulative Layout Shift |
| Next.js Image | Using `next/image` component | Automatic optimization, lazy loading, sizing |
| Responsive | `srcset` or responsive sizing | Serves appropriate size per device |

### Step 5: Check Core Web Vitals Indicators

Scan code for patterns that affect CWV scores:

```bash
# Render-blocking resources
grep -rn '<link.*stylesheet\|<script(?!.*defer\|.*async)' --include="*.html" . | grep -v node_modules

# Layout shift indicators (missing dimensions)
grep -rn '<img\|<video\|<iframe' --include="*.tsx" --include="*.jsx" . | grep -v 'width\|height\|aspect' | grep -v node_modules

# Large bundle imports
grep -rn "import .* from ['\"]lodash['\"]" --include="*.ts" --include="*.tsx" . | grep -v node_modules
```

**CWV targets:**

| Metric | Good | Needs Improvement | Poor | What Causes Failure |
|--------|------|-------------------|------|-------------------|
| LCP (Largest Contentful Paint) | < 2.5s | 2.5-4.0s | > 4.0s | Large hero images, slow server, render-blocking CSS |
| INP (Interaction to Next Paint) | < 200ms | 200-500ms | > 500ms | Heavy JS on main thread, long tasks |
| CLS (Cumulative Layout Shift) | < 0.1 | 0.1-0.25 | > 0.25 | Images without dimensions, dynamic content injection, web fonts |

**Code-level checks:**
- ❌ Large JavaScript bundles without code splitting
- ❌ Synchronous `<script>` tags (use `defer` or `async`)
- ❌ CSS loaded without `media` queries for non-critical styles
- ❌ Web fonts without `font-display: swap` (causes invisible text flash)
- ❌ Third-party scripts loaded in `<head>` (move to end of `<body>` or lazy load)

### Step 6: Check robots.txt and Sitemap

```bash
# Check for robots.txt
cat public/robots.txt 2>/dev/null

# Check for sitemap
cat public/sitemap.xml 2>/dev/null
ls public/sitemap*.xml 2>/dev/null
```

**robots.txt checklist:**

| Check | Expected | Issue if Missing |
|-------|----------|-----------------|
| File exists | `public/robots.txt` | Crawlers assume everything is allowed |
| Sitemap referenced | `Sitemap: https://domain.com/sitemap.xml` | Crawlers may not find your sitemap |
| Admin pages blocked | `Disallow: /admin` | Internal pages get indexed |
| API routes blocked | `Disallow: /api` | API endpoints appear in search |
| Auth pages blocked | `Disallow: /login`, `/register` | Auth pages waste crawl budget |
| Assets allowed | CSS/JS not blocked | Crawlers can't render the page |

**sitemap.xml checklist:**

| Check | Expected | Issue if Missing |
|-------|----------|-----------------|
| File exists | `public/sitemap.xml` | Crawlers may miss pages |
| All public pages listed | Every indexable page | Unlisted pages get lower priority |
| `<lastmod>` dates | Accurate last modified date | Stale dates reduce crawl frequency |
| No noindex pages included | Only indexable pages | Contradictory signals confuse crawlers |
| Submitted to Search Console | Verified in GSC | Google may not discover it |

### Step 7: Check Page Performance

```bash
# Check bundle size (Next.js)
ls -la .next/static/chunks/*.js 2>/dev/null | sort -k5 -n -r | head -10

# Check for render-blocking patterns
grep -rn "useEffect\|useState" --include="*.tsx" --include="*.jsx" . | grep -v node_modules | wc -l
```

**Performance checklist:**

| Check | Target | How to Fix |
|-------|--------|-----------|
| Total page weight | < 1MB (initial load) | Code split, lazy load, compress |
| JavaScript bundle | < 200KB (main bundle) | Tree shaking, dynamic imports |
| CSS | < 50KB (critical CSS) | Purge unused CSS, inline critical |
| Fonts | < 100KB total | Subset fonts, use `font-display: swap` |
| Images | < 200KB each | Compress, use WebP, lazy load |
| Time to First Byte | < 200ms | Server optimization, CDN |
| First Contentful Paint | < 1.8s | Optimize critical rendering path |

### Step 8: Check Structured Data

```bash
# Search for JSON-LD schema markup
grep -rn "application/ld+json\|schema.org" --include="*.tsx" --include="*.jsx" --include="*.html" . | grep -v node_modules

# Check for common schema types
grep -rn "Organization\|Product\|Article\|BreadcrumbList\|FAQPage\|WebSite" --include="*.tsx" --include="*.jsx" . | grep -v node_modules
```

**Required schema by page type:**

| Page Type | Required Schema | Rich Result Eligibility |
|-----------|----------------|----------------------|
| Homepage | Organization, WebSite, SearchAction | Sitelinks search box |
| Product page | Product (with price, availability) | Product rich results |
| Blog post | Article (with author, datePublished) | Article rich results |
| FAQ page | FAQPage | FAQ rich results |
| How-to page | HowTo | How-to rich results |
| Local business | LocalBusiness (with address, hours) | Local pack, knowledge panel |
| Breadcrumbs | BreadcrumbList | Breadcrumb trail in SERP |

**Flag if:** No structured data found at all — this is a significant missed opportunity for rich results in search.

### Step 9: Output Scorecard

```
🔎 Site Audit — Complete

Site: [domain]
Pages scanned: [count]
Overall score: [X/100]

Category scores:
  Meta tags:        [X/10] — [count] issues
  Heading hierarchy: [X/10] — [count] issues
  Broken links:      [X/10] — [count] issues
  Image optimization: [X/10] — [count] issues
  Core Web Vitals:   [X/10] — [count] issues
  Robots/sitemap:    [X/10] — [count] issues
  Performance:       [X/10] — [count] issues
  Structured data:   [X/10] — [count] issues

Priority fix list (by impact):
  🔴 Critical: [count]
    1. [Most impactful issue — e.g., "No sitemap.xml found"]
    2. [Second issue]
  🟠 High: [count]
    3. [Issue]
    4. [Issue]
  🟡 Medium: [count]
    5. [Issue]
  🔵 Low: [count]
    6. [Issue]

Page-by-page breakdown:
  / (homepage)           — Score: [X/10] — [issues summary]
  /about                 — Score: [X/10] — [issues summary]
  /blog/[slug]           — Score: [X/10] — [issues summary]
  /pricing               — Score: [X/10] — [issues summary]

Next steps:
1. Fix all Critical issues immediately
2. Run meta-tag-optimizer for tag-specific fixes
3. Run schema-markup to add missing structured data
4. Re-audit after fixes to verify improvement
5. Submit updated sitemap to Google Search Console
```

## Level History

- **Lv.1** — Base: Meta tag scanning, heading hierarchy, broken link detection, image optimization, Core Web Vitals code patterns, robots.txt/sitemap.xml, page performance, structured data presence, scored page-by-page output with prioritized fix list. (Origin: MemStack Pro v3.2, Mar 2026)
