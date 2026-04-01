---
name: memstack-product-user-story-generator
description: "Use this skill when the user says 'user stories', 'write stories', 'backlog', 'sprint planning', 'acceptance criteria', or needs prioritized stories with Given/When/Then criteria and story point estimates. Do NOT use for full PRDs or detailed feature specs."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# User Story Generator — Generating user stories...
*Produces prioritized user stories with Given/When/Then acceptance criteria, story point estimates, story mapping across epics, and MoSCoW prioritization for sprint planning.*

## Activation

When this skill activates, output:

`User Story Generator — Generating user stories...`

Then execute the protocol below.

## Context Guard

| Context | Status |
|---------|--------|
| User says "user stories", "write stories", "backlog" | ACTIVE |
| User says "sprint planning" or "acceptance criteria" | ACTIVE |
| User wants to break work into estimable, assignable stories | ACTIVE |
| User wants a full product requirements document | DORMANT — use PRD Writer |
| User wants a detailed spec for one feature | DORMANT — use Feature Spec |

## Common Mistakes

| Mistake | Why It's Wrong |
|---------|---------------|
| "As a user, I want the system to..." | Stories describe user needs, not system behavior. The "I want to" should be a user action. |
| "Write a story for every edge case" | Edge cases go in acceptance criteria, not separate stories. One story per user intent. |
| "Stories without acceptance criteria" | "Done" becomes subjective. Every story needs testable criteria before sprint planning. |
| "Estimate in hours" | Hours vary by person. Story points measure relative complexity, not calendar time. |
| "50-point stories in the sprint" | If it's bigger than 8 points, split it. Large stories hide unknowns and block the team. |

## Protocol

### Step 1: Gather Context

If the user hasn't provided details, ask:

> 1. **Feature/epic** — what area are you writing stories for?
> 2. **Personas** — who are the users? (roles, permissions, experience levels)
> 3. **Existing context** — is there a PRD, feature spec, or design to reference?
> 4. **Sprint goal** — what are you trying to ship this sprint?
> 5. **Team capacity** — how many story points can the team handle? (helps scope)

### Step 2: Identify Epics & Themes

Group stories under epics (large bodies of work):

```markdown
## Story Map

### Epic 1: [Epic Name]
**Theme:** [What area of the product this covers]
**Goal:** [What completing this epic achieves]

Stories:
- [ ] US-001: [Story title]
- [ ] US-002: [Story title]
- [ ] US-003: [Story title]

### Epic 2: [Epic Name]
**Theme:** [Theme]
**Goal:** [Goal]

Stories:
- [ ] US-004: [Story title]
- [ ] US-005: [Story title]
```

**Story mapping layout:**

```
            User Journey →
            ┌─────────────────────────────────────────────┐
            │ Step 1      │ Step 2      │ Step 3          │
Epics  ─────┼─────────────┼─────────────┼─────────────────┤
            │ US-001 (M)  │ US-003 (M)  │ US-006 (M)      │ ← Must
            │ US-002 (S)  │ US-004 (S)  │ US-007 (C)      │ ← Should/Could
            │             │ US-005 (C)  │                  │
            └─────────────┴─────────────┴─────────────────┘
```

The top row of each column is the minimum to deliver a working user journey. Everything below is enhancement.

### Step 3: Write User Stories

**Story template:**

```markdown
### US-[ID]: [Short descriptive title]

**As a** [persona/role],
**I want to** [action/capability],
**So that** [benefit/outcome].

**Priority:** [Must / Should / Could / Won't]
**Story points:** [1 / 2 / 3 / 5 / 8]
**Epic:** [Parent epic]
**Dependencies:** [US-XXX or None]

#### Acceptance Criteria

**AC-1: [Happy path]**
Given [precondition]
When [user action]
Then [expected result]

**AC-2: [Validation/error]**
Given [precondition]
When [invalid action or error condition]
Then [error handling behavior]

**AC-3: [Edge case or permission]**
Given [special condition]
When [action]
Then [expected behavior]

#### Notes
- [Design reference, API dependency, or technical consideration]
- [Out of scope for this story: X, Y]
```

**Story writing rules:**
- One user intent per story (splittable, not compound)
- The "so that" must describe a user benefit, not a system behavior
- 2-5 acceptance criteria per story (if you need more, split the story)
- Include at least one error/validation criterion per story
- Stories should be completable within one sprint

### Step 4: Estimate with Story Points

**Fibonacci scale reference:**

