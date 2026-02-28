# MemStack Changelog

## v3.2.1 — 2026-02-28 — Portability, KDP Spine Margins, Link Command

**Builds on:** v3.2.0 description audit and governance

### New: Link-Project Command

- `start-memstack.bat link <path>` creates a `.claude` junction from any project to MemStack
- Junction setup instructions added to README

### New: KDP Spine Text Margin Rules

- Added `### KDP Spine Text Margins` section to KDP Format skill
- Minimum 0.0625" (1/16") padding per side, 19px at 300 DPI
- Spine width formula: pages × 0.002252" (white paper)
- Font sizing constraint: `max_height = spine_width_px - 38`
- Updated in both `.claude/rules/kdp-format.md` and `skills/kdp-format/SKILL.md`

### Changed: Portable Launchers

- `start-memstack.bat` — replaced hardcoded `C:\Projects` with `%~dp0` dynamic detection
- `start-memstack.sh` — replaced hardcoded `$HOME/Projects` with `$(dirname "$0")` detection
- Both launchers now work from any clone location

### Changed: KDP Format Skill Made Public

- `kdp-format.md` added to `.claude/rules/` for always-on loading

### Bug Fixes & Maintenance

- Fixed step numbering in `start-memstack.sh`
- Fixed Echo search score normalization and vector dimension mismatch
- Fixed JSON injection and unbound variable risks in session hooks
- Fixed quoting and dual-format commit check in `post-commit.sh`
- Fixed dead `.env` leak check in `pre-push.sh`
- Added WAL and foreign_keys PRAGMAs to `migrate.py`
- Removed pandas dependency from Echo dedup logic
- Added input validation and malformed JSON handling in `memstack-db.py`
- Fixed `export-md` to include `architecture_decisions` and `current_branch`
- Added standard ignores to `.gitignore`
- Used `printf` instead of `echo -e` in `post-commit.sh` for portability
- Cleaned dead config keys, added Headroom startup flags
- Normalized path separators in `echo.md`
- Added completion notification beep (WAV playback, always-on rule)
- Compress skill: added `[code]` extra, updated startup command, added troubleshooting
- Corrected State skill auto-read claim, Forge example row count, diary.md Project reference

### Files Added
- `.claude/rules/kdp-format.md` — KDP Format as public rule

### Files Modified
- `start-memstack.bat` — Portable paths + link command
- `start-memstack.sh` — Portable paths + step numbering fix
- `skills/kdp-format/SKILL.md` — Spine text margin rules, Lv.2 history updated
- `README.md` — Junction setup, launcher docs, quick start update
- Multiple hook/rule/skill files — Bug fixes listed above

---

## v3.2.0 — 2026-02-24 — Description Audit, Anti-Rationalization, Portfolio Governance

**Builds on:** v3.1 skill additions and research analysis

### New: Governor Skill (#19)

- 3-tier portfolio governance: Prototype / MVP / Production
- Phase constraints per tier — prevents over-engineering
- Anti-patterns list per tier (19 items total)
- Triggers on "new project", "what tier", "scope", "project init"

### New: Anti-Rationalization Tables

- Added to Echo, Diary, and Verify SKILL.md files
- Two-column tables mapping known Claude excuses to rebuttals
- Pattern adopted from Superpowers plugin research

### Changed: Description Trap Audit

- All 17 active SKILL.md `description:` fields rewritten
- Descriptions now say WHEN to invoke, never HOW the skill works
- Prevents Claude from shortcutting full protocols by reading the summary

### Changed: Silent Context Compilation (Work Lv.5)

- Added Step 0 to Work skill protocol
- Silently reads STATE.md, CLAUDE.md, recent diary, and git state before any plan operation
- No output — internalizes context without wasting user's time

### Files Added
- `skills/governor/SKILL.md` — Governor skill
- `docs/plans/2026-02-24-v3.2-governance-design.md` — Design doc

### Files Modified
- All 16 existing `skills/*/SKILL.md` — Description field rewritten
- `skills/echo/SKILL.md` — Anti-rationalization table added
- `skills/diary/SKILL.md` — Anti-rationalization table added
- `skills/verify/SKILL.md` — Anti-rationalization table added
- `skills/work/SKILL.md` — Step 0 + Lv.5 level history
- `MEMSTACK.md` — v3.2, Governor in index, Work Lv.5
- `README.md` — v3.2 notes, Governor in skills table

---

## v3.1.0 — 2026-02-24 — Humanize, State, Verify + Diary/Echo Upgrades

**Builds on:** v3.0-rc hooks and rules architecture

### New Skills

