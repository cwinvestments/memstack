---
name: memstack-business-freelancer-toolkit
description: "Use when the user says 'track my time', 'freelancer invoice', 'billable hours', 'time tracking', 'freelance finances', 'client billing', 'project hours', or needs invoicing, time tracking, or analytics patterns for freelance work. Do NOT use for general invoice templates or proposal writing."
version: 1.0.0
---

# Freelancer Toolkit — Setting up freelancer workflows...
*Produces time tracking sheets, invoice calculations, and project analytics for freelancers managing multiple clients.*

## Activation

| Trigger | Status |
|---------|--------|
| User says "track my time" or "billable hours" | ACTIVE |
| User says "freelancer invoice" or "client billing" | ACTIVE |
| User says "freelance finances" or "project hours" | ACTIVE |
| User wants a formal proposal or SOW | NOT this skill — use Proposal Writer or Scope of Work |
| User wants a generic invoice template | NOT this skill — use Invoice Generator |

## Context Guard

- Do NOT use for proposal writing (that's proposal-writer)
- Do NOT use for scope of work documents (that's scope-of-work)
- Do NOT use for generic invoice templates (that's invoice-generator)
- This skill covers the full freelancer workflow: tracking time → calculating billable → generating invoice → analyzing profitability

## Steps

### Step 1: Gather freelancer context

| Parameter | Default | Example |
|-----------|---------|---------|
| Hourly rate | Ask | $150/hr, $85/hr |
| Currency | USD | EUR, GBP, AUD |
| Billing cycle | Monthly | Weekly, per-project |
| Clients | Ask | Acme Corp, StartupX |
| Tax rate | 0% (user adds) | 20% VAT, 25% self-employment |

### Step 2: Time tracking sheet

Create or update a tracking spreadsheet (CSV or markdown):

```markdown
# Time Log — [Month Year]

## [Client Name]

| Date | Project | Task | Hours | Billable | Notes |
|------|---------|------|-------|----------|-------|
| 2026-04-01 | Website Redesign | Homepage wireframes | 3.5 | Yes | Completed v1 |
| 2026-04-01 | Website Redesign | Client feedback call | 0.5 | Yes | Revision notes |
| 2026-04-02 | API Integration | Auth endpoint | 4.0 | Yes | |
| 2026-04-02 | Internal | Admin/invoicing | 1.0 | No | Non-billable |

**Subtotal:** 8.0 billable hours / 9.0 total hours
```

**Time tracking rules:**
1. Log daily — reconstructing from memory loses hours
2. Separate billable from non-billable (admin, learning, invoicing)
3. Round to nearest 15 minutes (0.25 hr increments)
4. Include project and task for accurate per-project reporting
5. Notes field captures context for invoice line items

### Step 3: Invoice calculation

Compute totals from the time log:

```markdown
# Invoice Calculation — [Client Name] — [Period]

| Project | Hours | Rate | Subtotal |
|---------|-------|------|----------|
| Website Redesign | 24.5 | $150 | $3,675.00 |
| API Integration | 16.0 | $150 | $2,400.00 |

| | |
|---|---|
| Subtotal | $6,075.00 |
| Tax ([rate]%) | $[amount] |
| **Total Due** | **$[amount]** |
| Payment terms | Net 30 |
| Due date | [date] |
```

For fixed-price projects, track hours anyway for profitability analysis.

### Step 4: Monthly analytics

Generate a freelancer dashboard:

```markdown
# Freelance Analytics — [Month Year]

## Revenue Summary
| Client | Invoiced | Paid | Outstanding |
|--------|----------|------|-------------|
| Acme Corp | $6,075 | $6,075 | $0 |
| StartupX | $3,200 | $0 | $3,200 |
| **Total** | **$9,275** | **$6,075** | **$3,200** |

## Time Breakdown
- Total hours logged: 82.0
- Billable hours: 68.5 (83.5% utilization)
- Non-billable hours: 13.5
- Effective hourly rate: $135.40 (revenue / total hours)

## Client Concentration
- Acme Corp: 65.5% of revenue (risk: high dependency)
- StartupX: 34.5%

## Profitability by Project
| Project | Hours | Revenue | Effective Rate |
|---------|-------|---------|----------------|
| Website Redesign | 24.5 | $3,675 | $150/hr |
| API Integration | 16.0 | $2,400 | $150/hr |
| Maintenance | 28.0 | $3,200 | $114/hr |
```

### Step 5: Alerts and recommendations

Flag issues automatically:

| Alert | Threshold | Action |
|-------|-----------|--------|
| Low utilization | < 70% billable | Review non-billable time, reduce admin overhead |
| Client concentration | > 50% one client | Diversify — pursue new leads |
| Outstanding invoices | > 30 days | Send payment reminder |
| Effective rate below target | < 80% of hourly rate | Review scope creep, renegotiate |
| Overwork | > 45 hrs/week sustained | Raise rates or reduce commitments |

### Step 6: File organization

Recommended folder structure:

```
freelance/
  clients/
    acme-corp/
      time-log-2026-04.md
      invoices/
        INV-2026-04-001.md
    startupx/
      time-log-2026-04.md
      invoices/
  analytics/
    2026-04-monthly.md
  templates/
    invoice-template.md
    time-log-template.md
```

## Output Template

```
Freelancer Report — [Period]:
- Billable hours: [N] ([utilization]% utilization)
- Revenue: $[amount] ([N] invoices)
- Outstanding: $[amount]
- Effective rate: $[rate]/hr
- Alerts: [list any flags]

Files updated: [list]
```

## Disambiguation

- "track my time" / "billable hours" / "freelancer invoice" = Freelancer Toolkit
- "write a proposal" / "project proposal" = Proposal Writer (not this skill)
- "scope of work" / "SOW" = Scope of Work (not this skill)
- "create invoice" / "invoice template" = Invoice Generator (not this skill)
- "financial model" / "projections" = Financial Model (not this skill)

## Level History

- **Lv.1** — Base: Time tracking, invoice calculation, monthly analytics, profitability analysis, alerts. (Origin: MemStack v3.5, Apr 2026)
