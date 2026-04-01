---
name: memstack-business-invoice-generator
description: "Use this skill when the user says 'invoice', 'generate invoice', 'create invoice', 'bill client', 'line items', 'payment terms', or needs professional invoices with tax calculations and payment instructions. Do NOT use for contracts or financial projections."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# Invoice Generator — Creating professional invoice...
*Generates professional invoices with line items, tax calculations, payment terms, due dates, and payment instructions — output as structured markdown ready for PDF conversion.*

## Activation

When this skill activates, output:

`Invoice Generator — Creating professional invoice...`

Then execute the protocol below.

## Context Guard

| Context | Status |
|---------|--------|
| User says "invoice", "generate invoice", "create invoice", "bill client" | ACTIVE |
| User says "line items" or "payment terms" | ACTIVE |
| User needs a professional invoice for a client | ACTIVE |
| User wants a contract or service agreement | DORMANT — use Contract Template |
| User wants financial projections | DORMANT — use Financial Model |

## Common Mistakes

| Mistake | Why It's Wrong |
|---------|---------------|
| "No invoice number" | Sequential invoice numbers are required for accounting and tax compliance. |
| "Vague line items" | "Consulting — $5,000" invites disputes. Itemize by deliverable, hours, or phase. |
| "No payment terms" | Without explicit terms (Net 30, due on receipt), clients have no obligation to pay on time. |
| "Skip tax line" | Even if tax is $0, show the tax line. It demonstrates professionalism and compliance. |
| "No late payment terms" | Without stated consequences, you have no leverage on overdue invoices. |

## Protocol

### Step 1: Gather Invoice Details

If the user hasn't provided details, ask:

> 1. **Client** — company name, contact person, billing address
> 2. **Your business** — business name, address, tax ID / EIN (if applicable)
> 3. **Line items** — what are you billing for? (description, quantity, rate)
> 4. **Payment terms** — Net 30, Net 15, due on receipt?
> 5. **Tax** — applicable tax rate? (state sales tax, VAT, or exempt)
> 6. **Currency** — USD, EUR, GBP, etc.?

### Step 2: Generate Invoice Number

**Invoice numbering convention:**

```
[PREFIX]-[YEAR][MONTH]-[SEQUENCE]
Example: INV-202603-001
```

| Component | Rule |
|-----------|------|
| Prefix | `INV` (standard), `PRO` (proforma), `CR` (credit note) |
| Date | YYYYMM of invoice date |
| Sequence | 001, 002, 003... (reset yearly or continuous) |

**Alternative formats:**
- Client-based: `INV-ACME-001`
- Project-based: `INV-PROJ042-001`

### Step 3: Build Line Items

**Line item table:**

| # | Description | Qty | Unit | Rate | Amount |
|---|------------|-----|------|------|--------|
| 1 | [Detailed description of work/deliverable] | [X] | [hours/units/flat] | $[X.XX] | $[X.XX] |
| 2 | [Detailed description] | [X] | [unit] | $[X.XX] | $[X.XX] |
| 3 | [Detailed description] | [X] | [unit] | $[X.XX] | $[X.XX] |

**Line item rules:**
- Each line should describe a specific deliverable or time period
- Include enough detail to prevent client questions ("Website development" → "Homepage redesign — responsive layout, 3 revision rounds")
- For hourly work: include date range and total hours
- For project work: reference the SOW or contract phase
- For expenses: mark as "Reimbursable expense" with receipt reference

**Totals calculation:**

```
Subtotal:                    $[sum of line amounts]
Discount ([X]%):            -$[discount amount]
Subtotal after discount:     $[adjusted subtotal]
Tax ([X]% [tax name]):      +$[tax amount]
──────────────────────────────────
Total Due:                   $[final total]
```

### Step 4: Set Payment Terms

**Standard payment terms:**

| Term | Meaning | Best For |
|------|---------|---------|
| Due on receipt | Pay immediately | Small amounts, first-time clients |
| Net 15 | Due within 15 days | Freelance, small projects |
| Net 30 | Due within 30 days | Standard business term |
| Net 60 | Due within 60 days | Enterprise, government |
| 50/50 | 50% upfront, 50% on completion | Projects >$5,000 |
| Milestone | Payment at each project phase | Large projects |

**Late payment clause:**

