---
name: memstack-seo-local-seo
description: "Use this skill when the user says 'local SEO', 'Google Business Profile', 'local search', 'NAP consistency', 'local listings', 'Google Maps', 'local pack', or is optimizing a business for local search results and map visibility. Do NOT use for general SEO audits or national keyword research."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# 📍 Local SEO — Optimizing for local search and map visibility...
*Evaluates Google Business Profile, NAP consistency, local schema markup, location pages, citations, and review management — producing an actionable local SEO scorecard.*

## Activation

When this skill activates, output:

`📍 Local SEO — Checking local search presence and consistency...`

Then execute the protocol below.

| Context | Status |
|---------|--------|
| User says "local SEO" or "Google Business Profile" or "local search" | ACTIVE |
| User says "NAP consistency" or "local listings" or "Google Maps" | ACTIVE |
| Optimizing a business with a physical location or service area | ACTIVE |
| Running a general site audit (broader scope) | DORMANT — use site-audit |
| Optimizing for global/national keywords (no local component) | DORMANT |

### Anti-patterns

| Trap | Reality Check |
|------|---------------|
| "We're online-only, local SEO doesn't apply" | If you serve specific regions or have a registered address, local SEO applies. Service-area businesses benefit enormously. |
| "Google Business Profile is set and forget" | GBP needs regular updates: posts, photos, Q&A responses, review replies. Stale profiles rank lower. |
| "Our address is on the Contact page, that's enough" | NAP must be consistent across every directory, citation, and page. One inconsistency can split your local authority. |
| "Reviews don't affect ranking" | Reviews are a top-3 local ranking factor. Quantity, quality, recency, and response rate all matter. |
| "We don't need location pages" | If you serve multiple areas, each needs a unique page with local content — not boilerplate with swapped city names. |

## Protocol

### Step 1: Check Google Business Profile

Verify the GBP listing is optimized:

**GBP optimization checklist:**

| Element | Check | Best Practice |
|---------|-------|--------------|
| Business name | Matches legal business name exactly | No keyword stuffing in the name |
| Primary category | Most specific category selected | "Italian Restaurant" not just "Restaurant" |
| Secondary categories | 2-5 relevant additional categories | Cover all services offered |
| Address | Complete, matches website exactly | Include suite/unit number if applicable |
| Phone | Local number, matches website | Avoid tracking numbers on GBP |
| Website URL | Links to homepage or location page | Not a redirect, not a social profile |
| Hours | Current, including holidays | Update for seasonal changes |
| Description | 750 chars, includes keywords naturally | Describe what makes you different |
| Photos | 10+ recent photos | Interior, exterior, team, products, menu |
| Posts | Weekly updates | Events, offers, updates, products |
| Q&A | Common questions answered proactively | Seed with your own FAQs |
| Services/Menu | Listed with prices if applicable | Complete and current |
| Attributes | All relevant attributes selected | Wi-Fi, parking, accessibility, etc. |

**GBP health indicators:**

| Signal | Healthy | Unhealthy |
|--------|---------|-----------|
| Profile completeness | 100% filled | Missing description, hours, or photos |
| Photo count | 10+ with recent uploads | 0-2 photos, outdated |
| Review count | 20+ with 4.0+ average | < 5 reviews or below 3.5 |
| Response rate | 100% of reviews replied | Unanswered reviews |
| Post frequency | Weekly | No posts in 30+ days |
| Q&A | Proactive answers | Unanswered questions |

### Step 2: Verify NAP Consistency

NAP (Name, Address, Phone) must be identical everywhere:

```bash
# Check website for NAP occurrences
grep -rn "address\|phone\|tel:\|street\|suite\|zip\|postal" --include="*.tsx" --include="*.jsx" --include="*.html" --include="*.json" . | grep -v node_modules
```

**NAP consistency audit:**

| Source | Name | Address | Phone | Consistent? |
|--------|------|---------|-------|------------|
| Website (footer) | ? | ? | ? | Baseline |
| Website (contact page) | ? | ? | ? | Match? |
| Google Business Profile | ? | ? | ? | Match? |
| Yelp | ? | ? | ? | Match? |
| Facebook | ? | ? | ? | Match? |
| Apple Maps | ? | ? | ? | Match? |
| BBB | ? | ? | ? | Match? |
| Industry directories | ? | ? | ? | Match? |

