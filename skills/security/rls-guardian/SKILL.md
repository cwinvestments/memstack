---
name: memstack-security-rls-guardian
description: "Use this skill when creating or altering database tables in Supabase or PostgreSQL projects. Triggers include: CREATE TABLE, ALTER TABLE, migration files, 'RLS', 'row level security', 'new table', 'database schema'. Enforces Row Level Security policies on every table to prevent unauthorized data access. Do NOT use for general SQL queries or non-schema database tasks."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# RLS Guardian — Enforcing Row Level Security...
*Enforces Row Level Security on every Supabase table creation, ensuring no table goes live without proper access policies. Provides 4 policy patterns, migration templates, pre-commit checks, and audit queries to find unprotected tables.*

## Activation

When this skill activates, output:

`RLS Guardian — Enforcing Row Level Security...`

Then execute the protocol below.

## Context Guard

| Context | Status |
|---------|--------|
| User writes CREATE TABLE or ALTER TABLE SQL | ACTIVE |
| User creates or edits a migration file | ACTIVE |
| User says "new table", "database schema", "add table" | ACTIVE |
| User says "RLS", "row level security", "table policies" | ACTIVE |
| User asks for a general RLS audit of existing tables | DORMANT — use RLS Checker |
| User asks a general SQL query unrelated to schema | DORMANT — do not activate |

## Common Mistakes

| Mistake | Why It's Wrong |
|---------|---------------|
| "Create table now, add RLS later" | Every minute without RLS is a window where all rows are accessible to any authenticated user. RLS must be in the same migration. |
| "Enable RLS but no policies" | `ALTER TABLE ENABLE ROW LEVEL SECURITY` with no policies blocks ALL access including the service role via API. Users get empty results, devs panic. |
| "Only add a SELECT policy" | SELECT-only leaves INSERT, UPDATE, DELETE wide open. All 4 operations need explicit policies. |
| "Use `true` as the policy expression" | `USING (true)` makes the table world-readable. Only valid for genuinely public data (e.g. blog posts). Never for user data. |
| "Forget the service role" | Supabase service role bypasses RLS by design. But if you switch to `anon` key on the frontend, every table without policies is exposed. |

## Protocol

### Step 1: Classify the Table

Before writing any policy, classify the table's access pattern:

| Pattern | Description | Example Tables |
|---------|------------|---------------|
| **User-scoped** | Each row belongs to one user via `user_id` | profiles, settings, api_keys, notifications |
| **Org-scoped** | Rows belong to an organization; users access via membership | projects, invoices, team_settings |
| **Public-read** | Anyone can read, only owners can write | blog_posts, public_profiles, product_listings |
| **Junction** | Many-to-many relationship linking two entities | team_members, project_collaborators |
| **System** | Internal tables not accessed by end users | migrations, cron_jobs, audit_logs |

**Decision tree:**

```
Does the table have a user_id column?
  YES → Does it also have an org/account_id?
    YES → Org-scoped (access via membership check)
    NO  → User-scoped (direct user_id match)
  NO  → Is the data meant to be publicly readable?
    YES → Public-read (open SELECT, restricted writes)
    NO  → Is it a many-to-many join table?
      YES → Junction (inherit access from parent tables)
      NO  → System table (service role only, no RLS policies needed)
```

### Step 2: Write the Migration

Every table migration MUST include 3 parts in this order:
1. `CREATE TABLE` — the schema
2. `ALTER TABLE ENABLE ROW LEVEL SECURITY` — the lock
3. `CREATE POLICY` — the keys (all 4 operations)

**Pattern A: User-scoped table**

```sql
-- 1. Create table
CREATE TABLE user_settings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  theme TEXT DEFAULT 'dark',
  notifications_enabled BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- 2. Enable RLS (MUST be in same migration)
ALTER TABLE user_settings ENABLE ROW LEVEL SECURITY;

-- 3. Policies for all 4 operations
CREATE POLICY "Users can view own settings"
  ON user_settings FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own settings"
  ON user_settings FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own settings"
  ON user_settings FOR UPDATE
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own settings"
  ON user_settings FOR DELETE
  USING (auth.uid() = user_id);
```

**Pattern B: Org-scoped table**

