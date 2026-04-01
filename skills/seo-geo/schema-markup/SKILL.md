---
name: memstack-seo-schema-markup
description: "Use this skill when the user says 'add schema', 'schema markup', 'JSON-LD', 'structured data', 'rich results', 'rich snippets', or is adding or fixing schema.org structured data for better search result appearance. Do NOT use for meta tag optimization or full SEO audits."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# 📊 Schema Markup — Generating structured data for rich results...
*Identifies applicable schema types, generates valid JSON-LD blocks, and verifies against Google's Rich Results requirements — ready to paste into page head.*

## Activation

When this skill activates, output:

`📊 Schema Markup — Analyzing pages for schema opportunities...`

Then execute the protocol below.

| Context | Status |
|---------|--------|
| User says "add schema" or "schema markup" or "JSON-LD" | ACTIVE |
| User says "structured data" or "rich results" or "rich snippets" | ACTIVE |
| Adding or fixing schema.org data on any page | ACTIVE |
| Doing a full SEO audit (broader scope) | DORMANT — use site-audit |
| Optimizing meta tags (not schema) | DORMANT — use meta-tag-optimizer |

### Anti-patterns

| Trap | Reality Check |
|------|---------------|
| "Schema is optional" | Pages with schema get rich results. Pages without get plain blue links. Rich results get 2-3x more clicks. |
| "Add every schema type" | Only add schema that matches actual page content. Irrelevant schema triggers manual actions from Google. |
| "Microdata is fine" | Google recommends JSON-LD. It's cleaner, easier to maintain, and separated from HTML. Use JSON-LD only. |
| "Copy schema from another site" | Schema must reflect YOUR content. Copying schema with different data violates Google's guidelines. |
| "Schema guarantees rich results" | Schema makes you eligible. Google decides whether to show rich results based on quality and relevance. |

## Protocol

### Step 1: Identify Applicable Schema Types

Map each page type to the correct schema:

```bash
# Scan for page types
find app/ pages/ -name "page.tsx" -o -name "*.tsx" 2>/dev/null | grep -v node_modules | grep -v "_\|layout\|loading\|error"

# Check for existing schema
grep -rn "application/ld+json\|schema.org" --include="*.tsx" --include="*.jsx" --include="*.html" . | grep -v node_modules
```

**Schema type mapping:**

| Page Type | Primary Schema | Additional Schema | Rich Result |
|-----------|---------------|-------------------|-------------|
| Homepage | `Organization` + `WebSite` | `SearchAction` | Sitelinks search box |
| About | `Organization` | `Person` (for founders) | Knowledge panel |
| Product/Pricing | `Product` | `Offer`, `AggregateRating` | Product rich results (price, rating) |
| Blog post | `Article` | `Person` (author), `ImageObject` | Article rich results |
| FAQ page | `FAQPage` | — | FAQ dropdowns in SERP |
| How-to guide | `HowTo` | `HowToStep` | How-to rich results |
| Contact/Local | `LocalBusiness` | `PostalAddress`, `GeoCoordinates` | Local pack |
| SaaS/Software | `SoftwareApplication` | `Offer` | Software rich results |
| Event page | `Event` | `Place`, `Offer` | Event rich results |
| Recipe | `Recipe` | `NutritionInformation` | Recipe card |
| All pages | `BreadcrumbList` | — | Breadcrumb trail |

### Step 2: Generate Organization Schema

For the homepage or site-wide layout:

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "[Company Name]",
  "url": "https://[domain]",
  "logo": "https://[domain]/logo.png",
  "description": "[One-sentence company description]",
  "foundingDate": "[YYYY]",
  "sameAs": [
    "https://twitter.com/[handle]",
    "https://github.com/[org]",
    "https://linkedin.com/company/[name]"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "contactType": "customer support",
    "email": "[support@domain.com]"
  }
}
```

### Step 3: Generate WebSite + SearchAction Schema

Enables the sitelinks search box in Google:

```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "[Site Name]",
  "url": "https://[domain]",
  "potentialAction": {
    "@type": "SearchAction",
    "target": {
      "@type": "EntryPoint",
      "urlTemplate": "https://[domain]/search?q={search_term_string}"
    },
    "query-input": "required name=search_term_string"
  }
}
```

**Note:** Only add `SearchAction` if your site has a working search page at the specified URL.

### Step 4: Generate Article Schema

For blog posts and articles:

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "[Post Title — max 110 chars]",
  "description": "[Post description — max 155 chars]",
  "image": "https://[domain]/blog/[slug]/hero.jpg",
  "datePublished": "[YYYY-MM-DDT00:00:00Z]",
  "dateModified": "[YYYY-MM-DDT00:00:00Z]",
  "author": {
    "@type": "Person",
    "name": "[Author Name]",
    "url": "https://[domain]/about"
  },
  "publisher": {
    "@type": "Organization",
    "name": "[Company Name]",
    "logo": {
      "@type": "ImageObject",
      "url": "https://[domain]/logo.png"
    }
  },
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://[domain]/blog/[slug]"
  }
}
```

