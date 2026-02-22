# MemStack Changelog

## v3.0.0-alpha — 2026-02-22 — Native CC Hook Architecture

**Inspired by:** CC Best Practices research (see `research/cc-best-practice-comparison.md`)

### Breaking Change: Prompt-Based Skills → Deterministic Hooks

Three passive skills that relied on the LLM remembering to follow protocols are now
deterministic shell scripts that fire automatically on CC lifecycle events.

| Skill | Replaced By | CC Event | Behavior |
|-------|-------------|----------|----------|
| **Seal** (commit safety) | `.claude/hooks/pre-push.sh` | `PreToolUse` on `git push` | Build check, secrets scan, commit format — **blocks push on failure** (exit 2) |
| **Deploy** (push safety) | `.claude/hooks/post-commit.sh` | `PostToolUse` on `git commit` | Debug artifact scan, secrets check — **warns after commit** |
| **Monitor** (session reporting) | `.claude/hooks/session-start.sh` + `session-end.sh` | `SessionStart` + `Stop` | Reports status to monitoring API |

**Why:** Hooks are deterministic — they always fire. Prompt-based skills only work if the LLM
remembers to follow the protocol. For safety-critical operations (blocking a push with secrets,
verifying builds), deterministic execution is essential.

### New: CC Native Infrastructure

- **`.claude/settings.json`** — Hook configuration wiring events to scripts
- **`.claude/hooks/`** — 4 shell scripts replacing 3 prompt-based skills
- **`.claude/rules/memstack.md`** — Global rules as native CC rules (replaces MEMSTACK.md Global Rules section)

### Deprecated Skills

Original skill files are preserved with `deprecated: true` in YAML frontmatter.
They serve as fallback documentation for CC versions without hook support.

- `skills/seal.md` — Deprecated, replaced by `pre-push.sh`
- `skills/deploy.md` — Deprecated, replaced by `post-commit.sh`
- `skills/monitor.md` — Deprecated, replaced by `session-start.sh` + `session-end.sh`

### Updated

- `MEMSTACK.md` — v3.0: Documents two-layer architecture (hooks + skills), updated skill index
- `config.json` — Version bump to 3.0.0-alpha

### Architecture: Two Layers

```
MemStack v3.0
├── Hooks (deterministic)     — Shell scripts, CC lifecycle events
│   ├── pre-push.sh           — Seal: build check, secrets scan, blocks bad pushes
│   ├── post-commit.sh        — Deploy: debug artifacts, format validation
│   ├── session-start.sh      — Monitor: report "working" to API
│   └── session-end.sh        — Monitor: report "completed" to API
├── Skills (context-aware)    — Markdown protocols, keyword/contextual triggers
│   ├── Echo, Diary, Work     — SQLite-backed memory (Lv.3)
│   ├── Project, Grimoire     — Session lifecycle (Lv.2-3)
│   ├── Scan, Quill           — Business tools (Lv.2)
│   └── Forge, Shard, Sight   — Dev tools (Lv.2)
└── Rules (.claude/rules/)    — Always-loaded behavioral constraints
```

### Files Added
- `.claude/settings.json` — Hook wiring configuration
- `.claude/hooks/pre-push.sh` — Seal hook (build + secrets + format)
- `.claude/hooks/post-commit.sh` — Deploy hook (debug artifacts + secrets)
- `.claude/hooks/session-start.sh` — Monitor hook (session start)
- `.claude/hooks/session-end.sh` — Monitor hook (session end)
- `.claude/rules/memstack.md` — Global rules as CC native rules
- `research/cc-best-practice-comparison.md` — CC capabilities comparison report

### Files Modified
- `MEMSTACK.md` — v3.0: Two-layer architecture, updated skill index
- `skills/seal.md` — Deprecated, added hook reference
- `skills/deploy.md` — Deprecated, added hook reference
- `skills/monitor.md` — Deprecated, added hook reference

---

## v2.1.0 — 2026-02-20 — SQLite Memory Backend

**Inspired by:** Accomplish AI research (see `research/accomplish-comparison.md`)

### New: SQLite Memory Backend
- **`db/memstack.db`** — SQLite database with WAL mode replaces flat markdown files as source of truth
- **`db/schema.sql`** — Schema with 4 tables: `sessions`, `insights`, `project_context`, `plans`
- **`db/memstack-db.py`** — Repository pattern CLI helper with 13 commands:
  `init`, `add-session`, `add-insight`, `search`, `get-sessions`, `get-insights`,
  `get-context`, `set-context`, `add-plan-task`, `get-plan`, `update-task`, `export-md`, `stats`
- **`db/migrate.py`** — One-time migration script (idempotent, safe to re-run)
  - Imported 2 existing session diaries
  - Auto-extracted 17 insights from session decisions
  - Seeded 6 project contexts from config.json

### New: Auto-Extracted Insights
- Diary skill now automatically extracts decisions from session logs and stores them as
  searchable insights in the `insights` table
- Echo skill can search insights independently from full session logs
- Cross-project insight search enables pattern discovery across all projects

### Improved: Context Guards
- Added **Priority levels** (P1/P2) to all context guards for deterministic activation
- Added **explicit negative patterns** to prevent false activations:
  - Echo: won't fire on "memory" as a code concept, won't fire on "save" (Diary's territory)
  - Diary: won't fire on "recall" (Echo's territory), won't fire at session start
  - Seal: won't fire on "push" (Deploy's territory), won't fire during active coding
  - Deploy: won't fire on "build" for local testing, won't fire on SSH deploys

### New: Skill Deconfliction Rules
- Added **Skill Deconfliction** section to MEMSTACK.md
- Clear ownership: "commit" → Seal, "push/deploy" → Deploy, "recall" → Echo, etc.
- Deploy invokes Seal as a sub-step when needed (no more double activation)

### Updated Skills (Lv.2 → Lv.3)
- **Echo** — SQLite search as primary source, markdown as fallback, insight search
- **Diary** — Writes to SQLite + extracts insights + markdown backup
- **Work** — SQLite-backed plans with per-task status, no size limits
- **Project** — SQLite project context for save/restore, combined DB+session+plan restore

### Architecture Decision
Markdown files are preserved as human-readable exports and fallback, but SQLite is the
source of truth. This matches Accomplish AI's repository pattern while keeping MemStack's
simplicity — no Node.js runtime, no build step, just Python's built-in sqlite3 module.

### Files Added
- `db/schema.sql` — Database schema
- `db/memstack-db.py` — CLI helper (repository pattern)
- `db/migrate.py` — Markdown → SQLite migration
- `db/memstack.db` — The database itself
- `CHANGELOG.md` — This file

### Files Modified
- `MEMSTACK.md` — v2.1, added Storage section, Deconfliction section, leveling update
- `config.json` — Version bump to 2.1.0
- `skills/echo.md` — Lv.3: SQLite backend, improved context guards
- `skills/diary.md` — Lv.3: SQLite backend, insight extraction, improved guards
- `skills/work.md` — Lv.3: SQLite plans, structured task tracking
- `skills/project.md` — Lv.3: SQLite project context, combined restore
- `skills/seal.md` — Improved context guards, deconfliction with Deploy
- `skills/deploy.md` — Improved context guards, deconfliction with Seal

---

## v2.0.0 — 2026-02-19 — MemoryCore Merge

- Merged Developer Kaki's MemoryCore architecture into MemStack
- Added YAML frontmatter to all skills
- Added Context Guards to prevent false activations
- Added activation messages for skill transparency
- 14 skills at Lv.2
