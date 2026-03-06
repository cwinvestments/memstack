---
name: feature-spec
description: "Use when the user says 'feature spec', 'spec this feature', 'write a spec', 'functional spec', 'technical spec', or needs a detailed specification for a single feature an engineer can implement without ambiguity."
---


# 📐 Feature Spec — Detailed Feature Specification
*Write an unambiguous spec for a single feature covering flows, edge cases, APIs, and acceptance criteria.*

## Activation

When this skill activates, output:

`📐 Feature Spec — Writing your feature specification...`

| Context | Status |
|---------|--------|
| **User says "feature spec", "spec this feature", "write a spec"** | ACTIVE |
| **User needs a detailed specification for ONE feature** | ACTIVE |
| **User mentions functional requirements + edge cases + acceptance criteria** | ACTIVE |
| **User wants a full product PRD (multiple features)** | DORMANT — see prd-writer |
| **User wants user stories only (no technical detail)** | DORMANT — see user-story-generator |

## Protocol

### Step 1: Gather Inputs

Ask the user for:
- **Feature name**: What is this feature called?
- **Parent product**: What product does this belong to?
- **User story**: "As a [user], I want [action] so that [benefit]"
- **Priority**: Must Have / Should Have / Could Have
- **Context**: Any existing specs, designs, or constraints

### Step 2: Functional Requirements

Define what the feature does:

**Overview:**
- One-paragraph description of the feature's purpose and behavior

**Detailed Requirements:**

| ID | Requirement | Details |
|----|-------------|---------|
| FR-01 | [requirement name] | [precise description of behavior] |
| FR-02 | [requirement name] | [precise description of behavior] |
| FR-03 | [requirement name] | [precise description of behavior] |

Rules for writing functional requirements:
- Each requirement is independently testable
- Use precise language: "shall", "must", "when X then Y"
- Avoid ambiguity: no "appropriate", "user-friendly", "fast"
- Include default values and boundary conditions

### Step 3: Non-Functional Requirements

**Performance:**
- Response time targets (e.g., "page loads in < 2s on 3G")
- Throughput requirements (e.g., "handles 100 concurrent users")
- Data volume limits (e.g., "supports up to 10,000 records per query")

**Security:**
- Authentication/authorization requirements
- Data encryption needs (at rest, in transit)
- Input validation and sanitization rules
- Rate limiting requirements

**Accessibility:**
- WCAG compliance level (A, AA, AAA)
- Keyboard navigation requirements
- Screen reader compatibility
- Color contrast minimums

**Compatibility:**
- Browser support matrix
- Mobile responsiveness requirements
- API versioning strategy

### Step 4: User Flow

Map the step-by-step interaction:

```
Step 1: User [action]
  → System [response]
  → UI shows [what the user sees]

Step 2: User [action]
  → System [validation/processing]
  → If success: [result]
  → If failure: [error handling]

Step 3: User [action]
  → System [final processing]
  → UI shows [confirmation/result]
```

Include:
- Entry points (how does the user get to this feature?)
- Happy path (ideal flow)
- Alternative paths (other valid flows)
- Exit points (where does the user go after?)

### Step 5: Edge Cases & Error States

| Scenario | Trigger | Expected Behavior | Error Message |
|----------|---------|-------------------|---------------|
| Empty input | User submits blank form | Inline validation, prevent submit | "This field is required" |
| Invalid data | User enters wrong format | Highlight field, show format hint | "[Field] must be [format]" |
| Duplicate | User creates existing item | Block creation, show existing item | "[Item] already exists" |
| Network failure | Connection lost mid-action | Retry with backoff, show status | "Connection lost. Retrying..." |
| Timeout | Server takes > Xs | Cancel request, offer retry | "Request timed out. Try again." |
| Permission denied | Unauthorized access attempt | Redirect to appropriate view | "You don't have access to this" |
| Concurrent edit | Two users edit same resource | Last-write-wins or merge conflict | "This was updated. Reload?" |
| Data limit | User exceeds quota/limit | Prevent action, show limit info | "Limit reached: [X] of [max]" |

