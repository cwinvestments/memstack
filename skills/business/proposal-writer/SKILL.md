---
name: memstack-business-proposal-writer
description: "Use this skill when the user says 'write proposal', 'create proposal', 'proposal for', 'client proposal', 'project proposal', 'bid on project', 'pitch', or is preparing a project proposal for a client or freelance engagement. Do NOT use for contracts, invoices, or onboarding."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# 📝 Proposal Writer — Drafting project proposal...
*Generates a professional project proposal with executive summary, deliverables, tiered pricing, timeline, and terms — ready to send as PDF or email.*

## Activation

When this skill activates, output:

`📝 Proposal Writer — Gathering project details...`

Then execute the protocol below.

| Context | Status |
|---------|--------|
| User says "write proposal" or "create proposal" | ACTIVE |
| User says "pitch" or "bid on project" or "client proposal" | ACTIVE |
| Preparing a document to send to a prospective client | ACTIVE |
| Writing internal project plans (no client) | DORMANT — use scope-of-work |
| Discussing pricing strategy generally | DORMANT |

### Anti-patterns

| Trap | Reality Check |
|------|---------------|
| "Just list what we'll build" | Proposals sell outcomes, not features. Lead with the problem you solve. |
| "One price, take it or leave it" | Tiered pricing lets clients choose their budget level. Always offer 2-3 options. |
| "We'll figure out scope later" | Vague scope creates disputes. Define deliverables AND exclusions explicitly. |
| "Terms can wait until contract" | Payment schedule, revision limits, and IP ownership prevent 80% of freelance conflicts. Include them. |
| "The longer the better" | Busy clients skim. Executive summary + pricing first. Details in appendix. |

## Protocol

### Step 1: Gather Project Requirements

If the user hasn't provided project details, ask:

> I need a few details for the proposal:
> 1. **Client name** and company
> 2. **Project type** (web app, mobile app, marketing site, API, etc.)
> 3. **Core problem** — what does the client need solved?
> 4. **Rough scope** — key features or deliverables
> 5. **Timeline** — any deadlines or target launch date?
> 6. **Budget range** — if known (helps calibrate tier pricing)

If the user provides partial info, ask only for what's missing. Don't ask for information you can infer.

### Step 2: Write Executive Summary

The executive summary is what the client reads first (and sometimes only). It must:

1. **Name the problem** the client faces — in their language, not technical jargon
2. **Present the solution** at a high level — what you'll build and why it works
3. **State the outcome** — what the client gets (revenue, time saved, users served)
4. **Establish credibility** — briefly mention relevant experience

**Template:**

```markdown
## Executive Summary

[Client name] needs [problem statement — what's broken, missing, or inefficient].

We propose [solution summary — what you'll build] using [key technology/approach].
This will [primary outcome — measurable benefit to the client].

Based on our experience with [relevant past work], we estimate [timeline]
for full delivery, with [key milestone] available within [shorter timeframe].
```

**Rules:**
- Max 150 words — if you can't summarize in 150 words, you don't understand the project
- No technical jargon the client wouldn't use
- Lead with their problem, not your solution
- Include one specific number (timeline, cost savings, user capacity)

### Step 3: Break Down Deliverables

List every deliverable with estimated hours per phase:

```markdown
## Deliverables

### Phase 1: Foundation (Week 1-2)
| Deliverable | Description | Est. Hours |
|-------------|-------------|-----------|
| Project setup | Repository, CI/CD, staging environment | 8 |
| Authentication | User registration, login, password reset | 16 |
| Database design | Schema, migrations, seed data | 12 |
| **Phase subtotal** | | **36** |

### Phase 2: Core Features (Week 3-5)
| Deliverable | Description | Est. Hours |
|-------------|-------------|-----------|
| Dashboard | Admin dashboard with key metrics | 24 |
| User management | CRUD, roles, permissions | 20 |
| API integration | Connect to [external service] | 16 |
| **Phase subtotal** | | **60** |

### Phase 3: Polish & Launch (Week 6-7)
| Deliverable | Description | Est. Hours |
|-------------|-------------|-----------|
| Testing | Unit tests, integration tests, QA | 16 |
| Deployment | Production setup, domain, SSL | 8 |
| Documentation | User guide, API docs | 8 |
| **Phase subtotal** | | **32** |

**Total estimated hours: 128**
```

**Rules:**
- Group deliverables by phase (foundation, core, polish)
- Each deliverable is specific and verifiable (not "backend work")
- Hours are estimates — include a buffer note ("+/- 15%")
- Include testing, deployment, and documentation — clients forget these exist

### Step 4: Tech Stack Recommendation

Justify the technology choices:

```markdown
## Technical Approach

| Layer | Technology | Why |
|-------|-----------|-----|
| Frontend | Next.js 15 + React | Fast development, SEO-friendly, scales well |
| Styling | Tailwind CSS | Rapid UI development, consistent design system |
| Backend | Next.js API Routes | Unified codebase, simplifies deployment |
| Database | Supabase (Postgres) | Real-time capabilities, built-in auth, RLS |
| Hosting | Railway + Netlify | Reliable, auto-scaling, CI/CD built-in |
| Auth | Supabase Auth | Secure, supports OAuth, handles sessions |

This stack was chosen for [speed of development / scalability / client's existing infrastructure / cost-effectiveness].
```

