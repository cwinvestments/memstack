---
name: lead-magnet
description: "Use when the user says 'lead magnet', 'opt-in', 'freebie', 'email list', 'list building', 'opt-in page', or wants to create a free resource to capture email subscribers."
---


# 🧲 Lead Magnet — Opt-In Asset & Delivery System
*Design a high-converting lead magnet with landing page copy, delivery emails, and nurture sequence.*

## Activation

When this skill activates, output:

`🧲 Lead Magnet — Designing your lead capture system...`

| Context | Status |
|---------|--------|
| **User says "lead magnet", "opt-in", "freebie", "list building"** | ACTIVE |
| **User wants to grow their email list** | ACTIVE |
| **User wants landing page copy for a free resource** | ACTIVE |
| **User wants the full funnel (not just lead magnet)** | DORMANT — see sales-funnel |
| **User wants paid ad copy to promote the lead magnet** | DORMANT — see facebook-ad or google-ad |

## Protocol

### Step 1: Gather Inputs

Ask the user for:
- **Niche/industry**: What space are you in?
- **Audience pain points**: Top 3 problems your audience faces
- **Existing content**: Do you have blog posts, videos, or tools to repurpose?
- **Core offer**: What paid product does the lead magnet lead toward?
- **Email platform**: ConvertKit, Mailchimp, SendGrid, Beehiiv, or other?

### Step 2: Suggest 5 Lead Magnet Concepts

Generate 5 options across different formats:

| # | Type | Concept | Est. Opt-in Rate | Effort |
|---|------|---------|-------------------|--------|
| 1 | **Checklist** | [specific checklist title] | 30-40% | Low |
| 2 | **Template** | [specific template title] | 25-35% | Low-Med |
| 3 | **Mini-course** | [specific course title, 3-5 emails] | 20-30% | Medium |
| 4 | **Tool/Calculator** | [specific tool description] | 35-50% | High |
| 5 | **Report/Guide** | [specific report title] | 15-25% | Medium |

Recommend the top pick based on audience, effort, and conversion potential.

### Step 3: Design the Top Pick

For the recommended lead magnet:

**Content Outline:**
- Title (specific, outcome-focused)
- Subtitle (what they'll achieve)
- Format and length (PDF pages, email count, tool type)
- Section-by-section outline (3-7 sections)
- Key takeaway per section
- Estimated creation time

**Design Direction:**
- Color palette suggestion (match brand or niche standard)
- Layout type (single-column, card-based, worksheet)
- Include: cover image, branded header, footer CTA

### Step 4: Write Opt-In Page Copy

**Headline** (8-12 words):
- Formula: [Get/Download/Grab] + [Specific Outcome] + [Timeframe/Ease]
- Example: "Download the 7-Step Checklist That Doubles Your Close Rate"

**Subheadline** (15-20 words):
- Expand on the promise, address skepticism
- Example: "Used by 500+ sales teams to increase revenue without cold calling"

**Bullet points** (3-5):
- Each starts with a benefit verb: Discover, Learn, Get, Unlock, Master
- Each promises a specific outcome

**Social proof** (if available):
- Subscriber count, testimonial quote, or credibility marker

**CTA button text**:
- Not "Submit" — use action words: "Send Me the Checklist", "Get Instant Access", "Yes, I Want This"

**Form fields**:
- Minimum viable: Email only (highest conversion)
- If segmentation needed: Email + First Name
- Never ask for more than necessary

### Step 5: Design Delivery Sequence

**Thank You Page (immediately after opt-in):**
- Confirm delivery ("Check your inbox!")
- Set expectations for what's coming next
- Optional: tripwire offer or low-cost upsell ($7-$27)

**Email 1 — Delivery (immediate):**
- Subject: "Here's your [Lead Magnet Name]"
- Body: Download link, quick-start tip, expectation for next emails
- PS: One-line about who you are and why you help

**Email 2 — Quick Win (Day 2):**
- Subject: "Do this first with your [Lead Magnet Name]"
- Body: Most impactful action they can take right now
- Build credibility through helpfulness

**Email 3 — Story/Proof (Day 4):**
- Subject: "How [Name] used this to [Result]"
- Body: Case study or personal story showing results
- Soft bridge toward core offer

**Email 4 — Bridge (Day 6):**
- Subject: "The next step after [Lead Magnet topic]"
- Body: Identify the gap between lead magnet and full transformation
- Introduce core offer as the bridge

**Email 5 — Offer (Day 8):**
- Subject: "Ready for [Full Outcome]?"
- Body: Full offer presentation with link
- Include FAQ or objection handling

### Step 6: Integration Guidance

Platform-specific setup for the top 3 email providers:

**ConvertKit:**
- Create Form → Connect to Sequence → Tag subscribers
- Automation: Form submit → Deliver email → Wait → Nurture sequence

**Mailchimp:**
- Create Landing Page → Connect to Automation → Add tags
- Automation: Subscriber joins list → Welcome series → Tag based on engagement

**SendGrid / Beehiiv:**
- Webhook setup for form submission
- API integration pattern for custom landing pages
- Drip sequence configuration

### Step 7: Metrics & Benchmarks

Expected performance benchmarks by lead magnet type:

| Metric | Checklist | Template | Mini-Course | Tool | Report |
|--------|-----------|----------|-------------|------|--------|
| Opt-in rate | 30-40% | 25-35% | 20-30% | 35-50% | 15-25% |
| Email open rate | 60-70% | 55-65% | 70-80% | 50-60% | 50-60% |
| Nurture-to-sale | 3-5% | 3-5% | 5-8% | 2-4% | 2-4% |

Track: opt-in rate, delivery email open rate, click rate, unsubscribe rate after sequence.

### Step 8: Output

Present the complete lead magnet specification:

```
━━━ LEAD MAGNET SPEC: [Title] ━━━━━━━━━━━━━

── CONCEPT ────────────────────────────────
Type: [checklist/template/etc.]
Title: [name]
Format: [PDF/email/tool]
Length: [pages/emails/etc.]
Creation time: [estimate]

── CONTENT OUTLINE ────────────────────────
1. [Section] — [key takeaway]
2. [Section] — [key takeaway]
...

── OPT-IN PAGE ────────────────────────────
Headline: [text]
Subheadline: [text]
Bullets:
  • [benefit 1]
  • [benefit 2]
  • [benefit 3]
CTA: [button text]

── DELIVERY SEQUENCE ──────────────────────
Email 1 (Day 0): [subject] — Deliver asset
Email 2 (Day 2): [subject] — Quick win
Email 3 (Day 4): [subject] — Story/proof
Email 4 (Day 6): [subject] — Bridge
Email 5 (Day 8): [subject] — Offer

── INTEGRATION ────────────────────────────
Platform: [name]
Setup: [key steps]

── BENCHMARKS ─────────────────────────────
Target opt-in rate: X%
Target open rate: X%
Target nurture-to-sale: X%
```

## Inputs
- Niche/industry
- Audience pain points (top 3)
- Existing content inventory
- Core paid offer
- Email platform

## Outputs
- 5 lead magnet concepts ranked by conversion potential and effort
- Detailed content outline for top pick
- Opt-in page copy (headline, subheadline, bullets, CTA)
- 5-email delivery and nurture sequence
- Email platform integration guidance
- Performance benchmarks by lead magnet type

## Level History

- **Lv.1** — Base: 5-concept suggestion matrix, opt-in page copywriting framework, 5-email delivery/nurture sequence, platform integration guidance (ConvertKit, Mailchimp, SendGrid), performance benchmarks by lead magnet type. (Origin: MemStack v3.2, Mar 2026)
