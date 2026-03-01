---
name: financial-model
description: "Use when the user says 'financial model', 'projections', 'revenue forecast', 'unit economics', 'break-even', 'cash flow', or wants to build financial projections for a business."
---

# 📈 Financial Model — Business Financial Projections
*Build monthly revenue projections, unit economics, break-even analysis, scenario modeling, and cash flow forecasts with key metrics dashboards.*

## Activation

When this skill activates, output:

`📈 Financial Model — Building your financial projections...`

| Context | Status |
|---------|--------|
| **User says "financial model", "projections", "revenue forecast"** | ACTIVE |
| **User wants unit economics, break-even, or cash flow analysis** | ACTIVE |
| **User mentions MRR, churn, CAC, LTV, or runway** | ACTIVE |
| **User wants to set pricing (not model revenue)** | DORMANT — see pricing-strategy |
| **User wants to generate an invoice** | DORMANT — see invoice-generator |
| **User wants to scope an MVP (budget is secondary)** | DORMANT — see mvp-scoper |

## Protocol

### Step 1: Gather Inputs

Ask the user for:
- **Business type**: SaaS, e-commerce, service business, marketplace, info product?
- **Revenue streams**: How do you make money? (subscriptions, one-time sales, usage fees, ads)
- **Pricing**: What do you charge? (per plan, per unit, per transaction)
- **Current metrics** (if existing): Current MRR, customer count, churn rate
- **Cost structure**: Major expenses (team, hosting, tools, marketing)
- **Growth assumptions**: How will you acquire customers? Expected growth rate?
- **Funding status**: Bootstrapped, pre-seed, seed, Series A?

### Step 2: Build Monthly Revenue Projections (12 Months)

**SaaS / Subscription Model:**

```
── MONTHLY REVENUE PROJECTION ─────────────

         M1     M2     M3     M4     M5     M6     M7     M8     M9     M10    M11    M12
New       [n]    [n]    [n]    [n]    [n]    [n]    [n]    [n]    [n]    [n]    [n]    [n]
Churned  -[n]   -[n]   -[n]   -[n]   -[n]   -[n]   -[n]   -[n]   -[n]   -[n]   -[n]   -[n]
Active    [n]    [n]    [n]    [n]    [n]    [n]    [n]    [n]    [n]    [n]    [n]    [n]
ARPU     $[x]   $[x]   $[x]   $[x]   $[x]   $[x]   $[x]   $[x]   $[x]   $[x]   $[x]   $[x]
MRR      $[x]   $[x]   $[x]   $[x]   $[x]   $[x]   $[x]   $[x]   $[x]   $[x]   $[x]   $[x]
ARR      $[x]   $[x]   $[x]   $[x]   $[x]   $[x]   $[x]   $[x]   $[x]   $[x]   $[x]   $[x]
```

**Revenue formulas:**
- New customers = marketing spend / CAC (or organic growth rate)
- Churned customers = previous active × monthly churn rate
- Active customers = previous active + new − churned
- MRR = active customers × ARPU
- ARR = MRR × 12

**E-commerce / Transactional Model:**
```
Orders/mo × Average Order Value = Gross Revenue
Gross Revenue − Returns − Refunds = Net Revenue
```

**Service Business:**
```
Billable Hours × Hourly Rate = Revenue
— OR —
Active Clients × Monthly Retainer = Revenue
```

### Step 3: Monthly Expense Projections

```
── MONTHLY EXPENSES ───────────────────────

Category          M1      M2      M3      ...    M12     Type
──────────────────────────────────────────────────────────────
PEOPLE
  Founder salary  $[x]    $[x]    $[x]    ...    $[x]    Fixed
  Engineer #1     $[x]    $[x]    $[x]    ...    $[x]    Fixed
  Contractor      $[x]    $[x]    $[x]    ...    $[x]    Variable
  Benefits/tax    $[x]    $[x]    $[x]    ...    $[x]    % of salary

INFRASTRUCTURE
  Hosting         $[x]    $[x]    $[x]    ...    $[x]    Scales w/ usage
  SaaS tools      $[x]    $[x]    $[x]    ...    $[x]    Fixed (step up)
  Domain/SSL      $[x]    —       —       ...    —       Annual

MARKETING
  Paid ads        $[x]    $[x]    $[x]    ...    $[x]    Variable
  Content         $[x]    $[x]    $[x]    ...    $[x]    Fixed
  Tools           $[x]    $[x]    $[x]    ...    $[x]    Fixed

OPERATIONS
  Legal/accounting $[x]   $[x]    $[x]    ...    $[x]    Fixed
  Insurance       $[x]    —       —       ...    —       Annual
  Office/misc     $[x]    $[x]    $[x]    ...    $[x]    Fixed

──────────────────────────────────────────────────────────────
TOTAL EXPENSES    $[x]    $[x]    $[x]    ...    $[x]
```

