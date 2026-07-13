# MemStack™ — Skill Quick Reference

> **130 skills across 10 categories** (86 free + 44 Pro-exclusive). Describe your task and the matching skill activates.
>
> Pro-exclusive skills are marked with **[PRO]**. Requires a Pro license key — activate via Dashboard Settings or `activate_license()` in Claude Code.

---

## Core (16)

| Skill | What It Does | Not For |
|-------|-------------|---------|
| `compress` | Monitor and manage TokenStack™ context compression for Claude Code sessions, tracking proxy status and token savings. | — |
| `diary` | Save a structured session diary capturing what was built, decisions made, and next steps at the end of a productive session. | — |
| `echo` | Recall information from past Claude Code sessions using semantic vector search when referencing previous work. | — |
| `goal` | Structure a task into TASK, WHY, OUTCOME, CONSTRAINTS, and a required VERIFICATION criterion before execution begins, so 'done' is defined and provable up front. | Tracking or updating an existing task list (use work) or step-by-step guidance mid-execution. |
| `grimoire` | Manage and update CLAUDE.md files across all projects after significant changes. | — |
| `sight` | Generate Mermaid diagrams showing project architecture, schema, and data flow for a visual overview of code structure. | — |
| `token-optimization` | Enable and understand TokenStack™, the built-in compression proxy that shrinks Claude Code tool output before it reaches the Anthropic API, covering how to turn it on, the free and Pro transforms, and how to read token savings on the dashboard. | Live proxy status or troubleshooting (use Compress). |
| `burn` **[PRO]** | Track Claude Code token consumption, API spend, and context-window usage with per-session logs, per-project rollups, and monthly budget alerts. | Choosing a model, proxy-level compression, or billing/subscription changes. |
| `checkpoint` **[PRO]** | Capture state and context before risky changes so you can roll back if things go wrong, creating structured save points with decision context and file states. | End-of-session diary, cross-session restore, or git commits. |
| `consolidate` **[PRO]** | Compress a week of diary entries into actionable insights and cross-project pattern summaries. | — |
| `context-db` **[PRO]** | Store and query structured project knowledge in a per-project SQLite database, reducing token usage by returning only relevant facts instead of reading full CLAUDE.md. | Session logging or memory recall. |
| `council` **[PRO]** | Run a structured multi-perspective debate with four voices analyzing tradeoffs before making significant technical decisions. | Simple factual questions, implementation tasks, or debugging. |
| `governor-pro` **[PRO]** | Enforce discipline guardrails for agentic coding: think before coding, no sycophancy, no infinite loops, verify before claiming done. | Tier/scope governance (Prototype/MVP/Production). |
| `model-router` **[PRO]** | Route tasks to the right AI model based on complexity, cost, and speed requirements, saving money without sacrificing quality where it matters. | Building AI applications or configuring providers. |
| `multi-agent` **[PRO]** | Orchestrate multiple Claude Code instances as a coordinated team where a Manager delegates, a Builder implements, and a Reviewer verifies. | — |
| `session-restore` **[PRO]** | Create structured snapshots capturing decisions, context, and next actions for seamless cross-session continuity and handoffs. | Diary logging or project memory. |

---

## Security (12)

