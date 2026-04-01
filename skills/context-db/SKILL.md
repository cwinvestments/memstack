---
name: memstack-context-db
description: "Use when the user says 'context-db', 'fact store', 'project facts', 'token savings', or when CC needs to query structured project knowledge instead of reading full CLAUDE.md. Creates a SQLite-backed facts database per project at .claude/context.db. Do NOT use for session logging (Diary) or memory recall (Echo)."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# 🗄️ Context DB — Querying project facts...
*A SQLite-backed facts database for each project. Stores structured project knowledge that CC can query instead of reading full CLAUDE.md every session — reducing token usage by returning only relevant facts.*

## Activation

When this skill activates, output:

`🗄️ Context DB — Querying project facts...`

Then execute the protocol below.

## Context Guard

| Context | Status |
|---------|--------|
| **User says "context-db", "fact store", "project facts"** | ACTIVE — full protocol |
| **User asks about token savings or context efficiency** | ACTIVE — show stats |
| **CC needs project knowledge for current task** | ACTIVE — query relevant facts |
| **User wants to add a fact or decision** | ACTIVE — add to DB |
| **Files exist in `inbox/` directory** | ACTIVE — auto-ingest |
| **User is logging a session (Diary territory)** | DORMANT — do not activate |
| **User is recalling past sessions (Echo territory)** | DORMANT — do not activate |

## Anti-Rationalization

| Thought | Correction |
|---------|------------|
| "I'll just read the whole CLAUDE.md, it's easier" | That wastes tokens. Query only what you need. |
| "The DB doesn't exist yet, skip it" | Create it on first use — that's the protocol. |
| "This fact isn't important enough to store" | If you learned it during a session, it's worth storing. |
| "I can remember this without a DB" | You start each session with a blank slate. Store it. |

## Database Schema

The SQLite database lives at `.claude/context.db` in the project root. Create it on first use:

```sql
CREATE TABLE IF NOT EXISTS facts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT NOT NULL,
    value TEXT NOT NULL,
    category TEXT NOT NULL CHECK(category IN (
        'decisions', 'patterns', 'components', 'config', 'gotchas'
    )),
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    source TEXT,
    UNIQUE(key, category)
);

CREATE INDEX IF NOT EXISTS idx_facts_category ON facts(category);
CREATE INDEX IF NOT EXISTS idx_facts_key ON facts(key);
```

### Categories

| Category | What to store | Example |
|----------|--------------|---------|
| **decisions** | Architectural choices and their rationale | "auth-method" → "JWT with httpOnly cookies — chose over session tokens for stateless scaling" |
| **patterns** | Code patterns and conventions used in the project | "api-error-handling" → "All API routes return {error, data} shape, never throw" |
| **components** | Key components, their purpose, and location | "auth-middleware" → "src/middleware/auth.ts — validates JWT, attaches user to req" |
| **config** | Configuration values and environment setup | "database-url-format" → "postgres://[user]:[pass]@[host]:5432/[db]?sslmode=require" |
| **gotchas** | Non-obvious pitfalls and workarounds | "prisma-json-fields" → "Must use Prisma.JsonValue type, not plain object — causes runtime errors" |

## Protocol

### Step 1: Initialize (first use only)

Check if `.claude/context.db` exists. If not, create it:

```bash
sqlite3 .claude/context.db <<'SQL'
CREATE TABLE IF NOT EXISTS facts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT NOT NULL,
    value TEXT NOT NULL,
    category TEXT NOT NULL CHECK(category IN (
        'decisions', 'patterns', 'components', 'config', 'gotchas'
    )),
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    source TEXT,
    UNIQUE(key, category)
);
CREATE INDEX IF NOT EXISTS idx_facts_category ON facts(category);
CREATE INDEX IF NOT EXISTS idx_facts_key ON facts(key);
SQL
```

### Step 2: Inbox Watcher

Check for files in the project's `inbox/` directory. If any exist, auto-ingest them:

```bash
ls inbox/*.md inbox/*.txt inbox/*.json 2>/dev/null
```

For each file found:
1. Parse the content for key/value facts (use headings as keys, content as values)
2. Insert each fact into the DB with an appropriate category
3. Move the ingested file to `inbox/processed/` with a timestamp
4. Report what was ingested

```bash
mkdir -p inbox/processed
# After ingestion:
mv inbox/filename.md inbox/processed/$(date +%Y%m%d-%H%M%S)-filename.md
```

### Step 3: Query Facts

Query only the facts relevant to the current task. Use category and key pattern matching:

```bash
# Query by category
sqlite3 -header -column .claude/context.db \
  "SELECT key, value FROM facts WHERE category = '<category>';"

# Query by keyword (searches both key and value)
sqlite3 -header -column .claude/context.db \
  "SELECT key, value, category FROM facts WHERE key LIKE '%<keyword>%' OR value LIKE '%<keyword>%';"

# Get all facts (use sparingly)
sqlite3 -header -column .claude/context.db \
  "SELECT category, key, value FROM facts ORDER BY category, key;"
```

### Step 4: Add/Update Facts

When you learn something new about the project during a session:

```bash
# Add a new fact (INSERT OR REPLACE handles upserts via UNIQUE constraint)
sqlite3 .claude/context.db \
  "INSERT OR REPLACE INTO facts (key, value, category, updated_at, source) VALUES (
    '<key>',
    '<value>',
    '<category>',
    datetime('now'),
    '<source>'
  );"
```

**Source** should indicate where the fact came from: `session`, `claude.md`, `inbox`, `code-review`, etc.

### Step 5: Estimate Token Savings

After each query, estimate and log the token savings:

1. Get the size of the project's CLAUDE.md (or equivalent context file):
   ```bash
   wc -c CLAUDE.md 2>/dev/null || wc -c .claude/rules/*.md 2>/dev/null
   ```

2. Calculate bytes returned by the query (the actual facts retrieved)

3. Log the savings to `.claude/context-db-stats.json`:
   ```bash
   # Read or initialize stats file
   cat .claude/context-db-stats.json 2>/dev/null || echo '{"queries":0,"total_context_bytes":0,"total_returned_bytes":0}'
   ```

   Update the stats:
   ```json
   {
     "queries": <incremented>,
     "total_context_bytes": <cumulative full-context size>,
     "total_returned_bytes": <cumulative bytes actually returned>,
     "estimated_tokens_saved": <(total_context - total_returned) / 4>,
     "last_query": "<timestamp>",
     "savings_percentage": "<calculated>%"
   }
   ```

### Step 6: Report

After any query or add operation, report:

```
🗄️ Context DB — [operation]

Facts: [count] total ([by category breakdown])
Query: "[keywords]" → [N] facts returned ([bytes] bytes)
Token savings: ~[N] tokens saved this session ([percentage]% reduction)
```

## Seeding from CLAUDE.md

On first initialization, offer to seed the DB from existing CLAUDE.md:

1. Parse CLAUDE.md for structured facts (headings → keys, content → values)
2. Categorize each fact using the 5 categories
3. Insert all facts with `source: 'claude.md'`
4. Report: "Seeded [N] facts from CLAUDE.md — future queries will use the DB instead"

## Cleanup

Remove stale facts periodically:

```bash
# Find facts not updated in 90 days
sqlite3 -header -column .claude/context.db \
  "SELECT key, category, updated_at FROM facts WHERE updated_at < datetime('now', '-90 days');"
```

## Attribution

Inspired by Google ADK Always-On Memory Agent — github.com/GoogleCloudPlatform/generative-ai/tree/main/gemini/agents/always-on-memory-agent

## Level History

- **Lv.1** — Base: SQLite-backed facts database with 5 categories (decisions, patterns, components, config, gotchas), keyword querying, token savings estimation, inbox auto-ingestion, CLAUDE.md seeding. (Origin: MemStack Pro v3.3, Mar 2026)
