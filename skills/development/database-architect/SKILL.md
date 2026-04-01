---
name: memstack-development-database-architect
description: "Use this skill when the user says 'design database', 'create tables', 'database schema', 'add table', 'database architect', 'ERD', 'data model', or is designing Supabase/Postgres table structures, relationships, RLS policies, or migrations. Do NOT use for schema migration of existing tables (use migration-planner) or code refactoring."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# 🗄️ Database Architect — Designing schema, relationships, and policies...
*Produces production-ready Supabase/Postgres schemas with proper naming, relationships, RLS policies, indexes, and migration SQL.*

## Activation

When this skill activates, output:

`🗄️ Database Architect — Analyzing requirements and designing schema...`

Then execute the protocol below.

| Context | Status |
|---------|--------|
| User says "design database" or "create tables" or "add table" | ACTIVE |
| User says "database schema" or "ERD" or "data model" | ACTIVE |
| Building a new feature that needs persistent storage | ACTIVE |
| Writing migration SQL for Supabase | ACTIVE |
| Querying existing data or debugging SQL | DORMANT |
| Discussing database concepts generally | DORMANT |

### Anti-patterns

| Trap | Reality Check |
|------|---------------|
| "I'll add RLS later" | RLS is the auth layer in Supabase. No RLS = public data. Design it with the schema. |
| "JSONB for everything" | JSONB skips type safety, indexing, and foreign keys. Use it for truly flexible data, not as a schema-avoidance crutch. |
| "I'll index when it's slow" | Known query patterns should get indexes from day one. Adding indexes to production tables locks writes. |
| "Free text for status" | `status TEXT` invites typos and inconsistency. Use an enum: `CREATE TYPE order_status AS ENUM (...)`. |
| "One big table is simpler" | Wide tables with nullable columns signal missing normalization. Split into focused tables with proper FKs. |
| "snake_case is just preference" | Supabase auto-generates TypeScript types from your schema. Inconsistent naming produces inconsistent types. Pick snake_case and enforce it. |

## Protocol

### Step 1: Gather Requirements

Before designing, understand what the data needs to represent:

1. **What entities exist?** (users, orders, products, organizations, etc.)
2. **What are the relationships?** (one-to-many, many-to-many, self-referential)
3. **Who accesses what?** (public data, org-scoped, user-private, admin-only)
4. **What are the query patterns?** (list by org, search by name, filter by date range)
5. **What status flows exist?** (draft → published, pending → approved → rejected)

If the user hasn't specified, ask:

> What entities and relationships does this feature need? Who should be able to read/write each table?

### Step 2: Design Table Structure

Apply naming conventions strictly:

| Convention | Rule | Example |
|------------|------|---------|
| Table names | `snake_case`, **plural** | `order_items`, `user_profiles` |
| Column names | `snake_case` | `first_name`, `created_at` |
| Foreign keys | `{singular_table}_id` | `user_id`, `organization_id` |
| Primary keys | `id` (uuid) | `id UUID DEFAULT gen_random_uuid()` |
| Junction tables | `{table1}_{table2}` alphabetical | `organizations_users` |
| Enums | `{table}_{column}` or descriptive | `order_status`, `subscription_tier` |
| Indexes | `idx_{table}_{columns}` | `idx_orders_org_id_created_at` |

**Standard columns on every table:**

```sql
id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
```

**Auto-update `updated_at`:**

```sql
-- Create this function once per database
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to each table
CREATE TRIGGER set_updated_at
  BEFORE UPDATE ON table_name
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();
```

### Step 3: Define Relationships

Design foreign keys with explicit constraint naming and cascading behavior:

```sql
-- One-to-many: organization has many projects
ALTER TABLE projects
  ADD CONSTRAINT fk_projects_organization
  FOREIGN KEY (organization_id) REFERENCES organizations(id)
  ON DELETE CASCADE;

-- Many-to-many: users belong to many organizations
CREATE TABLE organizations_users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  role TEXT NOT NULL DEFAULT 'member' CHECK (role IN ('owner', 'admin', 'member', 'viewer')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (organization_id, user_id)
);
```

**Cascade rules:**

