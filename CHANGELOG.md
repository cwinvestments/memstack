# MemStack™ Changelog

## v3.5.5 — 2026-06-29 — TokenStack Skill Refresh

### Changed
- **token-optimization skill** — description and content refreshed to center **TokenStack™** as the sole built-in compression proxy; dropped the retired Headroom / RTK / Serena three-layer framing. Skill-content/description refresh only — **no new skills**; total stays **128** (85 free + 43 Pro-exclusive).

### Notes
- Plugin-track patch (Option A): plugin → **3.5.5**, loader unchanged at **4.5.1**. Republished so the marketplace bundle refreshes — the version-string bump is what forces clients to re-pull the corrected skill (`/plugin marketplace update` keys on the version *differing*, not on semver ordering). GitHub Releases are human-facing only and not required for propagation.

## v3.5.4 — 2026-06-23 — Documentation Alignment + Skill-Change Guardrails

### Added
- **git-guard skill** (free) — installer + verifier for the secret-blocking git setup (gitleaks + pre-commit/pre-push hooks). Added to all skill catalogs with conformed naming.
- **ADDING-SKILLS.md** — canonical maintainer checklist for adding, removing, renaming, or re-counting skills: 16 count locations, the two-tier free/Pro scheme, and the 3-channel update architecture (marketplace plugin, PyPI loader, Pro site).
- **CLAUDE.md pointer** — mandatory reference to ADDING-SKILLS.md before any skill add/remove/rename/recount, so the checklist can't be skipped.

### Changed
- **Skill counts corrected to 128** — 128 total (85 free + 43 Pro-exclusive) across README, MEMSTACK, SKILL-REFERENCE, and catalogs.
- **Install docs** — restored the marketplace install step and documented the 3-channel update path.
- **Compression proxy** — removed deprecated Headroom; TokenStack™ is now the sole context-compression proxy.
- **Doc version alignment** — README badge, MEMSTACK title + changes-line, and SKILL-REFERENCE footer set to v3.5.4 (see versioning note below).
- **Version bumps** — plugin manifests advanced to 3.5.2, then 3.5.3.
- **Skill-count drift enforcement** (cross-repo) — `check_skill_drift.py` now fails on skill-count drift. Primary changelog entry lives in the memstack-skill-loader repo; noted here because it guards this repo's counts.

---

> **Versioning note.** The entry below was originally labeled **v4.3.0**, but the plugin manifest read **3.5.0** on 2026-05-27 — the "4.3.0" was an aspirational label that never shipped. It has been re-homed as **v3.5.0-docs** with its body preserved verbatim (including the now-superseded "plugin install" and "all docs updated to v4.3.0" lines) as the honest record of that day's documentation audit. No separate changelog entries exist for v3.5.1–v3.5.3 (release-only version bumps); versioning resumes at v3.5.4 above.

## v3.5.0-docs — 2026-05-27 — Documentation Audit

### Changed
- **Skill counts updated** — 127 total (84 free + 43 Pro-exclusive). `database-architect` moved to Pro.
- **Install method** — Removed deprecated `plugin install` references. Install is now `pip install memstack-skill-loader` + `claude mcp add`.
- **TokenStack™ branding** — All Headroom references updated to TokenStack™ across README, GETTING-STARTED, SKILL-REFERENCE, and MEMSTACK.
- **Version bumps** — All docs updated to v4.3.0.
- **Pro skill list** — Updated to 43 skills (added `database-architect`).

---

## v3.3.4 — 2026-03-28 — Git Audit + Docs Update

### Added
- **Branching skill** (`skills/branching/SKILL.md`) — Enforces dev-branch workflow: all work on `dev`, merge to `master` only after Reviewer confirms.
- **Dev branch** — Created `dev` branch as default working branch. All new work happens here; `master` is release-only.
- **SessionStart license nudge** — Hook fires at session start when `MEMSTACK_PRO_LICENSE_KEY` is not set, guiding users through Pro setup.
- **Tier structure documentation** — All docs now document the free/Pro tier split: 78 free skills, 81 total (78 free + 3 Pro-exclusive: consolidate, context-db, api-docs).
- **90-day graduation rule** — All new skills default to Pro-exclusive and drop to the free tier after 90 days unless marked permanent-Pro.

