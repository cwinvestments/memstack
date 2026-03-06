---
name: twitter-thread
description: "Use when the user says 'twitter thread', 'tweet thread', 'X thread', 'write a thread', or wants to create a multi-tweet narrative for Twitter/X."
---

# 🐦 Twitter Thread — Viral Thread Builder
*Generate engaging Twitter/X threads with hook tweets, narrative arc, data points, and clear CTAs ready to paste and post.*

## Activation

When this skill activates, output:

`🐦 Twitter Thread — Writing your thread...`

| Context | Status |
|---------|--------|
| **User says "twitter thread", "tweet thread", "X thread"** | ACTIVE |
| **User wants to create a multi-tweet narrative** | ACTIVE |
| **User mentions viral content or thread strategy** | ACTIVE |
| **User wants a TikTok script (not Twitter)** | DORMANT — see tiktok-script |
| **User wants a newsletter (not social)** | DORMANT — see newsletter |
| **User wants a LinkedIn post (not thread format)** | DORMANT — see content-pipeline for repurposing |

## Protocol

### Step 1: Gather Inputs

Ask the user for:
- **Topic**: What's the thread about?
- **Key insight**: What's the one thing readers should walk away knowing?
- **Target audience**: Who should care about this?
- **CTA**: What should readers do after? (follow, reply, visit link, sign up)
- **Tone**: Educational, provocative, storytelling, data-driven, personal?
- **Thread length**: Short (5-7 tweets), medium (8-10), long (11-15)?

### Step 2: Craft the Hook Tweet

The hook tweet determines whether anyone reads the rest. It must stop the scroll.

**Hook formulas:**

| Formula | Example | Best For |
|---------|---------|----------|
| **Bold claim** | "Most startup advice is wrong. Here's what actually works:" | Contrarian takes |
| **Surprising stat** | "97% of SaaS startups fail. The 3% that survive all do this one thing:" | Data-driven topics |
| **Story opener** | "Last year I was broke. This year I crossed $1M. Here's exactly what changed:" | Personal stories |
| **Question** | "Why do some people learn in 6 months what takes others 6 years?" | Educational content |
| **List promise** | "10 tools that replaced my entire $500/mo SaaS stack (all free):" | Practical guides |
| **Controversial** | "Unpopular opinion: You don't need a business plan. You need this instead:" | Debate starters |

**Hook tweet rules:**
- Must work as a standalone tweet (not "Thread 🧵")
- First 50 characters are the most important (preview in timeline)
- No hashtags in the hook tweet
- End with a colon or implication there's more to read
- Never start with "I" — start with the insight

### Step 3: Build Thread Structure

Design the narrative arc:

```
Tweet 1:  HOOK — Stop the scroll, promise value
Tweet 2:  CONTEXT — Why this matters now
Tweet 3:  POINT 1 — First key insight or step
Tweet 4:  EVIDENCE 1 — Data, example, or story supporting Point 1
Tweet 5:  POINT 2 — Second key insight or step
Tweet 6:  EVIDENCE 2 — Data, example, or story supporting Point 2
Tweet 7:  POINT 3 — Third key insight or step
Tweet 8:  EVIDENCE 3 — Data, example, or story supporting Point 3
Tweet 9:  INSIGHT — The "aha" moment connecting everything
Tweet 10: CTA — What to do next + engagement prompt
```

**Structure variations:**

| Type | Pattern | Best For |
|------|---------|----------|
| **How-to** | Hook → Step 1 → Step 2 → ... → CTA | Tutorials, guides |
| **Listicle** | Hook → Item 1 → Item 2 → ... → Summary → CTA | Tools, tips, resources |
| **Story** | Hook → Setup → Conflict → Resolution → Lesson → CTA | Personal experience |
| **Analysis** | Hook → Context → Data → Interpretation → Implication → CTA | Industry takes |
| **Myth-busting** | Hook → Myth 1 → Truth → Myth 2 → Truth → Key takeaway → CTA | Contrarian content |

### Step 4: Write Each Tweet

For each tweet, follow these rules:

**Format rules:**
- 280 characters max per tweet
- Short lines (2-5 words) for readability
- Line breaks between ideas
- One idea per tweet — never cram two points
- Each tweet must deliver value standalone
- End tweets 2-8 with an implied "and..." to pull readers forward

