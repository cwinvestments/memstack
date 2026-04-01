---
name: memstack-automation-webhook-designer
description: "Use this skill when the user says 'webhook', 'webhook handler', 'webhook endpoint', 'receive events', 'HMAC verification', 'idempotency', or needs secure webhook handlers with signature verification, retry handling, and dead letter queues. Do NOT use for full n8n workflows or scheduled tasks."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# Webhook Designer — Designing webhook handler...
*Creates secure webhook handlers with endpoint design, payload validation, HMAC signature verification, retry logic, idempotency, logging, and dead letter queues.*

## Activation

When this skill activates, output:

`Webhook Designer — Designing webhook handler...`

Then execute the protocol below.

## Context Guard

| Context | Status |
|---------|--------|
| User says "webhook", "webhook handler", "webhook endpoint" | ACTIVE |
| User says "receive events", "HMAC verification", "idempotency" | ACTIVE |
| User wants to build an endpoint that receives external events | ACTIVE |
| User wants a full n8n automation workflow | DORMANT — use n8n Workflow Builder |
| User wants a scheduled/cron job | DORMANT — use Cron Scheduler |

## Common Mistakes

| Mistake | Why It's Wrong |
|---------|---------------|
| "Skip signature verification" | Without HMAC, anyone can send fake events to your endpoint. Always verify. |
| "Process synchronously" | Long processing blocks the response. Return 200 immediately, process async. |
| "No idempotency" | Senders retry on timeout. Without idempotency keys, you'll process duplicates. |
| "Ignore retry headers" | Senders include retry count and delivery ID. Log them for debugging. |
| "Return detailed errors" | Never expose internals. Return 200 (accepted) or 400 (bad request), nothing more. |

## Protocol

### Step 1: Gather Webhook Requirements

If the user hasn't provided details, ask:

> 1. **Source** — what service sends the webhook? (Stripe, GitHub, Shopify, custom)
> 2. **Events** — which events do you need to handle? (e.g., payment.completed, push)
> 3. **Payload** — what does the payload look like? (JSON schema or example)
> 4. **Auth** — how does the source authenticate? (HMAC, bearer token, IP whitelist)
> 5. **Processing** — what should happen when an event arrives?
> 6. **Framework** — what's your stack? (Next.js, Express, FastAPI, etc.)

### Step 2: Design Endpoint

**Endpoint pattern:**

```
POST /api/webhooks/{source}
Headers:
  Content-Type: application/json
  X-Webhook-Signature: {hmac_signature}
  X-Webhook-ID: {delivery_id}
  X-Webhook-Timestamp: {unix_timestamp}
Body: {event payload}

Response: 200 OK (within 5 seconds)
```

**Handler flow:**

```
Request received
  ├── 1. Read raw body (before JSON parsing)
  ├── 2. Verify signature (HMAC-SHA256)
  │     └── Fail → 401 Unauthorized (log attempt)
  ├── 3. Parse JSON payload
  │     └── Fail → 400 Bad Request
  ├── 4. Check idempotency (delivery ID seen before?)
  │     └── Duplicate → 200 OK (skip processing)
  ├── 5. Validate event type (is it one we handle?)
  │     └── Unknown → 200 OK (acknowledge but ignore)
  ├── 6. Return 200 OK immediately
  └── 7. Process event asynchronously
        └── Fail → Write to dead letter queue
```

### Step 3: Implement Signature Verification

**HMAC-SHA256 verification (most common):**

```typescript
// Next.js / Express example
import crypto from 'crypto';

function verifyWebhookSignature(
  rawBody: string,
  signature: string,
  secret: string
): boolean {
  const expected = crypto
    .createHmac('sha256', secret)
    .update(rawBody, 'utf8')
    .digest('hex');

  // Timing-safe comparison prevents timing attacks
  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(expected)
  );
}
```

**Provider-specific patterns:**

| Provider | Header | Algorithm | Prefix |
|----------|--------|-----------|--------|
| Stripe | `Stripe-Signature` | HMAC-SHA256 | `t=timestamp,v1=signature` |
| GitHub | `X-Hub-Signature-256` | HMAC-SHA256 | `sha256=` |
| Shopify | `X-Shopify-Hmac-Sha256` | HMAC-SHA256 (base64) | None |
| Twilio | `X-Twilio-Signature` | HMAC-SHA1 (base64) | None |
| Slack | `X-Slack-Signature` | HMAC-SHA256 | `v0=` |
| Custom | `X-Webhook-Signature` | HMAC-SHA256 (hex) | None |

**Timestamp validation (replay protection):**

```typescript
function verifyTimestamp(timestamp: number, toleranceSeconds = 300): boolean {
  const now = Math.floor(Date.now() / 1000);
  return Math.abs(now - timestamp) <= toleranceSeconds;
}
```

### Step 4: Implement Idempotency

```typescript
// Using a database table for idempotency
async function isProcessed(deliveryId: string): Promise<boolean> {
  const existing = await db.webhookDeliveries.findUnique({
    where: { deliveryId }
  });
  return !!existing;
}

async function markProcessed(deliveryId: string, event: string): Promise<void> {
  await db.webhookDeliveries.create({
    data: {
      deliveryId,
      event,
      processedAt: new Date(),
      // Auto-delete after 7 days to prevent unbounded growth
    }
  });
}
```

