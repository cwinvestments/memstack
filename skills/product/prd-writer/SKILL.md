---
name: memstack-product-prd-writer
description: "Use this skill when the user says 'PRD', 'product requirements', 'requirements document', or needs a complete engineering-ready PRD with problem statement, personas, MoSCoW features, and success metrics. Do NOT use for single feature specs or user story backlogs."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# PRD Writer — Writing product requirements document...
*Generates a complete engineering-ready PRD with problem statement, user personas, functional and non-functional requirements, MoSCoW prioritization, success metrics, and implementation timeline.*

## Activation

When this skill activates, output:

`PRD Writer — Writing product requirements document...`

Then execute the protocol below.

## Context Guard

| Context | Status |
|---------|--------|
| User says "PRD", "product requirements", "requirements document" | ACTIVE |
| User wants a full product spec for engineering handoff | ACTIVE |
| User is planning a new product or major feature set | ACTIVE |
| User wants a spec for ONE feature | DORMANT — use Feature Spec |
| User wants user stories for sprint planning | DORMANT — use User Story Generator |

## Common Mistakes

| Mistake | Why It's Wrong |
|---------|---------------|
| "Start with the solution" | Start with the problem. Requirements without clear problems lead to building the wrong thing. |
| "List every possible feature" | A PRD with 50 features is a wish list, not a plan. MoSCoW forces hard trade-offs. |
| "Skip non-functional requirements" | Performance, security, and scalability are invisible until they break. Spec them upfront. |
| "No success metrics" | Without measurable outcomes, you can't tell if the product succeeded. Define metrics before building. |
| "Write it alone" | PRDs need input from engineering, design, and stakeholders. Write the draft, then review together. |

## Protocol

### Step 1: Gather Product Context

If the user hasn't provided details, ask:

> 1. **Product name** — what are you building?
> 2. **Problem statement** — what problem does this solve? For whom?
> 3. **Target users** — who are the primary and secondary users?
> 4. **Business context** — why now? What's the opportunity?
> 5. **Scope** — is this a new product, a major feature set, or a v2?
> 6. **Constraints** — timeline, budget, team size, tech stack?

### Step 2: Write Problem Statement

**Problem statement template:**

```markdown
## Problem Statement

### The Problem
[Target users] struggle with [specific problem].

Currently, they [workaround or current behavior], which results in
[negative consequences: wasted time, lost revenue, frustration, errors].

### Evidence
- [Data point 1: user research, support tickets, survey results]
- [Data point 2: market data, competitor traction, industry trends]
- [Data point 3: internal metrics showing the gap]

### Impact
If unsolved, this problem costs [users/business] approximately
[quantified impact: time, money, churn rate, opportunity cost].

### Opportunity
By solving this problem, we can [positive outcome for users]
and [positive outcome for the business: revenue, retention, growth].
```

**Problem statement rules:**
- Be specific — "Users struggle with X" not "The experience could be better"
- Include evidence — data, quotes, or research that proves the problem exists
- Quantify the impact — makes prioritization decisions easier
- Separate the problem from the solution (no feature names here)

### Step 3: Define User Personas

Create 2-3 personas (no more):

**Persona template:**

```markdown
### Persona: [Name] — [Role/Title]

**Demographics:** [Age range, job title, company size, tech savviness]

**Goals:**
1. [Primary goal — what they're trying to achieve]
2. [Secondary goal]

**Pain points:**
1. [Frustration 1 — related to the problem statement]
2. [Frustration 2]
3. [Frustration 3]

**Current behavior:**
- Currently uses [tool/process] to [accomplish task]
- Spends [X hours/week] on [manual process]
- Workaround: [How they hack around the limitation]

**Success criteria:**
- This persona succeeds when they can [measurable outcome]

**Quote:** "[A sentence that captures their frustration in their own words]"
```

**Persona rules:**
- Primary persona: The person the product is primarily designed for (gets priority in trade-offs)
- Secondary persona: Benefits from the product but doesn't drive design decisions
- Anti-persona: Who this product is NOT for (prevents scope creep)

### Step 4: List Requirements (MoSCoW)

**Functional requirements:**

| ID | Requirement | Priority | Persona | Notes |
|----|------------|----------|---------|-------|
| FR-001 | [User can do X] | Must | [Persona] | [Context] |
| FR-002 | [System does Y when Z] | Must | [Persona] | [Context] |
| FR-003 | [User can configure W] | Should | [Persona] | [Context] |
| FR-004 | [System supports V] | Could | [Persona] | [Context] |
| FR-005 | [User can do U] | Won't (this version) | [Persona] | [Context] |

**MoSCoW definitions:**

| Priority | Meaning | Rule of Thumb |
|----------|---------|--------------|
| **Must** | Product doesn't work without it | 60% of effort |
| **Should** | Important but not blocking launch | 20% of effort |
| **Could** | Nice to have, include if time allows | 15% of effort |
| **Won't** | Explicitly out of scope for this version | 5% (spec only, don't build) |

**Non-functional requirements:**

