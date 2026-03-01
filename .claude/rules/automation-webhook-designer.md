---
name: webhook-designer
description: "Use when the user says 'webhook', 'webhook handler', 'webhook endpoint', 'receive webhooks', 'webhook security', or needs to build a secure webhook receiver with validation and idempotency."
---


# 🪝 Webhook Designer — Secure Webhook Handler
*Build production-grade webhook endpoints with signature verification, idempotency, retry handling, and dead letter queues.*

## Activation

When this skill activates, output:

`🪝 Webhook Designer — Designing your webhook handler...`

| Context | Status |
|---------|--------|
| **User says "webhook", "webhook handler", "webhook endpoint"** | ACTIVE |
| **User needs to receive events from an external service** | ACTIVE |
| **User mentions HMAC, signature verification, or idempotency** | ACTIVE |
| **User wants to send webhooks (not receive)** | ACTIVE — design outbound delivery |
| **User wants a full n8n workflow (webhook is just the trigger)** | DORMANT — see n8n-workflow-builder |
| **User wants a scheduled task (not event-driven)** | DORMANT — see cron-scheduler |

## Protocol

### Step 1: Gather Inputs

Ask the user for:
- **Event type**: What event triggers the webhook? (payment completed, form submitted, deploy finished, etc.)
- **Source system**: Who sends it? (Stripe, GitHub, Shopify, SendGrid, custom)
- **Target system**: What should happen when received? (update database, send notification, trigger pipeline)
- **Payload format**: JSON? Form-encoded? Known schema?
- **Runtime**: Express, Next.js API route, Fastify, serverless function?

### Step 2: Design Webhook Endpoint

```javascript
// Route: POST /api/webhooks/[source]
// Auth: Signature verification (no bearer token)
// Rate limit: Standard or elevated for known webhook sources

router.post('/api/webhooks/[source]', async (req, res) => {
  // 1. Verify signature
  // 2. Parse and validate payload
  // 3. Check idempotency
  // 4. Process event
  // 5. Return 200 quickly
});
```

**Design decisions:**
- Respond with 200 immediately, process asynchronously if > 5s work
- Always return 200 for valid signatures (even if event is ignored)
- Return 400 only for malformed requests, 401 for bad signatures
- Log the raw body before any processing for debugging

### Step 3: Signature Verification

Provide code for the specific source system:

**HMAC-SHA256 pattern (Stripe, GitHub, Shopify):**

```javascript
const crypto = require('crypto');

function verifySignature(payload, signature, secret) {
  const expected = crypto
    .createHmac('sha256', secret)
    .update(payload, 'utf8')
    .digest('hex');

  // Timing-safe comparison prevents timing attacks
  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(expected)
  );
}
```

**Source-specific patterns:**
- **Stripe**: `stripe.webhooks.constructEvent(body, sig, endpointSecret)`
- **GitHub**: `X-Hub-Signature-256` header, `sha256=` prefix
- **Shopify**: `X-Shopify-Hmac-SHA256` header, base64 encoding
- **SendGrid**: Event Webhook signature verification
- **Custom**: Document the signing algorithm used

**Additional security layers:**
- Verify `Content-Type` header matches expected format
- Reject requests with missing or empty signature headers
- Log failed verification attempts (potential attack indicator)

### Step 4: Payload Validation

Define the expected schema:

```javascript
// Zod schema example
const WebhookPayload = z.object({
  event: z.enum(['payment.completed', 'payment.failed', 'refund.created']),
  data: z.object({
    id: z.string(),
    amount: z.number(),
    currency: z.string().length(3),
    customer_email: z.string().email(),
    metadata: z.record(z.unknown()).optional(),
  }),
  timestamp: z.string().datetime(),
  webhook_id: z.string(), // For idempotency
});

// Validate
const result = WebhookPayload.safeParse(req.body);
if (!result.success) {
  console.error('Invalid webhook payload:', result.error.issues);
  return res.status(400).json({ error: 'Invalid payload' });
}
```

**Validation rules:**
- Validate structure, not just presence (type-check every field)
- Allow unknown fields (source APIs add new fields without notice)
- Log validation failures with the raw payload for debugging
- Version your schema — source APIs evolve

### Step 5: Idempotency Handling

Prevent duplicate processing when webhooks are retried:

```javascript
async function isProcessed(eventId) {
  const result = await db.query(
    'SELECT id FROM processed_webhooks WHERE event_id = $1',
    [eventId]
  );
  return result.rows.length > 0;
}

async function markProcessed(eventId, eventType) {
  await db.query(
    `INSERT INTO processed_webhooks (event_id, event_type, processed_at)
     VALUES ($1, $2, NOW())
     ON CONFLICT (event_id) DO NOTHING`,
    [eventId, eventType]
  );
}

// In handler:
if (await isProcessed(event.id)) {
  console.log(`Duplicate webhook ignored: ${event.id}`);
  return res.status(200).json({ status: 'already_processed' });
}
// ... process event ...
await markProcessed(event.id, event.type);
```

**Idempotency table:**

```sql
CREATE TABLE processed_webhooks (
  id SERIAL PRIMARY KEY,
  event_id VARCHAR(255) UNIQUE NOT NULL,
  event_type VARCHAR(100),
  processed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  payload JSONB -- optional: store for debugging
);

-- Cleanup old records (keep 30 days)
CREATE INDEX idx_processed_webhooks_date ON processed_webhooks(processed_at);
```

