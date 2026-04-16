# JSON-LD Schema Template Bank

Ready-to-paste JSON-LD blocks for the ten most common schema.org types plus a combined `@graph` bundle. Each template lists the required fields Google checks for rich-result eligibility and leaves optional-but-useful fields in place with `YOUR_*` placeholders. Validate with the [Google Rich Results Test](https://search.google.com/test/rich-results) and the [Schema.org Validator](https://validator.schema.org/) after filling in.

All JSON blocks below go inside:

```html
<script type="application/ld+json">
  { ... paste template here ... }
</script>
```

Remove any optional field you can't populate with real data — empty or fake values can trigger Google manual actions. Never copy a template that references reviews, ratings, or prices you don't actually have.

---

## 1. FAQPage

**When to use:** Pages that primarily answer user questions (dedicated FAQ pages, product FAQ sections). Only use when the Q&A content is visible on the page and isn't user-generated support content.

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "YOUR_QUESTION_TEXT_HERE",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "YOUR_ANSWER_TEXT_HERE. Can include basic HTML: <a>, <strong>, <ul>, <ol>, <li>."
      }
    },
    {
      "@type": "Question",
      "name": "YOUR_SECOND_QUESTION_HERE",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "YOUR_SECOND_ANSWER_HERE."
      }
    }
  ]
}
```

**Required:** `mainEntity` array with at least one `Question` → `acceptedAnswer` → `Answer.text`.
**Rich result:** FAQ dropdowns in SERP (Google may show 2–4 questions).

---

## 2. WebPage

**When to use:** Generic content pages when no more specific type (Article, Product, HowTo) fits. Establishes basic page identity for crawlers.

```json
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "YOUR_PAGE_TITLE_HERE",
  "description": "YOUR_PAGE_DESCRIPTION_HERE",
  "url": "https://YOUR_DOMAIN.com/YOUR_PAGE_PATH",
  "datePublished": "2026-01-15",
  "dateModified": "2026-04-16",
  "inLanguage": "en-US",
  "isPartOf": {
    "@type": "WebSite",
    "name": "YOUR_SITE_NAME",
    "url": "https://YOUR_DOMAIN.com"
  }
}
```

**Required:** `name`, `url`.
**Recommended:** `description`, `datePublished`, `dateModified`, `inLanguage`, `isPartOf` pointing to your `WebSite`.

---

## 3. Article

**When to use:** Blog posts, news articles, tutorials, editorial content with a clear author and publish date.

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "YOUR_ARTICLE_HEADLINE_HERE",
  "description": "YOUR_ARTICLE_DESCRIPTION_HERE",
  "image": [
    "https://YOUR_DOMAIN.com/YOUR_IMAGE_16x9.jpg",
    "https://YOUR_DOMAIN.com/YOUR_IMAGE_4x3.jpg",
    "https://YOUR_DOMAIN.com/YOUR_IMAGE_1x1.jpg"
  ],
  "datePublished": "2026-01-15T08:00:00+00:00",
  "dateModified": "2026-04-16T10:30:00+00:00",
  "author": {
    "@type": "Person",
    "name": "YOUR_AUTHOR_NAME",
    "url": "https://YOUR_DOMAIN.com/about/YOUR_AUTHOR_SLUG"
  },
  "publisher": {
    "@type": "Organization",
    "name": "YOUR_ORG_NAME",
    "logo": {
      "@type": "ImageObject",
      "url": "https://YOUR_DOMAIN.com/logo.png"
    }
  },
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://YOUR_DOMAIN.com/YOUR_ARTICLE_PATH"
  }
}
```

**Required for rich results:** `headline` (≤110 chars), `image` (at least one crawlable URL), `datePublished`, `author.name`.
**Recommended:** `description`, `dateModified`, `publisher.logo`, `mainEntityOfPage`.
**Rich result:** Article card with thumbnail and byline.

---

## 4. SoftwareApplication

**When to use:** SaaS products, web apps, desktop/mobile apps, developer tools. Use a more specific subtype when applicable (`WebApplication`, `MobileApplication`, `VideoGame`).

```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "YOUR_PRODUCT_NAME",
  "description": "YOUR_PRODUCT_DESCRIPTION_HERE",
  "applicationCategory": "DeveloperApplication",
  "operatingSystem": "Web",
  "url": "https://YOUR_DOMAIN.com",
  "softwareVersion": "1.0.0",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock"
  },
  "author": {
    "@type": "Organization",
    "name": "YOUR_ORG_NAME",
    "url": "https://YOUR_DOMAIN.com"
  }
}
```

**Required for rich results:** `name`, `applicationCategory`, `operatingSystem`, `offers` (with `price` + `priceCurrency`).
**Optional:** `aggregateRating` — **only add if you have real, verifiable reviews**. Fake ratings trigger Google manual actions.
**Rich result:** Software info panel with price and category.

---

## 5. Organization

