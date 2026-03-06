---
name: feedback-analyzer
description: "Use when the user says 'analyze feedback', 'feedback analysis', 'customer feedback', 'feature requests', 'support tickets', 'user reviews', or has raw user feedback that needs categorization and prioritization."
---


# 📊 Feedback Analyzer — Customer Feedback Intelligence
*Categorize, score, and prioritize raw user feedback into an actionable report with executive summary.*

## Activation

When this skill activates, output:

`📊 Feedback Analyzer — Analyzing your customer feedback...`

| Context | Status |
|---------|--------|
| **User says "analyze feedback", "feedback analysis"** | ACTIVE |
| **User has support tickets, reviews, or survey data to process** | ACTIVE |
| **User asks "what are customers asking for?"** | ACTIVE |
| **User wants to build a roadmap from feedback** | Chain: feedback-analyzer → roadmap-builder |
| **User wants to write feature specs from feedback** | Chain: feedback-analyzer → feature-spec |
| **User wants competitor analysis (not user feedback)** | DORMANT — see competitor-analysis |

## Protocol

### Step 1: Gather Inputs

Ask the user for:
- **Feedback source**: What kind of feedback? (support tickets, app reviews, NPS surveys, social media, sales call notes, forum posts)
- **Raw data**: Paste the feedback, provide a file, or describe the themes
- **Product context**: What product is this feedback about?
- **Time period**: When was this feedback collected?
- **User segments**: Any known segmentation? (plan type, tenure, geography)

### Step 2: Categorize Feedback by Theme

Classify each piece of feedback into categories:

| Category | Icon | Description |
|----------|------|-------------|
| **Bug Report** | 🐛 | Something is broken or not working as expected |
| **Feature Request** | ✨ | User wants new functionality |
| **UX Issue** | 😤 | Feature exists but is confusing, slow, or frustrating |
| **Praise** | 💚 | Positive feedback, what users love |
| **Confusion** | ❓ | User doesn't understand how something works |
| **Churn Signal** | 🚪 | User is considering leaving or has left |

For each feedback item:
```
[ID] [Category Icon] [One-line summary]
     Source: [where it came from]
     Segment: [user type if known]
     Verbatim: "[exact user quote]"
```

### Step 3: Sentiment Analysis

Score sentiment per category and overall:

| Category | Count | Positive | Neutral | Negative | Avg Sentiment |
|----------|-------|----------|---------|----------|--------------|
| Bug Reports | [n] | — | — | [n] | -0.8 |
| Feature Requests | [n] | [n] | [n] | [n] | +0.2 |
| UX Issues | [n] | — | [n] | [n] | -0.5 |
| Praise | [n] | [n] | — | — | +0.9 |
| Confusion | [n] | — | [n] | [n] | -0.3 |
| Churn Signals | [n] | — | — | [n] | -0.9 |

**Overall sentiment**: [score from -1.0 to +1.0]
**Trend**: [improving / stable / declining] compared to last period (if available)

### Step 4: Frequency Ranking

Rank by how often each theme appears:

| Rank | Theme | Count | % of Total | Category | Trend |
|------|-------|-------|-----------|----------|-------|
| 1 | [most mentioned theme] | [n] | [%] | [type] | ↑↓→ |
| 2 | [second theme] | [n] | [%] | [type] | ↑↓→ |
| 3 | [third theme] | [n] | [%] | [type] | ↑↓→ |
| ... | ... | ... | ... | ... | ... |

Group related requests: "dark mode", "night theme", and "less bright" = same theme.

### Step 5: Impact Assessment

Score each theme by impact:

| Theme | Users Affected | Revenue Impact | Effort | Priority Score |
|-------|---------------|----------------|--------|---------------|
| [theme] | [many/some/few] | [high/med/low] | [high/med/low] | [1-10] |
| [theme] | [many/some/few] | [high/med/low] | [high/med/low] | [1-10] |

**Impact scoring:**
- Users Affected: Many (3) / Some (2) / Few (1)
- Revenue Impact: High (3) / Medium (2) / Low (1)
- Effort (inverted): Low effort (3) / Medium (2) / High (1)
- Priority Score = Users × Revenue × Effort (max 27, normalize to 10)

