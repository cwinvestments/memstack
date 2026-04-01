---
name: memstack-content-landing-page-copy
description: "Use this skill when the user says 'write landing page', 'landing page copy', 'sales page', 'hero section', 'conversion copy', or is creating persuasive short-form copy for a product or service landing page. Do NOT use for blog posts or email sequences."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# 🎯 Landing Page Copy — Writing conversion-optimized page copy...
*Produces structured landing page copy blocks — hero, problem, solution, features, social proof, FAQ, CTA — ready to drop into any template or design.*

## Activation

When this skill activates, output:

`🎯 Landing Page Copy — Gathering product and audience details...`

Then execute the protocol below.

| Context | Status |
|---------|--------|
| User says "write landing page" or "landing page copy" | ACTIVE |
| User says "sales page" or "hero section" or "conversion copy" | ACTIVE |
| Creating copy for a product, service, or signup page | ACTIVE |
| Writing blog content (long-form, educational) | DORMANT — use blog-post |
| Writing email copy | DORMANT — use email-sequence |
| Designing the page layout (not writing copy) | DORMANT |

### Anti-patterns

| Trap | Reality Check |
|------|---------------|
| "Describe all the features" | Features tell. Benefits sell. Lead with what the customer gets, not what the product does. |
| "Make the headline clever" | Clever headlines confuse. Clear headlines convert. Clarity beats creativity every time. |
| "Everyone is our audience" | Speaking to everyone means connecting with no one. Pick one persona and write to them. |
| "Long copy won't be read" | Long copy outperforms short copy when every sentence earns the next. Cut filler, not length. |
| "We don't need social proof yet" | No testimonials? Use stats, logos, case study snippets, or "built by" credibility. Something is always better than nothing. |

## Protocol

### Step 1: Gather Product Details

If the user hasn't provided details, ask:

> I need a few details for the landing page:
> 1. **Product/service name** — what are we selling?
> 2. **Target audience** — who is the ideal customer? (role, pain point, situation)
> 3. **Key benefit** — what's the #1 thing they get? (in their words, not yours)
> 4. **Price point** — free, freemium, one-time, subscription? (affects urgency strategy)
> 5. **CTA goal** — what's the primary action? (sign up, buy, book a call, download)
> 6. **Existing copy or brand voice** — any tone/style to match?

### Step 2: Write Hero Section

The hero section determines whether visitors stay or leave. Every word earns its place.

```markdown
## Hero Section

### Headline (10 words max)
[Clear statement of the primary benefit — what they get]

### Subheadline (20 words max)
[Specificity: who it's for, how it works, what makes it different]

### Primary CTA Button
[Action verb + outcome: "Start Free Trial" / "Get Your Report" / "Book a Demo"]

### Supporting text (optional, below CTA)
[Reduce friction: "No credit card required" / "Free for 14 days" / "Setup in 2 minutes"]
```

**Headline formulas:**

| Formula | Example |
|---------|---------|
| [Outcome] Without [Pain] | "Ship Faster Without Breaking Production" |
| [Outcome] for [Audience] | "Beautiful Dashboards for Data Teams" |
| The [Category] That [Difference] | "The CRM That Writes Itself" |
| Stop [Pain]. Start [Benefit]. | "Stop Guessing. Start Knowing." |
| [Number] [Outcome] in [Timeframe] | "10x Revenue in 90 Days" |

**Headline rules:**
- No jargon the visitor wouldn't say out loud
- Specific beats vague ("Save 10 hours/week" beats "Save time")
- One benefit only — trying to say everything says nothing
- If you can add "so what?" and it still makes sense, the headline is too vague

**CTA button rules:**
- Action verb first ("Start," "Get," "Try," "Download" — never "Submit" or "Click Here")
- 2-5 words max
- State the outcome, not the action ("Get My Free Report" not "Download PDF")
- One primary CTA per section — don't split attention

### Step 3: Problem / Agitation Section

Make the reader feel their problem before presenting the solution:

```markdown
## Problem Section

### Section headline
[Name the pain directly: "Tired of [problem]?" / "You know the feeling..."]

### Pain points (3-4 bullet points)
- [Specific frustration they experience daily]
- [Consequence of not solving this problem]
- [The thing they've tried that didn't work]
- [The emotional cost: stress, wasted time, missed opportunities]

### Agitation paragraph
[1-2 sentences amplifying the stakes: what happens if they do nothing?
Paint the future they don't want.]
```

**Problem section rules:**
- Use the reader's own language (words from reviews, support tickets, forums)
- Be specific — "You spend 3 hours every Monday compiling reports" not "Reports take too long"
- Don't insult the reader or their current tools — empathize with their situation
- The problem section ends with the reader thinking "Yes, that's exactly my problem"

### Step 4: Solution Section

Transition from pain to relief. This is where your product enters:

```markdown
## Solution Section

### Transition line
[Bridge from problem to solution: "What if you could..." / "That's why we built..." / "Imagine instead..."]

### Product introduction (2-3 sentences)
[Product name] [does what] for [whom]. [How it solves the problem stated above].
[One sentence about the approach or key differentiator.]

### How it works (3 steps)
1. **[Action verb]** — [Simple first step the user takes]
2. **[Action verb]** — [What happens next / the product's magic moment]
3. **[Action verb]** — [The outcome they get]

### Visual suggestion
[Screenshot, demo GIF, or product illustration showing the solution in action]
```

**Solution section rules:**
- The "how it works" should be 3 steps max — complexity kills conversion
- Each step starts with an action verb
- Show, don't tell — include a visual of the product
- Connect back to the problem: the solution should directly address the pain points listed above

### Step 5: Features with Benefit-Oriented Copy

List features, but lead with the benefit each feature provides:

```markdown
## Features Section

### Section headline
["Everything you need to [outcome]" / "Built for [audience] who [goal]"]

| Benefit (what they get) | Feature (how it works) |
|------------------------|----------------------|
| Never miss a deadline | Automated reminders and milestone tracking |
| See your data clearly | Real-time dashboard with custom views |
| Work from anywhere | Cloud-based with mobile-responsive design |
| Stay secure | End-to-end encryption and SSO |
| Scale without pain | Auto-scaling infrastructure, no DevOps needed |
| Save 10 hours/week | AI-powered automation for repetitive tasks |
```

**Alternative layout (for 3-6 features):**

```markdown
### [Benefit headline]
[1-2 sentences explaining the feature in terms of what the user gains.
Not what it does — what it means for them.]

### [Benefit headline]
[1-2 sentences...]
```

**Feature copy rules:**
- Lead column is the benefit (what they get), second column is the feature (how)
- Write benefits as outcomes: "Never miss a deadline" not "Has reminders"
- Include specific numbers when possible: "Save 10 hours/week" not "Save time"
- 4-6 features is the sweet spot — more than 8 overwhelms, fewer than 3 feels thin
- The most important feature goes first (or at the top-left if using a grid)

### Step 6: Social Proof Section

Build trust with evidence that others have succeeded:

```markdown
## Social Proof Section

### Testimonial template (if real testimonials aren't available yet)
> "[Specific result they achieved] since switching to [Product].
> [What they were doing before and what changed.]
> I'd recommend it to any [target audience descriptor]."
>
> — **[Name]**, [Title] at [Company]

### Stat-based proof (if available)
- **[Number]** [users/companies/projects] trust [Product]
- **[Percentage]%** [improvement metric] on average
- **[Timeframe]** average time to see results

### Trust badges
[Logos of notable customers, media mentions, or certifications]
"Trusted by teams at [Company 1], [Company 2], [Company 3]"

### Case study snippet (if available)
**[Company] increased [metric] by [X]% in [timeframe]**
[2-3 sentences about their situation, what they did, and the result]
[Link: "Read the full case study →"]
```

