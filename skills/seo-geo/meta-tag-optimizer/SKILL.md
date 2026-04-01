---
name: memstack-seo-meta-tag-optimizer
description: "Use this skill when the user says 'meta tags', 'title tag', 'meta description', 'optimize meta', 'SERP preview', or needs to write or optimize HTML meta tags for better search visibility and click-through rates. Do NOT use for schema markup or full site audits."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# 🏷️ Meta Tag Optimizer — Scanning and optimizing page meta tags...
*Scans all pages for existing meta tags, identifies issues, and generates optimized replacements — titles, descriptions, Open Graph, canonical URLs, and robots directives.*

## Activation

When this skill activates, output:

`🏷️ Meta Tag Optimizer — Scanning pages for meta tag issues...`

Then execute the protocol below.

| Context | Status |
|---------|--------|
| User says "optimize meta tags" or "fix meta tags" | ACTIVE |
| User says "title tags" or "meta description" or "og tags" | ACTIVE |
| Improving SEO for specific pages | ACTIVE |
| Running a full site audit (broader scope) | DORMANT — use site-audit |
| Adding structured data / JSON-LD | DORMANT — use schema-markup |

### Anti-patterns

| Trap | Reality Check |
|------|---------------|
| "Same meta description on every page" | Duplicate descriptions get ignored by Google. Each page needs unique, relevant meta. |
| "Title = just the page name" | "About" tells Google nothing. "About [Company] - [Key Differentiator]" ranks. |
| "OG tags are optional" | Without og:image, your shared links look broken on social. No image = no clicks. |
| "Canonical URLs don't matter" | Duplicate content splits ranking signals. Canonical tags consolidate authority to one URL. |
| "Longer titles rank better" | Google truncates after ~60 chars. Truncated titles look unprofessional and lose clicks. |

## Protocol

### Step 1: Scan All Pages

Identify every page and its current meta tags:

```bash
# Find all page/route files
find app/ pages/ src/ -name "*.tsx" -o -name "*.jsx" -o -name "*.html" 2>/dev/null | grep -v node_modules | grep -v "_\|layout\|loading\|error\|not-found"

# Next.js metadata exports
grep -rn "export const metadata\|export function generateMetadata" --include="*.tsx" --include="*.ts" . | grep -v node_modules

# Check for global/shared metadata
cat app/layout.tsx 2>/dev/null | head -30
```

**Build the page inventory:**

| Page | Route | Has Title | Has Description | Has OG | Has Canonical |
|------|-------|-----------|----------------|--------|--------------|
| Homepage | `/` | ? | ? | ? | ? |
| About | `/about` | ? | ? | ? | ? |
| Pricing | `/pricing` | ? | ? | ? | ? |
| Blog index | `/blog` | ? | ? | ? | ? |
| Blog post | `/blog/[slug]` | ? | ? | ? | ? |
| ... | ... | ... | ... | ... | ... |

### Step 2: Audit Title Tags

```bash
# Find all title definitions
grep -rn "title:" --include="*.tsx" --include="*.ts" . | grep -v node_modules | grep -v "\.test\.\|\.spec\."
```

**Title tag rules:**

| Rule | Requirement | Check |
|------|------------|-------|
| Unique per page | No two pages share the same title | Compare all titles |
| Length | 50-60 characters | Count characters |
| Keyword placement | Primary keyword in first 40 chars | Review keyword position |
| Brand suffix | " - [Brand]" or " \| [Brand]" at end | Consistent format |
| No keyword stuffing | Keyword appears once, naturally | Read aloud test |
| Compelling | Would you click this in search results? | Subjective but critical |

**Title optimization formula:**

```
[Primary Keyword]: [Value Proposition] | [Brand]
```

Examples:
- ❌ "Home" → ✅ "Project Management for Small Teams | Acme"
- ❌ "About Us" → ✅ "About Acme - Built by Developers, for Developers"
- ❌ "Blog" → ✅ "Acme Blog: Tips for Remote Team Management"
- ❌ "Contact" → ✅ "Contact Acme - Get a Free Consultation"

