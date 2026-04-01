---
name: memstack-content-twitter-thread
description: "Use this skill when the user says 'twitter thread', 'tweet thread', 'X thread', 'viral thread', or wants to create a multi-tweet narrative with hook tweets, data points, and CTAs. Do NOT use for TikTok scripts, newsletters, or LinkedIn posts."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# Twitter Thread — Writing viral thread...
*Creates multi-tweet threads (5-15 posts) with hook formulas, narrative arc, engagement tactics, data points, CTA placement, and scheduling strategy.*

## Activation

When this skill activates, output:

`Twitter Thread — Writing viral thread...`

Then execute the protocol below.

## Context Guard

| Context | Status |
|---------|--------|
| User says "twitter thread", "tweet thread", "X thread" | ACTIVE |
| User says "viral thread" or wants multi-tweet content | ACTIVE |
| User wants to share insights, stories, or frameworks on Twitter/X | ACTIVE |
| User wants a TikTok or Reels script | DORMANT — use TikTok Script |
| User wants a newsletter | DORMANT — use Newsletter |

## Common Mistakes

| Mistake | Why It's Wrong |
|---------|---------------|
| "Weak first tweet" | Tweet 1 is your headline. If it doesn't stop the scroll, no one reads tweets 2-15. |
| "Wall of text per tweet" | White space matters. Short lines, line breaks, and punchy sentences get read. |
| "No thread structure" | Random thoughts don't thread well. Use a framework: story, list, or lesson arc. |
| "Forget the CTA" | Every thread should end with a clear ask: follow, retweet, reply, or click. |
| "Post at random times" | Twitter engagement peaks at specific hours. Schedule for your audience's timezone. |

## Protocol

### Step 1: Gather Thread Requirements

If the user hasn't provided details, ask:

> 1. **Topic** — what's the thread about?
> 2. **Angle** — personal story, tactical how-to, hot take, data breakdown, or curated list?
> 3. **Goal** — followers, engagement, traffic to a link, or brand awareness?
> 4. **Length** — short (5-7 tweets), medium (8-12), or long (13-15)?
> 5. **Key points** — what are the 3-5 main takeaways?

### Step 2: Choose Thread Structure

| Structure | Best For | Pattern |
|----------|---------|---------|
| **Story arc** | Personal experience, case study | Setup → Conflict → Turning point → Resolution → Lesson |
| **Listicle** | Tips, tools, resources | Hook → Item 1 → Item 2 → ... → Summary → CTA |
| **Framework** | Teaching a method | Hook → Context → Step 1 → Step 2 → Step 3 → Recap → CTA |
| **Contrarian** | Hot takes, challenging norms | Bold claim → Evidence 1 → Evidence 2 → Nuance → Reframe → CTA |
| **Before/After** | Transformations, results | Old way → Problems → Discovery → New way → Results → CTA |

### Step 3: Write the Hook (Tweet 1)

The hook tweet determines 90% of thread performance.

**Hook formulas:**

| Formula | Template | Example |
|---------|---------|---------|
| **Bold claim** | "[Counter-intuitive statement]:" | "Most marketing advice is wrong:" |
| **Numbered list** | "[X] [things] that [outcome]:" | "7 pricing mistakes that cost me $50K:" |
| **Story opener** | "In [year], I [dramatic situation]." | "In 2023, I almost shut down my startup." |
| **Question** | "Why do [group] always [action]?" | "Why do most SaaS founders underprice?" |
| **Data hook** | "I analyzed [X] and found [surprising result]." | "I analyzed 500 landing pages. Here's what converts:" |
| **Time-based** | "[Time period] ago, I [situation]. Today, [result]." | "6 months ago I had 200 followers. Today: 50K." |

**Hook rules:**
- Maximum 2 lines visible without expanding (keep under 180 characters)
- Create a curiosity gap — make them need to read tweet 2
- End with a colon `:` or "Here's what I learned:" to signal more is coming
- No links in tweet 1 (links reduce reach by 50%+)

### Step 4: Write Body Tweets (2 through N-1)