**Idempotency table schema:**

```sql
CREATE TABLE webhook_deliveries (
  delivery_id  VARCHAR(255) PRIMARY KEY,
  event_type   VARCHAR(100) NOT NULL,
  processed_at TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
  payload_hash VARCHAR(64),  -- Optional: detect payload changes
  created_at   TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

-- Auto-cleanup: delete records older than 7 days
CREATE INDEX idx_webhook_deliveries_created ON webhook_deliveries(created_at);
```

### Step 5: Build Event Router

```typescript
// Event handler registry
const handlers: Record<string, (payload: any) => Promise<void>> = {
  'payment.completed': handlePaymentCompleted,
  'payment.failed':    handlePaymentFailed,
  'customer.created':  handleCustomerCreated,
  // Add handlers as needed
};

async function routeEvent(eventType: string, payload: any): Promise<void> {
  const handler = handlers[eventType];
  if (!handler) {
    console.log(`Unhandled event type: ${eventType}`);
    return; // Acknowledge but don't process
  }
  await handler(payload);
}
```

**Event handler template:**

```typescript
async function handlePaymentCompleted(payload: any): Promise<void> {
  // 1. Extract relevant data
  const { id, amount, customerId } = payload;

  // 2. Validate required fields
  if (!id || !amount || !customerId) {
    throw new Error('Missing required fields in payment.completed');
  }

  // 3. Execute business logic
  await updateOrderStatus(id, 'paid');
  await sendReceiptEmail(customerId, amount);

  // 4. Log success
  console.log(`Processed payment ${id} for $${amount / 100}`);
}
```

### Step 6: Dead Letter Queue

When async processing fails after retries, write to a dead letter queue:

```typescript
async function processWithRetry(
  deliveryId: string,
  eventType: string,
  payload: any,
  maxRetries = 3
): Promise<void> {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      await routeEvent(eventType, payload);
      return; // Success
    } catch (error) {
      if (attempt === maxRetries) {
        await writeToDeadLetter(deliveryId, eventType, payload, error);
        // Alert: send notification to ops team
      }
      await sleep(attempt * 1000); // Exponential backoff
    }
  }
}
```

**Dead letter table:**

```sql
CREATE TABLE webhook_dead_letters (
  id           SERIAL PRIMARY KEY,
  delivery_id  VARCHAR(255) NOT NULL,
  event_type   VARCHAR(100) NOT NULL,
  payload      JSONB        NOT NULL,
  error        TEXT         NOT NULL,
  attempts     INTEGER      NOT NULL DEFAULT 3,
  replayed     BOOLEAN      NOT NULL DEFAULT FALSE,
  created_at   TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);
```

### Step 7: Logging & Monitoring

**Structured logging for every webhook:**

```typescript
function logWebhook(phase: string, data: Record<string, any>): void {
  console.log(JSON.stringify({
    type: 'webhook',
    phase,        // 'received' | 'verified' | 'processed' | 'failed'
    timestamp: new Date().toISOString(),
    ...data
  }));
}

// Usage:
logWebhook('received', { deliveryId, eventType, source: 'stripe' });
logWebhook('verified', { deliveryId, signatureValid: true });
logWebhook('processed', { deliveryId, durationMs: 45 });
logWebhook('failed', { deliveryId, error: err.message, attempt: 3 });
```

**Monitoring checklist:**
- [ ] Alert on: >5% failure rate over 15 minutes
- [ ] Alert on: dead letter queue depth > 10
- [ ] Alert on: no events received in [expected window]
- [ ] Dashboard: events/minute by type, success rate, p95 latency
- [ ] Retention: keep webhook logs for 30 days minimum

## Output Format

```markdown
# Webhook Handler — [Source] Events

## Endpoint
- **URL:** POST /api/webhooks/[source]
- **Auth:** [HMAC-SHA256 / Bearer / IP whitelist]
- **Events handled:** [List]

## Handler Flow
[Flow diagram from Step 2]

## Signature Verification
[Code from Step 3]

## Idempotency
[Schema + code from Step 4]

## Event Handlers
[Router + handler templates from Step 5]

## Error Recovery
[Dead letter queue from Step 6]

## Monitoring
[Logging + alerts from Step 7]
```

## Completion

```
Webhook Designer — Complete!

Source: [Service name]
Endpoint: POST /api/webhooks/[source]
Events handled: [Count]
Auth method: [HMAC-SHA256 / etc.]
Idempotency: Delivery ID based
Dead letter: Database-backed

Next steps:
1. Implement the handler using the code templates above
2. Store the webhook secret in environment variables
3. Register the webhook URL in the source service
4. Send a test event and verify end-to-end
5. Set up monitoring alerts
```

## Level History

- **Lv.1** — Base: Endpoint design with handler flow, HMAC-SHA256 signature verification (6 provider patterns), timestamp replay protection, delivery-ID idempotency with DB schema, event router with handler registry, dead letter queue with retry/backoff, structured logging, monitoring checklist. (Origin: MemStack Pro v3.2, Mar 2026)
