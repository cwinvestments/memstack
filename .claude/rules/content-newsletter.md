---
name: newsletter
description: "Use when the user says 'newsletter', 'email newsletter', 'weekly digest', 'write a newsletter', or wants to create a complete newsletter edition with subject line, content, and growth strategy."
---

# 📬 Newsletter — Email Newsletter Builder
*Generate complete newsletter editions with subject lines, structured content, sponsorship placement, growth tactics, and platform-ready formatting.*

## Activation

When this skill activates, output:

`📬 Newsletter — Writing your newsletter edition...`

| Context | Status |
|---------|--------|
| **User says "newsletter", "email newsletter", "weekly digest"** | ACTIVE |
| **User wants to write a newsletter edition** | ACTIVE |
| **User mentions subject lines, open rates, or email growth** | ACTIVE |
| **User wants a lead magnet with nurture emails** | DORMANT — see lead-magnet |
| **User wants a content pipeline (newsletter is one channel)** | DORMANT — see content-pipeline |
| **User wants a Twitter thread (not email)** | DORMANT — see twitter-thread |

## Protocol

### Step 1: Gather Inputs

Ask the user for:
- **Audience**: Who reads this? (developers, marketers, founders, general)
- **Topic**: What's this edition about? (or main theme)
- **Frequency**: Daily, weekly, biweekly, monthly?
- **Brand voice**: Casual, professional, witty, authoritative?
- **Newsletter name**: What's it called?
- **Content type**: Original essays, curated links, industry news, tutorials, opinion?
- **Monetization**: Sponsored? Affiliate links? Paid tier?
- **Platform**: ConvertKit, Beehiiv, Substack, Mailchimp, SendGrid?

### Step 2: Write Subject Line & Preview Text

**Subject line (50 chars max for full visibility):**

| Formula | Example | Open Rate Impact |
|---------|---------|-----------------|
| **Number + benefit** | "5 tools that saved me 10 hours this week" | High — specific, practical |
| **Question** | "Are you making this hiring mistake?" | Medium — curiosity gap |
| **How-to** | "How to write copy that converts (template inside)" | High — clear value |
| **Contrarian** | "Why I stopped using React" | High — triggers curiosity |
| **Urgency** | "This deal expires Friday" | High — but use sparingly |
| **Personal** | "I almost quit last week. Here's why I didn't." | High — emotional connection |
| **News hook** | "Google just changed SEO forever" | High — timely relevance |

**Generate 3 subject line options** ranked by expected performance.

**Preview text (90 chars, visible after subject in inbox):**
- Complements the subject, doesn't repeat it
- Adds context or teases content
- Example: Subject: "5 tools that saved me 10 hours" → Preview: "Plus: why I'm rebuilding my entire stack"

### Step 3: Write Newsletter Content

**Structure template:**

```
── PERSONAL OPENER (2-3 sentences) ────────

[Start with a personal anecdote, observation, or
timely reference that connects to the main topic.
This builds connection before the content.]

── MAIN CONTENT ───────────────────────────

[The primary article, tutorial, insight, or essay.
This is the main value of the newsletter.]

Structure options:
  A) Original essay (500-800 words)
  B) Tutorial with steps (300-500 words + code/examples)
  C) Curated links with commentary (5-7 links, 2-3 sentences each)
  D) Industry analysis (400-600 words with data)

── SECONDARY CONTENT (optional) ───────────

[A shorter section with additional value:]
  • "Quick hits" — 3-5 bullet point links or tips
  • "Tool of the week" — one recommendation with why
  • "Quote I'm thinking about" — curated quote + your take
  • "Ask me anything" — answer a reader question

── CTA ────────────────────────────────────

[One clear call-to-action:]
  • Reply to this email with [question]
  • Check out [product/resource]
  • Share this newsletter with a friend
  • Upgrade to premium for [benefit]
```

**Content writing rules:**
- Write at a conversational level — like emailing a smart friend
- One main idea per edition — don't try to cover everything
- Use subheadings every 150-200 words for scannability
- Bold key phrases — readers scan before reading
- Keep paragraphs to 2-3 sentences max
- Include at least one actionable takeaway
- End sections with a transition or hook to the next

### Step 4: Content Curation

For curated newsletters, how to find and present items:

**Finding content:**
- RSS feeds from industry blogs
- Twitter/X lists of thought leaders
- Hacker News, Reddit, Lobsters for tech
- Product Hunt for tools
- Google Alerts for niche keywords
- Personal network and Slack communities

**Curation format per item:**
```
📌 [Headline/Title]
   [Source] — [reading time]

   [2-3 sentence summary in YOUR voice — not just the article abstract.
   Add your opinion, context, or why it matters to your audience.]

   → [Read the full article](link)
```

**Curation rules:**
- Add YOUR perspective — readers follow you, not the sources
- 5-7 items per curated edition (more feels like a dump)
- Mix sources — don't over-index on one publication
- Include at least one contrarian or surprising piece
- Date-stamp anything time-sensitive

### Step 5: Sponsorship/Ad Placement

