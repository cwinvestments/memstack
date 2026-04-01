---
name: memstack-content-newsletter
description: "Use this skill when the user says 'newsletter', 'email newsletter', 'weekly digest', 'subscriber growth', 'open rates', or needs subject lines, content structure, sponsorship placement, and growth tactics for email newsletters. Do NOT use for lead magnets or content pipelines."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# Newsletter — Writing email newsletter edition...
*Produces an email newsletter edition with subject line formulas, section structure, personalization, link placement strategy, growth tactics, and engagement optimization.*

## Activation

When this skill activates, output:

`Newsletter — Writing email newsletter edition...`

Then execute the protocol below.

## Context Guard

| Context | Status |
|---------|--------|
| User says "newsletter", "email newsletter", "weekly digest" | ACTIVE |
| User says "subscriber growth" or "open rates" | ACTIVE |
| User wants to write a newsletter edition or start a newsletter | ACTIVE |
| User wants a lead magnet with email capture | DORMANT — use Lead Magnet |
| User wants a full content automation pipeline | DORMANT — use Content Pipeline |

## Common Mistakes

| Mistake | Why It's Wrong |
|---------|---------------|
| "Newsletter = company updates" | Nobody cares about your company news. Deliver value: insights, tips, curated content. |
| "Generic subject line" | "[Company] Monthly Newsletter" gets 10% opens. Curiosity-driven subjects get 35%+. |
| "No consistent format" | Readers want predictable value. A consistent structure builds habit and trust. |
| "Too many links" | More than 3-5 links per section dilutes clicks. Feature one primary link prominently. |
| "No growth strategy" | "Build it and they will come" doesn't work. Actively promote every issue. |

## Protocol

### Step 1: Gather Newsletter Requirements

If the user hasn't provided details, ask:

> 1. **Topic/niche** — what's the newsletter about?
> 2. **Audience** — who reads it? (role, industry, experience level)
> 3. **Frequency** — weekly, biweekly, or monthly?
> 4. **Type** — curated links, original essays, tips, industry news, or mixed?
> 5. **Current state** — new or existing? (subscriber count, open rates)
> 6. **Monetization** — free, paid, or sponsored?

### Step 2: Write the Subject Line

**Subject line formulas:**