**Rules:**
- Only include if the client cares about technical details (some don't)
- Justify each choice in client terms (fast, cheap, reliable — not "it's cool")
- Mention alternatives you considered and why you didn't pick them
- Flag any client-side constraints (existing systems, team expertise)

### Step 5: Create Tiered Pricing

Always offer 2-3 options — never a single price:

```markdown
## Investment

### Option A: Essential — $X,XXX
Core functionality to solve the primary problem.
- [Deliverable 1]
- [Deliverable 2]
- [Deliverable 3]
- 1 round of revisions
- 30 days post-launch support

### Option B: Standard — $XX,XXX ⭐ Recommended
Full solution with all planned features.
- Everything in Essential, plus:
- [Additional deliverable 4]
- [Additional deliverable 5]
- [Additional deliverable 6]
- 2 rounds of revisions
- 60 days post-launch support

### Option C: Premium — $XX,XXX
Complete solution with ongoing support and future-proofing.
- Everything in Standard, plus:
- [Premium deliverable 7]
- [Premium deliverable 8]
- Priority support and maintenance
- 3 rounds of revisions
- 90 days post-launch support + monthly check-ins

All prices exclude applicable taxes. See Payment Terms below.
```

**Pricing rules:**
- Standard tier should be the one you actually want them to pick
- Essential is 60-70% of Standard price — stripped to minimum viable
- Premium is 140-160% of Standard price — adds ongoing value
- Mark the recommended tier visually
- Include revision rounds and support period in each tier — these are the #1 source of scope creep

### Step 6: Timeline with Milestones

```markdown
## Timeline

| Milestone | Target Date | Deliverables |
|-----------|------------|-------------|
| Kickoff | [Date] | Requirements review, access handoff |
| Phase 1 Complete | [Date + 2 weeks] | Foundation: auth, database, staging |
| Phase 1 Review | [Date + 2.5 weeks] | Client review and feedback |
| Phase 2 Complete | [Date + 5 weeks] | Core features on staging |
| Phase 2 Review | [Date + 5.5 weeks] | Client review and feedback |
| Phase 3 Complete | [Date + 7 weeks] | Testing, deployment, docs |
| Launch | [Date + 7.5 weeks] | Production deployment |
| Support Period Begins | [Date + 8 weeks] | Post-launch monitoring |

**Notes:**
- Timeline assumes prompt feedback at review milestones (2 business days)
- Delays in feedback shift subsequent milestones by the same duration
- Timeline is for [Standard tier] — Essential is shorter, Premium is longer
```

**Rules:**
- Include explicit review/feedback milestones (clients cause most delays)
- State feedback turnaround expectation
- Note that delayed feedback shifts the timeline
- Tie timeline to the recommended tier

### Step 7: Terms and Conditions

```markdown
## Terms

### Payment Schedule
| Milestone | Amount | Due |
|-----------|--------|-----|
| Project kickoff | 30% ($X,XXX) | Upon signing |
| Phase 2 complete | 40% ($X,XXX) | On delivery |
| Final delivery | 30% ($X,XXX) | On launch |

### Revision Policy
- Each tier includes [N] rounds of revisions per phase
- A "round" is a single set of consolidated feedback
- Additional revision rounds billed at $XXX/round
- Revisions must be submitted within 5 business days of delivery

### Intellectual Property
- All code and assets become client property upon final payment
- Third-party libraries remain under their original licenses
- We retain the right to use the project in our portfolio (unless client opts out)

### Cancellation
- Client may cancel with 7 days written notice
- Work completed to date is billed at hourly rate ($XXX/hr)
- Deposit is non-refundable after kickoff meeting

### Confidentiality
- Both parties agree to keep project details confidential
- NDA available upon request
```

**Rules:**
- Payment is milestone-based, never 100% upfront or 100% on completion
- Revision policy prevents infinite feedback loops
- IP transfers on final payment — protects you if they don't pay
- Cancellation terms protect both sides

### Step 8: Assemble Final Document

Output the complete proposal in clean markdown:

```markdown
# Project Proposal: [Project Name]

**Prepared for:** [Client Name], [Company]
**Prepared by:** [Your Name / Company]
**Date:** [YYYY-MM-DD]
**Valid until:** [Date + 30 days]

---

## Executive Summary
[Step 2 output]

## Deliverables
[Step 3 output]

## Technical Approach
[Step 4 output]

## Investment
[Step 5 output]

## Timeline
[Step 6 output]

## Terms
[Step 7 output]

---

## Next Steps

To proceed, please:
1. Select your preferred tier (Essential / Standard / Premium)
2. Sign this proposal (reply with written confirmation)
3. Submit the initial deposit

We'll schedule a kickoff meeting within 3 business days of receiving both.

Questions? Reply to this email or call [phone number].

---
*This proposal is valid for 30 days from the date above.*
```

**Output summary:**

```
📝 Proposal Writer — Complete

Client: [name]
Project: [project name]
Tiers: Essential ($X) / Standard ($XX) / Premium ($XXX)
Timeline: [N] weeks (Standard tier)
Phases: [N] with [N] review milestones

Document: [word count] words, ready for PDF conversion

Next steps:
1. Review and customize pricing figures
2. Add your company details and contact info
3. Export to PDF or paste into email
```

## Level History

- **Lv.1** — Base: Requirements gathering, executive summary, phased deliverables with hours, tech stack justification, 3-tier pricing, milestone timeline, terms (payment, revisions, IP, cancellation), final document assembly. Based on Quill skill patterns and real client work (Soul Siren Somatics, freelance projects). (Origin: MemStack Pro v3.2, Mar 2026)