**Social proof rules:**
- Specific results beat generic praise ("Saved us 15 hours/week" beats "Great product!")
- Include name, title, and company for credibility (anonymous quotes are weak)
- If you don't have testimonials yet, use stats, founding story, or "built by" credibility
- 3 testimonials is the sweet spot — 1 feels cherry-picked, 5+ feels desperate
- Place social proof after features (they've seen what it does, now they need validation)

### Step 7: FAQ Section

Address the top objections that prevent conversion:

```markdown
## FAQ Section

### Section headline
"Questions? We've got answers." / "Common questions"

**Q: [Price objection — "How much does it cost?" / "Is there a free trial?"]**
A: [Direct answer. If there's a free tier, lead with it. Include pricing page link.]

**Q: [Trust objection — "Is my data secure?" / "Who else uses this?"]**
A: [Specific security measures. Customer logos or numbers. Certifications.]

**Q: [Effort objection — "How long does setup take?" / "Do I need technical skills?"]**
A: [Minimize perceived effort. "Setup takes 5 minutes" / "No coding required."]

**Q: [Switching objection — "Can I import my existing data?" / "What about my current tool?"]**
A: [Migration path. Import tools. Compatibility assurances.]

**Q: [Commitment objection — "What if it doesn't work for me?" / "Can I cancel anytime?"]**
A: [Money-back guarantee. No lock-in. Cancel anytime policy.]
```

**FAQ rules:**
- 4-6 questions max on the landing page
- Phrase questions the way a customer would (not formal, not marketing-speak)
- Every answer ends with confidence, not hedging
- The FAQ is really an objection-handling section — structure it that way
- If the same question keeps coming up in sales calls, it belongs here

### Step 8: Final CTA Section

The bottom CTA converts readers who've scrolled the entire page:

```markdown
## Final CTA Section

### Headline
[Restate the primary benefit with urgency: "Ready to [outcome]?"]

### Supporting copy (1-2 sentences)
[Summarize value + reduce risk: "Join [X] teams already [achieving outcome].
Start free — no credit card required."]

### CTA Button
[Same as hero CTA, or stronger: "Start Free Trial" → "Start Your Free Trial Now"]

### Urgency element (use only if genuine)
- Time-limited: "Launch pricing ends [date]"
- Scarcity: "[X] spots remaining this month"
- Social: "[X] teams signed up this week"

### Secondary CTA (optional)
"Not ready yet? [Book a demo / Watch a 2-minute walkthrough / Read our blog]"
```

**Final CTA rules:**
- Don't introduce new information here — reinforce the hero message
- Urgency must be real — fake countdown timers destroy trust
- Always include a secondary/softer CTA for people who aren't ready to commit
- This CTA should be the most visually prominent element below the fold

### Step 9: Output Copy Blocks

Output all sections as clean, structured copy:

```markdown
# Landing Page Copy: [Product Name]

**Target audience:** [persona]
**Primary CTA:** [action]
**Tone:** [casual / professional / bold / etc.]

---

[Hero Section]
[Problem Section]
[Solution Section]
[Features Section]
[Social Proof Section]
[FAQ Section]
[Final CTA Section]

---
```

**Output summary:**

```
🎯 Landing Page Copy — Complete

Product: [name]
Audience: [target persona]
Sections: 7 (Hero, Problem, Solution, Features, Social Proof, FAQ, CTA)
Primary CTA: [button text]
Urgency element: [type or "none"]

Word count: ~[count] words across all sections
Headline: [headline] ([word count] words)

Conversion checklist:
  ✅ Clear headline (under 10 words)
  ✅ Benefit-oriented feature copy
  ✅ Problem/agitation section
  ✅ Social proof (testimonials/stats)
  ✅ Objection handling (FAQ)
  ✅ Single primary CTA throughout
  ✅ Friction reducer (free trial/no CC/guarantee)

Next steps:
1. Review and customize with brand voice
2. Add real testimonials and customer logos
3. Drop copy blocks into your page template
4. A/B test headline variations
```

## Level History

- **Lv.1** — Base: Product detail gathering, hero section (10-word headline, subheadline, CTA), problem/agitation, solution with 3-step process, benefit-oriented features, social proof templates, FAQ objection handling, final CTA with urgency, structured copy blocks. Based on adminstack.pro, ImageStack, and memstack.pro landing pages. (Origin: MemStack Pro v3.2, Mar 2026)
