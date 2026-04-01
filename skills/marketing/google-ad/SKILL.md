---
name: memstack-marketing-google-ad
description: "Use this skill when the user says 'google ad', 'search ad', 'PPC', 'Google Ads', 'responsive search ad', 'ad extensions', or needs keyword groups, headlines, descriptions, and Quality Score optimization for Google Ads. Do NOT use for Facebook/Meta ads or SEO."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# Google Ad — Creating Google Ads campaign...
*Designs search and display campaigns with keyword groups, bidding strategy, responsive search ads, ad extensions, and Quality Score optimization for Google Ads.*

## Activation

When this skill activates, output:

`Google Ad — Creating Google Ads campaign...`

Then execute the protocol below.

## Context Guard

| Context | Status |
|---------|--------|
| User says "Google ad", "search ad", "PPC", "Google Ads" | ACTIVE |
| User says "responsive search ad" or "ad extensions" | ACTIVE |
| User wants to run paid search or display campaigns | ACTIVE |
| User wants Facebook/Meta/Instagram ads | DORMANT — use Facebook Ad |
| User wants organic SEO ranking | DORMANT — use SEO skills |

## Common Mistakes

| Mistake | Why It's Wrong |
|---------|---------------|
| "Bid on your brand name? That's free in organic" | Competitors bid on your brand. Brand campaigns have 5-10x ROAS and protect your traffic. |
| "Use broad match for everything" | Broad match burns budget on irrelevant queries. Start with phrase and exact match. |
| "One ad group, all keywords" | Keyword-to-ad relevance drives Quality Score. Group tightly themed keywords (5-15 per ad group). |
| "Set it and forget it" | Check search term reports weekly. Negative keywords save 20-30% of wasted spend. |
| "More keywords = more traffic" | 10-20 high-intent keywords outperform 200 broad keywords every time. |

## Protocol

### Step 1: Gather Campaign Requirements

If the user hasn't provided details, ask:

> 1. **Product/service** — what are you advertising? (name, URL, price point)
> 2. **Campaign type** — Search, Display, Shopping, or Performance Max?
> 3. **Target location** — countries, states, cities, or radius?
> 4. **Monthly budget** — total ad spend available?
> 5. **Goal** — sales, leads, phone calls, or website traffic?
> 6. **Competitors** — who else bids on these terms?

### Step 2: Keyword Research & Grouping

**Keyword intent tiers:**

| Tier | Intent | Match Type | Example | Priority |
|------|--------|-----------|---------|----------|
| Tier 1 | Bottom-funnel (buy now) | Exact | [buy crm software] | Highest |
| Tier 2 | High-intent (solution-aware) | Exact/Phrase | "best crm for small business" | High |
| Tier 3 | Mid-intent (problem-aware) | Phrase | "how to manage customer data" | Medium |
| Tier 4 | Brand terms | Exact | [your brand name] | Always on |

**Ad group structure (SKAG-inspired):**

```
Campaign: [Product/Service] — Search
├── Ad Group 1: [Core keyword theme A]
│   ├── Keywords (5-15): [exact] and "phrase" match variations
│   ├── Responsive Search Ad 1
│   └── Responsive Search Ad 2
├── Ad Group 2: [Core keyword theme B]
│   ├── Keywords (5-15): [exact] and "phrase" match variations
│   ├── Responsive Search Ad 1
│   └── Responsive Search Ad 2
├── Ad Group 3: [Brand terms]
│   ├── Keywords: [brand name], [brand + product]
│   └── Responsive Search Ad (brand-specific)
└── Ad Group 4: [Competitor terms]
    ├── Keywords: [competitor name + alternative]
    └── Responsive Search Ad (comparison angle)
```

**Negative keyword starter list:**

| Category | Negative Keywords |
|----------|------------------|
| Free-seekers | free, cheap, discount, coupon, torrent, crack |
| Job-seekers | jobs, careers, hiring, salary, interview |
| Education | tutorial, course, how to, what is, definition |
| Irrelevant | review, complaint, lawsuit, scam |