| Relationship | ON DELETE | Rationale |
|-------------|-----------|-----------|
| Org → Projects | CASCADE | Deleting org removes its projects |
| User → Profile | CASCADE | Deleting user removes profile |
| Order → Items | CASCADE | Deleting order removes line items |
| User → Orders | RESTRICT | Don't delete user if they have orders |
| Category → Products | SET NULL | Keep products, clear category |

### Step 4: Design RLS Policies

Every table needs RLS enabled with explicit policies. No exceptions.

```sql
-- Enable RLS (do this for EVERY table)
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
```

**Common RLS patterns:**

```sql
-- Pattern 1: User owns their own rows
CREATE POLICY "Users read own data"
  ON user_profiles FOR SELECT
  USING (auth.uid() = user_id);

-- Pattern 2: Org-scoped access (most common in multi-tenant apps)
CREATE POLICY "Org members read projects"
  ON projects FOR SELECT
  USING (
    organization_id IN (
      SELECT organization_id FROM organizations_users
      WHERE user_id = auth.uid()
    )
  );

-- Pattern 3: Role-based write access
CREATE POLICY "Org admins write projects"
  ON projects FOR INSERT
  WITH CHECK (
    organization_id IN (
      SELECT organization_id FROM organizations_users
      WHERE user_id = auth.uid()
      AND role IN ('owner', 'admin')
    )
  );

-- Pattern 4: Public read, authenticated write
CREATE POLICY "Public read"
  ON articles FOR SELECT
  USING (published = true);

CREATE POLICY "Authors write own articles"
  ON articles FOR UPDATE
  USING (author_id = auth.uid());

-- Pattern 5: Service role bypass (for server-side operations)
-- Use supabase.rpc() or service_role key — RLS is bypassed with service role
```

**RLS checklist per table:**

| Operation | Policy | Who Can? |
|-----------|--------|----------|
| SELECT | Read own / org-scoped / public | Define per table |
| INSERT | Org members / authenticated / admin-only | Define per table |
| UPDATE | Owner / admin / role-based | Define per table |
| DELETE | Owner / admin / restrict | Define per table |

### Step 5: Create Indexes

Design indexes based on known query patterns:

```sql
-- Foreign keys used in JOINs (always index these)
CREATE INDEX idx_projects_organization_id ON projects(organization_id);
CREATE INDEX idx_orders_user_id ON orders(user_id);

-- Composite index for common filter + sort
CREATE INDEX idx_orders_org_created ON orders(organization_id, created_at DESC);

-- Partial index for active records (skip soft-deleted)
CREATE INDEX idx_projects_active ON projects(organization_id)
  WHERE deleted_at IS NULL;

-- GIN index for JSONB columns (if used)
CREATE INDEX idx_settings_metadata ON settings USING GIN(metadata);

-- Full-text search index
CREATE INDEX idx_articles_search ON articles USING GIN(
  to_tsvector('english', title || ' ' || content)
);
```

**Index decision matrix:**

| Query Pattern | Index Type | Example |
|--------------|-----------|---------|
| `WHERE fk_id = ?` | B-tree (single column) | `idx_orders_user_id` |
| `WHERE fk_id = ? ORDER BY created_at` | B-tree (composite) | `idx_orders_user_created` |
| `WHERE status = 'active'` | Partial index | `WHERE status = 'active'` |
| `WHERE metadata @> '{}'` | GIN | JSONB containment queries |
| `WHERE to_tsvector(...) @@ ?` | GIN | Full-text search |
| `WHERE col LIKE 'prefix%'` | B-tree (text_pattern_ops) | Prefix search |