**Common NAP inconsistencies:**

| Issue | Example | Fix |
|-------|---------|-----|
| Abbreviation mismatch | "St" vs "Street" vs "St." | Pick one format, use everywhere |
| Suite format | "#100" vs "Suite 100" vs "Ste 100" | Standardize to one format |
| Phone format | "(555) 123-4567" vs "555-123-4567" | Use one format consistently |
| Business name | "Acme LLC" vs "Acme" vs "ACME Inc." | Use exact legal name |
| Old address | Moved but didn't update all listings | Update every citation |

### Step 3: Check Local Schema Markup

```bash
# Search for LocalBusiness schema
grep -rn "LocalBusiness\|PostalAddress\|GeoCoordinates\|openingHours" --include="*.tsx" --include="*.jsx" --include="*.html" . | grep -v node_modules
```

**Required LocalBusiness schema:**

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "[Business Name]",
  "description": "[Business description]",
  "url": "https://[domain]",
  "telephone": "[phone]",
  "email": "[email]",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "[street]",
    "addressLocality": "[city]",
    "addressRegion": "[state]",
    "postalCode": "[zip]",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "[lat]",
    "longitude": "[lng]"
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "09:00",
      "closes": "17:00"
    }
  ],
  "image": "https://[domain]/images/storefront.jpg",
  "priceRange": "$$",
  "sameAs": [
    "https://facebook.com/[page]",
    "https://yelp.com/biz/[listing]"
  ]
}
```

**Use the most specific `@type`:**

| Business Type | Schema Type |
|-------------|------------|
| Restaurant | `Restaurant` |
| Law firm | `LegalService` or `Attorney` |
| Dentist | `Dentist` |
| Real estate | `RealEstateAgent` |
| Auto repair | `AutoRepair` |
| Generic | `LocalBusiness` |

### Step 4: Verify Location Pages

For businesses serving multiple locations:

```bash
# Check for location pages
find app/ pages/ -path "*location*" -o -path "*city*" -o -path "*area*" 2>/dev/null | grep -v node_modules
```

**Location page requirements:**

| Element | Required | Why |
|---------|----------|-----|
| Unique title with city name | Yes | "Plumbing Services in Austin, TX" ranks locally |
| Unique meta description | Yes | Describes services specific to that area |
| Unique content (300+ words) | Yes | Boilerplate with swapped city names gets penalized |
| Embedded Google Map | Recommended | Shows exact location, helps Google confirm address |
| Local testimonials | Recommended | Reviews from customers in that area |
| NAP for that location | Yes | Specific address and phone for that location |
| LocalBusiness schema | Yes | With location-specific address |
| Service-area mention | Yes | Neighborhoods, suburbs, or zip codes served |
| Local landmarks/references | Recommended | "Located near [landmark], serving [neighborhoods]" |

**Red flags for location pages:**
- ❌ Same content on every location page with only the city name swapped
- ❌ No actual presence in the claimed location
- ❌ Keyword-stuffed city names ("Austin plumber Austin TX plumbing Austin")
- ❌ Doorway pages that all redirect to the same main page

### Step 5: Check Local Keyword Targeting

```bash
# Check for local keywords in titles and headings
grep -rn "title:\|<h1\|<H1\|<h2\|<H2" --include="*.tsx" --include="*.jsx" --include="*.md" . | grep -v node_modules | head -20
```

**Local keyword patterns:**

| Pattern | Example | Where to Use |
|---------|---------|-------------|
| [Service] in [City] | "Plumbing in Austin" | Title tag, H1, meta description |
| [City] [Service] | "Austin plumber" | Body content, H2 headings |
| [Service] near [Landmark] | "Dentist near UT Austin" | Body content |
| [Service] [Neighborhood] | "HVAC repair East Austin" | Location pages |
| Best [Service] in [City] | "Best pizza in Austin" | Blog posts |
| [Service] [City] [State] | "Attorney Austin TX" | Schema, footer |

**Local keyword placement:**

| Location | Priority | Notes |
|----------|----------|-------|
| Title tag | High | "[Service] in [City] - [Brand]" |
| H1 heading | High | Include city name once naturally |
| Meta description | High | Mention service area |
| First paragraph | Medium | Natural mention of location |
| Footer | Medium | Full NAP in every page footer |
| Image alt text | Medium | "Team at [Brand] [City] office" |
| URL slug | Medium | `/locations/austin-tx` |

### Step 6: Review Citations and Directories

Key citation sources to verify:

**Tier 1 — Essential (verify first):**

| Directory | Why It Matters |
|-----------|---------------|
| Google Business Profile | #1 local ranking factor |
| Apple Maps / Apple Business Connect | iOS users, Siri results |
| Bing Places | Bing search, Cortana |
| Yelp | High domain authority, reviews |
| Facebook Business | Social signals, reviews |
| Better Business Bureau | Trust signals |

**Tier 2 — Industry-specific:**

| Industry | Directories |
|----------|------------|
| Restaurants | TripAdvisor, OpenTable, Zomato |
| Legal | Avvo, FindLaw, Justia |
| Medical | Healthgrades, Zocdoc, WebMD |
| Real estate | Zillow, Realtor.com, Redfin |
| Home services | HomeAdvisor, Angi, Thumbtack |
| General | YellowPages, Manta, MapQuest |

**Citation audit:**
- Verify NAP is identical on every listing
- Remove duplicate listings on the same directory
- Claim unclaimed listings (competitors can edit them)
- Add missing listings for uncovered directories

### Step 7: Check Review Management

```bash
# Check for review schema
grep -rn "Review\|AggregateRating\|ratingValue" --include="*.tsx" --include="*.jsx" . | grep -v node_modules
```

**Review strategy checklist:**

| Element | Status | Action |
|---------|--------|--------|
| Google review count | [count] | Target 20+ for local visibility |
| Average rating | [X.X] | Maintain 4.0+ |
| Review recency | Last review [date] | Get 1-2 new reviews per month minimum |
| Response rate | [X]% | Reply to 100% of reviews (positive and negative) |
| Review schema on site | [✅/❌] | Add AggregateRating if you display reviews |
| Review request process | [✅/❌] | Send post-service email with review link |

**Review response templates:**

Positive review response:
> "Thank you [Name]! We're glad [specific detail they mentioned]. We appreciate your business and look forward to helping you again."

Negative review response:
> "Thank you for your feedback, [Name]. We're sorry about [specific issue]. We'd like to make this right — please contact us at [email/phone] so we can resolve this for you."

**Review rules:**
- Never buy or fake reviews — Google detects and penalizes
- Don't offer incentives for reviews (violates most platform ToS)
- Respond within 24-48 hours
- Always address specific concerns in negative reviews
- Use the reviewer's name and reference specific details

### Step 8: Output Local SEO Scorecard

```
📍 Local SEO — Scorecard Complete