If the newsletter is monetized:

**Sponsorship slot types:**

| Slot | Position | Format | Pricing Range |
|------|----------|--------|---------------|
| **Header sponsor** | Top, before content | Logo + 1-line mention | $$$$ |
| **Mid-content ad** | Between sections | 2-3 sentences + link + image | $$$ |
| **Classified** | Bottom, after content | 1-2 sentences + link | $$ |
| **Dedicated send** | Entire email is sponsored | Full sponsor content | $$$$$ |

**Sponsor integration template:**
```
── SPONSORED ──────────────────────────────

[This edition is brought to you by [Sponsor Name]]

[2-3 sentences about the sponsor's product, written in
YOUR voice, not corporate copy. Focus on why your readers
would care.]

→ [Check out Sponsor Name](tracking link)

────────────────────────────────────────────
```

**Sponsorship rules:**
- Label sponsored content clearly
- Write sponsor copy in your voice (not theirs)
- Max 1 sponsor per edition (2 if header + classified)
- Never sponsor products you wouldn't genuinely recommend
- Track click-through rates for sponsor reporting

### Step 6: Growth Tactics

**Organic growth strategies:**

| Tactic | Effort | Expected Impact |
|--------|--------|-----------------|
| **Referral program** | Medium | High — "Refer 3 friends, get [reward]" |
| **Cross-promotion** | Low | Medium — swap recommendations with similar newsletters |
| **Lead magnet** | Medium | High — free resource for subscribing |
| **Social sharing** | Low | Medium — share snippets as threads/posts |
| **Guest posts** | High | Medium — write for other newsletters |
| **SEO archive** | Medium | High (long-term) — publish past editions as blog posts |
| **Giveaways** | Low | High (short-term) — "Subscribe to win [prize]" |

**Referral program design:**

| Referrals | Reward |
|-----------|--------|
| 1 | Shout-out in next edition |
| 3 | Exclusive template/resource |
| 5 | Free month of premium |
| 10 | 1-on-1 call with you |
| 25 | Lifetime premium access |

**Footer CTA template:**
```
────────────────────────────────────────────
📬 Enjoyed this? Share [Newsletter Name] with a friend:
[Referral link]

You've referred [X] people so far. [Y] more for [next reward]!
────────────────────────────────────────────
```

### Step 7: Analytics Benchmarks

Track these metrics per edition:

| Metric | Target | Industry Avg | Action if Below |
|--------|--------|-------------|-----------------|
| **Open rate** | 40-50% | 30-35% | Test subject lines, clean list |
| **Click rate** | 5-8% | 2-4% | Improve CTAs, reduce links |
| **Unsubscribe rate** | < 0.3% | 0.2-0.5% | Check frequency, content relevance |
| **Reply rate** | 1-3% | < 1% | Ask more questions, be personal |
| **Growth rate** | 5-10%/mo | 2-5%/mo | Increase promotion, add lead magnet |
| **Bounce rate** | < 2% | 2-5% | Clean list, verify emails on signup |
| **Spam complaint** | < 0.1% | 0.1% | Add clear unsubscribe, set expectations |

**List hygiene:**
- Remove unengaged subscribers (no opens in 90 days) quarterly
- Send re-engagement campaign before removing
- Use double opt-in for higher quality subscribers
- Monitor deliverability score monthly

### Step 8: Output

Present the complete newsletter edition:

```
━━━ NEWSLETTER: [Newsletter Name] ━━━━━━━━
Edition: #[number] — [date]
Topic: [main topic]
Audience: [who]

── SUBJECT LINES (pick one) ───────────────
Option A: [subject] — Preview: [preview text]
Option B: [subject] — Preview: [preview text]
Option C: [subject] — Preview: [preview text]

── NEWSLETTER BODY ────────────────────────

[Personal opener]

[Main content — essay, tutorial, or curated links]

[Sponsored section — if applicable]

[Secondary content]

[CTA]

[Footer with referral link + unsubscribe]

── GROWTH PLAN ────────────────────────────
This month's focus: [tactic]
Referral program: [status]
Target: [subscriber goal]

── ANALYTICS TARGETS ──────────────────────
Open rate target: [X]%
Click rate target: [X]%
Growth target: [X] new subscribers this month
```

## Inputs
- Audience and niche
- Topic or theme for this edition
- Frequency and brand voice
- Newsletter name
- Content type (original, curated, hybrid)
- Monetization strategy (optional)
- Email platform

## Outputs
- 3 subject line options with preview text
- Complete newsletter body (opener, main content, secondary, CTA)
- Content curation framework with commentary format
- Sponsorship slot placement with integration template
- Growth tactics with referral program design
- Analytics benchmarks with action thresholds
- Platform-ready formatted edition

## Level History

- **Lv.1** — Base: 7 subject line formulas with preview text, structured newsletter template (opener/main/secondary/CTA), content curation format with commentary, sponsorship slot types and integration, growth tactics with referral program tiers, analytics benchmarks with action thresholds, platform-ready output. (Origin: MemStack v3.2, Mar 2026)
