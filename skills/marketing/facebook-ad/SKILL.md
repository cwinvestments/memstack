---
name: memstack-marketing-facebook-ad
description: "Use this skill when the user says 'facebook ad', 'FB ad', 'Meta ad', 'Instagram ad', or needs social media ad copy with targeting, creative direction, and A/B test plans for Meta Ads Manager. Do NOT use for Google search ads or organic social content."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# Facebook Ad — Creating Meta ad campaign...
*Creates complete ad campaigns with audience targeting, ad copy variations, creative direction, budget allocation, and A/B testing protocol for Meta Ads Manager.*

## Activation

When this skill activates, output:

`Facebook Ad — Creating Meta ad campaign...`

Then execute the protocol below.

## Context Guard

| Context | Status |
|---------|--------|
| User says "Facebook ad", "FB ad", "Meta ad", "Instagram ad" | ACTIVE |
| User needs social media ad copy with targeting | ACTIVE |
| User wants to run paid campaigns on Meta platforms | ACTIVE |
| User wants Google Search or Display ads | DORMANT — use Google Ad |
| User wants organic social media content | DORMANT — not an ad skill |

## Common Mistakes

| Mistake | Why It's Wrong |
|---------|---------------|
| "Target everyone" | Broad audiences burn budget. Start narrow (1-5M), expand after finding winners. |
| "One ad, one audience" | Always test 3-5 ad variations per ad set. Meta's algorithm needs options. |
| "Start with $5/day" | Too little for the algorithm to learn. Minimum $20/day per ad set for meaningful data. |
| "Judge ads after 24 hours" | Meta needs 50+ conversions per ad set per week to exit learning phase. Wait 3-7 days. |
| "Use stock photos" | UGC-style creative outperforms polished studio content 2-3x on Meta. |

## Protocol

### Step 1: Gather Campaign Requirements

If the user hasn't provided details, ask:

> 1. **Product/service** — what are you promoting? (name, price, URL)
> 2. **Objective** — leads, sales, traffic, or brand awareness?
> 3. **Target audience** — who is the ideal customer? (age, interests, pain points)
> 4. **Budget** — daily or monthly ad spend?
> 5. **Existing assets** — do you have customer testimonials, product photos, or video?
> 6. **Previous campaigns** — any past Meta ads data to build on?

### Step 2: Define Campaign Structure

Build the campaign using Meta's three-tier hierarchy:

```
Campaign (1 objective)
├── Ad Set 1: [Audience A] — $[budget]/day
│   ├── Ad 1: [Hook A + Creative A]
│   ├── Ad 2: [Hook B + Creative A]
│   └── Ad 3: [Hook A + Creative B]
├── Ad Set 2: [Audience B] — $[budget]/day
│   ├── Ad 1: [Hook A + Creative A]
│   ├── Ad 2: [Hook B + Creative A]
│   └── Ad 3: [Hook A + Creative B]
└── Ad Set 3: [Lookalike/Retargeting] — $[budget]/day
    ├── Ad 1: [Social proof hook]
    ├── Ad 2: [Urgency hook]
    └── Ad 3: [Testimonial creative]
```

**Campaign objective mapping:**

| Goal | Meta Objective | Optimization Event |
|------|---------------|-------------------|
| Email signups | Leads | Lead form submission |
| Product sales | Sales | Purchase |
| Website traffic | Traffic | Landing page views |
| App installs | App Promotion | App install |
| Brand awareness | Awareness | Reach or ThruPlay |
| Webinar signups | Leads | Lead form submission |

### Step 3: Build Audience Targeting

**Audience A — Interest-based (cold):**
- Age: [range]
- Gender: [if relevant]
- Location: [countries/regions]
- Interests: [3-5 relevant interests]
- Behaviors: [purchase behavior, device usage]
- Audience size target: 1-5 million