| Points | Relative Size | Team Example | Typical Duration |
|--------|-------------|-------------|-----------------|
| **1** | Trivial | Copy change, config update | Hours |
| **2** | Small | Simple UI component, basic CRUD | 0.5-1 day |
| **3** | Medium | Feature with some logic, API integration | 1-2 days |
| **5** | Large | Complex feature, multiple components | 2-4 days |
| **8** | Very large | Multi-system integration, new architecture | 3-5 days |
| **13** | Epic-level | Should be split into smaller stories | Split it |

**Estimation heuristic:**
1. Pick a reference story the team agrees is a "3" (your baseline)
2. Compare each new story: "Is this bigger or smaller than a 3?"
3. Account for: complexity, uncertainty, testing effort, and coordination needed
4. If you can't estimate confidently → add a spike story (time-boxed research)

**Spike story template:**

```markdown
### US-[ID]: [Spike] Investigate [unknown]

**As a** developer,
**I want to** research [technical question or unknown],
**So that** we can estimate and plan [dependent stories].

**Time box:** [X hours/days]
**Output:** Decision document with recommendation

#### Acceptance Criteria
- [ ] [Specific question 1] is answered
- [ ] [Specific question 2] is answered
- [ ] Recommendation documented for team review
```

### Step 5: Prioritize (MoSCoW + Value/Effort)

**MoSCoW assignment:**

| Priority | Stories | Rationale |
|----------|---------|-----------|
| **Must** | US-001, US-003, US-006 | Product doesn't function without these |
| **Should** | US-002, US-004 | Important for good experience, not blocking |
| **Could** | US-005, US-007 | Nice to have, include if sprint has capacity |
| **Won't** | US-008 | Deferred to future sprint |

**Value/Effort matrix:**

```
             High Value
                │
    Quick Wins  │  Strategic
    (Do first)  │  (Plan carefully)
────────────────┼────────────────
    Fill-ins    │  Avoid (for now)
    (If time)   │  (High cost, low reward)
                │
             Low Value

      Low Effort ──────── High Effort
```

Place each story on the matrix. Sprint should be loaded with Quick Wins and Strategic items.

### Step 6: Organize Sprint Backlog

**Sprint planning output:**

```markdown
## Sprint [X] Backlog — [Sprint Goal]

**Capacity:** [X] story points
**Duration:** [2 weeks]
**Sprint goal:** [One sentence: what we're shipping]

### Committed Stories

| ID | Story | Points | Priority | Assignee | Dependencies |
|----|-------|--------|----------|----------|-------------|
| US-001 | [Title] | 3 | Must | [Name] | None |
| US-003 | [Title] | 5 | Must | [Name] | US-001 |
| US-002 | [Title] | 2 | Should | [Name] | None |
| US-004 | [Title] | 3 | Should | [Name] | US-003 |
| **Total** | | **13** | | | |

### Stretch Goals (if capacity)
| US-005 | [Title] | 2 | Could | — | None |

### Not This Sprint
| US-008 | [Title] | 8 | Won't | — | Needs design |
```

**Sprint planning rules:**
- Total committed points should not exceed team velocity
- Must stories go in first, then Should, then Could
- Respect dependency order (don't commit US-003 without US-001)
- Leave 10-20% buffer for bugs, reviews, and unexpected work

## Output Format

```markdown
# User Stories — [Feature/Epic Name]

## Story Map
[Epic/theme overview from Step 2]

## Stories

### US-001: [Title]
[Full story from Step 3]

### US-002: [Title]
[Full story from Step 3]

[... all stories ...]

## Prioritization
[MoSCoW table from Step 5]
[Value/Effort matrix placement]

## Sprint Backlog
[Sprint planning table from Step 6]

## Definition of Done
- [ ] Code complete and reviewed
- [ ] Unit tests passing
- [ ] Acceptance criteria verified
- [ ] No regressions in existing tests
- [ ] Deployed to staging environment
```

## Completion

```
User Story Generator — Complete!

Epics: [Count]
Total stories: [Count]
Must-have: [Count] ([X] points)
Should-have: [Count] ([X] points)
Could-have: [Count] ([X] points)
Total story points: [X]
Sprint capacity needed: [X sprints]

Next steps:
1. Review stories with the team (estimation poker)
2. Validate acceptance criteria with QA
3. Resolve any dependency blockers
4. Commit to Sprint [X] backlog
5. Create tasks/subtasks in project management tool
```

## Level History

- **Lv.1** — Base: Epic/theme identification, story map layout, story template (As a/I want to/So that), Given/When/Then acceptance criteria, Fibonacci story points with estimation heuristic, spike story template, MoSCoW prioritization, value/effort matrix, sprint backlog organization with capacity planning, definition of done checklist. (Origin: MemStack Pro v3.2, Mar 2026)