**When to use:** Homepage, about page, or anywhere you want to identify the company/entity behind the site. Add once per site (usually in the root layout).

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "YOUR_ORG_NAME",
  "url": "https://YOUR_DOMAIN.com",
  "logo": "https://YOUR_DOMAIN.com/logo.png",
  "description": "YOUR_ORG_DESCRIPTION_HERE",
  "foundingDate": "YYYY",
  "sameAs": [
    "https://twitter.com/YOUR_HANDLE",
    "https://github.com/YOUR_ORG",
    "https://linkedin.com/company/YOUR_COMPANY"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "contactType": "customer support",
    "email": "support@YOUR_DOMAIN.com"
  }
}
```

**Required:** `name`, `url`.
**Recommended:** `logo` (PNG, min 112×112), `sameAs` (social profile URLs — feeds Google's knowledge graph), `contactPoint`.
**Rich result:** Knowledge panel eligibility (not guaranteed).

---

## 6. Product

**When to use:** E-commerce product pages with price and availability. Do not use for software (use `SoftwareApplication`) or for category/collection pages.

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "YOUR_PRODUCT_NAME",
  "description": "YOUR_PRODUCT_DESCRIPTION_HERE",
  "image": [
    "https://YOUR_DOMAIN.com/YOUR_PRODUCT_IMG_1.jpg",
    "https://YOUR_DOMAIN.com/YOUR_PRODUCT_IMG_2.jpg"
  ],
  "sku": "YOUR_SKU_HERE",
  "brand": {
    "@type": "Brand",
    "name": "YOUR_BRAND_NAME"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://YOUR_DOMAIN.com/YOUR_PRODUCT_PATH",
    "price": "99.99",
    "priceCurrency": "USD",
    "priceValidUntil": "2026-12-31",
    "availability": "https://schema.org/InStock",
    "itemCondition": "https://schema.org/NewCondition",
    "seller": {
      "@type": "Organization",
      "name": "YOUR_SELLER_NAME"
    }
  }
}
```

**Required for rich results:** `name`, `image`, `offers` (with `price`, `priceCurrency`, `availability`), and **one of** `review` or `aggregateRating`.
**Note:** Only add `aggregateRating` with real review data. `priceValidUntil` must be a real future date.
**Rich result:** Product snippet with price, availability, ratings.

---

## 7. HowTo

**When to use:** Step-by-step tutorials, recipes (use `Recipe` for food specifically), DIY guides, configuration walkthroughs. Each step must be visible on the page.

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to YOUR_TASK_HERE",
  "description": "YOUR_GUIDE_DESCRIPTION_HERE",
  "image": "https://YOUR_DOMAIN.com/YOUR_HOWTO_IMG.jpg",
  "totalTime": "PT15M",
  "estimatedCost": {
    "@type": "MonetaryAmount",
    "currency": "USD",
    "value": "0"
  },
  "supply": [
    {
      "@type": "HowToSupply",
      "name": "YOUR_REQUIRED_ITEM_HERE"
    }
  ],
  "tool": [
    {
      "@type": "HowToTool",
      "name": "YOUR_REQUIRED_TOOL_HERE"
    }
  ],
  "step": [
    {
      "@type": "HowToStep",
      "position": 1,
      "name": "YOUR_STEP_1_NAME",
      "text": "YOUR_STEP_1_DETAILED_INSTRUCTIONS",
      "image": "https://YOUR_DOMAIN.com/YOUR_STEP_1_IMG.jpg",
      "url": "https://YOUR_DOMAIN.com/YOUR_GUIDE_PATH#step-1"
    },
    {
      "@type": "HowToStep",
      "position": 2,
      "name": "YOUR_STEP_2_NAME",
      "text": "YOUR_STEP_2_DETAILED_INSTRUCTIONS"
    }
  ]
}
```

**Required:** `name`, `step` array with at least two `HowToStep` entries (each with `text`).
**Recommended:** `totalTime` (ISO 8601 duration like `PT15M`), `supply`, `tool`, per-step `image`.
**Rich result:** Step-by-step carousel in SERP.

---

## 8. BreadcrumbList

**When to use:** Any page with hierarchical navigation. Include on every indexable page except the homepage. The breadcrumb must match a visible breadcrumb trail on the page.

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://YOUR_DOMAIN.com"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "YOUR_CATEGORY_NAME",
      "item": "https://YOUR_DOMAIN.com/YOUR_CATEGORY_PATH"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "YOUR_CURRENT_PAGE_NAME"
    }
  ]
}
```