```sql
-- 1. Create table
CREATE TABLE projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  account_id UUID NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  status TEXT DEFAULT 'active',
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- 2. Enable RLS
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;

-- 3. Policies with membership check
CREATE POLICY "Members can view org projects"
  ON projects FOR SELECT
  USING (
    account_id IN (
      SELECT account_id FROM account_members
      WHERE user_id = auth.uid()
    )
  );

CREATE POLICY "Members can insert org projects"
  ON projects FOR INSERT
  WITH CHECK (
    account_id IN (
      SELECT account_id FROM account_members
      WHERE user_id = auth.uid()
    )
  );

CREATE POLICY "Members can update org projects"
  ON projects FOR UPDATE
  USING (
    account_id IN (
      SELECT account_id FROM account_members
      WHERE user_id = auth.uid()
    )
  )
  WITH CHECK (
    account_id IN (
      SELECT account_id FROM account_members
      WHERE user_id = auth.uid()
    )
  );

CREATE POLICY "Members can delete org projects"
  ON projects FOR DELETE
  USING (
    account_id IN (
      SELECT account_id FROM account_members
      WHERE user_id = auth.uid()
    )
  );
```

**Pattern C: Public-read table**

```sql
-- 1. Create table
CREATE TABLE blog_posts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  author_id UUID NOT NULL REFERENCES auth.users(id),
  title TEXT NOT NULL,
  content TEXT,
  published BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- 2. Enable RLS
ALTER TABLE blog_posts ENABLE ROW LEVEL SECURITY;

-- 3. Public read, author-only write
CREATE POLICY "Anyone can view published posts"
  ON blog_posts FOR SELECT
  USING (published = true);

CREATE POLICY "Authors can insert own posts"
  ON blog_posts FOR INSERT
  WITH CHECK (auth.uid() = author_id);

CREATE POLICY "Authors can update own posts"
  ON blog_posts FOR UPDATE
  USING (auth.uid() = author_id)
  WITH CHECK (auth.uid() = author_id);

CREATE POLICY "Authors can delete own posts"
  ON blog_posts FOR DELETE
  USING (auth.uid() = author_id);
```

**Pattern D: Junction table**

```sql
-- 1. Create table
CREATE TABLE team_members (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  team_id UUID NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  role TEXT DEFAULT 'member',
  joined_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE(team_id, user_id)
);

-- 2. Enable RLS
ALTER TABLE team_members ENABLE ROW LEVEL SECURITY;

-- 3. Members can see co-members, only admins can manage
CREATE POLICY "Members can view team roster"
  ON team_members FOR SELECT
  USING (
    team_id IN (
      SELECT team_id FROM team_members
      WHERE user_id = auth.uid()
    )
  );

CREATE POLICY "Admins can add team members"
  ON team_members FOR INSERT
  WITH CHECK (
    team_id IN (
      SELECT team_id FROM team_members
      WHERE user_id = auth.uid() AND role = 'admin'
    )
  );

CREATE POLICY "Admins can update team members"
  ON team_members FOR UPDATE
  USING (
    team_id IN (
      SELECT team_id FROM team_members
      WHERE user_id = auth.uid() AND role = 'admin'
    )
  )
  WITH CHECK (
    team_id IN (
      SELECT team_id FROM team_members
      WHERE user_id = auth.uid() AND role = 'admin'
    )
  );

CREATE POLICY "Admins can remove team members"
  ON team_members FOR DELETE
  USING (
    team_id IN (
      SELECT team_id FROM team_members
      WHERE user_id = auth.uid() AND role = 'admin'
    )
  );
```

### Step 3: Pre-Commit Checklist

Before committing any migration that creates or alters a table, verify:

```markdown
## RLS Guardian Checklist

- [ ] `ALTER TABLE [name] ENABLE ROW LEVEL SECURITY` present in migration
- [ ] SELECT policy defined
- [ ] INSERT policy defined (with WITH CHECK)
- [ ] UPDATE policy defined (with both USING and WITH CHECK)
- [ ] DELETE policy defined
- [ ] Policy expressions use `auth.uid()` (not `current_setting()` or hardcoded UUIDs)
- [ ] Org-scoped tables use membership subquery (not direct account_id match)
- [ ] No `USING (true)` on non-public tables
- [ ] Policy names are descriptive (not "policy_1", "policy_2")
- [ ] RLS + policies are in the SAME migration file as CREATE TABLE
```

**Critical rule:** If any checkbox fails, do NOT commit. Fix first. A table without RLS in production is a data breach waiting to happen.

### Step 4: Audit Existing Tables

Run this query to find unprotected tables:

```sql
-- Find all public tables without RLS enabled
SELECT
  schemaname,
  tablename,
  rowsecurity
FROM pg_tables
WHERE schemaname = 'public'
  AND rowsecurity = false
ORDER BY tablename;
```