### Step 6: Retry Logic

**Inbound retries (receiving):**
- Source systems retry on non-2xx responses
- Stripe: Retries up to 3 days with exponential backoff
- GitHub: Retries for 3 days
- Always return 200 quickly to prevent retries for successfully received events

**Outbound retries (if you're sending webhooks):**

```javascript
async function deliverWebhook(url, payload, attempt = 1, maxAttempts = 5) {
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
      signal: AbortSignal.timeout(10000), // 10s timeout
    });

    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return { success: true, attempt };
  } catch (err) {
    if (attempt >= maxAttempts) {
      await sendToDeadLetterQueue(url, payload, err.message);
      return { success: false, attempt, error: err.message };
    }

    const delay = Math.min(1000 * Math.pow(2, attempt), 30000); // Max 30s
    await new Promise(r => setTimeout(r, delay));
    return deliverWebhook(url, payload, attempt + 1, maxAttempts);
  }
}
```

**Dead letter queue:**
- Store failed deliveries in a table or queue
- Include: URL, payload, error, attempt count, timestamp
- Review and retry manually or with a separate cron job

### Step 7: Logging

What to log for every webhook event:

```javascript
const logEntry = {
  webhook_id: event.id,
  event_type: event.type,
  source: 'stripe',
  received_at: new Date().toISOString(),
  signature_valid: true,
  payload_valid: true,
  processing_status: 'success', // or 'failed', 'skipped', 'duplicate'
  processing_time_ms: endTime - startTime,
  error: null, // or error message
};

console.log(JSON.stringify(logEntry));
```

**Logging levels:**
- **INFO**: Successful processing, duplicate skipped
- **WARN**: Unknown event type (ignored), payload validation failed
- **ERROR**: Signature verification failed, processing error, delivery failure

**DO NOT log:** Full payload in production (may contain PII). Log event ID and type only, store full payload in the idempotency table for debugging.

### Step 8: Security Checklist

- [ ] **Signature verification**: HMAC with timing-safe comparison
- [ ] **Replay prevention**: Reject events older than 5 minutes (check timestamp)
- [ ] **IP allowlisting**: Restrict to source system's IP ranges (if published)
- [ ] **HTTPS only**: Never accept webhooks over plain HTTP
- [ ] **Rate limiting**: Protect against abuse even on webhook endpoints
- [ ] **No secrets in URLs**: Don't put API keys in the webhook URL path
- [ ] **Idempotency**: Prevent duplicate processing
- [ ] **Input validation**: Validate payload schema before processing
- [ ] **Error isolation**: A bad webhook shouldn't crash your server

**Replay prevention example:**

```javascript
const eventTimestamp = new Date(event.timestamp).getTime();
const now = Date.now();
const fiveMinutes = 5 * 60 * 1000;

if (Math.abs(now - eventTimestamp) > fiveMinutes) {
  console.warn('Webhook replay rejected:', event.id);
  return res.status(401).json({ error: 'Timestamp too old' });
}
```

### Step 9: Testing

Provide curl commands to simulate webhook events:

```bash
# Generate test signature
SECRET="whsec_test_secret"
PAYLOAD='{"event":"payment.completed","data":{"id":"evt_123","amount":5000}}'
SIGNATURE=$(echo -n "$PAYLOAD" | openssl dgst -sha256 -hmac "$SECRET" | cut -d' ' -f2)

# Send test webhook
curl -X POST http://localhost:3000/api/webhooks/stripe \
  -H "Content-Type: application/json" \
  -H "X-Signature: $SIGNATURE" \
  -d "$PAYLOAD"

# Test invalid signature
curl -X POST http://localhost:3000/api/webhooks/stripe \
  -H "Content-Type: application/json" \
  -H "X-Signature: invalid_signature" \
  -d "$PAYLOAD"

# Test duplicate (send same event twice)
curl -X POST ... # same as above, expect "already_processed"
```

### Step 10: Output

Present the complete webhook handler:

```
━━━ WEBHOOK HANDLER: [Source] Events ━━━━━━

── ENDPOINT ───────────────────────────────
Route: POST /api/webhooks/[source]
Auth: HMAC-SHA256 signature
Events handled: [list]

── CODE ───────────────────────────────────
[complete handler implementation]

── SCHEMA ─────────────────────────────────
[Zod or JSON Schema for payload validation]

── IDEMPOTENCY TABLE ──────────────────────
[SQL migration]

── SECURITY ───────────────────────────────
[checklist with implementation status]

── TEST COMMANDS ──────────────────────────
[curl commands for testing]
```

## Inputs
- Event type and source system
- Target system / processing logic
- Payload format and schema
- Runtime environment
- Security requirements

## Outputs
- Complete webhook handler code
- Signature verification implementation
- Payload validation schema (Zod/JSON Schema)
- Idempotency table migration and handler
- Retry logic with dead letter queue
- Structured logging configuration
- Security checklist with implementations
- curl test commands for simulation

## Level History

- **Lv.1** — Base: Secure webhook handler with HMAC signature verification (timing-safe), Zod payload validation, idempotency with dedup table, exponential backoff retry, dead letter queue, structured logging, replay prevention, security checklist, curl test commands. (Origin: MemStack v3.2, Mar 2026)