**Audience B — Narrowed interest stack:**
- Must match: [Interest 1] AND [Interest 2]
- Exclude: [competitors' audiences or existing customers]
- Audience size target: 500K-2M

**Audience C — Lookalike:**
- Source: Customer list, website visitors, or video viewers
- Lookalike %: Start at 1% (closest match), test up to 3%
- Country: Same as primary market

**Retargeting audiences (create separately):**
- Website visitors (last 30 days) — exclude purchasers
- Video viewers (75%+ watched) — last 60 days
- Engagement (Instagram/Facebook) — last 90 days
- Cart abandoners — last 14 days

### Step 4: Write Ad Copy Variations

Write 3 copy variations for each hook type:

**Hook Type 1 — Problem-Agitation:**
```
Primary text:
[Problem question that stops the scroll]

[Agitation — what happens if they don't solve it]

[Introduce your solution in 1-2 sentences]

[Key benefit 1]
[Key benefit 2]
[Key benefit 3]

[CTA: Click below to [desired action]]

Headline: [Benefit-driven, 5-8 words]
Description: [Supporting detail or urgency, 20 words max]
CTA button: [Learn More / Shop Now / Sign Up / Get Offer]
```

**Hook Type 2 — Social Proof:**
```
Primary text:
"[Customer testimonial quote — specific result]"

[Bridge: Explain how others are getting the same result]

Here's what you get:
✓ [Benefit 1]
✓ [Benefit 2]
✓ [Benefit 3]

[CTA with urgency or limited offer]

Headline: [Result-focused, 5-8 words]
Description: [Star rating, customer count, or guarantee]
CTA button: [Get Started / Try Free / Shop Now]
```

**Hook Type 3 — Direct Offer:**
```
Primary text:
[Bold claim or stat that grabs attention]

[1-2 sentences explaining the offer]

What's included:
→ [Item/benefit 1]
→ [Item/benefit 2]
→ [Item/benefit 3]

[Urgency: Limited time / spots / bonus]

[CTA: Get yours before [deadline]]

Headline: [Offer + urgency, 5-8 words]
Description: [Price, discount, or guarantee]
CTA button: [Get Offer / Claim Discount / Buy Now]
```

**Ad copy rules:**
- Primary text: 125 characters visible before "See more" — front-load the hook
- Headline: 40 characters max for full display
- Description: 25 characters max on mobile
- Use line breaks for readability (no walls of text)
- Emojis: 1-2 max, only if audience-appropriate

### Step 5: Creative Direction

**Image ads (1080x1080 or 1080x1350):**
- Style: UGC (user-generated content) feel outperforms polished studio
- Text overlay: Keep under 20% of image area
- Include: Product in use, face showing emotion, before/after, or bold text overlay
- Avoid: Cluttered backgrounds, tiny text, stock photo look

**Video ads (9:16 for Reels/Stories, 1:1 for Feed):**
- Hook: First 3 seconds must stop the scroll (movement, text, question)
- Length: 15-30 seconds for cold traffic, 30-60 seconds for retargeting
- Structure: Hook → Problem → Solution → Proof → CTA
- Captions: Always add — 85% of videos are watched without sound
- Thumbnail: Custom frame that works as a static image

**Creative testing matrix:**

| Test | Variable | Hold Constant |
|------|----------|--------------|
| Test 1 | 3 different hooks (first 3 sec) | Same body, same audience |
| Test 2 | Image vs. Video vs. Carousel | Same copy, same audience |
| Test 3 | UGC vs. polished creative | Same copy, same audience |

### Step 6: Budget Allocation & Bidding

**Budget framework:**

| Phase | Duration | Daily Budget/Ad Set | Goal |
|-------|----------|-------------------|------|
| Testing | 3-7 days | $20-50 | Find winning ad + audience combos |
| Validation | 7-14 days | $50-100 | Confirm CPA is sustainable |
| Scaling | Ongoing | 20% increase every 3-4 days | Increase volume while holding CPA |

**Bidding strategy:**
- Start with: Lowest cost (automatic bidding)
- Switch to: Cost cap once you know your target CPA
- Set cost cap at: 1.2x your target CPA (gives algorithm room)
- Never: Set bid cap too low — the algorithm won't spend and won't learn

**Scaling rules:**
- Horizontal scaling: Duplicate winning ad set to new audiences
- Vertical scaling: Increase budget 20% every 3-4 days (never more than 20%)
- Kill rule: If CPA exceeds 2x target for 3+ days, pause and diagnose

### Step 7: A/B Testing Protocol

**Test priority order:**
1. **Audiences** (biggest impact) — Test 3+ audiences first
2. **Creative format** (image vs. video vs. carousel)
3. **Hook/headline** (first thing people see)
4. **Body copy** (supporting message)
5. **CTA** (button text and offer framing)

**Testing rules:**
- Change ONE variable at a time
- Minimum budget: $20/day per variation
- Minimum duration: 3-7 days (or 50+ conversion events)
- Winner threshold: 20%+ better CPA with statistical significance
- Use Meta's built-in A/B test tool for clean attribution

**Testing log template:**

| Test # | Variable | Variation A | Variation B | Winner | CPA Difference |
|--------|----------|------------|------------|--------|---------------|
| 1 | Audience | Interest stack | 1% Lookalike | | |
| 2 | Creative | UGC video | Product image | | |
| 3 | Hook | Problem Q | Bold stat | | |

## Output Format

Deliver the complete campaign as:

```markdown
# Meta Ad Campaign — [Product/Service Name]

## Campaign Settings
- **Objective:** [Objective]
- **Daily budget:** $[amount] ([X] ad sets × $[amount] each)
- **Optimization event:** [Event]
- **Schedule:** [Start date] — ongoing

## Audiences
### Ad Set 1: [Audience name]
[Targeting details]

### Ad Set 2: [Audience name]
[Targeting details]

### Ad Set 3: [Retargeting]
[Targeting details]

## Ad Copy
### Variation 1: [Hook type]
[Complete ad copy]

### Variation 2: [Hook type]
[Complete ad copy]

### Variation 3: [Hook type]
[Complete ad copy]

## Creative Direction
[Image/video specs and style notes]

## Budget & Timeline
[Phase breakdown with daily budgets]

## A/B Testing Plan
[Test priority queue with log template]

## Tracking Setup
- Meta Pixel: [events to track]
- UTM parameters: [structure]
- Conversion window: [7-day click, 1-day view recommended]
```

## Completion

```
Facebook Ad — Complete!

Campaign objective: [Objective]
Ad sets: [Count] audiences
Ad variations: [Count] per ad set
Total ads: [Count]
Daily budget: $[amount]
Testing duration: [X] days before first optimization

Next steps:
1. Install Meta Pixel on your website (if not already done)
2. Upload custom audiences and create lookalikes
3. Create ads in Meta Ads Manager using the copy above
4. Set up conversion tracking events
5. Launch and wait 3-7 days before making changes
6. Review testing log weekly and kill underperformers
```

## Level History

- **Lv.1** — Base: Campaign structure (3-tier hierarchy), audience targeting (interest, narrowed, lookalike, retargeting), 3 copy formulas (problem-agitation, social proof, direct offer), creative direction (image + video specs), budget allocation by phase, bidding strategy, scaling rules, A/B testing protocol with priority order and log template. (Origin: MemStack Pro v3.2, Mar 2026)
