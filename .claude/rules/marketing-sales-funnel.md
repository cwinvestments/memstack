---
name: sales-funnel
description: "Use when the user says 'sales funnel', 'funnel', 'conversion funnel', 'customer journey', 'funnel strategy', or wants to map awareness-to-retention flow for a product."
---


# 🔄 Sales Funnel — Full-Funnel Conversion Architecture
*Map the complete customer journey from stranger to repeat buyer with copy hooks and conversion targets.*

## Activation

When this skill activates, output:

`🔄 Sales Funnel — Mapping your conversion architecture...`

| Context | Status |
|---------|--------|
| **User says "sales funnel", "funnel", "conversion funnel"** | ACTIVE |
| **User wants to map customer journey stages** | ACTIVE |
| **User asks about lead magnets or tripwires in funnel context** | ACTIVE |
| **User is writing ad copy (not funnel structure)** | DORMANT — see facebook-ad or google-ad |
| **User is planning a launch (not funnel design)** | DORMANT — see launch-plan |

## Protocol

### Step 1: Gather Inputs

Ask the user for:
- **Product/service**: What are you selling?
- **Price point**: What does it cost? (or price range for tiered)
- **Target audience**: Who is the ideal buyer? Demographics, psychographics
- **Primary traffic source**: Where do visitors come from? (organic, paid, social, referral)

### Step 2: Map the Full Funnel

Build a 5-stage funnel with specific definitions:

| Stage | Goal | Content Type | CTA | Key Metric |
|-------|------|-------------|-----|------------|
| **Awareness** | Attract strangers | Blog posts, social content, SEO, ads | Click / Follow | Impressions, reach, CTR |
| **Interest** | Capture attention | Lead magnet, free resource, webinar | Opt-in / Subscribe | Opt-in rate (target: 25-40%) |
| **Consideration** | Build trust | Email nurture, case studies, demos | Book call / Try free | Email open rate, demo requests |
| **Conversion** | Close the sale | Sales page, checkout, 1:1 call | Buy now | Conversion rate (target: 1-5%) |
| **Retention** | Keep & expand | Onboarding, support, loyalty program | Refer / Upgrade | LTV, churn rate, NPS |

### Step 3: Design Lead Magnet (Top of Funnel)

Recommend a lead magnet based on audience and product type:
- **B2B / High-ticket**: Free assessment, ROI calculator, industry report
- **B2C / E-commerce**: Discount code, style guide, quiz
- **SaaS**: Free trial, template library, mini-course
- **Info products**: Cheat sheet, checklist, sample chapter

Include: title, format, estimated creation time, opt-in page headline.

### Step 4: Design Tripwire Offer (Middle of Funnel)

Create a low-cost offer ($7-$47) that converts leads into buyers:
- Must deliver immediate, tangible value
- Must be related to the core offer
- Purpose: break the "non-buyer" psychological barrier
- Examples: mini-course, template pack, tool access, quick-win guide

Include: tripwire name, price, what's included, bridge to core offer.

### Step 5: Core Offer Positioning

Position the main product with:
- **Value proposition**: One sentence — what they get and why it matters
- **3 key benefits**: Outcome-focused, not feature-focused
- **Objection handling**: Top 3 objections with responses
  - Price objection → ROI framing or payment plan
  - Trust objection → Social proof, guarantee, case study
  - Timing objection → Cost of delay, urgency element
- **Guarantee**: Risk-reversal offer (30-day, results-based, etc.)

### Step 6: Post-Purchase Strategy

Design retention and expansion:
- **Immediate**: Thank you page with upsell offer (bump or OTO)
- **Week 1**: Onboarding sequence — help them get first win
- **Week 2-4**: Cross-sell complementary product
- **Month 2+**: Referral program, loyalty rewards, case study request
- **Ongoing**: Re-engagement campaigns for inactive customers

### Step 7: Output Funnel Diagram

Present the complete funnel as a structured diagram:

```
AWARENESS  ──→  [Traffic Source]
    │           Content: ___________
    │           CTA: _______________
    │           Target: ____________ visitors/mo
    ▼
INTEREST   ──→  [Lead Magnet: ___________]
    │           Opt-in rate: ____%
    │           Target: ____________ leads/mo
    ▼
CONSIDER   ──→  [Tripwire: $___ ___________]
    │           Conversion: ____%
    │           Nurture: ___ emails over ___ days
    ▼
CONVERT    ──→  [Core Offer: $___ ___________]
    │           Conversion: ____%
    │           Revenue target: $______/mo
    ▼
RETAIN     ──→  [Upsell: ___________]
                Upsell rate: ____%
                LTV target: $______
```

Include copy hooks (headline/angle) for each stage transition.

## Inputs
- Product name and description
- Price point(s)
- Target audience profile
- Primary traffic source

## Outputs
- 5-stage funnel map with content, CTAs, and metrics per stage
- Lead magnet recommendation with opt-in copy
- Tripwire offer design
- Core offer positioning with objection handling
- Post-purchase upsell/cross-sell strategy
- Visual funnel diagram with conversion targets

## Level History

- **Lv.1** — Base: 5-stage funnel architecture (awareness → retention), lead magnet selection matrix, tripwire design, core offer positioning with objection handling, post-purchase expansion strategy, funnel diagram template with conversion targets. (Origin: MemStack v3.2, Mar 2026)
