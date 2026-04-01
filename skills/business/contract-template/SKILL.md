---
name: memstack-business-contract-template
description: "Use this skill when the user says 'contract', 'agreement', 'service agreement', 'NDA', 'freelance contract', 'consulting agreement', or needs service agreements with IP ownership, payment terms, and termination clauses. Do NOT use for invoicing or client onboarding."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# Contract Template — Drafting service agreement...
*Provides service agreement, NDA, and subcontractor templates with scope, payment, IP ownership, confidentiality, termination, and liability clauses.*

## Activation

When this skill activates, output:

`Contract Template — Drafting service agreement...`

Then execute the protocol below.

## Context Guard

| Context | Status |
|---------|--------|
| User says "contract", "agreement", "service agreement", "NDA" | ACTIVE |
| User says "freelance contract" or "consulting agreement" | ACTIVE |
| User needs a written agreement for client or vendor work | ACTIVE |
| User wants an invoice | DORMANT — use Invoice Generator |
| User wants a project proposal | DORMANT — use Proposal Writer |

## Common Mistakes

| Mistake | Why It's Wrong |
|---------|---------------|
| "Handshake deal, no contract" | Verbal agreements are unenforceable. A simple contract protects both parties. |
| "Skip IP ownership clause" | Without explicit IP transfer, the creator often retains rights by default. Always specify. |
| "No termination clause" | Without exit terms, either party is trapped. Define how and when the contract can end. |
| "Copy a template without reading" | Every clause should match your actual arrangement. Mismatched terms create liability. |
| "No dispute resolution" | Without a specified method (mediation, arbitration, jurisdiction), disputes escalate to costly litigation. |

**Disclaimer:** These templates are starting points, not legal advice. Have an attorney review contracts before use, especially for high-value engagements.

## Protocol

### Step 1: Gather Contract Requirements

If the user hasn't provided details, ask:

> 1. **Contract type** — service agreement, NDA, subcontractor agreement, or other?
> 2. **Parties** — who is the provider and who is the client?
> 3. **Scope** — what work is being performed?
> 4. **Payment** — flat fee, hourly, retainer, milestone-based?
> 5. **Duration** — start date, end date, or ongoing?
> 6. **Special terms** — non-compete, exclusivity, IP considerations?

### Step 2: Select Contract Type

| Type | Use When | Key Clauses |
|------|---------|-------------|
| **Service Agreement** | Providing professional services to a client | Scope, payment, IP, liability, termination |
| **NDA (Mutual)** | Both parties share confidential information | Definition of confidential info, exclusions, duration, remedies |
| **NDA (One-way)** | Only one party shares confidential info | Same as mutual but obligations on one side |
| **Subcontractor Agreement** | Hiring someone to help deliver client work | Scope, payment, IP assignment, confidentiality, non-solicitation |
| **Retainer Agreement** | Ongoing monthly services at a fixed rate | Hours/month, rollover policy, scope boundaries, renewal |

### Step 3: Draft Core Clauses

**1. Parties & Effective Date:**
```
This [Agreement Type] ("Agreement") is entered into as of [Date]
("Effective Date") by and between:

**[Provider Name]** ("[Provider/Contractor]")
[Address]
[Email]

and

**[Client Name]** ("Client")
[Address]
[Email]
```

**2. Scope of Work:**
```
Provider agrees to perform the following services ("Services"):

1. [Deliverable 1 — specific description]
2. [Deliverable 2 — specific description]
3. [Deliverable 3 — specific description]

Out of scope (requires separate agreement or change order):
- [Excluded item 1]
- [Excluded item 2]
```

**3. Payment Terms:**
```
Compensation:
- [Flat fee: $X for completion of all Services]
  OR
- [Hourly rate: $X/hour, billed [weekly/monthly], capped at [X] hours]
  OR
- [Milestone: $X upon completion of each milestone per Schedule A]
  OR
- [Retainer: $X/month for up to [X] hours, additional hours at $X/hour]

Payment schedule:
- [50% deposit due upon signing; 50% upon completion]
  OR
- [Net 30 from invoice date]

Late payment:
- Invoices unpaid after [30] days will incur [1.5]% monthly interest.
- Provider may suspend Services after [15] days of non-payment.
```

**4. Intellectual Property:**
```
Option A — Full IP Transfer (most common for client work):
Upon full payment, all work product created under this Agreement
("Work Product") shall be the exclusive property of Client. Provider
assigns all rights, title, and interest in the Work Product to Client.

Option B — License (provider retains ownership):
Provider retains all rights to the Work Product and grants Client a
perpetual, non-exclusive, worldwide license to use, modify, and
distribute the Work Product for Client's business purposes.

Option C — Shared (split ownership):
Client owns the final deliverables. Provider retains the right to
reuse general techniques, methodologies, and non-client-specific
components ("Provider Tools") in future work.

Pre-existing IP:
Any pre-existing intellectual property brought to this engagement
remains the property of its original owner.
```

