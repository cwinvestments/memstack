---
name: memstack-product-roadmap-builder
description: "Use this skill when the user says 'roadmap', 'product roadmap', 'quarterly plan', 'now/next/later', 'OKRs', or needs strategic planning with themes, milestones, resource allocation, and stakeholder-ready views. Do NOT use for MVP scoping or sprint-level planning."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# Roadmap Builder — Building product roadmap...
*Creates a strategic product roadmap in Now/Next/Later format with quarterly themes, milestones, dependency mapping, resource allocation, and stakeholder communication templates.*

## Activation

When this skill activates, output:

`Roadmap Builder — Building product roadmap...`

Then execute the protocol below.

## Context Guard

| Context | Status |
|---------|--------|
| User says "roadmap", "product roadmap", "quarterly plan" | ACTIVE |
| User says "now/next/later" or "OKRs" | ACTIVE |
| User wants to plan product direction for 3-12 months | ACTIVE |
| User wants to scope an MVP | DORMANT — use MVP Scoper |
| User wants sprint-level stories | DORMANT — use User Story Generator |

## Common Mistakes

| Mistake | Why It's Wrong |
|---------|---------------|
| "Roadmap with exact delivery dates" | Dates become promises. Use time horizons (Now/Next/Later) to preserve flexibility. |
| "Feature list disguised as a roadmap" | Roadmaps communicate outcomes and themes, not feature checklists. |
| "One roadmap for everyone" | Engineering, sales, and executives need different views of the same plan. |
| "Plan 12 months in detail" | Detailed plans beyond 3 months are fiction. Be specific for Now, directional for Later. |
| "Set it and forget it" | Roadmaps are living documents. Review and adjust monthly or quarterly. |

## Protocol

### Step 1: Gather Strategic Context

If the user hasn't provided details, ask:

> 1. **Product** — what product are you roadmapping?
> 2. **Current state** — what's been built? What's the current version?
> 3. **Company goals** — what's the business trying to achieve this year?
> 4. **User feedback** — what are the top 5 user requests or complaints?
> 5. **Competitive pressure** — what are competitors shipping that matters?
> 6. **Resources** — team size, key constraints, upcoming changes?

### Step 2: Define Strategic Themes

Themes are the "why" behind your roadmap — outcomes, not features.

**Theme template:**

```markdown
### Theme: [Theme Name]

**Outcome:** [What success looks like — measurable]
**Time horizon:** [Now / Next / Later]
**Business driver:** [Revenue / Retention / Acquisition / Efficiency]
**Key metric:** [Specific metric this theme moves]

**Initiatives under this theme:**
1. [Initiative A — concrete work that delivers on this theme]
2. [Initiative B]
3. [Initiative C]
```

**Example themes (not features):**
- "Reduce time-to-first-value" (not "Add onboarding wizard")
- "Expand to mid-market" (not "Build SSO and audit logs")
- "Increase weekly engagement" (not "Add notifications and dashboards")

**Recommended: 3-5 themes per quarter.** More than 5 means you're spreading too thin.

### Step 3: Build Now/Next/Later Roadmap

| Horizon | Timeframe | Certainty | Detail Level |
|---------|----------|-----------|-------------|
| **Now** | This quarter (0-3 months) | High (committed) | Specific features with milestones |
| **Next** | Next quarter (3-6 months) | Medium (planned) | Themes and initiatives |
| **Later** | 6-12 months | Low (exploratory) | Themes and direction only |

**Roadmap template:**

```markdown
## Now (Q[X] [Year]) — [Quarter Theme]

### Theme 1: [Theme Name]
| Initiative | Description | Owner | Target | Status |
|-----------|------------|-------|--------|--------|
| [Initiative A] | [What it delivers] | [Team/person] | [Month] | [Not started / In progress / Done] |
| [Initiative B] | [What it delivers] | [Team/person] | [Month] | [Status] |

### Theme 2: [Theme Name]
| Initiative | Description | Owner | Target | Status |
|-----------|------------|-------|--------|--------|
| [Initiative C] | [What it delivers] | [Team/person] | [Month] | [Status] |

---

## Next (Q[X+1] [Year]) — [Quarter Theme]

### Theme 3: [Theme Name]
- [Initiative D] — [One-line description]
- [Initiative E] — [One-line description]

### Theme 4: [Theme Name]
- [Initiative F] — [One-line description]

---

## Later ([Year] H2) — [Direction]

### Theme 5: [Theme Name]
- [Exploratory direction 1]
- [Exploratory direction 2]
```

### Step 4: Map Dependencies

```markdown
## Dependency Map

| Initiative | Depends On | Blocks | Risk Level |
|-----------|-----------|--------|-----------|
| [Initiative A] | None (can start immediately) | [Initiative C] | Low |
| [Initiative B] | [External: design system v2] | None | Medium |
| [Initiative C] | [Initiative A] + [API team delivery] | [Initiative E] | High |
```

**Dependency visualization:**

```
Initiative A ──→ Initiative C ──→ Initiative E
                      ↑
Initiative B ─────────┘ (also needs API team delivery)

Critical path: A → C → E (any delay cascades)
```

**Dependency rules:**
- Highlight the critical path — the longest chain of dependent work
- Flag external dependencies (other teams, vendors, regulatory) as high risk
- If an initiative has 3+ dependencies, consider splitting it or re-sequencing

### Step 5: Allocate Resources

**Team allocation by theme:**