| Skill | What It Does | Not For |
|-------|-------------|---------|
| `api-audit` | Audit Next.js API routes for authentication, authorization, input validation, and common vulnerabilities with a prioritized findings report. | Frontend security headers or dependency scanning. |
| `csp-headers` | Audit existing security headers, identify overly permissive directives, and generate a production-ready Content-Security-Policy with companion headers. | API route audits or dependency scanning. |
| `dependency-audit` | Scan project dependencies for vulnerabilities, outdated packages, abandoned libraries, and supply chain risks with a prioritized upgrade plan. | Application-level security or secrets scanning. |
| `git-guard` | Install or verify machine-wide secret-blocking on a repo by confirming the global pre-commit hook, .gitignore coverage, a non-neutered gitleaks config, and a reachable gitleaks binary. | Scanning code or git history for existing secrets. |
| `owasp-top10` | Audit a web application against the OWASP Top 10 (2021) vulnerability categories with actionable findings and remediation steps. | Dependency audits or secret scanning alone. |
| `rls-checker` | Audit Supabase Row Level Security policies across all tables in a project to verify table-level access control. | Non-Supabase projects or writing RLS policies from scratch. |
| `rls-guardian` | Enforce Row Level Security on every Supabase table creation, ensuring no table goes live without proper access policies, with migration templates and pre-commit checks. | General SQL queries or non-schema database tasks. |
| `secrets-scanner` | Scan a codebase for hardcoded secrets, leaked API keys, and credential exposure across files and git history. | Dependency vulnerabilities or RLS auditing. |
| `advanced-security` **[PRO]** | Perform deep security analysis covering authentication, authorization, input validation, API security, dependency CVEs, and infrastructure hardening with proof-of-concept examples and remediation guides. | Basic OWASP scanning or dependency-only audits. |
| `config-audit` **[PRO]** | Scan Claude Code project configuration (.claude/, hooks, MCP servers, .gitignore, .env) for secrets, dangerous patterns, and misconfigurations before they cause problems. | Runtime security scanning, penetration testing, network security, or production monitoring. |
| `dependency-auditor` **[PRO]** | Perform deep dependency analysis covering CVE vulnerabilities, license compatibility, unused packages, version freshness, and safe update paths. | Code quality linting or documentation drift detection. |
| `env-manager-pro` **[PRO]** | Sync .env files with code, manage multi-environment configs, detect secrets in git, handle rotation workflows, and generate env documentation. | Basic env audit or deployment config. |

---

## Deployment (8)

| Skill | What It Does | Not For |
|-------|-------------|---------|
| `ci-cd-pipeline` | Detect the project type and generate a complete CI/CD pipeline with lint, test, build, and deploy stages plus rollback strategy and environment management. | One-time manual deployments. |
| `docker-setup` | Analyze a project and generate optimized Dockerfiles, docker-compose configs, and deployment-ready container setups with health checks and volume management. | Serverless or static site deployments. |
| `domain-ssl` | Validate DNS records, SSL certificates, redirects, HSTS, and domain health across all managed properties. | Full deployment workflows. |
| `hetzner-setup` | Provision a Hetzner Cloud server with security hardening, reverse proxy, SSL, database setup, monitoring, and automated backups. | Managed platform deployments like Railway or Netlify. |
| `marketplace-submit` | Submit skills, plugins, or tools to community marketplaces via pull request with a step-by-step guide. | Building skills or writing plugin code. |
| `netlify-deploy` | Validate build config, redirects, environment variables, and deployment readiness for Netlify static/SPA hosting. | Railway, Vercel, or VPS deployments. |
| `railway-deploy` | Validate project configuration, environment variables, and deployment readiness before pushing a Node.js, Python, or Docker application to Railway. | Netlify, Vercel, or Hetzner deployments. |
| `ios-app-store` **[PRO]** | Follow a step-by-step checklist for submitting apps to the Apple App Store, covering pre-submission, common rejections, Capacitor/React Native specifics, and metadata optimization. | Android/Google Play, web deployment, or app development/coding. |

---

## Development (37)

