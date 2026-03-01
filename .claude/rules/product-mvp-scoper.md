---
name: mvp-scoper
description: "Use when the user says 'MVP', 'minimum viable product', 'scope the MVP', 'strip to minimum', 'what to build first', or needs to ruthlessly cut a product idea down to its fastest-to-validate form."
---


# 🎯 MVP Scoper — Minimum Viable Product Definition
*Strip a product idea to its core hypothesis, define the smallest build that proves it, and plan the fastest path to validation.*

## Activation

When this skill activates, output:

`🎯 MVP Scoper — Scoping your minimum viable product...`

| Context | Status |
|---------|--------|
| **User says "MVP", "minimum viable product", "scope the MVP"** | ACTIVE |
| **User wants to cut features to build faster** | ACTIVE |
| **User asks "what should I build first?"** | ACTIVE |
| **User wants a full PRD (not just MVP scope)** | DORMANT — see prd-writer |
| **User wants a roadmap beyond MVP** | DORMANT — see roadmap-builder |
| **User wants project tier assessment** | DORMANT — see governor skill |

## Protocol

### Step 1: Gather Inputs

Ask the user for:
- **Product idea**: What do you want to build? (2-3 sentences)
- **Target market**: Who is this for?
- **Timeline constraint**: How fast do you need to ship? (weeks/months)
- **Budget constraint**: Solo dev, small team, or funded team?
- **Validation goal**: What hypothesis are you testing?

### Step 2: Identify Core Value Proposition

Force clarity with the "one sentence" test:

> "[Product] helps [target user] to [solve problem] by [unique mechanism]."

If the user can't fill this in clearly, the idea needs refinement before scoping.

**The Core Loop:**
- What is the ONE action users must take repeatedly?
- What is the ONE outcome that keeps them coming back?
- Strip everything that doesn't serve this loop.

### Step 3: Feature Triage

Take the full feature wishlist and ruthlessly categorize:

| Feature | MVP? | Rationale |
|---------|------|-----------|
| [feature] | ✅ IN | [why it's essential for the hypothesis] |
| [feature] | ❌ OUT | [why it can wait — what workaround exists] |
| [feature] | ❌ OUT | [why it's a nice-to-have, not a must] |
| [feature] | ⚠️ MAYBE | [include only if [condition]] |

**Triage rules:**
- If removing it doesn't prevent the user from getting the core value → OUT
- If it can be done manually instead of automated → OUT (for now)
- If only 1 in 10 users would use it → OUT
- If it requires a new integration or service → OUT (unless it IS the core)
- Auth/login → only if data must persist across sessions
- Admin dashboard → OUT (use database queries)
- Analytics → OUT (use Mixpanel/PostHog free tier)
- Email notifications → OUT (unless core to the loop)

### Step 4: MVP vs V2 Scope

Present a clear boundary:

```
━━━ MVP (Ship This) ━━━━━━━━━━━━━━━━━━━━━━
• [feature 1] — [why essential]
• [feature 2] — [why essential]
• [feature 3] — [why essential]
Hypothesis tested: [what you'll learn]

━━━ V2 (Ship After Validation) ━━━━━━━━━━━
• [feature A] — [trigger: add when X users do Y]
• [feature B] — [trigger: add when retention > Z%]
• [feature C] — [trigger: add when revenue hits $X]

━━━ BACKLOG (Maybe Never) ━━━━━━━━━━━━━━━━
• [feature X] — [only if market demands it]
• [feature Y] — [only if pivot in this direction]
```

Each V2 feature has a **trigger condition** — a specific metric or event that justifies adding it.

### Step 5: Tech Stack Recommendation

Recommend the fastest stack for the constraints:

| Constraint | Recommended Stack | Why |
|-----------|-------------------|-----|
| Solo dev, ship in 2 weeks | Next.js + Supabase + Vercel | Full-stack in one framework, free tier hosting |
| Solo dev, mobile needed | React Native/Expo + Supabase | Cross-platform, rapid iteration |
| Team of 2-3, ship in 4 weeks | Next.js + PostgreSQL + Railway | Scalable from day one |
| Non-technical founder | No-code: Bubble/Softr/Webflow | Ship without engineering |
| API/data product | FastAPI + PostgreSQL + Fly.io | Lightweight, fast to build |

Principles:
- Use what you already know — learning = time
- Managed services over self-hosted — ops overhead kills MVPs
- Free tiers first — don't spend before validating
- Monolith over microservices — always for MVP

### Step 6: Build Estimate

Estimate time and cost:

```
── BUILD ESTIMATE ─────────────────────────

Feature 1: [name]
  Effort: [X days]
  Complexity: [low/med/high]

Feature 2: [name]
  Effort: [X days]
  Complexity: [low/med/high]

Feature 3: [name]
  Effort: [X days]
  Complexity: [low/med/high]

──────────────────────────────────────────
Total dev time: [X days/weeks]
Buffer (1.5x): [X days/weeks]
Realistic ship date: [date]

Cost estimate:
  Hosting: $[X]/mo (free tier if possible)
  Services: $[X]/mo
  Domain: $[X]/yr
  Dev cost: $[X] (if hiring) or $0 (if self)
```

### Step 7: Launch Criteria

Define what "done" means for MVP:

**Launch checklist:**
- [ ] Core loop works end-to-end (user can [action] and get [result])
- [ ] Can onboard a new user in under [X] minutes without help
- [ ] Data doesn't get lost (basic persistence works)
- [ ] Payments work (if monetized from day 1)
- [ ] Landing page exists with clear value proposition
- [ ] At least [X] beta users lined up to try it

**NOT required for launch:**
- [ ] ~~Perfect UI~~ — functional is fine
- [ ] ~~Error handling for every edge case~~ — crash and learn
- [ ] ~~Automated testing~~ — manual testing is fine for MVP
- [ ] ~~CI/CD pipeline~~ — git push to deploy is fine
- [ ] ~~Documentation~~ — the product should be self-explanatory

### Step 8: Risk Assessment

Identify what could invalidate the MVP hypothesis:

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Users don't have this problem | Medium | Fatal | Pre-sell or waitlist validation first |
| Solution too complex to use | Medium | High | User test with 3 people before building |
| Can't build it in time | Low | High | Cut scope further, not timeline |
| Market already saturated | Low | Medium | Find differentiated niche |
| Technical infeasibility | Low | Fatal | Prototype the hardest part first |

**Pre-validation suggestions:**
- Before building: Can you sell it with a landing page and waitlist?
- Before building: Can you deliver the value manually for 5 users?
- Before building: Have 10 people said "I'd pay for this"?

### Step 9: Output

Present the complete MVP scope document:

```
━━━ MVP SCOPE DOCUMENT ━━━━━━━━━━━━━━━━━━━
Product: [name]
One-liner: [value proposition]
Target: [user]
Timeline: [X weeks]

── HYPOTHESIS ─────────────────────────────
We believe [target users] will [use product] because [reason].
We'll know this is true when [measurable signal].

── MVP SCOPE ──────────────────────────────
IN: [feature list with rationale]
OUT: [deferred features with triggers]

── TECH STACK ─────────────────────────────
[recommended stack with justification]

── BUILD PLAN ─────────────────────────────
[feature-by-feature estimate]
Ship date: [date]

── LAUNCH CRITERIA ────────────────────────
[checklist]

── RISKS ──────────────────────────────────
[risk table with mitigations]

── VALIDATION PLAN ────────────────────────
Before build: [pre-validation steps]
After launch: [metrics to watch]
Decision point: [when to persevere, pivot, or kill]
```

## Inputs
- Product idea (2-3 sentences)
- Target market
- Timeline and budget constraints
- Validation goal / hypothesis

## Outputs
- Core value proposition (one sentence)
- Feature triage: IN / OUT / MAYBE with rationale
- MVP vs V2 scope with trigger conditions for V2 features
- Tech stack recommendation for fastest build
- Build estimate with time, cost, and realistic ship date
- Launch criteria checklist
- Risk assessment with mitigations and pre-validation steps

## Level History

- **Lv.1** — Base: Core value proposition forcing function, ruthless feature triage with cut rationale, MVP/V2/backlog scope boundaries with trigger conditions, speed-optimized tech stack recommendations, build estimates, launch criteria, risk assessment with pre-validation steps. (Origin: MemStack v3.2, Mar 2026)