| Theme | Engineering | Design | % of Capacity |
|-------|-----------|--------|--------------|
| [Theme 1] | [X] devs | [X] designers | [X]% |
| [Theme 2] | [X] devs | [X] designers | [X]% |
| Tech debt / maintenance | [X] devs | — | 15-20% |
| Bug fixes / support | [X] devs | — | 10% |
| **Total** | | | **100%** |

**Allocation rules:**
- Reserve 15-20% for tech debt (skip this and velocity drops over time)
- Reserve 10% for unplanned bugs and support escalations
- No theme should get less than 20% (or it won't make meaningful progress)
- One team shouldn't work on more than 2 themes simultaneously

### Step 6: Define Milestones & OKRs

**Quarterly OKRs:**

```markdown
## Q[X] Objectives & Key Results

### Objective 1: [Outcome statement — inspirational but measurable]
- KR1: [Metric] from [current] to [target]
- KR2: [Metric] from [current] to [target]
- KR3: [Metric] from [current] to [target]

### Objective 2: [Outcome statement]
- KR1: [Metric] from [current] to [target]
- KR2: [Metric] from [current] to [target]
```

**Milestone timeline:**

| Milestone | Date | Owner | Definition of Done |
|-----------|------|-------|-------------------|
| [Milestone 1] | [Date] | [Team] | [What "done" means — specific, verifiable] |
| [Milestone 2] | [Date] | [Team] | [Definition of done] |
| [Milestone 3] | [Date] | [Team] | [Definition of done] |
| **Quarter review** | [End of quarter] | PM | All OKRs scored, next quarter planned |

**OKR scoring (end of quarter):**
- **0.0-0.3:** Failed — significant miss, understand why
- **0.4-0.6:** Partial — progress made, needs another quarter
- **0.7-1.0:** Success — target met or exceeded
- **Sweet spot: 0.7** — means targets were ambitious but achievable

### Step 7: Create Stakeholder Views

Different audiences need different roadmap views:

**Executive view (1 page):**

```markdown
# Product Roadmap — Q[X]-Q[X+2] [Year]

## Vision: [One-line product vision]

| Quarter | Theme | Key Deliverable | Business Impact |
|---------|-------|----------------|----------------|
| Q[X] | [Theme 1] | [Major deliverable] | [Revenue / retention / efficiency] |
| Q[X] | [Theme 2] | [Major deliverable] | [Business impact] |
| Q[X+1] | [Theme 3] | [Planned direction] | [Expected impact] |
| Q[X+2] | [Theme 4] | [Exploratory] | [Potential impact] |

**Key risks:** [1-2 biggest risks in plain language]
**Resource ask:** [What you need from leadership — headcount, budget, decisions]
```

**Sales/customer view:**

```markdown
# What's Coming — [Product Name]

## Shipping Now (This Quarter)
- [Feature/improvement] — [Customer benefit in their language]
- [Feature/improvement] — [Customer benefit]

## Coming Next
- [Planned initiative] — [Customer benefit]
- [Planned initiative] — [Customer benefit]

## Exploring
- [Direction] — we're researching how to [solve X]
- [Direction] — early exploration of [area]

*Dates and specifics may change. Updated quarterly.*
```

**Engineering view:**

```markdown
# Engineering Roadmap — Q[X]

## Committed Work
| Initiative | Epic | Points | Team | Sprint Target |
|-----------|------|--------|------|--------------|
[Detailed sprint-level breakdown]

## Tech Debt Budget (20%)
| Item | Priority | Effort | Impact |
|------|----------|--------|--------|
[Tech debt items with priority]

## Architecture Decisions Needed
- [Decision 1: by when, who decides]
- [Decision 2: by when, who decides]
```

## Output Format

```markdown
# Product Roadmap — [Product Name]

## Strategic Context
- **Vision:** [One-line vision]
- **Annual goal:** [Primary business goal]
- **Planning period:** Q[X] — Q[X+2] [Year]
- **Team size:** [X engineers, X designers]

## Themes
[From Step 2 — 3-5 themes with outcomes]

## Now/Next/Later Roadmap
[From Step 3 — detailed Now, directional Next, thematic Later]

## Dependencies
[From Step 4 — dependency map with critical path]

## Resource Allocation
[From Step 5 — team allocation by theme]

## OKRs & Milestones
[From Step 6 — quarterly OKRs with milestone timeline]

## Stakeholder Views
### Executive Summary
[1-page executive view]
### Customer-Facing Roadmap
[What's Coming view]
```

## Completion

```
Roadmap Builder — Complete!

Planning horizon: [X quarters]
Themes: [Count]
Now initiatives: [Count] (committed)
Next initiatives: [Count] (planned)
Later directions: [Count] (exploratory)
OKRs: [Count] objectives, [Count] key results
Stakeholder views: 3 (executive, customer, engineering)

Next steps:
1. Review with engineering leads for feasibility
2. Present executive view to leadership for alignment
3. Publish customer-facing roadmap
4. Schedule monthly roadmap review checkpoints
5. Score OKRs at end of quarter and plan next
```

## Level History

- **Lv.1** — Base: Strategic theme definition (outcome-based, not feature-based), Now/Next/Later roadmap format with certainty levels, dependency mapping with critical path, resource allocation with tech debt/bug budget, quarterly OKRs with scoring guide, milestone timeline, 3 stakeholder views (executive, customer, engineering). (Origin: MemStack Pro v3.2, Mar 2026)
