---
name: memstack-product-feedback-analyzer
description: "Use this skill when the user says 'analyze feedback', 'feedback analysis', 'what are customers asking for', or has support tickets, reviews, or survey data to categorize, score, and prioritize into actionable reports. Do NOT use for competitor analysis or market research."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# Feedback Analyzer — Analyzing customer feedback...
*Categorizes, scores, and prioritizes customer feedback from support tickets, reviews, and surveys into actionable reports with feature request rankings, sentiment trends, and action items.*

## Activation

When this skill activates, output:

`Feedback Analyzer — Analyzing customer feedback...`

Then execute the protocol below.

## Context Guard

| Context | Status |
|---------|--------|
| User says "analyze feedback", "feedback analysis" | ACTIVE |
| User says "what are customers asking for" | ACTIVE |
| User has support tickets, reviews, or survey data to analyze | ACTIVE |
| User wants competitor pricing or market analysis | DORMANT — use Competitor Analysis |
| User wants to write a PRD from scratch | DORMANT — use PRD Writer |

## Common Mistakes

| Mistake | Why It's Wrong |
|---------|---------------|
| "Build what the loudest customer asks for" | Loudest ≠ most valuable. One enterprise client's niche request shouldn't override 500 users' common need. |
| "Count votes to prioritize" | "Most requested" ignores impact and effort. A rarely requested feature might retain your best customers. |
| "Ignore negative reviews" | 1-star reviews reveal real pain. Positive reviews confirm what works — negatives reveal what to fix. |
| "Read feedback literally" | Users describe symptoms, not root causes. "I need an export button" might mean "I can't get data out." |
| "Analyze once, never again" | Feedback is a continuous signal. Batch-analyze monthly or quarterly to spot trends. |

## Protocol

### Step 1: Collect Feedback Data

If the user hasn't provided feedback data, ask:

> 1. **Source** — where is the feedback? (support tickets, app reviews, survey responses, social media, sales call notes)
> 2. **Volume** — how much feedback? (helps determine analysis approach)
> 3. **Time range** — what period does this cover?
> 4. **Format** — text dump, CSV, spreadsheet, or screenshot?
> 5. **Product context** — any recent launches, changes, or known issues?

**Supported input formats:**
- Raw text (pasted feedback items)
- CSV/spreadsheet with feedback column
- Support ticket exports (Intercom, Zendesk, Help Scout)
- App store review exports
- Survey responses (Typeform, Google Forms)
- Social media mentions or comments

### Step 2: Categorize Feedback

Classify each piece of feedback into categories:

**Primary categories:**

| Category | Definition | Example |
|----------|-----------|---------|
| **Feature request** | User wants new functionality | "I wish I could export to PDF" |
| **Bug report** | Something is broken or unexpected | "The save button doesn't work on mobile" |
| **UX issue** | Works but confusing or frustrating | "I can never find the settings page" |
| **Performance** | Speed, reliability, or scaling | "The dashboard takes 30 seconds to load" |
| **Praise** | Positive feedback about what works | "Love the new dark mode!" |
| **Churn signal** | Indicates potential or actual churn | "I'm switching to [competitor] because..." |
| **Pricing** | Feedback about cost or value | "Too expensive for what I get" |
| **Support** | About the support experience itself | "Took 3 days to get a response" |

**Categorization output:**

```markdown
## Feedback Categorization

| ID | Feedback (summarized) | Category | Sentiment | Source | Date |
|----|----------------------|----------|-----------|--------|------|
| F-001 | [Summarized feedback] | Feature request | Neutral | Support | [Date] |
| F-002 | [Summarized feedback] | Bug report | Negative | App store | [Date] |
| F-003 | [Summarized feedback] | Praise | Positive | Survey | [Date] |
```

### Step 3: Sentiment Analysis

Rate each feedback item and calculate aggregate sentiment:

**Sentiment scale:**

| Score | Label | Indicators |
|-------|-------|-----------|
| -2 | Very negative | Anger, threats to cancel, profanity, "terrible", "worst" |
| -1 | Negative | Frustration, disappointment, "can't", "doesn't work" |
| 0 | Neutral | Factual request, no emotional language |
| +1 | Positive | Satisfaction, mild praise, "nice", "helpful" |
| +2 | Very positive | Enthusiasm, recommendation, "love", "amazing", "game-changer" |

**Aggregate sentiment dashboard:**

```markdown
## Sentiment Overview

**Overall sentiment score:** [Average across all feedback]
**Distribution:**
- Very positive (★★): [X]% ([count])
- Positive (★): [X]% ([count])
- Neutral (—): [X]% ([count])
- Negative (✗): [X]% ([count])
- Very negative (✗✗): [X]% ([count])

**Sentiment by category:**
| Category | Avg Sentiment | Volume | Trend |
|----------|-------------|--------|-------|
| Feature requests | [Score] | [Count] | [↑ ↓ →] |
| Bug reports | [Score] | [Count] | [↑ ↓ →] |
| UX issues | [Score] | [Count] | [↑ ↓ →] |
| Praise | [Score] | [Count] | [↑ ↓ →] |
```

### Step 4: Extract Feature Requests & Themes

Group related feature requests into themes:

```markdown
## Feature Request Themes

### Theme 1: [Theme Name] — [X mentions]
**User need:** [What users actually need, not what they asked for]

| Request | Mentions | Example Quotes |
|---------|----------|---------------|
| [Specific request A] | [X] | "[Direct quote]" |
| [Specific request B] | [X] | "[Direct quote]" |
| [Specific request C] | [X] | "[Direct quote]" |

**Root need:** [The underlying problem these requests share]
**Potential solutions:**
1. [Solution option A — simplest]
2. [Solution option B — most complete]

---

### Theme 2: [Theme Name] — [X mentions]
[Same format]
```

