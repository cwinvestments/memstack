---
name: memstack-marketing-pricing-strategy
description: "Use this skill when the user says 'pricing strategy', 'how to price', 'pricing model', 'tier structure', 'pricing psychology', or needs to design pricing tiers, apply pricing psychology, and plan A/B price tests. Do NOT use for competitor pricing comparison alone."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# Pricing Strategy — Designing pricing model...
*Designs pricing tiers using cost-plus, value-based, and competitor-based models with psychology triggers, tier structure templates, and A/B test plans.*

## Activation

When this skill activates, output:

`Pricing Strategy — Designing pricing model...`

Then execute the protocol below.

## Context Guard

| Context | Status |
|---------|--------|
| User says "pricing strategy", "how to price", "pricing model" | ACTIVE |
| User says "tier structure" or "pricing psychology" | ACTIVE |
| User wants to design or redesign their pricing | ACTIVE |
| User wants competitor pricing comparison only | DORMANT — use Competitor Analysis |
| User wants to create an invoice | DORMANT — use Invoice Generator |

## Common Mistakes

| Mistake | Why It's Wrong |
|---------|---------------|
| "Price based on what it costs to make" | Customers pay for outcomes, not your expenses. Cost-plus leaves money on the table. |
| "Match the cheapest competitor" | Racing to the bottom kills margins. Differentiate on value, not price. |
| "Three tiers is always right" | Some products need 2 (simple choice), some need 4 (enterprise). Match tiers to buyer segments. |
| "Never raise prices" | Grandfathering old prices forever means your best customers pay the least. Raise annually. |
| "Free tier for everyone" | Free tiers attract non-buyers. Only use freemium if free users create viral growth. |

## Protocol

### Step 1: Gather Pricing Requirements

If the user hasn't provided details, ask:

> 1. **Product/service** — what are you pricing? (SaaS, physical product, service, course)
> 2. **Costs** — what does it cost to deliver? (COGS, hosting, labor)
> 3. **Target customer** — freelancer, SMB, mid-market, or enterprise?
> 4. **Current pricing** — is this a new product or a re-pricing?
> 5. **Competitors** — what do alternatives cost?
> 6. **Value delivered** — what outcome or ROI does the customer get?

### Step 2: Select Pricing Model

| Model | Best For | How It Works |
|-------|---------|-------------|
| **Cost-plus** | Physical products, commodities | Cost × markup (e.g., 2.5x) |
| **Value-based** | SaaS, consulting, info products | Price = fraction of value delivered to customer |
| **Competitor-based** | Crowded markets with clear benchmarks | Position relative to market (below, at, or above) |
| **Usage-based** | API, infrastructure, metered services | Pay per unit (API call, GB stored, seat) |
| **Freemium** | PLG (product-led growth) SaaS | Free core + paid premium features |
| **Flat rate** | Simple products with one buyer type | One price, everything included |

**Decision framework:**

```
Can you quantify the ROI your product delivers?
├── Yes → Value-based pricing (capture 10-20% of customer's ROI)
└── No
    ├── Is the market well-established with clear price benchmarks?
    │   ├── Yes → Competitor-based (position strategically)
    │   └── No → Cost-plus (ensure margins, then test market willingness)
    └── Does usage vary dramatically between customers?
        └── Yes → Usage-based or hybrid (base + usage)
```

### Step 3: Calculate Price Anchors

**Cost-plus calculation:**
```
Direct cost per unit: $[X]
Overhead allocation: $[X]
Total cost: $[X]
Target margin: [X]%
Price = Total cost ÷ (1 - margin%)
Example: $40 cost ÷ (1 - 0.70) = $133 price (70% margin)
```

**Value-based calculation:**
```
Customer's problem cost (annual): $[X]
Your product saves them: $[X]/year
Value capture rate: 10-20%
Price = Annual savings × capture rate
Example: $50,000 saved × 15% = $7,500/year ($625/mo)
```

**Competitor-based positioning:**
```
Cheapest competitor: $[X]/mo
Average competitor: $[X]/mo
Premium competitor: $[X]/mo

Your position:
- Below average → justify with "same features, lower price"
- At average → justify with "better UX/support/speed"
- Above average → justify with "more value/features/outcomes"
```

### Step 4: Design Tier Structure

**3-tier template (most common):**

| | Starter | Professional | Enterprise |
|---|---|---|---|
| **Target buyer** | Freelancers, individuals | Small teams, SMBs | Large teams, companies |
| **Price** | $[X]/mo | $[X]/mo | Custom |
| **Billing** | Monthly or annual | Annual (15-20% discount) | Annual contract |
| **Seats/usage** | 1 user / [limit] | Up to [X] users / [limit] | Unlimited |
| **Feature 1** | Basic | Full | Full |
| **Feature 2** | — | Full | Full |
| **Feature 3** | — | — | Full |
| **Support** | Email | Priority email | Dedicated CSM |
| **SLA** | — | — | 99.9% uptime |

**Tier design rules:**
1. **Starter** must be useful on its own (not crippled). It proves value and creates habit.
2. **Professional** is the target tier — design the page to highlight it ("Most Popular").
3. **Enterprise** exists for price anchoring even if you have few enterprise buyers.
4. Each tier should have 1-2 clear upgrade triggers (the feature you hit a wall without).

**Naming conventions:**

| Tone | Tier 1 | Tier 2 | Tier 3 |
|------|--------|--------|--------|
| Professional | Starter | Professional | Enterprise |
| Friendly | Free | Pro | Business |
| Creative | Solo | Team | Scale |
| Simple | Basic | Plus | Premium |

