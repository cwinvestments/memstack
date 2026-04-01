---
name: memstack-development-code-reviewer
description: "Use this skill when the user says 'review code', 'code review', 'check my code', 'audit this', 'review PR', 'review changes', 'what\'s wrong with this', or is requesting a structured review of code quality, security, performance, or maintainability. Do NOT use for refactoring plans or test generation."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# 🔍 Code Reviewer — Reviewing code for issues and improvements...
*Systematic code review across security, performance, maintainability, error handling, testing, and accessibility — with severity-ranked findings and specific fixes.*

## Activation

When this skill activates, output:

`🔍 Code Reviewer — Scanning for issues...`

Then execute the protocol below.

| Context | Status |
|---------|--------|
| User says "review code" or "code review" or "check my code" | ACTIVE |
| User says "audit this" or "review PR" or "review changes" | ACTIVE |
| User asks "what's wrong with this" about code | ACTIVE |
| Reviewing a specific file or set of changes | ACTIVE |
| User is writing code and hasn't asked for review | DORMANT |
| Discussing code architecture at a high level | DORMANT |

### Anti-patterns

| Trap | Reality Check |
|------|---------------|
| "This looks fine to me" | Check every category systematically. Skimming misses auth gaps and N+1 queries. |
| "Style issues are important" | Linters handle style. Focus on logic, security, and correctness. |
| "I'll flag everything I see" | Noise kills reviews. Only report issues with real impact. Severity matters. |
| "The code works so it's fine" | Working does not mean correct. Race conditions, edge cases, and security holes all "work" until they don't. |
| "I'll suggest a complete rewrite" | Review what's there. Propose targeted fixes, not architectural overhauls. |

## Severity Levels

| Level | Label | Meaning | Action |
|-------|-------|---------|--------|
| 🔴 | **Critical** | Security vulnerability, data loss risk, crash in production | Fix before merge |
| 🟠 | **High** | Bug, incorrect behavior, significant performance issue | Fix this sprint |
| 🟡 | **Medium** | Code smell, minor performance issue, missing edge case | Fix when touching the file |
| 🔵 | **Low** | Style preference, minor improvement, documentation gap | Consider for future |

## Protocol

### Step 1: Security Review

Scan for security vulnerabilities — this category takes priority.

**Authentication gaps:**

Search for route handlers and verify each has auth checks:

```bash
grep -rn "export async function\|export function" --include="*.ts" app/api/ | head -20
```

Flag these patterns:
- Route handler without auth check (e.g., `getAuthContext`) at the top
- Org-scoped route without `verifyOrgAccess`
- Admin action without role verification
- Webhook endpoint without signature verification

**Exposed secrets:**

Search for hardcoded credentials:

```bash
grep -rn "sk_live\|sk_test\|password\s*=\s*['\"]" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.env" . | grep -v node_modules | grep -v .env.example
```

Flag these patterns:
- API keys or tokens hardcoded in source
- `.env` files committed to git
- Secrets in client-side code (`NEXT_PUBLIC_` prefix on secret values)
- Database connection strings in source files

**Injection vulnerabilities:**

Search for unsafe input handling:

```bash
grep -rn "\.raw(\|\.unsafeRaw\|innerHTML\s*=" --include="*.ts" --include="*.tsx" --include="*.js" . | grep -v node_modules
```

Flag these patterns:
- String concatenation in SQL queries (use parameterized queries)
- Unsafe HTML rendering with user-supplied content
- Unsanitized URL parameters used in redirects (open redirect)
- User input reflected in HTML without escaping (XSS)

### Step 2: Performance Review

Identify patterns that degrade under load.

**N+1 queries:**

```bash
# Find loops that might contain database calls
grep -rn "\.forEach\|\.map\|for.*of\|for.*in" --include="*.ts" --include="*.tsx" . | grep -v node_modules | head -20
```

Flag these patterns:
- Database query inside a loop (fetch all in one query, then map)
- `await` inside `.map()` without `Promise.all()` (sequential when it could be parallel)
- Sequential `await` calls that could be `Promise.all([...])` (parallelizable)

**Missing indexes:**
- Foreign key columns without an index (causes slow JOINs)
- Columns used in `WHERE` or `ORDER BY` without indexes
- Composite queries that need composite indexes

**Frontend performance:**

```bash
# Check for large imports that should be tree-shaken
grep -rn "import .* from ['\"]lodash['\"]" --include="*.ts" --include="*.tsx" . | grep -v node_modules
```

Flag these patterns:
- Full library imports instead of tree-shakeable imports (`import _ from 'lodash'`)
- Large dependencies in client bundles (check with `next build --analyze`)
- Missing `React.memo`, `useMemo`, or `useCallback` on expensive renders
- Images without width/height or `next/image` optimization
- Unthrottled event handlers (scroll, resize, input without debounce)

**Data fetching:**
- Fetching more data than needed (SELECT * instead of specific columns)
- Missing pagination on list endpoints
- No caching on expensive, infrequently-changing queries
- Client-side fetching for data that could be server-rendered

### Step 3: Maintainability Review

Evaluate code clarity and organization.

**Dead code:**

```bash
grep -rn "export " --include="*.ts" --include="*.tsx" . | grep -v node_modules | head -30
```

Flag these patterns:
- Functions/components that are never imported
- Commented-out code blocks (delete it — git has history)
- Unused variables, imports, or parameters
- Feature flags for features that shipped months ago

**Duplicated logic:**
- Same validation logic in multiple route handlers (extract to shared schema)
- Repeated auth patterns (extract to middleware or helper)
- Copy-pasted components with minor differences (extract shared component)
- Same error handling try/catch in every handler (extract to wrapper)

