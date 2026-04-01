---
name: memstack-marketing-sales-funnel
description: "Use this skill when the user says 'sales funnel', 'funnel', 'conversion funnel', 'customer journey', or wants to map the complete customer journey from stranger to repeat buyer with copy hooks and conversion targets. Do NOT use for ad copy creation or time-bound launch plans."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# Sales Funnel — Mapping customer journey from stranger to buyer...
*Maps the complete customer journey across TOFU/MOFU/BOFU stages with page templates, copy hooks, conversion targets, and optimization checklist.*

## Activation

When this skill activates, output:

`Sales Funnel — Mapping customer journey from stranger to buyer...`

Then execute the protocol below.

## Context Guard

| Context | Status |
|---------|--------|
| User says "sales funnel", "funnel", "conversion funnel" | ACTIVE |
| User says "customer journey" or "buyer journey" | ACTIVE |
| User wants to map awareness → conversion → retention flow | ACTIVE |
| User wants ad copy only (no funnel structure) | DORMANT — use Facebook Ad or Google Ad |
| User wants a time-bound launch plan | DORMANT — use Launch Plan |

## Common Mistakes

| Mistake | Why It's Wrong |
|---------|---------------|
| "Start with a sales page" | Strangers don't buy. Build awareness and trust first, then pitch. |
| "One funnel fits all" | B2B, B2C, SaaS, and e-commerce funnels have fundamentally different structures. |
| "Skip the nurture stage" | MOFU is where trust is built. Jumping from ad to checkout kills conversion. |
| "Optimize before traffic" | You need 1,000+ visitors per stage before conversion data is meaningful. |
| "Same message everywhere" | Each stage needs copy matched to the buyer's awareness level. |

## Protocol

### Step 1: Gather Funnel Requirements

If the user hasn't provided details, ask:

> 1. **Product/service** — what are you selling? (price point, delivery model)
> 2. **Business model** — B2B SaaS, B2C e-commerce, info product, service business?
> 3. **Target audience** — who is the ideal buyer? (demographics, pain points)
> 4. **Current state** — do you have existing traffic, email list, or social following?
> 5. **Primary goal** — lead generation, direct sales, subscription, or booking calls?

### Step 2: Define Funnel Type

Select the funnel architecture based on business model:

| Model | Funnel Type | Key Stages |
|-------|------------|------------|
| **B2C E-commerce** | Product Funnel | Ad → Product Page → Cart → Checkout → Upsell → Follow-up |
| **B2B SaaS** | Free Trial Funnel | Content → Lead Magnet → Email Nurture → Free Trial → Onboarding → Paid |
| **Info Products** | Webinar Funnel | Ad → Registration → Webinar → Offer → Checkout → Delivery |
| **Service Business** | Consultation Funnel | Content → Lead Magnet → Case Study → Application → Call → Close |
| **Subscription** | Value Ladder | Free Content → Low-Ticket → Core Offer → Premium → VIP |

### Step 3: Map TOFU (Top of Funnel) — Awareness

**Goal:** Attract strangers and create awareness. Conversion target: 2-5% to MOFU.

**Traffic sources:**
- Organic: SEO blog posts, YouTube, social media, podcast appearances
- Paid: Facebook/Instagram ads, Google Search ads, YouTube ads
- Referral: Partnerships, affiliates, guest posting

**TOFU page template:**

```
[TOFU Landing Page]
├── Headline: Address the #1 pain point (problem-aware hook)
├── Subheadline: Promise a specific outcome
├── Social proof: "Join 10,000+ [audience type]"
├── Lead magnet offer: Free [resource] that solves an immediate problem
├── Email capture form: Name + Email (minimal friction)
├── Trust signals: Logos, testimonials, media mentions
└── Exit intent popup: Alternative offer or discount
```

**Copy formula — Problem-Agitation-Solution (PAS):**
1. **Problem:** "Struggling with [pain point]?"
2. **Agitation:** "Every day you wait, [consequence gets worse]"
3. **Solution:** "Download our free [resource] to [specific outcome]"

**KPIs:** Traffic volume, email opt-in rate (target: 25-40% on dedicated landing pages), cost per lead

### Step 4: Map MOFU (Middle of Funnel) — Consideration

**Goal:** Nurture leads and build trust. Conversion target: 5-15% to BOFU.

**Nurture sequence:**
1. **Email 1 (Day 0):** Deliver lead magnet + quick win
2. **Email 2 (Day 2):** Share a relevant story/case study
3. **Email 3 (Day 4):** Teach a framework (demonstrate expertise)
4. **Email 4 (Day 7):** Address top objection with proof
5. **Email 5 (Day 10):** Soft pitch — introduce the solution

**MOFU content types:**
- Case studies with specific results ("How [Customer] achieved [Result] in [Timeframe]")
- Comparison guides (your solution vs. alternatives)
- Free workshops or mini-courses
- Behind-the-scenes content (builds authenticity)

**MOFU page template:**

```
[Case Study / Social Proof Page]
├── Headline: "[Customer] achieved [specific result]"
├── Before state: The problem they faced
├── Journey: What they tried, why it failed
├── Solution: How your product/service helped
├── Results: Specific metrics (revenue, time saved, growth)
├── Testimonial quote: In their own words
├── CTA: "Ready for similar results? [Next step]"
└── Objection handler: FAQ section addressing top 3-5 concerns
```

**KPIs:** Email open rate (target: 30%+), click-through rate (target: 3-5%), content engagement time

### Step 5: Map BOFU (Bottom of Funnel) — Decision