### Step 3: Audit Meta Descriptions

```bash
# Find all description definitions
grep -rn "description:" --include="*.tsx" --include="*.ts" . | grep -v node_modules | grep -v "\.test\.\|\.spec\."
```

**Description rules:**

| Rule | Requirement | Check |
|------|------------|-------|
| Unique per page | No duplicates | Compare all descriptions |
| Length | 150-155 characters | Count characters |
| Includes keyword | Primary keyword present | Keyword search |
| Includes CTA | Action-oriented language | Look for verbs |
| Matches page content | Description reflects actual content | Manual review |
| No truncation | Complete thought within limit | Check ending |

**Description formula:**

```
[What the page offers]. [Specific benefit or differentiator]. [CTA - action verb].
```

Examples:
- ❌ "Welcome to our website" → ✅ "Manage projects 3x faster with Acme's all-in-one platform. Built for remote teams with real-time collaboration. Start free today."
- ❌ "" (empty) → ✅ "Learn proven strategies for managing distributed teams. Practical tips from 10 years of remote-first experience. Read the latest posts."

### Step 4: Audit Open Graph Tags

```bash
# Find OG tag definitions
grep -rn "openGraph\|og:" --include="*.tsx" --include="*.ts" --include="*.html" . | grep -v node_modules
```

**Required OG tags per page:**

| Tag | Required | Specification |
|-----|----------|--------------|
| `og:title` | Yes | Can differ from `<title>` — optimize for social, not search |
| `og:description` | Yes | Can differ from meta description — more casual tone ok |
| `og:image` | Yes | 1200x630px, < 5MB, shows product/brand/visual |
| `og:url` | Yes | Canonical URL of the page |
| `og:type` | Yes | `website` for homepage, `article` for blog posts |
| `og:site_name` | Recommended | Brand name |
| `twitter:card` | Recommended | `summary_large_image` for image-heavy shares |
| `twitter:title` | Recommended | Can match og:title |
| `twitter:description` | Recommended | Can match og:description |
| `twitter:image` | Recommended | Can match og:image |

**Common og:image issues:**
- ❌ No og:image → shared links show no preview (kills click-through)
- ❌ Image too small (< 600px wide) → blurry preview
- ❌ Image URL is relative (`/images/og.png`) → must be absolute URL
- ❌ Image doesn't exist at URL → broken preview
- ❌ Same og:image on every page → all shares look identical

### Step 5: Audit Canonical URLs

```bash
# Find canonical definitions
grep -rn "canonical\|alternates" --include="*.tsx" --include="*.ts" --include="*.html" . | grep -v node_modules
```

**Canonical URL rules:**

| Check | Rule | Common Mistake |
|-------|------|---------------|
| Self-referencing | Every page canonicals to itself | Missing canonical = Google guesses |
| Consistency | Always use one format (www vs non-www, trailing slash vs not) | Mixed formats split authority |
| HTTPS | Canonical always uses `https://` | `http://` canonical on `https://` page |
| Absolute URL | Full URL, not relative path | `/about` instead of `https://domain.com/about` |
| No noindex + canonical conflict | Don't canonical to a noindexed page | Contradictory signals |
| Pagination | Paginated pages canonical to themselves or page 1 | All pages canonical to page 1 (outdated pattern) |

**Duplicate content scenarios requiring canonicals:**
- URL parameters: `/products?sort=price` → canonical to `/products`
- www vs non-www: `www.example.com/about` → canonical to `example.com/about`
- HTTP vs HTTPS: `http://` → canonical to `https://`
- Trailing slashes: `/about/` → canonical to `/about` (pick one)
- Print pages: `/about/print` → canonical to `/about`

### Step 6: Audit Robots Meta

