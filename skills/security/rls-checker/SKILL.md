---
name: memstack-security-rls-checker
description: "Use this skill when the user says 'check RLS', 'audit RLS', 'RLS policies', 'row level security', 'Supabase security audit', or needs to verify table-level access control. Audits Supabase Row Level Security policies across all tables. Do NOT use for non-Supabase projects or writing RLS policies from scratch."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---


# 🔒 RLS Checker — Auditing Row Level Security...
*Audit Supabase Row Level Security policies across all tables in a project.*

## Activation

When this skill activates, output:

`🔒 RLS Checker — Auditing Row Level Security...`

Then execute the protocol below.

## Context Guard

| Context | Status |
|---------|--------|
| **User asks to check/audit RLS** | ACTIVE — full audit |
| **User mentions Supabase security** | ACTIVE — full audit |
| **User asks about table permissions** | ACTIVE — full audit |
| **User is writing RLS policies** | DORMANT — they know what they're doing |
| **Non-Supabase project** | DORMANT — not applicable |

## Protocol

### Step 1: Discover Tables

Find all Supabase tables referenced in the project. Search in priority order:

1. **Migration files** — most authoritative source:
   ```bash
   find . -path "*/migrations/*.sql" -o -path "*/supabase/migrations/*.sql" | head -50
   ```
   Look for `CREATE TABLE` statements.

2. **Generated types** — comprehensive if available:
   ```
   types/database.ts, types/supabase.ts, src/types/database.types.ts, database.types.ts
   ```
   Parse the `Tables` interface for all table names.

3. **Client usage** — catches tables missed by above:
   ```
   grep -r "\.from(['\"]" --include="*.ts" --include="*.tsx" --include="*.js"
   ```
   Extract table names from `.from('table_name')` calls.

4. **Storage buckets** — separate RLS surface:
   ```
   grep -r "storage\.from\|createBucket\|storage-api" --include="*.ts" --include="*.tsx" --include="*.sql"
   ```

Compile a deduplicated list of all tables and storage buckets.

### Step 2: Extract RLS Policies

For each table, find its RLS configuration:

1. **Search migration SQL for RLS statements:**
   - `ALTER TABLE <name> ENABLE ROW LEVEL SECURITY` — RLS is on
   - `CREATE POLICY` statements — extract policy name, operation (SELECT/INSERT/UPDATE/DELETE/ALL), and USING/WITH CHECK expressions
   - `ALTER TABLE <name> FORCE ROW LEVEL SECURITY` — RLS enforced even for table owners

2. **Check for intentionally unprotected tables:**
   - Tables with `GRANT SELECT ON <table> TO anon` without RLS are intentionally public
   - Look for comments like `-- public table`, `-- no RLS needed`, or `-- rls:skip` in migration SQL
   - Tables marked with `-- rls:skip` should be classified as ✅ OK (Intentional) in the report, not flagged as missing RLS. This lets teams explicitly document tables that rely on application-level authorization (e.g., service-role-first architectures).
   - If no `-- rls:skip` marker exists and no RLS is enabled, flag normally.

3. **Check Supabase dashboard-configured policies:**
   - Policies created via the Supabase Dashboard do NOT appear in migration SQL files. They exist only in the live database.
   - If a table has no RLS in migration files but is referenced in application code, note in the report: "⚠️ Policy may exist in Supabase Dashboard — verify via `supabase inspect db policies` or the Dashboard UI."
   - Search for Supabase CLI config files (`supabase/config.toml`, `.supabase/`) that might indicate whether the project uses Dashboard-managed policies.
   - Recommend teams capture all Dashboard-created policies in migration files for auditability:
     ```bash
     supabase db dump --schema public --data-only=false | grep -A5 "CREATE POLICY"
     ```

4. **Check Supabase dashboard seed/init files** for policy definitions that may not be in migrations.

### Step 3: Analyze Policies

For each table with RLS enabled, evaluate policy quality:

