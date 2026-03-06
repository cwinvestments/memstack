---
name: cron-scheduler
description: "Use when the user says 'cron job', 'scheduled task', 'cron', 'scheduler', 'run every', 'periodic task', or needs a recurring background job with monitoring and failure handling."
---


# ⏰ Cron Scheduler — Scheduled Job Design
*Design production-grade cron jobs with overlap prevention, monitoring, structured logging, and platform-specific deployment.*

## Activation

When this skill activates, output:

`⏰ Cron Scheduler — Designing your scheduled job...`

| Context | Status |
|---------|--------|
| **User says "cron job", "scheduled task", "run every"** | ACTIVE |
| **User wants a recurring background process** | ACTIVE |
| **User mentions cron expressions or scheduling** | ACTIVE |
| **User wants an n8n workflow with a schedule trigger** | DORMANT — see n8n-workflow-builder |
| **User wants an event-driven webhook (not time-based)** | DORMANT — see webhook-designer |

## Protocol

### Step 1: Gather Inputs

Ask the user for:
- **Task description**: What does the job do?
- **Frequency**: How often? (every 5 min, hourly, daily, weekly, monthly)
- **Runtime environment**: Where does it run? (Railway, Netlify, VPS, local server, n8n)
- **Expected duration**: How long does a typical run take?
- **Dependencies**: What does it need? (database, external APIs, file system)
- **Failure severity**: What happens if it doesn't run? (critical / important / low impact)

### Step 2: Write Cron Expression

```
── SCHEDULE ───────────────────────────────

Cron Expression: [expression]
Human Readable: "[description]"
Timezone: [timezone]

┌─── minute (0-59)
│ ┌─── hour (0-23)
│ │ ┌─── day of month (1-31)
│ │ │ ┌─── month (1-12)
│ │ │ │ ┌─── day of week (0-7, 0 and 7 = Sunday)
│ │ │ │ │
* * * * *
```

**Common expressions:**

| Schedule | Expression | Notes |
|----------|-----------|-------|
| Every 5 minutes | `*/5 * * * *` | High frequency — ensure fast execution |
| Every 15 minutes | `*/15 * * * *` | Good for sync jobs |
| Every hour | `0 * * * *` | Runs at :00 |
| Every hour (offset) | `7 * * * *` | Runs at :07 — avoids peak traffic |
| Daily at 2 AM | `0 2 * * *` | Low-traffic window for heavy jobs |
| Weekdays at 9 AM | `0 9 * * 1-5` | Business hours only |
| Weekly Sunday midnight | `0 0 * * 0` | Weekly cleanup/reports |
| First of month 6 AM | `0 6 1 * *` | Monthly billing/reports |

### Step 3: Design the Job

Structure the job with clear phases:

```javascript
async function runJob() {
  const runId = crypto.randomUUID();
  const startTime = Date.now();

  console.log(JSON.stringify({
    event: 'job_started', runId, job: '[job_name]',
    timestamp: new Date().toISOString()
  }));

  try {
    // Phase 1: Acquire lock
    const lock = await acquireLock('[job_name]');
    if (!lock) {
      console.log(JSON.stringify({ event: 'job_skipped', runId, reason: 'lock_held' }));
      return;
    }

    // Phase 2: Gather data
    const data = await gatherData();

    // Phase 3: Process
    const results = await processData(data);

    // Phase 4: Report
    await reportResults(results);

    // Phase 5: Cleanup
    await releaseLock('[job_name]');

    const duration = Date.now() - startTime;
    console.log(JSON.stringify({
      event: 'job_completed', runId, job: '[job_name]',
      duration_ms: duration, items_processed: results.length
    }));
  } catch (err) {
    const duration = Date.now() - startTime;
    console.error(JSON.stringify({
      event: 'job_failed', runId, job: '[job_name]',
      duration_ms: duration, error: err.message
    }));

    await sendAlert('[job_name] failed', err.message);
    await releaseLock('[job_name]');
  }
}
```

### Step 4: Error Handling

Define what happens when the job fails:

| Failure Type | Detection | Response |
|-------------|-----------|----------|
| **Crash mid-run** | Process exits | Lock expires, alert sent, next run retries |
| **Partial data processed** | Check progress markers | Resume from last checkpoint, don't re-process |
| **External API down** | HTTP timeout/5xx | Retry 3x with backoff, then skip and alert |
| **Database unreachable** | Connection error | Abort immediately, alert, retry next cycle |
| **Job takes too long** | Duration > threshold | Log warning, consider killing if lock-breaking |

**Checkpoint pattern for long jobs:**

```javascript
async function processData(items) {
  const checkpoint = await getCheckpoint('[job_name]');
  const startIndex = checkpoint?.lastIndex || 0;

  for (let i = startIndex; i < items.length; i++) {
    await processItem(items[i]);
    // Save progress every 100 items
    if (i % 100 === 0) {
      await saveCheckpoint('[job_name]', { lastIndex: i });
    }
  }

  await clearCheckpoint('[job_name]');
}
```

### Step 5: Overlap Prevention

Prevent multiple instances from running simultaneously:

**Database lock (recommended for multi-instance):**

```sql
CREATE TABLE cron_locks (
  job_name VARCHAR(100) PRIMARY KEY,
  locked_by VARCHAR(255),
  locked_at TIMESTAMPTZ,
  expires_at TIMESTAMPTZ
);
```