**Power techniques:**
```
• Use numbers:        "3 reasons", "saved $50K", "in 14 days"
• Use contrast:       "Most people X. Top performers Y."
• Use specificity:    "$10,847 in revenue" not "lots of money"
• Use analogies:      "Writing code is like building LEGO"
• Use white space:    Short paragraphs, line breaks, breathing room
• Use formatting:     • Bullets for lists
                      → Arrows for steps
                      ↳ Nested for sub-points
```

**What NOT to do:**
- Don't start tweets with "Also," or "Additionally,"
- Don't number tweets (1/10, 2/10) — the platform does this
- Don't use 🧵 emoji — it's overdone
- Don't end every tweet with a question — one or two max
- Don't stuff hashtags mid-thread — save for last tweet or skip entirely

### Step 5: Include Data Points

Each thread needs credibility. Include at least 2-3 of:

| Evidence Type | Example | Impact |
|---------------|---------|--------|
| **Statistic** | "Companies with blogs get 67% more leads" | High — concrete, shareable |
| **Case study** | "When Airbnb did X, they grew Y" | High — narrative + proof |
| **Personal data** | "My email list went from 0 to 10K in 6 months" | Medium — relatable |
| **Expert quote** | "As Naval says, 'Code and media are permissionless leverage'" | Medium — borrowed authority |
| **Comparison** | "Tool A costs $500/mo. This free alternative does 90% of it" | High — practical |
| **Before/after** | "Before: 2 hours/day on email. After: 20 minutes" | High — transformation |

### Step 6: Write the Final CTA Tweet

The last tweet should do two things: summarize and prompt action.

**CTA formulas:**

```
── SUMMARY + FOLLOW ───────────────────────
TL;DR:

• [Point 1]
• [Point 2]
• [Point 3]

If you found this useful, follow me @[handle] for more [topic].

── SUMMARY + LINK ─────────────────────────
I wrote a complete guide on this.

[X] pages, [Y] templates, free.

Grab it here: [link]

── SUMMARY + ENGAGEMENT ───────────────────
Which of these resonated most?

Reply with the number:
1. [Point 1]
2. [Point 2]
3. [Point 3]

── RETWEET + FOLLOW ───────────────────────
If this thread saved you time, RT the first tweet to help others find it.

Follow @[handle] for a thread like this every [frequency].
```

### Step 7: Formatting & Readability

Apply final formatting:

```
── FORMATTING CHECKLIST ───────────────────

☐ Hook tweet < 280 chars, no hashtags
☐ Each tweet standalone-valuable
☐ Short lines (phone-optimized readability)
☐ Data points in 2+ tweets
☐ One idea per tweet
☐ No filler words ("basically", "actually", "just")
☐ Active voice throughout
☐ CTA is clear and single-action
☐ Thread reads well without images
☐ Total thread: [5-15] tweets
```

### Step 8: Output

Present the numbered thread ready to paste:

```
━━━ TWITTER THREAD: [Topic] ━━━━━━━━━━━━━━
Tweets: [count]
Target: [audience]
CTA: [action]

── THREAD ─────────────────────────────────

1/
[Hook tweet — 280 chars max]

2/
[Context tweet]

3/
[Point 1]

4/
[Evidence 1]

5/
[Point 2]

6/
[Evidence 2]

7/
[Point 3]

8/
[Evidence 3]

9/
[Key insight]

10/
[CTA tweet]

── POSTING NOTES ──────────────────────────
Best times to post: [day/time recommendations]
Reply to your own thread to boost engagement
Pin the thread after posting
Quote-tweet the hook with a teaser 24 hours later

── ENGAGEMENT STRATEGY ────────────────────
• Reply to every comment in the first 2 hours
• Like all quote tweets
• Follow back engaged accounts in your niche
• Repost the thread in 30 days with updated data
```

## Inputs
- Topic and key insight
- Target audience
- CTA (follow, link, reply, sign up)
- Tone (educational, provocative, storytelling, data-driven)
- Thread length preference (short/medium/long)

## Outputs
- Hook tweet using proven scroll-stopping formulas
- Structured thread with narrative arc (5-15 tweets)
- Each tweet standalone-valuable with proper formatting
- Data points, case studies, or evidence integrated
- Final CTA tweet with engagement prompt
- Posting and engagement strategy
- Complete numbered thread ready to paste into Twitter/X

## Level History

- **Lv.1** — Base: 6 hook tweet formulas, 5 thread structure patterns (how-to/listicle/story/analysis/myth-busting), per-tweet formatting rules (280 chars, short lines, one idea), data point integration, CTA tweet templates, posting strategy with engagement tips, paste-ready numbered output. (Origin: MemStack v3.2, Mar 2026)
