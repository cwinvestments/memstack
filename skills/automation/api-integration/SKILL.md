---
name: memstack-automation-api-integration
description: "Use this skill when the user says 'API integration', 'connect APIs', 'sync data', 'data mapping', 'rate limiting', or needs system-to-system connectors with authentication, rate limit handling, and error recovery. Generates API integration code with authentication (OAuth, API key, JWT), request/response mapping, rate limit handling, error recovery with circuit breakers, and sync monitoring. Do NOT use for visual n8n workflows or webhook receiving."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# API Integration — Building system connector...
*Develops system-to-system connectors with REST/GraphQL patterns, authentication flows, rate limit handling, data mapping, error recovery, and SDK wrapper generation.*

## Activation

When this skill activates, output:

`API Integration — Building system connector...`

Then execute the protocol below.

## Context Guard

| Context | Status |
|---------|--------|
| User says "API integration", "connect APIs", "sync data" | ACTIVE |
| User says "data mapping" or "rate limiting" | ACTIVE |
| User needs to build a connector between two systems | ACTIVE |
| User wants a visual n8n workflow | DORMANT — use n8n Workflow Builder |
| User wants to receive webhooks | DORMANT — use Webhook Designer |

## Common Mistakes

| Mistake | Why It's Wrong |
|---------|---------------|
| "Ignore rate limits" | Getting blocked by the API wastes hours of debugging. Implement rate limiting from day one. |
| "No retry logic" | APIs have transient failures. Without retry + backoff, your sync silently drops data. |
| "Store tokens in code" | Use environment variables or a secrets manager. Tokens in code end up in git history. |
| "Map fields manually every time" | Build a reusable mapping layer. Manual field-by-field transforms are fragile and hard to update. |
| "No pagination handling" | Most APIs return paginated results. If you only read page 1, you're missing data. |

## Protocol

### Step 1: Gather Integration Requirements

If the user hasn't provided details, ask:

> 1. **Source system** — where does the data come from? (API name, docs URL)
> 2. **Destination** — where does it go? (your DB, another API, file)
> 3. **Data** — what entities are synced? (users, orders, products, events)
> 4. **Direction** — one-way, two-way, or event-driven?
> 5. **Auth** — how does the API authenticate? (API key, OAuth 2.0, JWT, Basic)
> 6. **Volume** — how much data? How often? (1K records/day vs 1M)

### Step 2: Implement Authentication

| Auth Type | Implementation | Token Lifecycle |
|-----------|---------------|----------------|
| **API Key** | Header: `X-API-Key: {key}` or query param | Static — rotate manually |
| **Bearer Token** | Header: `Authorization: Bearer {token}` | Expires — refresh needed |
| **OAuth 2.0** | Auth code flow → access + refresh tokens | Auto-refresh on 401 |
| **JWT** | Sign claims → `Authorization: Bearer {jwt}` | Short-lived — re-sign |
| **Basic Auth** | Header: `Authorization: Basic {base64}` | Static |
| **HMAC** | Sign request body → custom header | Per-request signing |

**OAuth 2.0 token refresh pattern:**

```typescript
class ApiClient {
  private accessToken: string;
  private refreshToken: string;
  private expiresAt: number;

  async request(method: string, path: string, body?: any): Promise<any> {
    if (Date.now() >= this.expiresAt - 60_000) { // Refresh 60s early
      await this.refreshAccessToken();
    }

    const response = await fetch(`${this.baseUrl}${path}`, {
      method,
      headers: {
        'Authorization': `Bearer ${this.accessToken}`,
        'Content-Type': 'application/json',
      },
      body: body ? JSON.stringify(body) : undefined,
    });

    if (response.status === 401) {
      await this.refreshAccessToken();
      return this.request(method, path, body); // Retry once
    }

    return response.json();
  }
}
```

### Step 3: Handle Rate Limiting

**Rate limit detection and backoff:**

```typescript
async function requestWithRateLimit(
  fn: () => Promise<Response>,
  maxRetries = 3
): Promise<Response> {
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    const response = await fn();

    if (response.status === 429) {
      const retryAfter = parseInt(response.headers.get('Retry-After') || '0');
      const waitMs = retryAfter > 0
        ? retryAfter * 1000
        : Math.min(1000 * Math.pow(2, attempt), 30_000); // Exponential backoff, max 30s

      console.log(`Rate limited. Waiting ${waitMs}ms (attempt ${attempt + 1})`);
      await sleep(waitMs);
      continue;
    }

    return response;
  }
  throw new Error('Rate limit exceeded after max retries');
}
```

**Proactive rate limiting (token bucket):**

```typescript
class RateLimiter {
  private tokens: number;
  private lastRefill: number;

  constructor(
    private maxTokens: number,    // e.g., 100
    private refillRate: number,   // tokens per second, e.g., 10
  ) {
    this.tokens = maxTokens;
    this.lastRefill = Date.now();
  }

  async acquire(): Promise<void> {
    this.refill();
    if (this.tokens <= 0) {
      const waitMs = (1 / this.refillRate) * 1000;
      await sleep(waitMs);
      this.refill();
    }
    this.tokens--;
  }

  private refill(): void {
    const now = Date.now();
    const elapsed = (now - this.lastRefill) / 1000;
    this.tokens = Math.min(this.maxTokens, this.tokens + elapsed * this.refillRate);
    this.lastRefill = now;
  }
}
```

### Step 4: Build Data Mapper

**Mapping layer pattern:**