```javascript
async function acquireLock(jobName, ttlMinutes = 30) {
  const result = await db.query(
    `INSERT INTO cron_locks (job_name, locked_by, locked_at, expires_at)
     VALUES ($1, $2, NOW(), NOW() + INTERVAL '${ttlMinutes} minutes')
     ON CONFLICT (job_name) DO UPDATE
       SET locked_by = $2, locked_at = NOW(),
           expires_at = NOW() + INTERVAL '${ttlMinutes} minutes'
     WHERE cron_locks.expires_at < NOW()
     RETURNING job_name`,
    [jobName, os.hostname()]
  );
  return result.rows.length > 0;
}

async function releaseLock(jobName) {
  await db.query('DELETE FROM cron_locks WHERE job_name = $1', [jobName]);
}
```

**Lock TTL**: Set expiration longer than the maximum expected job duration. If a job crashes without releasing the lock, the TTL prevents permanent deadlock.

### Step 6: Monitoring

**Health check endpoint:**

```javascript
app.get('/api/health/cron', async (req, res) => {
  const jobs = await db.query(
    `SELECT job_name, last_run, last_status, last_duration_ms
     FROM cron_job_runs
     ORDER BY last_run DESC`
  );

  const unhealthy = jobs.rows.filter(j => {
    const minutesSinceRun = (Date.now() - new Date(j.last_run).getTime()) / 60000;
    return j.last_status === 'failed' || minutesSinceRun > j.expected_interval_minutes * 2;
  });

  res.status(unhealthy.length > 0 ? 500 : 200).json({
    status: unhealthy.length > 0 ? 'unhealthy' : 'healthy',
    jobs: jobs.rows,
    unhealthy: unhealthy.map(j => j.job_name),
  });
});
```

**Last-run tracking table:**

```sql
CREATE TABLE cron_job_runs (
  id SERIAL PRIMARY KEY,
  job_name VARCHAR(100) NOT NULL,
  run_id UUID NOT NULL,
  started_at TIMESTAMPTZ NOT NULL,
  completed_at TIMESTAMPTZ,
  status VARCHAR(20) DEFAULT 'running', -- running, completed, failed
  duration_ms INTEGER,
  items_processed INTEGER DEFAULT 0,
  error_message TEXT,
  metadata JSONB
);

CREATE INDEX idx_cron_runs_job ON cron_job_runs(job_name, started_at DESC);
```

**Failure alerts:**
- Slack notification on failure
- Email alert if job hasn't run in 2x the expected interval
- Aggregate: Don't alert on every failure if job fails repeatedly — send one alert, then summarize

### Step 7: Structured Logging

Every log entry should include:

```json
{
  "event": "job_started|job_completed|job_failed|job_skipped",
  "job": "job_name",
  "runId": "uuid",
  "timestamp": "ISO 8601",
  "duration_ms": 1234,
  "items_processed": 50,
  "error": null
}
```

**Log at these points:**
1. Job started (with run ID)
2. Lock acquired or skipped
3. Data gathered (count of items to process)
4. Checkpoint saved (every N items)
5. Job completed (with duration and item count)
6. Job failed (with error message and stack trace)

### Step 8: Platform-Specific Deployment

**Railway (recommended for Node.js apps):**
```json
// In railway.json or use Railway CLI
// Set cron schedule in Railway dashboard → Service → Settings → Cron
// Railway runs the service, triggers the job, then shuts it down
```

**Netlify Scheduled Functions:**
```javascript
// netlify/functions/my-cron-job.mts
import { Config } from '@netlify/functions';

export default async (req) => {
  // Job logic here
  return new Response('OK');
};

export const config: Config = {
  schedule: '@daily', // or cron expression
};
```

**System crontab (VPS/dedicated):**
```bash
# Edit: crontab -e
# Format: minute hour day month weekday command
0 2 * * * cd /app && node jobs/my-job.js >> /var/log/cron/my-job.log 2>&1
```

**n8n (visual):**
- Use Schedule Trigger node
- Set cron expression in node config
- Connect to workflow nodes for processing

**node-cron (in-process):**
```javascript
const cron = require('node-cron');
cron.schedule('0 2 * * *', runJob, { timezone: 'America/Chicago' });
```

### Step 9: Output

Present the complete cron job specification:

```
━━━ CRON JOB: [Job Name] ━━━━━━━━━━━━━━━━━

── SCHEDULE ───────────────────────────────
Expression: [cron]
Readable: "[description]"
Timezone: [tz]

── JOB LOGIC ──────────────────────────────
[complete job function code]

── ERROR HANDLING ─────────────────────────
[failure types and responses]

── LOCK TABLE ─────────────────────────────
[SQL migration for cron_locks]

── MONITORING ─────────────────────────────
[health endpoint + run tracking table]

── DEPLOYMENT ─────────────────────────────
Platform: [name]
Config: [deployment-specific setup]

── ALERTS ─────────────────────────────────
[notification setup for failures]
```

## Inputs
- Task description and purpose
- Frequency / schedule
- Runtime environment
- Expected duration
- Dependencies (database, APIs)
- Failure severity

## Outputs
- Cron expression with human-readable explanation
- Complete job code with phases (lock, gather, process, report, cleanup)
- Error handling with checkpoints for long jobs
- Database lock mechanism for overlap prevention
- Health check endpoint and run-tracking table
- Structured logging format
- Platform-specific deployment instructions
- Failure alert configuration

## Level History

- **Lv.1** — Base: Cron expression builder, phased job structure, checkpoint-based error recovery, database lock for overlap prevention, health check endpoint, run-tracking table, structured JSON logging, multi-platform deployment (Railway, Netlify, crontab, n8n, node-cron), failure alerting. (Origin: MemStack v3.2, Mar 2026)
