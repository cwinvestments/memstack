# MemStack™

[![Version: 3.5.7](https://img.shields.io/badge/Version-3.5.7-green.svg)](CHANGELOG.md)

The structured skill framework for Claude Code — **130 professional skills** for deployment, security, databases, content, marketing, and more.

Skills activate automatically when you need them. Say "deploy this to Railway" and the right skill loads on demand.

### Install

MemStack installs in two parts: the **skills** (via the Claude Code plugin
marketplace) and the **engine** (the MCP skill loader, via PyPI). You need
both — the loader reads skill files from the installed marketplace plugin.
Every command below is labeled **(in Claude Code)** or **(in terminal)** —
running one in the wrong place is the most common setup mistake.

**Step 1 — Install the free skills · (in Claude Code):**
```
/plugin marketplace add cwinvestments/memstack
/plugin install memstack@cwinvestments-memstack
```
Run both commands. This unlocks the 86 free skills right away.

> **SSH error?** ("Host key verification failed" on a fresh server that's never used GitHub over SSH.)
> **Default fix · (in terminal)** — rewrite GitHub to HTTPS, then retry Step 1:
> ```bash
> git config --global url."https://github.com/".insteadOf "git@github.com:"
> ```
> **Backup fix · (in terminal)** — add GitHub's host key, then retry Step 1:
> ```bash
> mkdir -p ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts
> ```

**Step 2 — Install the engine · (in terminal):**

Windows:
```bash
pip install memstack-skill-loader
```

Linux / Mac — use the explicit interpreter (the same one you register in Step 3):
```bash
/usr/bin/python3 -m pip install memstack-skill-loader --break-system-packages
```
Find yours with `which python3` and substitute it if it isn't `/usr/bin/python3`. The `--break-system-packages` flag is required on newer externally-managed Python. No pip for that interpreter? Run `sudo apt install python3-pip` first (Debian/Ubuntu).

**Step 3 — Register the MCP server · (in terminal):** register against the **same interpreter you installed onto in Step 2.**

Windows:
```bash
claude mcp add --scope user memstack-skills -- python -m memstack_skill_loader
```

Linux / Mac:
```bash
claude mcp add --scope user memstack-skills -- /usr/bin/python3 -m memstack_skill_loader
```
If this doesn't match Step 2's interpreter, the server won't launch (you'll see a "failed to reconnect" error and `activate_license` will be missing).

**Step 4 — Activate your license · (in Claude Code, after a full restart):** fully quit and reopen Claude Code first so it picks up the new MCP server, then run:
```
activate_license(key="your-key", email="you@example.com")
```
This unlocks the 44 Pro-exclusive skills (86 free + 44 Pro = 130 total). Free-tier users can skip this step — type `list skills` to verify the 86 free skills loaded.

See [GETTING-STARTED.md](GETTING-STARTED.md) for detailed setup, and the [Troubleshooting](#troubleshooting) section below.

### Troubleshooting

**`error: externally-managed-environment` (during Step 2)** — pip refuses to install on a system-managed Python. Add `--break-system-packages` · (in terminal):
```bash
/usr/bin/python3 -m pip install memstack-skill-loader --break-system-packages
```

**Plugin clone fails: "Host key verification failed" (during Step 1)** — a fresh server that's never connected to GitHub over SSH. **Default fix · (in terminal):** `git config --global url."https://github.com/".insteadOf "git@github.com:"` then retry Step 1. **Backup fix · (in terminal):** `mkdir -p ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts` then retry Step 1.

**`activate_license` not found, or MCP "failed to reconnect (-32000)"** — the loader was installed onto a **different Python interpreter** than the one Claude Code launches (the classic bare-`python` mismatch on Linux/Mac). Check · (in terminal):
```bash
/usr/bin/python3 -c "import memstack_skill_loader; print('ok')"
```
If it prints `ok`, make sure Step 3 registered that exact path, then fully restart Claude Code. If it errors with `ModuleNotFoundError`, reinstall onto the explicit interpreter and re-register against that same path · (in terminal):
```bash
/usr/bin/python3 -m pip install memstack-skill-loader --break-system-packages
claude mcp add --scope user memstack-skills -- /usr/bin/python3 -m memstack_skill_loader
```
Then fully restart Claude Code. Rule of thumb: whatever interpreter you `import`-check as `ok` is the path that must appear in your `claude mcp add` command.

**`No module named pip` (during Step 2)** — that interpreter ships without pip (common on minimal Debian/Ubuntu server images). Install it, then retry the Step 2 install · (in terminal):
```bash
sudo apt install python3-pip
```

### Tier Structure

| Tier | Skills | Access |
|------|--------|--------|
| **Free** | 85 skills | Included with MemStack™ base |
| **Pro** | 130 total (86 free + 44 Pro-exclusive) | Requires Pro Skill Loader ([memstack.pro](https://memstack.pro)) |

**Architecture note:** Pro skills are license-gated — when you activate a valid Pro key, the loader downloads them from our server to `~/.memstack/pro-skills`. Free users see free skills only; Pro license holders unlock the full catalog. This design keeps a single source codebase with no separate repos or branches for Pro content.

<!-- BEGIN GENERATED PRO LIST -->
**Pro-exclusive skills (44):** `advanced-security`, `api-docs`, `api-load-tester`, `branching`, `browser-use`, `burn`, `checkpoint`, `claude-api-helper`, `codebase-index`, `config-audit`, `consolidate`, `context-db`, `council`, `database-architect`, `database-migration`, `dependency-auditor`, `developer-growth-analysis`, `diagram-generator`, `doc-index`, `drift-detection`, `env-manager-pro`, `error-handler`, `frontend-design`, `git-worktrees`, `governor-pro`, `gtm-validator`, `hooks-integration`, `ios-app-store`, `log-analyzer`, `mcp-builder`, `meeting-insights-analyzer`, `model-router`, `multi-agent`, `nextjs-conventions`, `performance-profiler`, `python-conventions`, `rag-builder`, `session-restore`, `social-media`, `test-generator`, `us-privacy-compliance`, `video-pipeline`, `video-review`, `web-scraper` — these require an active Pro license.
<!-- END GENERATED PRO LIST -->

**New skill rule:** All newly added skills default to Pro-exclusive. After 90 days, they drop to the free tier unless marked permanent-Pro.

### Unlock Pro Skills

Complete the **Install** steps above first (marketplace + engine). Then, in Claude Code, ask Claude to run:

```
activate_license(key="your-key", email="you@example.com")
```

Pro skills download automatically from our server to `~/.memstack/pro-skills` — there is **no** separate marketplace step for Pro. Your key is saved permanently — no environment variables needed.

> **Alternative:** You can also set `MEMSTACK_PRO_LICENSE_KEY` as an environment variable instead of using `activate_license`. Use `setx` on Windows or add to `~/.bashrc` on Mac/Linux, then restart your terminal and Claude Code.

### Updating

MemStack updates through three independent channels — refresh whichever you need, then restart Claude Code:

**1. Free skills** (including newly released ones) — in Claude Code:
```
/plugin marketplace update cwinvestments-memstack
```
then `/reload-plugins` (or restart Claude Code).

*Fallback:* if a new skill doesn't appear (marketplace version-detection can be unreliable), re-run `/plugin install memstack@cwinvestments-memstack`. As a last resort, clear the cached plugin and reinstall it.

**2. Pro skills** — auto-update within 24 hours. To force an immediate re-download, ask Claude to run the `refresh_pro_skills` tool.

**3. Engine** (the skill loader itself) — in your terminal:
```bash
pip install --upgrade memstack-skill-loader
```

## Free Base (Included)

Everything from [MemStack free](https://github.com/cwinvestments/memstack):
- SQLite-backed persistent memory with semantic vector search
- Deterministic hooks (commit safety, build verification, secret scanning)
- 17 core skills (Echo, Diary, Work, Forge, Scan, Governor, etc.)
- TTS voice notifications (task complete, needs attention, error alerts)
- TokenStack™ context compression
- Always-on rules and slash commands

## All Skills (130 total — 86 free + 44 Pro-exclusive)

All 130 skills are **fully implemented** with complete protocols, context guards, activation messages, and level history. Skills load on-demand via the MCP catalog system — only the skill matching your current task is loaded, preventing context bloat. 44 Pro-exclusive skills require an active license key. Get a key at [memstack.pro](https://memstack.pro).

<!-- BEGIN GENERATED SKILLS CATALOG -->
### Core (16 — 7 free + 9 Pro)

| Skill | Description |
|-------|-------------|
| `compress` | Monitor and manage TokenStack™ context compression for Claude Code sessions, tracking proxy status and token savings. |
| `diary` | Save a structured session diary capturing what was built, decisions made, and next steps at the end of a productive session. |
| `echo` | Recall information from past Claude Code sessions using semantic vector search when referencing previous work. |
| `goal` | Structure a task into TASK, WHY, OUTCOME, CONSTRAINTS, and a required VERIFICATION criterion before execution begins, so 'done' is defined and provable up front. |
| `grimoire` | Manage and update CLAUDE.md files across all projects after significant changes. |
| `sight` | Generate Mermaid diagrams showing project architecture, schema, and data flow for a visual overview of code structure. |
| `token-optimization` | Enable and understand TokenStack™, the built-in compression proxy that shrinks Claude Code tool output before it reaches the Anthropic API, covering how to turn it on, the free and Pro transforms, and how to read token savings on the dashboard. |
| `burn` **[PRO]** | Track Claude Code token consumption, API spend, and context-window usage with per-session logs, per-project rollups, and monthly budget alerts. |
| `checkpoint` **[PRO]** | Capture state and context before risky changes so you can roll back if things go wrong, creating structured save points with decision context and file states. |
| `consolidate` **[PRO]** | Compress a week of diary entries into actionable insights and cross-project pattern summaries. |
| `context-db` **[PRO]** | Store and query structured project knowledge in a per-project SQLite database, reducing token usage by returning only relevant facts instead of reading full CLAUDE.md. |
| `council` **[PRO]** | Run a structured multi-perspective debate with four voices analyzing tradeoffs before making significant technical decisions. |
| `governor-pro` **[PRO]** | Enforce discipline guardrails for agentic coding: think before coding, no sycophancy, no infinite loops, verify before claiming done. |
| `model-router` **[PRO]** | Route tasks to the right AI model based on complexity, cost, and speed requirements, saving money without sacrificing quality where it matters. |
| `multi-agent` **[PRO]** | Orchestrate multiple Claude Code instances as a coordinated team where a Manager delegates, a Builder implements, and a Reviewer verifies. |
| `session-restore` **[PRO]** | Create structured snapshots capturing decisions, context, and next actions for seamless cross-session continuity and handoffs. |

### Security (12 — 8 free + 4 Pro)

| Skill | Description |
|-------|-------------|
| `api-audit` | Audit Next.js API routes for authentication, authorization, input validation, and common vulnerabilities with a prioritized findings report. |
| `csp-headers` | Audit existing security headers, identify overly permissive directives, and generate a production-ready Content-Security-Policy with companion headers. |
| `dependency-audit` | Scan project dependencies for vulnerabilities, outdated packages, abandoned libraries, and supply chain risks with a prioritized upgrade plan. |
| `git-guard` | Install or verify machine-wide secret-blocking on a repo by confirming the global pre-commit hook, .gitignore coverage, a non-neutered gitleaks config, and a reachable gitleaks binary. |
| `owasp-top10` | Audit a web application against the OWASP Top 10 (2021) vulnerability categories with actionable findings and remediation steps. |
| `rls-checker` | Audit Supabase Row Level Security policies across all tables in a project to verify table-level access control. |
| `rls-guardian` | Enforce Row Level Security on every Supabase table creation, ensuring no table goes live without proper access policies, with migration templates and pre-commit checks. |
| `secrets-scanner` | Scan a codebase for hardcoded secrets, leaked API keys, and credential exposure across files and git history. |
| `advanced-security` **[PRO]** | Perform deep security analysis covering authentication, authorization, input validation, API security, dependency CVEs, and infrastructure hardening with proof-of-concept examples and remediation guides. |
| `config-audit` **[PRO]** | Scan Claude Code project configuration (.claude/, hooks, MCP servers, .gitignore, .env) for secrets, dangerous patterns, and misconfigurations before they cause problems. |
| `dependency-auditor` **[PRO]** | Perform deep dependency analysis covering CVE vulnerabilities, license compatibility, unused packages, version freshness, and safe update paths. |
| `env-manager-pro` **[PRO]** | Sync .env files with code, manage multi-environment configs, detect secrets in git, handle rotation workflows, and generate env documentation. |

### Deployment (8 — 7 free + 1 Pro)

| Skill | Description |
|-------|-------------|
| `ci-cd-pipeline` | Detect the project type and generate a complete CI/CD pipeline with lint, test, build, and deploy stages plus rollback strategy and environment management. |
| `docker-setup` | Analyze a project and generate optimized Dockerfiles, docker-compose configs, and deployment-ready container setups with health checks and volume management. |
| `domain-ssl` | Validate DNS records, SSL certificates, redirects, HSTS, and domain health across all managed properties. |
| `hetzner-setup` | Provision a Hetzner Cloud server with security hardening, reverse proxy, SSL, database setup, monitoring, and automated backups. |
| `marketplace-submit` | Submit skills, plugins, or tools to community marketplaces via pull request with a step-by-step guide. |
| `netlify-deploy` | Validate build config, redirects, environment variables, and deployment readiness for Netlify static/SPA hosting. |
| `railway-deploy` | Validate project configuration, environment variables, and deployment readiness before pushing a Node.js, Python, or Docker application to Railway. |
| `ios-app-store` **[PRO]** | Follow a step-by-step checklist for submitting apps to the Apple App Store, covering pre-submission, common rejections, Capacitor/React Native specifics, and metadata optimization. |

### Development (37 — 16 free + 21 Pro)

| Skill | Description |
|-------|-------------|
| `api-designer` | Produce production-ready Next.js App Router API routes with auth guards, Zod validation, typed responses, and consistent error handling. |
| `changelog-generator` | Generate a formatted CHANGELOG.md from git commit history, grouped by type and ready for release. |
| `code-reviewer` | Conduct a systematic code review across security, performance, maintainability, error handling, testing, and accessibility with severity-ranked findings and specific fixes. |
| `familiar` | Break large tasks into coordinated Claude Code session prompts for parallel execution across multiple instances. |
| `forge` | Create new MemStack skills or improve existing ones with proper structure and progressive disclosure. |
| `mentor` | Narrate decisions, tradeoffs, and reasoning in plain language as you build, so the user learns by working alongside you. |
| `migration-planner` | Plan safe database schema migrations with zero-downtime strategies, rollback procedures, data validation checkpoints, and version tracking. |
| `performance-audit` | Identify and prioritize performance bottlenecks across frontend, backend, and network layers with measured impact and fix priority. |
| `project` | Save and restore project state between Claude Code sessions for seamless handoffs when context is running low. |
| `refactor-planner` | Identify code smells, assess refactoring risk, select appropriate patterns, and build incremental execution plans with rollback strategies and verification checkpoints. |
| `shard` | Split monolithic files into focused, maintainable modules when working with files over 1000 lines. |
| `state` | Maintain a living document of where you are right now in a project, loading current context at session start. |
| `test-writer` | Generate comprehensive test suites with unit, integration, and e2e tests, proper mocking strategies, edge case coverage, naming conventions, and CI integration patterns. |
| `verify` | Review completed work against requirements before committing to ensure nothing was missed. |
| `webapp-testing` | Produce Playwright end-to-end tests that verify real user flows in a browser for web application QA. |
| `work` | Track tasks, manage plans, and survive Claude Code compacts with three operating modes for staying organized across sessions. |
| `api-docs` **[PRO]** | Fetch current API documentation via Context Hub before writing code that calls external APIs, ensuring code targets the latest API surface instead of stale training data. |
| `api-load-tester` **[PRO]** | Design and run load tests to measure API throughput, find bottlenecks under stress, and validate scalability using tools like k6 and Artillery. |
| `branching` **[PRO]** | Enforce a dev-branch workflow where all work happens on dev and merges to master only after review. |
| `claude-api-helper` **[PRO]** | Generate correct Anthropic API integration code for Python and TypeScript covering messages, streaming, tool use, batches, vision, and prompt caching with proper error handling. |
| `codebase-index` **[PRO]** | Generate compact markdown index files from the codebase so Claude Code can skip the exploration phase, saving approximately 50K tokens per session. |
| `database-architect` **[PRO]** | Produce production-ready Supabase/Postgres schemas with proper naming, relationships, RLS policies, indexes, and migration SQL. |
| `database-migration` **[PRO]** | Execute production-grade database migrations for PostgreSQL/Supabase with zero-downtime DDL, rollback strategies, data backfills, and Supabase-specific workflows. |
| `developer-growth-analysis` **[PRO]** | Analyze Claude Code session history and diary entries to surface coding patterns, identify growth areas, and generate a personalized development report. |
| `diagram-generator` **[PRO]** | Generate architecture diagrams, ERDs, flowcharts, and sequence diagrams from natural language, code, or project context in Mermaid, Excalidraw, or SVG format. |
| `doc-index` **[PRO]** | Ingest external documentation from URLs or local directories into a hybrid vector+keyword index for instant retrieval, so Claude Code answers from current docs instead of stale training data. |
| `drift-detection` **[PRO]** | Validate project documentation against the actual codebase, catching stale references, missing env vars, phantom dependencies, and broken instructions. |
| `error-handler` **[PRO]** | Generate standardized error handling patterns including retry logic, circuit breakers, error boundaries, structured error responses, and custom error classes. |
| `frontend-design` **[PRO]** | Apply opinionated frontend conventions for Next.js + Tailwind + shadcn/ui projects, covering component patterns, responsive layouts, and professional UI that ships on the first pass. |
| `git-worktrees` **[PRO]** | Manage git worktrees for isolated parallel development with separate directories per branch or agent, including sync and cleanup automation. |
| `log-analyzer` **[PRO]** | Parse application logs, detect error patterns, trace root causes, and generate fix recommendations, turning walls of log text into actionable insights. |
| `mcp-builder` **[PRO]** | Scaffold complete MCP server projects with tool definitions, testing, and registration to wrap any API, database, or service as MCP tools. |
| `nextjs-conventions` **[PRO]** | Apply Next.js 14+ App Router conventions for file-based routing, server/client component boundaries, data fetching, API routes, middleware, and environment variables. |
| `performance-profiler` **[PRO]** | Identify performance bottlenecks, memory leaks, and optimization opportunities through static analysis of code, queries, and bundle composition. |
| `python-conventions` **[PRO]** | Apply Python 3.10+ best practices for production code including project structure, type hints, error handling, FastAPI/Flask patterns, CLI design, and dependency management. |
| `rag-builder` **[PRO]** | Guide construction of a Retrieval-Augmented Generation system covering document ingestion, embedding, vector storage, and retrieval-augmented prompting. |
| `test-generator` **[PRO]** | Auto-generate comprehensive test suites from existing code covering happy path, edge cases, error scenarios, and boundary conditions using the project's test framework. |

### Business (15 — 13 free + 2 Pro)

| Skill | Description |
|-------|-------------|
| `client-onboarding` | Produce a complete client onboarding package with welcome email, intake questionnaire, kickoff meeting agenda, access provisioning checklist, and check-in schedule. |
| `contract-template` | Generate service agreement, NDA, and subcontractor templates with scope, payment, IP ownership, confidentiality, termination, and liability clauses. |
| `financial-model` | Build monthly revenue projections, expense forecasts, unit economics (CAC, LTV, payback), break-even analysis, cash flow tracking, and scenario modeling. |
| `freelancer-toolkit` | Produce time tracking sheets, invoice calculations, and project analytics for freelancers managing multiple clients and billable hours. |
| `gdpr` | Scan a repository for personal data collection, classify sensitivity under GDPR, determine whether GDPR applies, and report required roles, obligations, and remediation. |
| `governor` | Enforce tier-appropriate complexity and prevent over-engineering by matching project maturity to appropriate scope and patterns. |
| `invoice-generator` | Generate professional invoices with line items, tax calculations, payment terms, due dates, and payment instructions as structured markdown ready for PDF conversion. |
| `licensing` | Scan a repository for every license that touches the product (deps, vendored code, fonts, assets), then produce a per-package verdict table for commercial use readiness. |
| `proposal-writer` | Generate a professional project proposal with executive summary, deliverables, tiered pricing, timeline, and terms ready to send as PDF or email. |
| `quill` | Generate professional client quotations and proposals with itemized pricing and terms. |
| `scan` | Analyze a project's codebase complexity and generate pricing recommendations for freelance or consulting engagements. |
| `scope-of-work` | Generate a formal Scope of Work document with objectives, deliverables, acceptance criteria, in/out scope definitions, work breakdown structure, and milestones. |
| `sop-builder` | Generate a structured Standard Operating Procedure with numbered steps, prerequisites, decision points, verification checkpoints, rollback steps, and time estimates. |
| `meeting-insights-analyzer` **[PRO]** | Extract decisions, action items, key insights, and behavioral patterns from meeting transcripts or notes. |
| `us-privacy-compliance` **[PRO]** | Provide an actionable implementation checklist for US state privacy laws (CCPA/CPRA + 13 other states) covering consent, deletion, and data rights in web apps. |

### Content (10 — 9 free + 1 Pro)

| Skill | Description |
|-------|-------------|
| `blog-post` | Produce a complete, publish-ready blog post with SEO metadata, structured sections, readability optimization, and internal linking suggestions. |
| `email-sequence` | Produce a complete multi-email sequence with subject lines, preview text, body copy, CTAs, and A/B test suggestions ready to load into any email platform. |
| `humanize` | Remove AI tells and rewrite content to sound like a human wrote it, making text feel natural rather than machine-generated. |
| `landing-page-copy` | Produce structured landing page copy blocks (hero, problem, solution, features, social proof, FAQ, CTA) ready to drop into any template or design. |
| `newsletter` | Produce an email newsletter edition with subject line formulas, section structure, personalization, link placement strategy, growth tactics, and engagement optimization. |
| `product-description` | Create conversion-optimized product descriptions with feature-to-benefit conversion, sensory language, SEO keywords, and platform-specific formats for Amazon, Shopify, and Etsy. |
| `tiktok-script` | Create timestamped scripts for TikTok, Reels, and Shorts (15-60 seconds) with hook-in-first-2-seconds, visual cues, caption text, trending audio strategy, and hashtag research. |
| `twitter-thread` | Create multi-tweet threads (5-15 posts) with hook formulas, narrative arc, engagement tactics, data points, CTA placement, and scheduling strategy. |
| `youtube-script` | Produce a timestamped video script with hook, retention techniques, visual directions, SEO metadata, and thumbnail concept optimized for YouTube's algorithm. |
| `social-media` **[PRO]** | Create cross-platform organic social media posts for developers and solo founders who need to promote products without sounding like a marketing robot. |

### SEO & GEO (6 skills)

| Skill | Description |
|-------|-------------|
| `ai-search-visibility` | Evaluate and optimize content for citation by AI search engines like ChatGPT, Perplexity, Google AI Overview, and Claude by checking crawler access, content structure, llms.txt, and AI-friendly patterns. |
| `keyword-research` | Analyze a niche, existing content, and competitor landscape to produce a prioritized keyword map with search intent, difficulty estimates, and page assignments. |
| `local-seo` | Evaluate Google Business Profile, NAP consistency, local schema markup, location pages, citations, and review management to produce an actionable local SEO scorecard. |
| `meta-tag-optimizer` | Scan all pages for existing meta tags, identify issues, and generate optimized replacements for titles, descriptions, Open Graph, canonical URLs, and robots directives. |
| `schema-markup` | Identify applicable schema types, generate valid JSON-LD blocks, and verify against Google's Rich Results requirements ready to paste into page head. |
| `site-audit` | Scan every page for meta tags, heading hierarchy, broken links, image optimization, Core Web Vitals, robots/sitemap, performance, and structured data to produce a prioritized fix list. |

### Marketing (9 — 8 free + 1 Pro)

| Skill | Description |
|-------|-------------|
| `competitor-analysis` | Produce a structured competitive analysis covering pricing, features, positioning, traffic sources, and weaknesses as a comparison matrix with strategic recommendations. |
| `facebook-ad` | Create complete Facebook/Meta ad campaigns with audience targeting, ad copy variations, creative direction, budget allocation, and A/B testing protocols. |
| `google-ad` | Design Google Ads search and display campaigns with keyword groups, bidding strategy, responsive search ads, ad extensions, and Quality Score optimization. |
| `launch-plan` | Develop a day-by-day launch timeline with pre-launch buildup, launch week execution, post-launch optimization, channel strategy, and PR outreach templates. |
| `lead-magnet` | Create a lead magnet with format selection, content outline, landing page copy, email capture integration, delivery sequence, and nurture follow-up. |
| `pricing-strategy` | Design pricing tiers using cost-plus, value-based, and competitor-based models with psychology triggers, tier structure templates, and A/B test plans. |
| `sales-funnel` | Map the complete customer journey across TOFU/MOFU/BOFU stages with page templates, copy hooks, conversion targets, and optimization checklists. |
| `webinar-script` | Produce a full timestamped webinar script with hook, teaching segments, offer transition, Q&A handling, CTA placement, slide suggestions, and replay follow-up email sequence. |
| `gtm-validator` **[PRO]** | Simulate buyer reactions to pricing, messaging, and positioning to find weak spots before spending money on ads or launching publicly. |

### Product (6 skills)

| Skill | Description |
|-------|-------------|
| `feature-spec` | Create a detailed specification for a single feature including user story, acceptance criteria, user flows, edge cases, API definitions, dependencies, and effort estimate. |
| `feedback-analyzer` | Categorize, score, and prioritize customer feedback from support tickets, reviews, and surveys into actionable reports with feature request rankings and sentiment trends. |
| `mvp-scoper` | Define the smallest buildable product that validates a core hypothesis using feature triage, effort/impact scoring, a 2-week sprint scope, and success criteria. |
| `prd-writer` | Generate a complete engineering-ready PRD with problem statement, user personas, functional and non-functional requirements, MoSCoW prioritization, and success metrics. |
| `roadmap-builder` | Create a strategic product roadmap in Now/Next/Later format with quarterly themes, milestones, dependency mapping, resource allocation, and stakeholder communication templates. |
| `user-story-generator` | Produce prioritized user stories with Given/When/Then acceptance criteria, story point estimates, story mapping across epics, and MoSCoW prioritization for sprint planning. |

### Automation (11 — 6 free + 5 Pro)

| Skill | Description |
|-------|-------------|
| `api-integration` | Build system-to-system connectors with REST/GraphQL patterns, authentication flows (OAuth, API key, JWT), rate limit handling, data mapping, error recovery with circuit breakers, and sync monitoring. |
| `content-pipeline` | Automate end-to-end content workflows from ideation through draft, review, approval, cross-platform formatting, scheduling, and publishing with CMS integration. |
| `cron-scheduler` | Build production-grade scheduled jobs with cron syntax, timezone handling, overlap prevention, health checks, monitoring, alerting, and structured logging. |
| `hosted-mcp-catalog` | Discover zero-setup hosted MCP servers that require no API keys or local install, providing a reference catalog of immediately usable MCP tools. |
| `n8n-workflow-builder` | Design visual n8n workflows with trigger selection, node mapping, data transformations, error handling, and webhook integration. |
| `webhook-designer` | Create secure webhook handlers with endpoint design, payload validation, HMAC signature verification, retry logic, idempotency, logging, and dead letter queues. |
| `browser-use` **[PRO]** | Automate browser interactions for QA testing, deploy verification, form filling, and link checking using Playwright from within Claude Code. |
| `hooks-integration` **[PRO]** | Bridge MemStack skills into Claude Code's native hooks system, auto-triggering skills on session start, file changes, commits, and context compaction events. |
| `video-pipeline` **[PRO]** | Design an n8n + AI automated pipeline for video content covering ideation, scripting, asset generation, assembly, and publishing to YouTube. |
| `video-review` **[PRO]** | Download a video (YouTube, Loom, TikTok, X, Instagram, Vimeo, or local file), extract frames, and pull a transcript so Claude can review a demo, UI walkthrough, or content clip grounded in what is on screen and in the audio. |
| `web-scraper` **[PRO]** | Extract structured data from websites including text, tables, links, and images with pagination handling, rate limiting, and robots.txt compliance. |
<!-- END GENERATED SKILLS CATALOG -->

## Pro Templates

### Starter Templates (8)

| Template | Description |
|----------|-------------|
| `nextjs-supabase` | Next.js + Supabase full-stack starter |
| `react-node-postgres` | React + Node.js + PostgreSQL starter |
| `saas-starter` | SaaS boilerplate with auth, billing, dashboard |
| `landing-page` | Marketing landing page with conversion optimization |
| `api-backend` | REST/GraphQL API backend starter |
| `chrome-extension` | Chrome extension with Manifest V3 |
| `electron-app` | Desktop app with Electron |
| `mobile-react-native` | Mobile app with React Native |

### Utility Templates (3)

| Template | Description |
|----------|-------------|
| `client-quote` | Client quotation document (used by Quill skill) |
| `handoff` | Session handoff document (used by Diary skill) |
| `project-snapshot` | Project status snapshot |

## Key Features

- **On-demand loading**: Skills load from the catalog only when matched — no context bloat from 130 skills
- **TTS notifications**: Voice alerts when tasks complete, questions need attention, or errors occur
- **Pre-prompt alerts**: "Claude needs your attention" plays BEFORE approval prompts so you know to return to the terminal
- **Diary webhook**: Session logs auto-POST to n8n webhook for devlog automation
- **PostToolUse observation capture**: Auto-logs every file write and bash command to `.claude/observations/` with timestamps and parsed summaries
- **SessionStart context injection**: Injects last 3 diary + observation summaries into `.claude/session-context.md` at session start for instant recall
- **TokenStack™ integration**: Context compression proxy for token savings

## Installation

The recommended install is via PyPI (see Install section above).

For manual setup or advanced configuration, see [GETTING-STARTED.md](GETTING-STARTED.md).

## Dashboard

MemStack includes a localhost dashboard for managing skills, monitoring token usage, and running multi-agent tasks.

```bash
pip install memstack-skill-loader
python -m memstack_skill_loader dashboard
```

Then open [http://localhost:3333](http://localhost:3333).

| Page | Description |
|------|-------------|
| **Overview** | Skill fire stats, recent projects, session diary |
| **Skills Manager** | Toggle skills on/off, set modes |
| **Burn Report** | Token usage analytics |
| **Memory Browser** | Browse project memories |
| **Agent Monitor** | Launch 3-agent tasks (Manager/Builder/Reviewer) with real-time streaming |
| **Settings** | Agent names, model selection, MCP tools defaults, profile |

The dashboard is free for all users. Pro skills require a [license](https://memstack.pro).

## License

MIT — see [LICENSE](LICENSE). © 2026 CW Affiliate Investments LLC.
