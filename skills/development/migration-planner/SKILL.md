---
name: migration-planner
description: "Use when the user says 'migration', 'schema change', 'database migration', 'alter table', or wants to plan safe database schema changes with rollback strategies."
---

# 🗃️ Migration Planner — Safe Database Schema Evolution
*Analyze schema differences, generate migration scripts with rollback, and plan zero-downtime deployment for production databases.*

## Activation

When this skill activates, output:

`🗃️ Migration Planner — Planning your database migration...`

| Context | Status |
|---------|--------|
| **User says "migration", "schema change", "database migration"** | ACTIVE |
| **User wants to alter tables, add columns, or change types** | ACTIVE |
| **User mentions rollback, zero-downtime, or breaking changes** | ACTIVE |
| **User wants to refactor code (not schema)** | DORMANT — see refactor-planner |
| **User wants to write tests for migration code** | DORMANT — see test-writer |
| **User wants a full API integration (data sync, not schema)** | DORMANT — see api-integration |

## Protocol

### Step 1: Gather Inputs

Ask the user for:
- **Current schema**: What does the database look like now? (SQL dump, ORM models, or describe)
- **Desired schema**: What should it look like after migration?
- **Database**: PostgreSQL, MySQL, SQLite, MongoDB?
- **ORM**: Prisma, Drizzle, Knex, TypeORM, raw SQL?
- **Environment**: Is this running in production with live data?
- **Data volume**: Rough row counts for affected tables
- **Downtime tolerance**: Can you take the app offline, or must it be zero-downtime?

### Step 2: Analyze Schema Differences

Compare current vs desired and categorize changes:

| Change | Table | Column | Type | Risk Level |
|--------|-------|--------|------|------------|
| ADD column | [table] | [column] | [type] | 🟢 Low — nullable or has default |
| ADD column (NOT NULL) | [table] | [column] | [type] | 🟡 Medium — needs data backfill |
| RENAME column | [table] | [old → new] | — | 🔴 High — breaks all queries using old name |
| CHANGE type | [table] | [column] | [old → new] | 🔴 High — data loss possible |
| DROP column | [table] | [column] | — | 🔴 High — irreversible data loss |
| ADD table | [table] | — | — | 🟢 Low — no existing data affected |
| DROP table | [table] | — | — | 🔴 High — all data lost |
| ADD index | [table] | [columns] | — | 🟡 Medium — locks table during creation |
| ADD constraint | [table] | [constraint] | — | 🟡 Medium — existing data may violate |
| ADD foreign key | [table] | [column → ref] | — | 🟡 Medium — existing data must satisfy |

### Step 3: Generate Migration Scripts

For each change, provide up and down scripts:

```sql
-- Migration: [NNN]_[descriptive_name]
-- Created: [date]
-- Description: [what this migration does]

-- ========== UP ==========

-- Step 1: [description]
ALTER TABLE [table] ADD COLUMN [column] [type] [constraints];

-- Step 2: [description]
UPDATE [table] SET [column] = [default_value] WHERE [column] IS NULL;

-- Step 3: [description]
ALTER TABLE [table] ALTER COLUMN [column] SET NOT NULL;

-- ========== DOWN ==========

-- Reverse Step 3
ALTER TABLE [table] ALTER COLUMN [column] DROP NOT NULL;

-- Reverse Step 1 (Step 2 data is lost on rollback)
ALTER TABLE [table] DROP COLUMN [column];
```

**Migration file naming:**
```
001_create_users_table.sql
002_add_email_to_users.sql
003_create_orders_table.sql
004_add_user_id_fk_to_orders.sql
```

**ORM-specific formats:**

Prisma:
```prisma
// schema.prisma change
model User {
  id    String @id @default(uuid())
  email String @unique          // ← added
  name  String
}
// Run: npx prisma migrate dev --name add_email_to_users
```

