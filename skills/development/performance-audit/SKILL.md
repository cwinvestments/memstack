---
name: memstack-development-performance-audit
description: "Use this skill when the user says 'performance audit', 'why is it slow', 'optimize performance', 'page speed', 'Core Web Vitals', 'lighthouse', 'load time', or needs to diagnose and fix frontend or backend performance issues. Do NOT use for code reviews or security audits."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# 🚀 Performance Audit — Full-Stack Performance Scanner
*Identify and prioritize performance bottlenecks across frontend, backend, and network layers with measured impact and fix priority.*

## Activation

When this skill activates, output:

`🚀 Performance Audit — Scanning for performance bottlenecks...`

| Context | Status |
|---------|--------|
| **User says "performance audit", "optimize", "slow app"** | ACTIVE |
| **User mentions bundle size, N+1 queries, or Core Web Vitals** | ACTIVE |
| **User wants to find memory leaks or unnecessary re-renders** | ACTIVE |
| **User wants database schema optimization specifically** | DORMANT — see database-architect |
| **User wants API design review (not performance)** | DORMANT — see api-designer |
| **User wants general code quality review** | DORMANT — see code-reviewer |

## Protocol

### Step 1: Gather Inputs

Ask the user for:
- **Stack**: Frontend framework, backend language, database?
- **Symptoms**: What feels slow? (initial load, interactions, API responses, builds)
- **Scale**: How many users? How much data?
- **Metrics**: Any existing performance data? (Lighthouse scores, APM dashboards)
- **Priority**: User-facing speed or server-side efficiency?

### Step 2: Frontend — Bundle Analysis

**Check bundle size and composition:**

```bash
# Next.js
npx @next/bundle-analyzer
# or: ANALYZE=true next build

# Webpack (generic)
npx webpack-bundle-analyzer stats.json

# Vite
npx vite-bundle-visualizer
```

**What to look for:**

| Issue | Detection | Impact | Fix |
|-------|-----------|--------|-----|
| Large dependencies | Bundle > 200KB gzipped | Slow initial load | Replace with lighter alternatives |
| Duplicate packages | Same lib in multiple versions | Wasted bytes | Dedupe or pin single version |
| Unused exports | Tree-shaking not working | Wasted bytes | Use ESM imports, avoid barrel files |
| No code splitting | Single large bundle | Slow initial load | Dynamic imports, route-based splitting |
| Unoptimized images | Images > 100KB without optimization | Slow load | next/image, sharp, WebP/AVIF |
| Missing compression | No gzip/brotli on responses | 60-80% larger payloads | Enable in server/CDN config |

**Common heavy dependencies and alternatives:**

| Package | Size (minified) | Lighter Alternative | Size |
|---------|----------------|-------------------|------|
| `moment` | 72 KB | `date-fns` (tree-shakeable) | ~2-5 KB used |
| `lodash` (full) | 72 KB | `lodash-es` (tree-shakeable) | ~1-3 KB used |
| `axios` | 14 KB | `fetch` (native) | 0 KB |
| `classnames` | 1 KB | Template literals | 0 KB |
| `uuid` | 3 KB | `crypto.randomUUID()` | 0 KB |
| `chart.js` | 65 KB | Specific chart lib for your use case | Varies |

**Tree-shaking checks:**
```
── TREE-SHAKING ISSUES ────────────────────

[x] Barrel files (index.ts re-exporting everything)
    File: src/utils/index.ts
    Impact: Imports entire utils even if using one function
    Fix: Import directly from source file

[x] CommonJS modules (require() instead of import)
    File: src/legacy/helper.js
    Impact: Cannot tree-shake CJS modules
    Fix: Convert to ESM or find ESM version of dependency

[x] Side effects not declared
    Package: [name]
    Impact: Bundler can't safely remove unused code
    Fix: Add "sideEffects": false to package.json
```

### Step 3: Frontend — Core Web Vitals

Audit for the three Core Web Vitals:

```
── CORE WEB VITALS AUDIT ──────────────────

LCP (Largest Contentful Paint) — Target: < 2.5s
  Current: [measured or estimated]
  Issues found:
    [ ] Hero image not optimized (missing width/height, no lazy loading)
    [ ] Render-blocking CSS in <head> (large stylesheet before content)
    [ ] Web fonts blocking render (no font-display: swap)
    [ ] Server response time > 600ms (TTFB too high)
    [ ] Third-party scripts blocking main thread

FID / INP (Interaction to Next Paint) — Target: < 200ms
  Current: [measured or estimated]
  Issues found:
    [ ] Long tasks on main thread (> 50ms blocks)
    [ ] Heavy JavaScript execution on page load
    [ ] Synchronous XHR calls blocking interaction
    [ ] Event handlers doing expensive computation

CLS (Cumulative Layout Shift) — Target: < 0.1
  Current: [measured or estimated]
  Issues found:
    [ ] Images without explicit dimensions (width/height)
    [ ] Dynamically injected content above fold
    [ ] Web fonts causing layout shift (FOUT/FOIT)
    [ ] Ads or embeds without reserved space
```

