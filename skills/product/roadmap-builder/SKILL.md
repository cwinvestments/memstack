---
name: roadmap-builder
description: "Use when the user says 'roadmap', 'product roadmap', 'feature roadmap', 'quarterly plan', 'now next later', or needs to plan product development across a time horizon."
---


# 🗺️ Roadmap Builder — Strategic Product Roadmap
*Create a now/next/later roadmap with quarterly milestones, resource allocation, and stakeholder-ready presentation.*

## Activation

When this skill activates, output:

`🗺️ Roadmap Builder — Planning your product roadmap...`

| Context | Status |
|---------|--------|
| **User says "roadmap", "product roadmap", "quarterly plan"** | ACTIVE |
| **User wants to plan features across a time horizon** | ACTIVE |
| **User mentions now/next/later or OKRs for product** | ACTIVE |
| **User wants to scope just the MVP** | DORMANT — see mvp-scoper |
| **User wants sprint-level task planning** | DORMANT — see user-story-generator |
| **User wants project task management** | DORMANT — see work skill |

## Protocol

### Step 1: Gather Inputs

Ask the user for:
- **Product vision**: Where is this product going in 12-18 months?
- **Current state**: What exists today? What stage? (MVP, growth, mature)
- **Team capacity**: How many engineers/designers? Full-time or part-time?
- **Time horizon**: 3 months, 6 months, or 12 months?
- **Key constraints**: Technical debt, platform migrations, compliance deadlines?
- **Stakeholder priorities**: What does leadership/board care most about?

### Step 2: Define Themes/Pillars

Organize the roadmap around 3-5 strategic themes:

| Theme | Description | Strategic Goal |
|-------|-------------|---------------|
| **Growth** | Features that acquire new users | Increase MAU by X% |
| **Retention** | Features that keep users coming back | Reduce churn to X% |
| **Revenue** | Features that drive monetization | Reach $X MRR |
| **Platform** | Infrastructure, performance, tech debt | Reduce deploy time to X |
| **Expansion** | New markets, integrations, partnerships | Launch in X market |

Each theme should tie directly to a business metric. No theme exists "because it's interesting."

### Step 3: Map Features to Themes

For each proposed feature:

| Feature | Theme | Impact | Effort | Priority Score |
|---------|-------|--------|--------|---------------|
| [feature] | Growth | High | Medium | 8/10 |
| [feature] | Retention | Medium | Low | 7/10 |
| [feature] | Revenue | High | High | 6/10 |
| [feature] | Platform | Low | High | 3/10 |

**Priority scoring formula:**
- Impact (1-5): How much does this move the theme's metric?
- Confidence (1-5): How sure are we this will work?
- Effort (1-5, inverted): How easy is it to build? (5 = trivial)
- Score = (Impact × Confidence) / Effort

Rank by score. Top items go to "Now."

### Step 4: Quarterly Milestones

Break the time horizon into quarters with concrete deliverables:

```
━━━ Q1: [Quarter Name/Theme] ━━━━━━━━━━━━━
Objective: [what we aim to achieve]
Key Result: [measurable outcome]

Deliverables:
  • [Feature A] — [owner] — [est. weeks]
  • [Feature B] — [owner] — [est. weeks]
  • [Infrastructure work] — [owner] — [est. weeks]

Milestone: By end of Q1, [concrete achievement].

━━━ Q2: [Quarter Name/Theme] ━━━━━━━━━━━━━
Objective: [what we aim to achieve]
Key Result: [measurable outcome]

Deliverables:
  • [Feature C] — [owner] — [est. weeks]
  • [Feature D] — [owner] — [est. weeks]

Milestone: By end of Q2, [concrete achievement].

━━━ Q3-Q4: [Horizon Planning] ━━━━━━━━━━━━
[Less detailed, more directional]
```

Rule: Q1 is detailed, Q2 is planned, Q3+ is directional. Don't fake precision for the future.

### Step 5: Dependencies & Sequencing

Map what blocks what:

```
DEPENDENCY GRAPH:
  [Feature A] ──→ [Feature C] (needs A's data model)
  [Platform work] ──→ [Feature B] (needs new infra)
  [Feature D] ──→ [Feature E] (iterates on D's feedback)

CRITICAL PATH:
  [Platform] → [Feature A] → [Feature C] → [Feature E]
  Duration: ~[X] weeks
  Risk: If platform work slips, everything shifts.
```