**Goal:** Convert qualified leads into buyers. Conversion target: 2-10% depending on price point.

**BOFU page template — Sales Page:**

```
[Sales Page Structure]
├── Hero: Headline + subheadline + hero image/video
├── Problem: 3 pain points the audience recognizes
├── Agitation: Cost of inaction (emotional + financial)
├── Solution: Introduce your offer as the bridge
├── Benefits: 5-7 outcome-focused bullet points
├── Features: What's included (with benefit framing)
├── Social proof: 3-5 testimonials, case study snippets
├── Pricing: Tier structure or single offer with value stack
├── Value stack: List everything included with "value" prices
├── Guarantee: Risk reversal (money-back, free trial, etc.)
├── FAQ: Top 5-7 objections answered
├── Urgency: Deadline, limited spots, or bonus expiration
├── Final CTA: Clear action button with benefit-driven text
└── P.S.: Restate the key benefit and deadline
```

**Pricing psychology triggers:**
- Anchoring: Show the "full value" before the actual price
- Decoy: Include a middle tier that makes the top tier look like a deal
- Urgency: "Offer expires [date]" or "Only [X] spots remaining"
- Risk reversal: "30-day money-back guarantee — no questions asked"

**KPIs:** Sales page conversion rate, average order value, cart abandonment rate (target: <70%)

### Step 6: Map Post-Purchase — Retention & Expansion

**Goal:** Maximize lifetime value and generate referrals.

**Post-purchase sequence:**
1. **Immediate:** Order confirmation + onboarding guide
2. **Day 1:** Welcome email + how to get started
3. **Day 3:** Quick win tutorial (ensure first success)
4. **Day 7:** Check-in + ask for feedback
5. **Day 14:** Upsell/cross-sell related product
6. **Day 30:** Request testimonial or review
7. **Day 60:** Referral program invitation

**Retention strategies:**
- Upsell: Higher-tier version of what they bought
- Cross-sell: Complementary product or service
- Referral: "Give $20, get $20" program
- Community: Private group or membership access

**KPIs:** Customer lifetime value (LTV), repeat purchase rate, Net Promoter Score (NPS), referral rate

### Step 7: Build Conversion Optimization Checklist

For each funnel stage, verify:

**TOFU checklist:**
- [ ] Landing page loads in <3 seconds
- [ ] One clear CTA above the fold
- [ ] Lead magnet solves an immediate, specific problem
- [ ] Form asks for minimum info (name + email only)
- [ ] Mobile-responsive design
- [ ] Tracking pixels installed (Meta, Google, analytics)

**MOFU checklist:**
- [ ] Email sequence delivers value before pitching
- [ ] Case studies include specific, measurable results
- [ ] Objections addressed before the sales page
- [ ] Re-engagement flow for inactive leads (30+ days)
- [ ] Segmentation based on engagement level

**BOFU checklist:**
- [ ] Sales page has above-the-fold CTA
- [ ] Price anchoring with value stack
- [ ] Risk reversal guarantee prominently displayed
- [ ] Checkout is 1-2 steps maximum
- [ ] Abandoned cart email sequence (3 emails over 72 hours)
- [ ] Order bump or upsell on checkout page

**Post-purchase checklist:**
- [ ] Onboarding email sends within 5 minutes
- [ ] First-use tutorial included
- [ ] Review/testimonial request at day 14-30
- [ ] Upsell offer at day 14-30
- [ ] Referral program active

## Output Format

Deliver the complete funnel as a structured document:

```markdown
# [Product/Service] — Sales Funnel Architecture

## Funnel Overview
- **Type:** [Funnel type from Step 2]
- **Target audience:** [Description]
- **Price point:** [Amount]
- **Estimated funnel conversion:** [X]% end-to-end

## Stage 1: TOFU — Awareness
**Traffic sources:** [List]
**Lead magnet:** [Description]
**Landing page headline:** "[Headline]"
**Target conversion:** [X]% opt-in rate

## Stage 2: MOFU — Consideration
**Nurture sequence:** [5-email summary]
**Key content pieces:** [List]
**Target conversion:** [X]% to BOFU

## Stage 3: BOFU — Decision
**Sales page headline:** "[Headline]"
**Value stack:** [List of inclusions with values]
**Guarantee:** [Risk reversal offer]
**Target conversion:** [X]% purchase rate

## Stage 4: Post-Purchase — Retention
**Onboarding sequence:** [Summary]
**Upsell offer:** [Description]
**Referral mechanism:** [Description]

## Conversion Optimization Checklist
[Completed checklist from Step 7]

## Tech Stack Recommendations
[Email platform, landing page builder, payment processor, analytics]
```

## Completion

```
Sales Funnel — Complete!

Funnel type: [Type]
Stages mapped: 4 (TOFU → MOFU → BOFU → Retention)
Pages needed: [Count]
Email sequences: [Count] ([total emails] emails)
Estimated end-to-end conversion: [X]%

Next steps:
1. Build landing pages using the templates above
2. Write email sequences (use Email Sequence skill)
3. Set up tracking pixels and analytics
4. Drive initial traffic (minimum 1,000 visitors) before optimizing
5. Review conversion data weekly and A/B test underperforming stages
```

## Level History

- **Lv.1** — Base: TOFU/MOFU/BOFU architecture, funnel type selection by business model, page templates per stage, copy formulas (PAS), nurture sequence structure, pricing psychology triggers, post-purchase retention flow, conversion optimization checklist, tech stack recommendations, KPIs per stage. (Origin: MemStack Pro v3.2, Mar 2026)