| Skill | What It Does | Not For |
|-------|-------------|---------|
| `api-designer` | Produce production-ready Next.js App Router API routes with auth guards, Zod validation, typed responses, and consistent error handling. | API security audits or database design. |
| `changelog-generator` | Generate a formatted CHANGELOG.md from git commit history, grouped by type and ready for release. | Diary entries, git log viewing, or commit message writing. |
| `code-reviewer` | Conduct a systematic code review across security, performance, maintainability, error handling, testing, and accessibility with severity-ranked findings and specific fixes. | Refactoring plans or test generation. |
| `familiar` | Break large tasks into coordinated Claude Code session prompts for parallel execution across multiple instances. | — |
| `forge` | Create new MemStack skills or improve existing ones with proper structure and progressive disclosure. | — |
| `mentor` | Narrate decisions, tradeoffs, and reasoning in plain language as you build, so the user learns by working alongside you. | Code review or debugging. |
| `migration-planner` | Plan safe database schema migrations with zero-downtime strategies, rollback procedures, data validation checkpoints, and version tracking. | Initial database design or code refactoring. |
| `performance-audit` | Identify and prioritize performance bottlenecks across frontend, backend, and network layers with measured impact and fix priority. | Code reviews or security audits. |
| `project` | Save and restore project state between Claude Code sessions for seamless handoffs when context is running low. | — |
| `refactor-planner` | Identify code smells, assess refactoring risk, select appropriate patterns, and build incremental execution plans with rollback strategies and verification checkpoints. | Writing new features or database migrations. |
| `shard` | Split monolithic files into focused, maintainable modules when working with files over 1000 lines. | — |
| `state` | Maintain a living document of where you are right now in a project, loading current context at session start. | — |
| `test-writer` | Generate comprehensive test suites with unit, integration, and e2e tests, proper mocking strategies, edge case coverage, naming conventions, and CI integration patterns. | Refactoring plans or database migrations. |
| `verify` | Review completed work against requirements before committing to ensure nothing was missed. | — |
| `webapp-testing` | Produce Playwright end-to-end tests that verify real user flows in a browser for web application QA. | Unit tests, API tests, or non-browser testing. |
| `work` | Track tasks, manage plans, and survive Claude Code compacts with three operating modes for staying organized across sessions. | — |
| `api-docs` **[PRO]** | Fetch current API documentation via Context Hub before writing code that calls external APIs, ensuring code targets the latest API surface instead of stale training data. | Internal project APIs or code explanation. |
| `api-load-tester` **[PRO]** | Design and run load tests to measure API throughput, find bottlenecks under stress, and validate scalability using tools like k6 and Artillery. | Unit testing, code profiling, query optimization, or CDN configuration. |
| `branching` **[PRO]** | Enforce a dev-branch workflow where all work happens on dev and merges to master only after review. | — |
| `claude-api-helper` **[PRO]** | Generate correct Anthropic API integration code for Python and TypeScript covering messages, streaming, tool use, batches, vision, and prompt caching with proper error handling. | Claude Code CLI usage or MCP server development. |
| `codebase-index` **[PRO]** | Generate compact markdown index files from the codebase so Claude Code can skip the exploration phase, saving approximately 50K tokens per session. | One-off file searches or symbol lookups. |
| `database-architect` **[PRO]** | Produce production-ready Supabase/Postgres schemas with proper naming, relationships, RLS policies, indexes, and migration SQL. | Schema migration of existing tables or code refactoring. |
| `database-migration` **[PRO]** | Execute production-grade database migrations for PostgreSQL/Supabase with zero-downtime DDL, rollback strategies, data backfills, and Supabase-specific workflows. | Database design from scratch, query optimization, RLS policies, or ORM setup. |
| `developer-growth-analysis` **[PRO]** | Analyze Claude Code session history and diary entries to surface coding patterns, identify growth areas, and generate a personalized development report. | Code review or debugging. |
| `diagram-generator` **[PRO]** | Generate architecture diagrams, ERDs, flowcharts, and sequence diagrams from natural language, code, or project context in Mermaid, Excalidraw, or SVG format. | ASCII art or text-only representations. |
| `doc-index` **[PRO]** | Ingest external documentation from URLs or local directories into a hybrid vector+keyword index for instant retrieval, so Claude Code answers from current docs instead of stale training data. | Codebase structure mapping or API doc fetching via Context Hub. |
| `drift-detection` **[PRO]** | Validate project documentation against the actual codebase, catching stale references, missing env vars, phantom dependencies, and broken instructions. | Code quality linting or security scanning. |
| `error-handler` **[PRO]** | Generate standardized error handling patterns including retry logic, circuit breakers, error boundaries, structured error responses, and custom error classes. | Debugging existing errors or testing error scenarios. |
| `frontend-design` **[PRO]** | Apply opinionated frontend conventions for Next.js + Tailwind + shadcn/ui projects, covering component patterns, responsive layouts, and professional UI that ships on the first pass. | Backend logic, database design, API routes, or deployment. |
| `git-worktrees` **[PRO]** | Manage git worktrees for isolated parallel development with separate directories per branch or agent, including sync and cleanup automation. | Simple branch switching or stashing. |
| `log-analyzer` **[PRO]** | Parse application logs, detect error patterns, trace root causes, and generate fix recommendations, turning walls of log text into actionable insights. | Real-time monitoring or metrics dashboards. |
| `mcp-builder` **[PRO]** | Scaffold complete MCP server projects with tool definitions, testing, and registration to wrap any API, database, or service as MCP tools. | Consuming existing MCP servers or Claude Code plugin development. |
| `nextjs-conventions` **[PRO]** | Apply Next.js 14+ App Router conventions for file-based routing, server/client component boundaries, data fetching, API routes, middleware, and environment variables. | UI styling, database design, deployment, or React fundamentals without Next.js context. |
| `performance-profiler` **[PRO]** | Identify performance bottlenecks, memory leaks, and optimization opportunities through static analysis of code, queries, and bundle composition. | Runtime monitoring or load testing. |
| `python-conventions` **[PRO]** | Apply Python 3.10+ best practices for production code including project structure, type hints, error handling, FastAPI/Flask patterns, CLI design, and dependency management. | Data science/ML, Jupyter notebooks, Django, or JS/TS projects. |
| `rag-builder` **[PRO]** | Guide construction of a Retrieval-Augmented Generation system covering document ingestion, embedding, vector storage, and retrieval-augmented prompting. | General database setup or API integration. |
| `test-generator` **[PRO]** | Auto-generate comprehensive test suites from existing code covering happy path, edge cases, error scenarios, and boundary conditions using the project's test framework. | Running existing tests or test-driven development. |