### Changed
- **Full git audit** — Verified entire git history and working tree are clean: no secrets, no .env files, no grace period files, no hardcoded keys. Repo is safe for public visibility.
- **Delivery model updated** — Removed private GitHub repo references. New model: one public repo + `MEMSTACK_PRO_LICENSE_KEY` activation. Customer pays Stripe ($29) -> gets key via email -> sets env var -> Pro skills unlock.
- **Docs updated** — README.md, GETTING-STARTED.md, SKILL-REFERENCE.md, MEMSTACK.md, and docs/MARKETPLACE-PREP.md updated with current version (3.3.4), accurate skill counts (81 total), and Pro tier info.

---

## v3.3.3 — 2026-03-24 — Production-Grade Secrets Scanning

### Added
- **Pre-commit secrets hook** (`pre-commit-secrets.sh`) — Scans all staged files before every `git commit` using production-grade detection covering 700+ credential formats across every major cloud provider and API service. Blocks commits containing secrets with redacted output. Falls back to built-in regex scan if production scanner is not installed.
- **`.gitleaks.toml`** — Project-level scanner configuration excluding test fixtures, example files, `.claude/diary/`, and `.claude/observations/` directories from scanning.

### Changed
- **Pre-push hook** (`pre-push.sh`) — Upgraded from 5-keyword regex scan to production-grade detection (700+ credential formats). Full working-tree scan before every push. Silent fallback to regex if scanner is not installed.
- **secrets-scanner skill (Lv.3)** — Documented automated hook coverage, fallback behavior, and relationship between manual audits and automated scanning.

---

## v3.3.2 — 2026-03-16 — PostToolUse Observations + SessionStart Context Injection

### Added
- **PostToolUse observation hook** (`post-tool-monitor.sh`) — Captures lightweight observations after every Write, Edit, MultiEdit, and Bash tool call. Logs timestamp, tool name, parsed input summary, and working directory to `.claude/observations/YYYY-MM-DD.md` (daily file, append-only). Uses Python JSON parsing with grep fallback.
- **SessionStart context loader** (`session-context-load.sh`) — On every new CC session, reads last 3 diary entries and last 3 observation files, writes a condensed summary to `.claude/session-context.md` (max 200 lines). Idempotent — overwrites previous context on each session start. Checks both `.claude/diary/` and `memory/sessions/` for diary sources.

### Changed
- **settings.json** — Added two new independent hook entries (PostToolUse observation monitor, SessionStart context loader) following Option B architecture — each with its own timeout budget, separate from existing hooks.

---

## v3.3.1 — 2026-03-12 — PreCompact Auto-Diary

### Added
- **PreCompact hook** — Automatically saves a diary snapshot before Claude Code context compaction runs. Captures uncommitted changes, recent commits, shell history, and modified files. Entries saved to `.claude/diary/{date}-compaction.md` with `COMPACTION_INTERRUPTED` flag. Multiple compactions in one day append to the same file. Fully automatic — no user input required.

### Changed
- **Diary skill (Lv.6)** — Documented PreCompact hook behavior, comparison with manual diary, and session resume guidance.

---

## v3.3.0 — 2026-03-12 — Context DB & API Docs Skills