| Formula | Template | Example |
|---------|---------|---------|
| **Curiosity gap** | [Topic]: The [thing] nobody talks about | "Pricing: The metric nobody tracks" |
| **Numbered value** | [X] [things] to [outcome] this week | "5 tools to ship faster this week" |
| **Question** | Why [common practice] [doesn't work / is wrong]? | "Why your landing page isn't converting?" |
| **Personal** | I [did thing] — here's what happened | "I quit meetings for a month" |
| **Direct value** | How to [outcome] (in [constraint]) | "How to write copy that converts (in 20 min)" |
| **Current event** | [Event/trend]: What it means for [audience] | "GPT-5: What it means for developers" |

**Subject line rules:**
- 6-10 words (40-50 characters) for mobile display
- No ALL CAPS, no spam triggers ("FREE", "ACT NOW", "!!!")
- Preview text (first 90 characters of email) should complement, not repeat the subject
- A/B test 2 subjects per send (most platforms support this)
- Track open rates by subject formula — double down on what works

### Step 3: Design Section Structure

**Newsletter format template:**

```markdown
# [Newsletter Name] — [Edition Title or Number]

## Intro (2-3 sentences)
[Personal note, context for this edition, or a hook that frames the content]

---

## [Section 1: Primary Content] (60% of newsletter)
[Your main value — original insight, deep dive, or featured piece]
[Include one primary CTA link]

---

## [Section 2: Quick Hits / Curated] (25% of newsletter)
### [Item 1 title]
[1-2 sentence summary + link]

### [Item 2 title]
[1-2 sentence summary + link]

### [Item 3 title]
[1-2 sentence summary + link]

---

## [Section 3: Closer] (15% of newsletter)
[Personal sign-off, question for readers, or community highlight]

---

[Footer: Unsubscribe | Forward to a friend | [Social links]]
```

**Section type options (pick 2-4 per edition):**

| Section | Content | Purpose |
|---------|---------|---------|
| **Deep Dive** | Original essay or analysis (500-800 words) | Demonstrate expertise |
| **Quick Hits** | 3-5 curated links with one-line summaries | Deliver breadth of value |
| **Tool/Resource** | Featured tool with your take on it | Practical value |
| **Tip of the Week** | One actionable tactic they can use today | Quick win |
| **Community Spotlight** | Reader question, testimonial, or submission | Build community |
| **Sponsor Section** | Sponsored content (clearly labeled) | Monetization |
| **Poll/Question** | Ask readers something — drives replies | Engagement signal |

### Step 4: Write the Edition

**Intro paragraph rules:**
- 2-3 sentences maximum
- Personal and conversational (not corporate)
- Frames why THIS edition matters
- Optional: reference a current event or reader feedback

**Body content rules:**
- Write at an 8th-grade reading level (clear, accessible)
- Use headers, bold, and bullet points for scannability
- One idea per paragraph (3 sentences max)
- Link text should describe the destination ("Read the full case study" not "Click here")
- Primary CTA should appear within the first scroll (above 300 words)

**Personalization techniques:**

| Technique | Implementation | Impact |
|----------|---------------|--------|
| First name in subject | "Hey {first_name}, [subject]" | +10-15% open rate |
| Segment by interest | Tag subscribers → send relevant content | +20-30% click rate |
| Reference past behavior | "Since you read about [topic]..." | Higher engagement |
| Reader-submitted content | Feature reader questions or wins | Community loyalty |

### Step 5: Link Placement Strategy

**Link placement hierarchy:**

| Position | Purpose | Click Priority |
|----------|---------|---------------|
| **Above the fold** (first 100 words) | Primary CTA or featured link | Highest |
| **End of main section** | Deeper reading link | High |
| **Quick hits section** | Curated resource links | Medium |
| **Closer** | Social follow or referral link | Low |

**Rules:**
- 1 primary link per edition (the ONE thing you want them to click)
- 3-5 secondary links maximum (curated content, resources)
- No more than 8 total links (including footer) — too many dilutes clicks
- Use descriptive anchor text, not raw URLs
- Track clicks with UTM parameters: `?utm_source=newsletter&utm_medium=email&utm_campaign=edition-[N]`

### Step 6: Growth Tactics

**Subscriber acquisition channels:**

| Channel | Tactic | Expected Growth |
|---------|--------|----------------|
| **Website** | Email capture in header, footer, and exit-intent popup | Steady baseline |
| **Social media** | Share a highlight from each edition with subscribe link | 5-15 subs/post |
| **Twitter/X threads** | End threads with "I go deeper in my newsletter: [link]" | 10-50 subs/thread |
| **Cross-promotion** | Swap recommendations with similar-sized newsletters | 50-200 per swap |
| **Referral program** | "Refer 3 friends → get [bonus]" | 10-20% of new subs |
| **Gated content** | Best content behind email signup (lead magnet) | High conversion |
| **Guest posts** | Write for others, link to newsletter in bio | 20-100 per post |

**Retention metrics to track:**

| Metric | Target | Red Flag |
|--------|--------|----------|
| Open rate | >35% | <20% |
| Click rate | >3% | <1% |
| Unsubscribe rate | <0.5% per send | >1% |
| Reply rate | >0.5% | 0% (no engagement) |
| Growth rate (net) | >5% monthly | Negative (losing subs) |

### Step 7: Scheduling & Send Optimization

**Optimal send times:**

| Audience | Best Day | Best Time | Why |
|----------|---------|-----------|-----|
| Business / B2B | Tuesday-Thursday | 9-10 AM local | Morning inbox check |
| Creators / Solo | Tuesday or Saturday | 8-9 AM local | Before the day fills up |
| Developers | Wednesday | 10 AM local | Mid-week engagement peak |
| General / Consumer | Sunday or Tuesday | 9-10 AM local | Weekend reading or fresh week |

**Pre-send checklist:**
- [ ] Subject line is 6-10 words, creates curiosity
- [ ] Preview text complements the subject (not a repeat)
- [ ] All links work (click-test every one)
- [ ] UTM parameters on all links
- [ ] Images have alt text
- [ ] Mobile preview looks good (60%+ open on mobile)
- [ ] Unsubscribe link is visible
- [ ] Spell check passed
- [ ] Send a test email to yourself first

## Output Format

```markdown
# [Newsletter Name] — Edition [#]

**Subject:** [Subject line]
**Preview text:** [90 characters]
**Send date:** [Date, Time, Timezone]

---

[Full newsletter content following the structure from Step 3]

---

## Metrics to Track
- Open rate target: [X]%
- Click rate target: [X]%
- Primary CTA link: [URL]
```

## Completion

```
Newsletter — Complete!

Edition: [#/Title]
Subject line: "[Subject]"
Sections: [Count]
Links: [Count] ([1] primary, [X] secondary)
Word count: [X]

Next steps:
1. Load into your email platform
2. Preview on mobile (most opens are mobile)
3. A/B test the subject line (send 2 variants to 20% each, winner to 60%)
4. Schedule for [optimal time]
5. After sending: share a highlight on social media with subscribe CTA
```

## Level History

- **Lv.1** — Base: 6 subject line formulas, section structure template (intro, deep dive, quick hits, closer), body writing rules with personalization techniques, link placement hierarchy (primary + secondary), 7 growth channels with expected results, retention metrics with red flags, send time optimization, pre-send checklist. (Origin: MemStack Pro v3.2, Mar 2026)