**5. Confidentiality:**
```
Each party agrees to keep confidential all non-public information
disclosed by the other party ("Confidential Information"), including
but not limited to: business plans, customer data, financial records,
technical specifications, and trade secrets.

Exclusions — Information is not confidential if it:
(a) is or becomes publicly available without breach;
(b) was known to the receiving party before disclosure;
(c) is independently developed without use of confidential information;
(d) is disclosed pursuant to legal requirement (with prior notice).

Duration: Confidentiality obligations survive for [2/3/5] years
after termination of this Agreement.
```

**6. Termination:**
```
Either party may terminate this Agreement:
(a) For convenience: with [30] days written notice;
(b) For cause: if the other party materially breaches and fails to
    cure within [15] days of written notice;
(c) Immediately: if the other party becomes insolvent or bankrupt.

Upon termination:
- Client pays for all Services performed through the termination date.
- Provider delivers all completed and in-progress Work Product.
- Confidentiality and IP provisions survive termination.
```

**7. Liability & Indemnification:**
```
Limitation of Liability:
Provider's total liability under this Agreement shall not exceed
the total fees paid by Client in the [12] months preceding the claim.
Neither party shall be liable for indirect, incidental, consequential,
or punitive damages.

Indemnification:
Each party shall indemnify and hold harmless the other from claims
arising from their own negligence, willful misconduct, or breach
of this Agreement.
```

**8. Dispute Resolution:**
```
Any dispute arising from this Agreement shall be resolved as follows:
1. Good faith negotiation between the parties (30 days);
2. If unresolved, mediation in [City, State];
3. If mediation fails, binding arbitration under [AAA/JAMS] rules;
4. Governing law: State of [State].
```

### Step 4: NDA Template (If Requested)

```markdown
## NON-DISCLOSURE AGREEMENT

This NDA is entered into as of [Date] between:
**Disclosing Party:** [Name]
**Receiving Party:** [Name]

1. **Definition:** "Confidential Information" means all non-public
   information disclosed in writing, orally, or by inspection,
   marked as confidential or reasonably understood to be confidential.

2. **Obligations:** Receiving Party shall: (a) use Confidential
   Information solely for [Purpose]; (b) not disclose to third
   parties without written consent; (c) protect with reasonable care.

3. **Exclusions:** [Same as Section 5 above]

4. **Duration:** [2] years from date of disclosure.

5. **Return:** Upon request, Receiving Party shall return or destroy
   all Confidential Information and certify destruction in writing.

6. **Remedies:** Unauthorized disclosure may cause irreparable harm.
   Disclosing Party may seek injunctive relief in addition to damages.

7. **Governing Law:** State of [State].
```

### Step 5: Signature Block

```markdown
IN WITNESS WHEREOF, the parties have executed this Agreement
as of the Effective Date.

**[Provider Name]**

Signature: _________________________
Name: [Full name]
Title: [Title]
Date: [Date]

**[Client Name]**

Signature: _________________________
Name: [Full name]
Title: [Title]
Date: [Date]
```

### Step 6: Contract Checklist

Before sending:
- [ ] All party names, addresses, and contact info are correct
- [ ] Scope of work matches the proposal or SOW exactly
- [ ] Payment terms, amounts, and schedule are specified
- [ ] IP ownership clause matches the agreed arrangement
- [ ] Confidentiality duration is specified
- [ ] Termination conditions are clear for both parties
- [ ] Liability cap is set at a reasonable amount
- [ ] Dispute resolution jurisdiction/method is specified
- [ ] Both parties have time to review before signing
- [ ] Sent for legal review (recommended for engagements >$10K)

## Output Format

Deliver the contract as a complete document with all selected clauses assembled in order, ready for legal review and signing.

## Completion

```
Contract Template — Complete!

Type: [Service Agreement / NDA / Subcontractor / Retainer]
Parties: [Provider] and [Client]
Duration: [Start] to [End / Ongoing]
Payment: [Terms summary]
IP: [Transfer / License / Shared]

Next steps:
1. Review all clauses to ensure they match your arrangement
2. Have an attorney review before sending (especially >$10K)
3. Send to client for review with reasonable response time
4. Both parties sign and date
5. Store executed copy securely (both parties keep a copy)
```

## Level History

- **Lv.1** — Base: 5 contract types (service, NDA mutual/one-way, subcontractor, retainer), 8 core clauses (parties, scope, payment, IP with 3 options, confidentiality, termination, liability, dispute), standalone NDA template, signature block, pre-send checklist. (Origin: MemStack Pro v3.2, Mar 2026)