```typescript
// Define field mappings declaratively
interface FieldMapping {
  source: string;        // Source field path (dot notation)
  target: string;        // Target field path
  transform?: (val: any) => any;  // Optional transformation
  required?: boolean;
}

const orderMappings: FieldMapping[] = [
  { source: 'id',              target: 'externalId',  required: true },
  { source: 'customer.email',  target: 'email',       required: true },
  { source: 'total_price',     target: 'amount',      transform: (v) => parseFloat(v) * 100 }, // dollars to cents
  { source: 'created_at',      target: 'createdAt',   transform: (v) => new Date(v).toISOString() },
  { source: 'line_items',      target: 'items',       transform: mapLineItems },
];

function mapRecord(source: any, mappings: FieldMapping[]): any {
  const target: any = {};
  for (const m of mappings) {
    const value = getNestedValue(source, m.source);
    if (value === undefined && m.required) {
      throw new Error(`Missing required field: ${m.source}`);
    }
    if (value !== undefined) {
      setNestedValue(target, m.target, m.transform ? m.transform(value) : value);
    }
  }
  return target;
}
```

### Step 5: Handle Pagination

**Common pagination patterns:**

| Pattern | How to Detect | Implementation |
|---------|--------------|----------------|
| **Offset/limit** | `?offset=0&limit=100` | Increment offset until empty results |
| **Page number** | `?page=1&per_page=100` | Increment page until last page |
| **Cursor-based** | `next_cursor` in response | Use cursor until null/empty |
| **Link header** | `Link: <url>; rel="next"` | Follow the `next` URL |

**Generic paginator:**

```typescript
async function* paginate<T>(
  fetchPage: (cursor?: string) => Promise<{ data: T[]; nextCursor?: string }>
): AsyncGenerator<T> {
  let cursor: string | undefined;
  do {
    const page = await fetchPage(cursor);
    for (const item of page.data) {
      yield item;
    }
    cursor = page.nextCursor;
  } while (cursor);
}

// Usage
for await (const order of paginate(fetchOrders)) {
  await processOrder(order);
}
```

### Step 6: Error Recovery & Sync State

**Sync state tracking:**

```sql
CREATE TABLE sync_state (
  integration  VARCHAR(100) PRIMARY KEY,
  last_cursor  VARCHAR(255),
  last_sync_at TIMESTAMPTZ  NOT NULL,
  items_synced INTEGER      NOT NULL DEFAULT 0,
  status       VARCHAR(20)  NOT NULL DEFAULT 'idle', -- idle | running | failed
  error        TEXT
);
```

**Incremental sync pattern:**

```typescript
async function incrementalSync(integration: string): Promise<void> {
  const state = await getSyncState(integration);
  let cursor = state.lastCursor;
  let count = 0;

  try {
    await updateSyncState(integration, { status: 'running' });

    for await (const item of paginate((c) => fetchItems(c || cursor))) {
      await processItem(item);
      cursor = item.id; // Track progress
      count++;

      // Checkpoint every 100 items (resume from here on failure)
      if (count % 100 === 0) {
        await updateSyncState(integration, { lastCursor: cursor, itemsSynced: count });
      }
    }

    await updateSyncState(integration, {
      status: 'idle', lastCursor: cursor,
      lastSyncAt: new Date(), itemsSynced: count
    });
  } catch (error) {
    await updateSyncState(integration, {
      status: 'failed', lastCursor: cursor, error: error.message
    });
    throw error;
  }
}
```

### Step 7: Production Checklist

- [ ] Authentication handles token refresh (no manual token replacement)
- [ ] Rate limiter respects API's documented limits
- [ ] Retry logic with exponential backoff for 429 and 5xx responses
- [ ] Pagination handles all pages (not just page 1)
- [ ] Data mapper validates required fields before writing
- [ ] Sync state persisted — can resume from last checkpoint on failure
- [ ] Structured logging with correlation IDs
- [ ] Secrets in environment variables or secrets manager
- [ ] Error alerts configured (Slack, email, or PagerDuty)
- [ ] Integration tested with production-volume data

## Output Format

```markdown
# API Integration — [Source] → [Destination]

## Overview
- **Direction:** [One-way / Two-way / Event-driven]
- **Entities:** [What's being synced]
- **Auth:** [Auth method]
- **Rate limit:** [X requests/second]
- **Sync frequency:** [Real-time / Every X minutes / Daily]

## Authentication
[Implementation from Step 2]

## Rate Limiting
[Implementation from Step 3]

## Data Mapping
[Mapping definitions from Step 4]

## Pagination
[Pattern from Step 5]

## Sync State & Recovery
[Implementation from Step 6]

## Production Checklist
[From Step 7]
```

## Completion

```
API Integration — Complete!

Integration: [Source] → [Destination]
Entities synced: [List]
Auth method: [Method]
Rate limit handling: [Strategy]
Pagination: [Pattern]
Sync state: [Checkpoint-based]

Next steps:
1. Implement using the code patterns above
2. Set up credentials in your secrets manager
3. Run an initial full sync with a small dataset
4. Verify data mapping accuracy in destination
5. Enable incremental sync on schedule
```

## Level History

- **Lv.1** — Base: 6 auth patterns (API key, Bearer, OAuth 2.0 with refresh, JWT, Basic, HMAC), reactive + proactive rate limiting (token bucket), declarative data mapper with transformations, 4 pagination patterns with generic async generator, incremental sync with checkpoint-based recovery, sync state table, production checklist. (Origin: MemStack Pro v3.2, Mar 2026)