### Step 5: Apply Pricing Psychology

| Trigger | Implementation | Why It Works |
|---------|---------------|-------------|
| **Anchoring** | Show the highest price first (or "value" price before actual price) | First number seen sets the reference point |
| **Decoy effect** | Make the middle tier the obvious best deal (closest to top tier, much cheaper) | The "bad deal" tier makes the target tier look irresistible |
| **Charm pricing** | $97, $197, $497 instead of $100, $200, $500 | Left-digit effect: $97 feels closer to $90 than $100 |
| **Annual discount** | "Save 20% with annual billing" — show monthly equivalent | Increases LTV, reduces churn, feels like a deal |
| **Price framing** | "$8/day" instead of "$249/month" | Smaller daily number is easier to justify |
| **Loss aversion** | "You're losing $X/month without this" instead of "Save $X/month" | Pain of loss is 2x stronger than joy of gain |
| **Social proof at price** | "Join 5,000+ teams on Pro" next to the tier | Reduces purchase anxiety at the moment of decision |
| **Risk reversal** | 30-day money-back guarantee prominently displayed | Removes fear of making the wrong choice |
| **Urgency** | "Launch price — increases to $[higher] on [date]" | Deadline accelerates decisions |

**Pricing page layout (top to bottom):**
1. Headline: Value proposition (not "Pricing")
2. Billing toggle: Monthly / Annual (annual pre-selected)
3. Tier cards: 3 side-by-side, middle highlighted
4. Feature comparison table: Detailed breakdown below cards
5. FAQ: Address top 5 pricing objections
6. Social proof: Customer logos or testimonial
7. CTA: Repeat the primary tier's button

### Step 6: Plan A/B Price Tests

**What to test (priority order):**

| Priority | Test | Expected Impact |
|----------|------|----------------|
| 1 | Price point ($97 vs $127 vs $147) | High — directly affects revenue and conversion |
| 2 | Annual vs monthly default | Medium — affects LTV and churn |
| 3 | Tier naming and positioning | Medium — affects which tier people choose |
| 4 | Feature bundling across tiers | Medium — affects upgrade rate |
| 5 | Guarantee (30-day vs 60-day vs none) | Low-Medium — affects conversion confidence |

**A/B test protocol:**
1. Test ONE variable at a time
2. Split traffic 50/50 (or 70/30 for pricing to limit revenue risk)
3. Minimum sample: 100+ conversions per variation
4. Duration: 2-4 weeks (avoid day-of-week bias)
5. Track: Conversion rate AND revenue per visitor (higher price may convert less but earn more)
6. Winner metric: Revenue per visitor (not just conversion rate)

**Price sensitivity survey (Van Westendorp):**
Ask 50-100 target customers these four questions:
1. At what price would this be **too expensive** to consider?
2. At what price would this be **expensive but worth considering**?
3. At what price would this be a **great deal**?
4. At what price would this be **so cheap** you'd question quality?

Plot the four curves — the intersection defines your acceptable price range.

### Step 7: Build Pricing Migration Plan (Re-pricing)

If changing existing prices:

| Scenario | Approach |
|----------|---------|
| **Price increase (existing customers)** | Grandfather for 6-12 months, then migrate with 60-day notice |
| **Price increase (new customers only)** | Update pricing page immediately, existing stay on old plan |
| **Adding a new tier** | Launch the new tier, don't change existing tiers |
| **Removing a tier** | Migrate users to nearest tier, give 90-day notice |
| **Switching pricing model** | Run both models in parallel for 3-6 months |

**Price increase email template:**

```
Subject: Changes to your [Product] plan

Hi [Name],

We're updating our pricing on [date] to reflect [reason: new features, rising costs, improved value].

What's changing:
- [Plan] moves from $[old] to $[new]/month

What you get:
- [New feature/improvement 1]
- [New feature/improvement 2]

Your plan won't change until [date — 60+ days out].

If you have questions, reply to this email — I read every response.

[Name]
```

## Output Format

```markdown
# Pricing Strategy — [Product Name]

## Pricing Model
- **Model:** [Value-based / Competitor-based / etc.]
- **Rationale:** [Why this model fits]

## Price Calculation
[Show the math — cost basis, value calculation, or competitor benchmarks]

## Tier Structure
[3-column tier comparison table]

## Pricing Page Layout
[Section-by-section wireframe description]

## Psychology Triggers Applied
[List of triggers used with implementation details]

## A/B Test Plan
[Priority-ordered test queue with metrics and duration]

## Migration Plan (if re-pricing)
[Timeline and communication plan]
```

## Completion

```
Pricing Strategy — Complete!

Pricing model: [Model]
Tiers: [Count] ([names])
Recommended price range: $[low] — $[high]/mo
Psychology triggers: [Count] applied
A/B tests queued: [Count]

Next steps:
1. Validate with 10+ customer conversations before finalizing
2. Design pricing page using the layout above
3. Run Van Westendorp survey if unsure about price point
4. Launch with the A/B test plan to optimize within 30 days
5. Re-evaluate pricing quarterly
```

## Level History

- **Lv.1** — Base: 6 pricing models with decision framework, cost-plus/value-based/competitor-based calculation methods, 3-tier template with design rules, 9 pricing psychology triggers with implementation, pricing page layout guide, A/B test protocol (priority-ordered with Van Westendorp), price migration plan with email template. (Origin: MemStack Pro v3.2, Mar 2026)
