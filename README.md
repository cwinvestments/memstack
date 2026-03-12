# MemStack v3.2.3

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE) [![Version: 3.2.3](https://img.shields.io/badge/Version-3.2.3-green.svg)](CHANGELOG.md) [![Skills: 77](https://img.shields.io/badge/Skills-77-purple.svg)](MEMSTACK.md) [![Projects: 35%2B](https://img.shields.io/badge/Projects-35%2B-orange.svg)](MEMSTACK.md) [![CI: Passing](https://img.shields.io/badge/CI-Passing-brightgreen.svg)](.github/workflows/skill-guard.yml)

> Not a prompt collection. Not a cheat sheet. A battle-tested methodology for solo founders who ship.

77 specialist skills — each one loaded only when its expertise is needed. Drop in the React expert when building UI. Activate the RLS Guardian when writing migrations. Zero token bloat.

A structured skill framework for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) with SQLite-backed persistent memory, semantic vector search, deterministic hooks, always-on rules, and slash commands.

## What It Does

MemStack gives Claude Code **persistent memory** across sessions, **semantic recall** via vector search, **automated safety checks** on every commit and push, **portfolio governance** to prevent over-engineering, **work verification**, and **context compression** to make your sessions last longer.

## What's New in v3.2.3

- **TTS voice notifications** — Cross-platform text-to-speech (Windows, macOS, Linux). Pre-prompt alerts fire BEFORE approval prompts so you know to return to the terminal.
- **Diary webhook** — Session logs POST to n8n endpoint after markdown backup. Fire-and-forget so webhook failure never blocks saves.
- **Pro skills catalog** — `pro-catalog.md` rule provides organic upsell: mentions relevant Pro skills once per session when a task matches.

## What's New in v3.2

- **Governor** (#19) — Portfolio governance with 3-tier system (Prototype/MVP/Production). Prevents over-engineering by enforcing tier-appropriate complexity.
- **Description trap audit** — All 17 skill descriptions rewritten to say WHEN to invoke, never HOW the skill works. Prevents Claude from shortcutting full protocols.
- **Anti-rationalization tables** — Echo, Diary, and Verify now include tables of known Claude excuses with rebuttals, improving protocol compliance.
- **Silent context compilation** — Work skill (Lv.5) now silently gathers STATE.md, CLAUDE.md, recent diary, and git state before any plan operation.
- Patterns adopted from [Intellegix Code Agent Toolkit](https://github.com/intellegix/intellegix-code-agent-toolkit) and [Superpowers](https://github.com/obra/superpowers) plugin research.

## What's New in v3.1

- **Humanize** (#16) — Remove AI writing patterns from text output. Curated pattern table + voice guidelines.
- **State** (#17) — Living STATE.md document tracking current task, blockers, and next steps. Auto-reads at session start.
- **Verify** (#18) — Pre-commit verification reports. Checks build, tests, and requirements before committing.
- **Seal upgrade** — Commit format now supports conventional commits (`feat(scope): description`) alongside `[ProjectName]` format.
- **Diary upgrade** (Lv.5) — Structured Session Handoff section for seamless pickup between sessions.
- **Echo upgrade** (Lv.5) — Semantic vector search via LanceDB with SQLite fallback (added in v3.0.1).

MemStack is a lightweight alternative to heavyweight frameworks like GSD — same capabilities, pure markdown, zero dependencies.

## Prerequisites

- **Claude Code** — Install guide: https://docs.anthropic.com/en/docs/claude-code
- **Python 3.10+** — Download: https://www.python.org/downloads/
- **Git** — Download: https://git-scm.com/downloads
- **LanceDB + sentence-transformers** (optional, for semantic recall) — `pip install lancedb sentence-transformers`

## How It Works

MemStack™ follows a **Progressive Disclosure** pattern:

- Skills load lean (~80 lines of context)
- The MCP Skill Loader surgically fetches only what your exact task needs
- Full expert depth activates on demand — not dumped into every session
- Result: zero token bloat, full specialist precision

## Quick Start

**One command. Works across every project immediately.**

```bash
git clone https://github.com/cwinvestments/memstack .claude/skills
```

### Advanced: Deploy across multiple projects

Clone the full repo, then link it into each project:

```bash
git clone https://github.com/cwinvestments/memstack.git
cd memstack
```

### Step 2: Create your local config
```bash
cp config.json config.local.json
```

Open `config.local.json` and edit the `projects` section with your actual paths:

Windows: `"path": "C:\\Projects\\my-app"`

Mac/Linux: `"path": "/home/user/projects/my-app"`

Everything else works with defaults.

### Step 3: Initialize the database
```bash
python db/memstack-db.py init
```

### Step 4: Install to your project

Copy the `.claude/` folder into any project you want MemStack to manage:

Windows:
```cmd
xcopy /E /I /Y C:\Projects\memstack\.claude C:\Projects\yourproject\.claude
```

Mac/Linux:
```bash
cp -r /path/to/memstack/.claude /path/to/yourproject/.claude
```

That's it. Start Claude Code in your project directory and begin working — hooks fire automatically, rules load every session, and skills activate on matching triggers. No activation line needed.

> **Without `.claude/` installed:** If you're in a project that doesn't have MemStack's `.claude/` folder, you can still use skills manually by adding this to your prompt: `Read C:\Projects\memstack\MEMSTACK.md and follow the MemStack skill framework.`

### Step 5 (Optional): Install Semantic Search

LanceDB + sentence-transformers enables semantic vector search for the Echo skill — finding relevant past sessions by meaning, not just keywords.

```bash
pip install lancedb sentence-transformers
```

Index your existing sessions:
```bash
python skills/echo/index-sessions.py
```

Echo will automatically use semantic search when LanceDB is available, and fall back to SQLite keyword search when it's not.

For higher-quality embeddings, optionally set an OpenAI API key:

Windows: `setx OPENAI_API_KEY sk-...`

Mac/Linux: `echo 'export OPENAI_API_KEY=sk-...' >> ~/.bashrc && source ~/.bashrc`

### Step 6 (Optional): Install Headroom

[Headroom](https://github.com/chopratejas/headroom) compresses tool outputs by ~34%, making sessions last longer.
```bash
pip install headroom-ai
```

MemStack auto-detects and auto-starts it. To make permanent:

Windows: `setx ANTHROPIC_BASE_URL http://127.0.0.1:8787`

Mac/Linux: `echo 'export ANTHROPIC_BASE_URL=http://127.0.0.1:8787' >> ~/.bashrc && source ~/.bashrc`

## Launcher

MemStack includes one-click launcher scripts that start Headroom, verify it's healthy, and open VS Code.

| Platform | File | How to run |
|----------|------|------------|
| Windows | `start-memstack.bat` | Double-click, or right-click → Send to → Desktop (create shortcut) |
| Mac/Linux | `start-memstack.sh` | `chmod +x start-memstack.sh` then `./start-memstack.sh` |

**What the launcher does:**

1. Checks if Headroom is already running on port 8787 (skips start if so)
2. Starts the Headroom proxy if needed and waits for initialization
3. Runs a health check to confirm the proxy is responding
4. Opens VS Code to your projects directory

If Headroom is not installed, the launcher reports the failure and continues — it's optional.

## Adding MemStack to Your Projects

MemStack's rules, hooks, and commands live in `.claude/`. Link this folder into any project using a junction (Windows) or symlink (macOS/Linux) so updates propagate instantly.

**First-time setup:**

```bash
git clone https://github.com/cwinvestments/memstack.git C:\Projects\memstack
```

**Link a project (Windows):**

```bat
start-memstack.bat link C:\Projects\YourProject
```

Or manually:

```bat
mklink /J C:\Projects\YourProject\.claude C:\Projects\memstack\.claude
```

**Link a project (macOS/Linux):**

```bash
ln -s /path/to/memstack/.claude /path/to/YourProject/.claude
```

**How it works:** The junction/symlink makes your project's `.claude/` point to MemStack's `.claude/`. Any updates to rules, hooks, or commands in MemStack instantly apply to all linked projects — no copying or re-syncing needed.

**Removing a link:**

| Platform | Command | Notes |
|----------|---------|-------|
| Windows | `rmdir C:\Projects\YourProject\.claude` | Removes the junction only, not the source |
| macOS/Linux | `rm C:\Projects\YourProject\.claude` | Removes the symlink only, not the source |

## Three-Layer Architecture

MemStack v3.2.3 uses three layers with increasing reliability:

```
MemStack v3.2.3
├── Hooks (deterministic)        — Shell scripts, CC lifecycle events
│   ├── pre-push.sh              — Build check, secrets scan, commit format (standard + conventional)
│   ├── post-commit.sh           — Debug artifacts, format validation
│   ├── session-start.sh         — Headroom auto-start + CLAUDE.md indexer + API monitor
│   └── session-end.sh           — Report "completed" to monitoring API
├── Rules (always-loaded)        — Markdown files, loaded every session
│   ├── memstack.md              — Global conventions, commit format, deprecated skill guard
│   ├── echo.md                  — Memory recall protocol (vector + SQLite)
│   ├── diary.md                 — Session logging protocol (with handoff)
│   ├── work.md                  — Task planning protocol
│   └── headroom.md              — Compression proxy awareness
├── Commands (slash)             — Quick-access utilities
│   ├── memstack-search.md       — /memstack-search <query>
│   └── memstack-headroom.md     — /memstack-headroom (proxy stats)
└── Skills (context-aware)       — Markdown protocols, keyword triggers
    ├── Echo, Diary, Work        — SQLite + LanceDB vector memory (Lv.5)
    ├── Governor                 — Portfolio governance (Lv.1) ← NEW in v3.2
    ├── State, Verify, Humanize  — Workflow quality (Lv.1)
    ├── Project, Grimoire        — Session lifecycle (Lv.2-3)
    ├── Scan, Quill              — Business tools (Lv.2)
    └── Forge, Shard, Sight      — Dev tools (Lv.2)
```

**Hooks** always fire (deterministic, zero tokens). **Rules** always load (persistent awareness). **Skills** fire on keyword/condition match.

## Slash Commands

| Command | What It Does |
|---------|-------------|
| `/memstack-search <query>` | Search SQLite memory for past sessions, insights, and project context |
| `/memstack-headroom` | Check Headroom proxy status and token savings |

## Skills

| Skill | Emoji | Level | What It Does |
|-------|-------|-------|-------------|
| Echo | 🔊 | **Lv.5** | Semantic recall via LanceDB vectors + SQLite fallback |
| Diary | 📓 | **Lv.5** | Documents sessions to SQLite + structured handoff for seamless pickup |
| Work | 📋 | **Lv.5** | Plan execution with SQLite-backed task tracking + silent context compilation |
| Governor | 🏛️ | Lv.1 | Portfolio governance — tier/phase constraints prevent over-engineering |
| Project | 💾 | **Lv.3** | Saves/restores project state via SQLite context |
| Humanize | ✍️ | Lv.1 | Removes AI writing patterns — makes text sound human |
| State | 📍 | Lv.1 | Living STATE.md — tracks current task, blockers, next steps |
| Verify | ✅ | Lv.1 | Pre-commit verification — checks build, tests, requirements |
| Grimoire | 📖 | Lv.2 | Manages CLAUDE.md files across projects |
| Familiar | 👻 | Lv.2 | Splits tasks across multiple CC sessions |
| Scan | 🔍 | Lv.2 | Analyzes project scope and suggests pricing |
| Quill | ✒️ | Lv.2 | Generates professional client quotations |
| Forge | 🔨 | Lv.2 | Creates new MemStack skills |
| Shard | 💎 | Lv.2 | Refactors large files into smaller modules |
| Sight | 👁️ | Lv.2 | Generates Mermaid architecture diagrams |
| Compress | ⚙️ | Lv.1 | Manages Headroom proxy — status, stats, troubleshooting |

Deprecated skills (Seal, Deploy, Monitor) have been replaced by deterministic hooks that always fire — no LLM required.

## Storage

All memory is stored in SQLite (`db/memstack.db`) with WAL mode:
```bash
python db/memstack-db.py search "authentication"     # Search everything
python db/memstack-db.py get-sessions my-app          # Recent sessions
python db/memstack-db.py get-insights my-app          # Decisions and patterns
python db/memstack-db.py stats                        # Database overview
```

| Table | Purpose |
|-------|---------|
| `sessions` | Session diary entries (written by Diary, read by Echo) |
| `insights` | Extracted decisions and patterns |
| `project_context` | Current state of each project (auto-indexed from CLAUDE.md) |
| `plans` | Task lists with per-task status |

## Configuration Reference

`config.local.json` sections:

| Section | Required | Purpose |
|---------|----------|---------|
| `projects` | Yes | Your project paths and CLAUDE.md locations |
| `headroom` | No | Context compression settings (port, auto-start) |
| `cc_monitor` | No | External dashboard API URL and key |
| `session_limits` | No | Max lines for session log exports (default: 500) |
| `defaults` | No | Commit format, auto-diary, auto-monitor toggles |

## Upgrading from v2.x
```bash
git pull
python db/memstack-db.py init      # Update database schema
python db/migrate.py               # Import existing markdown files (safe to re-run)
python db/memstack-db.py stats     # Verify migration
```

## Creating Custom Skills

Use the **Forge** skill: say `"forge a new skill for [description]"` in any CC session. Forge generates the file with YAML frontmatter and registers it in the master index.

## Troubleshooting

**"Python was not found"** — Install Python 3.10+ and make sure "Add Python to PATH" is checked during install. Restart your terminal after installing.

**CC sessions not using Headroom** — Run `headroom proxy` in a separate terminal first, then launch CC. Or install permanently with `setx ANTHROPIC_BASE_URL http://127.0.0.1:8787` (Windows).

**Hook errors on push** — The pre-push hook blocks pushes that contain secrets or fail build checks. Fix the issue it reports, then push again.

**"Database locked" errors** — Close any other process accessing `db/memstack.db`, or delete the `.db-wal` and `.db-shm` files and retry.

## License

## Upgrade to Pro

The free repo includes **77 skills** (17 core + 60 categorized). [MemStack™ Pro](https://memstack.pro) adds **3 Pro-exclusive skills** — bringing the total to **80 across 10 categories** — plus an **MCP Skill Loader**, a semantic search MCP server where Claude Code calls `find_skill("your task")` and loads only the relevant skill on demand.

### Free Skills (77) — Full List

<details>
<summary><strong>Core (17)</strong> — Memory, planning, workflow, and utilities</summary>

| Skill | Description |
|-------|-------------|
| Diary | Session logging with git integration and SQLite storage |
| Echo | Past session recall via semantic vector search + SQLite |
| Work | Task planning and todo list management |
| State | Load and update project context at session start |
| Project | Save project state and handoff context |
| Verify | Verification before committing completed work |
| Governor | Project maturity assessment and complexity budgeting |
| Grimoire | Update project context files after significant changes |
| Compress | Headroom proxy status and token savings |
| Humanize | Make AI-generated text sound natural |
| Forge | Create new MemStack skills |
| Familiar | Dispatch work across parallel CC sessions |
| Scan | Codebase complexity analysis and project estimation |
| Quill | Generate client-facing price quotations |
| Shard | Split and manage files over 1000 lines |
| Sight | Visual diagrams and architecture overviews |
| KDP Format | Convert manuscripts to KDP-ready .docx |

</details>

<details>
<summary><strong>Security (7)</strong> — Audits, policies, vulnerability scanning</summary>

| Skill | Description |
|-------|-------------|
| RLS Checker | Supabase Row Level Security policy verification |
| RLS Guardian | RLS enforcement on new/altered database tables |
| API Audit | API endpoint protection verification |
| OWASP Top 10 | Comprehensive web security review against OWASP Top 10 |
| Secrets Scanner | Exposed secrets detection in source code |
| Dependency Audit | Vulnerability scanning and abandoned package detection |
| CSP Headers | HTTP security headers (CSP, HSTS, X-Frame-Options) |

</details>

<details>
<summary><strong>Deployment (6)</strong> — CI/CD, containers, hosting, DNS</summary>

| Skill | Description |
|-------|-------------|
| Railway Deploy | Application deployment to Railway with env vars and domains |
| Netlify Deploy | Static site and serverless function deployment to Netlify |
| Docker Setup | Container optimization with Dockerfile and docker-compose |
| CI/CD Pipeline | Automated build, test, and deployment pipelines (GitHub Actions) |
| Domain SSL | DNS records, SSL certificates, and custom domain configuration |
| Hetzner Setup | VPS provisioning, hardening, and deployment |

</details>

<details>
<summary><strong>Development (7)</strong> — Architecture, testing, performance</summary>

| Skill | Description |
|-------|-------------|
| Database Architect | Supabase/Postgres table structures, relationships, and RLS |
| API Designer | RESTful API route design with request/response schemas |
| Code Reviewer | Structured code quality, security, and performance reviews |
| Test Writer | Unit, integration, and component tests with mocking |
| Migration Planner | Safe schema evolution with zero-downtime strategies |
| Performance Audit | Frontend and backend performance diagnosis and optimization |
| Refactor Planner | Systematic code improvement and tech debt reduction |

</details>

<details>
<summary><strong>Business (6)</strong> — Proposals, contracts, invoicing</summary>

| Skill | Description |
|-------|-------------|
| Proposal Writer | Project proposals for client and freelance engagements |
| Scope of Work | Project boundaries, deliverables, and acceptance criteria |
| Contract Template | Professional service contracts with legal clauses |
| Client Onboarding | Structured onboarding process for new clients |
| Invoice Generator | Professional invoices with line items and payment instructions |
| Financial Model | Financial projections with scenario modeling and unit economics |

</details>

<details>
<summary><strong>Content (8)</strong> — Blog, email, video, social</summary>

| Skill | Description |
|-------|-------------|
| Blog Post | Long-form written content for blogs and publications |
| Email Sequence | Multi-email automated campaigns with nurture sequences |
| Landing Page Copy | Persuasive short-form copy for product landing pages |
| Newsletter | Newsletter editions with subject lines, content, and growth strategy |
| Product Description | Conversion-optimized product descriptions for e-commerce |
| TikTok Script | Scripts with hooks and visual cues for 15–60s vertical videos |
| Twitter Thread | Multi-tweet narratives with hooks, data points, and CTAs |
| YouTube Script | Scripted content for YouTube with hooks, chapters, and CTAs |

</details>

<details>
<summary><strong>SEO & GEO (6)</strong> — Search optimization, structured data</summary>

| Skill | Description |
|-------|-------------|
| Site Audit | Website SEO health evaluation |
| Keyword Research | Target keywords with search volume and difficulty |
| Meta Tag Optimizer | HTML meta tag optimization for search visibility |
| Schema Markup | Schema.org structured data (JSON-LD) for rich results |
| AI Search Visibility | Content optimization for AI-powered search engines |
| Local SEO | Local search optimization (Google Business Profile, NAP) |

</details>

<details>
<summary><strong>Marketing (8)</strong> — Funnels, ads, launches, pricing</summary>

| Skill | Description |
|-------|-------------|
| Sales Funnel | Complete customer journey from stranger to repeat buyer |
| Facebook Ad | Social media ad copy with targeting for Meta platforms |
| Google Ad | Keyword groups, headlines, and Quality Score optimization |
| Launch Plan | Day-by-day launch timeline with pre/post checklists |
| Competitor Analysis | Pricing, feature, and messaging comparisons against competitors |
| Pricing Strategy | Pricing tiers, psychology application, and A/B testing |
| Lead Magnet | Lead capture assets with landing page copy and nurture sequences |
| Webinar Script | Timestamped presentation scripts with slide notes |

</details>

<details>
<summary><strong>Product (6)</strong> — PRDs, specs, roadmaps, backlog</summary>

| Skill | Description |
|-------|-------------|
| PRD Writer | Engineering-ready PRD with problem statement and personas |
| Feature Spec | Detailed feature specifications with user flows and edge cases |
| User Story Generator | Prioritized stories with Given/When/Then criteria |
| MVP Scoper | Smallest viable build that validates product hypothesis |
| Roadmap Builder | Strategic planning with themes, milestones, and resources |
| Feedback Analyzer | Support ticket and review categorization and prioritization |

</details>

<details>
<summary><strong>Automation (5)</strong> — Workflows, webhooks, scheduling</summary>

| Skill | Description |
|-------|-------------|
| n8n Workflow Builder | Design automated workflows with triggers and data transformations |
| Webhook Designer | Secure webhook receivers with validation and idempotency |
| Cron Scheduler | Recurring background jobs with monitoring and failure handling |
| API Integration | Build reliable connections between systems via their APIs |
| Content Pipeline | Automate creation, formatting, and publishing across platforms |

</details>

### Pro-Exclusive Skills (3) — 🔒

| Skill | Description | Unlock |
|-------|-------------|--------|
| 🔒 Consolidate | Weekly cross-project summaries and pattern detection | [Pro](https://memstack.pro) |
| 🔒 Context DB | SQLite-backed facts database — query project knowledge instead of reading full CLAUDE.md | [Pro](https://memstack.pro) |
| 🔒 API Docs | Fetch current API documentation via Context Hub before writing API code | [Pro](https://memstack.pro) |

## License

MIT — see [LICENSE](LICENSE) for details.

Copyright (c) 2026 CW Affiliate Investments LLC