- **Humanize** (#16, Lv.1) — Remove AI writing patterns from text. Curated replacement table + voice guidelines
- **State** (#17, Lv.1) — Living STATE.md tracking current task, blockers, next steps. Auto-reads at session start
- **Verify** (#18, Lv.1) — Pre-commit verification reports. Checks build, tests, requirements

### Upgraded Skills

- **Diary** (Lv.5) — Structured Session Handoff section: in-progress work, uncommitted changes, exact pickup instructions
- **Echo** (Lv.5) — LanceDB vector-powered semantic recall with sentence-transformers. Auto-indexes sessions, SQLite fallback
- **Seal hook** — Commit format now supports conventional commits (`feat(scope): description`) alongside `[ProjectName]`

### Files Added
- `skills/humanize/SKILL.md` — Humanize skill
- `skills/state/SKILL.md` — State skill
- `skills/verify/SKILL.md` — Verify skill
- `skills/echo/index-sessions.py` — Vector index builder
- `skills/echo/search.py` — Semantic search CLI
- `skills/_research/memstack-v31-upgrade-spec.md` — Upgrade spec

### Files Modified
- `skills/diary/SKILL.md` — Lv.5, Session Handoff section
- `skills/echo/SKILL.md` — Lv.5, vector search protocol
- `.claude/hooks/pre-push.sh` — Conventional commit format support
- `MEMSTACK.md` — v3.1, new skills, level updates
- `README.md` — v3.1 notes, updated architecture tree

---

## v3.0.0-rc — 2026-02-22 — Plugin Packaging + Headroom Integration

**Builds on:** v3.0-beta rules and slash commands

### New: Headroom Auto-Integration

- `session-start.sh` now auto-detects and auto-starts the Headroom compression proxy
- Checks `localhost:8787/health` — if running, does nothing; if installed but stopped, auto-starts it
- Exports `ANTHROPIC_BASE_URL` when proxy starts successfully
- Never blocks session start — all Headroom logic is non-blocking with timeouts
- Configurable via `config.json` `headroom` section (`auto_start`, `port`)
- New rule: `.claude/rules/headroom.md` — proxy awareness and troubleshooting
- New command: `/memstack-headroom` — check proxy status and token savings

### New: Plugin Packaging

- `package.json` — NPM-style package manifest for `@cwinvestments/memstack`
- `files` list includes all distributable assets, excludes `config.local.json`, `memory/`, `db/memstack.db`
- Future install: `npx skills add cwinvestments/memstack`

### Updated

- `README.md` — Full rewrite for v3.0: installation, three-layer architecture diagram, Headroom section, slash commands, v3.0 badge
- `MEMSTACK.md` — v3.0-rc: Headroom in hook/rules/commands tables
- `config.json` — Added `headroom` section, version bump to 3.0.0-rc

### Files Added
- `package.json` — Plugin package manifest
- `.claude/rules/headroom.md` — Headroom proxy awareness rule
- `.claude/commands/memstack-headroom.md` — Slash command for proxy stats

### Files Modified
- `.claude/hooks/session-start.sh` — Headroom auto-detection and auto-start
- `MEMSTACK.md` — v3.0-rc architecture tables
- `CHANGELOG.md` — This entry
- `README.md` — Full rewrite for v3.0
- `config.json` — Headroom section, version bump

---

## v3.0.0-beta — 2026-02-22 — Rules Integration, Slash Commands, Auto-Indexing

**Builds on:** v3.0-alpha hook architecture

### New: CC Native Rules for Core Skills

Rules in `.claude/rules/` are loaded automatically every session — no need to read MEMSTACK.md first.

| Rule File | Skill | What It Does |
|-----------|-------|-------------|
| `echo.md` | Echo (Lv.4) | Always-on memory recall — search SQLite on past session references |
| `diary.md` | Diary (Lv.4) | Always-on session logging — log after task completion |
| `work.md` | Work (Lv.4) | Always-on task planning — activate on plan/todo/task keywords |

### New: Slash Command — `/memstack-search`

- `.claude/commands/memstack-search.md` — Quick memory lookup
- Invoked with `/memstack-search <query>` in CC
- Runs `memstack-db.py search` without activating full Echo skill
- Returns sessions, insights, and project context matching the query

### New: CLAUDE.md Auto-Indexing

- `session-start.sh` now auto-indexes CLAUDE.md into SQLite `project_context` table
- Extracts headings and first paragraphs from CLAUDE.md (or `*-CLAUDE.md` variants)
- Stores up to 1500 chars of key facts in `architecture_decisions` field
- Keeps SQLite memory in sync with project documentation automatically
- Restructured session-start.sh so auto-indexing runs even without API key

### Updated Skills (Lv.3 → Lv.4)

- **Echo** — Lv.4: CC rules integration + `/memstack-search` slash command + auto-indexed context
- **Diary** — Lv.4: CC rules integration + always-on session logging awareness
- **Work** — Lv.4: CC rules integration + always-on task planning awareness

### Architecture: Three Layers

```
MemStack v3.0-beta
├── Hooks (deterministic)     — Shell scripts, CC lifecycle events
│   ├── pre-push.sh           — Seal: build check, secrets scan, blocks bad pushes
│   ├── post-commit.sh        — Deploy: debug artifacts, format validation
│   ├── session-start.sh      — Monitor + CLAUDE.md auto-indexer
│   └── session-end.sh        — Monitor: report "completed" to API
├── Rules (always-loaded)     — Markdown files, loaded every session
│   ├── memstack.md           — Global conventions, deprecated skill guard
│   ├── echo.md               — Memory recall protocol
│   ├── diary.md              — Session logging protocol
│   └── work.md               — Task planning protocol
├── Commands (slash)          — Quick-access utilities
│   └── memstack-search.md    — /memstack-search <query>
├── Skills (context-aware)    — Markdown protocols, keyword/contextual triggers
│   ├── Echo, Diary, Work     — SQLite-backed memory (Lv.4)
│   ├── Project, Grimoire     — Session lifecycle (Lv.2-3)
│   ├── Scan, Quill           — Business tools (Lv.2)
│   └── Forge, Shard, Sight   — Dev tools (Lv.2)
└── Rules (.claude/rules/)    — Always-loaded behavioral constraints
```

### Files Added
- `.claude/rules/echo.md` — Echo memory recall rule
- `.claude/rules/diary.md` — Diary session logging rule
- `.claude/rules/work.md` — Work task planning rule
- `.claude/commands/memstack-search.md` — Slash command for memory search

### Files Modified
- `.claude/hooks/session-start.sh` — Added CLAUDE.md auto-indexing, restructured flow
- `MEMSTACK.md` — v3.0-beta: Three-layer architecture, rules table, commands table
- `CHANGELOG.md` — This entry
- `config.json` — Version bump to 3.0.0-beta
- `skills/echo.md` — Lv.4 level history
- `skills/diary.md` — Lv.4 level history
- `skills/work.md` — Lv.4 level history

---

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