---

## Business (15)

| Skill | What It Does | Not For |
|-------|-------------|---------|
| `client-onboarding` | Produce a complete client onboarding package with welcome email, intake questionnaire, kickoff meeting agenda, access provisioning checklist, and check-in schedule. | Contracts or invoicing. |
| `contract-template` | Generate service agreement, NDA, and subcontractor templates with scope, payment, IP ownership, confidentiality, termination, and liability clauses. | Invoicing or client onboarding. |
| `financial-model` | Build monthly revenue projections, expense forecasts, unit economics (CAC, LTV, payback), break-even analysis, cash flow tracking, and scenario modeling. | Pricing strategy or invoice generation. |
| `freelancer-toolkit` | Produce time tracking sheets, invoice calculations, and project analytics for freelancers managing multiple clients and billable hours. | General invoice templates or proposal writing. |
| `gdpr` | Scan a repository for personal data collection, classify sensitivity under GDPR, determine whether GDPR applies, and report required roles, obligations, and remediation. | General security audits or contract drafting. |
| `governor` | Enforce tier-appropriate complexity and prevent over-engineering by matching project maturity to appropriate scope and patterns. | — |
| `invoice-generator` | Generate professional invoices with line items, tax calculations, payment terms, due dates, and payment instructions as structured markdown ready for PDF conversion. | Contracts or financial projections. |
| `licensing` | Scan a repository for every license that touches the product (deps, vendored code, fonts, assets), then produce a per-package verdict table for commercial use readiness. | Vulnerability scanning or contract drafting. |
| `proposal-writer` | Generate a professional project proposal with executive summary, deliverables, tiered pricing, timeline, and terms ready to send as PDF or email. | Contracts, invoices, or onboarding. |
| `quill` | Generate professional client quotations and proposals with itemized pricing and terms. | — |
| `scan` | Analyze a project's codebase complexity and generate pricing recommendations for freelance or consulting engagements. | — |
| `scope-of-work` | Generate a formal Scope of Work document with objectives, deliverables, acceptance criteria, in/out scope definitions, work breakdown structure, and milestones. | Proposals, contracts, or invoicing. |
| `sop-builder` | Generate a structured Standard Operating Procedure with numbered steps, prerequisites, decision points, verification checkpoints, rollback steps, and time estimates. | Project proposals or scope documents. |
| `meeting-insights-analyzer` **[PRO]** | Extract decisions, action items, key insights, and behavioral patterns from meeting transcripts or notes. | Scheduling meetings or writing agendas. |
| `us-privacy-compliance` **[PRO]** | Provide an actionable implementation checklist for US state privacy laws (CCPA/CPRA + 13 other states) covering consent, deletion, and data rights in web apps. | GDPR, HIPAA, PCI-DSS, or SOC 2. |

---

## Content (10)