| ID | Category | Requirement | Target |
|----|----------|------------|--------|
| NFR-001 | Performance | Page load time | <2 seconds (p95) |
| NFR-002 | Performance | API response time | <500ms (p95) |
| NFR-003 | Scalability | Concurrent users | [X] users |
| NFR-004 | Availability | Uptime SLA | 99.9% |
| NFR-005 | Security | Authentication | [Method: OAuth, JWT, etc.] |
| NFR-006 | Security | Data encryption | At rest + in transit |
| NFR-007 | Accessibility | WCAG compliance | Level AA |
| NFR-008 | Compatibility | Browser support | [List of browsers] |
| NFR-009 | Data | Backup frequency | [Daily/hourly] |
| NFR-010 | Compliance | Regulations | [GDPR, SOC 2, HIPAA, etc.] |

**Requirement writing rules:**
- Each requirement should be testable (you can verify it's done)
- Use "User can [action]" or "System [behavior] when [condition]"
- Never combine two requirements in one row
- Include "Won't" items explicitly — prevents scope creep conversations later

### Step 5: Define User Flows

For each Must requirement, document the primary user flow:

**User flow template:**

```markdown
### Flow: [Action Name]

**Trigger:** [What initiates this flow]
**Actor:** [Which persona]
**Preconditions:** [What must be true before this flow starts]

**Happy path:**
1. User [action]
2. System [response]
3. User [action]
4. System [response]
5. User sees [outcome/confirmation]

**Error states:**
- If [condition], show [error message] and [recovery action]
- If [condition], redirect to [fallback]

**Edge cases:**
- [Edge case 1: what happens when...]
- [Edge case 2: what happens when...]
```

### Step 6: Define Success Metrics

| Metric | Current | Target | Timeframe | How to Measure |
|--------|---------|--------|-----------|---------------|
| [Primary metric — e.g., conversion rate] | [X]% | [Y]% | [90 days] | [Analytics tool] |
| [Secondary metric — e.g., time-on-task] | [X min] | [Y min] | [90 days] | [Analytics tool] |
| [Business metric — e.g., revenue impact] | $[X] | $[Y] | [6 months] | [Revenue dashboard] |
| [User satisfaction — e.g., NPS] | [X] | [Y] | [90 days] | [Survey tool] |

**Metric rules:**
- 1 primary metric (the North Star for this product/feature)
- 2-3 secondary metrics (supporting indicators)
- 1 guardrail metric (something that must NOT get worse — e.g., page load time)
- All metrics must have current baselines and targets with timeframes

### Step 7: Outline Timeline & Dependencies

**Phase breakdown:**

| Phase | Scope | Duration | Dependencies |
|-------|-------|----------|-------------|
| Phase 1: Foundation | Must-have features only | [X weeks] | [None / design complete / API ready] |
| Phase 2: Enhancement | Should-have features | [X weeks] | Phase 1 complete |
| Phase 3: Polish | Could-have features + optimization | [X weeks] | Phase 2 complete |

**Key dependencies:**
- [ ] [Dependency 1: Design mockups for [flow] — needed by [date]]
- [ ] [Dependency 2: API endpoint from [team] — needed by [date]]
- [ ] [Dependency 3: Third-party integration approval — needed by [date]]

**Risks:**

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|-----------|
| [Risk 1] | High/Med/Low | High/Med/Low | [Mitigation strategy] |
| [Risk 2] | High/Med/Low | High/Med/Low | [Mitigation strategy] |

## Output Format

```markdown
# PRD: [Product Name]

**Author:** [Name]
**Date:** [Date]
**Version:** [1.0]
**Status:** [Draft / In Review / Approved]

## 1. Problem Statement
[From Step 2]

## 2. User Personas
[From Step 3]

## 3. Requirements
### 3.1 Functional Requirements
[MoSCoW table from Step 4]
### 3.2 Non-Functional Requirements
[NFR table from Step 4]

## 4. User Flows
[From Step 5]

## 5. Success Metrics
[From Step 6]

## 6. Timeline & Dependencies
[From Step 7]

## 7. Open Questions
[Anything unresolved that needs stakeholder input]

## 8. Appendix
[Wireframes, research data, competitive context]
```

## Completion

```
PRD Writer — Complete!

Product: [Name]
Problem: [One-line summary]
Personas: [Count]
Must-have requirements: [Count]
Total requirements: [Count]
Phases: [Count]
Estimated timeline: [X weeks]

Next steps:
1. Review with engineering for feasibility and estimates
2. Review with design for user flow validation
3. Get stakeholder sign-off on MoSCoW priorities
4. Break Phase 1 "Must" requirements into user stories (use User Story Generator)
5. Schedule kickoff meeting
```

## Level History

- **Lv.1** — Base: Problem statement template with evidence/impact/opportunity, persona template (goals, pains, behaviors, quote), MoSCoW functional requirements table, non-functional requirements (10 categories), user flow template with error states and edge cases, success metrics with baselines/targets/timeframes, phased timeline with dependencies and risk matrix. (Origin: MemStack Pro v3.2, Mar 2026)