```bash
# Find robots meta directives
grep -rn "robots\|noindex\|nofollow" --include="*.tsx" --include="*.ts" --include="*.html" . | grep -v node_modules
```

**Pages that SHOULD have `noindex`:**

| Page Type | Directive | Why |
|-----------|----------|-----|
| Admin dashboard | `noindex, nofollow` | Internal tool, not for search |
| Login / register | `noindex, follow` | Auth pages waste crawl budget |
| Search results | `noindex, follow` | Dynamic pages with thin content |
| Thank you / confirmation | `noindex, nofollow` | Post-conversion, no search value |
| Staging / preview | `noindex, nofollow` | Duplicate content with production |
| User profiles (if private) | `noindex, nofollow` | Privacy concern |

**Pages that should NOT have `noindex`:**
- ❌ Homepage, product pages, blog posts, pricing — these should all be indexed
- Check: no accidental `noindex` on important pages (common after staging → production migration)

### Step 7: Generate Optimized Replacements

For every failing tag, generate the corrected version:

```markdown
## Optimized Meta Tags

### / (Homepage)

**Current:**
- Title: "Home"
- Description: (missing)
- OG Image: (missing)

**Recommended:**
```tsx
export const metadata: Metadata = {
  title: 'Acme - Project Management for Remote Teams',
  description: 'Manage projects 3x faster with real-time collaboration, task tracking, and team dashboards. Built for remote teams. Start free today.',
  openGraph: {
    title: 'Acme - Project Management for Remote Teams',
    description: 'All-in-one project management for distributed teams. Real-time collaboration, built-in reporting.',
    images: [{ url: 'https://acme.com/og/homepage.png', width: 1200, height: 630 }],
    url: 'https://acme.com',
    type: 'website',
    siteName: 'Acme',
  },
  twitter: {
    card: 'summary_large_image',
  },
  alternates: {
    canonical: 'https://acme.com',
  },
};
```

### /pricing

**Current:**
- Title: "Pricing"
- Description: "View our pricing plans"

**Recommended:**
```tsx
export const metadata: Metadata = {
  title: 'Pricing - Acme Plans Starting at $0/mo',
  description: 'Compare Acme plans: Free, Pro ($19/mo), and Enterprise. All plans include unlimited projects and real-time collaboration. Start free today.',
  // ... (full OG tags)
};
```
```

### Step 8: Output Tag Report

```
🏷️ Meta Tag Optimizer — Complete

Pages scanned: [count]
Issues found: [count]

Summary:
  Title tags:     [X/count] optimized — [count] need fixing
  Descriptions:   [X/count] optimized — [count] need fixing
  OG tags:        [X/count] complete — [count] missing
  Canonical URLs: [X/count] correct — [count] missing or wrong
  Robots meta:    [X/count] correct — [count] need review

Page-by-page comparison:
| Page | Title (current → recommended) | Description | OG | Canonical |
|------|------------------------------|-------------|----|-----------|
| / | "Home" → "Acme - PM for Remote Teams" | ❌ missing | ❌ missing | ❌ missing |
| /about | "About" → "About Acme - Built by Devs" | ⚠️ too short | ✅ ok | ✅ ok |
| /blog | ✅ ok | ✅ ok | ❌ no image | ✅ ok |
| /pricing | ⚠️ too short | ⚠️ generic | ✅ ok | ❌ missing |

Next steps:
1. Apply recommended tags to each page
2. Test social sharing previews (Facebook Debugger, Twitter Card Validator)
3. Verify canonical URLs resolve correctly
4. Check robots.txt doesn't conflict with robots meta
5. Submit updated pages to Google Search Console for re-indexing
```

## Level History

- **Lv.1** — Base: Page scanning, title tag audit (50-60 chars, keyword placement), meta description audit (150-155 chars, CTA), Open Graph tags (og:title/description/image), canonical URL verification, robots meta directives, optimized replacement generation, page-by-page comparison output. (Origin: MemStack Pro v3.2, Mar 2026)
