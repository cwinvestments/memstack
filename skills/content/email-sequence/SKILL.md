---
name: memstack-content-email-sequence
description: "Use this skill when the user says 'write email sequence', 'email sequence', 'drip campaign', 'email series', 'nurture sequence', 'onboarding emails', 'launch emails', or is creating a multi-email automated campaign. Do NOT use for newsletters or single marketing emails."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# 📧 Email Sequence — Writing automated email campaign...
*Produces a complete multi-email sequence with subject lines, preview text, body copy, CTAs, and A/B test suggestions — ready to load into any email platform.*

## Activation

When this skill activates, output:

`📧 Email Sequence — Designing email campaign structure...`

Then execute the protocol below.

| Context | Status |
|---------|--------|
| User says "write email sequence" or "email series" or "drip campaign" | ACTIVE |
| User says "nurture sequence" or "onboarding emails" or "launch emails" | ACTIVE |
| Creating a multi-email automated campaign | ACTIVE |
| Writing a single one-off email | DORMANT — just write the email directly |
| Writing newsletter content | DORMANT |
| Writing email for support or personal communication | DORMANT |

### Anti-patterns

| Trap | Reality Check |
|------|---------------|
| "Pitch in the first email" | Email 1 is for trust, not selling. Premature pitching gets unsubscribes, not conversions. |
| "More emails = more sales" | Frequency breeds fatigue. 5 focused emails beat 12 filler emails. Quality per email matters more than quantity. |
| "Long subject lines explain more" | Subject lines are read on mobile. After 50 characters, they're truncated. Short + curious wins. |
| "The body copy needs to be short" | Length doesn't kill — boring does. A 500-word email that's engaging outperforms a 100-word email that's bland. |
| "Everyone gets the same sequence" | Segmentation doubles conversion. At minimum, separate new subscribers from existing customers. |

## Protocol

### Step 1: Gather Campaign Details

If the user hasn't provided details, ask:

> I need a few details for the email sequence:
> 1. **Product/service** — what are you promoting or onboarding for?
> 2. **Target audience** — who receives these emails? (new signups, leads, customers, etc.)
> 3. **Sequence goal** — what's the purpose?
>    - Nurture (build trust over time)
>    - Launch (build anticipation, sell on launch day)
>    - Onboarding (activate new users)
>    - Re-engagement (win back inactive users)
> 4. **Entry trigger** — what puts someone into this sequence? (signup, purchase, abandoned cart, etc.)
> 5. **Existing relationship** — do they already know you, or is this first contact?

### Step 2: Design Sequence Structure

Plan the sequence length and cadence based on the goal:

| Goal | Emails | Cadence | Arc |
|------|--------|---------|-----|
| **Nurture** | 5-7 | Every 2-3 days | Welcome → Story → Value → Value → Soft pitch → Hard pitch → Last chance |
| **Launch** | 4-6 | Daily during launch week | Announcement → Behind-the-scenes → Early access → Launch day → Reminder → Last chance |
| **Onboarding** | 3-5 | Day 0, 1, 3, 7, 14 | Welcome → Quick win → Key feature → Advanced tip → Check-in |
| **Re-engagement** | 3-4 | Every 3-5 days | Miss you → What's new → Special offer → Goodbye (unsubscribe) |

**Sequence map:**

```
Email 1 (Day 0)   → [Welcome/Hook]     — Set expectations, deliver value
     ↓ 2 days
Email 2 (Day 2)   → [Story/Credibility] — Build trust, share journey
     ↓ 2 days
Email 3 (Day 4)   → [Value/Teaching]    — Prove expertise, give actionable tip
     ↓ 3 days
Email 4 (Day 7)   → [Soft Pitch]       — Introduce offer naturally
     ↓ 3 days
Email 5 (Day 10)  → [Hard Pitch]       — Urgency, scarcity, direct CTA
```

Present the sequence map for user approval before writing emails.

### Step 3: Write Email 1 — Welcome / Hook

The first email sets the tone for the entire relationship:

```markdown
## Email 1: Welcome / Hook

**Send:** Immediately upon trigger (Day 0)
**Goal:** Set expectations, deliver promised value, make a first impression
**Tone:** Warm, personal, not salesy

---

**Subject line:** [50 chars max — deliver on signup promise]
**Preview text:** [90 chars max — extends subject line, visible in inbox]

---

Hey [First Name],

[Opening: Thank them for signing up / downloading / purchasing.
Be specific about what they signed up for.]

[Deliver the promised value immediately — if they signed up for a
guide, link it here. If they signed up for a tool, show them the
first step. Never make them wait for what was promised.]

Here's what to expect from me:
- [Frequency]: You'll hear from me [every X days / weekly / etc.]
- [Content type]: I'll share [tips, strategies, behind-the-scenes, etc.]
- [Value promise]: Every email will [teach you something / save you time / etc.]

[One quick win — give them something actionable they can do right now,
in under 5 minutes, that gets a result.]

Talk soon,
[Name]

P.S. [Curiosity hook for Email 2: "Tomorrow, I'll share the story of
how [interesting teaser]..."]

---

**CTA:** [Deliver the lead magnet / Start using the product / Reply to say hello]
```

