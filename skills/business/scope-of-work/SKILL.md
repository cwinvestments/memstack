---
name: memstack-business-scope-of-work
description: "Use this skill when the user says 'scope of work', 'SOW', 'define scope', 'project scope', 'write SOW', 'scope document', or is defining project boundaries, deliverables, and acceptance criteria for a formal engagement. Do NOT use for proposals, contracts, or invoicing."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# 📐 Scope of Work — Defining project boundaries and deliverables...
*Generates a formal Scope of Work document with objectives, deliverables, acceptance criteria, in/out scope definitions, work breakdown structure, milestones, and change request process.*

## Activation

When this skill activates, output:

`📐 Scope of Work — Defining project scope and deliverables...`

Then execute the protocol below.

| Context | Status |
|---------|--------|
| User says "scope of work" or "SOW" or "define scope" | ACTIVE |
| User says "write SOW" or "project scope" or "scope document" | ACTIVE |
| Defining formal project boundaries for a client engagement | ACTIVE |
| Writing internal task lists (no formal scope needed) | DORMANT — use Work skill |
| Writing a proposal (includes pricing/sales) | DORMANT — use proposal-writer |

### Anti-patterns

| Trap | Reality Check |
|------|---------------|
| "The scope is obvious from the proposal" | Proposals sell. SOWs define. Same project, different documents, different purpose. |
| "We don't need to list exclusions" | Every scope dispute starts with "I assumed it was included." List what's OUT explicitly. |
| "Acceptance criteria slow us down" | Acceptance criteria prevent "it's not what I wanted" after you've built it. They speed up delivery. |
| "We'll handle changes informally" | Informal changes create informal expectations. Formal change requests protect the timeline and budget. |
| "Dependencies don't matter yet" | Dependencies determine what blocks what. Discovering them mid-project causes delays. Map them upfront. |

## Protocol

### Step 1: Define Project Objectives

Establish what success looks like at the highest level:

```markdown
## 1. Project Objectives

### Primary Objective
[One sentence: what this project delivers and why it matters]

Example: Build a multi-tenant SaaS dashboard that enables [Client]'s customers
to manage their accounts, view analytics, and configure integrations — replacing
the current manual process that requires 3 support staff.

### Success Criteria
| Criteria | Measurement | Target |
|----------|------------|--------|
| Core functionality | All deliverables pass acceptance criteria | 100% |
| Performance | Page load time under 3 seconds | p95 < 3s |
| Reliability | Uptime during business hours | 99.5% |
| User adoption | Active users within 30 days of launch | > 50% of target audience |
| Support reduction | Decrease in support tickets for covered workflows | > 40% reduction |

Success criteria must be **measurable**. "The client is happy" is not a success criterion.
"Support tickets decrease by 40%" is.
```

**Rules:**
- One primary objective, max 2 sentences
- 3-5 measurable success criteria with specific targets
- Criteria should be verifiable by both parties (no subjective measures)

### Step 2: List Deliverables with Acceptance Criteria

Every deliverable needs a clear definition of "done":

```markdown
## 2. Deliverables

### D1: User Authentication System
**Description:** Complete authentication flow including registration, login, password reset, and OAuth integration with Google.

**Acceptance criteria:**
- [ ] Users can register with email and password
- [ ] Users can log in with email/password and receive a session token
- [ ] Users can reset their password via email link
- [ ] Users can log in with Google OAuth
- [ ] Invalid credentials return appropriate error messages
- [ ] Session expires after 24 hours of inactivity
- [ ] All auth endpoints have rate limiting (5 attempts per 15 minutes)

**Depends on:** None (first deliverable)
**Estimated effort:** 20 hours

---

### D2: Admin Dashboard
**Description:** Administrative interface for managing users, viewing analytics, and configuring system settings.

**Acceptance criteria:**
- [ ] Dashboard loads within 3 seconds on standard broadband
- [ ] Displays active user count, revenue metrics, and system health
- [ ] User management: view, search, edit roles, deactivate accounts
- [ ] Data refreshes automatically every 60 seconds
- [ ] Responsive layout works on desktop (1024px+) and tablet (768px+)
- [ ] Role-based access: admin sees all, manager sees their org only

**Depends on:** D1 (Authentication)
**Estimated effort:** 32 hours

---

### D3: [Next Deliverable]
...
```

**Acceptance criteria rules:**
- Each criterion is a binary yes/no check — not subjective ("looks good")
- Include functional requirements (what it does)
- Include non-functional requirements (performance, responsiveness, accessibility)
- Include negative cases (error handling, invalid input)
- Number deliverables (D1, D2, D3) for easy reference in change requests

### Step 3: Define In-Scope and Out-of-Scope

This section prevents scope disputes. Be exhaustive on exclusions:

```markdown
## 3. Scope Definition

### In Scope
| Item | Details |
|------|---------|
| User authentication | Registration, login, password reset, Google OAuth |
| Admin dashboard | User management, analytics display, system settings |
| API development | RESTful endpoints for all dashboard operations |
| Database design | Schema, migrations, seed data, RLS policies |
| Deployment | Railway (backend) + Netlify (frontend), CI/CD pipeline |
| Testing | Unit tests for critical paths, integration tests for API |
| Documentation | API docs, deployment guide, user manual |
| Post-launch support | 30-day bug fix window (Standard tier) |

### Out of Scope
| Item | Rationale | If Needed Later |
|------|-----------|----------------|
| Mobile application | Not required for MVP; web app is responsive | Can be added via Change Request |
| Content creation | Client provides all copy, images, and branding | Content services available separately |
| Email marketing | No email campaigns or newsletter integration | Recommend Mailchimp integration post-launch |
| Payment processing | No billing or payment features in this phase | Phase 2 scope, separate SOW |
| Data migration | No import of existing data from legacy systems | Can be scoped as separate project |
| SEO optimization | Beyond basic meta tags and semantic HTML | SEO audit available as add-on |
| Accessibility audit | WCAG compliance testing by third party | Recommend post-launch audit |
| Browser support | IE11 or older browsers | Modern browsers only (Chrome, Firefox, Safari, Edge) |
| Load testing | Stress testing beyond normal usage patterns | Recommend before scaling |

### Assumptions
| # | Assumption | Impact if Wrong |
|---|-----------|----------------|
| A1 | Client provides branding assets (logo, colors, fonts) by kickoff | Delays Phase 2 by duration of delay |
| A2 | Client designates one decision-maker for feedback | Multiple reviewers slow approval cycles |
| A3 | Existing API documentation is accurate and current | Additional discovery time needed |
| A4 | Production hosting costs are paid by client directly | Hosting setup may differ |
| A5 | Feedback is provided within 2 business days of each review | Timeline shifts day-for-day |
```