**Find tables with RLS enabled but missing policies:**

```sql
-- Tables with RLS but no policies (locked out — no access at all)
SELECT t.tablename
FROM pg_tables t
LEFT JOIN pg_policies p ON t.tablename = p.tablename
WHERE t.schemaname = 'public'
  AND t.rowsecurity = true
  AND p.policyname IS NULL
ORDER BY t.tablename;
```

**Find tables with incomplete policy coverage:**

```sql
-- Tables missing one or more CRUD policies
SELECT
  t.tablename,
  COUNT(CASE WHEN p.cmd = 'r' THEN 1 END) AS select_policies,
  COUNT(CASE WHEN p.cmd = 'a' THEN 1 END) AS insert_policies,
  COUNT(CASE WHEN p.cmd = 'w' THEN 1 END) AS update_policies,
  COUNT(CASE WHEN p.cmd = 'd' THEN 1 END) AS delete_policies
FROM pg_tables t
LEFT JOIN pg_policies p ON t.tablename = p.tablename
WHERE t.schemaname = 'public'
  AND t.rowsecurity = true
GROUP BY t.tablename
HAVING
  COUNT(CASE WHEN p.cmd = 'r' THEN 1 END) = 0
  OR COUNT(CASE WHEN p.cmd = 'a' THEN 1 END) = 0
  OR COUNT(CASE WHEN p.cmd = 'w' THEN 1 END) = 0
  OR COUNT(CASE WHEN p.cmd = 'd' THEN 1 END) = 0
ORDER BY t.tablename;
```

### Step 5: Handle Special Cases

**System tables (no user access needed):**

```sql
-- Mark as system table with comment, enable RLS with no policies
-- This blocks ALL access except service role (which bypasses RLS)
ALTER TABLE cron_jobs ENABLE ROW LEVEL SECURITY;
COMMENT ON TABLE cron_jobs IS 'rls:system — service role only, no user access';
```

**Tables with soft-delete:**

```sql
-- Include soft-delete filter in SELECT policy
CREATE POLICY "Users see own non-deleted records"
  ON documents FOR SELECT
  USING (auth.uid() = user_id AND deleted_at IS NULL);
```

**Tables with row-level roles:**

```sql
-- Different access levels within the same table
CREATE POLICY "Owners have full access"
  ON documents FOR ALL
  USING (auth.uid() = owner_id);

CREATE POLICY "Viewers can only read"
  ON documents FOR SELECT
  USING (
    id IN (
      SELECT document_id FROM document_shares
      WHERE user_id = auth.uid() AND permission = 'view'
    )
  );
```

**ALTER TABLE — adding columns:**

```sql
-- When adding a sensitive column to an existing table,
-- verify existing policies still cover the new data appropriately.
-- No new policies needed unless the column changes access logic.
ALTER TABLE profiles ADD COLUMN phone TEXT;
-- Existing RLS policies automatically apply to the new column.
-- But if phone should be more restricted, add a column-level grant:
REVOKE ALL ON profiles FROM anon, authenticated;
GRANT SELECT (id, name, avatar_url) ON profiles TO authenticated;
-- Then RLS + column grants together control both row AND column access.
```

## Output Format

When generating a migration that includes a table, output:

```markdown
## Migration: [description]

### Table Classification
| Table | Pattern | Key Column |
|-------|---------|-----------|
| [name] | [user/org/public/junction/system] | [user_id/account_id/etc.] |

### SQL
[Complete migration SQL with CREATE TABLE + ENABLE RLS + all 4 policies]

### RLS Guardian Checklist
- [x] RLS enabled in same migration
- [x] SELECT policy
- [x] INSERT policy
- [x] UPDATE policy
- [x] DELETE policy
- [x] Uses auth.uid()
- [x] Descriptive policy names
```

## Completion

```
RLS Guardian — Enforced!

Table: [name]
Pattern: [user-scoped / org-scoped / public-read / junction / system]
Policies: [count] (SELECT, INSERT, UPDATE, DELETE)
RLS enabled: Yes (same migration)

Checklist: All items passed
```

## Level History

- **Lv.1** — Base: 5 table classification patterns (user-scoped, org-scoped, public-read, junction, system), decision tree for pattern selection, 4 complete migration templates with RLS + all CRUD policies, pre-commit checklist (10 items), 3 audit queries (unprotected tables, missing policies, incomplete coverage), special case handling (system tables, soft-delete, row-level roles, ALTER TABLE). (Origin: MemStack Pro v3.2, Mar 2026)