**Body tweet rules:**
- One idea per tweet (never two concepts in one tweet)
- Use line breaks for readability
- Short sentences. Punchy paragraphs.
- Include a mini-hook every 3-4 tweets to retain scrollers
- Use numbered tweets (`1/`, `2/`) OR natural flow (no numbers) — don't mix

**Formatting patterns:**

```
[Concept tweet]
This is the key insight.

Most people think [common belief].

But the reality is [contrarian truth].

Here's why:
```

```
[Tactical tweet]
Step 3: [Action]

→ Do [specific thing]
→ Then [specific thing]
→ Result: [outcome]

This alone [impressive result].
```

```
[Data tweet]
I tested this on [X samples].

Results:
• [Finding 1]: [XX]%
• [Finding 2]: [XX]%
• [Finding 3]: [XX]%

The winner? [Finding].
```

**Engagement re-hooks (insert at tweets 4, 7, 10):**
- "But here's where it gets interesting:"
- "This next one changed everything:"
- "Most people miss this part:"
- "(save this one)"

### Step 5: Write the Closing CTA (Final Tweet)

**CTA formulas:**

| Goal | CTA Template |
|------|-------------|
| Followers | "Follow me @[handle] for more [topic]. I share [value] every [frequency]." |
| Retweet | "If this was helpful, retweet the first tweet so others can find it." |
| Reply | "What would you add? Drop your best [topic] tip below." |
| Link click | "I wrote a full breakdown here: [link]" |
| Newsletter | "I go deeper on this in my newsletter. Subscribe: [link]" |
| Engagement | "Which of these was most surprising? Reply with the number." |

**CTA rules:**
- ONE primary CTA only (multiple CTAs dilute action)
- If driving to a link, put it in the last tweet (not tweet 1)
- Add the self-retweet ask: "Retweet tweet 1 to help others find this"
- Reply to your own thread with the link (keeps link out of main thread)

### Step 6: Final Polish

**Thread checklist:**
- [ ] Tweet 1 creates a curiosity gap (would YOU click to read more?)
- [ ] Each tweet can stand alone (make sense without surrounding context)
- [ ] No tweet exceeds 280 characters
- [ ] Line breaks and white space make each tweet scannable
- [ ] Engagement re-hooks at tweets 4, 7, and 10
- [ ] CTA in the final tweet is clear and specific
- [ ] No links in tweet 1 (put links in last tweet or reply)
- [ ] Thread length matches content depth (don't pad, don't rush)
- [ ] Read the full thread aloud — does it flow naturally?

**Scheduling strategy:**
- Best times: Weekdays 8-10 AM or 12-1 PM (audience's timezone)
- Best days: Tuesday through Thursday
- Post tweet 1, then unroll the rest within 1-2 minutes
- Self-retweet the thread 6-8 hours later for a second wave

## Output Format

```markdown
# Twitter/X Thread — [Topic]

**Structure:** [Story / Listicle / Framework / etc.]
**Length:** [X] tweets
**Goal:** [Followers / Engagement / Traffic]
**Best posting time:** [Day, Time, Timezone]

## Thread

**Tweet 1 (Hook):**
[Hook tweet — under 180 chars]

**Tweet 2:**
[Body tweet]

**Tweet 3:**
[Body tweet]

[...all tweets...]

**Tweet [N] (CTA):**
[Closing CTA tweet]

**Reply to thread:**
[Link or bonus content — posted as a reply to tweet 1]
```

## Completion

```
Twitter Thread — Complete!

Topic: [Topic]
Structure: [Type]
Length: [X] tweets
Hook type: [Formula used]
CTA: [Primary action]

Next steps:
1. Read the full thread aloud — trim anything that doesn't flow
2. Schedule for [optimal time] using a scheduling tool
3. Self-retweet 6-8 hours after posting
4. Engage with every reply in the first 2 hours (boosts algorithm)
5. Track impressions and engagement rate to learn what works
```

## Level History

- **Lv.1** — Base: 5 thread structures (story, listicle, framework, contrarian, before/after), 6 hook formulas with examples, body tweet formatting patterns, engagement re-hooks, CTA formulas by goal (6 types), scheduling strategy, full thread checklist. (Origin: MemStack Pro v3.2, Mar 2026)