**Required fields for Article rich results:**
- `headline` (max 110 chars)
- `image` (at least one, must be crawlable)
- `datePublished`
- `author.name`

### Step 5: Generate Product / SoftwareApplication Schema

For product or pricing pages:

```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "[Product Name]",
  "applicationCategory": "[BusinessApplication / DeveloperApplication / etc.]",
  "operatingSystem": "Web",
  "description": "[Product description]",
  "url": "https://[domain]",
  "offers": {
    "@type": "AggregateOffer",
    "lowPrice": "[lowest tier price]",
    "highPrice": "[highest tier price]",
    "priceCurrency": "USD",
    "offerCount": "[number of tiers]"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "[X.X]",
    "ratingCount": "[count]",
    "bestRating": "5"
  }
}
```

**Only include `aggregateRating` if you have real reviews.** Fake ratings violate Google's guidelines and risk manual action.

### Step 6: Generate FAQ Schema

For FAQ pages or sections:

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "[Question text]",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[Answer text — can include basic HTML: links, bold, lists]"
      }
    },
    {
      "@type": "Question",
      "name": "[Question text]",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[Answer text]"
      }
    }
  ]
}
```

**FAQ schema rules:**
- Only use on pages that are primarily FAQ content
- Questions and answers must be visible on the page (not hidden behind JS)
- Don't use FAQ schema for support tickets or user-generated Q&A
- Google may show 2-4 FAQ results directly in the SERP

### Step 7: Generate Breadcrumb Schema

For all pages with navigation hierarchy:

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://[domain]"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Blog",
      "item": "https://[domain]/blog"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "[Post Title]",
      "item": "https://[domain]/blog/[slug]"
    }
  ]
}
```

**Breadcrumb rules:**
- Position starts at 1 (home) and increments
- Last item can omit `item` (current page)
- Must match visible breadcrumb navigation on the page

### Step 8: Verify and Validate

Check all generated schema for correctness:

**Validation checklist:**

| Check | How | Pass Criteria |
|-------|-----|--------------|
| Valid JSON | JSON.parse() | No syntax errors |
| Required fields | Compare to Google's requirements | All required fields present |
| URLs are absolute | Check all `url` and `@id` fields | Start with `https://` |
| Dates are ISO 8601 | Check `datePublished`, `dateModified` | Format: `YYYY-MM-DDT00:00:00Z` |
| Images are crawlable | URLs are accessible, not behind auth | Returns 200 |
| Content matches page | Schema data matches visible content | No mismatches |
| No duplicate types | One schema per type per page | No conflicts |

**Testing tools:**
- Google Rich Results Test: `https://search.google.com/test/rich-results`
- Schema.org Validator: `https://validator.schema.org/`
- Google Search Console: Enhancements section for schema coverage

**Implementation in Next.js:**

Add JSON-LD as a script tag in your page component or layout. Use `JSON.stringify()` on a developer-defined schema object and inject it via a `<script type="application/ld+json">` element. This is safe because the data is controlled by the developer, not user input.

### Step 9: Output Schema Blocks

```
📊 Schema Markup — Complete

Pages analyzed: [count]
Schema blocks generated: [count]

Schema by page:
  / (homepage)     → Organization, WebSite + SearchAction, BreadcrumbList
  /pricing         → SoftwareApplication + Offer, BreadcrumbList
  /blog/[slug]     → Article, BreadcrumbList
  /faq             → FAQPage, BreadcrumbList
  /contact         → LocalBusiness, BreadcrumbList

Rich result eligibility:
  ✅ Sitelinks search box (WebSite + SearchAction)
  ✅ Article rich results (Article schema)
  ✅ FAQ dropdowns (FAQPage schema)
  ✅ Software/product info (SoftwareApplication)
  ✅ Breadcrumb trail (BreadcrumbList)

Next steps:
1. Add generated JSON-LD to each page
2. Test with Google Rich Results Test
3. Deploy and monitor in Search Console → Enhancements
4. Rich results may take days to weeks to appear after indexing
```

## Level History

- **Lv.1** — Base: Schema type identification by page type, JSON-LD generation (Organization, WebSite, Article, SoftwareApplication, FAQPage, BreadcrumbList), Google Rich Results verification checklist, ready-to-paste code blocks. (Origin: MemStack Pro v3.2, Mar 2026)