**Email 1 rules:**
- Deliver what was promised (lead magnet, access, resource) immediately
- Set expectations for frequency and content type
- Include one quick win (builds trust through immediate value)
- P.S. line teases Email 2 (creates anticipation)
- No selling — this email is about trust

### Step 4: Write Email 2 — Story / Credibility

```markdown
## Email 2: Story / Credibility

**Send:** Day 2
**Goal:** Build personal connection, establish credibility through narrative
**Tone:** Conversational, vulnerable, relatable

---

**Subject line:** [50 chars max — hint at a story or revelation]
**Preview text:** [90 chars max]

---

Hey [First Name],

[Opening: Bridge from Email 1 — "Yesterday I shared [X].
Today I want to tell you why I built this / started this / care about this."]

[Story: Share your origin story, a failure that led to insight,
or a customer's transformation story. Structure:]

1. **Situation** — where you/they were before (relatable pain)
2. **Turning point** — what changed (discovery, decision, realization)
3. **Result** — where you/they are now (credibility proof)

[Connect the story to the reader's situation — "I share this because
you're probably in a similar spot. You're dealing with [their pain],
and I know what that feels like."]

[Transition to expertise — "That experience taught me [lesson], and
it's exactly why [product/approach] works the way it does."]

[Name]

P.S. [Tease Email 3: "In my next email, I'll share the exact
[strategy/framework/technique] that made the biggest difference..."]

---

**CTA:** [Soft — reply to share their story / follow on social / read a blog post]
```

### Step 5: Write Email 3 — Value / Teaching

```markdown
## Email 3: Value / Teaching

**Send:** Day 4
**Goal:** Demonstrate expertise by teaching something immediately useful
**Tone:** Expert, generous, practical

---

**Subject line:** [50 chars max — promise a specific takeaway]
**Preview text:** [90 chars max]

---

Hey [First Name],

[Opening: Jump straight into the value — no lengthy preamble.]

Here's [the framework / the technique / the strategy] I promised:

**[Name the framework or technique]**

[Step-by-step breakdown — teach them something they can implement today:]

**Step 1: [Action]**
[1-2 sentences explaining how and why]

**Step 2: [Action]**
[1-2 sentences explaining how and why]

**Step 3: [Action]**
[1-2 sentences explaining how and why]

[Show the result: "When you do this, you'll see [specific outcome].
[Customer name] used this exact approach and [result with numbers]."]

[Bridge to product (subtle): "This is actually one of the core ideas
behind [product] — we built [feature] specifically to make Step 2
automatic."]

[Name]

P.S. [Tease Email 4: "I have something special coming in a few days.
Stay tuned."]

---

**CTA:** [Try the technique / Read the full guide / Watch the tutorial]
```

**Email 3 rules:**
- Teach something genuinely useful — not a watered-down teaser
- Include specific steps, not abstract advice
- One subtle bridge to the product (not a pitch — a connection)
- This email should work as standalone content even without the sequence

### Step 6: Write Email 4 — Soft Pitch

```markdown
## Email 4: Soft Pitch

**Send:** Day 7
**Goal:** Introduce the offer naturally, without pressure
**Tone:** Helpful, confident, low-pressure

---

**Subject line:** [50 chars max — curiosity or question format]
**Preview text:** [90 chars max]

---

Hey [First Name],

[Opening: Reference the value from Email 3 — "Last week I shared
[technique]. Did you try it?"]

[Transition: "A lot of people who try [technique] hit a wall at
[common obstacle]. That's actually why I built [product]."]

Here's what [product] does differently:

- **[Benefit 1]** — [how it solves the obstacle from the teaching email]
- **[Benefit 2]** — [additional value they haven't heard yet]
- **[Benefit 3]** — [outcome with social proof: "[Customer] saw [result]"]

[Soft CTA: "If you're curious, you can [try it free / see it in action /
check out the details] here: [link]"]

[No-pressure close: "No rush — I just wanted you to know it exists.
Either way, I'll keep sharing [value type] with you."]

[Name]

P.S. [Social proof: "[Number] people are already using [product] to
[outcome]. Here's what [Name] said: '[short testimonial]'"]

---

**CTA:** [Check it out / Try free / See pricing — but positioned as optional]
```

