---
name: memstack-content-product-description
description: "Use this skill when the user says 'product description', 'product listing', 'product copy', 'Amazon listing', 'Shopify listing', 'e-commerce copy', or needs conversion-optimized product descriptions with benefit-driven headlines and platform-specific SEO. Do NOT use for pricing strategy or sales funnels."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# Product Description — Writing product copy...
*Creates conversion-optimized product descriptions with feature-to-benefit conversion, sensory language, SEO keywords, A/B variants, and platform-specific formats for Amazon, Shopify, and Etsy.*

## Activation

When this skill activates, output:

`Product Description — Writing product copy...`

Then execute the protocol below.

## Context Guard

| Context | Status |
|---------|--------|
| User says "product description", "product listing", "product copy" | ACTIVE |
| User says "Amazon listing", "Shopify listing", "e-commerce copy" | ACTIVE |
| User wants to write or improve copy for a product listing | ACTIVE |
| User wants to set pricing | DORMANT — use Pricing Strategy |
| User wants a full sales funnel | DORMANT — use Sales Funnel |

## Common Mistakes

| Mistake | Why It's Wrong |
|---------|---------------|
| "List features, not benefits" | "500mAh battery" means nothing. "Lasts 12 hours so you never run out mid-day" sells. |
| "Generic descriptions" | "High quality product" could describe anything. Be specific about WHAT makes it quality. |
| "Ignore the platform" | Amazon, Shopify, and Etsy have different algorithms, formats, and buyer expectations. |
| "No keywords" | E-commerce search is keyword-driven. No keywords = invisible in search results. |
| "One version only" | A/B testing descriptions is easy and can improve conversion 10-30%. Write variants. |

## Protocol

### Step 1: Gather Product Details

If the user hasn't provided details, ask:

> 1. **Product** — what is it? (name, category, physical/digital)
> 2. **Features** — what are its key specs and features? (list 5-10)
> 3. **Audience** — who buys this? (demographics, use case, pain point)
> 4. **Platform** — where is it listed? (Amazon, Shopify, Etsy, other)
> 5. **Price point** — what does it cost? (affects copy tone and positioning)
> 6. **Competitors** — what are the top 3 alternatives? (for differentiation)

### Step 2: Feature-to-Benefit Conversion

Transform every feature into a customer benefit:

| Feature (What It Is) | Benefit (Why They Care) | Emotional Trigger |
|---------------------|----------------------|------------------|
| [Technical spec] | [Practical outcome] | [Feeling it creates] |

**Examples:**

| Feature | → Benefit | → Emotional |
|---------|----------|------------|
| "Made from organic cotton" | "Gentle on sensitive skin" | "Safe for your baby" |
| "5000mAh battery" | "Lasts 2 full days on one charge" | "Never stress about dying battery" |
| "Adjustable height: 28-36 inches" | "Fits any desk setup, standing or sitting" | "Work comfortably, your way" |
| "Ships in recyclable packaging" | "Zero waste delivery to your door" | "Feel good about your purchase" |

**Conversion formula:**
```
[Feature] → so you can → [Benefit] → which means → [Emotional outcome]
```

### Step 3: Write the Product Description

**Universal structure:**

```markdown
## [Product Title — Keyword-Rich, Benefit-Driven]

### Opening Hook (1-2 sentences)
[Address the pain point or desire. Create an "I need that" reaction.]

### Key Benefits (bullet points)
• [Benefit 1] — [supporting detail]
• [Benefit 2] — [supporting detail]
• [Benefit 3] — [supporting detail]
• [Benefit 4] — [supporting detail]
• [Benefit 5] — [supporting detail]

### Body Description (2-3 short paragraphs)
[Paint a picture of using the product. Use sensory language.
Address the top objection. Include social proof if available.]

### Specifications
[Technical details for comparison shoppers]

### Call to Action
[Urgency or reassurance: "Order now" + guarantee or shipping info]
```

**Sensory language guide:**

| Sense | Words | Use For |
|-------|-------|---------|
| **Touch** | Silky, rugged, lightweight, cushioned, velvety | Clothing, furniture, tools |
| **Sight** | Vibrant, sleek, crystal-clear, polished, matte | Electronics, decor, fashion |
| **Sound** | Whisper-quiet, crisp, deep bass, silent | Electronics, appliances |
| **Taste** | Rich, smooth, zesty, creamy, bold | Food, beverages |
| **Smell** | Fresh, earthy, aromatic, clean, invigorating | Candles, skincare, food |

### Step 4: Platform-Specific Formatting

**Amazon listing format:**

```markdown
## Product Title (200 characters max)
[Brand] [Product Name] — [Key Benefit] [Key Feature] [Size/Variant] — [Use Case]
Example: "EcoBottle Premium Insulated Water Bottle — Keeps Drinks Cold 24 Hours — BPA-Free Stainless Steel, 32oz — Perfect for Hiking & Gym"

## Bullet Points (5 bullets, 200 chars each)
• [BENEFIT IN CAPS] — [Explanation]. [Spec detail].
• [BENEFIT IN CAPS] — [Explanation]. [Spec detail].
• [BENEFIT IN CAPS] — [Explanation]. [Spec detail].
• [BENEFIT IN CAPS] — [Explanation]. [Spec detail].
• [BENEFIT IN CAPS] — [Explanation]. [Spec detail].

## Product Description (2000 chars max)
[Rich HTML-formatted description with headers, paragraphs, and bold text]

## Backend Keywords (250 bytes)
[Hidden keywords separated by spaces — no commas, no repeats, no brand names]
```

