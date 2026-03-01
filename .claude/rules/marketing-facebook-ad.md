---
name: facebook-ad
description: "Use when the user says 'facebook ad', 'FB ad', 'Meta ad', 'Instagram ad', 'social ad', or wants ad copy for Facebook/Instagram Ads Manager."
---


# 📘 Facebook Ad — Meta Ads Copy & Strategy
*Generate 3 ready-to-load ad variants with targeting, creative direction, and A/B test plan.*

## Activation

When this skill activates, output:

`📘 Facebook Ad — Generating Meta ad variants...`

| Context | Status |
|---------|--------|
| **User says "facebook ad", "FB ad", "Meta ad", "Instagram ad"** | ACTIVE |
| **User wants social media ad copy with targeting** | ACTIVE |
| **User mentions Ads Manager or ad sets** | ACTIVE |
| **User wants Google search ads** | DORMANT — see google-ad |
| **User wants organic social content (not paid)** | DORMANT |

## Protocol

### Step 1: Gather Inputs

Ask the user for:
- **Product/service**: What are you advertising?
- **Target audience**: Age, interests, pain points, demographics
- **Monthly budget**: Total ad spend
- **Campaign objective**: Traffic, leads, conversions, or awareness
- **Landing page URL**: Where does the ad send people? (optional)

### Step 2: Write 3 Ad Variants

Generate three distinct ad approaches:

#### Variant A — Storytelling
Hook with a relatable story or scenario. Structure:
- **Primary text** (above fold, first 125 chars matter most): Open with a story hook that stops the scroll. Continue with the narrative, connect to product, soft CTA.
- **Headline** (40 chars max): Outcome-focused
- **Description**: Supporting detail
- **CTA button**: Learn More / Shop Now / Sign Up

#### Variant B — Problem-Solution
Lead with the pain point. Structure:
- **Primary text**: State the problem bluntly (first 125 chars). Agitate. Present product as solution. Hard CTA.
- **Headline** (40 chars max): Solution-focused
- **Description**: Proof or urgency element
- **CTA button**: Get Offer / Learn More

#### Variant C — Social Proof
Lead with results or testimonials. Structure:
- **Primary text**: Open with a specific result or quote (first 125 chars). Expand with context. Invite them to get similar results.
- **Headline** (40 chars max): Results-focused
- **Description**: Credibility marker
- **CTA button**: See How / Get Started

### Step 3: Audience Targeting

For each variant, recommend:
- **Core targeting**: 3-5 interests, behaviors, or demographics
- **Custom audiences**: Website visitors, email list, video viewers
- **Lookalike audiences**: 1%, 3%, 5% lookalikes from best customers
- **Exclusions**: Who to exclude (existing customers, competitors' employees)
- **Placement recommendation**: Feed, Stories, Reels, or Automatic

### Step 4: Creative Direction

For each variant, describe the visual concept:
- **Format**: Single image, carousel, or video
- **Visual concept**: What the image/video shows, mood, colors
- **Text overlay**: Any on-image text (keep under 20% of image area)
- **Aspect ratios**: 1:1 for feed, 9:16 for Stories/Reels

### Step 5: A/B Test Plan

Recommend testing sequence:
1. **Week 1**: Test creative (same copy, different images/videos) — find winning visual
2. **Week 2**: Test copy (winning creative, different ad variants) — find winning message
3. **Week 3**: Test audience (winning creative + copy, different targeting) — find best audience
4. **Week 4**: Scale winning combination, test new angles

### Step 6: Budget Allocation

Recommend budget split:
- **Testing phase** (first 2 weeks): Equal split across variants, $5-10/day per ad set minimum
- **Scaling phase**: 70% to winning ad set, 30% to new tests
- **Retargeting**: Reserve 20% of total budget for warm audiences
- **Daily vs lifetime**: Recommend daily budget for testing, lifetime for campaigns with end dates

### Step 7: Output

Present all 3 ad sets in a format ready to load into Ads Manager:

```
━━━ AD SET A: STORYTELLING ━━━━━━━━━━━━━━━━━━
Primary Text: [full text]
Headline: [40 chars]
Description: [text]
CTA Button: [button type]
Audience: [targeting details]
Creative: [visual direction]
Placement: [recommended placements]

━━━ AD SET B: PROBLEM-SOLUTION ━━━━━━━━━━━━━━
[same structure]

━━━ AD SET C: SOCIAL PROOF ━━━━━━━━━━━━━━━━━━
[same structure]

━━━ TEST PLAN ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Week 1: [test details]
Week 2: [test details]
Budget: [allocation]
```

## Inputs
- Product/service description
- Target audience profile
- Monthly budget
- Campaign objective
- Landing page URL (optional)

## Outputs
- 3 complete ad variants (storytelling, problem-solution, social proof)
- Audience targeting recommendations per variant
- Creative direction briefs
- 4-week A/B test plan
- Budget allocation strategy

## Level History

- **Lv.1** — Base: 3-variant ad generation (storytelling, problem-solution, social proof), audience targeting with lookalikes, creative direction briefs, A/B test sequence, budget allocation strategy, Ads Manager-ready output format. (Origin: MemStack v3.2, Mar 2026)