| Skill | What It Does | Not For |
|-------|-------------|---------|
| `blog-post` | Produce a complete, publish-ready blog post with SEO metadata, structured sections, readability optimization, and internal linking suggestions. | Landing page copy, email sequences, or social media posts. |
| `email-sequence` | Produce a complete multi-email sequence with subject lines, preview text, body copy, CTAs, and A/B test suggestions ready to load into any email platform. | Newsletters or single marketing emails. |
| `humanize` | Remove AI tells and rewrite content to sound like a human wrote it, making text feel natural rather than machine-generated. | — |
| `landing-page-copy` | Produce structured landing page copy blocks (hero, problem, solution, features, social proof, FAQ, CTA) ready to drop into any template or design. | Blog posts or email sequences. |
| `newsletter` | Produce an email newsletter edition with subject line formulas, section structure, personalization, link placement strategy, growth tactics, and engagement optimization. | Lead magnets or content pipelines. |
| `product-description` | Create conversion-optimized product descriptions with feature-to-benefit conversion, sensory language, SEO keywords, and platform-specific formats for Amazon, Shopify, and Etsy. | Pricing strategy or sales funnels. |
| `tiktok-script` | Create timestamped scripts for TikTok, Reels, and Shorts (15-60 seconds) with hook-in-first-2-seconds, visual cues, caption text, trending audio strategy, and hashtag research. | Twitter threads or webinar scripts. |
| `twitter-thread` | Create multi-tweet threads (5-15 posts) with hook formulas, narrative arc, engagement tactics, data points, CTA placement, and scheduling strategy. | TikTok scripts, newsletters, or LinkedIn posts. |
| `youtube-script` | Produce a timestamped video script with hook, retention techniques, visual directions, SEO metadata, and thumbnail concept optimized for YouTube's algorithm. | TikTok/Reels short-form scripts or webinar presentations. |
| `social-media` **[PRO]** | Create cross-platform organic social media posts for developers and solo founders who need to promote products without sounding like a marketing robot. | Email marketing, SEO content, blog writing, paid ads, or graphic design. |

---

## SEO & GEO (6)

| Skill | What It Does | Not For |
|-------|-------------|---------|
| `ai-search-visibility` | Evaluate and optimize content for citation by AI search engines like ChatGPT, Perplexity, Google AI Overview, and Claude by checking crawler access, content structure, llms.txt, and AI-friendly patterns. | Traditional SEO audits or Google Ads. |
| `keyword-research` | Analyze a niche, existing content, and competitor landscape to produce a prioritized keyword map with search intent, difficulty estimates, and page assignments. | Full site audits or ad keyword groups. |
| `local-seo` | Evaluate Google Business Profile, NAP consistency, local schema markup, location pages, citations, and review management to produce an actionable local SEO scorecard. | General SEO audits or national keyword research. |
| `meta-tag-optimizer` | Scan all pages for existing meta tags, identify issues, and generate optimized replacements for titles, descriptions, Open Graph, canonical URLs, and robots directives. | Schema markup or full site audits. |
| `schema-markup` | Identify applicable schema types, generate valid JSON-LD blocks, and verify against Google's Rich Results requirements ready to paste into page head. | Meta tag optimization or full SEO audits. |
| `site-audit` | Scan every page for meta tags, heading hierarchy, broken links, image optimization, Core Web Vitals, robots/sitemap, performance, and structured data to produce a prioritized fix list. | Keyword research or schema markup generation alone. |

---

## Marketing (9)

| Skill | What It Does | Not For |
|-------|-------------|---------|
| `competitor-analysis` | Produce a structured competitive analysis covering pricing, features, positioning, traffic sources, and weaknesses as a comparison matrix with strategic recommendations. | Setting your own pricing strategy. |
| `facebook-ad` | Create complete Facebook/Meta ad campaigns with audience targeting, ad copy variations, creative direction, budget allocation, and A/B testing protocols. | Google search ads or organic social content. |
| `google-ad` | Design Google Ads search and display campaigns with keyword groups, bidding strategy, responsive search ads, ad extensions, and Quality Score optimization. | Facebook/Meta ads or SEO. |
| `launch-plan` | Develop a day-by-day launch timeline with pre-launch buildup, launch week execution, post-launch optimization, channel strategy, and PR outreach templates. | Ongoing funnel design or ad copy alone. |
| `lead-magnet` | Create a lead magnet with format selection, content outline, landing page copy, email capture integration, delivery sequence, and nurture follow-up. | Full funnel design or paid ad copy. |
| `pricing-strategy` | Design pricing tiers using cost-plus, value-based, and competitor-based models with psychology triggers, tier structure templates, and A/B test plans. | Competitor pricing comparison alone. |
| `sales-funnel` | Map the complete customer journey across TOFU/MOFU/BOFU stages with page templates, copy hooks, conversion targets, and optimization checklists. | Ad copy creation or time-bound launch plans. |
| `webinar-script` | Produce a full timestamped webinar script with hook, teaching segments, offer transition, Q&A handling, CTA placement, slide suggestions, and replay follow-up email sequence. | Launch plans or static sales page copy. |
| `gtm-validator` **[PRO]** | Simulate buyer reactions to pricing, messaging, and positioning to find weak spots before spending money on ads or launching publicly. | Actual market research or competitor analysis. |

