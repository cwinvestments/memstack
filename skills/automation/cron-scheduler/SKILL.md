---
name: memstack-automation-cron-scheduler
description: "Use this skill when the user says 'cron job', 'scheduled task', 'run every', 'cron expression', 'recurring job', or needs production-grade scheduled jobs with overlap prevention, monitoring, and structured logging. Do NOT use for n8n workflows or event-driven webhooks."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# Cron Scheduler — Building scheduled job...
*Builds production-grade scheduled jobs with cron syntax, timezone handling, overlap prevention, health checks, monitoring, alerting, and structured logging.*

## Activation

When this skill activates, output:

`Cron Scheduler — Building scheduled job...`

Then execute the protocol below.

## Context Guard

| Context | Status |
|---------|--------|
| User says "cron job", "scheduled task", "run every" | ACTIVE |
| User says "cron expression" or "recurring job" | ACTIVE |
| User needs a time-based scheduled task with monitoring | ACTIVE |
| User wants a visual n8n workflow | DORMANT — use n8n Workflow Builder |
| User wants an event-driven webhook | DORMANT — use Webhook Designer |

## Common Mistakes

| Mistake | Why It's Wrong |
|---------|---------------|
| "No overlap prevention" | If a job takes 10 min and runs every 5 min, you get concurrent executions corrupting data. |
| "Ignore timezones" | Cron defaults to server timezone. Midnight UTC ≠ midnight local. Always set TZ explicitly. |
| "No monitoring" | Silent job failures are invisible. You won't know it broke until users complain. |
| "Log to stdout only" | Stdout disappears on restart. Use structured logging with persistence. |
| "Run as root" | Principle of least privilege. Run jobs under a dedicated service account. |

## Protocol

### Step 1: Gather Job Requirements

If the user hasn't provided details, ask:

> 1. **Task** — what does the job do? (sync data, send emails, clean up, generate reports)
> 2. **Schedule** — how often? (every 5 min, hourly, daily at 2 AM, weekly)
> 3. **Duration** — how long does a typical run take?
> 4. **Timezone** — which timezone matters? (UTC, user's local, business hours)
> 5. **Platform** — where does this run? (server crontab, cloud function, Docker, Kubernetes)
> 6. **Failure mode** — what happens if it fails? (retry, alert, skip until next run)

### Step 2: Write the Cron Expression

**Cron syntax (5-field standard):**

```
┌───────────── minute (0-59)
│ ┌───────────── hour (0-23)
│ │ ┌───────────── day of month (1-31)
│ │ │ ┌───────────── month (1-12)
│ │ │ │ ┌───────────── day of week (0-7, 0 and 7 = Sunday)
│ │ │ │ │
* * * * *
```

**Common schedule reference:**

| Schedule | Expression | Notes |
|----------|-----------|-------|
| Every minute | `* * * * *` | Testing only — too aggressive for production |
| Every 5 minutes | `*/5 * * * *` | Good for near-real-time sync |
| Every 15 minutes | `*/15 * * * *` | Light polling |
| Every hour | `0 * * * *` | At minute 0 of every hour |
| Every 6 hours | `0 */6 * * *` | 4x daily |
| Daily at 2 AM UTC | `0 2 * * *` | Maintenance window |
| Daily at 9 AM ET | `0 14 * * *` | 14:00 UTC = 9:00 AM ET (EST, adjust for DST) |
| Weekdays at 8 AM | `0 8 * * 1-5` | Monday through Friday |
| Weekly (Sunday midnight) | `0 0 * * 0` | Weekly cleanup |
| Monthly (1st at midnight) | `0 0 1 * *` | Monthly reports |
| Quarterly (Jan/Apr/Jul/Oct 1st) | `0 0 1 1,4,7,10 *` | Quarterly processing |

**Timezone handling:**

```bash
# System crontab — set TZ per job
CRON_TZ=America/New_York
0 9 * * * /path/to/job.sh    # Runs at 9 AM Eastern (handles DST)

# Or set in the crontab header
TZ=UTC
```

```typescript
// Node.js (node-cron) — explicit timezone
import cron from 'node-cron';

cron.schedule('0 9 * * *', () => {
  runDailyReport();
}, {
  timezone: 'America/New_York'
});
```

### Step 3: Implement Overlap Prevention

**Lock-based approach (recommended):**

```typescript
import { acquireLock, releaseLock } from './lockService';

async function runJob() {
  const lockKey = 'job:daily-report';
  const lockTTL = 3600; // seconds — must exceed max job duration

  const acquired = await acquireLock(lockKey, lockTTL);
  if (!acquired) {
    console.log('Job already running — skipping this execution');
    return;
  }

  try {
    await executeJobLogic();
  } finally {
    await releaseLock(lockKey);
  }
}
```

**Lock implementations by platform:**

| Platform | Lock Method | TTL Support |
|----------|-----------|-------------|
| Redis | `SET key value NX EX ttl` | Yes |
| PostgreSQL | `pg_advisory_lock(id)` | Session-based |
| File system | `flock` or PID file | Manual cleanup |
| DynamoDB | Conditional put with TTL | Yes |
| Kubernetes | CronJob `concurrencyPolicy: Forbid` | Built-in |

**PID file approach (simple servers):**

```bash
#!/bin/bash
PIDFILE="/tmp/myjob.pid"

if [ -f "$PIDFILE" ] && kill -0 $(cat "$PIDFILE") 2>/dev/null; then
    echo "Job already running (PID $(cat $PIDFILE))"
    exit 0
fi

echo $$ > "$PIDFILE"
trap "rm -f $PIDFILE" EXIT

# Job logic here
```

### Step 4: Structured Logging

```typescript
interface JobLog {
  job: string;
  runId: string;        // Unique per execution
  phase: 'start' | 'progress' | 'complete' | 'error';
  timestamp: string;
  durationMs?: number;
  itemsProcessed?: number;
  error?: string;
  metadata?: Record<string, any>;
}

function logJob(entry: JobLog): void {
  console.log(JSON.stringify(entry));
}

// Usage
const runId = crypto.randomUUID();
const start = Date.now();

logJob({ job: 'daily-report', runId, phase: 'start', timestamp: new Date().toISOString() });

try {
  const result = await executeJobLogic();
  logJob({
    job: 'daily-report', runId, phase: 'complete',
    timestamp: new Date().toISOString(),
    durationMs: Date.now() - start,
    itemsProcessed: result.count
  });
} catch (error) {
  logJob({
    job: 'daily-report', runId, phase: 'error',
    timestamp: new Date().toISOString(),
    durationMs: Date.now() - start,
    error: error.message
  });
  throw error;
}
```

### Step 5: Monitoring & Alerting

**Health check pattern — heartbeat:**

```typescript
// After successful job completion, ping a health check URL
async function pingHealthCheck(url: string): Promise<void> {
  await fetch(url); // Services: Cronitor, Healthchecks.io, Better Uptime
}

// The monitoring service alerts if it doesn't receive a ping within the expected window
```

**Alert conditions:**

| Condition | Severity | Action |
|-----------|----------|--------|
| Job didn't run (missed heartbeat) | Critical | Page on-call |
| Job failed (error thrown) | High | Slack + email alert |
| Job duration > 2x normal | Warning | Slack notification |
| Job processed 0 items (expected >0) | Warning | Review logs |
| Job overlap detected (lock contention) | Info | Log, investigate if frequent |

**Job history table (for dashboard):**

```sql
CREATE TABLE job_runs (
  id           SERIAL PRIMARY KEY,
  job_name     VARCHAR(100) NOT NULL,
  run_id       UUID         NOT NULL,
  status       VARCHAR(20)  NOT NULL, -- 'success' | 'failure' | 'skipped'
  started_at   TIMESTAMPTZ  NOT NULL,
  completed_at TIMESTAMPTZ,
  duration_ms  INTEGER,
  items_count  INTEGER,
  error        TEXT,
  metadata     JSONB
);

CREATE INDEX idx_job_runs_name_started ON job_runs(job_name, started_at DESC);
```

### Step 6: Production Checklist

**Before deploying:**
- [ ] Cron expression tested with [crontab.guru](https://crontab.guru)
- [ ] Timezone explicitly set (never rely on server default)
- [ ] Overlap prevention implemented (lock or concurrency policy)
- [ ] Structured logging with run IDs
- [ ] Health check / heartbeat URL configured
- [ ] Alert rules set for: missed run, failure, slow run
- [ ] Graceful shutdown handling (finish current item, don't corrupt)
- [ ] Environment variables for all config (no hardcoded values)
- [ ] Job runs under dedicated service account (not root)
- [ ] Tested with realistic data volume

**Maintenance:**
- [ ] Review job duration trends monthly (creeping duration = scaling issue)
- [ ] Clean up job history older than 90 days
- [ ] Verify health check alerts with a test failure quarterly

## Output Format

```markdown
# Cron Job — [Job Name]

## Schedule
- **Expression:** [cron expression]
- **Timezone:** [TZ]
- **Frequency:** [Human-readable]
- **Expected duration:** [X minutes]

## Job Logic
[What the job does, step by step]

## Implementation
[Code with overlap prevention, logging, error handling]

## Monitoring
- **Health check:** [URL or service]
- **Alerts:** [Alert conditions]
- **Dashboard:** [Where to view job history]

## Production Checklist
[Completed checklist from Step 6]
```

## Completion

```
Cron Scheduler — Complete!

Job: [Name]
Schedule: [Expression] ([timezone])
Overlap prevention: [Lock method]
Monitoring: [Health check service]
Alerts: [Count] conditions configured

Next steps:
1. Implement the job using the code templates above
2. Test the cron expression at crontab.guru
3. Deploy with overlap prevention and structured logging
4. Set up health check monitoring
5. Verify the first 3 runs succeed, then check weekly
```

## Level History

- **Lv.1** — Base: Cron syntax guide with 12 common schedules, timezone handling (crontab + Node.js), overlap prevention (Redis lock, PID file, K8s ConcurrencyPolicy), structured logging with run IDs, heartbeat monitoring pattern, alert conditions (5 severities), job history table, production deployment checklist. (Origin: MemStack Pro v3.2, Mar 2026)
