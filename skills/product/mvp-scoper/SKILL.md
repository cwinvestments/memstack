---
name: memstack-product-mvp-scoper
description: "Use this skill when the user says 'MVP', 'minimum viable product', 'scope the MVP', 'what should I build first', 'strip to core', or needs to define the smallest build that validates a product hypothesis. Do NOT use for full PRDs or roadmap planning."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# MVP Scoper — Scoping minimum viable product...
*Defines the smallest buildable product that validates a core hypothesis using feature triage, effort/impact scoring, a 2-week sprint scope, and success criteria.*

## Activation

When this skill activates, output:

`MVP Scoper — Scoping minimum viable product...`

Then execute the protocol below.

## Context Guard

| Context | Status |
|---------|--------|
| User says "MVP", "minimum viable product", "scope the MVP" | ACTIVE |
| User says "what should I build first" or "strip to core" | ACTIVE |
| User has an idea and wants to know the smallest thing to build | ACTIVE |
| User wants a full product requirements document | DORMANT — use PRD Writer |
| User wants a roadmap beyond MVP | DORMANT — use Roadmap Builder |

## Common Mistakes

| Mistake | Why It's Wrong |
|---------|---------------|
| "MVP means bad quality" | Minimum viable means minimum scope, not minimum quality. Ship fewer features, but polish them. |
| "Add just one more thing" | Every "one more thing" adds a week. The MVP is a hypothesis test, not a product launch. |
| "Build the whole backend first" | Start with what users see and interact with. Fake the backend if needed (wizard of oz MVP). |
| "Skip the hypothesis" | Without a hypothesis, you're just building. The MVP exists to test ONE assumption. |
| "No success criteria" | How will you know if the MVP worked? Define the test before building. |

## Protocol

### Step 1: Define the Hypothesis

If the user hasn't provided details, ask:

> 1. **Idea** — what are you building? (one paragraph)
> 2. **Target user** — who is the first user? (be specific — not "everyone")
> 3. **Problem** — what painful problem does this solve?
> 4. **Assumption** — what's the riskiest assumption? (the thing that must be true for this to work)
> 5. **Existing alternatives** — how do people solve this today?

**Hypothesis template:**

```markdown
## Core Hypothesis

We believe that [target users]
have a problem with [specific pain point].

If we build [proposed solution],
they will [expected behavior: sign up, pay, use weekly, share].

We will know this is true when [measurable success criteria].

### Riskiest Assumption
[The single assumption that, if wrong, makes the whole product fail]

### How the MVP Tests This
[Specifically how the MVP will validate or invalidate the assumption]
```

### Step 2: List ALL Desired Features

Brain-dump every feature the user imagines, without filtering:

```markdown
## Feature Wish List (Unfiltered)

1. [Feature A]
2. [Feature B]
3. [Feature C]
4. [Feature D]
...
[List everything — the filtering comes next]
```

**Goal:** Get everything out of the user's head so nothing feels "lost." This makes the cutting process psychologically easier.

### Step 3: Score Features (Effort vs Impact)

Rate each feature on two axes:

| Feature | Impact (1-5) | Effort (1-5) | Score | MVP? |
|---------|-------------|-------------|-------|------|
| [Feature A] | 5 | 2 | 2.5 | Yes |
| [Feature B] | 4 | 4 | 1.0 | Maybe |
| [Feature C] | 2 | 5 | 0.4 | No |
| [Feature D] | 5 | 1 | 5.0 | Yes |

**Score = Impact ÷ Effort** (higher is better)

**Impact criteria (how much does this feature validate the hypothesis?):**
- **5:** Directly tests the core hypothesis — users can't use the MVP without it
- **4:** Strongly supports the core experience
- **3:** Nice to have, improves experience but not essential to the test
- **2:** Quality-of-life improvement, not related to core hypothesis
- **1:** Cool idea, but doesn't help validate anything right now

**Effort criteria (how long to build it?):**
- **1:** Hours — trivial implementation
- **2:** 1-2 days — straightforward
- **3:** 3-5 days — moderate complexity
- **4:** 1-2 weeks — significant work
- **5:** 2+ weeks — major undertaking

### Step 4: Apply the MVP Cut

**Three buckets:**

| Bucket | Criteria | Action |
|--------|---------|--------|
| **Core (build)** | Score ≥ 2.0 AND directly tests hypothesis | Include in MVP |
| **Defer (v1.1)** | Score 1.0-2.0 OR supports but doesn't test hypothesis | Build after validation |
| **Cut (maybe never)** | Score < 1.0 OR unrelated to hypothesis | Remove from backlog |

**The 2-week test:**
After bucketing, verify the Core features fit in a 2-week sprint (10 working days):

```markdown
## MVP Scope — 2-Week Build

| Feature | Effort (days) | Notes |
|---------|-------------|-------|
| [Core Feature A] | 2 | [Brief note] |
| [Core Feature B] | 1 | [Brief note] |
| [Core Feature C] | 3 | [Brief note] |
| [Core Feature D] | 2 | [Brief note] |
| Buffer (20%) | 2 | Bugs, blockers, integration |
| **Total** | **10 days** | ✓ Fits in 2-week sprint |
```

