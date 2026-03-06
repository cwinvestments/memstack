---
name: contract-template
description: "Use when the user says 'contract', 'agreement', 'service agreement', 'NDA', 'freelance contract', or wants to generate a professional service contract with legal clauses."
---

# 📜 Contract Template — Service Agreement Generator
*Generate professional service agreements with scope, payment terms, IP ownership, confidentiality, termination, and dispute resolution clauses.*

## Activation

When this skill activates, output:

`📜 Contract Template — Drafting your service agreement...`

| Context | Status |
|---------|--------|
| **User says "contract", "agreement", "service agreement"** | ACTIVE |
| **User wants NDA, freelance contract, or consulting agreement** | ACTIVE |
| **User mentions IP ownership, payment terms, or termination clauses** | ACTIVE |
| **User wants to generate an invoice (not a contract)** | DORMANT — see invoice-generator |
| **User wants client onboarding (contract is one piece)** | DORMANT — see client-onboarding |

## Protocol

### Step 1: Gather Inputs

Ask the user for:
- **Parties**: Your name/company and client name/company
- **Project scope**: What work will be performed?
- **Timeline**: Start date, end date, milestones
- **Payment**: Total amount, payment schedule, method
- **Work type**: Freelance, consulting, agency, SaaS development?
- **IP preference**: Client owns all work? Shared? You retain license?
- **Jurisdiction**: State/country for governing law

### Step 2: Choose Contract Type

Recommend the appropriate template:

| Type | Best For | Key Clauses |
|------|----------|-------------|
| **Fixed-Price Service Agreement** | Project with defined deliverables | Scope, milestones, payment on delivery |
| **Retainer Agreement** | Ongoing monthly work | Monthly hours, rollover policy, rate |
| **Consulting Agreement** | Advisory/strategy work | Hourly rate, expense reimbursement |
| **NDA (Standalone)** | Pre-engagement confidentiality | Definition of confidential info, duration |
| **SaaS Development Agreement** | Building a software product | IP assignment, source code, hosting |

### Step 3: Generate Service Agreement

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            SERVICE AGREEMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This Service Agreement ("Agreement") is entered into as of
[DATE] ("Effective Date") by and between:

SERVICE PROVIDER:
[Provider Name/Company]
[Address]
[Email]
("Provider")

CLIENT:
[Client Name/Company]
[Address]
[Email]
("Client")
```

### Step 4: Scope of Work

```
1. SCOPE OF WORK

1.1 Provider agrees to perform the following services
    ("Services"):

    a) [Deliverable 1 — detailed description]
    b) [Deliverable 2 — detailed description]
    c) [Deliverable 3 — detailed description]

1.2 The Services shall be completed according to the
    following milestones:

    Milestone 1: [description] — Due: [date]
    Milestone 2: [description] — Due: [date]
    Milestone 3: [description] — Due: [date]
    Final delivery: [description] — Due: [date]

1.3 Any work outside the scope defined in Section 1.1
    shall require a written Change Order signed by both
    parties, which may include adjusted timeline and fees.

1.4 Client shall provide all necessary materials, access,
    and feedback within [X] business days of request.
    Delays in Client response may extend project timelines
    proportionally.
```

### Step 5: Payment Terms

```
2. PAYMENT

2.1 Total project fee: $[AMOUNT] [CURRENCY]

2.2 Payment schedule:
    a) [X]% ($[amount]) due upon signing this Agreement
    b) [X]% ($[amount]) due upon completion of Milestone [N]
    c) [X]% ($[amount]) due upon final delivery and acceptance

    — OR for retainer —

    a) $[AMOUNT] per month, due on the [X]th of each month
    b) Includes up to [X] hours of work per month
    c) Unused hours [do / do not] roll over to the next month
    d) Hours exceeding the monthly allowance are billed at
       $[RATE]/hour

2.3 Payment method: [bank transfer / Stripe / PayPal / check]

2.4 Invoices are due within [15/30] days of receipt.
    Late payments incur a fee of [1.5]% per month on the
    outstanding balance.

2.5 Provider reserves the right to pause work if payment
    is overdue by more than [15] days.

2.6 Expenses: [Client will / will not] reimburse reasonable
    expenses. Expenses over $[X] require prior written approval.
```

### Step 6: IP Ownership & Work-for-Hire

```
3. INTELLECTUAL PROPERTY

    — OPTION A: Full Assignment (Client Owns All) —

3.1 All work product created under this Agreement
    ("Work Product") shall be considered "work made for
    hire" under applicable copyright law. To the extent
    any Work Product does not qualify as work made for
    hire, Provider hereby assigns all right, title, and
    interest in such Work Product to Client.

3.2 Provider retains no rights to use, reproduce, or
    display the Work Product except for portfolio purposes
    with Client's written consent.

    — OPTION B: License (Provider Retains Ownership) —

3.1 Provider retains all intellectual property rights in
    the Work Product. Upon full payment, Provider grants
    Client a perpetual, non-exclusive, worldwide license
    to use, modify, and display the Work Product for
    Client's business purposes.

3.2 Provider may reuse general techniques, knowledge,
    and non-proprietary components in future work.

    — OPTION C: Split (Common for SaaS) —

3.1 Client owns all custom code, designs, and content
    created specifically for Client's project.

3.2 Provider retains ownership of pre-existing tools,
    frameworks, and libraries used in the project
    ("Provider Tools"). Provider grants Client a perpetual,
    non-exclusive license to use Provider Tools as
    incorporated in the Work Product.

3.3 Open-source components remain subject to their
    respective licenses.
```

### Step 7: Confidentiality

```
4. CONFIDENTIALITY

