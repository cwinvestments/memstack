---
name: user-story-generator
description: "Use when the user says 'user stories', 'write stories', 'backlog', 'story generator', 'acceptance criteria', 'sprint planning', or needs structured user stories for project management tools."
---


# 📝 User Story Generator — Backlog-Ready Story Builder
*Generate prioritized user stories with acceptance criteria, story points, and epic groupings ready for Jira, Linear, or GitHub Projects.*

## Activation

When this skill activates, output:

`📝 User Story Generator — Building your story backlog...`

| Context | Status |
|---------|--------|
| **User says "user stories", "write stories", "backlog"** | ACTIVE |
| **User needs stories for sprint planning** | ACTIVE |
| **User wants acceptance criteria in Given/When/Then** | ACTIVE |
| **User wants a full PRD (stories are one section)** | DORMANT — see prd-writer |
| **User wants a detailed spec for ONE feature** | DORMANT — see feature-spec |

## Protocol

### Step 1: Gather Inputs

Ask the user for:
- **Product/feature context**: What are we writing stories for?
- **User types**: Who are the different users? (e.g., admin, end user, viewer)
- **Scope**: Full product backlog or specific feature area?
- **Sprint duration**: 1 week or 2 weeks? (for story point calibration)
- **Existing context**: PRD, wireframes, or feature list (optional)

### Step 2: Define Personas

For each user type, create a brief persona card:

```
👤 [Persona Name] — [Role]
   Goal: [primary goal]
   Context: [how/when/where they use the product]
   Tech level: [low/medium/high]
```

### Step 3: Generate User Stories by Persona

For each persona, generate stories grouped by functional area:

```
── [Persona Name] Stories ─────────────────

US-001: As a [persona], I want to [action] so that [benefit].
US-002: As a [persona], I want to [action] so that [benefit].
US-003: As a [persona], I want to [action] so that [benefit].
```

Story writing rules:
- Action must be specific and observable ("filter results by date" not "have better search")
- Benefit must explain WHY, not restate the action
- One story = one testable behavior
- If a story needs "and" in the action, split it into two stories

### Step 4: Add Acceptance Criteria

For each story, write 2-4 acceptance criteria in Given/When/Then:

```
US-001: As a [persona], I want to [action] so that [benefit].

  AC-1: Given [precondition]
        When [user action]
        Then [expected result]

  AC-2: Given [edge case condition]
        When [user action]
        Then [expected handling]

  AC-3: Given [error condition]
        When [user action]
        Then [error response]
```

### Step 5: MoSCoW Priority

Assign priority to each story:

| Priority | Meaning | Criteria |
|----------|---------|----------|
| **Must** | Required for launch | Product doesn't work without it |
| **Should** | Expected by users | Important but has workaround |
| **Could** | Nice to have | Enhances experience, not critical |
| **Won't** | Deferred to future | Acknowledged but not in this cycle |

### Step 6: Story Point Estimates

Estimate complexity using Fibonacci scale (1, 2, 3, 5, 8, 13):

| Points | Complexity | Typical Work |
|--------|-----------|--------------|
| **1** | Trivial | Copy change, config update |
| **2** | Simple | Single component, clear implementation |
| **3** | Moderate | Multiple components, some unknowns |
| **5** | Complex | Cross-cutting, integration work |
| **8** | Very complex | Significant unknowns, research needed |
| **13** | Epic-level | Should be broken down further |

Flag any story estimated at 13+ for breakdown.

### Step 7: Group into Epics

Organize stories into epics for sprint planning:

```
━━━ EPIC: [Epic Name] ━━━━━━━━━━━━━━━━━━━━
Description: [what this epic delivers]
Total points: [sum]
Stories: [count]

  US-001 [Must]  (3pts) [story title]
  US-002 [Must]  (2pts) [story title]
  US-003 [Should](5pts) [story title]

━━━ EPIC: [Epic Name] ━━━━━━━━━━━━━━━━━━━━
...
```

Recommended epic size: 13-40 story points (roughly 1-2 sprints).

### Step 8: Identify Dependencies

Map dependencies between stories:

```
DEPENDENCY MAP:
  US-005 → blocks → US-008 (need auth before profile)
  US-003 → blocks → US-012 (need data model before reports)
  US-001 → blocks → US-002, US-003 (foundation story)
```

Flag circular dependencies as risks. Recommend implementation sequence.

**Sprint loading suggestion:**
- Sprint 1: Foundation stories (US-001, US-003, ...) — [X pts]
- Sprint 2: Core features (US-005, US-008, ...) — [X pts]
- Sprint 3: Enhancement stories (US-012, ...) — [X pts]

### Step 9: Output

Present the complete backlog:

```
━━━ USER STORY BACKLOG ━━━━━━━━━━━━━━━━━━━━
Product: [name]
Personas: [count]
Stories: [total count]
Total points: [sum]
Epics: [count]

── PERSONAS ───────────────────────────────
[persona cards]

── EPIC 1: [Name] ─────────────────────────
US-001 [Must] (3pts): As a..., I want..., so that...
  AC-1: Given... When... Then...
  AC-2: Given... When... Then...

US-002 [Must] (2pts): As a..., I want..., so that...
  AC-1: Given... When... Then...
  ...

── EPIC 2: [Name] ─────────────────────────
...

── DEPENDENCIES ───────────────────────────
[dependency map]

── SPRINT SUGGESTION ──────────────────────
Sprint 1: [stories] — [X pts]
Sprint 2: [stories] — [X pts]
Sprint 3: [stories] — [X pts]

── EXPORT FORMAT ──────────────────────────
[CSV or structured format for import]
```

**Export format** (for tool import):

```csv
Epic,Story ID,Title,Description,Priority,Points,Acceptance Criteria
[epic],[id],[title],[full story text],[must/should/could],[pts],[AC text]
```

## Inputs
- Product or feature context
- User types / personas
- Scope (full product or specific area)
- Sprint duration (optional)
- Existing PRD or feature list (optional)

## Outputs
- Persona cards for each user type
- User stories in standard format grouped by persona
- Acceptance criteria in Given/When/Then per story
- MoSCoW priority assignment
- Fibonacci story point estimates
- Epic groupings with point totals
- Dependency map with sprint loading suggestion
- CSV export format for Jira/Linear/GitHub Projects import

## Level History

- **Lv.1** — Base: Persona-grouped story generation, Given/When/Then acceptance criteria, MoSCoW prioritization, Fibonacci story point estimation, epic groupings, dependency mapping with sprint loading, CSV export format for tool import. (Origin: MemStack v3.2, Mar 2026)
