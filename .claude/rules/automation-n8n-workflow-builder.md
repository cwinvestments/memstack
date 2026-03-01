---
name: n8n-workflow-builder
description: "Use when the user says 'n8n workflow', 'build a workflow', 'automation workflow', 'n8n', 'workflow builder', or wants to design an automated workflow with triggers, processing, and outputs."
---


# ⚙️ N8N Workflow Builder — Visual Automation Design
*Design complete n8n workflows with node mapping, data transformations, error handling, and importable JSON.*

## Activation

When this skill activates, output:

`⚙️ N8N Workflow Builder — Designing your automation workflow...`

| Context | Status |
|---------|--------|
| **User says "n8n workflow", "build a workflow", "automation"** | ACTIVE |
| **User wants to connect services with trigger → process → output** | ACTIVE |
| **User mentions n8n nodes, credentials, or workflow JSON** | ACTIVE |
| **User wants a webhook endpoint (not a full workflow)** | DORMANT — see webhook-designer |
| **User wants a cron job (not n8n scheduled)** | DORMANT — see cron-scheduler |
| **User wants an API-to-API integration (not visual workflow)** | DORMANT — see api-integration |

## Protocol

### Step 1: Gather Inputs

Ask the user for:
- **Trigger event**: What starts the workflow? (webhook, schedule, app event, manual)
- **Data source**: Where does input data come from? (API, database, email, file, form)
- **Desired output**: What should happen at the end? (send email, update database, post to Slack, create record)
- **Integrations needed**: Which services? (Google Sheets, Slack, Stripe, GitHub, Notion, Airtable, etc.)
- **Frequency**: One-time, on-demand, or recurring? If recurring, how often?

### Step 2: Design Workflow Nodes

Map the workflow as a node chain:

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   TRIGGER    │───→│   PROCESS    │───→│  TRANSFORM   │───→│    OUTPUT    │
│              │    │              │    │              │    │              │
│ [node type]  │    │ [node type]  │    │ [node type]  │    │ [node type]  │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
```

For each node, specify:

| Node | Type | Purpose | Config |
|------|------|---------|--------|
| 1. Trigger | [Webhook/Schedule/App Trigger] | [what starts it] | [settings] |
| 2. Fetch | [HTTP Request/App Node] | [get data] | [endpoint, auth] |
| 3. Process | [Code/Set/IF/Switch] | [transform/filter] | [logic] |
| 4. Output | [App Node/HTTP Request] | [deliver result] | [settings] |

Include branching where needed:
- **IF nodes**: For conditional paths (e.g., if status === 'paid', send receipt; else send reminder)
- **Switch nodes**: For multi-path routing
- **Merge nodes**: For combining parallel branches

### Step 3: Map Data Transformations

For each connection between nodes, define the field mapping:

```
── Node 1 → Node 2 ────────────────────────
Source Field          →  Target Field          Transform
─────────────────────────────────────────────
{{ $json.email }}     →  to                    direct
{{ $json.name }}      →  subject               template: "Hello {{ $json.name }}"
{{ $json.amount }}    →  price                 Number: {{ $json.amount / 100 }}
{{ $json.created }}   →  date                  Format: {{ DateTime.fromISO($json.created).toFormat('yyyy-MM-dd') }}
```

Common transformations:
- **String**: `.toLowerCase()`, `.trim()`, template literals
- **Number**: Division (cents to dollars), rounding, formatting
- **Date**: ISO parse, format conversion, timezone handling
- **Array**: `.map()`, `.filter()`, `.reduce()` in Code node
- **Object**: Spread, pick fields, rename keys

### Step 4: Error Handling

Design failure paths for each critical node:

```
┌──────────────┐    ┌──────────────┐
│  Main Node   │──✗─│ Error Branch │
│              │    │              │
│  [action]    │    │ • Log error  │
│              │    │ • Notify     │
│              │    │ • Retry/Skip │
└──────────────┘    └──────────────┘
```

**Error handling strategy per node:**

| Node | On Failure | Retry? | Fallback |
|------|-----------|--------|----------|
| HTTP Request | Log + retry | 3x with 5s backoff | Send alert, skip item |
| Database | Log + alert | 1x | Queue for manual review |
| External API | Log + retry | 3x with exponential | Use cached data |
| Webhook delivery | Log + retry | 5x with backoff | Dead letter queue |

**Error notification node** (add to every workflow):
- Send to Slack channel, email, or webhook on any unhandled error
- Include: workflow name, node that failed, error message, input data

### Step 5: Credential Setup

For each integration, provide setup guidance:

```
── CREDENTIALS NEEDED ─────────────────────