**Expense scaling rules:**
- People: Step function — add hires at specific months
- Hosting: Linear with customer count (estimate $/customer/mo)
- Marketing: Set as % of revenue or fixed budget
- SaaS tools: Step up at tier thresholds

### Step 4: Unit Economics

```
── UNIT ECONOMICS ─────────────────────────

Customer Acquisition Cost (CAC):
  Total marketing spend / New customers acquired
  CAC = $[amount]

Lifetime Value (LTV):
  ARPU × (1 / monthly churn rate)
  LTV = $[ARPU] × [months] = $[amount]

  — OR detailed —
  LTV = ARPU × Gross Margin × (1 / churn rate)
  LTV = $[amount]

LTV:CAC Ratio:
  $[LTV] / $[CAC] = [X]:1
  Target: ≥ 3:1 (healthy), ≥ 5:1 (very healthy)
  Below 3:1 → Acquisition is too expensive or LTV too low

CAC Payback Period:
  CAC / (ARPU × Gross Margin)
  Payback = [X] months
  Target: ≤ 12 months (SaaS), ≤ 3 months (e-commerce)

Gross Margin:
  (Revenue − COGS) / Revenue × 100
  GM = [X]%
  Target: ≥ 70% (SaaS), ≥ 40% (e-commerce), ≥ 50% (services)

Monthly Churn Rate:
  Lost customers / Total customers at start of month
  Churn = [X]%
  Target: ≤ 5% monthly (early stage), ≤ 2% (mature)

Net Revenue Retention (NRR):
  (MRR at end − new MRR) / MRR at start × 100
  NRR = [X]%
  Target: ≥ 100% (expansion offsets churn)
```

### Step 5: Break-Even Analysis

```
── BREAK-EVEN ANALYSIS ────────────────────

Fixed Costs (monthly):       $[amount]
Variable Cost per Customer:  $[amount]
Revenue per Customer:        $[amount]
Contribution Margin:         $[revenue − variable cost]

Break-even Customers = Fixed Costs / Contribution Margin
Break-even Customers = [number]

Break-even Revenue = Break-even Customers × Revenue per Customer
Break-even Revenue = $[amount]/month

Current trajectory: Break-even in Month [X]

           Revenue  ─────── Expenses
    $│     /                   /
     │    /              ════/═══ Fixed + Variable
     │   /          ════/
     │  /      ════/
     │ /  ════/
     │/══/──────────────────────── Break-even point
     │/                            Month [X]
     └────────────────────────────────
      M1   M3   M5   M7   M9   M12
```

### Step 6: Scenario Modeling

Build three scenarios:

```
── SCENARIO COMPARISON ────────────────────

                    Conservative   Moderate    Aggressive
──────────────────────────────────────────────────────────
ASSUMPTIONS
Growth rate/mo      [X]%           [X]%        [X]%
Churn rate/mo       [X]%           [X]%        [X]%
CAC                 $[X]           $[X]        $[X]
ARPU                $[X]           $[X]        $[X]
Marketing spend/mo  $[X]           $[X]        $[X]

MONTH 6 METRICS
Active customers    [n]            [n]         [n]
MRR                 $[X]           $[X]        $[X]
Monthly burn        $[X]           $[X]        $[X]
Cash position       $[X]           $[X]        $[X]

MONTH 12 METRICS
Active customers    [n]            [n]         [n]
MRR                 $[X]           $[X]        $[X]
ARR                 $[X]           $[X]        $[X]
Cumulative revenue  $[X]           $[X]        $[X]
Profit/Loss (mo)    $[X]           $[X]        $[X]
Break-even month    [M]            [M]         [M]
Runway remaining    [X] months     [X] months  [X] months
```

