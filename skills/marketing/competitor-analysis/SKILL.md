---
name: memstack-marketing-competitor-analysis
description: "Use this skill when the user says 'competitor analysis', 'competitive analysis', 'compare products', 'market positioning', 'competitive gaps', or needs pricing, feature, and messaging comparisons against competitors. Do NOT use for setting your own pricing strategy."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# Competitor Analysis — Analyzing competitive landscape...
*Provides a structured 5-point competitive analysis covering pricing, features, positioning, traffic sources, and weaknesses — output as a comparison matrix with strategic recommendations.*

## Activation

When this skill activates, output:

`Competitor Analysis — Analyzing competitive landscape...`

Then execute the protocol below.

## Context Guard

| Context | Status |
|---------|--------|
| User says "competitor analysis", "competitive analysis" | ACTIVE |
| User says "compare products" or "market positioning" | ACTIVE |
| User wants to understand competitive landscape before building/launching | ACTIVE |
| User wants to set their own pricing | DORMANT — use Pricing Strategy |
| User wants to write ad copy against competitors | DORMANT — use Facebook Ad or Google Ad |

## Common Mistakes

| Mistake | Why It's Wrong |
|---------|---------------|
| "Copy the market leader" | What works at their scale and brand recognition won't work for a newcomer. Find gaps, don't clone. |
| "They do everything, we can't compete" | Incumbents have feature bloat. Pick 1-3 things and do them 10x better. |
| "Ignore indirect competitors" | Spreadsheets and manual processes are often the real competition, not just SaaS tools. |
| "Only look at features" | Positioning, pricing model, and distribution channel matter more than feature checklists. |
| "One-time analysis" | Markets shift. Re-run competitive analysis quarterly. |

## Protocol

### Step 1: Identify Competitors

If the user hasn't provided competitors, ask:

> 1. **Your product** — what do you offer? (name, category, price point)
> 2. **Known competitors** — who do customers compare you to?
> 3. **Market** — B2B or B2C? Industry vertical? Geographic focus?

Then identify three competitor tiers:

| Tier | Definition | How Many |
|------|-----------|----------|
| **Direct** | Same product category, same target market | 3-5 |
| **Indirect** | Different approach to the same problem | 2-3 |
| **Aspirational** | Market leaders you aim to compete with eventually | 1-2 |

**Research sources:**
- Their website (pricing page, features page, about page)
- G2, Capterra, Trustpilot reviews (filter by 1-3 star for weaknesses)
- Product Hunt, Reddit discussions, Twitter mentions
- SimilarWeb or SEMrush for traffic data (if available)
- Their blog, changelog, and social media for positioning signals
- Job postings (reveal strategic priorities and tech stack)

### Step 2: Pricing Comparison

Build a pricing comparison matrix:

| | Your Product | Competitor A | Competitor B | Competitor C |
|---|---|---|---|---|
| **Free tier** | Yes/No | | | |
| **Entry price** | $X/mo | | | |
| **Mid-tier price** | $X/mo | | | |
| **Enterprise price** | $X/mo or custom | | | |
| **Pricing model** | Per seat / flat / usage | | | |
| **Annual discount** | X% | | | |
| **Free trial** | X days | | | |

**Pricing analysis questions:**
- Who is the cheapest? Who is the most expensive? Where do you sit?
- What pricing model do they use? (per seat, per usage, flat rate, freemium)
- Is there a pricing gap in the market? (e.g., no good option between $0 and $99/mo)
- What's their free-to-paid conversion strategy?

### Step 3: Feature Comparison

Build a feature matrix for the top 15-20 features customers care about:

| Feature | Your Product | Comp A | Comp B | Comp C |
|---------|---|---|---|---|
| [Feature 1] | Full | Full | Partial | None |
| [Feature 2] | Full | None | Full | Full |
| [Feature 3] | Partial | Full | Full | None |
| ... | | | | |

**Feature rating scale:**
- **Full** — feature is complete and polished
- **Partial** — feature exists but limited or in beta
- **None** — feature not available
- **Superior** — best-in-class implementation

**Feature analysis questions:**
- Which features do ALL competitors have? (table stakes — you must have them)
- Which features does NO competitor have? (potential differentiator if valuable)
- Where are competitors weakest? (opportunity to excel)
- What features do customers complain about most in reviews?

### Step 4: Positioning & Messaging Analysis

For each competitor, document:

```
Competitor: [Name]
Tagline: "[Their homepage tagline]"
Target audience: [Who they're clearly targeting]
Key message: [Their primary value proposition]
Tone: [Professional / Casual / Technical / Fun]
Positioning: [Cheapest / Best / Easiest / Most Powerful / Niche-specific]

Homepage hero:
- Headline: "[Exact text]"
- Subheadline: "[Exact text]"
- CTA: "[Button text]"
- Social proof: "[What they show — logos, numbers, testimonials]"
```