### Added
- **context-db** — New Core skill: SQLite-backed facts database per project (`.claude/context.db`). Stores structured knowledge as key/value pairs across 5 categories (decisions, patterns, components, config, gotchas). CC queries only relevant facts instead of reading full CLAUDE.md — estimates and logs token savings to `.claude/context-db-stats.json`. Includes inbox watcher for auto-ingestion and CLAUDE.md seeding. Inspired by Google ADK Always-On Memory Agent.
- **api-docs** — New Core skill: fetches current API documentation via Context Hub (`chub`) before CC writes code that calls external APIs. Supports 13 APIs (Supabase, Stripe, SendGrid, Railway, Netlify, Anthropic, OpenAI, Vercel, Cloudflare, Firebase, Resend, Twilio, GitHub). Graceful fallback when chub is not installed. Built on Context Hub by Andrew Ng / AISuite team.

---

## v3.2.2 — 2026-03-01 — Documentation Audit, TTS Notifications, Diary Webhook

### Added
- **rls-guardian** — New Security skill (7th): auto-generates RLS policies for every new `CREATE TABLE` or `ALTER TABLE` statement, enforcing row-level security by default

### Changed
- **notify.md** — Pre-prompt voice notification: TTS "Claude needs your attention" now fires BEFORE approval prompts and questions, not just after task completion
- **diary.md** — Added devlog webhook (step 7): POSTs diary content to n8n endpoint after markdown backup is saved. Fire-and-forget with `.catch()` so webhook failure never blocks diary save
- **README.md** — Complete rewrite: removed "DRAFT stubs" status (all 75+ skills are implemented), added Key Features section, documented on-demand loading, TTS, webhook, templates breakdown (8 starters + 3 utilities)
- **MEMSTACK.md** — Version bump to v3.2.2, updated v3.2 changes description
- **package.json** — Version bump to 3.2.2
- **CHANGELOG.md** — Full history backfill from project inception

---

## v3.2.1-templates — 2026-03-01 — Starter Templates

### Added: 8 Starter Templates
- `nextjs-supabase` — Next.js + Supabase full-stack starter
- `react-node-postgres` — React + Node.js + PostgreSQL starter
- `saas-starter` — SaaS boilerplate with auth, billing, dashboard
- `landing-page` — Marketing landing page with conversion optimization
- `api-backend` — REST/GraphQL API backend starter
- `chrome-extension` — Chrome extension with Manifest V3
- `electron-app` — Desktop app with Electron
- `mobile-react-native` — Mobile app with React Native

---

## v3.2.1-catalog — 2026-03-01 — On-Demand Skill Loading

### Changed: Architecture Overhaul
- Moved all 59 Pro skills from `.claude/rules/` (always-loaded) to `skills/` (on-demand)
- Created `pro-skills.md` catalog rule — skills load only when a task matches their triggers
- Prevents context window bloat from loading 59 skill protocols at session start
- Upgraded notification system from chime to cross-platform TTS (Windows, macOS, Linux)

---

## v3.2.1-skills — 2026-02-28 to 2026-03-01 — All 59 Skills Implemented

### Security (6 skills)
- `rls-checker` — Row Level Security policy auditor for Supabase (first production Pro skill)
- `api-audit` — API endpoint security analysis
- `secrets-scanner` — Leaked credentials and env file auditor
- `owasp-top10` — OWASP Top 10 vulnerability checker
- `dependency-audit` — Package dependency vulnerability scanner
- `csp-headers` — Content Security Policy header generator

All 4 security skills (rls-checker, api-audit, secrets-scanner, owasp-top10) were refined based on AdminStack audit feedback.

### Deployment (6 skills)
- `railway-deploy` — Railway platform deployment guide
- `netlify-deploy` — Netlify deployment and configuration
- `domain-ssl` — Domain DNS and SSL/HTTPS setup
- `hetzner-setup` — Hetzner VPS provisioning and configuration
- `ci-cd-pipeline` — CI/CD pipeline design and setup
- `docker-setup` — Docker containerization guide

### Development (7 skills)
- `database-architect` — Database schema design and optimization
- `api-designer` — REST/GraphQL API architecture
- `code-reviewer` — Systematic code review protocol
- `performance-audit` — Application performance analysis
- `refactor-planner` — Systematic code improvement planning
- `test-writer` — Comprehensive test generation (unit, integration, component)
- `migration-planner` — Safe database schema evolution