**Scenario definitions:**
- **Conservative**: Lower growth, higher churn, higher CAC — what if things go slowly?
- **Moderate**: Realistic assumptions based on comparable companies
- **Aggressive**: Higher growth, lower churn, lower CAC — what if things go very well?

### Step 7: Cash Flow & Runway

```
── CASH FLOW PROJECTION ───────────────────

         M1      M2      M3      ...    M12
─────────────────────────────────────────────
Revenue  $[x]    $[x]    $[x]    ...    $[x]
Expenses $[x]    $[x]    $[x]    ...    $[x]
─────────────────────────────────────────────
Net      $[x]    $[x]    $[x]    ...    $[x]
─────────────────────────────────────────────
Cash     $[x]    $[x]    $[x]    ...    $[x]
         (starting cash + cumulative net)

── RUNWAY CALCULATION ─────────────────────

Starting cash:           $[amount]
Average monthly burn:    $[amount]
Months of runway:        [X] months
Cash-out date:           [month/year]

If runway < 6 months → URGENT: reduce burn or raise funds
If runway 6-12 months → START fundraising or path to profit
If runway > 12 months → COMFORTABLE: focus on growth
```

### Step 8: Key Metrics Dashboard

```
── KEY METRICS DASHBOARD ──────────────────

REVENUE
  MRR:              $[amount]    ([+X]% MoM)
  ARR:              $[amount]
  Revenue growth:   [X]% MoM

CUSTOMERS
  Total active:     [n]
  New this month:   [n]
  Churned:          [n]
  Net new:          [n]

UNIT ECONOMICS
  CAC:              $[amount]
  LTV:              $[amount]
  LTV:CAC:          [X]:1
  Payback period:   [X] months

PROFITABILITY
  Gross margin:     [X]%
  Net margin:       [X]%
  Monthly burn:     $[amount]
  Runway:           [X] months

EFFICIENCY
  Revenue per employee:  $[amount]
  CAC payback:           [X] months
  NRR:                   [X]%
  Quick ratio:           [X] (new MRR / lost MRR)
```

### Step 9: Output

Present the complete financial model:

```
━━━ FINANCIAL MODEL: [Business Name] ━━━━━━

── REVENUE PROJECTIONS (12 Mo) ────────────
[monthly revenue table]

── EXPENSE PROJECTIONS (12 Mo) ────────────
[monthly expense table by category]

── UNIT ECONOMICS ─────────────────────────
CAC: $[X]  |  LTV: $[X]  |  LTV:CAC: [X]:1
Payback: [X] mo  |  Gross Margin: [X]%

── BREAK-EVEN ─────────────────────────────
Break-even customers: [N]
Break-even revenue: $[X]/mo
Projected break-even: Month [X]

── SCENARIOS ──────────────────────────────
Conservative: ARR $[X] by M12, break-even M[X]
Moderate:     ARR $[X] by M12, break-even M[X]
Aggressive:   ARR $[X] by M12, break-even M[X]

── CASH FLOW & RUNWAY ─────────────────────
Starting cash: $[X]
Monthly burn: $[X]
Runway: [X] months

── METRICS DASHBOARD ──────────────────────
[key metrics summary]

── ASSUMPTIONS & RISKS ────────────────────
[list of key assumptions with sensitivity notes]
```

## Inputs
- Business type and revenue model
- Pricing and current metrics (if existing)
- Cost structure (people, infrastructure, marketing)
- Growth and churn assumptions
- Starting cash and funding status

## Outputs
- 12-month revenue projection (monthly granularity)
- 12-month expense projection by category
- Unit economics (CAC, LTV, LTV:CAC, payback period, gross margin, churn, NRR)
- Break-even analysis with customer and revenue targets
- 3-scenario comparison (conservative, moderate, aggressive)
- Cash flow projection with runway calculation
- Key metrics dashboard (MRR, ARR, growth, efficiency)

## Level History

- **Lv.1** — Base: 12-month revenue/expense projections (SaaS, e-commerce, service models), unit economics (CAC, LTV, LTV:CAC, payback, margins, churn, NRR), break-even analysis, 3-scenario modeling (conservative/moderate/aggressive), cash flow with runway calculation, key metrics dashboard. (Origin: MemStack v3.2, Mar 2026)