**Quick LCP fixes:**
```javascript
// 1. Preload hero image
<link rel="preload" as="image" href="/hero.webp" fetchpriority="high" />

// 2. Font display swap
@font-face {
  font-family: 'CustomFont';
  src: url('/fonts/custom.woff2') format('woff2');
  font-display: swap;
}

// 3. Next.js Image component (automatic optimization)
import Image from 'next/image';
<Image src="/hero.jpg" width={1200} height={600} priority alt="Hero" />
```

### Step 4: Frontend — React Performance

**Unnecessary re-render detection:**

| Pattern | Detection | Impact | Fix |
|---------|-----------|--------|-----|
| Passing new objects/arrays as props | `onClick={() => {}}` in JSX | Child re-renders every parent render | Extract handler, use `useCallback` |
| Missing memoization on expensive computation | Computed value in render body | Recalculated every render | `useMemo` for expensive calculations |
| Context causing tree-wide re-renders | Context value changes frequently | All consumers re-render | Split context, use selectors |
| Missing `key` on list items | React DevTools warnings | Incorrect DOM reconciliation | Add stable unique key |
| Props drilling deep component trees | Props passed through 5+ levels | Tight coupling, re-render chains | Context or composition pattern |

**React performance audit checklist:**
```
── REACT PERFORMANCE ──────────────────────

Component rendering:
  [ ] React.memo on pure presentational components
  [ ] useCallback for handlers passed to memoized children
  [ ] useMemo for expensive computed values (> 1ms)
  [ ] Stable keys on list items (not array index for dynamic lists)

State management:
  [ ] State colocated to where it's used (not lifted too high)
  [ ] Context split: frequent-update values separate from static config
  [ ] Avoid storing derived state (compute from source of truth)
  [ ] Batch state updates where possible

Data fetching:
  [ ] Loading states prevent waterfall fetches
  [ ] Parallel fetches where data is independent
  [ ] Cache API responses (React Query, SWR)
  [ ] Pagination/infinite scroll for large lists

Rendering:
  [ ] Virtualize long lists (react-window, @tanstack/virtual)
  [ ] Lazy load below-fold components (React.lazy + Suspense)
  [ ] Avoid layout thrashing (reading DOM then writing immediately)
  [ ] Debounce/throttle scroll and resize handlers
```

### Step 5: Backend — Database Performance

**N+1 query detection:**

```
── N+1 QUERY PATTERNS ─────────────────────

Pattern: Fetching related data in a loop
  Example:
    const users = await db.query('SELECT * FROM users');
    for (const user of users) {
      user.posts = await db.query('SELECT * FROM posts WHERE user_id = ?', [user.id]);
    }
  Queries generated: 1 + N (where N = number of users)

  Fix: JOIN or subquery
    SELECT u.*, p.* FROM users u
    LEFT JOIN posts p ON p.user_id = u.id;

  ORM fix (Prisma):
    await prisma.user.findMany({ include: { posts: true } });

  ORM fix (Drizzle):
    await db.query.users.findMany({ with: { posts: true } });
```

**Missing index detection:**

```sql
-- Find slow queries (PostgreSQL)
SELECT query, calls, mean_exec_time, total_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 20;

-- Find missing indexes
SELECT relname, seq_scan, seq_tup_read, idx_scan
FROM pg_stat_user_tables
WHERE seq_scan > 100 AND idx_scan < seq_scan / 10
ORDER BY seq_scan DESC;

-- Suggested indexes for common patterns:
-- Foreign keys: CREATE INDEX idx_posts_user_id ON posts(user_id);
-- Filtered queries: CREATE INDEX idx_users_active ON users(status) WHERE status = 'active';
-- Sorting: CREATE INDEX idx_posts_created ON posts(created_at DESC);
-- Text search: CREATE INDEX idx_users_email ON users(email);
```

**Query optimization checklist:**

