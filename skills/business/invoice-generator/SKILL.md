---
name: invoice-generator
description: "Use when the user says 'invoice', 'generate invoice', 'billing', 'send invoice', or wants to create a professional invoice with line items and payment instructions."
---

# 🧾 Invoice Generator — Professional Invoice Builder
*Generate complete invoices with line items, tax calculations, payment instructions, and structured data ready for PDF generation or email delivery.*

## Activation

When this skill activates, output:

`🧾 Invoice Generator — Generating your invoice...`

| Context | Status |
|---------|--------|
| **User says "invoice", "generate invoice", "create invoice"** | ACTIVE |
| **User wants to bill a client for completed work** | ACTIVE |
| **User mentions line items, payment terms, or invoice numbers** | ACTIVE |
| **User wants a full contract (not just billing)** | DORMANT — see contract-template |
| **User wants financial projections (not invoicing)** | DORMANT — see financial-model |
| **User wants to onboard a new client** | DORMANT — see client-onboarding |

## Protocol

### Step 1: Gather Inputs

Ask the user for:
- **Your business info**: Company name, address, email, phone, logo URL (optional)
- **Client info**: Client name, company, address, email
- **Line items**: Description, quantity, unit price for each item/service
- **Payment terms**: Net 15, Net 30, Net 60, due on receipt?
- **Tax**: Tax rate (%), tax ID/VAT number (optional)
- **Discounts**: Any discounts to apply? (% or fixed amount)
- **Payment methods**: Bank transfer, Stripe, PayPal, check?
- **Invoice number format**: Preference? (e.g., INV-2026-001, or auto-generate)
- **Currency**: USD, EUR, GBP, etc.

### Step 2: Generate Invoice Number

**Configurable formats:**

| Format | Example | Best For |
|--------|---------|----------|
| Sequential | INV-001 | Simple, solo freelancer |
| Year-sequential | INV-2026-001 | Annual tracking |
| Client-prefixed | INV-ACME-001 | Multi-client businesses |
| Date-based | INV-20260301-001 | High volume, daily tracking |
| Project-based | INV-PROJ42-001 | Per-project billing |

**Auto-generation logic:**
```
Format: [PREFIX]-[YEAR]-[SEQ]
Example: INV-2026-001

Next invoice: Check last invoice number, increment sequence.
If new year: reset sequence to 001.
```

### Step 3: Calculate Totals

Build the invoice calculation:

```
── LINE ITEMS ─────────────────────────────

#  Description                    Qty    Rate       Amount
1  [item description]             [qty]  $[rate]    $[amount]
2  [item description]             [qty]  $[rate]    $[amount]
3  [item description]             [qty]  $[rate]    $[amount]

───────────────────────────────────────────
                          Subtotal:  $[subtotal]
                      Discount (X%): -$[discount]
                   Subtotal after discount: $[after_discount]
                          Tax (X%):  $[tax]
                          ─────────────────
                            TOTAL:  $[total]
```

**Calculation rules:**
- Subtotal = Σ (quantity × unit_rate) for each line item
- Discount applied to subtotal (before tax)
- Tax calculated on discounted subtotal
- Total = discounted subtotal + tax
- Round all amounts to 2 decimal places
- Display currency symbol consistently

### Step 4: Payment Instructions

Generate payment details based on selected methods:

**Bank Transfer:**
```
── PAYMENT BY BANK TRANSFER ───────────────
Bank: [bank name]
Account name: [name]
Account number: [number]
Routing number: [number]
SWIFT/BIC: [code] (for international)
Reference: [invoice number]
```

**Stripe Payment Link:**
```
── PAY ONLINE ─────────────────────────────
Pay securely via credit card:
[Stripe payment link URL]
```

**PayPal:**
```
── PAYPAL ─────────────────────────────────
Send payment to: [email]
Reference: [invoice number]
```

**Check:**
```
── PAY BY CHECK ───────────────────────────
Make payable to: [company name]
Mail to: [address]
Memo: [invoice number]
```

### Step 5: Due Date & Late Fee Terms

**Due date calculation:**

| Terms | Due Date | Late Fee |
|-------|----------|----------|
| Due on receipt | Invoice date | 1.5%/month after 7 days |
| Net 15 | Invoice date + 15 days | 1.5%/month after due date |
| Net 30 | Invoice date + 30 days | 1.5%/month after due date |
| Net 60 | Invoice date + 60 days | 1.0%/month after due date |
| Custom | [specific date] | [custom terms] |

**Late fee clause:**
```
A late fee of [X]% per month ([Y]% annually) will be applied to
balances unpaid after the due date. Partial months are prorated.
```

### Step 6: Professional Layout

Define the invoice layout structure:

```
┌─────────────────────────────────────────┐
│  [LOGO]              INVOICE            │
│  [Your Company]      Invoice #: [num]   │
│  [Your Address]      Date: [date]       │
│  [Your Email]        Due: [due date]    │
│  [Your Phone]        Terms: [terms]     │
├─────────────────────────────────────────┤
│  BILL TO:                               │
│  [Client Name]                          │
│  [Client Company]                       │
│  [Client Address]                       │
│  [Client Email]                         │
├─────────────────────────────────────────┤
│  # │ Description    │ Qty │ Rate │ Amt  │
│  ──┼────────────────┼─────┼──────┼───── │
│  1 │ [item]         │ [q] │ $[r] │ $[a] │
│  2 │ [item]         │ [q] │ $[r] │ $[a] │
│  3 │ [item]         │ [q] │ $[r] │ $[a] │
│  ──┴────────────────┴─────┴──────┴───── │
│                    Subtotal:  $[sub]     │
│                    Discount:  -$[disc]   │
│                    Tax (X%):  $[tax]     │
│                    ───────────────────── │
│                    TOTAL DUE: $[total]   │
├─────────────────────────────────────────┤
│  PAYMENT INSTRUCTIONS:                  │
│  [payment method details]               │
├─────────────────────────────────────────┤
│  NOTES:                                 │
│  [optional notes — thank you message,   │
│   project reference, etc.]              │
│                                         │
│  TERMS:                                 │
│  [late fee policy]                      │
└─────────────────────────────────────────┘
```

### Step 7: Structured Data Output

Generate invoice as structured JSON for programmatic use:

```json
{
  "invoice_number": "INV-2026-001",
  "date": "2026-03-01",
  "due_date": "2026-03-31",
  "terms": "Net 30",
  "currency": "USD",
  "from": {
    "name": "Your Company",
    "address": "123 Main St, City, State 12345",
    "email": "billing@company.com",
    "phone": "+1-555-0100",
    "tax_id": "XX-XXXXXXX"
  },
  "to": {
    "name": "Client Name",
    "company": "Client Corp",
    "address": "456 Oak Ave, City, State 67890",
    "email": "accounts@client.com"
  },
  "line_items": [
    {
      "description": "Web Development",
      "quantity": 40,
      "unit": "hours",
      "rate": 150.00,
      "amount": 6000.00
    }
  ],
  "subtotal": 6000.00,
  "discount": { "type": "percentage", "value": 10, "amount": 600.00 },
  "tax": { "rate": 8.25, "amount": 445.50 },
  "total": 5845.50,
  "payment_methods": ["bank_transfer", "stripe"],
  "notes": "Thank you for your business!",
  "late_fee": "1.5% per month on overdue balances"
}
```

### Step 8: Email Template

Provide email copy for sending the invoice:

```
Subject: Invoice [INV-NUMBER] from [Your Company] — Due [Due Date]

Hi [Client First Name],

Please find attached invoice [INV-NUMBER] for [brief description of work].

Amount due: $[TOTAL]
Due date: [DUE DATE]
Payment: [payment method summary]

If you have any questions about this invoice, please reply to this email.

Thank you for your business!

[Your Name]
[Your Company]
[Your Phone]
```

### Step 9: Output

Present the complete invoice package:

```
━━━ INVOICE: [Invoice Number] ━━━━━━━━━━━━

── INVOICE DETAILS ────────────────────────
From: [your company]
To: [client]
Date: [date]
Due: [due date]
Terms: [payment terms]

── LINE ITEMS ─────────────────────────────
[formatted line item table]

── TOTALS ─────────────────────────────────
Subtotal: $[amount]
Discount: -$[amount]
Tax: $[amount]
Total: $[amount]

── PAYMENT INSTRUCTIONS ───────────────────
[payment method details]

── STRUCTURED DATA (JSON) ─────────────────
[complete JSON for programmatic use]

── EMAIL TEMPLATE ─────────────────────────
[ready-to-send email copy]

── NOTES ──────────────────────────────────
[thank you message + late fee terms]
```

## Inputs
- Business info (name, address, email, phone)
- Client info (name, company, address, email)
- Line items (description, quantity, rate)
- Payment terms and methods
- Tax rate and discount (optional)
- Currency and invoice number format (optional)

## Outputs
- Unique invoice number with configurable format
- Calculated totals (subtotal, discount, tax, total)
- Payment instructions for selected methods (bank, Stripe, PayPal, check)
- Due date with late fee terms
- Professional layout template
- Structured JSON data for PDF generation or API integration
- Email template for invoice delivery

## Level History

- **Lv.1** — Base: Configurable invoice numbering (5 formats), line item calculation with discount and tax, multi-method payment instructions (bank/Stripe/PayPal/check), due date calculation with late fee terms, professional layout template, structured JSON output, email delivery template. (Origin: MemStack v3.2, Mar 2026)
