---
name: product-description
description: "Use when the user says 'product description', 'product listing', 'product copy', 'Amazon listing', 'Shopify description', or wants to write optimized product listing copy for an e-commerce platform."
---

# 🏷️ Product Description — E-Commerce Listing Copy
*Write conversion-optimized product descriptions with benefit-driven headlines, feature bullets, storytelling, specs, and platform-specific SEO formatting.*

## Activation

When this skill activates, output:

`🏷️ Product Description — Writing your product listing...`

| Context | Status |
|---------|--------|
| **User says "product description", "product listing", "product copy"** | ACTIVE |
| **User wants Amazon, Shopify, or e-commerce listing copy** | ACTIVE |
| **User mentions product features, benefits, or listing optimization** | ACTIVE |
| **User wants pricing strategy (not copy)** | DORMANT — see pricing-strategy |
| **User wants a full sales funnel (product page is one piece)** | DORMANT — see sales-funnel |
| **User wants SEO for a website (not a product listing)** | DORMANT — see seo-geo skill |

## Protocol

### Step 1: Gather Inputs

Ask the user for:
- **Product name**: What is the product called?
- **Category**: What type of product? (electronics, clothing, software, food, etc.)
- **Key features**: Top 5-7 features or specifications
- **Target buyer**: Who buys this? (demographics, needs, pain points)
- **Price point**: How much does it cost?
- **Platform**: Where is this being sold? (Amazon, Shopify, own website, Etsy, eBay)
- **Competitors**: What are they competing against?
- **Unique selling point**: What makes this different?
- **Target keyword**: Primary SEO keyword (optional — skill can suggest)

### Step 2: Write the Headline

Lead with the primary benefit, not the product name:

**Headline formulas:**

| Formula | Example | Platform |
|---------|---------|----------|
| **[Product] — [Primary Benefit]** | "ErgoDesk Pro — Eliminate Back Pain with Adjustable Standing" | Amazon |
| **[Benefit] + [Product Category]** | "Ultra-Quiet Sleep Fan with 12-Speed White Noise Control" | Amazon |
| **[Product Name]: [Outcome]** | "ZenBrew: Pour-Over Coffee in 90 Seconds" | Shopify |
| **[Adjective] [Product] for [Audience]** | "Professional Wireless Microphone for Content Creators" | Multi-platform |

**Headline rules by platform:**

| Platform | Max Length | SEO Focus |
|----------|-----------|-----------|
| **Amazon** | 200 chars (80 visible on mobile) | Keywords in first 80 chars |
| **Shopify** | No limit (H1 tag) | Primary keyword + benefit |
| **Etsy** | 140 chars | Long-tail keywords, specific descriptors |
| **Own site** | No limit | SEO title tag ≤ 60 chars |

Include the target keyword naturally in the headline. Don't keyword-stuff.

### Step 3: Write Benefit-Driven Bullet Points

Transform features into benefits using the Feature → Benefit format:

```
── BULLET POINTS ──────────────────────────

• [FEATURE]: [BENEFIT — what this means for the buyer]
  Example: "Noise-canceling microphone → Crystal-clear calls even in noisy coffee shops"

• [FEATURE]: [BENEFIT]
  Example: "12-hour battery → All-day power from morning commute to evening workout"

• [FEATURE]: [BENEFIT]
  Example: "IPX7 waterproof → Sweat-proof and rain-proof — take it anywhere"

• [FEATURE]: [BENEFIT]
  Example: "One-touch pairing → Connect to your phone in 3 seconds flat"

• [FEATURE]: [BENEFIT]
  Example: "30-day money-back guarantee → Try risk-free — love it or return it"
```

**Bullet writing rules:**
- Lead with the benefit, follow with the feature (inverted from spec sheets)
- 5-7 bullets for Amazon, 3-5 for Shopify, 3-4 for Etsy
- Use title case or start with action verbs for scannability
- Include one bullet about guarantee/support/trust
- Each bullet should answer a potential objection
- Bold the first few words of each bullet (Amazon allows HTML in some contexts)

### Step 4: Write Storytelling Paragraph

Paint a picture of life WITH this product:

```
── PRODUCT STORY ──────────────────────────

[Opening — the problem]
You know that feeling when [pain point the buyer experiences].
[Specific scenario that makes the buyer nod in recognition.]

[The transformation]
[Product Name] changes that. [Describe the experience of using the product.
What does the buyer's day look like now? What frustration is gone?
What do they gain — time, money, confidence, comfort?]

[Social proof or credibility]
[Trusted by X customers / Featured in Y / Built by Z with N years experience.]

[Close — reinforce the decision]
[Make the buyer feel smart for choosing this product.
Remove any last hesitation.]
```

**Storytelling rules:**
- Use "you" language — it's about THEM, not the product
- Be specific — "saves 45 minutes every morning" not "saves time"
- Address the emotional benefit, not just the functional one
- Keep it to 100-200 words (scannable, not a novel)
- One paragraph = one idea

### Step 5: Technical Specifications

Present specs in a clean, scannable format:

```
── SPECIFICATIONS ─────────────────────────

Dimensions:       [L × W × H] in / cm
Weight:           [X] oz / g
Material:         [material]
Color options:    [colors available]
Compatibility:    [devices, systems, standards]
Battery:          [capacity, life, charge time]
Connectivity:     [Bluetooth 5.3, USB-C, Wi-Fi, etc.]
Warranty:         [duration and coverage]
In the box:       [list of included items]
Certifications:   [FCC, CE, UL, etc.]
```

