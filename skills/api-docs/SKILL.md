---
name: memstack-api-docs
description: "Use when the user says 'api-docs', 'fetch docs', 'current API', 'chub', or when CC is about to write code that calls an external API (Supabase, Stripe, SendGrid, Railway, Netlify, Anthropic, etc.). Fetches current API documentation via Context Hub before writing API-calling code. Do NOT use for internal project APIs or code explanation."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# 📡 API Docs — Fetching current API documentation...
*Fetches current API documentation via Context Hub before CC writes code that calls external APIs. Ensures code is written against the latest API surface, not stale training data.*

## Activation

When this skill activates, output:

`📡 API Docs — Fetching current API documentation...`

Then execute the protocol below.

## Context Guard

| Context | Status |
|---------|--------|
| **User says "api-docs", "fetch docs", "current API", "chub"** | ACTIVE — full protocol |
| **CC is about to write code calling an external API** | ACTIVE — fetch docs first |
| **User asks about API endpoints, parameters, or responses** | ACTIVE — fetch and summarize |
| **Task involves integrating a new external service** | ACTIVE — fetch docs for that service |
| **User is writing internal project code (no external API)** | DORMANT — do not activate |
| **User is explaining or reading existing API code** | DORMANT — do not activate |
| **User explicitly says "skip docs" or "I know the API"** | DORMANT — respect override |

## Anti-Rationalization

| Thought | Correction |
|---------|------------|
| "I know this API from training data" | Training data may be outdated. Fetch current docs. |
| "It's just one endpoint, I remember it" | One wrong parameter wastes more time than a quick fetch. |
| "chub isn't installed, skip it" | Log the warning and continue — but tell the user to install it. |
| "I'll fetch docs after writing the code" | No. Docs BEFORE code. Always. |

## Prerequisites

Context Hub (`chub`) must be installed globally:

```bash
npm install -g @aisuite/chub
```

If `chub` is not installed, the skill logs a warning and continues without fetching. It does NOT block the task.

## Supported APIs

| API | chub identifier | Common endpoints |
|-----|----------------|-----------------|
| **Supabase** | `supabase` | auth, database, storage, edge-functions, realtime |
| **Stripe** | `stripe` | charges, customers, subscriptions, invoices, webhooks |
| **SendGrid** | `sendgrid` | mail/send, contacts, templates, stats |
| **Railway** | `railway` | deployments, services, variables, domains |
| **Netlify** | `netlify` | sites, deploys, forms, functions, dns |
| **Anthropic** | `anthropic` | messages, models, tool-use, streaming |
| **OpenAI** | `openai` | chat/completions, embeddings, assistants, files |
| **Vercel** | `vercel` | deployments, domains, env, projects |
| **Cloudflare** | `cloudflare` | workers, dns, zones, cache, r2 |
| **Firebase** | `firebase` | auth, firestore, storage, hosting, functions |
| **Resend** | `resend` | emails, domains, api-keys |
| **Twilio** | `twilio` | messages, calls, verify, conversations |
| **GitHub** | `github` | repos, pulls, issues, actions, webhooks |

## Protocol

### Step 1: Detect APIs

Scan the current task and codebase for external API references:

1. Check the user's request for API mentions
2. Scan relevant source files for import statements and API client usage:
   ```bash
   grep -rn "import.*supabase\|import.*stripe\|import.*sendgrid\|import.*anthropic\|import.*openai\|import.*@netlify\|import.*@railway\|import.*@vercel\|import.*firebase\|import.*resend\|import.*twilio" src/ lib/ app/ pages/ api/ 2>/dev/null | head -20
   ```
3. Check environment variables for API keys:
   ```bash
   grep -n "SUPABASE\|STRIPE\|SENDGRID\|ANTHROPIC\|OPENAI\|NETLIFY\|RAILWAY\|VERCEL\|FIREBASE\|RESEND\|TWILIO" .env .env.local .env.example 2>/dev/null | head -20
   ```

### Step 2: Check chub availability

```bash
which chub 2>/dev/null && chub --version || echo "CHUB_NOT_INSTALLED"
```

If `CHUB_NOT_INSTALLED`:
- Log: `⚠️ Context Hub (chub) not installed. Install with: npm install -g @aisuite/chub`
- Continue the task without fetching docs
- Note in output that API code is based on training data, not current docs

### Step 3: Fetch documentation

For each detected API, fetch the relevant endpoint documentation:

```bash
# Fetch specific endpoint docs
chub get <api>/<endpoint>

# Examples:
chub get stripe/subscriptions
chub get supabase/auth
chub get anthropic/messages
chub get sendgrid/mail-send
chub get netlify/deploys
```

If fetching a specific endpoint:
```bash
chub get <api>/<endpoint>/<sub-endpoint>
```

### Step 4: Inject into context

After fetching, summarize the key information before writing code:

1. **Endpoint URL and method** (GET, POST, PUT, DELETE)
2. **Required parameters** and their types
3. **Authentication method** (Bearer token, API key header, etc.)
4. **Response shape** (success and error formats)
5. **Rate limits** if documented
6. **Breaking changes** or deprecation notices

### Step 5: Write code

Only after docs are fetched and summarized, proceed to write the API-calling code. Reference specific documentation sections in code comments where helpful:

```typescript
// Per Stripe API docs (fetched via chub):
// POST /v1/subscriptions — requires customer, price[], payment_behavior
```

### Step 6: Report

After fetching docs, report what was loaded:

```
📡 API Docs — Loaded

APIs detected: [list]
Docs fetched: [count] endpoints
Source: Context Hub (chub) — current as of [date]
Status: Ready to write code against current API surface
```

If chub was unavailable:
```
📡 API Docs — Fallback mode

APIs detected: [list]
⚠️ chub not installed — using training data (may be outdated)
Install: npm install -g @aisuite/chub
```

## Batch Fetching

When a task involves multiple APIs, fetch all docs in parallel:

```bash
# Fetch multiple endpoints
chub get stripe/subscriptions &
chub get supabase/auth &
chub get sendgrid/mail-send &
wait
```

## Custom API Sources

If the project uses APIs not in the chub registry, check for local documentation:

```bash
# Check for OpenAPI/Swagger specs
ls docs/api*.yaml docs/api*.json docs/swagger* docs/openapi* 2>/dev/null

# Check for API documentation in the project
ls docs/API* README*api* 2>/dev/null
```

## Attribution

Built on Context Hub by Andrew Ng / AISuite team — github.com/andrewyng/context-hub — MIT License

## Level History

- **Lv.1** — Base: Context Hub integration for 13 supported APIs, auto-detection from imports and env vars, graceful fallback when chub is unavailable, batch fetching, custom API source support. (Origin: MemStack Pro v3.3, Mar 2026)