### Step 6: API Requirements (if applicable)

For each endpoint:

```
── ENDPOINT: [Method] /api/v1/[resource] ──

Purpose: [what this endpoint does]
Auth: [required auth level]
Rate limit: [requests per minute]

Request:
  Headers:
    Authorization: Bearer {token}
    Content-Type: application/json

  Body:
    {
      "field1": "string (required, max 255 chars)",
      "field2": "number (optional, default: 0)",
      "field3": "enum: [value1, value2, value3]"
    }

Response (200):
    {
      "id": "string",
      "field1": "string",
      "created_at": "ISO 8601 datetime"
    }

Error Responses:
    400: { "error": "validation_error", "details": [...] }
    401: { "error": "unauthorized" }
    404: { "error": "not_found" }
    429: { "error": "rate_limit_exceeded", "retry_after": 60 }
```

### Step 7: Database Changes

**New Tables:**

```sql
CREATE TABLE [table_name] (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  [column]    [type] [constraints],
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

**Schema Changes to Existing Tables:**

| Table | Change | Column | Type | Notes |
|-------|--------|--------|------|-------|
| [table] | ADD | [column] | [type] | [nullable? default? index?] |
| [table] | MODIFY | [column] | [new type] | [migration strategy] |

**Indexes:**
- [index name]: [columns] — [justification]

**Migration Notes:**
- Backward compatibility considerations
- Data backfill requirements
- Rollback strategy

### Step 8: Acceptance Criteria

Write testable acceptance criteria in Given/When/Then format:

```
AC-01: [Criterion name]
  Given [precondition]
  When [action]
  Then [expected result]
  And [additional verification]

AC-02: [Criterion name]
  Given [precondition]
  When [action]
  Then [expected result]

AC-03: [Criterion name]
  Given [precondition with edge case]
  When [action]
  Then [expected handling]
```

Checklist for completeness:
- [ ] Happy path covered
- [ ] Each edge case has an acceptance criterion
- [ ] Error states have acceptance criteria
- [ ] Performance requirements have acceptance criteria
- [ ] Security requirements have acceptance criteria

### Step 9: Output

Present the complete feature spec:

```
━━━ FEATURE SPECIFICATION ━━━━━━━━━━━━━━━━━
Feature: [name]
Product: [parent product]
Priority: [MoSCoW level]
Author: [name]
Date: [date]

── 1. USER STORY ──────────────────────────
As a [user], I want [action] so that [benefit].

── 2. FUNCTIONAL REQUIREMENTS ─────────────
[requirements table]

── 3. NON-FUNCTIONAL REQUIREMENTS ─────────
[performance, security, accessibility, compatibility]

── 4. USER FLOW ───────────────────────────
[step-by-step interaction map]

── 5. EDGE CASES & ERRORS ─────────────────
[edge case table]

── 6. API REQUIREMENTS ────────────────────
[endpoint definitions]

── 7. DATABASE CHANGES ────────────────────
[schema changes, migrations]

── 8. ACCEPTANCE CRITERIA ─────────────────
[Given/When/Then test cases]
```

## Inputs
- Feature name
- Parent product name
- User story (As a/I want/So that)
- Priority level
- Existing designs, specs, or constraints (optional)

## Outputs
- Functional requirements table with precise descriptions
- Non-functional requirements (performance, security, accessibility)
- Step-by-step user flow with happy and alternative paths
- Edge case and error state matrix
- API endpoint definitions with request/response schemas
- Database schema changes with migration notes
- Acceptance criteria in Given/When/Then format

## Level History

- **Lv.1** — Base: Complete feature specification with functional/non-functional requirements, user flow mapping, edge case matrix, API endpoint definitions, database schema changes, Given/When/Then acceptance criteria. Zero-ambiguity engineering handoff format. (Origin: MemStack v3.2, Mar 2026)