**If it doesn't fit in 2 weeks:**
1. Cut the lowest-scoring Core feature
2. Simplify the highest-effort feature (can you build a simpler version?)
3. Consider a different MVP type (see Step 5)

### Step 5: Choose MVP Type

Not every MVP requires writing code:

| MVP Type | Build Time | Best For | What You Learn |
|----------|-----------|---------|---------------|
| **Landing page** | 1-2 days | Validating demand | Do people want this enough to sign up? |
| **Wizard of Oz** | 1-2 weeks | Service-based products | Can you deliver value with manual processes? |
| **Concierge** | 1 week | High-touch products | What does the customer actually need? |
| **Single feature** | 2 weeks | Tool/SaaS products | Does the core mechanic work? |
| **Piecemeal** | 1 week | Marketplace/platform | Can you connect supply and demand? |
| **Video/demo** | 2-3 days | Complex products | Do people understand and want this? |

**Decision tree:**

```
Is the riskiest assumption about DEMAND (will people want this)?
├── Yes → Landing page MVP or Video MVP
│         (Validate demand before building anything)
└── No → Is the riskiest assumption about VALUE (can you deliver)?
    ├── Yes → Wizard of Oz or Concierge MVP
    │         (Deliver value manually, automate later)
    └── No → Is it about USABILITY (can people figure it out)?
        └── Yes → Single Feature MVP or Piecemeal MVP
                  (Build the core mechanic, skip everything else)
```

### Step 6: Define Success Criteria

```markdown
## MVP Success Criteria

### Primary metric (must hit to continue):
- [Metric]: [Target] within [Timeframe]
- Example: "50 signups within 2 weeks of launch"
- Example: "10% of free users convert to paid within 30 days"
- Example: "Users return 3+ times per week"

### Secondary metrics (supporting signals):
- [Metric]: [Target]
- [Metric]: [Target]

### Kill criteria (stop if):
- [Metric] below [threshold] after [timeframe]
- Example: "Fewer than 20 signups after 2 weeks of promotion"
- Example: "Zero paying customers after 30-day free trial"

### What happens next:

| Result | Action |
|--------|--------|
| Hit primary metric | Proceed to v1.1 — add Deferred features |
| Mixed results | Run 2-3 user interviews to understand why. Iterate MVP. |
| Failed kill criteria | Pivot: change target user, problem, or solution |
```

### Step 7: Build the MVP Spec

Assemble the final MVP specification:

```markdown
## Tech Stack Recommendation

| Layer | Recommendation | Rationale |
|-------|---------------|-----------|
| Frontend | [Framework] | [Why — speed, familiarity, ecosystem] |
| Backend | [Framework/service] | [Why] |
| Database | [DB] | [Why] |
| Hosting | [Platform] | [Why — deployment speed, free tier] |
| Auth | [Solution] | [Why] |

### Build vs Buy decisions:
- [Component]: Build / Buy / Skip for MVP
- Auth: Use [Clerk/Supabase Auth/NextAuth] — don't build auth from scratch
- Payments: Use [Stripe] — don't build payment processing
- Email: Use [Resend/SendGrid] — don't build email infrastructure
```

**MVP build rule:** Buy or use existing services for everything except your core differentiator. Only build what makes your product unique.

## Output Format

```markdown
# MVP Scope — [Product Name]

## Hypothesis
[From Step 1]

## Feature Triage

### Core (Build in MVP)
| Feature | Impact | Effort | Days |
[Core features table]

### Deferred (v1.1)
| Feature | Impact | Effort | Rationale |
[Deferred features table]

### Cut
| Feature | Rationale |
[Cut features with brief explanation]

## MVP Type
[Selected type from Step 5 with rationale]

## Build Plan
[2-week schedule from Step 4]

## Success Criteria
[From Step 6]

## Tech Stack
[From Step 7]

## Risks
| Risk | Mitigation |
[Top 3 risks and how to address them]
```

## Completion

```
MVP Scoper — Complete!

Hypothesis: [One-line summary]
MVP type: [Type]
Core features: [Count] ([X days] to build)
Deferred features: [Count]
Cut features: [Count]
Build timeline: [X weeks]
Success metric: [Primary metric + target]

Next steps:
1. Validate the hypothesis with 5 target users before building (show the spec)
2. Set up the tech stack
3. Build Core features in priority order
4. Launch to [initial audience: waitlist, beta group, community]
5. Measure success criteria at [timeframe]
```

## Level History

- **Lv.1** — Base: Hypothesis template with riskiest assumption, feature brain-dump + impact/effort scoring, 3-bucket feature triage (core/defer/cut), 2-week sprint fit test, 6 MVP types with decision tree, success criteria with kill criteria, tech stack recommendation with build/buy guidance. (Origin: MemStack Pro v3.2, Mar 2026)
