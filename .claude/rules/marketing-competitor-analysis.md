---
name: competitor-analysis
description: "Use when the user says 'competitor analysis', 'competitive analysis', 'compare competitors', 'competitor research', 'market analysis', or wants to understand their competitive landscape."
---


# 🎯 Competitor Analysis — Competitive Intelligence Report
*Analyze competitors' pricing, positioning, features, and weaknesses to find your strategic advantage.*

## Activation

When this skill activates, output:

`🎯 Competitor Analysis — Building your competitive intelligence report...`

| Context | Status |
|---------|--------|
| **User says "competitor analysis", "competitive analysis"** | ACTIVE |
| **User wants to compare their product against competitors** | ACTIVE |
| **User asks about market positioning or competitive gaps** | ACTIVE |
| **User wants to set their own pricing (not compare)** | DORMANT — see pricing-strategy |
| **User wants ad copy targeting competitor audiences** | DORMANT — see facebook-ad or google-ad |

## Protocol

### Step 1: Gather Inputs

Ask the user for:
- **Your product**: What do you sell? Key features, price, positioning
- **Competitor URLs**: 3-5 competitor websites to analyze
- **Your differentiation**: What do you believe makes you different? (optional — skill may identify this)
- **Target market**: Who are you both competing for?

### Step 2: Analyze Each Competitor

For each competitor, extract and assess:

**Company Profile:**
- Company name, URL, estimated size
- Target audience (who they're speaking to)
- Brand positioning (premium, budget, niche, mass-market)
- Unique selling proposition (their main claim)

**Product/Service:**
- Core offering and key features
- Pricing model and price points
- Free tier or trial availability
- Strengths (what they do well)
- Weaknesses (where they fall short)

**Messaging:**
- Homepage headline and main claim
- Proof elements (testimonials, case studies, numbers)
- Tone and voice (professional, casual, technical, aspirational)
- Trust signals (certifications, press mentions, logos)

### Step 3: Feature Comparison Matrix

Build a side-by-side feature matrix:

| Feature | Your Product | Competitor A | Competitor B | Competitor C |
|---------|-------------|-------------|-------------|-------------|
| Feature 1 | ✅ | ✅ | ❌ | ✅ |
| Feature 2 | ✅ | ❌ | ✅ | ❌ |
| Feature 3 | ❌ | ✅ | ✅ | ✅ |
| ... | ... | ... | ... | ... |

Mark features as: ✅ (included), ❌ (missing), ⚡ (best-in-class), 🔜 (planned)

### Step 4: Pricing Comparison

Build a pricing analysis:

| | Your Product | Competitor A | Competitor B | Competitor C |
|---|-------------|-------------|-------------|-------------|
| Lowest tier | $X/mo | $X/mo | $X/mo | $X/mo |
| Mid tier | $X/mo | $X/mo | $X/mo | $X/mo |
| Top tier | $X/mo | $X/mo | $X/mo | $X/mo |
| Free tier | Yes/No | Yes/No | Yes/No | Yes/No |
| Value ratio | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |

**Value-per-dollar analysis**: Which product delivers the most features per dollar at each tier?

### Step 5: Messaging Analysis

For each competitor, document:
- **Primary claim**: What they say on their homepage hero
- **Proof offered**: Testimonials, stats, case studies, logos
- **Emotional angle**: Fear, aspiration, frustration, belonging
- **Gaps in claims**: What they promise vs what reviews say
- **Common review complaints**: What customers actually dislike

### Step 6: Weakness Identification

Identify exploitable gaps:
- **Feature gaps**: Features competitors lack that your audience wants
- **Service gaps**: Support quality, onboarding, documentation
- **Price gaps**: Underserved price point (too expensive or no premium option)
- **Audience gaps**: Segments competitors ignore or serve poorly
- **Messaging gaps**: Claims nobody is making that would resonate

Rank by: impact (high/medium/low) × difficulty to exploit (easy/medium/hard)

### Step 7: SEO Overlap Analysis

Identify content and keyword competitive dynamics:
- **Shared keywords**: Terms you both rank for (or should)
- **Their keywords you miss**: Terms they rank for that you don't
- **Your keyword opportunities**: Terms nobody ranks well for
- **Content gaps**: Topics competitors cover that you don't
- **Content advantages**: Topics you cover better than anyone

### Step 8: Output

Present the complete competitive intelligence report:

```
━━━ COMPETITIVE INTELLIGENCE REPORT ━━━━━━━━

── YOUR POSITIONING ───────────────────────
Product: [name]
USP: [one-line positioning]
Target: [audience]

── COMPETITOR PROFILES ────────────────────
[A]: [name] — [one-line summary]
[B]: [name] — [one-line summary]
[C]: [name] — [one-line summary]

── FEATURE MATRIX ─────────────────────────
[comparison table]

── PRICING ANALYSIS ───────────────────────
[pricing table + value analysis]

── EXPLOITABLE WEAKNESSES ─────────────────
1. [gap] — Impact: [H/M/L], Difficulty: [E/M/H]
2. [gap] — Impact: [H/M/L], Difficulty: [E/M/H]
...

── SEO OPPORTUNITIES ──────────────────────
[keyword gaps and content opportunities]

── STRATEGIC RECOMMENDATIONS ──────────────
1. [action item with rationale]
2. [action item with rationale]
3. [action item with rationale]
```

## Inputs
- Your product description, features, and pricing
- 3-5 competitor URLs
- Target market definition
- Current differentiation (optional)

## Outputs
- Individual competitor profiles (positioning, features, messaging)
- Feature comparison matrix
- Pricing comparison with value-per-dollar analysis
- Messaging analysis with proof and emotional angles
- Weakness identification ranked by impact and difficulty
- SEO overlap and content gap analysis
- Strategic recommendations with action items

## Level History

- **Lv.1** — Base: Multi-competitor profiling, feature comparison matrix, pricing value analysis, messaging and proof audit, weakness identification with impact/difficulty ranking, SEO overlap analysis, strategic recommendations output. (Origin: MemStack v3.2, Mar 2026)