```
Late Payment: Invoices not paid within [X] days of the due date will
incur a late fee of [1.5]% per month ([18]% annually) on the outstanding
balance. All collection costs, including attorney fees, will be the
responsibility of the client.
```

**Early payment discount (optional):**

```
2/10 Net 30: 2% discount if paid within 10 days; full amount due in 30 days.
```

### Step 5: Add Payment Instructions

```markdown
## Payment Methods

**Bank Transfer (preferred):**
Bank: [Bank name]
Account name: [Business name]
Routing number: [XXXXXXXXX]
Account number: [XXXXXXXXX]
Reference: [Invoice number]

**Online Payment:**
Pay online: [Payment link — Stripe, PayPal, or Square invoice URL]

**Check:**
Make payable to: [Business name]
Mail to: [Mailing address]
Memo: [Invoice number]

**Wire Transfer (international):**
SWIFT/BIC: [Code]
IBAN: [Number]
Bank address: [Address]
```

### Step 6: Assemble the Invoice

**Invoice template:**

```markdown
─────────────────────────────────────────────────────────

                        INVOICE

─────────────────────────────────────────────────────────

**From:**                          **Invoice #:** [INV-YYYYMM-NNN]
[Your Business Name]               **Date:** [Invoice date]
[Your Address]                      **Due Date:** [Due date]
[City, State ZIP]                   **Terms:** [Net 30 / etc.]
[Email]
[Phone]
[Tax ID: XX-XXXXXXX]

**Bill To:**
[Client Company Name]
[Client Contact Name]
[Client Address]
[City, State ZIP]
[Client Email]

─────────────────────────────────────────────────────────

| #  | Description                     | Qty  | Rate      | Amount    |
|----|---------------------------------|------|-----------|-----------|
| 1  | [Line item description]         | [X]  | $[X.XX]   | $[X.XX]   |
| 2  | [Line item description]         | [X]  | $[X.XX]   | $[X.XX]   |
| 3  | [Line item description]         | [X]  | $[X.XX]   | $[X.XX]   |

─────────────────────────────────────────────────────────
                              Subtotal:      $[X,XXX.XX]
                              Tax ([X]%):    $[XXX.XX]
                              ──────────────────────────
                              **TOTAL DUE:   $[X,XXX.XX]**
─────────────────────────────────────────────────────────

## Payment Instructions
[From Step 5]

## Terms
- Payment is due within [X] days of invoice date.
- [Late payment clause from Step 4]
- [Early payment discount if applicable]

─────────────────────────────────────────────────────────
Thank you for your business.
─────────────────────────────────────────────────────────
```

### Step 7: Recurring Invoice Setup

For ongoing retainer or subscription billing:

```markdown
## Recurring Invoice Schedule

| Invoice # | Period | Amount | Due Date | Status |
|-----------|--------|--------|----------|--------|
| INV-202601-001 | Jan 2026 | $[X] | [Date] | Paid |
| INV-202602-001 | Feb 2026 | $[X] | [Date] | Paid |
| INV-202603-001 | Mar 2026 | $[X] | [Date] | Current |
| INV-202604-001 | Apr 2026 | $[X] | [Date] | Upcoming |
```

**Automation tips:**
- Use Stripe Invoicing, QuickBooks, or FreshBooks for recurring invoices
- Set automatic payment reminders: 3 days before due, on due date, 7 days overdue
- Auto-generate the next invoice on a fixed schedule (1st of month, etc.)

## Output Format

Deliver the complete invoice in the template format from Step 6, ready to be:
- Converted to PDF (via Pandoc, browser print, or invoicing tool)
- Pasted into an invoicing platform
- Sent directly to the client

## Completion

```
Invoice Generator — Complete!

Invoice #: [Number]
Client: [Name]
Line items: [Count]
Subtotal: $[Amount]
Tax: $[Amount]
Total due: $[Amount]
Payment terms: [Terms]
Due date: [Date]

Next steps:
1. Review all line items for accuracy
2. Convert to PDF or enter into your invoicing tool
3. Send to client with payment instructions
4. Set a calendar reminder for the due date
5. Follow up if not paid within 3 days of due date
```

## Level History

- **Lv.1** — Base: Invoice numbering convention, detailed line items with totals/tax/discount, 6 payment term options, late payment clause, early payment discount, 4 payment method templates (bank, online, check, wire), complete invoice template, recurring invoice schedule, automation tips. (Origin: MemStack Pro v3.2, Mar 2026)