**Revenue impact indicators:**
- Churn mentions → High revenue impact
- Upgrade blockers → High revenue impact
- Nice-to-haves with no urgency → Low revenue impact

### Step 6: Map to Existing Roadmap

If the user has an existing roadmap or backlog:

| Feedback Theme | Existing Roadmap Item | Status | Gap |
|----------------|----------------------|--------|-----|
| [theme] | [feature/epic] | Planned Q2 | Aligned ✅ |
| [theme] | [feature/epic] | In Progress | Already building ✅ |
| [theme] | — | Not planned | NEW — needs evaluation ⚠️ |
| [theme] | [feature/epic] | Deprioritized | Users disagree — re-evaluate 🔄 |

Flag items where user demand contradicts roadmap priorities.

### Step 7: Quick Wins

Identify high-impact, low-effort actions:

```
━━━ QUICK WINS (Do This Week) ━━━━━━━━━━━━

1. [Action] — fixes [theme]
   Impact: [X users affected]
   Effort: [hours/days]
   Why now: [urgency reason]

2. [Action] — fixes [theme]
   Impact: [X users affected]
   Effort: [hours/days]
   Why now: [urgency reason]

3. [Action] — fixes [theme]
   Impact: [X users affected]
   Effort: [hours/days]
   Why now: [urgency reason]
```

Quick win criteria: < 1 week of effort, affects > 10% of feedback volume, no dependencies.

### Step 8: Executive Summary

Write a concise summary for leadership:

```
━━━ EXECUTIVE SUMMARY ━━━━━━━━━━━━━━━━━━━━

Feedback analyzed: [X] items from [sources] over [time period]
Overall sentiment: [score] ([trend])

TOP 5 ACTION ITEMS:

1. 🔴 [Critical]: [action] — [X] users affected, [revenue impact]
   Owner: [suggested team]
   Timeline: [urgency]

2. 🟡 [Important]: [action] — [X] users affected
   Owner: [suggested team]
   Timeline: [urgency]

3. 🟡 [Important]: [action] — [X] users affected
   Owner: [suggested team]
   Timeline: [urgency]

4. 🟢 [Nice-to-have]: [action] — [X] users requesting
   Owner: [suggested team]
   Timeline: [can wait]

5. 🟢 [Nice-to-have]: [action] — [X] users requesting
   Owner: [suggested team]
   Timeline: [can wait]

KEY INSIGHT:
[One paragraph: the single most important thing this feedback tells you
about your product direction, user satisfaction, or market position.]
```

### Step 9: Output

Present the complete feedback analysis:

```
━━━ FEEDBACK ANALYSIS REPORT ━━━━━━━━━━━━━
Product: [name]
Period: [date range]
Sources: [list]
Total items: [count]

── EXECUTIVE SUMMARY ──────────────────────
[top 5 action items + key insight]

── CATEGORY BREAKDOWN ─────────────────────
[category table with counts and sentiment]

── FREQUENCY RANKING ──────────────────────
[ranked theme list]

── IMPACT ASSESSMENT ──────────────────────
[prioritized theme scores]

── ROADMAP ALIGNMENT ──────────────────────
[mapping to existing plans]

── QUICK WINS ─────────────────────────────
[immediate actions]

── RAW FEEDBACK LOG ───────────────────────
[categorized individual items]
```

## Inputs
- Raw feedback data (pasted, file, or described themes)
- Feedback source type
- Product context
- Time period
- User segments (optional)
- Existing roadmap or backlog (optional, for mapping)

## Outputs
- Categorized feedback (bug, feature request, UX, praise, confusion, churn)
- Sentiment analysis per category and overall
- Frequency ranking of themes
- Impact assessment with priority scoring
- Roadmap alignment mapping
- Quick wins list (high impact, low effort)
- Executive summary with top 5 action items and key insight

## Level History

- **Lv.1** — Base: 6-category feedback taxonomy, sentiment scoring, frequency ranking with deduplication, impact assessment (users × revenue × effort), roadmap alignment mapping, quick wins identification, executive summary with prioritized action items. (Origin: MemStack v3.2, Mar 2026)