Customize negatives based on the specific business.

### Step 3: Write Responsive Search Ads (RSA)

Each RSA requires up to 15 headlines (30 chars each) and 4 descriptions (90 chars each). Google rotates and tests combinations automatically.

**Headline categories (provide at least 3 from each):**

| Category | Purpose | Example |
|----------|---------|---------|
| Keyword match | Relevance to search query | "CRM Software for Small Teams" |
| Benefit-driven | Why they should care | "Close 3x More Deals" |
| Feature-specific | What's included | "Built-In Email & Pipeline" |
| Social proof | Trust signals | "Trusted by 10,000+ Companies" |
| Urgency/offer | Drive immediate action | "Start Free — No Card Required" |

**RSA template:**

```
Headlines (15):
H1: [Primary keyword + core benefit]              ← pin to position 1
H2: [Secondary benefit or feature]                  ← pin to position 2
H3: [Social proof — customer count or rating]
H4: [Offer — free trial, discount, or guarantee]    ← pin to position 3
H5: [Feature 1]
H6: [Feature 2]
H7: [Feature 3]
H8: [Urgency — limited time or scarcity]
H9: [Question — "Need [solution]?"]
H10: [Brand name + value proposition]
H11: [Competitor comparison angle]
H12: [Outcome — "Get [result] in [timeframe]"]
H13: [Trust — "Award-Winning" or "Top Rated"]
H14: [Location-specific if relevant]
H15: [Alternative phrasing of H1]

Descriptions (4):
D1: [Expand on the core value prop. Include a CTA. 90 chars max.]  ← pin to position 1
D2: [List 2-3 features with benefits. 90 chars max.]
D3: [Social proof + trust signal. 90 chars max.]
D4: [Offer details + urgency + CTA. 90 chars max.]                  ← pin to position 2
```

**Pinning strategy:**
- Pin your best keyword-match headline to position 1 (guarantees relevance)
- Pin your best CTA description to position 1
- Leave all others unpinned so Google can optimize combinations
- Never pin more than 3 elements — over-pinning kills Google's ability to test

### Step 4: Configure Ad Extensions

Ad extensions increase ad real estate and improve CTR by 10-15%.

| Extension | Purpose | Example |
|-----------|---------|---------|
| **Sitelinks** (4-6) | Direct links to key pages | "Pricing", "Features", "Case Studies", "Free Trial" |
| **Callouts** (4-6) | Highlight benefits | "24/7 Support", "No Setup Fee", "Free Migration" |
| **Structured snippets** | List features/categories | Types: "Features: Pipeline, Automation, Reports, API" |
| **Call extension** | Show phone number | Business phone for call-heavy businesses |
| **Price extension** | Show pricing | Plan names with starting prices |
| **Image extension** | Add product images | Product screenshot or logo |
| **Lead form** | Capture leads in-SERP | For lead gen campaigns |

**Sitelink template:**

```
Sitelink 1: [Page Name]
  - Description 1: [Benefit or detail, 35 chars]
  - Description 2: [Supporting detail, 35 chars]
  - URL: [landing page URL]
```

### Step 5: Quality Score Optimization

Quality Score (1-10) directly affects CPC and ad position. Three factors:

| Factor | Weight | How to Improve |
|--------|--------|---------------|
| **Expected CTR** | ~40% | Write compelling headlines, use ad extensions, test RSA variations |
| **Ad relevance** | ~25% | Match ad copy to keyword intent — keyword in headline + description |
| **Landing page experience** | ~35% | Fast load (<3s), mobile-friendly, keyword on page, clear CTA, relevant content |

**Quality Score action plan:**

| Score | Action |
|-------|--------|
| 7-10 | Performing well. Monitor and maintain. |
| 5-6 | Review ad relevance — tighten keyword-to-ad matching. Improve landing page. |
| 3-4 | Rewrite ads. Consider splitting ad group into tighter themes. Audit landing page. |
| 1-2 | Pause keyword. The intent mismatch is too large to fix with copy alone. |

