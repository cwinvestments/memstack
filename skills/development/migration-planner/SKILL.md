---
name: memstack-development-migration-planner
description: "Use this skill when the user says 'migration', 'schema change', 'database migration', 'alter table', 'add column', 'change type', 'rollback plan', or needs safe database schema evolution with zero-downtime strategies. Do NOT use for initial database design (use database-architect) or code refactoring."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# Migration Planner — Planning database migration...
*Plans safe database schema migrations with zero-downtime strategies, rollback procedures, data validation checkpoints, and version tracking for PostgreSQL, MySQL, and SQLite.*

## Activation

When this skill activates, output:

`Migration Planner — Planning database migration...`

Then execute the protocol below.

## Context Guard

| Context | Status |
|---------|--------|
| User says "migration", "schema change", "database migration" | ACTIVE |
| User says "alter table", "add column", "change type", "rollback plan" | ACTIVE |
| User wants to evolve an existing database schema safely | ACTIVE |
| User wants to design a new database from scratch | DORMANT — use Database Architect |
| User wants to refactor application code | DORMANT — use Refactor Planner |

## Common Mistakes

| Mistake | Why It's Wrong |
|---------|---------------|
| "Just ALTER TABLE in production" | Unplanned schema changes cause outages. Lock durations, data backfills, and app compatibility all need planning. |
| "No rollback plan" | Migrations fail. Without a tested rollback, a failed deploy means manual emergency recovery at 3 AM. |
| "Rename columns directly" | Renaming breaks all queries referencing the old name instantly. Use add → migrate → drop (3-phase). |
| "Big bang data migration" | Migrating millions of rows in one transaction locks the table for minutes/hours. Batch in chunks. |
| "Skip validation" | Assuming data migrated correctly without checking is gambling. Validate row counts, checksums, and spot checks. |

## Protocol

### Step 1: Gather Migration Requirements

If the user hasn't provided details, ask:

> 1. **Database** — what engine? (PostgreSQL, MySQL, SQLite, MongoDB)
> 2. **Current schema** — what does the table/schema look like now?
> 3. **Target schema** — what should it look like after migration?
> 4. **Data volume** — how many rows in affected tables?
> 5. **Downtime tolerance** — zero-downtime required, or maintenance window OK?
> 6. **Migration tool** — what do you use? (Prisma, Knex, Flyway, Alembic, raw SQL, other)

### Step 2: Classify the Migration

**Migration type classification:**

