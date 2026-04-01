---
name: memstack-product-feature-spec
description: "Use this skill when the user says 'feature spec', 'spec this feature', 'write a spec', 'functional requirements', or needs a detailed specification for one feature with user flows, edge cases, API definitions, and acceptance criteria. Do NOT use for full PRDs or user story generation."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# Feature Spec — Writing feature specification...
*Creates a detailed specification for a single feature including user story, acceptance criteria, user flows, edge cases, API definitions, dependencies, and effort estimate.*

## Activation

When this skill activates, output:

`Feature Spec — Writing feature specification...`

Then execute the protocol below.

## Context Guard

| Context | Status |
|---------|--------|
| User says "feature spec", "spec this feature", "write a spec" | ACTIVE |
| User says "functional requirements" for a specific feature | ACTIVE |
| User needs a detailed breakdown of ONE feature for engineering | ACTIVE |
| User wants a full product requirements document | DORMANT — use PRD Writer |
| User wants multiple user stories for sprint planning | DORMANT — use User Story Generator |

## Common Mistakes

| Mistake | Why It's Wrong |
|---------|---------------|
| "Spec the happy path only" | Edge cases cause 80% of bugs. Spec them upfront or pay for them in QA. |
| "Skip the API contract" | Frontend and backend need to agree on the contract before building in parallel. |
| "No acceptance criteria" | Without testable criteria, "done" is subjective. Define done before starting. |
| "Spec the UI, not the behavior" | UIs change. Behavior specs survive redesigns. Focus on what happens, not what it looks like. |
| "Forget to list what's out of scope" | Ambiguity invites scope creep. Explicitly list what this feature does NOT include. |

## Protocol

### Step 1: Gather Feature Context

If the user hasn't provided details, ask:

> 1. **Feature name** — what are you building?
> 2. **User problem** — what problem does this feature solve?
> 3. **Target user** — which persona uses this feature?
> 4. **Context** — is this part of a larger project? What already exists?
> 5. **Constraints** — timeline, tech stack, or design constraints?

### Step 2: Write Feature Brief

```markdown
## Feature Brief

**Feature:** [Feature name]
**Owner:** [Product owner / author]
**Date:** [Date]
**Status:** [Draft / In Review / Approved]

### Summary
[2-3 sentences: what this feature does and why it matters]

### User Story
As a [persona], I want to [action] so that [outcome].

### Business Value
- [Why this matters for the business — revenue, retention, efficiency]
- [Metric this feature is expected to move]

### Scope
**In scope:**
- [Specific capability 1]
- [Specific capability 2]
- [Specific capability 3]

**Out of scope:**
- [Explicitly excluded capability 1]
- [Explicitly excluded capability 2]
```

### Step 3: Define User Flows

**Primary flow (happy path):**

```markdown
### Primary Flow: [Action Name]

**Entry point:** [Where/how the user accesses this feature]
**Preconditions:** [What must be true — logged in, has permission, etc.]

1. User [action — clicks, enters, selects]
   → System [response — shows, loads, validates]
2. User [action]
   → System [response]
3. User [action — confirms, submits]
   → System [response — saves, sends, updates]
4. User sees [confirmation — success message, updated state, redirect]

**Exit state:** [What the system looks like after completion]
```

**Alternative flows:**

```markdown
### Alternative Flow: [Variation Name]

**Trigger:** [When this flow happens instead of the primary]

1. [Step that diverges from primary flow]
2. [How the system handles the variation]
3. [Where it rejoins the primary flow, or how it terminates]
```

### Step 4: Document Edge Cases & Error States

| # | Scenario | Expected Behavior | Priority |
|---|----------|-------------------|----------|
| E1 | User submits empty form | Show inline validation errors on required fields | Must handle |
| E2 | Network request fails | Show error toast, preserve form state, offer retry | Must handle |
| E3 | User double-clicks submit | Disable button after first click, prevent duplicate submission | Must handle |
| E4 | Session expires during flow | Save draft state, redirect to login, restore after auth | Should handle |
| E5 | Concurrent edit by another user | Show conflict notification, offer merge or overwrite | Should handle |
| E6 | Input exceeds character limit | Enforce limit in UI, validate server-side, show remaining count | Must handle |
| E7 | User navigates away with unsaved changes | Show "Unsaved changes" confirmation dialog | Should handle |

**Edge case discovery checklist:**
- What happens with empty/null input?
- What happens with maximum-length input?
- What happens with special characters or Unicode?
- What happens if the user has no permission?
- What happens offline or with slow network?
- What happens with concurrent actions?
- What happens if a dependency (API, service) is down?