**Spec rules:**
- Include only specs buyers actually care about
- Use standard units (provide both imperial and metric if selling globally)
- List what's IN THE BOX — reduces "what's included?" questions
- Highlight certifications for trust-building

### Step 6: SEO Optimization

Optimize for the target platform's search algorithm:

**Amazon SEO:**
- **Title**: Primary keyword in first 80 chars, secondary keywords after
- **Bullets**: Include 2-3 related keywords naturally
- **Description**: Use remaining relevant keywords
- **Backend keywords**: Misspellings, synonyms, Spanish translations (250 char limit)
- **A+ Content**: Enhanced brand content with images and comparison charts

**Shopify SEO:**
- **URL slug**: `/products/[primary-keyword]`
- **Meta title**: `[Product Name] — [Primary Benefit] | [Brand]` (≤ 60 chars)
- **Meta description**: Benefit-focused summary with keyword (≤ 155 chars)
- **Alt text**: Descriptive image alt text with keywords
- **Schema markup**: Product schema with price, availability, reviews

**General keyword placement:**
```
Title:          [primary keyword] ← MUST
Bullet 1:      [primary keyword] ← SHOULD
Bullet 2-3:    [secondary keywords] ← SHOULD
Description:   [primary + secondary + long-tail keywords] ← MUST
Image alt text: [primary keyword + visual description] ← SHOULD
```

### Step 7: Platform-Specific Formatting

**Amazon:**
```
TITLE (200 chars max):
[Brand] [Product Name] — [Key Feature 1], [Key Feature 2], [Key Feature 3], [Size/Color]

BULLET POINTS (5, 500 chars each):
• BENEFIT IN CAPS — Supporting detail with keyword inclusion
• BENEFIT IN CAPS — Supporting detail with specific numbers
...

PRODUCT DESCRIPTION (2000 chars):
[Storytelling paragraph + additional features + use cases]

BACKEND KEYWORDS (250 chars):
[comma-separated: synonyms, misspellings, related terms]
```

**Shopify:**
```
PRODUCT TITLE:
[Product Name]: [Primary Benefit]

SHORT DESCRIPTION (appears on collection pages):
[1-2 sentences with primary keyword]

FULL DESCRIPTION:
[Rich HTML with headings, bullets, storytelling, and specs]
[Use <h2>, <h3>, <ul>, <strong> for structure]

META TITLE (60 chars):
[Product Name] — [Benefit] | [Brand]

META DESCRIPTION (155 chars):
[Benefit-focused summary with CTA: "Shop now" or "Free shipping"]
```

**Etsy:**
```
TITLE (140 chars):
[Descriptive, keyword-rich — Etsy searches title heavily]
Example: "Minimalist Leather Wallet, Slim Card Holder for Men, RFID Blocking, Personalized Gift"

DESCRIPTION:
[Start with keywords in first 160 chars (used as meta description)]
[Storytelling format works well on Etsy — craft and process story]
[Include care instructions, shipping details, personalization options]

TAGS (13 tags, 20 chars each):
[Long-tail phrases: "slim leather wallet", "personalized gift men"]
```

### Step 8: Output

Present the complete product listing:

```
━━━ PRODUCT LISTING: [Product Name] ━━━━━━

── HEADLINE ───────────────────────────────
[Platform-optimized title]

── BULLET POINTS ──────────────────────────
• [Benefit 1]: [Feature detail]
• [Benefit 2]: [Feature detail]
• [Benefit 3]: [Feature detail]
• [Benefit 4]: [Feature detail]
• [Benefit 5]: [Feature detail]

── PRODUCT STORY ──────────────────────────
[100-200 word storytelling paragraph]

── SPECIFICATIONS ─────────────────────────
[clean spec table]

── SEO ────────────────────────────────────
Primary keyword: [keyword]
Secondary keywords: [list]
Meta title: [title]
Meta description: [description]
Backend keywords: [if Amazon]

── PLATFORM FORMAT ────────────────────────
[Complete copy formatted for target platform]

── CONVERSION NOTES ───────────────────────
• Primary objection addressed: [which bullet handles it]
• Trust signal: [guarantee, reviews, certification]
• Urgency element: [if applicable — limited stock, seasonal]
```

## Inputs
- Product name, category, and features
- Target buyer profile
- Price point
- Platform (Amazon, Shopify, Etsy, own site)
- Competitors and unique selling point
- Target keyword (optional)

## Outputs
- Benefit-led headline optimized for target platform
- 5-7 feature → benefit bullet points
- Storytelling paragraph (100-200 words) painting life with the product
- Technical specifications in scannable format
- SEO optimization (keywords, meta tags, backend keywords)
- Platform-specific formatting (Amazon, Shopify, Etsy)
- Complete product listing copy ready to paste

## Level History

- **Lv.1** — Base: 4 headline formulas by platform, feature → benefit bullet point conversion, storytelling paragraph framework, technical spec template, platform-specific SEO (Amazon/Shopify/Etsy), platform-specific formatting with character limits, paste-ready listing output. (Origin: MemStack v3.2, Mar 2026)