**Shopify product page:**

```markdown
## Product Title
[Concise, descriptive, SEO-friendly — 60-70 characters]

## Price + Compare-at Price (if on sale)

## Short Description (visible above the fold)
[2-3 sentences: hook + primary benefit + social proof snippet]

## Full Description (tabbed or expandable)
### Why You'll Love It
[3-5 benefit bullets]

### How It Works
[Use case description or instructions]

### What's Included
[List of everything in the box/package]

### Specifications
[Technical details table]

## SEO
- Meta title: [Product] — [Benefit] | [Brand] (60 chars)
- Meta description: [Compelling summary with CTA] (155 chars)
- URL handle: /products/[keyword-slug]
```

**Etsy listing:**

```markdown
## Title (140 characters)
[Keywords first: "Handmade [Product] for [Occasion] — [Key Feature] [Material] [Size]"]

## Description (first 160 chars appear in search)
[Hook sentence first — this shows in search preview]
[Full description with story element — why you made this, materials used, care instructions]
[Size guide / dimensions]
[Shipping information]
[Care instructions]
[Customization options]

## Tags (13 tags, 20 chars each)
[Long-tail keywords that match buyer search behavior]
[Focus on: material, use case, recipient, occasion, style]

## Attributes
[Fill ALL available attributes — material, color, occasion, style]
```

### Step 5: SEO Keyword Integration

**Keyword research for product listings:**

| Keyword Type | Where to Use | Example |
|-------------|-------------|---------|
| Primary keyword | Title, first sentence of description | "insulated water bottle" |
| Secondary keywords | Bullet points, body description | "BPA-free", "stainless steel", "cold 24 hours" |
| Long-tail keywords | Backend/tags, lower in description | "best water bottle for hiking 2026" |
| Competitor keywords | Backend/tags | "hydroflask alternative", "yeti competitor" |

**Keyword placement rules:**
- Primary keyword appears in: title, first bullet/sentence, one subheading
- Don't keyword-stuff — read it aloud; if it sounds robotic, rewrite
- Backend keywords (Amazon) or tags (Etsy) are invisible — use them for synonyms and misspellings
- Use natural language — "water bottle that keeps drinks cold" beats "cold water bottle insulated"

### Step 6: Write A/B Variants

Write 2 description variants to test:

```markdown
## Variant A: Benefit-Led
[Opens with the primary benefit and emotional outcome]
"Never worry about your drink going warm again. The [Product] keeps
beverages ice-cold for 24 hours..."

## Variant B: Problem-Led
[Opens with the pain point the product solves]
"Tired of lukewarm water halfway through your hike? [Product] uses
double-wall vacuum insulation to keep your drinks cold all day..."
```

**What to A/B test:**
- Headline approach (benefit-led vs. problem-led)
- Bullet point order (most popular benefit first vs. most unique)
- Description length (short punchy vs. detailed comprehensive)
- CTA text ("Add to Cart" vs. "Get Yours Now" vs. "Buy Now — Free Shipping")

### Step 7: Pre-Publish Checklist

- [ ] Primary keyword in title and first sentence
- [ ] All features converted to benefits (no naked specs)
- [ ] Sensory language used where appropriate
- [ ] Platform-specific format followed (Amazon bullets, Shopify tabs, Etsy story)
- [ ] Backend keywords / tags filled in
- [ ] Images referenced match description claims
- [ ] Price and shipping info are accurate
- [ ] Social proof included if available (reviews, awards, "bestseller")
- [ ] Scannability: bullets, bold, short paragraphs
- [ ] Read aloud — does it sound natural and persuasive?
- [ ] Mobile preview checked (most shopping is mobile)

## Output Format

```markdown
# Product Description — [Product Name]

## Platform: [Amazon / Shopify / Etsy]
## Primary Keyword: [Keyword]

### Title
[Platform-optimized title]

### Description
[Full description following platform format from Step 4]

### SEO
[Keywords, meta tags, backend keywords]

### A/B Variant
[Second version for testing]
```

## Completion

```
Product Description — Complete!

Product: [Name]
Platform: [Platform]
Primary keyword: [Keyword]
Benefits highlighted: [Count]
A/B variants: 2
SEO elements: Title, description, backend keywords

Next steps:
1. Upload to your platform using the formatted copy
2. Add high-quality images that match the description claims
3. Set up A/B test between Variant A and Variant B
4. Monitor conversion rate for 2 weeks before picking a winner
5. Update quarterly based on new reviews and competitor changes
```

## Level History

- **Lv.1** — Base: Feature-to-benefit conversion formula, sensory language guide (5 senses), universal product description structure, platform-specific formats (Amazon, Shopify, Etsy), SEO keyword integration with placement rules, A/B testing variants (benefit-led vs. problem-led), pre-publish checklist. (Origin: MemStack Pro v3.2, Mar 2026)