Drizzle:
```typescript
// drizzle/migrations/0001_add_email.ts
import { sql } from 'drizzle-orm';
import { pgTable, text } from 'drizzle-orm/pg-core';

export async function up(db) {
  await db.execute(sql`ALTER TABLE users ADD COLUMN email TEXT UNIQUE`);
}

export async function down(db) {
  await db.execute(sql`ALTER TABLE users DROP COLUMN email`);
}
```

### Step 4: Handle Data Migrations

When schema changes require data transformation:

```sql
-- Data migration: transform existing data to fit new schema

-- Step 1: Add new column (nullable)
ALTER TABLE orders ADD COLUMN amount_cents INTEGER;

-- Step 2: Backfill data (batch to avoid locking)
DO $$
DECLARE
  batch_size INTEGER := 1000;
  rows_updated INTEGER;
BEGIN
  LOOP
    UPDATE orders
    SET amount_cents = (amount * 100)::INTEGER
    WHERE amount_cents IS NULL
    AND id IN (
      SELECT id FROM orders
      WHERE amount_cents IS NULL
      LIMIT batch_size
    );

    GET DIAGNOSTICS rows_updated = ROW_COUNT;
    EXIT WHEN rows_updated = 0;

    RAISE NOTICE 'Updated % rows', rows_updated;
    PERFORM pg_sleep(0.1); -- Brief pause to reduce lock pressure
  END LOOP;
END $$;

-- Step 3: Verify backfill
SELECT COUNT(*) FROM orders WHERE amount_cents IS NULL;
-- Expected: 0

-- Step 4: Add NOT NULL constraint
ALTER TABLE orders ALTER COLUMN amount_cents SET NOT NULL;

-- Step 5: Drop old column (only after code is updated)
-- ALTER TABLE orders DROP COLUMN amount;
-- ⚠️ DO NOT run Step 5 until all code reads from amount_cents
```

**Data migration rules:**
- Always batch large updates (1000-10000 rows per batch)
- Add `pg_sleep()` between batches to reduce lock contention
- Verify data integrity after backfill before adding constraints
- Never drop old columns in the same migration as adding new ones

### Step 5: Zero-Downtime Strategy

For production migrations that can't tolerate downtime:

**Phase approach:**

| Phase | Migration Action | Code Change | Duration |
|-------|-----------------|-------------|----------|
| **Phase 1** | Add new column (nullable) | None — old code ignores new column | Minutes |
| **Phase 2** | Backfill data | None — background job | Hours |
| **Phase 3** | Deploy code that writes to BOTH columns | Dual-write code | Deploy cycle |
| **Phase 4** | Deploy code that reads from NEW column | Switch read path | Deploy cycle |
| **Phase 5** | Add NOT NULL constraint | None | Minutes |
| **Phase 6** | Deploy code that stops writing OLD column | Remove dual-write | Deploy cycle |
| **Phase 7** | Drop old column | None — column unused | Minutes |

**Column rename (zero-downtime):**
```
Step 1: Add new column → Step 2: Dual-write both → Step 3: Backfill →
Step 4: Read from new → Step 5: Stop writing old → Step 6: Drop old
```

**Table rename (zero-downtime):**
```
Step 1: Create new table → Step 2: Dual-write → Step 3: Backfill →
Step 4: Switch reads → Step 5: Stop writing old → Step 6: Drop old
```

### Step 6: Rollback Plan

For every migration step, define the rollback:

| Migration Step | Rollback Action | Data Loss? | Time to Rollback |
|----------------|----------------|------------|-----------------|
| ADD column | DROP column | No (column was empty) | Seconds |
| Backfill data | No action needed (old column still has data) | No | Instant |
| ADD NOT NULL | DROP NOT NULL | No | Seconds |
| DROP old column | ⚠️ CANNOT rollback — data is gone | YES | N/A |
| RENAME column | RENAME back | No | Seconds |
| CHANGE type | CHANGE back (if no data loss) | Maybe | Seconds-minutes |

**Rollback rules:**
- Every migration must have a tested DOWN script
- DROP and data-destructive operations get a **24-hour holding period** — deploy migration, wait, then drop
- Before dropping anything, verify no code references the old schema
- Keep database backups from before the migration for 7 days minimum