### Step 7: Write Email 5 — Hard Pitch

```markdown
## Email 5: Hard Pitch

**Send:** Day 10
**Goal:** Close the sale with urgency and a direct ask
**Tone:** Direct, confident, urgent (but not desperate)

---

**Subject line:** [50 chars max — urgency or FOMO element]
**Preview text:** [90 chars max]

---

Hey [First Name],

[Opening: Direct and honest — "I'll keep this short."]

Over the past [timeframe], I've shared:
- [Email 1 value recap — one line]
- [Email 2 story/lesson recap — one line]
- [Email 3 technique recap — one line]

[Product] is [one-sentence value proposition].

**Here's what you get:**
- [Key benefit 1]
- [Key benefit 2]
- [Key benefit 3]
- [Bonus or guarantee]

[Urgency element — must be genuine:]
- Price increase: "This price goes up to $XX on [date]"
- Limited availability: "Only [X] spots left at this rate"
- Bonus expiration: "The [bonus] is only available until [date]"
- Time-limited offer: "This link expires in 48 hours"

**[CTA button text]: [Link]**

[Risk reversal: "30-day money-back guarantee. If it's not for you,
email me and I'll refund you — no questions asked."]

[Name]

P.S. [Final nudge: "If you've been on the fence, this is the best
time. [Urgency element]. [Link]"]

---

**CTA:** [Buy now / Start now / Claim your spot — direct, urgent, single action]
```

**Email 5 rules:**
- Be direct — the reader has been warmed up over 4 emails
- Recap the value they've received (reciprocity principle)
- Urgency must be genuine — fake scarcity destroys trust permanently
- Include risk reversal (guarantee, free trial, cancel anytime)
- One clear CTA — don't offer alternatives here

### Step 8: Write Subject Line Variants

For each email, provide A/B test options:

```markdown
## A/B Test Suggestions

### Email 1: Welcome
- A: "[Lead magnet name] — your download is inside"
- B: "Welcome! Here's your [promise] + a quick win"

### Email 2: Story
- A: "I almost quit [thing] — here's what saved me"
- B: "The mistake that changed everything"

### Email 3: Value
- A: "The [framework] that [specific result]"
- B: "[Number] steps to [outcome] (takes 10 min)"

### Email 4: Soft pitch
- A: "Quick question about [their pain point]"
- B: "This might help with [obstacle]"

### Email 5: Hard pitch
- A: "Last chance: [offer] ends [date]"
- B: "[First Name], I made you something"
```

**A/B testing rules:**
- Test ONE variable at a time (subject line OR send time, not both)
- Need 1,000+ recipients per variant for statistical significance
- Wait 24-48 hours before declaring a winner
- Winners become the control for the next test

### Step 9: Output Complete Sequence

```markdown
# Email Sequence: [Campaign Name]

**Product:** [name]
**Audience:** [segment]
**Goal:** [nurture / launch / onboarding / re-engagement]
**Entry trigger:** [what puts them in this sequence]
**Cadence:** [X] emails over [Y] days

---

[Email 1 — complete]
[Email 2 — complete]
[Email 3 — complete]
[Email 4 — complete]
[Email 5 — complete]

---

## A/B Test Plan
[Subject line variants per email]

## Platform Setup Notes
- **SendGrid:** Create automation, set delays between emails
- **ConvertKit:** Create sequence, add emails with wait steps
- **Mailchimp:** Create customer journey, add email actions
- Tag subscribers who complete the sequence for next campaign
```

**Output summary:**

```
📧 Email Sequence — Complete

Campaign: [name]
Emails: [count] over [days] days
Goal: [type]
Trigger: [event]

Per-email summary:
  1. Welcome (Day 0) — [subject line]
  2. Story (Day 2) — [subject line]
  3. Value (Day 4) — [subject line]
  4. Soft pitch (Day 7) — [subject line]
  5. Hard pitch (Day 10) — [subject line]

A/B variants: [count] subject line alternatives
Total word count: ~[count] words

Next steps:
1. Customize with brand voice and personal anecdotes
2. Add real customer testimonials to Emails 4-5
3. Set up in your email platform with proper delays
4. Test all links before activating
5. Monitor open rates and click rates for first 2 weeks
```

## Level History

- **Lv.1** — Base: Campaign planning (goal, cadence, arc), 5-email structure (welcome, story, value, soft pitch, hard pitch), subject lines (50 chars), preview text, P.S. lines, A/B test suggestions, platform setup notes, complete sequence output. (Origin: MemStack Pro v3.2, Mar 2026)