### Step 6: Bidding Strategy & Budget

**Bidding strategy selection:**

| Strategy | When to Use | Minimum Data |
|----------|------------|-------------|
| Manual CPC | Starting out, want full control | None |
| Maximize clicks | Early testing, building data | None |
| Target CPA | Steady conversion volume | 30+ conversions/month |
| Target ROAS | E-commerce with variable order values | 50+ conversions/month |
| Maximize conversions | Budget-constrained, want volume | 15+ conversions/month |

**Budget allocation:**

| Campaign Type | Budget % | Reasoning |
|--------------|----------|-----------|
| Brand terms | 10-15% | Low CPC, high conversion, defensive |
| High-intent non-brand | 50-60% | Primary revenue driver |
| Mid-intent | 20-25% | Pipeline building |
| Competitor terms | 5-10% | Offensive, higher CPC expected |

**Daily budget calculation:**
- Monthly budget ÷ 30.4 = daily budget
- Allocate per campaign based on percentages above
- Google may spend up to 2x daily budget on high-traffic days (averages over month)

### Step 7: Launch Checklist & Optimization Schedule

**Pre-launch checklist:**
- [ ] Conversion tracking verified (test conversion fires correctly)
- [ ] Google Tag installed on all landing pages
- [ ] Negative keyword list applied
- [ ] Ad extensions configured (minimum: sitelinks + callouts)
- [ ] Landing pages load <3 seconds (test on mobile)
- [ ] Geotargeting set correctly
- [ ] Ad schedule matches business hours (if applicable)
- [ ] Budget and bidding strategy configured

**Optimization schedule:**

| Frequency | Action |
|-----------|--------|
| Daily (first week) | Check spend pacing, pause any obvious waste |
| Weekly | Review search terms report, add negatives, check Quality Scores |
| Bi-weekly | Analyze RSA asset performance, replace "Low" rated headlines/descriptions |
| Monthly | Review campaign-level metrics, reallocate budget to top performers |
| Quarterly | Full account audit — structure, keywords, landing pages, competitor landscape |

## Output Format

```markdown
# Google Ads Campaign — [Product/Service]

## Campaign Structure
[Campaign hierarchy diagram with ad groups]

## Keywords by Ad Group
### Ad Group 1: [Theme]
| Keyword | Match Type | Estimated CPC |
[Keyword table]

### Negative Keywords
[Categorized negative keyword list]

## Ad Copy
### Ad Group 1 RSA
[15 headlines + 4 descriptions with pinning notes]

## Extensions
[All configured extensions with copy]

## Bidding & Budget
- Strategy: [Selected strategy]
- Monthly budget: $[amount]
- Daily allocation: [Per-campaign breakdown]

## Quality Score Targets
[Per ad group targets and improvement plan]

## Optimization Calendar
[Weekly/monthly action items]
```

## Completion

```
Google Ad — Complete!

Campaign type: [Search/Display/Shopping]
Ad groups: [Count]
Keywords: [Count] across [match types]
RSA variations: [Count]
Extensions: [Count] types configured
Monthly budget: $[amount]

Next steps:
1. Set up Google Ads conversion tracking on your site
2. Create the campaign in Google Ads using the structure above
3. Upload keyword lists and negative keywords
4. Submit ads for review (usually approved within 24 hours)
5. Monitor daily for the first week, then shift to weekly optimization
```

## Level History

- **Lv.1** — Base: Keyword research with intent tiers, SKAG-inspired ad group structure, RSA templates (15 headlines + 4 descriptions) with pinning strategy, 7 ad extension types, Quality Score optimization (3-factor breakdown), bidding strategy selection matrix, budget allocation by campaign type, negative keyword management, weekly/monthly optimization schedule. (Origin: MemStack Pro v3.2, Mar 2026)