1. [Service Name]
   Type: [API Key / OAuth2 / Basic Auth]
   Setup:
     a. Go to [URL]
     b. Create [API key / OAuth app]
     c. Copy [key/secret/token]
     d. In n8n: Settings → Credentials → Add → [Service]
     e. Paste credentials
   Scopes needed: [list required scopes]
   Notes: [rate limits, expiration, rotation]

2. [Service Name]
   ...
```

### Step 6: Testing Approach

**Test each node individually:**
1. Run trigger node alone — verify it produces expected data shape
2. Test each processing node with pinned test data
3. Verify data transformations match expected output
4. Test error paths by deliberately sending bad data

**End-to-end testing:**
1. Execute workflow with test data (use n8n's "Test Workflow" button)
2. Verify each node's output in the execution log
3. Confirm final output in destination system
4. Test with edge cases: empty data, large payloads, special characters
5. Test error recovery: disconnect a service, verify error handling fires

### Step 7: Scheduling

If the workflow runs on a schedule:

```
── SCHEDULE CONFIGURATION ─────────────────

Cron Expression: [expression]
Human Readable: [description]
Timezone: [timezone]

Examples:
  Every 15 minutes:  */15 * * * *
  Every hour:        0 * * * *
  Daily at 9 AM:     0 9 * * *
  Mon-Fri at 8 AM:   0 8 * * 1-5
  First of month:    0 0 1 * *
```

Scheduling considerations:
- Set timezone explicitly (n8n defaults to server timezone)
- Avoid running at exact hour marks (:00) — high API traffic
- For API-heavy workflows, stagger by a few minutes
- Consider overlap: will the previous run finish before next starts?

### Step 8: Output

Present the complete workflow specification:

```
━━━ N8N WORKFLOW: [Workflow Name] ━━━━━━━━━

── OVERVIEW ───────────────────────────────
Trigger: [what starts it]
Purpose: [what it does]
Schedule: [frequency]
Services: [list of integrations]

── NODE MAP ───────────────────────────────
[visual node chain with descriptions]

── NODE DETAILS ───────────────────────────
Node 1: [name] — [type]
  Config: [settings]
  Input: [data shape]
  Output: [data shape]

Node 2: [name] — [type]
  ...

── DATA TRANSFORMATIONS ───────────────────
[field mapping tables]

── ERROR HANDLING ─────────────────────────
[error paths per node]

── CREDENTIALS ────────────────────────────
[setup instructions per service]

── TEST PLAN ──────────────────────────────
[node-by-node + end-to-end tests]

── WORKFLOW JSON ──────────────────────────
[importable n8n JSON or instructions to build]
```

If the workflow is simple enough, provide the actual n8n workflow JSON that can be imported via Settings → Import Workflow.

## Inputs
- Trigger event type
- Data source and format
- Desired output / destination
- Required integrations
- Frequency / schedule

## Outputs
- Visual node map with connections
- Detailed node configurations
- Data transformation mappings between nodes
- Error handling strategy per node
- Credential setup guide per service
- Testing plan (node-by-node + end-to-end)
- Schedule configuration with cron expression
- Importable workflow JSON (when feasible)

## Level History

- **Lv.1** — Base: Node chain design with trigger/process/transform/output mapping, data transformation tables, error handling with retry and fallback paths, credential setup guides, testing approach (node-level + E2E), cron scheduling, importable JSON output format. (Origin: MemStack v3.2, Mar 2026)