### Business (7 skills)
- `proposal-writer` — Professional proposal and pitch generation
- `sop-builder` — Standard operating procedure documentation
- `scope-of-work` — Project scope definition and boundaries
- `invoice-generator` — Professional invoice builder with calculations
- `contract-template` — Service agreement generator with legal clauses
- `client-onboarding` — New client setup system with welcome sequence
- `financial-model` — Business financial projections and unit economics

### Content (8 skills)
- `blog-post` — SEO-optimized blog article writer
- `landing-page-copy` — Conversion-focused landing page copy
- `email-sequence` — Automated email drip sequence builder
- `youtube-script` — Long-form video script with chapters
- `twitter-thread` — Viral thread builder with hook formulas
- `tiktok-script` — Short-form video script with timestamped cues
- `newsletter` — Email newsletter builder with growth tactics
- `product-description` — E-commerce listing copy optimizer

### SEO & GEO (6 skills)
- `site-audit` — Technical SEO site health analysis
- `keyword-research` — Keyword strategy and opportunity mapping
- `meta-tag-optimizer` — Meta title/description optimization
- `schema-markup` — JSON-LD structured data generator
- `ai-search-visibility` — AI search engine optimization (ChatGPT, Perplexity, etc.)
- `local-seo` — Local business SEO strategy

### Marketing (8 skills)
- `sales-funnel` — Full-funnel conversion architecture
- `facebook-ad` — Meta ads copy and targeting strategy
- `google-ad` — Search campaign builder with RSA format
- `launch-plan` — Go-to-market calendar with contingencies
- `competitor-analysis` — Competitive intelligence report
- `pricing-strategy` — Revenue-optimized pricing design
- `lead-magnet` — Opt-in asset and delivery system
- `webinar-script` — Teach-to-sell presentation script

### Product (6 skills)
- `prd-writer` — Product requirements document generator
- `feature-spec` — Detailed feature specification with acceptance criteria
- `user-story-generator` — Backlog-ready story builder with Given/When/Then
- `mvp-scoper` — Minimum viable product definition
- `roadmap-builder` — Strategic Now/Next/Later roadmap
- `feedback-analyzer` — Customer feedback intelligence and prioritization

### Automation (5 skills)
- `n8n-workflow-builder` — Visual automation workflow design
- `webhook-designer` — Secure webhook handler with HMAC verification
- `cron-scheduler` — Scheduled job design with overlap prevention
- `api-integration` — System-to-system API connector
- `content-pipeline` — Multi-platform content automation

---

## v3.2.1-init — 2026-02-28 — Project Initialization

### Added
- Initialized MemStack Pro repository with complete free MemStack base
- Created premium skill directory structure across 9 categories
- Added 3 utility templates: `client-quote`, `handoff`, `project-snapshot`
- Headroom startup command fix in rules
- All free base skills, hooks, rules, commands, and database infrastructure included

### Architecture
```
MemStack Pro v3.2.2
├── Free Base (complete MemStack)
│   ├── Hooks (deterministic)      — pre-push, post-commit, session-start/end
│   ├── Rules (always-loaded)      — memstack, echo, diary, work, notify, headroom, pro-skills catalog
│   ├── Commands (slash)           — /memstack-search
│   └── Skills (19 core)           — Echo, Diary, Work, Forge, Scan, Governor, etc.
├── Pro Skills (59, on-demand)     — Loaded via catalog when task matches triggers
│   ├── Security (6)
│   ├── Deployment (6)
│   ├── Development (7)
│   ├── Business (7)
│   ├── Content (8)
│   ├── SEO & GEO (6)
│   ├── Marketing (8)
│   ├── Product (6)
│   └── Automation (5)
└── Templates (11)
    ├── Starter (8)                — nextjs-supabase, react-node-postgres, saas-starter, etc.
    └── Utility (3)                — client-quote, handoff, project-snapshot
```
