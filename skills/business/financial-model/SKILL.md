---
name: memstack-business-financial-model
description: "Use this skill when the user says 'financial model', 'projections', 'revenue forecast', 'unit economics', 'break-even', 'cash flow', or mentions MRR, churn, CAC, LTV, or runway. Builds monthly projections with scenario modeling. Do NOT use for pricing strategy or invoice generation."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# Financial Model — Building financial projections...
*Builds monthly revenue projections, expense forecasts, unit economics (CAC, LTV, payback), break-even analysis, cash flow tracking, and scenario modeling (best/base/worst).*

## Activation

When this skill activates, output:

`Financial Model — Building financial projections...`

Then execute the protocol below.

## Context Guard

| Context | Status |
|---------|--------|
| User says "financial model", "projections", "revenue forecast" | ACTIVE |
| User mentions MRR, churn, CAC, LTV, runway, or break-even | ACTIVE |
| User wants to forecast revenue, expenses, or cash flow | ACTIVE |
| User wants to set pricing tiers | DORMANT — use Pricing Strategy |
| User wants to generate an invoice | DORMANT — use Invoice Generator |

## Common Mistakes

| Mistake | Why It's Wrong |
|---------|---------------|
| "Hockey stick revenue" | Realistic projections beat optimistic fantasies. Start conservative, model scenarios. |
| "Forget to model churn" | SaaS without churn modeling is fiction. Even 3% monthly churn compounds fast. |
| "Revenue only, no expenses" | Revenue without expenses is a dream. Model all costs to see actual profitability. |
| "One scenario only" | A single forecast is a guess. Model best/base/worst to understand the range. |
| "Skip unit economics" | If CAC > LTV, growth loses money. Unit economics tell you if the business model works. |

## Protocol

### Step 1: Gather Business Data

If the user hasn't provided details, ask:

> 1. **Business model** — SaaS, e-commerce, service, marketplace, or other?
> 2. **Revenue streams** — subscriptions, one-time sales, services, ads?
> 3. **Current numbers** — existing revenue, customers, growth rate?
> 4. **Pricing** — price points, tiers, average revenue per user?
> 5. **Costs** — known fixed and variable costs?
> 6. **Funding** — bootstrapped or funded? Current cash balance?

### Step 2: Revenue Model

**SaaS / Subscription revenue:**

```
Month N Revenue = (Previous customers - Churned + New) × ARPU

Where:
- Previous customers: end of prior month
- Churned: Previous × monthly churn rate
- New: Acquired through marketing/sales
- ARPU: Average Revenue Per User (monthly)
```

| Month | Starting | New | Churned | Ending | MRR | ARR |
|-------|---------|-----|---------|--------|-----|-----|
| 1 | 0 | [X] | 0 | [X] | $[X] | — |
| 2 | [X] | [X] | [X] | [X] | $[X] | — |
| 3 | [X] | [X] | [X] | [X] | $[X] | — |
| ... | | | | | | |
| 12 | [X] | [X] | [X] | [X] | $[X] | $[X] |

**E-commerce / Transaction revenue:**

```
Monthly Revenue = Visitors × Conversion Rate × Average Order Value

Where:
- Visitors: Monthly unique visitors (organic + paid)
- Conversion Rate: % of visitors who purchase (target: 1-3%)
- AOV: Average Order Value
```

**Service revenue:**

```
Monthly Revenue = Active Clients × Average Monthly Retainer
  + Project Revenue (one-time)
```

### Step 3: Unit Economics

**Key SaaS metrics:**

```
CAC (Customer Acquisition Cost):
  = Total Sales & Marketing Spend ÷ New Customers Acquired
  Target: recover within 12 months

LTV (Customer Lifetime Value):
  = ARPU × Gross Margin% × (1 ÷ Monthly Churn Rate)
  Example: $50 × 80% × (1 ÷ 0.05) = $800

LTV:CAC Ratio:
  = LTV ÷ CAC
  Target: > 3:1 (every $1 spent acquires $3+ in lifetime value)

Payback Period:
  = CAC ÷ (ARPU × Gross Margin%)
  Example: $200 ÷ ($50 × 80%) = 5 months
  Target: < 12 months
```

**Unit economics table:**

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| ARPU (monthly) | $[X] | — | — |
| Monthly churn rate | [X]% | <5% | [OK / At Risk] |
| CAC | $[X] | — | — |
| LTV | $[X] | >3× CAC | [OK / At Risk] |
| LTV:CAC ratio | [X]:1 | >3:1 | [OK / At Risk] |
| Payback period | [X] months | <12 months | [OK / At Risk] |
| Gross margin | [X]% | >70% (SaaS) | [OK / At Risk] |

### Step 4: Expense Forecast

**Fixed costs (monthly):**

| Category | Monthly Cost | Annual Cost | Notes |
|----------|-------------|-------------|-------|
| Salaries & wages | $[X] | $[X] | [Headcount × avg salary ÷ 12] |
| Office / co-working | $[X] | $[X] | |
| Software & tools | $[X] | $[X] | [List: hosting, SaaS tools, etc.] |
| Insurance | $[X] | $[X] | |
| Legal & accounting | $[X] | $[X] | |
| **Total fixed** | **$[X]** | **$[X]** | |