**Rules:**
- Out-of-scope section must be at least as detailed as in-scope
- Every exclusion gets a rationale (why it's out) and a path back in (change request)
- List all assumptions that, if wrong, change the timeline or budget
- Number assumptions (A1, A2) for reference in change requests

### Step 4: Create Work Breakdown Structure

Map tasks with dependencies:

```markdown
## 4. Work Breakdown Structure

### Phase 1: Foundation (Week 1-2)
| Task | Deliverable | Depends On | Hours |
|------|------------|-----------|-------|
| 1.1 Project setup (repo, CI/CD, environments) | D1 | — | 6 |
| 1.2 Database schema design and migration | D1 | — | 8 |
| 1.3 Authentication: email/password flow | D1 | 1.1, 1.2 | 10 |
| 1.4 Authentication: Google OAuth | D1 | 1.3 | 6 |
| 1.5 Authentication: password reset | D1 | 1.3 | 4 |
| 1.6 Auth testing and hardening | D1 | 1.3, 1.4, 1.5 | 6 |
| **Phase 1 total** | | | **40** |

### Phase 2: Core Features (Week 3-5)
| Task | Deliverable | Depends On | Hours |
|------|------------|-----------|-------|
| 2.1 Dashboard layout and navigation | D2 | 1.3 | 8 |
| 2.2 User management CRUD | D2 | 2.1, 1.6 | 12 |
| 2.3 Analytics display components | D2 | 2.1 | 10 |
| 2.4 System settings interface | D2 | 2.1 | 8 |
| 2.5 Role-based access control | D2 | 2.2 | 8 |
| 2.6 Dashboard testing | D2 | 2.2, 2.3, 2.4, 2.5 | 10 |
| **Phase 2 total** | | | **56** |

### Phase 3: Polish & Launch (Week 6-7)
| Task | Deliverable | Depends On | Hours |
|------|------------|-----------|-------|
| 3.1 API documentation | D3 | 2.6 | 6 |
| 3.2 Deployment setup (production) | D3 | 2.6 | 8 |
| 3.3 User manual / guides | D3 | 2.6 | 6 |
| 3.4 Final QA and bug fixes | All | 3.1, 3.2, 3.3 | 12 |
| 3.5 Client UAT support | All | 3.4 | 4 |
| **Phase 3 total** | | | **36** |

**Total hours: 132** (+/- 15% contingency)
```

**WBS rules:**
- Every task maps to a deliverable (D1, D2, etc.)
- Dependencies are explicit — no hidden assumptions about ordering
- Tasks are small enough to estimate (max 12 hours per task)
- Include testing and documentation as explicit tasks, not afterthoughts

### Step 5: Define Milestones

```markdown
## 5. Milestones

| # | Milestone | Target Date | Go/No-Go Criteria | Deliverables |
|---|-----------|------------|-------------------|-------------|
| M1 | Kickoff | [Date] | Signed SOW, deposit received, access granted | — |
| M2 | Phase 1 Review | [Date + 2 wk] | All D1 acceptance criteria pass on staging | D1: Auth system |
| M3 | Phase 2 Review | [Date + 5 wk] | All D2 acceptance criteria pass on staging | D2: Dashboard |
| M4 | UAT Begin | [Date + 6.5 wk] | Client begins user acceptance testing | All deliverables on staging |
| M5 | Launch | [Date + 7.5 wk] | All acceptance criteria pass, client sign-off | Production deployment |
| M6 | Support Period End | [Date + 11.5 wk] | No critical bugs open | Support handoff |

### Go/No-Go Process
At each milestone review:
1. Vendor demonstrates completed deliverables against acceptance criteria
2. Client has **2 business days** to review and provide feedback
3. **Go:** Client confirms acceptance criteria are met → proceed to next phase
4. **No-Go:** Client provides specific items that fail acceptance criteria → vendor addresses within 3 business days → re-review
5. If no response within 2 business days, milestone is considered accepted

**Milestone acceptance is required before the next phase begins.** This protects both parties from building on unapproved work.
```

### Step 6: Constraints and Dependencies

```markdown
## 6. Constraints & Dependencies

### Constraints
| Constraint | Impact |
|-----------|--------|
| Budget ceiling of $XX,XXX | Scope adjustments if estimates exceed budget |
| Launch deadline of [date] | Feature prioritization required if timeline slips |
| Must integrate with [existing system] | API compatibility required, may limit tech choices |
| Data must remain in [region] | Hosting provider and database region restricted |

### External Dependencies
| Dependency | Owner | Required By | Risk if Delayed |
|-----------|-------|------------|----------------|
| Branding assets (logo, colors) | Client | M1 (Kickoff) | Delays Phase 2 UI work |
| API credentials for [service] | Client | Phase 2 start | Blocks integration tasks |
| DNS access for domain setup | Client | Phase 3 start | Blocks production deployment |
| Stakeholder availability for UAT | Client | M4 | Delays launch milestone |
| Code review approval | Vendor lead | Each phase end | Blocks milestone sign-off |
```

### Step 7: Change Request Process

```markdown
## 7. Change Management

### Change Request Process
Changes to scope, timeline, or budget follow this process:

1. **Request:** Either party submits a written change request describing:
   - What changes (new feature, modified requirement, removed item)
   - Why the change is needed
   - Which deliverables are affected

2. **Impact Assessment:** Vendor provides within 3 business days:
   - Hours impact (additional or reduced)
   - Cost impact (additional or credit)
   - Timeline impact (delay or no change)
   - Risk assessment (what else might be affected)

3. **Approval:** Client reviews and provides written approval or rejection
   - Approved changes update this SOW as an amendment
   - Rejected changes are documented but not implemented

4. **Implementation:** Approved changes begin in the next phase or sprint

### Change Request Template
```
CHANGE REQUEST #[number]
Date: YYYY-MM-DD
Requested by: [Name]

Description: [What changes and why]

Affected deliverables: [D1, D2, etc.]
Hours impact: [+/- N hours]
Cost impact: [+/- $X,XXX]
Timeline impact: [+/- N days/weeks]

Approved: [ ] Yes  [ ] No
Signature: _______________  Date: ___________
```

### Out-of-Process Changes
Work requested outside the change request process (verbal, chat, email without formal CR) is not included in this SOW and will not be implemented. This protects both parties from scope drift.
```

### Step 8: Assemble Final Document

Output the complete SOW:

```markdown
# Scope of Work: [Project Name]

| Field | Value |
|-------|-------|
| **Client** | [Client Name, Company] |
| **Vendor** | [Your Name / Company] |
| **Date** | YYYY-MM-DD |
| **Version** | 1.0 |
| **Valid until** | [Date + 30 days] |

---

## Table of Contents
1. Project Objectives
2. Deliverables
3. Scope Definition
4. Work Breakdown Structure
5. Milestones
6. Constraints & Dependencies
7. Change Management

---

[Section 1-7 content]

---

## Signatures

This Scope of Work is agreed to by both parties:

**Client:**
Name: ___________________________
Title: ___________________________
Signature: ___________________________
Date: ___________________________

**Vendor:**
Name: ___________________________
Title: ___________________________
Signature: ___________________________
Date: ___________________________

---

## Amendments

| # | Date | Description | Approved By |
|---|------|-------------|------------|
| — | — | Original SOW | — |

---
*This document, together with any approved amendments, constitutes the complete
agreement regarding the scope of work for this project.*
```

**Output summary:**

```
📐 Scope of Work — Complete

Project: [name]
Client: [client name]
Deliverables: [count] with [total] acceptance criteria
Phases: [count] across [weeks] weeks
Total hours: [count] (+/- 15%)
Milestones: [count] with go/no-go gates
Assumptions: [count]
Exclusions: [count] items explicitly out of scope

Document: [word count] words

Next steps:
1. Review with client, negotiate any changes
2. Both parties sign the document
3. File signed copy and begin kickoff preparations
4. Set up milestone calendar reminders
```

## Level History

- **Lv.1** — Base: Project objectives with measurable success criteria, deliverables with acceptance criteria, explicit in/out scope, work breakdown structure with dependencies, milestones with go/no-go gates, constraints and external dependencies, formal change request process, signatures and amendments. (Origin: MemStack Pro v3.2, Mar 2026)