4.1 "Confidential Information" means any non-public
    information disclosed by either party, including but
    not limited to: business plans, customer data, source
    code, financial information, trade secrets, and the
    terms of this Agreement.

4.2 Each party agrees to:
    a) Use Confidential Information only for purposes of
       this Agreement
    b) Not disclose Confidential Information to third
       parties without prior written consent
    c) Protect Confidential Information with at least the
       same care used for its own confidential information

4.3 Exclusions. Confidential Information does not include
    information that:
    a) Is or becomes publicly available through no fault
       of the receiving party
    b) Was known to the receiving party prior to disclosure
    c) Is independently developed without use of the
       disclosing party's information
    d) Is required to be disclosed by law or court order

4.4 This confidentiality obligation survives termination
    of this Agreement for a period of [2/3/5] years.
```

### Step 8: Termination

```
5. TERMINATION

5.1 Either party may terminate this Agreement with [15/30]
    days' written notice.

5.2 Upon termination:
    a) Client shall pay for all Services performed through
       the termination date
    b) Provider shall deliver all completed Work Product
    c) Provider shall return or destroy Client's
       Confidential Information within [10] days

5.3 Termination for Cause: Either party may terminate
    immediately if the other party:
    a) Materially breaches this Agreement and fails to
       cure within [15] days of written notice
    b) Becomes insolvent or files for bankruptcy

5.4 Kill Fee: If Client terminates without cause before
    project completion, Client shall pay [a kill fee of X%
    of the remaining project value / for work completed
    plus 2 weeks of planned work].
```

### Step 9: Liability, Indemnification & Disputes

```
6. LIMITATION OF LIABILITY

6.1 IN NO EVENT SHALL EITHER PARTY'S TOTAL LIABILITY
    EXCEED THE TOTAL FEES PAID OR PAYABLE UNDER THIS
    AGREEMENT IN THE [12] MONTHS PRECEDING THE CLAIM.

6.2 NEITHER PARTY SHALL BE LIABLE FOR INDIRECT, INCIDENTAL,
    CONSEQUENTIAL, SPECIAL, OR PUNITIVE DAMAGES, REGARDLESS
    OF THE CAUSE OF ACTION.

6.3 Provider makes no warranty that Services will be
    error-free, but will correct material defects reported
    within [30] days of delivery at no additional cost.


7. INDEMNIFICATION

7.1 Provider indemnifies Client against third-party claims
    arising from Provider's infringement of intellectual
    property rights in the Work Product.

7.2 Client indemnifies Provider against third-party claims
    arising from Client's use of the Work Product or
    Client-provided materials.


8. DISPUTE RESOLUTION

    — OPTION A: Arbitration —

8.1 Any dispute arising under this Agreement shall be
    resolved by binding arbitration in [City, State],
    conducted by [AAA / JAMS] under its commercial rules.

    — OPTION B: Litigation —

8.1 Any dispute arising under this Agreement shall be
    subject to the exclusive jurisdiction of the courts
    of [State/Country].

8.2 Before initiating formal proceedings, both parties
    agree to attempt resolution through good-faith
    negotiation for a period of [30] days.


9. GENERAL PROVISIONS

9.1 Governing Law: This Agreement is governed by the laws
    of [State/Country].

9.2 Entire Agreement: This Agreement constitutes the
    entire agreement and supersedes all prior negotiations.

9.3 Amendments: Modifications require written agreement
    signed by both parties.

9.4 Severability: If any provision is unenforceable, the
    remaining provisions remain in full force.

9.5 Independent Contractor: Provider is an independent
    contractor, not an employee of Client.

9.6 Force Majeure: Neither party is liable for delays
    caused by events beyond reasonable control.


SIGNATURES:

Provider: ________________________  Date: __________
          [Provider Name]

Client:   ________________________  Date: __________
          [Client Name]
```

### Step 10: Output

Present the complete contract package:

```
━━━ CONTRACT: [Project Name] ━━━━━━━━━━━━━

── CONTRACT TYPE ───────────────────────────
Type: [fixed-price / retainer / consulting / NDA]
Parties: [provider] ↔ [client]

── FULL AGREEMENT TEXT ────────────────────
[complete contract with all sections]

── FILL-IN SECTIONS ───────────────────────
[list of all [BRACKETED] items that need values]

── CUSTOMIZATION NOTES ────────────────────
• IP: Using [Option A/B/C] — [rationale]
• Disputes: Using [arbitration/litigation] — [rationale]
• Payment: [schedule summary]
• Termination: [notice period + kill fee]

── DISCLAIMER ─────────────────────────────
This template is for informational purposes only and does
not constitute legal advice. Have an attorney review before
signing.
```

## Inputs
- Party details (provider and client)
- Project scope and deliverables
- Payment amount, schedule, and method
- Timeline and milestones
- IP ownership preference
- Jurisdiction for governing law

## Outputs
- Complete service agreement with standard legal clauses
- Scope of work with milestones and change order provisions
- Payment terms (fixed-price or retainer) with late fee policy
- IP ownership section (3 options: full assignment, license, split)
- Confidentiality/NDA section with exclusions
- Termination conditions with notice period and kill fee
- Limitation of liability and indemnification
- Dispute resolution (arbitration or litigation option)
- Fill-in-the-blank section list for customization

## Level History

- **Lv.1** — Base: 5 contract types (fixed-price, retainer, consulting, NDA, SaaS dev), scope with change orders, payment schedules with late fees, 3-option IP ownership (assignment/license/split), confidentiality with exclusions, termination with kill fee, liability cap, indemnification, dual dispute resolution options (arbitration/litigation), fill-in-the-blank output. (Origin: MemStack v3.2, Mar 2026)
