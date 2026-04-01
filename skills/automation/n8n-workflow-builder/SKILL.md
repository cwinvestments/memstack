---
name: memstack-automation-n8n-workflow-builder
description: "Use this skill when the user says 'n8n workflow', 'build a workflow', 'automation workflow', 'connect services', or needs visual workflow design with node mapping, data transformations, and error handling for n8n. Do NOT use for standalone webhook endpoints or cron jobs."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# n8n Workflow Builder — Designing automation workflow...
*Designs visual n8n workflows with trigger selection, node mapping, data transformations, error handling, and webhook integration.*

## Activation

When this skill activates, output:

`n8n Workflow Builder — Designing automation workflow...`

Then execute the protocol below.

## Context Guard

| Context | Status |
|---------|--------|
| User says "n8n workflow", "build a workflow", "automation workflow" | ACTIVE |
| User says "connect services" or wants visual automation | ACTIVE |
| User wants to automate a multi-step process with n8n | ACTIVE |
| User needs a standalone webhook endpoint | DORMANT — use Webhook Designer |
| User needs a cron/scheduled job without n8n | DORMANT — use Cron Scheduler |

## Common Mistakes

| Mistake | Why It's Wrong |
|---------|---------------|
| "One giant workflow" | Workflows over 20 nodes become unmaintainable. Split into sub-workflows with triggers. |
| "No error handling" | Silent failures mean lost data. Every workflow needs an Error Trigger node. |
| "Hardcoded credentials" | Use n8n's credential store — never paste API keys into HTTP Request nodes. |
| "Skip testing with real data" | Test with production-like payloads. Dummy data hides type mismatches and missing fields. |
| "Poll when you can webhook" | Polling wastes resources. If the service supports webhooks, use the Webhook trigger instead. |

## Protocol

### Step 1: Gather Workflow Requirements

If the user hasn't provided details, ask:

> 1. **Trigger** — what starts the workflow? (webhook, schedule, app event, manual)
> 2. **Input** — what data comes in? (payload shape, source service)
> 3. **Actions** — what should happen step-by-step?
> 4. **Output** — where does the result go? (database, API, email, Slack, file)
> 5. **Error handling** — what happens if a step fails?
> 6. **Frequency** — how often does this run? (per event, hourly, daily)

### Step 2: Select Trigger Node

| Trigger Type | n8n Node | When to Use |
|-------------|---------|-------------|
| **Incoming webhook** | Webhook | External service sends data to you |
| **Schedule** | Schedule Trigger | Run at fixed intervals (cron) |
| **App event** | [App] Trigger | Slack message, GitHub PR, Stripe payment, etc. |
| **Manual** | Manual Trigger | Testing or on-demand execution |
| **Email** | Email Trigger (IMAP) | React to incoming emails |
| **File change** | Local File Trigger | Watch a directory for new files |
| **Another workflow** | Execute Workflow Trigger | Sub-workflow called by parent |

**Trigger configuration template:**

```
Trigger: [Node name]
Type: [Webhook / Schedule / App event]
Configuration:
  - [Setting 1: e.g., HTTP Method: POST]
  - [Setting 2: e.g., Path: /webhook/orders]
  - [Setting 3: e.g., Authentication: Header Auth]
Output schema:
  {
    "field1": "type — description",
    "field2": "type — description"
  }
```

### Step 3: Map the Workflow Nodes

Design the node sequence from trigger to output:

**Workflow diagram template:**

```
[Trigger] → [Transform/Filter] → [Action 1] → [Action 2] → [Output]
                                       ↓ (on error)
                                  [Error Handler]
```

**Common node patterns:**

| Pattern | Nodes | Use Case |
|---------|-------|----------|
| **Filter & route** | IF / Switch | Route data based on conditions |
| **Transform** | Set / Code / Item Lists | Reshape data between nodes |
| **Batch process** | SplitInBatches → Loop | Process large datasets without timeout |
| **Merge streams** | Merge | Combine data from parallel branches |
| **Lookup & enrich** | HTTP Request → Merge | Add data from external APIs |
| **Deduplicate** | Code (Set-based check) | Prevent processing the same item twice |

**Node specification template (for each node):**

```
Node [N]: [Name]
Type: [n8n node type]
Purpose: [What this node does]
Input: [What it receives from the previous node]
Configuration:
  - [Key setting 1]
  - [Key setting 2]
Output: [What it passes to the next node]
```

### Step 4: Data Transformations

**Accessing data between nodes:**