Identify the **critical path** — the longest chain of dependent work. This determines your actual timeline.

### Step 6: Resource Allocation

Map team capacity to milestones:

```
── TEAM ALLOCATION ────────────────────────

Q1:
  Engineer 1: Feature A (6 weeks) → Feature B (4 weeks)
  Engineer 2: Platform work (8 weeks) → Bug fixes (2 weeks)
  Designer:   Feature A design (3 weeks) → Feature C design (3 weeks)

Q2:
  Engineer 1: Feature C (6 weeks) → Feature D (4 weeks)
  Engineer 2: Feature D (6 weeks) → Tech debt (4 weeks)
  Designer:   Feature D design (4 weeks) → User research (6 weeks)
```

**Capacity rules:**
- Plan to 70-80% capacity (leave room for bugs, support, unexpected work)
- No person on more than 2 projects per quarter
- Design should lead engineering by 2-4 weeks
- Include dedicated time for tech debt (15-20% of capacity)

### Step 7: Risk Flags & Contingencies

| Risk | Probability | Impact | Contingency |
|------|------------|--------|-------------|
| Key engineer leaves | Low | High | Document decisions, cross-train |
| Scope creep on Feature A | High | Medium | Fixed deadline, cut scope not timeline |
| Dependency on external API | Medium | High | Build abstraction layer, have fallback |
| Customer priorities shift | Medium | Medium | Keep Q3+ flexible, re-prioritize quarterly |
| Technical approach fails | Low | High | Spike/prototype before committing to build |

For each high-impact risk, define a **trigger** (how you'll know it's happening) and **action** (what you'll do).

### Step 8: Stakeholder Communication Format

Present the roadmap in Now/Next/Later view for non-technical stakeholders:

```
━━━ PRODUCT ROADMAP ━━━━━━━━━━━━━━━━━━━━━━

🟢 NOW (This Quarter)
  Committed. In progress or starting soon.
  ├── [Feature A]: [one-line benefit to users]
  ├── [Feature B]: [one-line benefit to users]
  └── [Platform]: [one-line benefit — why it matters]

🟡 NEXT (Next Quarter)
  Planned. High confidence, may shift in scope.
  ├── [Feature C]: [one-line benefit]
  ├── [Feature D]: [one-line benefit]
  └── [Research]: [what we're exploring]

🔵 LATER (Future)
  Directional. Subject to change based on learnings.
  ├── [Feature E]: [one-line vision]
  ├── [Expansion]: [one-line vision]
  └── [Big bet]: [one-line vision]
```

**Communication rules:**
- NOW = commitments (don't include anything you might cut)
- NEXT = plans (signal that scope might change)
- LATER = direction (explicitly say "subject to change")
- Never put dates on LATER items
- Update this view monthly at minimum

### Step 9: Output

Present both views:

```
━━━ PRODUCT ROADMAP: [Product Name] ━━━━━━━
Vision: [one sentence]
Horizon: [X months]
Team: [X engineers, X designers]

── STAKEHOLDER VIEW (Now/Next/Later) ──────
[Now/Next/Later format from Step 8]

── DETAILED QUARTERLY PLAN ────────────────
Q1: [deliverables, owners, milestones]
Q2: [deliverables, owners, milestones]
Q3+: [directional themes]

── THEMES & METRICS ───────────────────────
[theme table with target metrics]

── DEPENDENCIES ───────────────────────────
[dependency graph + critical path]

── RESOURCE ALLOCATION ────────────────────
[team allocation by quarter]

── RISKS ──────────────────────────────────
[risk table with triggers and contingencies]
```

## Inputs
- Product vision (12-18 month)
- Current state and stage
- Team capacity
- Time horizon
- Key constraints and stakeholder priorities

## Outputs
- 3-5 strategic themes tied to business metrics
- Feature-to-theme mapping with priority scores
- Quarterly milestones with deliverables and owners
- Dependency graph with critical path identification
- Resource allocation plan at 70-80% capacity
- Risk flags with triggers and contingency actions
- Now/Next/Later stakeholder-ready view
- Detailed quarterly breakdown

## Level History

- **Lv.1** — Base: Theme-driven roadmap with ICE priority scoring, quarterly milestone planning, dependency graphing with critical path, resource allocation at 70-80% capacity, Now/Next/Later stakeholder format, risk flags with triggers and contingencies. Dual output: stakeholder view + detailed plan. (Origin: MemStack v3.2, Mar 2026)