| Change Type | Risk | Lock Behavior (PostgreSQL) | Strategy |
|------------|------|---------------------------|----------|
| **Add column (nullable)** | Low | Brief `ACCESS EXCLUSIVE` lock | Direct ALTER |
| **Add column (with default)** | Low (PG 11+) | Brief lock (PG 11+ doesn't rewrite) | Direct ALTER |
| **Add column (NOT NULL, no default)** | High | Fails on existing rows | Add nullable → backfill → add constraint |
| **Drop column** | Medium | Brief lock, but app must not reference it | Remove app refs first → then DROP |
| **Rename column** | High | Breaks all queries instantly | 3-phase: add new → migrate → drop old |
| **Change column type** | High | Full table rewrite + lock | New column → backfill → swap → drop |
| **Add index** | Medium | Blocks writes (without CONCURRENTLY) | `CREATE INDEX CONCURRENTLY` |
| **Add foreign key** | Medium | Validates all rows (lock) | `NOT VALID` → `VALIDATE CONSTRAINT` separately |
| **Drop table** | High | Irreversible data loss | Backup → verify no refs → drop |
| **Add table** | Low | No lock on existing tables | Direct CREATE |

**Migration classification output:**

```markdown
## Migration Classification

| # | Change | Type | Risk | Lock Duration | Strategy |
|---|--------|------|------|--------------|----------|
| 1 | [Change description] | [Type] | Low/Med/High | [Est. duration] | [Strategy] |
| 2 | [Change description] | [Type] | Low/Med/High | [Est. duration] | [Strategy] |
```

### Step 3: Design the Migration

**Safe migration patterns:**

**Pattern A: Add nullable column (simple, low risk)**

```sql
-- Migration UP
ALTER TABLE users ADD COLUMN phone VARCHAR(20);

-- Migration DOWN
ALTER TABLE users DROP COLUMN phone;
```

**Pattern B: Add NOT NULL column (3-step)**

```sql
-- Step 1: Add nullable column
ALTER TABLE users ADD COLUMN status VARCHAR(20);

-- Step 2: Backfill existing rows (in batches)
UPDATE users SET status = 'active' WHERE status IS NULL AND id BETWEEN 1 AND 10000;
UPDATE users SET status = 'active' WHERE status IS NULL AND id BETWEEN 10001 AND 20000;
-- ... continue in batches

-- Step 3: Add NOT NULL constraint
ALTER TABLE users ALTER COLUMN status SET NOT NULL;
ALTER TABLE users ALTER COLUMN status SET DEFAULT 'active';
```

**Pattern C: Rename column (3-phase, zero-downtime)**

```sql
-- Phase 1: Add new column + trigger
ALTER TABLE orders ADD COLUMN total_amount DECIMAL(10,2);
-- Create trigger to sync old → new
CREATE OR REPLACE FUNCTION sync_amount() RETURNS TRIGGER AS $$
BEGIN
  NEW.total_amount := NEW.amount;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER sync_amount_trigger BEFORE INSERT OR UPDATE ON orders
  FOR EACH ROW EXECUTE FUNCTION sync_amount();

-- Phase 2: Backfill existing rows
UPDATE orders SET total_amount = amount WHERE total_amount IS NULL AND id BETWEEN 1 AND 10000;

-- Phase 3: (After app code updated to use total_amount)
DROP TRIGGER sync_amount_trigger ON orders;
DROP FUNCTION sync_amount();
ALTER TABLE orders DROP COLUMN amount;
```

**Pattern D: Change column type (safe swap)**

```sql
-- Step 1: Add new column with target type
ALTER TABLE products ADD COLUMN price_v2 DECIMAL(12,4);

-- Step 2: Backfill with type conversion
UPDATE products SET price_v2 = price::DECIMAL(12,4) WHERE id BETWEEN 1 AND 10000;

-- Step 3: Swap columns (after app code updated)
ALTER TABLE products DROP COLUMN price;
ALTER TABLE products RENAME COLUMN price_v2 TO price;
```

**Pattern E: Add index without blocking writes**

```sql
-- PostgreSQL: CONCURRENTLY avoids blocking writes (cannot run in a transaction)
CREATE INDEX CONCURRENTLY idx_users_email ON users (email);

-- MySQL 5.6+: ALGORITHM=INPLACE avoids table copy
ALTER TABLE users ADD INDEX idx_email (email), ALGORITHM=INPLACE, LOCK=NONE;
```

**Pattern F: Add foreign key without full scan lock**

```sql
-- Step 1: Add constraint as NOT VALID (skips validation, brief lock)
ALTER TABLE orders ADD CONSTRAINT fk_orders_user
  FOREIGN KEY (user_id) REFERENCES users(id) NOT VALID;

-- Step 2: Validate separately (scans but allows concurrent writes)
ALTER TABLE orders VALIDATE CONSTRAINT fk_orders_user;
```

### Step 4: Data Backfill Strategy

For migrations that require updating existing data:

**Batch processing template:**

```sql
-- Batch update to avoid long locks
DO $$
DECLARE
  batch_size INT := 10000;
  rows_updated INT;
BEGIN
  LOOP
    UPDATE target_table
    SET new_column = compute_value(old_column)
    WHERE new_column IS NULL
    AND id IN (
      SELECT id FROM target_table
      WHERE new_column IS NULL
      LIMIT batch_size
      FOR UPDATE SKIP LOCKED
    );

    GET DIAGNOSTICS rows_updated = ROW_COUNT;
    RAISE NOTICE 'Updated % rows', rows_updated;

    EXIT WHEN rows_updated = 0;

    -- Brief pause to reduce load
    PERFORM pg_sleep(0.1);
  END LOOP;
END $$;
```

**Backfill sizing guide:**

| Table Size | Batch Size | Estimated Time | Pause Between |
|-----------|-----------|---------------|--------------|
| <10K rows | All at once | <1 second | None |
| 10K-100K | 10,000 | 10-60 seconds | 100ms |
| 100K-1M | 10,000 | 1-10 minutes | 100ms |
| 1M-10M | 50,000 | 10-60 minutes | 200ms |
| 10M-100M | 50,000 | 1-8 hours | 500ms |
| >100M | 100,000 | Schedule off-peak | 1s |

### Step 5: Write Rollback Procedures

Every migration MUST have a tested rollback:

```markdown
## Rollback Plan

### Automatic Rollback (migration tool)
[Migration tool command to roll back, e.g.:]
- Prisma: `npx prisma migrate resolve --rolled-back [migration_name]`
- Knex: `npx knex migrate:rollback`
- Flyway: `flyway undo`
- Alembic: `alembic downgrade -1`

### Manual Rollback SQL
[Exact SQL to reverse the migration — tested before deploying forward]

### Rollback Verification
After rolling back, verify:
- [ ] Schema matches pre-migration state
- [ ] Row counts unchanged
- [ ] Application health check passes
- [ ] No orphaned data or broken references

### Point of No Return
[Define when rollback is no longer possible:]
- After Phase 2 backfill: rollback requires data reconstruction
- After old column drop: rollback requires restore from backup
- After app code deployed to new schema: rollback requires app revert too
```

**Rollback SQL templates:**

| Migration Type | Rollback SQL |
|---------------|-------------|
| Add column | `ALTER TABLE t DROP COLUMN c;` |
| Drop column | Restore from backup (cannot undo) |
| Add index | `DROP INDEX idx_name;` |
| Add constraint | `ALTER TABLE t DROP CONSTRAINT c_name;` |
| Rename column | `ALTER TABLE t RENAME COLUMN new TO old;` |
| Change type | Reverse swap (if old column still exists) |

### Step 6: Validation Checkpoints

Verify migration correctness at each stage:

**Pre-migration checks:**

```sql
-- Record baseline metrics before migration
SELECT COUNT(*) AS total_rows FROM target_table;
SELECT COUNT(*) AS null_count FROM target_table WHERE critical_column IS NULL;
SELECT pg_total_relation_size('target_table') AS table_size;
```

**Post-migration checks:**

```sql
-- Verify row count unchanged (no accidental deletes)
SELECT COUNT(*) AS total_rows FROM target_table;
-- Should match pre-migration count

-- Verify new column populated correctly
SELECT COUNT(*) AS null_count FROM target_table WHERE new_column IS NULL;
-- Should be 0 (after backfill)

-- Verify data integrity
SELECT COUNT(*) FROM target_table WHERE new_column != expected_transform(old_column);
-- Should be 0

-- Verify constraints active
SELECT conname, convalidated FROM pg_constraint WHERE conrelid = 'target_table'::regclass;
-- All should show convalidated = true

-- Spot check random sample
SELECT * FROM target_table ORDER BY RANDOM() LIMIT 10;
-- Manual verification of data correctness
```

**Validation checklist:**

```markdown
## Migration Validation

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| Row count (before) | [X] | [X] | [OK / FAIL] |
| Row count (after) | [X] | [X] | [OK / FAIL] |
| Null count (new column) | 0 | [X] | [OK / FAIL] |
| Constraint validation | All valid | [X] | [OK / FAIL] |
| App health check | 200 OK | [X] | [OK / FAIL] |
| Query performance | <[X]ms | [X]ms | [OK / FAIL] |
```

### Step 7: Build Migration Plan

Assemble everything into an execution plan:

```markdown
## Migration Execution Plan

### Pre-Flight
- [ ] Backup database (verified restore works)
- [ ] Test migration on staging with production-size data
- [ ] Verify rollback works on staging
- [ ] Schedule maintenance window (if needed): [Date, Time, Duration]
- [ ] Notify stakeholders: [Who to notify]
- [ ] Record baseline metrics

### Execution Steps

**Phase 1: Schema Change** (estimated: [X] minutes)
1. [ ] Run migration: `[migration command]`
2. [ ] Verify schema change applied
3. [ ] Checkpoint: app still functional

**Phase 2: Data Backfill** (estimated: [X] minutes)
1. [ ] Start batch backfill: `[backfill command]`
2. [ ] Monitor progress: `[monitoring query]`
3. [ ] Checkpoint: verify [X]% of rows updated

**Phase 3: Constraint Enforcement** (estimated: [X] minutes)
1. [ ] Add NOT NULL / constraints: `[constraint SQL]`
2. [ ] Validate constraints: `[validation SQL]`
3. [ ] Checkpoint: all constraints valid

**Phase 4: Cleanup** (after app code deployed)
1. [ ] Remove old column/trigger: `[cleanup SQL]`
2. [ ] Run VACUUM ANALYZE: `VACUUM ANALYZE target_table;`
3. [ ] Verify final schema matches target

### Post-Migration
- [ ] Run validation checklist (Step 6)
- [ ] Verify application logs — no errors
- [ ] Monitor query performance for 24 hours
- [ ] Update schema documentation
- [ ] Close migration ticket
```

### Step 8: Version Tracking

**Migration file naming convention:**

| Tool | Convention | Example |
|------|----------|---------|
| Prisma | Auto-generated timestamp | `20260303120000_add_phone_to_users/` |
| Knex | `YYYYMMDDHHMMSS_description.js` | `20260303120000_add_phone_to_users.js` |
| Flyway | `V[version]__Description.sql` | `V2.1__Add_phone_to_users.sql` |
| Alembic | Auto-generated revision ID | `a1b2c3d4_add_phone_to_users.py` |
| Raw SQL | `[sequence]_[description].sql` | `003_add_phone_to_users.sql` |

**Migration log table (for raw SQL projects):**

```sql
CREATE TABLE IF NOT EXISTS schema_migrations (
  id SERIAL PRIMARY KEY,
  version VARCHAR(50) NOT NULL UNIQUE,
  description VARCHAR(255),
  applied_at TIMESTAMP DEFAULT NOW(),
  execution_time_ms INTEGER,
  rolled_back_at TIMESTAMP,
  checksum VARCHAR(64)
);
```

## Output Format

```markdown
# Migration Plan — [Description]

## Classification
[From Step 2 — change types, risk levels, strategies]

## Migration SQL
[From Step 3 — forward migration with safe patterns]

## Backfill Strategy
[From Step 4 — batch processing plan, if data migration needed]

## Rollback Plan
[From Step 5 — rollback SQL + point of no return]

## Validation
[From Step 6 — pre/post checks with expected values]

## Execution Plan
[From Step 7 — phased checklist with time estimates]

## Version
[From Step 8 — migration file naming and tracking]
```

## Completion

```
Migration Planner — Complete!

Database: [Engine]
Changes: [X] schema changes planned
Risk level: [Overall Low/Medium/High]
Estimated execution: [X] minutes
Downtime required: [Zero / X minutes window]
Rollback tested: [Yes/No]

Next steps:
1. Test migration on staging with production-size data
2. Test rollback on staging — verify clean reversal
3. Run validation queries after staging migration
4. Schedule production migration: [suggested window]
5. Execute migration following the phased checklist
6. Monitor for 24 hours post-migration
```

## Level History

- **Lv.1** — Base: 10 migration types with risk/lock classification, 6 safe migration patterns (add nullable, add NOT NULL 3-step, rename 3-phase, type swap, concurrent index, NOT VALID FK), batch backfill with sizing guide, rollback procedures with point-of-no-return, pre/post validation checkpoints, phased execution plan template, version tracking conventions for 5 tools. (Origin: MemStack Pro v3.2, Mar 2026)