**Emergency rollback procedure:**
```
1. Stop the application (or route traffic away)
2. Run DOWN migration: [specific command]
3. Deploy previous code version
4. Verify application health
5. Investigate what went wrong
```

### Step 7: Check for Breaking Changes

Audit all code that touches affected tables:

| Breaking Change | Detection | Mitigation |
|----------------|-----------|------------|
| Column renamed | Grep for old column name in codebase | Dual-column period, then rename in code |
| Column type changed | Find all queries/ORM refs to column | Verify type coercion or explicit cast |
| Column dropped | Grep for column name in all queries | Remove all references before dropping |
| NOT NULL added | Find INSERT/UPDATE without this column | Add default or update all write paths |
| Foreign key added | Check for orphaned rows | Clean up orphans before adding FK |
| Index added | Check table size and lock behavior | Use `CONCURRENTLY` for large tables |

**PostgreSQL concurrent index creation:**
```sql
-- Won't lock the table (PostgreSQL only)
CREATE INDEX CONCURRENTLY idx_orders_user_id ON orders(user_id);
```

### Step 8: Dependency Order

Determine safe migration sequence:

```
── MIGRATION ORDER ────────────────────────

1. [independent tables first — no foreign keys]
2. [parent/referenced tables]
3. [child/referencing tables — have FKs to step 2]
4. [indexes and constraints — after data is in place]
5. [data backfills — after schema is ready]
6. [cleanup — drop old columns/tables]

DEPENDENCY GRAPH:
  users (no deps) → migrate first
    ↓
  orders (FK → users) → migrate second
    ↓
  order_items (FK → orders) → migrate third
```

**Rules:**
- Create referenced tables before referencing tables
- Add foreign keys AFTER both tables exist and data is valid
- Drop foreign keys BEFORE dropping referenced tables
- Run data migrations AFTER schema changes, BEFORE constraints

### Step 9: Output

Present the complete migration plan:

```
━━━ MIGRATION PLAN ━━━━━━━━━━━━━━━━━━━━━━━

── SCHEMA DIFF ────────────────────────────
[change table: type, table, column, risk]

── MIGRATION FILES ────────────────────────
001_[name].sql
  UP: [SQL]
  DOWN: [SQL]

002_[name].sql
  UP: [SQL]
  DOWN: [SQL]

── DATA MIGRATIONS ────────────────────────
[backfill scripts with batching]

── ZERO-DOWNTIME PLAN ─────────────────────
Phase 1: [action] — [timing]
Phase 2: [action] — [timing]
...

── ROLLBACK PLAN ──────────────────────────
[per-step rollback actions with data loss flags]

── BREAKING CHANGES ───────────────────────
[code audit results]

── DEPENDENCY ORDER ───────────────────────
[migration sequence with FK graph]

── DEPLOYMENT CHECKLIST ───────────────────
□ Backup database before starting
□ Run migrations in staging first
□ Verify data integrity after each step
□ Monitor error rates during deployment
□ Keep rollback scripts ready for 24 hours
□ Drop old columns only after 24-hour hold
```

## Inputs
- Current schema (SQL, ORM models, or description)
- Desired schema changes
- Database type and ORM
- Production status and data volume
- Downtime tolerance

## Outputs
- Schema diff analysis with risk levels per change
- Numbered migration files with UP/DOWN scripts
- Data migration scripts with batching for large tables
- Zero-downtime deployment strategy (phased approach)
- Rollback plan per migration step with data loss flags
- Breaking change audit (code references to changed schema)
- Dependency-ordered migration sequence
- Deployment checklist

## Level History

- **Lv.1** — Base: Schema diff analysis with risk categorization, UP/DOWN migration scripts (raw SQL + Prisma + Drizzle), batched data migrations, zero-downtime phased deployment, per-step rollback plans, breaking change detection, FK dependency ordering, deployment checklist. (Origin: MemStack v3.2, Mar 2026)