**Theme extraction rules:**
- Merge duplicates — "PDF export", "download as PDF", "save to PDF" = one request
- Look for the root need behind surface requests
- Group by problem, not by proposed solution
- Note the user segment making each request (free vs. paid, new vs. veteran)

### Step 5: Prioritize with RICE Framework

Score each theme or major request:

| Theme | Reach | Impact | Confidence | Effort | RICE Score |
|-------|-------|--------|-----------|--------|-----------|
| [Theme 1] | [X] | [1-3] | [%] | [person-weeks] | [Score] |
| [Theme 2] | [X] | [1-3] | [%] | [person-weeks] | [Score] |
| [Theme 3] | [X] | [1-3] | [%] | [person-weeks] | [Score] |

**RICE scoring:**

```
Score = (Reach × Impact × Confidence) ÷ Effort
```

| Factor | How to Score |
|--------|-------------|
| **Reach** | How many users per quarter? (estimated or from feedback volume) |
| **Impact** | 3 = massive, 2 = high, 1 = medium, 0.5 = low, 0.25 = minimal |
| **Confidence** | 100% = high (data-backed), 80% = medium, 50% = low (gut feel) |
| **Effort** | Person-weeks to build (smaller = better score) |

**Priority buckets (after scoring):**

| Priority | RICE Range | Action |
|----------|-----------|--------|
| P0 — Do now | Top 20% of scores | Schedule for next sprint/quarter |
| P1 — Plan | Middle 40% | Add to roadmap for next quarter |
| P2 — Consider | Lower 30% | Keep in backlog, monitor volume |
| P3 — Decline | Bottom 10% | Close with explanation, revisit if volume grows |

### Step 6: Identify Churn Signals

Flag feedback that indicates churn risk:

```markdown
## Churn Risk Signals

| Signal | Severity | Count | Example |
|--------|----------|-------|---------|
| Mentions competitor by name | High | [X] | "[Quote]" |
| "Canceling" or "switching" | High | [X] | "[Quote]" |
| Pricing complaints from paying users | Medium | [X] | "[Quote]" |
| Repeated bug reports (same user, same issue) | Medium | [X] | "[Quote]" |
| Feature request marked as "blocker" | Medium | [X] | "[Quote]" |
| Declining usage mentioned | Low | [X] | "[Quote]" |

### Churn prevention recommendations:
1. **Immediate:** [Action for high-severity signals]
2. **This quarter:** [Action for medium-severity patterns]
3. **Ongoing:** [Monitoring approach for low-severity]
```

### Step 7: Generate Action Items

```markdown
## Action Items

### Immediate (this sprint)
| # | Action | Owner | Source |
|---|--------|-------|--------|
| 1 | [Fix critical bug X] | Engineering | [F-002, F-015] |
| 2 | [Respond to churn risk Y] | Support | [F-008] |

### This Quarter
| # | Action | Owner | Source |
|---|--------|-------|--------|
| 3 | [Build top RICE-scored feature] | Product + Eng | [Theme 1] |
| 4 | [Address UX issue pattern] | Design + Eng | [Theme 3] |

### Process Improvements
| # | Action | Owner | Source |
|---|--------|-------|--------|
| 5 | [Set up feedback tagging in support tool] | Support | — |
| 6 | [Schedule monthly feedback review] | Product | — |

### Communicate Back to Users
| # | Action | Channel |
|---|--------|---------|
| 7 | "We heard you — [feature] is shipping in [timeframe]" | Email / Changelog |
| 8 | "Known issue: [bug] — fix incoming [date]" | Status page |
```

## Output Format

```markdown
# Feedback Analysis — [Product Name]

**Period:** [Date range]
**Sources:** [List of sources]
**Total feedback items:** [Count]

## 1. Sentiment Overview
[Dashboard from Step 3]

## 2. Category Breakdown
[Categorization summary from Step 2]

## 3. Feature Request Themes
[Themed groupings from Step 4]

## 4. Priority Rankings (RICE)
[Scored and ranked table from Step 5]

## 5. Churn Signals
[Churn risk table from Step 6]

## 6. Action Items
[Prioritized actions from Step 7]

## 7. Trends & Patterns
[Any notable trends: increasing complaints in area X, praise for recent change Y]

## Appendix: Raw Data
[Categorized feedback table — every item with ID, summary, category, sentiment]
```

## Completion

```
Feedback Analyzer — Complete!

Feedback items analyzed: [Count]
Sources: [List]
Overall sentiment: [Score] ([Label])
Feature themes identified: [Count]
Top priority: [Theme name] (RICE: [score])
Churn signals: [Count] ([severity breakdown])
Action items: [Count]

Next steps:
1. Review RICE priorities with product team
2. Address immediate action items this sprint
3. Communicate "we heard you" to users on top themes
4. Schedule monthly feedback analysis cadence
5. Set up tagging taxonomy in support tool for easier future analysis
```

## Level History

- **Lv.1** — Base: 8-category feedback classification, sentiment scoring (-2 to +2) with aggregate dashboard, feature request theme extraction with root need analysis, RICE prioritization framework (reach, impact, confidence, effort), churn signal identification with severity levels, action item generation (immediate/quarterly/process/communication), trends and patterns identification. (Origin: MemStack Pro v3.2, Mar 2026)
