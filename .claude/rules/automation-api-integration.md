---
name: api-integration
description: "Use when the user says 'API integration', 'connect APIs', 'sync data', 'API to API', 'integrate with', or needs to build a reliable connection between two systems via their APIs."
---


# 🔗 API Integration — System-to-System Connector
*Design reliable API integrations with authentication, rate limiting, data mapping, error recovery, and sync monitoring.*

## Activation

When this skill activates, output:

`🔗 API Integration — Designing your system integration...`

| Context | Status |
|---------|--------|
| **User says "API integration", "connect APIs", "sync data"** | ACTIVE |
| **User wants to move data between two systems** | ACTIVE |
| **User mentions OAuth, rate limits, or data mapping** | ACTIVE |
| **User wants a visual n8n workflow** | DORMANT — see n8n-workflow-builder |
| **User wants to receive webhooks (not build a full integration)** | DORMANT — see webhook-designer |
| **User wants a cron job (the integration is secondary)** | DORMANT — see cron-scheduler |

## Protocol

### Step 1: Gather Inputs

Ask the user for:
- **Source API**: What system provides the data? (name, docs URL)
- **Target system**: Where should data go? (database, another API, file)
- **Data to sync**: What specific data? (users, orders, products, events)
- **Sync frequency**: Real-time, near-real-time, hourly, daily, on-demand?
- **Volume**: How many records? How often do they change?
- **Direction**: One-way (source → target) or bidirectional?

### Step 2: Choose Integration Pattern

Evaluate which pattern fits:

| Pattern | Best For | Latency | Complexity | Cost |
|---------|----------|---------|------------|------|
| **Polling** | APIs without webhooks, batch sync | Minutes-hours | Low | Higher API calls |
| **Webhook** | Event-driven, real-time updates | Seconds | Medium | Low API calls |
| **Event-driven** | High-volume, microservice comms | Milliseconds | High | Infra cost (queue) |
| **Hybrid** | Webhook for real-time + polling for reconciliation | Seconds + batch | Medium-High | Balanced |

**Decision guide:**
- Source has webhooks? → Webhook-first, poll for reconciliation
- Source has no webhooks? → Poll at reasonable interval
- Need real-time? → Webhook or event stream
- Need guaranteed delivery? → Add queue (SQS, Redis, BullMQ)
- Bidirectional? → Be very careful about sync loops — use change tokens

Recommend the pattern with justification.

### Step 3: Authentication Setup

Provide setup for the source API's auth method:

**API Key:**
```javascript
const client = axios.create({
  baseURL: 'https://api.service.com/v1',
  headers: { 'Authorization': `Bearer ${process.env.SERVICE_API_KEY}` },
  timeout: 10000,
});
```

**OAuth 2.0:**
```javascript
class OAuthClient {
  constructor(clientId, clientSecret, tokenUrl) {
    this.clientId = clientId;
    this.clientSecret = clientSecret;
    this.tokenUrl = tokenUrl;
    this.accessToken = null;
    this.expiresAt = 0;
  }

  async getToken() {
    if (this.accessToken && Date.now() < this.expiresAt - 60000) {
      return this.accessToken;
    }

    const response = await axios.post(this.tokenUrl, {
      grant_type: 'client_credentials',
      client_id: this.clientId,
      client_secret: this.clientSecret,
    });

    this.accessToken = response.data.access_token;
    this.expiresAt = Date.now() + (response.data.expires_in * 1000);
    return this.accessToken;
  }

  async request(config) {
    const token = await this.getToken();
    return axios({ ...config, headers: { ...config.headers, Authorization: `Bearer ${token}` } });
  }
}
```

**JWT:**
```javascript
const jwt = require('jsonwebtoken');
const token = jwt.sign({ sub: serviceId }, privateKey, {
  algorithm: 'RS256',
  expiresIn: '1h',
});
```

Store all credentials in environment variables. Document which scopes/permissions are needed.

### Step 4: Rate Limit Handling

Design rate limit respect:

```javascript
class RateLimitedClient {
  constructor(client, maxPerSecond = 10) {
    this.client = client;
    this.queue = [];
    this.interval = 1000 / maxPerSecond;
    this.lastRequest = 0;
  }

  async request(config) {
    const now = Date.now();
    const wait = Math.max(0, this.lastRequest + this.interval - now);

    if (wait > 0) await new Promise(r => setTimeout(r, wait));
    this.lastRequest = Date.now();

    try {
      return await this.client.request(config);
    } catch (err) {
      if (err.response?.status === 429) {
        const retryAfter = parseInt(err.response.headers['retry-after'] || '60', 10);
        console.warn(`Rate limited. Retrying after ${retryAfter}s`);
        await new Promise(r => setTimeout(r, retryAfter * 1000));
        return this.request(config); // Retry once
      }
      throw err;
    }
  }
}
```

**Rate limit strategies:**
- **Pre-emptive**: Track calls, delay to stay under limit
- **Reactive**: Catch 429s, respect `Retry-After` header
- **Batch**: Group multiple operations into single API calls where supported
- **Queue**: Use a job queue (BullMQ) to process at controlled rate

Document the source API's rate limits:
| Endpoint | Limit | Window | Notes |
|----------|-------|--------|-------|
| `GET /items` | 100/min | Rolling | Use pagination cursor |
| `POST /items` | 20/min | Rolling | Batch endpoint: 100 items/call |
| Global | 1000/hr | Fixed | Across all endpoints |

### Step 5: Data Mapping

Define how source fields transform to target fields:

```
── DATA MAPPING ───────────────────────────

Source: [API Name]         Target: [System Name]
─────────────────────────────────────────────
source.id               →  external_id         String, direct
source.email             →  email               String, .toLowerCase().trim()
source.created_at        →  created_date        Date, parse ISO → YYYY-MM-DD
source.amount_cents      →  amount              Number, / 100
source.status            →  status              Enum map: { active: 'enabled', inactive: 'disabled' }
source.metadata.tags     →  tags                Array, .join(', ')
source.address.line1     →  street_address      String, concat line1 + line2
[not in source]          →  sync_source         Constant: 'api_name'
[not in source]          →  last_synced_at      Timestamp: NOW()
```

**Mapping implementation:**
```javascript
function mapRecord(source) {
  return {
    external_id: source.id,
    email: source.email?.toLowerCase().trim(),
    created_date: source.created_at?.split('T')[0],
    amount: source.amount_cents / 100,
    status: { active: 'enabled', inactive: 'disabled' }[source.status] || 'unknown',
    tags: source.metadata?.tags?.join(', ') || '',
    street_address: [source.address?.line1, source.address?.line2].filter(Boolean).join(' '),
    sync_source: 'api_name',
    last_synced_at: new Date().toISOString(),
  };
}
```

### Step 6: Error Handling

Design error recovery for each failure mode:

| Failure | Detection | Recovery | Data Impact |
|---------|-----------|----------|-------------|
| **Source API down** | Connection timeout / 5xx | Retry 3x, then skip cycle + alert | No data loss — retry next cycle |
| **Bad data from source** | Validation failure | Log + skip record, process rest | One record skipped |
| **Target write fails** | Insert/update error | Retry record 3x, then dead-letter | Record queued for manual fix |
| **Partial sync** | Crash mid-batch | Resume from last cursor/checkpoint | Already-synced records safe |
| **Rate limit hit** | 429 response | Backoff, resume from where stopped | No data loss |
| **Auth expired** | 401 response | Refresh token, retry request | No data loss |

**Compensating transactions:**
If a multi-step sync fails partway through:
1. Log what was successfully synced
2. Store the sync cursor/position
3. On next run, detect partial sync and resume (not restart)
4. For reversible operations, consider rollback on failure

### Step 7: Caching

When and what to cache:

| Data | Cache? | TTL | Reason |
|------|--------|-----|--------|
| Lookup tables (categories, types) | Yes | 1 hour | Rarely changes, called often |
| User profiles | Yes | 5 min | Moderate change rate |
| Transaction data | No | — | Must be real-time accurate |
| API tokens | Yes | Until expiry - 60s | Avoid unnecessary auth calls |
| Pagination cursors | Yes | Duration of sync | Resume interrupted syncs |

**Cache implementation:**
```javascript
const cache = new Map();

async function cachedGet(key, fetchFn, ttlMs = 300000) {
  const cached = cache.get(key);
  if (cached && Date.now() < cached.expiresAt) return cached.data;

  const data = await fetchFn();
  cache.set(key, { data, expiresAt: Date.now() + ttlMs });
  return data;
}
```

### Step 8: Monitoring

**Sync status tracking:**

```sql
CREATE TABLE sync_status (
  id SERIAL PRIMARY KEY,
  integration_name VARCHAR(100) NOT NULL,
  last_sync_at TIMESTAMPTZ,
  last_sync_status VARCHAR(20), -- success, partial, failed
  records_synced INTEGER DEFAULT 0,
  records_failed INTEGER DEFAULT 0,
  last_cursor TEXT, -- for pagination resume
  error_message TEXT,
  sync_duration_ms INTEGER
);
```

**Metrics to track:**
- Sync frequency: Is it running on schedule?
- Data freshness: When was the last successful sync?
- Error rate: What % of records fail?
- Throughput: Records per second
- Latency: Time from source change to target update

**Dashboard output:**
```
Integration: [name]
Status: ✅ Healthy | ⚠️ Degraded | ❌ Failed
Last sync: [timestamp] ([X minutes ago])
Records: [synced] synced, [failed] failed
Data freshness: [X minutes]
Next sync: [timestamp]
```

### Step 9: Output

Present the complete integration specification:

```
━━━ API INTEGRATION: [Source] → [Target] ━━

── PATTERN ────────────────────────────────
Type: [polling/webhook/event-driven/hybrid]
Frequency: [schedule]
Direction: [one-way/bidirectional]

── AUTHENTICATION ─────────────────────────
Source: [auth method + setup]
Target: [auth method + setup]

── RATE LIMITS ────────────────────────────
[limit table + handling strategy]

── DATA MAPPING ───────────────────────────
[field mapping table + transform code]

── ERROR HANDLING ─────────────────────────
[failure matrix with recovery strategies]

── CACHING ────────────────────────────────
[what to cache + TTLs]

── MONITORING ─────────────────────────────
[sync_status table + metrics + dashboard]

── CODE ───────────────────────────────────
[complete integration implementation]
```

## Inputs
- Source API (name, docs, auth method)
- Target system (database, API, file)
- Data to sync (entities, fields)
- Sync frequency and direction
- Volume estimates

## Outputs
- Integration pattern recommendation with justification
- Authentication setup (API key, OAuth 2.0, JWT)
- Rate limit handling with pre-emptive and reactive strategies
- Data mapping table with transformation functions
- Error handling matrix with recovery per failure type
- Caching strategy with TTLs
- Monitoring dashboard with sync status table and metrics
- Complete integration code

## Level History

- **Lv.1** — Base: Integration pattern selection (polling/webhook/event-driven/hybrid), auth setup (API key, OAuth 2.0, JWT), rate limit handling (pre-emptive + reactive + queue), data mapping with transforms, error recovery matrix with compensating transactions, caching strategy, sync status monitoring with freshness tracking. (Origin: MemStack v3.2, Mar 2026)