**Required:** `itemListElement` array with `ListItem` entries (each with `position`, `name`; `item` required for all except the last).
**Rule:** `position` starts at 1 and increments by 1. Last item may omit `item` (it's the current page).
**Rich result:** Breadcrumb trail replaces the URL in SERP.

---

## 9. LocalBusiness

**When to use:** Businesses with a physical location or a defined service area. Use the most specific subtype available (`Restaurant`, `Dentist`, `Attorney`, `AutoRepair`, etc.) rather than generic `LocalBusiness` when possible.

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "YOUR_BUSINESS_NAME",
  "description": "YOUR_BUSINESS_DESCRIPTION_HERE",
  "image": "https://YOUR_DOMAIN.com/storefront.jpg",
  "url": "https://YOUR_DOMAIN.com",
  "telephone": "+1-555-555-5555",
  "email": "contact@YOUR_DOMAIN.com",
  "priceRange": "$$",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "YOUR_STREET_ADDRESS",
    "addressLocality": "YOUR_CITY",
    "addressRegion": "YOUR_STATE_OR_REGION",
    "postalCode": "YOUR_ZIP_OR_POSTAL",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 37.7749,
    "longitude": -122.4194
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "09:00",
      "closes": "17:00"
    },
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": "Saturday",
      "opens": "10:00",
      "closes": "14:00"
    }
  ],
  "sameAs": [
    "https://www.facebook.com/YOUR_PAGE",
    "https://www.yelp.com/biz/YOUR_LISTING"
  ]
}
```

**Required:** `name`, `address` (complete `PostalAddress`), `image` (at least one), `telephone`.
**Recommended:** `openingHoursSpecification`, `priceRange`, `geo`, `sameAs`, `url`.
**Rich result:** Local pack, knowledge panel, Google Maps integration.

---

## 10. SpeakableSpecification

**When to use:** Voice search and smart-speaker optimization. Marks the sections of a page most suitable for text-to-speech extraction (summaries, key points, H1, hero).

```json
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "YOUR_PAGE_TITLE_HERE",
  "url": "https://YOUR_DOMAIN.com/YOUR_PAGE_PATH",
  "speakable": {
    "@type": "SpeakableSpecification",
    "cssSelector": [
      "h1",
      ".page-summary",
      ".key-takeaways",
      ".faq-answer"
    ]
  }
}
```

**Required:** One of `cssSelector` (array) or `xpath` (array).
**Note:** `SpeakableSpecification` is always nested inside another schema (usually `WebPage` or `Article`). Point CSS selectors at sections that read well out of context — avoid selectors that grab navigation, forms, or raw lists.

---

## Combined `@graph` Example

**When to use:** Bundling multiple schemas on a single page (common for homepages — Organization + WebSite + FAQPage all in one block). A single `@graph` array keeps related schemas explicitly linked via `@id` references and avoids duplicate `@context` declarations.

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://YOUR_DOMAIN.com/#org",
      "name": "YOUR_ORG_NAME",
      "url": "https://YOUR_DOMAIN.com",
      "logo": "https://YOUR_DOMAIN.com/logo.png",
      "sameAs": [
        "https://twitter.com/YOUR_HANDLE",
        "https://github.com/YOUR_ORG"
      ]
    },
    {
      "@type": "WebSite",
      "@id": "https://YOUR_DOMAIN.com/#website",
      "name": "YOUR_SITE_NAME",
      "url": "https://YOUR_DOMAIN.com",
      "publisher": { "@id": "https://YOUR_DOMAIN.com/#org" },
      "potentialAction": {
        "@type": "SearchAction",
        "target": {
          "@type": "EntryPoint",
          "urlTemplate": "https://YOUR_DOMAIN.com/search?q={search_term_string}"
        },
        "query-input": "required name=search_term_string"
      }
    },
    {
      "@type": "WebPage",
      "@id": "https://YOUR_DOMAIN.com/#webpage",
      "url": "https://YOUR_DOMAIN.com",
      "name": "YOUR_HOMEPAGE_TITLE",
      "isPartOf": { "@id": "https://YOUR_DOMAIN.com/#website" },
      "about": { "@id": "https://YOUR_DOMAIN.com/#org" },
      "speakable": {
        "@type": "SpeakableSpecification",
        "cssSelector": ["h1", ".hero-description"]
      }
    },
    {
      "@type": "FAQPage",
      "@id": "https://YOUR_DOMAIN.com/#faq",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "YOUR_QUESTION_TEXT_HERE",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "YOUR_ANSWER_TEXT_HERE."
          }
        }
      ]
    }
  ]
}
```

**Pattern:** Declare `@context` once at the top, then put each schema as an array element in `@graph`. Use `@id` values as stable identifiers so schemas can reference each other (the `WebSite.publisher` here points to the `Organization` by `@id`, which helps Google connect them).

**Rule:** Only include a schema if it's genuinely applicable to the page. An irrelevant `@graph` entry (e.g. `FAQPage` on a page with no real FAQs) is worse than no schema at all.

---

## Validation checklist

Before deploying any schema block:

- [ ] Parses as valid JSON (`JSON.parse` without errors — no trailing commas, no single quotes)
- [ ] All `url` / `@id` / image fields are absolute URLs with `https://`
- [ ] Dates are ISO 8601 (`YYYY-MM-DD` or `YYYY-MM-DDTHH:MM:SS+00:00`)
- [ ] Required fields for the `@type` are all present (see per-type requirements above)
- [ ] Image URLs return 200 and are publicly crawlable (not behind auth)
- [ ] Schema content matches what's visible on the page
- [ ] Passes [Google Rich Results Test](https://search.google.com/test/rich-results)
- [ ] Passes [Schema.org Validator](https://validator.schema.org/)
- [ ] No `aggregateRating` / `review` unless the reviews are real and attributable