| Issue | Detection | Impact | Fix |
|-------|-----------|--------|-----|
| N+1 queries | Loop with DB call inside | O(N) queries → O(1) | JOIN or eager loading |
| Missing indexes | Full table scans on filtered columns | Slow queries as data grows | Add targeted indexes |
| SELECT * | Fetching all columns | Excess data transfer | Select only needed columns |
| No pagination | Returning all records | Memory + transfer overhead | LIMIT/OFFSET or cursor pagination |
| Missing connection pooling | New connection per query | Connection overhead | Use pgBouncer or built-in pool |
| Unoptimized JOINs | Joining on non-indexed columns | Slow JOINs | Index JOIN columns |

### Step 6: Backend — API Performance

**Over-fetching and under-fetching:**

```
── API RESPONSE AUDIT ─────────────────────

Endpoint: GET /api/users
  Response size: 45 KB per request
  Fields returned: 28
  Fields used by client: 8
  Over-fetch ratio: 71% wasted

  Fix: Add field selection
    GET /api/users?fields=id,name,email,avatar
    or: implement GraphQL for flexible queries

Endpoint: GET /api/dashboard
  Requests made: 6 sequential API calls
  Could be: 1 aggregated endpoint
  Waterfall time: 1.8s
  Parallel time: 0.4s (if batched)

  Fix: Create /api/dashboard aggregate endpoint
    or: use Promise.all() on client for parallel fetches
```

**Missing pagination:**
```
── PAGINATION AUDIT ───────────────────────

Endpoint: GET /api/products
  Current: Returns ALL products (2,400 records)
  Response size: 890 KB
  Response time: 1.2s

  Fix: Add cursor-based pagination
    GET /api/products?cursor=abc123&limit=50
    Response: { data: [...], nextCursor: "def456", hasMore: true }
```

**Caching opportunities:**
```
── CACHE AUDIT ────────────────────────────

Endpoint             Cacheable?   TTL          Strategy
────────────────────────────────────────────────────────
GET /api/products    Yes          5 min        CDN + browser Cache-Control
GET /api/user/:id    Conditional  1 min        ETag / If-None-Match
GET /api/config      Yes          1 hour       CDN, stale-while-revalidate
POST /api/orders     No           —            Never cache mutations
GET /api/search      Maybe        30 sec       Vary by query params

Missing headers:
  [ ] Cache-Control not set on static assets
  [ ] No ETag on API responses
  [ ] No compression (gzip/brotli) on responses
```

### Step 7: Backend — Memory & Resource Leaks

**Common memory leak patterns:**

| Leak Type | Detection | Symptoms | Fix |
|-----------|-----------|----------|-----|
| **Event listeners** | Listeners added without removal | Memory grows over time | `removeEventListener` in cleanup |
| **Unclosed DB connections** | Connection pool exhaustion | "too many connections" errors | Close connections in finally/cleanup |
| **Growing arrays/maps** | In-memory cache without eviction | RSS grows indefinitely | Add TTL, LRU cache, or size limit |
| **Unreferenced timers** | `setInterval` without `clearInterval` | Timer continues after context dies | Clear timers on shutdown/cleanup |
| **Unresolved promises** | Promises that never settle | Memory for callbacks retained | Add timeouts to all async operations |
| **Circular references** | Objects referencing each other | GC can't collect (rare in V8) | Break cycles, use WeakRef |

**Detection approach:**
```bash
# Node.js heap snapshot
node --inspect app.js
# Open Chrome DevTools → Memory → Take heap snapshot
# Compare two snapshots to find growing objects

# Watch RSS over time
watch -n 5 'ps -o rss -p $(pgrep -f "node app.js") | tail -1'
```

**Cleanup patterns:**
```javascript
// Express: cleanup on server shutdown
const server = app.listen(3000);
const connections = new Set();
server.on('connection', (conn) => {
  connections.add(conn);
  conn.on('close', () => connections.delete(conn));
});

process.on('SIGTERM', () => {
  server.close();
  for (const conn of connections) conn.destroy();
  db.end();          // Close DB pool
  redis.quit();      // Close Redis
  clearInterval(heartbeat);  // Clear timers
});
```

### Step 8: Network Performance

**Unnecessary API calls:**

```
── REDUNDANT REQUEST AUDIT ────────────────

Issue: Same data fetched multiple times
  /api/user/me called 4 times on dashboard load
  Fix: Cache response, share via context/store

Issue: Polling when WebSocket would work
  /api/notifications polled every 5 seconds
  Fix: WebSocket/SSE for real-time updates

Issue: No request deduplication
  Search input triggers API call per keystroke
  Fix: Debounce (300ms), cancel previous request (AbortController)

Issue: Large uncompressed responses
  /api/export returns 2.4 MB JSON without gzip
  Fix: Enable compression middleware
```

