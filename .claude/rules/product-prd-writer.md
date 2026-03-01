---
name: prd-writer
description: "Use when the user says 'PRD', 'product requirements', 'product spec', 'requirements document', 'write a PRD', or needs a structured product requirements document for engineering handoff."
---


# 📋 PRD Writer — Product Requirements Document
*Generate a complete, engineering-ready PRD from problem statement to success metrics.*

## Activation

When this skill activates, output:

`📋 PRD Writer — Drafting your product requirements document...`

| Context | Status |
|---------|--------|
| **User says "PRD", "product requirements", "requirements document"** | ACTIVE |
| **User wants a full product spec for engineering handoff** | ACTIVE |
| **User mentions problem statement + user personas + features** | ACTIVE |
| **User wants a single feature spec (not full product)** | DORMANT — see feature-spec |
| **User wants user stories only** | DORMANT — see user-story-generator |
| **User wants to scope an MVP** | DORMANT — see mvp-scoper |

## Protocol

### Step 1: Gather Inputs

Ask the user for:
- **Product name**: What is this product called?
- **Problem statement**: What problem does it solve? (1-2 sentences)
- **Target user**: Who is the primary user?
- **Success metrics**: How will you know it's working?
- **Timeline**: Target launch date or development window (optional)
- **Existing context**: Any prior docs, wireframes, or research (optional)

### Step 2: Problem Section

Write the problem section with:

**Problem Statement:**
- Clear articulation of the user pain in 2-3 sentences
- Who experiences this pain and how often
- What triggers the pain point

**Current Alternatives:**
| Alternative | How Users Solve It Today | Why It Falls Short |
|-------------|--------------------------|-------------------|
| [Alt 1] | [behavior] | [limitation] |
| [Alt 2] | [behavior] | [limitation] |
| [Alt 3] | [behavior] | [limitation] |

**Cost of Inaction:**
- What happens if this problem isn't solved?
- Quantify where possible (time wasted, revenue lost, churn caused)

### Step 3: User Personas

Define 2-3 user personas:

For each persona:
- **Name & role**: "Sarah, Marketing Manager at a 50-person SaaS company"
- **Goals**: What they're trying to accomplish (3 bullets)
- **Frustrations**: What blocks them today (3 bullets)
- **Technical comfort**: Low / Medium / High
- **Usage frequency**: Daily / Weekly / Monthly
- **Quote**: A fictional but realistic quote capturing their need

### Step 4: Solution Overview

Write a concise solution description:
- **One-liner**: What the product does in one sentence
- **How it works**: 3-5 step user flow at the highest level
- **Key differentiator**: What makes this approach better than alternatives
- **What it is NOT**: Explicitly state what's out of scope

### Step 5: Feature Requirements (MoSCoW)

Prioritize features using MoSCoW:

| Priority | Feature | Description | Persona |
|----------|---------|-------------|---------|
| **Must Have** | [feature] | [what it does] | [who needs it] |
| **Must Have** | [feature] | [what it does] | [who needs it] |
| **Should Have** | [feature] | [what it does] | [who needs it] |
| **Could Have** | [feature] | [what it does] | [who needs it] |
| **Won't Have (v1)** | [feature] | [why deferred] | [who wants it] |

For each Must Have feature, include:
- Brief functional description
- Key user interaction
- Dependencies on other features

### Step 6: User Stories

Write user stories for all Must Have and Should Have features:

```
Epic: [Epic Name]

US-001: As a [persona], I want to [action] so that [benefit].
  Acceptance: [testable criterion]

US-002: As a [persona], I want to [action] so that [benefit].
  Acceptance: [testable criterion]
```

Group stories by epic. Number them for reference.

### Step 7: Success Metrics

Define measurable success criteria:

| Metric | Target | Measurement Method | Timeframe |
|--------|--------|--------------------|-----------|
| DAU/MAU | [number or ratio] | [analytics tool] | [by when] |
| Activation rate | [%] | [what counts as activated] | [by when] |
| Retention (D7/D30) | [%] | [cohort analysis] | [by when] |
| Task completion rate | [%] | [funnel tracking] | [by when] |
| NPS | [score] | [survey cadence] | [by when] |
| Revenue / Conversion | [$] | [billing/analytics] | [by when] |

Include leading indicators (engagement) and lagging indicators (revenue, retention).

### Step 8: Technical Constraints & Assumptions

**Constraints:**
- Platform requirements (web, mobile, both)
- Performance targets (load time, uptime SLA)
- Compliance/security requirements (GDPR, SOC2, etc.)
- Integration requirements (must work with X)
- Browser/device support matrix

**Dependencies:**
- External services or APIs required
- Team/resource dependencies
- Infrastructure prerequisites

**Assumptions:**
- Assumptions about user behavior
- Assumptions about technical feasibility
- Assumptions about market conditions
- What must be true for this PRD to be valid

**Open Questions:**
- Unresolved decisions that need stakeholder input
- Areas requiring further research or validation

### Step 9: Output

Present the complete PRD:

```
━━━ PRODUCT REQUIREMENTS DOCUMENT ━━━━━━━━━
Product: [name]
Version: 1.0
Author: [name]
Date: [date]
Status: Draft

── 1. PROBLEM ─────────────────────────────
[problem statement, alternatives, cost of inaction]

── 2. PERSONAS ────────────────────────────
[2-3 persona profiles]

── 3. SOLUTION OVERVIEW ───────────────────
[one-liner, how it works, differentiator, not-scope]

── 4. REQUIREMENTS ────────────────────────
[MoSCoW feature table]

── 5. USER STORIES ────────────────────────
[stories grouped by epic]

── 6. SUCCESS METRICS ─────────────────────
[metrics table]

── 7. CONSTRAINTS & ASSUMPTIONS ───────────
[technical constraints, dependencies, assumptions, open questions]

── APPENDIX ───────────────────────────────
[wireframes, research links, competitive context]
```

## Inputs
- Product name
- Problem statement
- Target user description
- Success metrics (initial)
- Timeline (optional)
- Existing research or context (optional)

## Outputs
- Complete PRD document with 7 sections
- Problem analysis with current alternatives
- 2-3 user personas with goals and frustrations
- MoSCoW-prioritized feature requirements
- User stories grouped by epic with acceptance criteria
- Success metrics with targets and measurement methods
- Technical constraints, dependencies, and open questions

## Level History

- **Lv.1** — Base: Full PRD generation with problem analysis, user personas, solution overview, MoSCoW feature prioritization, user stories by epic, success metrics framework, technical constraints and assumptions. Engineering-handoff ready format. (Origin: MemStack v3.2, Mar 2026)