**Variable costs (scales with revenue):**

| Category | Cost Basis | Monthly Estimate | Notes |
|----------|-----------|-----------------|-------|
| Hosting / infrastructure | [X]% of revenue | $[X] | Scales with users |
| Payment processing | 2.9% + $0.30/txn | $[X] | Stripe standard rate |
| Customer support | $[X] per 100 customers | $[X] | |
| Sales commissions | [X]% of new revenue | $[X] | |
| Marketing spend | $[X] fixed + [X]% of revenue | $[X] | |
| **Total variable** | | **$[X]** | |

**Total monthly burn:**
```
Burn Rate = Fixed Costs + Variable Costs - Revenue
Runway = Cash Balance ÷ Monthly Burn Rate
```

### Step 5: Break-Even Analysis

```
Break-Even Point (customers):
  = Fixed Costs ÷ (ARPU - Variable Cost per Customer)

Break-Even Point (revenue):
  = Fixed Costs ÷ Gross Margin%

Example:
  Fixed costs: $10,000/month
  ARPU: $50/month
  Variable cost per customer: $10/month
  Break-even: $10,000 ÷ ($50 - $10) = 250 customers
```

**Monthly P&L projection:**

| | Mo 1 | Mo 3 | Mo 6 | Mo 12 |
|---|---|---|---|---|
| **Revenue** | $[X] | $[X] | $[X] | $[X] |
| COGS / variable costs | ($[X]) | ($[X]) | ($[X]) | ($[X]) |
| **Gross profit** | $[X] | $[X] | $[X] | $[X] |
| Gross margin % | [X]% | [X]% | [X]% | [X]% |
| Operating expenses | ($[X]) | ($[X]) | ($[X]) | ($[X]) |
| **Net income** | ($[X]) | ($[X]) | $[X] | $[X] |
| Cumulative cash | $[X] | $[X] | $[X] | $[X] |

### Step 6: Scenario Modeling

**Three scenarios:**

| Assumption | Worst Case | Base Case | Best Case |
|-----------|-----------|----------|----------|
| Monthly new customers | [X] | [X] | [X] |
| Monthly churn rate | [X]% | [X]% | [X]% |
| ARPU | $[X] | $[X] | $[X] |
| Marketing spend | $[X] | $[X] | $[X] |
| Hiring timeline | Delayed | On time | Accelerated |

**12-month outcome by scenario:**

| Metric | Worst | Base | Best |
|--------|-------|------|------|
| Customers (Mo 12) | [X] | [X] | [X] |
| MRR (Mo 12) | $[X] | $[X] | $[X] |
| ARR (Mo 12) | $[X] | $[X] | $[X] |
| Monthly burn (avg) | $[X] | $[X] | $[X] |
| Break-even month | Mo [X] | Mo [X] | Mo [X] |
| Runway remaining | [X] months | [X] months | [X] months |
| Cash needed | $[X] | $[X] | $0 |

### Step 7: Cash Flow Summary

**Monthly cash flow:**

| Month | Revenue | Expenses | Net | Cumulative |
|-------|---------|----------|-----|------------|
| 1 | $[X] | $[X] | ($[X]) | $[X] |
| 2 | $[X] | $[X] | ($[X]) | $[X] |
| 3 | $[X] | $[X] | ($[X]) | $[X] |
| ... | | | | |
| 12 | $[X] | $[X] | $[X] | $[X] |

**Key dates:**
- **Cash-flow positive:** Month [X] (when monthly net turns positive)
- **Break-even (cumulative):** Month [X] (when cumulative losses are recovered)
- **Runway exhausted:** Month [X] at current burn (worst case)

## Output Format

```markdown
# Financial Model — [Business Name]

## Revenue Model
[From Step 2 — monthly revenue projections]

## Unit Economics
[From Step 3 — CAC, LTV, payback, margins]

## Expense Forecast
[From Step 4 — fixed + variable costs]

## Break-Even Analysis
[From Step 5 — break-even point + P&L]

## Scenario Analysis
[From Step 6 — worst/base/best]

## Cash Flow
[From Step 7 — monthly cash flow + key dates]

## Key Assumptions
[List every assumption with the value used]
```

## Completion

```
Financial Model — Complete!

Business model: [Type]
12-month ARR (base case): $[X]
Break-even: Month [X]
LTV:CAC ratio: [X]:1
Runway: [X] months
Scenarios modeled: 3 (worst/base/best)

Next steps:
1. Validate assumptions with real data (update monthly)
2. Track actual vs projected monthly
3. If LTV:CAC < 3:1, reduce CAC or increase ARPU before scaling
4. If runway < 6 months, raise capital or cut burn
5. Update the model quarterly with actuals
```

## Level History

- **Lv.1** — Base: Revenue models (SaaS, e-commerce, service), unit economics (CAC, LTV, payback, LTV:CAC, gross margin), expense forecast (fixed + variable), break-even analysis with P&L projection, 3-scenario modeling (worst/base/best), cash flow timeline with key dates (cash-positive, break-even, runway). (Origin: MemStack Pro v3.2, Mar 2026)