**Check 1 — Operation Coverage:**
Flag tables missing policies for any CRUD operation:
- Has SELECT but no INSERT → partial coverage (WARNING)
- Has SELECT but no UPDATE/DELETE → partial coverage (WARNING)
- Has no policies at all despite RLS enabled → locked out (CRITICAL)

**Check 2 — User Isolation:**
Verify policies filter by authenticated user:
- `auth.uid()` in USING clause — standard user isolation (OK)
- `auth.uid()` in WITH CHECK clause — write isolation (OK)
- No `auth.uid()` reference — overly permissive (WARNING)
- Hardcoded UUIDs instead of `auth.uid()` — security risk (CRITICAL)
- `current_setting('app.*')` instead of `auth.uid()` — anti-pattern (WARNING). This relies on the application explicitly setting a PostgreSQL session variable before every query. If the variable is unset, the policy may fail open or closed unpredictably. Prefer `auth.uid()` which Supabase populates automatically from the JWT. Flag with:
  ```
  grep -rn "current_setting" --include="*.sql"
  ```

**Check 3 — Multi-Tenant Isolation:**
For tables with `organization_id` or `team_id` columns:
- Policy should JOIN against a membership table to verify org access
- Direct `organization_id = <value>` without membership check is insufficient (WARNING)
- Example of correct pattern:
  ```sql
  CREATE POLICY "org_isolation" ON documents
    USING (organization_id IN (
      SELECT org_id FROM organization_members
      WHERE user_id = auth.uid()
    ));
  ```

**Check 4 — Service Role Bypass:**
Search codebase for service role usage that bypasses RLS:
```
grep -r "service_role\|serviceRole\|supabaseAdmin\|SUPABASE_SERVICE_ROLE" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.env*"
```
- Server-side API routes using service role — acceptable if intentional (INFO)
- Client-side code with service role key — critical vulnerability (CRITICAL)
- Service role in `.env` committed to git — critical vulnerability (CRITICAL)

**Check 5 — Storage Bucket Policies:**
For each storage bucket found:
- Check for bucket-level RLS policies in migrations
- Verify upload policies restrict by user path (e.g., `auth.uid()::text = (storage.foldername(name))[1]`)
- Flag buckets with no policies (WARNING)

### Step 3b: Defense-in-Depth Score (Service-Role Architectures)

If the project uses service role for most/all database access (Check 4 found widespread `supabaseAdmin` / `SUPABASE_SERVICE_ROLE` usage), compute a defense-in-depth score:

**Score calculation:**
- Count total tables with sensitive data (contains passwords, tokens, PII, financial data, or credentials)
- Count how many of those tables have RLS enabled
- Score = `(tables with RLS / total sensitive tables) × 100`

**Classification:**
| Score | Rating | Meaning |
|-------|--------|---------|
| 80–100% | 🟢 Strong | RLS provides meaningful backup even though service role bypasses it |
| 50–79% | 🟡 Partial | Some defense-in-depth but gaps remain |
| 20–49% | 🟠 Weak | Most sensitive tables unprotected at DB layer |
| 0–19% | 🔴 None | Entire security model depends on application code — single bug = full breach |

**Include in report:**
```
## Defense-in-Depth Score
Architecture: Service-role-first (all API routes use service role key)
Sensitive tables: <count>
Sensitive tables with RLS: <count>
Score: <percentage> — <rating>

Note: Service role bypasses RLS by design. This score measures how well
the database would protect data if an application-level auth bug occurred.
```

**Recommendation for low scores:** Even in service-role architectures, enabling RLS on sensitive tables provides a safety net. If a developer accidentally uses the anon key, creates a new route without auth, or a future refactor introduces a bug, RLS prevents cross-tenant data access at the database layer.

### Step 4: Generate Report

Output a structured report with this format:

```
🔒 RLS Audit Report
Project: <project-name>
Tables found: <count>
Storage buckets: <count>

## Table Audit

| Table | RLS | Policies | Coverage | Risk | Issue |
|-------|-----|----------|----------|------|-------|
| users | ON | 4 | Full | ✅ OK | — |
| documents | ON | 2 | Partial | ⚠️ WARN | Missing DELETE policy |
| payments | OFF | 0 | None | 🔴 CRIT | No RLS enabled |
| public_posts | OFF | 0 | N/A | ✅ OK | Intentionally public (-- rls:skip) |

## Storage Buckets

| Bucket | Policies | Risk | Issue |
|--------|----------|------|-------|
| avatars | 2 | ✅ OK | — |
| uploads | 0 | ⚠️ WARN | No upload restriction |

## Critical Issues
1. **payments** — No RLS enabled. Any authenticated user can read/write all rows.
   → Fix: `ALTER TABLE payments ENABLE ROW LEVEL SECURITY;` then add user-scoped policies.

2. **service_role in client** — Found in `src/lib/supabase.ts:14`.
   → Fix: Remove service role key from client code. Use server-side API route instead.

## Warnings
1. **documents** — Missing DELETE policy. Users may not be able to delete their own documents, or deletion may be unrestricted.
   → Fix: Add `CREATE POLICY "delete_own" ON documents FOR DELETE USING (user_id = auth.uid());`

2. **uploads bucket** — No storage policies defined.
   → Fix: Add bucket policies restricting uploads to user-specific paths.

## Summary
- 🔴 Critical: <count>
- ⚠️ Warning: <count>
- ✅ OK: <count>
- Total tables: <count>
```

### Step 5: Suggest Fixes

For each CRITICAL and WARNING issue, provide:
1. The exact SQL migration to fix it
2. Where to add it (new migration file name following project conventions)
3. Any application code changes needed (e.g., removing service role from client)

Offer to generate a migration file with all fixes: `supabase/migrations/<timestamp>_rls_fixes.sql`

## Risk Levels

| Level | Meaning | Action |
|-------|---------|--------|
| 🔴 CRITICAL | Data exposed or writable by unauthorized users | Fix immediately |
| ⚠️ WARNING | Incomplete coverage or weak isolation | Fix before production |
| ℹ️ INFO | Acceptable pattern that should be verified | Review and confirm intentional |
| ✅ OK | Properly secured | No action needed |

## Common Patterns Reference

**User-owned rows:**
```sql
CREATE POLICY "users_own_data" ON table_name
  FOR ALL USING (user_id = auth.uid())
  WITH CHECK (user_id = auth.uid());
```

**Org-scoped with membership check:**
```sql
CREATE POLICY "org_members_access" ON table_name
  FOR ALL USING (
    organization_id IN (
      SELECT org_id FROM organization_members
      WHERE user_id = auth.uid()
    )
  );
```

**Public read, authenticated write:**
```sql
CREATE POLICY "public_read" ON table_name FOR SELECT USING (true);
CREATE POLICY "auth_insert" ON table_name FOR INSERT WITH CHECK (auth.role() = 'authenticated');
```

**Storage bucket user isolation:**
```sql
CREATE POLICY "user_uploads" ON storage.objects
  FOR INSERT WITH CHECK (
    bucket_id = 'uploads' AND
    auth.uid()::text = (storage.foldername(name))[1]
  );
```

## Level History

- **Lv.1** — Base: Table discovery (migrations, types, client usage), RLS policy extraction, 5-point analysis (coverage, user isolation, multi-tenant, service role, storage), structured report with risk levels, fix generation. Patterns derived from AdminStack, EpsteinScan, and 10+ production Supabase projects. (Origin: MemStack Pro v1.0, Mar 2026)
- **Lv.2** — Audit feedback: Added `current_setting()` anti-pattern detection (vs `auth.uid()`), `-- rls:skip` marker for intentionally unprotected tables, Supabase Dashboard policy detection guidance (`supabase inspect db policies`), defense-in-depth score for service-role-first architectures. (Origin: AdminStack audit, Mar 2026)
