---
name: pricing-strategy
description: "Use when the user says 'pricing strategy', 'how to price', 'pricing model', 'tier pricing', 'pricing table', 'what to charge', or needs help setting prices for a product or service."
---


# 💰 Pricing Strategy — Revenue-Optimized Pricing Design
*Analyze pricing models, design tier structures, and apply pricing psychology for maximum conversion and revenue.*

## Activation

When this skill activates, output:

`💰 Pricing Strategy — Designing your pricing architecture...`

| Context | Status |
|---------|--------|
| **User says "pricing strategy", "how to price", "pricing model"** | ACTIVE |
| **User wants to design tiers, set prices, or compare models** | ACTIVE |
| **User asks about pricing psychology or A/B testing prices** | ACTIVE |
| **User wants competitor pricing comparison** | DORMANT — see competitor-analysis |
| **User wants to generate a client quote/proposal** | DORMANT — see quill skill |

## Protocol

### Step 1: Gather Inputs

Ask the user for:
- **Product type**: SaaS, physical product, service, digital product, info product
- **Cost structure**: COGS, delivery cost, fixed costs, marginal cost per unit
- **Target market**: B2B or B2C? Enterprise or SMB? Price-sensitive or value-driven?
- **Competitor pricing**: What do alternatives cost? (or use competitor-analysis output)
- **Current pricing** (if any): What are you charging now? What's working/not working?

### Step 2: Analyze Pricing Models

Evaluate each model against the product type:

| Model | Best For | Pros | Cons |
|-------|----------|------|------|
| **One-time purchase** | Physical goods, digital downloads, lifetime tools | Simple, high perceived value | No recurring revenue, hard to upsell |
| **Subscription (flat)** | SaaS, media, memberships | Predictable revenue, high LTV | Churn risk, feature bloat pressure |
| **Tiered subscription** | SaaS, services with scaling needs | Captures multiple segments, natural upsell | Complexity, tier confusion |
| **Freemium** | SaaS with network effects, tools | Low barrier, viral growth | Low conversion (2-5%), support cost |
| **Usage-based** | APIs, infrastructure, consumables | Fair perceived pricing, scales with value | Unpredictable revenue, bill shock |
| **Per-seat** | B2B collaboration tools | Scales with customer size | Seat-sharing workarounds, growth penalty |
| **One-time + subscription** | Courses with community, hardware + service | High initial revenue + recurring | Complex messaging |

Recommend the top 1-2 models with justification for this specific product.

### Step 3: Design Tier Structure

If tiered pricing is recommended, design 3 tiers (or recommend against tiers with rationale):

| | Starter | Professional | Enterprise |
|---|---------|-------------|------------|
| **Price** | $X/mo | $X/mo | Custom |
| **Target** | [who] | [who] | [who] |
| **Feature 1** | ✅ | ✅ | ✅ |
| **Feature 2** | ❌ | ✅ | ✅ |
| **Feature 3** | ❌ | ❌ | ✅ |
| **Limits** | [cap] | [cap] | Unlimited |
| **Support** | Email | Priority | Dedicated |

**Feature gating principles:**
- Gate by **volume/scale**, not by crippling the product
- Each tier should feel complete for its target user
- Middle tier should be the obvious "best value" (most popular tag)
- Enterprise tier exists to anchor high value (and for actual enterprise)

### Step 4: Apply Pricing Psychology

Recommend applicable techniques:

**Anchor pricing (decoy effect):**
- Add a tier that makes the target tier look like better value
- Example: $9 / **$29** / $49 — the $49 tier makes $29 feel like a deal

**Charm pricing:**
- Use .99 or .97 endings for consumer products ($29.99 not $30)
- Use round numbers for premium/B2B ($500 not $499 — signals confidence)

**Price framing:**
- Annual billing: Show monthly equivalent ("Just $24/mo billed annually")
- Daily framing: "Less than $1/day" for monthly subscriptions
- ROI framing: "Saves 10 hours/month — that's $X at your hourly rate"

**Comparison anchoring:**
- Compare to alternatives: "vs $200/hr consultant"
- Compare to cost of problem: "vs $X,000 lost to [problem] per year"

### Step 5: Calculate Minimum Viable Price

Determine the floor price:

```
Fixed costs (monthly)        = $______
Variable cost per unit       = $______
Target margin                = ____%
Break-even volume            = ______ units
Minimum price per unit       = $______ (covers costs + margin)

Sanity check:
  Market rate range          = $______ – $______
  Your floor price           = $______
  Recommended price          = $______ (aim for top 30% of market)
```

### Step 6: A/B Test Plan for Pricing

Recommend a testing approach:
- **What to test**: Price point, tier names, feature gating, annual vs monthly default
- **How to test**: Split traffic 50/50, minimum 2-week test, track conversion rate AND revenue (not just signups)
- **Caution**: Never show different prices to same user — use cohorts, time-based splits, or geographic segments
- **Metrics**: Conversion rate, revenue per visitor, LTV of each cohort
- **Sequence**: Test price point first → then tier structure → then psychology elements

### Step 7: Output

Present the complete pricing strategy:

```
━━━ PRICING STRATEGY: [Product Name] ━━━━━━━

── RECOMMENDED MODEL ──────────────────────
Model: [name]
Rationale: [why this model fits]

── TIER STRUCTURE ─────────────────────────
[pricing table]

── PSYCHOLOGY APPLIED ─────────────────────
Anchor: [technique + example]
Framing: [technique + example]
Charm: [pricing format chosen]

── MINIMUM VIABLE PRICE ───────────────────
Floor: $[amount]
Recommended: $[amount]
Market range: $[low] – $[high]

── REVENUE PROJECTIONS ────────────────────
| Scenario | Conv Rate | Volume | Monthly Rev |
|----------|-----------|--------|-------------|
| Conservative | X% | N | $X,XXX |
| Moderate | X% | N | $X,XXX |
| Optimistic | X% | N | $X,XXX |

── A/B TEST PLAN ──────────────────────────
Test 1: [what to test + method]
Test 2: [what to test + method]
```

## Inputs
- Product type and description
- Cost structure (fixed + variable)
- Target market characteristics
- Competitor pricing (or competitor-analysis output)
- Current pricing (if exists)

## Outputs
- Pricing model recommendation with justification
- Tier structure with feature gating (if tiered)
- Pricing psychology techniques applied
- Minimum viable price calculation
- Revenue projections at 3 conversion scenarios
- A/B test plan for pricing validation

## Level History

- **Lv.1** — Base: 7-model pricing analysis, tier structure design with feature gating, pricing psychology toolkit (anchoring, charm, framing), minimum viable price calculation, revenue projections, A/B test plan for price validation. (Origin: MemStack v3.2, Mar 2026)