**Naming clarity:**
- Single-letter variables outside of loops (`d`, `x`, `t` — what are these?)
- Boolean variables without `is`/`has`/`should` prefix (`active` vs `isActive`)
- Functions that don't describe their action (`process()`, `handle()`, `doStuff()`)
- Inconsistent naming between related files (camelCase in one, snake_case in another)

**Type safety:**
- `any` type used where a specific type is known
- Type assertions (`as Type`) hiding real type errors
- Missing return types on exported functions
- `@ts-ignore` or `@ts-expect-error` without explanation

### Step 4: Error Handling Review

Check that errors are caught and handled appropriately.

**Uncaught promises:**

```bash
grep -rn "await " --include="*.ts" --include="*.tsx" . | grep -v "try\|catch\|\.catch" | grep -v node_modules | head -20
```

Flag these patterns:
- `await` calls without `try/catch` in route handlers (returns 500 with no context)
- `.then()` chains without `.catch()` (unhandled rejection)
- Event handlers with `async` but no error boundary
- Fire-and-forget promises (no `await`, no `.catch()`, no `void`)

**Error quality:**
- Generic `catch (e) { throw e }` (adds nothing — let it propagate or add context)
- Swallowed errors: `catch (e) {}` (at minimum, log them)
- Stack traces or internal details exposed to users in API responses
- Missing error boundaries in React component trees

**Edge cases:**
- No handling for empty arrays/null results from database queries
- No handling for network timeouts or external API failures
- No handling for concurrent modification (optimistic locking)
- No handling for file not found, permission denied, or disk full

### Step 5: Testing Review

Assess test coverage for critical paths.

**Untested critical paths:**
- Auth flows (login, logout, token refresh) without tests
- Payment/billing logic without tests
- Data mutation endpoints (POST, PATCH, DELETE) without tests
- RLS policies without tests (test that users CAN'T access other orgs' data)

**Missing edge cases:**
- Only happy path tested (what about invalid input? empty data? max limits?)
- No tests for error responses (401, 403, 404, 422)
- No tests for boundary conditions (0 items, 1 item, max items)
- No tests for concurrent operations (race conditions)

**Test quality:**
- Tests that test implementation details instead of behavior
- Tests with no assertions (they "pass" but verify nothing)
- Flaky tests that depend on timing, external services, or test order
- Test data that doesn't represent realistic scenarios

### Step 6: Accessibility Review

Check that UI code is usable by everyone.

**Image and media:**
- `<img>` without `alt` attribute (screen readers announce nothing)
- Decorative images without `alt=""` (screen readers read the filename)
- Video/audio without captions or transcripts
- Icon buttons without accessible labels

**Keyboard navigation:**
- Click handlers on non-interactive elements instead of `<button>` (not keyboard accessible)
- Custom dropdowns/modals without focus trapping
- No visible focus indicator on interactive elements
- Tab order that doesn't match visual layout

**ARIA and semantics:**
- Missing `aria-label` on icon-only buttons
- Using generic elements for navigation instead of `<nav>`
- Form inputs without associated `<label>` elements
- Missing `role` attributes on custom interactive components
- Live regions (toast notifications) without `aria-live`

**Color and contrast:**
- Information conveyed by color alone (add icons or text)
- Low contrast text (below 4.5:1 ratio for normal text, below 3:1 for large text)
- Focus indicators that rely on color change alone

### Step 7: Output Per-File Report

For each file reviewed, output findings grouped by file:

```
file: app/api/organizations/[orgId]/route.ts

🔴 Critical: No auth check on DELETE handler
   Line 45: export async function DELETE(req) { ... }
   Fix: Add getAuthContext + verifyOrgAccess + admin role check
   ```typescript
   const auth = await getAuthContext(req);
   if (!auth) return apiError('Authentication required', 401);
   const access = await verifyOrgAccess(auth.userId, params.orgId);
   if (!access || access.role !== 'owner') return apiError('Access denied', 403);
   ```

🟠 High: N+1 query in project listing
   Line 62: projects.map(async (p) => await getProjectMembers(p.id))
   Fix: Batch fetch members for all projects in one query
   ```typescript
   const membersByProject = await db.members.findByProjectIds(
     projects.map(p => p.id)
   );
   ```

🟡 Medium: Generic error message
   Line 78: catch (e) { return apiError('Something went wrong', 500); }
   Fix: Log the error with context, return safe message
   ```typescript
   catch (error) {
     console.error('DELETE /organizations failed:', { orgId: params.orgId, error });
     return apiError('Failed to delete organization', 500);
   }
   ```

🔵 Low: Missing return type on handler
   Line 45: export async function DELETE(req)
   Fix: Add explicit return type
   ```typescript
   export async function DELETE(req: NextRequest): Promise<NextResponse>
   ```
```

### Step 8: Summary Report

After reviewing all files, output a summary:

```
🔍 Code Review — Complete

Files reviewed: [count]
Issues found: [total]

By severity:
  🔴 Critical: [count] — fix before merge
  🟠 High:     [count] — fix this sprint
  🟡 Medium:   [count] — fix when touching the file
  🔵 Low:      [count] — consider for future

By category:
  Security:        [count] issues
  Performance:     [count] issues
  Maintainability: [count] issues
  Error handling:  [count] issues
  Testing:         [count] issues
  Accessibility:   [count] issues

Top 3 priorities:
  1. [Most critical issue with file:line]
  2. [Second most critical]
  3. [Third most critical]

Estimated fix effort:
  Critical + High: ~[X] hours
  All issues: ~[X] hours
```

## Level History

- **Lv.1** — Base: Six-category systematic review (security, performance, maintainability, error handling, testing, accessibility), severity-ranked findings, per-file reports with specific code fixes, summary with prioritized action items. (Origin: MemStack Pro v3.2, Mar 2026)