**Don't index:**
- Boolean columns with low cardinality (Postgres won't use the index)
- Columns that are rarely queried
- Tables with < 1000 rows (sequential scan is faster)

### Step 6: Use JSONB Appropriately

JSONB is powerful but should be used intentionally:

**✅ Good use cases:**
- User preferences/settings (schema varies per user)
- External API response caching (shape is unstable)
- Metadata that varies by record type (e.g., `metadata` on polymorphic tables)
- Audit log payloads (recording what changed)

**❌ Bad use cases:**
- Core business fields (use typed columns instead)
- Fields you query frequently (use dedicated columns + indexes)
- Replacing relationships (use junction tables)
- Fields that need foreign key constraints (JSONB can't reference other tables)

```sql
-- Good: flexible metadata alongside typed columns
CREATE TABLE products (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  price_cents INTEGER NOT NULL,
  category_id UUID REFERENCES categories(id),
  metadata JSONB DEFAULT '{}'::jsonb,    -- flexible extras
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### Step 7: Define Enums for Status Fields

```sql
-- Create enum types for finite status sets
CREATE TYPE order_status AS ENUM (
  'draft', 'pending', 'confirmed', 'processing',
  'shipped', 'delivered', 'cancelled', 'refunded'
);

CREATE TYPE subscription_tier AS ENUM (
  'free', 'starter', 'professional', 'enterprise'
);

-- Use in table definition
CREATE TABLE orders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  status order_status NOT NULL DEFAULT 'draft',
  -- ...
);
```

**Enum vs CHECK constraint vs lookup table:**

| Approach | When to Use | Trade-off |
|----------|------------|-----------|
| `CREATE TYPE ... AS ENUM` | Fixed set, rarely changes | Adding values requires `ALTER TYPE` |
| `CHECK (col IN (...))` | Very short lists (2-3 values) | Inline, no separate type |
| Lookup table | Values change often or have metadata | More flexible, extra JOIN |

**Adding values to an existing enum:**
```sql
ALTER TYPE order_status ADD VALUE 'on_hold' AFTER 'processing';
-- Note: you cannot remove or reorder enum values without recreating the type
```

### Step 8: Generate Migration SQL

Produce a complete, ordered migration file:

```sql
-- Migration: 001_create_[feature]_tables.sql
-- Description: [what this migration creates]
-- Date: YYYY-MM-DD

BEGIN;

-- 1. Create enum types
CREATE TYPE ...;

-- 2. Create tables (parent tables first, then children)
CREATE TABLE ...;

-- 3. Add foreign key constraints
ALTER TABLE ...;

-- 4. Create indexes
CREATE INDEX ...;

-- 5. Enable RLS on all tables
ALTER TABLE ... ENABLE ROW LEVEL SECURITY;

-- 6. Create RLS policies
CREATE POLICY ...;

-- 7. Create triggers (updated_at)
CREATE TRIGGER ...;

-- 8. Insert seed data (if needed)
INSERT INTO ...;

COMMIT;
```

**Migration rules:**
- Wrap in `BEGIN`/`COMMIT` for atomicity
- Create parent tables before children (FK dependency order)
- Always include a rollback script:

```sql
-- Rollback: 001_create_[feature]_tables.sql
BEGIN;
DROP TABLE IF EXISTS child_table CASCADE;
DROP TABLE IF EXISTS parent_table CASCADE;
DROP TYPE IF EXISTS custom_enum;
COMMIT;
```

### Step 9: Document Environment Variables

If new connection strings or configuration are needed, output `.env.example` entries:

```bash
# Database
DATABASE_URL=postgresql://user:pass@host:5432/dbname
DIRECT_URL=postgresql://user:pass@host:5432/dbname  # For migrations (bypasses pooler)

# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_ROLE_KEY=eyJ...    # Server-side only, never expose to client
```

**Remind user:** Add to `.env.local` with real values. Never commit secrets.

### Step 10: Output Summary

Present the complete design:

```
🗄️ Database Architect — Schema Complete

Feature: [name]
Tables: [count] new, [count] modified
Enums: [list]
Relationships: [count] foreign keys, [count] junction tables

ERD Summary:
  organizations ──< projects ──< tasks
       │                          │
       └──< organizations_users   └──< task_comments
                  │
              auth.users

RLS Policies: [count] policies across [count] tables
Indexes: [count] new indexes
Migration: [filename] ([line count] lines)

Files generated:
  - supabase/migrations/001_create_[feature].sql
  - supabase/migrations/001_create_[feature]_rollback.sql

Next steps:
  1. Review migration SQL
  2. Run: supabase db push (or supabase migration up)
  3. Verify RLS policies in Supabase dashboard → Auth → Policies
  4. Test queries with different user roles
```

## Level History

- **Lv.1** — Base: Requirements gathering, naming conventions, standard columns, relationship design, RLS policies, index strategy, JSONB guidance, enum patterns, migration generation, environment documentation. Based on Supabase patterns across AdminStack (40+ tables), EpsteinScan, DeedStack, and GreenAcres. (Origin: MemStack Pro v3.2, Mar 2026)