```javascript
// Reference previous node output
{{ $json.fieldName }}

// Reference a specific node by name
{{ $('Node Name').item.json.fieldName }}

// Access all items from a node
{{ $('Node Name').all() }}

// Current item index in a loop
{{ $itemIndex }}

// Environment variables
{{ $env.MY_VARIABLE }}
```

**Common transformation patterns:**

| Transformation | Node | Expression Example |
|---------------|------|--------------------|
| Rename field | Set | `newName: {{ $json.oldName }}` |
| Format date | Set / Code | `{{ DateTime.fromISO($json.date).toFormat('yyyy-MM-dd') }}` |
| Filter items | IF | `{{ $json.status === 'active' }}` |
| Concatenate | Set | `{{ $json.first + ' ' + $json.last }}` |
| Parse JSON string | Code | `JSON.parse($json.rawBody)` |
| Map array | Code | `items.map(i => ({ json: { id: i.json.id } }))` |
| Aggregate | Code | `[{ json: { total: items.reduce((s,i) => s + i.json.amount, 0) } }]` |

**Code node template (JavaScript):**

```javascript
// Process all items
const results = [];
for (const item of $input.all()) {
  results.push({
    json: {
      id: item.json.id,
      processed: true,
      // Add transformed fields here
    }
  });
}
return results;
```

### Step 5: Error Handling

**Error handling strategy:**

```
[Main Workflow]
  ├── [Error Trigger] → [Log to DB] → [Send Alert]
  └── [Individual nodes with retry]
```

**Three layers of error handling:**

| Layer | Implementation | Purpose |
|-------|---------------|---------|
| **Node retry** | Settings → Retry on Fail (max 3, wait 1s) | Transient failures (network, rate limits) |
| **Error Trigger** | Error Trigger node → notification workflow | Catch any unhandled errors |
| **Dead letter** | On error → write to DB/queue for later replay | Don't lose failed items |

**Error Trigger workflow template:**

```
Node 1: Error Trigger
  → Receives: error message, workflow name, node name, execution ID

Node 2: Set (format error)
  → Builds: { workflow, node, error, timestamp, executionUrl }

Node 3: Send alert (Slack / Email / PagerDuty)
  → Message: "Workflow '[name]' failed at node '[node]': [error]"

Node 4: Log to database (optional)
  → Insert error record for tracking and replay
```

### Step 6: Testing & Deployment

**Testing checklist:**
- [ ] Test with real-shaped data (not just `{ "test": true }`)
- [ ] Test the error path (disable a downstream service and verify error handling fires)
- [ ] Test with empty arrays and null values
- [ ] Test with maximum expected payload size
- [ ] Verify credentials are in n8n credential store (not hardcoded)
- [ ] Check timezone settings on Schedule triggers

**Production deployment:**
- [ ] Set workflow to Active
- [ ] Verify webhook URLs are registered in source services
- [ ] Enable execution logging (Settings → Save Execution Progress)
- [ ] Set execution timeout appropriate for workload
- [ ] Tag workflow with version number and description
- [ ] Document the workflow in your team's runbook

## Output Format

```markdown
# n8n Workflow — [Workflow Name]

## Overview
- **Trigger:** [Trigger type and config]
- **Purpose:** [What this workflow automates]
- **Frequency:** [How often it runs]
- **Services connected:** [List of external services]

## Workflow Diagram
[ASCII diagram of node flow]

## Node Specifications
### Node 1: [Trigger]
[Config template from Step 3]

### Node 2: [Transform/Action]
[Config template from Step 3]

[...all nodes...]

## Data Transformations
[Key expressions from Step 4]

## Error Handling
[Strategy from Step 5]

## Testing Checklist
[From Step 6]
```

## Completion

```
n8n Workflow Builder — Complete!

Workflow: [Name]
Trigger: [Type]
Nodes: [Count]
Services connected: [List]
Error handling: [Strategy summary]

Next steps:
1. Create the workflow in n8n using the node specs above
2. Configure credentials in n8n's credential store
3. Test with sample data before activating
4. Activate and verify the first real execution
5. Set up the Error Trigger workflow for monitoring
```

## Level History

- **Lv.1** — Base: Trigger selection (7 types), node mapping with specification templates, data transformation patterns (expressions + Code node), 3-layer error handling (retry, Error Trigger, dead letter), common workflow patterns (filter, batch, merge, deduplicate), testing checklist, production deployment checklist. (Origin: MemStack Pro v3.2, Mar 2026)