---

## Product (6)

| Skill | What It Does | Not For |
|-------|-------------|---------|
| `feature-spec` | Create a detailed specification for a single feature including user story, acceptance criteria, user flows, edge cases, API definitions, dependencies, and effort estimate. | Full PRDs or user story backlogs. |
| `feedback-analyzer` | Categorize, score, and prioritize customer feedback from support tickets, reviews, and surveys into actionable reports with feature request rankings and sentiment trends. | Competitor analysis or market research. |
| `mvp-scoper` | Define the smallest buildable product that validates a core hypothesis using feature triage, effort/impact scoring, a 2-week sprint scope, and success criteria. | Full PRDs or roadmap planning. |
| `prd-writer` | Generate a complete engineering-ready PRD with problem statement, user personas, functional and non-functional requirements, MoSCoW prioritization, and success metrics. | Single feature specs or user story backlogs. |
| `roadmap-builder` | Create a strategic product roadmap in Now/Next/Later format with quarterly themes, milestones, dependency mapping, resource allocation, and stakeholder communication templates. | MVP scoping or sprint-level planning. |
| `user-story-generator` | Produce prioritized user stories with Given/When/Then acceptance criteria, story point estimates, story mapping across epics, and MoSCoW prioritization for sprint planning. | Full PRDs or detailed feature specs. |

---

## Automation (11)

| Skill | What It Does | Not For |
|-------|-------------|---------|
| `api-integration` | Build system-to-system connectors with REST/GraphQL patterns, authentication flows (OAuth, API key, JWT), rate limit handling, data mapping, error recovery with circuit breakers, and sync monitoring. | Visual n8n workflows or webhook receiving. |
| `content-pipeline` | Automate end-to-end content workflows from ideation through draft, review, approval, cross-platform formatting, scheduling, and publishing with CMS integration. | Single social media posts or individual blog posts. |
| `cron-scheduler` | Build production-grade scheduled jobs with cron syntax, timezone handling, overlap prevention, health checks, monitoring, alerting, and structured logging. | n8n workflows or event-driven webhooks. |
| `hosted-mcp-catalog` | Discover zero-setup hosted MCP servers that require no API keys or local install, providing a reference catalog of immediately usable MCP tools. | Building MCP servers or configuring local MCP. |
| `n8n-workflow-builder` | Design visual n8n workflows with trigger selection, node mapping, data transformations, error handling, and webhook integration. | Standalone webhook endpoints or cron jobs. |
| `webhook-designer` | Create secure webhook handlers with endpoint design, payload validation, HMAC signature verification, retry logic, idempotency, logging, and dead letter queues. | Full n8n workflows or scheduled tasks. |
| `browser-use` **[PRO]** | Automate browser interactions for QA testing, deploy verification, form filling, and link checking using Playwright from within Claude Code. | Unit testing or API testing. |
| `hooks-integration` **[PRO]** | Bridge MemStack skills into Claude Code's native hooks system, auto-triggering skills on session start, file changes, commits, and context compaction events. | Git hooks or CI/CD webhooks. |
| `video-pipeline` **[PRO]** | Design an n8n + AI automated pipeline for video content covering ideation, scripting, asset generation, assembly, and publishing to YouTube. | Writing individual video scripts or editing videos manually. |
| `video-review` **[PRO]** | Download a video (YouTube, Loom, TikTok, X, Instagram, Vimeo, or local file), extract frames, and pull a transcript so Claude can review a demo, UI walkthrough, or content clip grounded in what is on screen and in the audio. | Producing or publishing videos via n8n automation (use video-pipeline), reviewing source code or PRs, or writing video scripts. |
| `web-scraper` **[PRO]** | Extract structured data from websites including text, tables, links, and images with pagination handling, rate limiting, and robots.txt compliance. | API documentation fetching or browser testing. |

---

*MemStack™ v3.5.4 — 130 skills across 10 categories (86 free + 44 Pro-exclusive), one prompt away.*