### Step 5: Define API Contract (if applicable)

```markdown
### API Endpoints

#### POST /api/[resource]
**Purpose:** [What this endpoint does]
**Auth:** Required — [Bearer token / API key / session]
**Rate limit:** [X requests per minute]

**Request:**
```json
{
  "field1": "string (required) — [description]",
  "field2": "number (optional) — [description, default: X]",
  "field3": "enum (required) — [allowed values: a, b, c]"
}
```

**Response (200):**
```json
{
  "id": "string — [description]",
  "field1": "string",
  "createdAt": "ISO 8601 datetime"
}
```

**Error responses:**
| Status | Code | Message | When |
|--------|------|---------|------|
| 400 | VALIDATION_ERROR | "field1 is required" | Missing required field |
| 401 | UNAUTHORIZED | "Authentication required" | No/invalid token |
| 403 | FORBIDDEN | "Insufficient permissions" | User lacks permission |
| 409 | CONFLICT | "Resource already exists" | Duplicate creation |
| 429 | RATE_LIMITED | "Too many requests" | Rate limit exceeded |
```

### Step 6: Write Acceptance Criteria

Use Given/When/Then format for each criterion:

```markdown
### Acceptance Criteria

**AC-1: [Primary happy path]**
Given [precondition]
When [user action]
Then [expected outcome]
And [additional verification]

**AC-2: [Validation]**
Given [precondition]
When [user submits invalid input]
Then [error message] is displayed
And [form state is preserved]

**AC-3: [Permission check]**
Given [user without permission]
When [user attempts action]
Then [access denied response]
And [appropriate error shown]

**AC-4: [Edge case]**
Given [edge condition]
When [action]
Then [graceful handling]
```

**Acceptance criteria rules:**
- Write criteria for EVERY in-scope item (not just the happy path)
- Each criterion must be independently testable
- Include at least one criterion for: happy path, validation, error, and permission
- QA should be able to write test cases directly from these criteria

### Step 7: Estimate Effort & Dependencies

**Effort estimate:**

| Component | Effort | Confidence | Notes |
|-----------|--------|-----------|-------|
| Frontend UI | [X days] | High/Med/Low | [Notes] |
| Backend API | [X days] | High/Med/Low | [Notes] |
| Database changes | [X days] | High/Med/Low | [Notes] |
| Testing (unit + integration) | [X days] | High/Med/Low | [Notes] |
| Code review + QA | [X days] | High/Med/Low | [Notes] |
| **Total** | **[X days]** | | |

**Dependencies:**

| Dependency | Owner | Status | Blocking? |
|-----------|-------|--------|-----------|
| [Design mockups for X] | Design | [Done/In Progress/Not Started] | Yes/No |
| [API from service Y] | Backend team | [Done/In Progress/Not Started] | Yes/No |
| [Third-party SDK setup] | DevOps | [Done/In Progress/Not Started] | Yes/No |

**Technical considerations:**
- [Any architectural decisions needed]
- [Migration requirements]
- [Performance implications]
- [Security considerations]

## Output Format

```markdown
# Feature Spec: [Feature Name]

**Owner:** [Name]
**Date:** [Date]
**Status:** [Draft / In Review / Approved]
**Estimated effort:** [X days]

## 1. Feature Brief
[From Step 2 — summary, user story, scope]

## 2. User Flows
### Primary Flow
[From Step 3]
### Alternative Flows
[From Step 3]

## 3. Edge Cases & Error States
[Table from Step 4]

## 4. API Contract
[From Step 5]

## 5. Acceptance Criteria
[From Step 6]

## 6. Effort & Dependencies
[From Step 7]

## 7. Open Questions
[Anything that needs design, engineering, or stakeholder input]
```

## Completion

```
Feature Spec — Complete!

Feature: [Name]
User story: As a [persona], I want to [action] so that [outcome]
Acceptance criteria: [Count]
Edge cases documented: [Count]
API endpoints: [Count]
Estimated effort: [X days]

Next steps:
1. Review with engineering for technical feasibility
2. Review with design for UX validation
3. Get stakeholder approval on scope
4. Break into tasks/subtasks for sprint planning
5. Write unit tests based on acceptance criteria
```

## Level History

- **Lv.1** — Base: Feature brief template (summary, user story, scope), primary + alternative user flow documentation, edge case table with discovery checklist, API contract template (request, response, errors), Given/When/Then acceptance criteria, effort estimation table with confidence levels, dependency tracking. (Origin: MemStack Pro v3.2, Mar 2026)