**Positioning map:**

Plot competitors on a 2x2 matrix using the two most relevant axes for your market:

```
                    Premium
                      │
                      │
    Complex ──────────┼────────── Simple
                      │
                      │
                   Affordable
```

Place each competitor (and yourself) on the map. Identify the open quadrant — that's your positioning opportunity.

### Step 5: Traffic & Distribution Analysis

For each competitor, research:

| Channel | Comp A | Comp B | Comp C |
|---------|--------|--------|--------|
| **Organic search** (estimated monthly visits) | | | |
| **Paid search** (running Google Ads?) | Y/N | | |
| **Social media** (primary platform + follower count) | | | |
| **Content marketing** (blog frequency, topics) | | | |
| **Email** (newsletter? nurture sequences?) | | | |
| **Referral/affiliate** (partner programs?) | | | |
| **Community** (Slack, Discord, forum?) | | | |
| **Product Hunt** (launched? ranking?) | | | |

**Distribution analysis questions:**
- Which channels drive the most traffic for each competitor?
- Are there underutilized channels where you can win? (e.g., YouTube, podcast)
- What content topics are they ranking for? (use SEO tools or manual search)
- What's their social media engagement rate, not just follower count?

### Step 6: Weakness & Opportunity Analysis

For each competitor, extract weaknesses from:
- **1-3 star reviews** on G2, Capterra, Trustpilot, App Store
- **Reddit/Twitter complaints** — search "[competitor] sucks" or "[competitor] alternative"
- **Churned customer feedback** — if you can find it

**Weakness categories:**

| Category | Comp A Weakness | Comp B Weakness | Comp C Weakness |
|----------|----------------|----------------|----------------|
| **UX/Design** | | | |
| **Performance** | | | |
| **Pricing** | | | |
| **Support** | | | |
| **Missing features** | | | |
| **Integration gaps** | | | |
| **Onboarding** | | | |

**SWOT summary per competitor:**

```
Competitor: [Name]
Strengths: [2-3 key strengths]
Weaknesses: [2-3 key weaknesses]
Opportunities: [What you can exploit]
Threats: [What they might do that hurts you]
```

### Step 7: Strategic Recommendations

Based on the analysis, provide:

**1. Positioning recommendation:**
> "Position as [positioning angle] because [reasoning based on competitive gaps]"

**2. Feature priority (build these first):**
| Priority | Feature | Rationale |
|----------|---------|-----------|
| P0 | [Feature] | Table stakes — every competitor has it |
| P0 | [Feature] | Biggest competitor weakness |
| P1 | [Feature] | Differentiator — no one does this well |
| P2 | [Feature] | Nice-to-have — builds on P1 |

**3. Pricing recommendation:**
> "[Pricing strategy] at [$X/mo] because [competitive gap or positioning reason]"

**4. Channel recommendation:**
> "Focus on [2-3 channels] because [competitors are weak here / audience is underserved]"

**5. Messaging recommendation:**
> "Lead with [angle] because [no competitor owns this message]"

## Output Format

```markdown
# Competitive Analysis — [Your Product] vs. [Market]

## Competitor Overview
| | Your Product | Comp A | Comp B | Comp C |
[High-level summary row: founded, team size, funding, pricing]

## Pricing Comparison
[Pricing matrix from Step 2]

## Feature Comparison
[Feature matrix from Step 3]

## Positioning Map
[2x2 matrix from Step 4]

## Traffic & Distribution
[Channel table from Step 5]

## Weakness Analysis
[Weakness table from Step 6]

## SWOT Summaries
[Per-competitor SWOT from Step 6]

## Strategic Recommendations
1. Positioning: [Recommendation]
2. Feature priorities: [P0/P1/P2 list]
3. Pricing: [Recommendation]
4. Channels: [Recommendation]
5. Messaging: [Recommendation]

## Open Questions
[Anything that needs more research or customer validation]
```

## Completion

```
Competitor Analysis — Complete!

Competitors analyzed: [Count] ([direct] direct, [indirect] indirect)
Pricing gaps found: [Count]
Feature opportunities: [Count]
Recommended positioning: [One-line summary]

Next steps:
1. Validate findings with 5-10 customer interviews
2. Run positioning statement by your team
3. Update product roadmap based on feature priorities
4. Re-run this analysis next quarter
```

## Level History

- **Lv.1** — Base: 3-tier competitor identification, pricing comparison matrix, feature comparison with rating scale, positioning & messaging capture (tagline, hero, 2x2 map), traffic & distribution channel analysis, weakness extraction from reviews/social, SWOT per competitor, 5-point strategic recommendations (positioning, features, pricing, channels, messaging). (Origin: MemStack Pro v3.2, Mar 2026)