**Compression check:**
```javascript
// Express
const compression = require('compression');
app.use(compression());

// Verify: response should have
// Content-Encoding: gzip  (or br for brotli)
```

**CDN and static asset optimization:**
```
── STATIC ASSET AUDIT ─────────────────────

Asset Type    Current          Optimized        Savings
────────────────────────────────────────────────────────
Images        PNG 2.4 MB       WebP 180 KB      92%
Fonts         4 font files     2 subsetted      60%
CSS           3 files, 120 KB  1 file, 45 KB    62%
JS            1.2 MB bundle    4 chunks, 280 KB  77%

Recommendations:
  [ ] Serve images in WebP/AVIF with fallback
  [ ] Subset fonts to used characters only
  [ ] Enable HTTP/2 for parallel asset loading
  [ ] Set Cache-Control: max-age=31536000 for hashed assets
  [ ] Use CDN for static assets (Cloudflare, CloudFront)
```

### Step 9: Performance Scorecard

Generate a scored report:

```
━━━ PERFORMANCE SCORECARD ━━━━━━━━━━━━━━━━
Project: [name]
Audit date: [date]
Overall score: [X/100]

── FRONTEND ───────────────────────────────
Bundle size:        [X/25]  [size]KB gzipped
  Issues: [list]
Core Web Vitals:    [X/25]
  LCP: [value]s    [good/needs-work/poor]
  INP: [value]ms   [good/needs-work/poor]
  CLS: [value]     [good/needs-work/poor]
React performance:  [X/10]
  Re-render issues: [count]

── BACKEND ────────────────────────────────
Database:           [X/15]
  N+1 queries:      [count found]
  Missing indexes:  [count found]
API efficiency:     [X/10]
  Over-fetching:    [count endpoints]
  Missing cache:    [count endpoints]
  No pagination:    [count endpoints]
Memory safety:      [X/5]
  Potential leaks:  [count found]

── NETWORK ────────────────────────────────
Compression:        [X/5]   [enabled/missing]
Asset optimization: [X/5]   [optimized/unoptimized]

── PRIORITIZED FIX LIST ───────────────────

Priority  Issue                          Impact    Effort   Category
──────────────────────────────────────────────────────────────────────
🔴 P1     [issue description]            High      Low      [area]
🔴 P1     [issue description]            High      Medium   [area]
🟡 P2     [issue description]            Medium    Low      [area]
🟡 P2     [issue description]            Medium    Medium   [area]
🟠 P3     [issue description]            Low       Low      [area]
🟠 P3     [issue description]            Medium    High     [area]
```

**Priority scoring:**
- **P1 (Do now)**: High impact + Low-Medium effort — biggest wins
- **P2 (Plan soon)**: Medium impact or High effort for high impact
- **P3 (Backlog)**: Low impact or very high effort

**Impact estimation guide:**

| Optimization | Typical Impact |
|-------------|---------------|
| Fix N+1 queries | 50-90% reduction in query time |
| Add missing indexes | 10-100x faster queries |
| Enable compression | 60-80% smaller responses |
| Code splitting | 30-60% faster initial load |
| Image optimization | 50-90% smaller images |
| Remove unused deps | 10-40% smaller bundle |
| Add caching | 80-99% fewer API calls |
| Virtualize lists | 90% less DOM, smooth scrolling |

## Inputs
- Tech stack (frontend framework, backend language, database)
- Performance symptoms (what feels slow)
- Scale information (users, data volume)
- Existing metrics (Lighthouse scores, APM data)
- Priority area (user-facing or server-side)

## Outputs
- Bundle analysis with heavy dependency identification and alternatives
- Core Web Vitals audit (LCP, INP, CLS) with specific fixes
- React performance checklist (re-renders, memoization, data fetching)
- Database audit (N+1 detection, missing indexes, query optimization)
- API audit (over-fetching, pagination, caching opportunities)
- Memory leak detection patterns and cleanup
- Network audit (compression, CDN, redundant requests)
- Performance scorecard (0-100) with prioritized fix list
- Impact estimates per optimization

## Level History

- **Lv.1** — Base: Full-stack performance scanner covering frontend (bundle analysis, Core Web Vitals, React re-renders), backend (N+1 queries, missing indexes, API over-fetching, memory leaks), and network (compression, CDN, caching). Performance scorecard with priority-ranked fix list and impact estimates. (Origin: MemStack v3.2, Mar 2026)
