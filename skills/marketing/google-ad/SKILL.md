---
name: google-ad
description: "Use when the user says 'google ad', 'search ad', 'PPC', 'Google Ads', 'AdWords', 'responsive search ad', or wants paid search campaign copy."
---


# 🔍 Google Ad — Search Campaign Builder
*Generate responsive search ads, keyword groups, and extensions ready to import into Google Ads.*

## Activation

When this skill activates, output:

`🔍 Google Ad — Building your search campaign...`

| Context | Status |
|---------|--------|
| **User says "google ad", "search ad", "PPC", "Google Ads"** | ACTIVE |
| **User wants responsive search ad copy** | ACTIVE |
| **User mentions keywords, ad extensions, or Quality Score** | ACTIVE |
| **User wants Facebook/social ads** | DORMANT — see facebook-ad |
| **User wants SEO (organic search, not paid)** | DORMANT — see seo-geo skill |

## Protocol

### Step 1: Gather Inputs

Ask the user for:
- **Product/service**: What are you advertising?
- **Target keywords**: 5-10 seed keywords (or let the skill suggest them)
- **Landing page URL**: Where does the ad send people?
- **Monthly budget**: Total Google Ads spend
- **Geographic targeting**: Country, region, or city (optional)
- **Competitor names**: For negative keyword planning (optional)

### Step 2: Write Responsive Search Ads

Generate assets for Google's responsive search ad format:

**15 Headlines** (max 30 characters each):
- Headlines 1-3: Include primary keyword + benefit
- Headlines 4-6: Include secondary keywords + differentiation
- Headlines 7-9: Social proof (numbers, awards, reviews)
- Headlines 10-12: CTA-focused (Get, Try, Start, Save, etc.)
- Headlines 13-15: Urgency/offer-focused (Limited, Free, Today, etc.)

**4 Descriptions** (max 90 characters each):
- Description 1: Value proposition + primary keyword
- Description 2: Features/benefits list
- Description 3: Social proof + trust signal
- Description 4: CTA + urgency element

Pin recommendations: Pin keyword-rich headline to position 1, CTA headline to position 3.

### Step 3: Keyword Grouping

Organize keywords into tightly themed ad groups:

| Ad Group | Keywords | Match Type |
|----------|----------|------------|
| **Brand** | [brand name], [brand + product] | Exact |
| **Product** | [product type], [product category] | Phrase |
| **Problem** | [pain point], [problem phrase] | Phrase |
| **Competitor** | [competitor name + alternative] | Exact |
| **Long-tail** | [specific use case queries] | Broad (with monitoring) |

For each keyword:
- Provide exact `[keyword]`, phrase `"keyword"`, and broad match versions
- Estimate search volume tier (high/medium/low)
- Suggest max CPC bid range

### Step 4: Negative Keywords

Build a negative keyword list to prevent wasted spend:
- **Universal negatives**: free, cheap, download, torrent, DIY, how to (if selling premium)
- **Job-related**: jobs, career, salary, hiring, intern
- **Informational**: what is, definition, wiki, tutorial (unless content marketing)
- **Competitor brand terms**: (if not running competitor campaigns)
- **Irrelevant modifiers**: industry-specific terms that attract wrong audience

Group negatives by category for easy management.

### Step 5: Ad Extensions

Write all applicable extension types:

**Sitelinks** (4-6):
- Each with: link text (25 chars), description line 1 (35 chars), description line 2 (35 chars), URL

**Callouts** (4-6):
- Short benefit phrases (25 chars each): "Free Shipping", "24/7 Support", etc.

**Structured Snippets** (2-3 headers):
- Header type + values. Example: "Types: Basic, Pro, Enterprise"

**Other extensions** (recommend if applicable):
- Call extension (phone number)
- Location extension
- Price extension (product/tier cards)
- Promotion extension (sales/offers)

### Step 6: Landing Page Alignment Check

Audit the landing page against ad copy:
- **Keyword presence**: Do target keywords appear in page H1, H2, body?
- **Message match**: Does the page headline match the ad headline?
- **CTA consistency**: Does the page CTA match the ad promise?
- **Load speed**: Flag if landing page appears slow (affects Quality Score)
- **Mobile readiness**: Flag if not mobile-responsive

Provide specific recommendations for alignment fixes.

### Step 7: Quality Score Optimization Tips

Provide actionable tips for each Quality Score factor:
- **Expected CTR**: Use power words, numbers, question marks in headlines
- **Ad relevance**: Ensure keywords appear in at least 3 headlines and 2 descriptions
- **Landing page experience**: Match ad intent, fast load, clear CTA, mobile-friendly

### Step 8: Output

Present the complete campaign structure:

```
━━━ CAMPAIGN: [Product Name] Search ━━━━━━━━━━

── AD GROUP 1: [Theme] ──────────────────────
Keywords: [list with match types]
Negative KWs: [list]

  Headlines (15):
  H1:  [pinned — keyword + benefit]
  H2:  [text]
  ...
  H15: [text]

  Descriptions (4):
  D1: [value prop]
  D2: [features]
  D3: [social proof]
  D4: [CTA + urgency]

── EXTENSIONS ───────────────────────────────
Sitelinks:
  1. [link text] — [URL] — [desc]
  ...

Callouts: [list]
Snippets: [header]: [values]

── LANDING PAGE NOTES ──────────────────────
[alignment recommendations]

── QUALITY SCORE TIPS ──────────────────────
[actionable improvements]
```

## Inputs
- Product/service description
- Target keywords (or seed terms)
- Landing page URL
- Monthly budget
- Geographic targeting (optional)

## Outputs
- 15 headlines + 4 descriptions (responsive search ad format)
- Keyword groups with match types across 4-5 ad groups
- Negative keyword list by category
- Ad extensions (sitelinks, callouts, structured snippets, others)
- Landing page alignment audit
- Quality Score optimization tips
- Campaign structure ready for Google Ads import

## Level History

- **Lv.1** — Base: Responsive search ad generation (15 headlines + 4 descriptions), keyword grouping with match types, negative keyword lists, full ad extensions suite, landing page alignment audit, Quality Score optimization tips, import-ready campaign format. (Origin: MemStack v3.2, Mar 2026)