Business: [name]
Location(s): [city/cities]
Overall local score: [X/100]

Category scores:
  Google Business Profile:  [X/10] — [summary]
  NAP consistency:          [X/10] — [count] inconsistencies found
  Local schema:             [X/10] — [present/missing]
  Location pages:           [X/10] — [count] pages, unique content check
  Local keywords:           [X/10] — [coverage summary]
  Citations/directories:    [X/10] — [count] verified, [count] missing
  Reviews:                  [X/10] — [count] reviews, [rating] avg

Priority action items:
  🔴 Critical:
    1. [e.g., "Claim unclaimed Google Business Profile"]
    2. [e.g., "Fix NAP inconsistency on Yelp listing"]
  🟠 High:
    3. [e.g., "Add LocalBusiness schema to homepage"]
    4. [e.g., "Create unique location pages for 3 service areas"]
  🟡 Medium:
    5. [e.g., "Add local keywords to title tags"]
    6. [e.g., "Submit to 5 missing citation directories"]
  🔵 Low:
    7. [e.g., "Implement review request email workflow"]

Next steps:
1. Fix all Critical items this week
2. Submit to missing citation directories
3. Set up review request workflow
4. Update GBP with weekly posts and fresh photos
5. Re-audit in 3 months
```

## Level History

- **Lv.1** — Base: Google Business Profile audit, NAP consistency verification, LocalBusiness schema generation, location page requirements, local keyword targeting, citation/directory audit, review management with response templates, scored local SEO output. (Origin: MemStack Pro v3.2, Mar 2026)
