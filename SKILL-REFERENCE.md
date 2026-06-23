# MemStack™ — Skill Quick Reference

> **128 skills across 10 categories** (85 free + 43 Pro-exclusive). Say any trigger phrase to activate.
>
> Pro-exclusive skills are marked with **[PRO]**. Requires a Pro license key — activate via Dashboard Settings or `activate_license()` in Claude Code.

---

## Core (21)

| Skill | What It Does | Say This to Activate |
|-------|-------------|----------------------|
| Diary | Logs session accomplishments, decisions, and handoff state to SQLite + markdown | "Save diary" or "Log session" or "Wrapping up" |
| Echo | Searches past sessions using semantic vector search + SQLite for context recall | "What did we do last time?" or "Recall" or "Last session" |
| Work | Manages task plans with per-task status tracking in SQLite | "Plan" or "Todo" or "What's next?" or "Resume plan" |
| State | Maintains a living STATE.md tracking current task, blockers, and next steps | "Update state" or "Project state" or "Where was I?" |
| Project | Saves and restores full project state between sessions for seamless handoffs | "Save project" or "Handoff" |
| Verify | Pre-commit verification — checks build, tests, and requirements before committing | "Verify" or "Check this work" or "Does it pass?" |
| Governor | Portfolio governance with tier system (Prototype/MVP/Production) to prevent over-engineering | "New project" or "What tier?" or "Scope this" |
| Grimoire | Manages and updates CLAUDE.md files across projects after significant changes | "Update context" or "Update claude" or "Save library" |
| Compress | Manages TokenStack™ context compression proxy — status, stats, troubleshooting | "Compression" or "Token savings" or "TokenStack" |
| Humanize | Removes AI writing patterns from text — makes output sound natural and human | "Humanize" or "Clean up writing" or "Make it sound natural" |
| Forge | Creates new MemStack™ skills with proper YAML frontmatter and registration | "Forge this" or "New skill" or "Create enchantment" |
| Familiar | Splits large tasks into coordinated prompts for parallel CC sessions | "Dispatch" or "Send familiar" or "Split task" |
| Scan | Analyzes codebase complexity and estimates project scope for pricing | "Scan project" or "Estimate" or "How much to charge?" |
| Quill | Generates professional client-facing quotation documents | "Create quotation" or "Generate quote" or "Proposal" |
| Shard | Refactors large files (1000+ lines) into smaller, focused modules | "Shard this" or "Split file" |
| Sight | Generates Mermaid architecture diagrams and visual code structure overviews | "Draw" or "Diagram" or "Visualize" or "Architecture" |
| Consolidate | **[PRO]** Cross-project weekly summaries and pattern extraction from diary entries | "Consolidate" or "Weekly summary" or "Cross-project patterns" |
| Context DB | **[PRO]** Lightweight fact store for project context with token-efficient retrieval | "Context-db" or "Fact store" or "Project facts" |
| API Docs | **[PRO]** Fetches current API documentation for libraries to prevent stale knowledge | "Api-docs" or "Fetch docs" or "Current API" |
| Token Optimization | Built-in TokenStack™ compression proxy: enable, free vs Pro transforms, savings | "Token optimization" or "Save tokens" or "TokenStack" |
| Branching | **[PRO]** Dev-branch workflow — all work on dev, merge to master only after review | "Branch" or "Dev branch" or "Merge to master" |

---

## Security (8)

| Skill | What It Does | Say This to Activate |
|-------|-------------|----------------------|
| RLS Checker | Audits Supabase tables for missing or misconfigured Row Level Security policies | "Run an RLS audit" or "Check my database security" |
| RLS Guardian | Enforces RLS policies on every new table — prevents tables going live without access controls | "Create a new table" or triggers on any CREATE TABLE / migration file |
| API Audit | Reviews API endpoints for auth, validation, and authorization gaps | "Audit my API routes" or "Check endpoint security" |
| Secrets Scanner | Scans your codebase and git history for leaked API keys and hardcoded credentials | "Scan for leaked secrets" or "Check for hardcoded keys" |
| OWASP Top 10 | Audits your app against the OWASP Top 10 vulnerability categories with remediation steps | "Run an OWASP audit" or "Check for security vulnerabilities" |
| Dependency Audit | Scans project dependencies for known vulnerabilities, outdated packages, and supply chain risks | "Audit my dependencies" or "Are any packages vulnerable?" |
| CSP Headers | Audits security headers and generates production-ready Content-Security-Policy configs | "Check my security headers" or "Generate a CSP policy" |
| Git-Guard | Installs and verifies a repo's pre-commit secret-blocking setup — global hook, .gitignore coverage, and an armed gitleaks config (it verifies; gitleaks does the scanning) | "Set up git-guard" or "Is this repo protected?" |

## Deployment (6)

| Skill | What It Does | Say This to Activate |
|-------|-------------|----------------------|
| Railway Deploy | Validates config and environment variables for Railway deployment readiness | "Deploy this to Railway" or "Is this ready for Railway?" |
| Netlify Deploy | Validates build config, redirects, and env vars for Netlify static site deployment | "Deploy to Netlify" or "Set up Netlify for this project" |
| Domain & SSL | Validates DNS records, SSL certificates, HSTS, and domain health | "Set up my custom domain" or "Fix my SSL certificate" |
| Hetzner Setup | Provisions a Hetzner VPS with security hardening, reverse proxy, SSL, and monitoring | "Set up a Hetzner server" or "Provision a VPS" |
| CI/CD Pipeline | Detects project type and generates a complete CI/CD pipeline with GitHub Actions | "Set up CI/CD" or "Create a GitHub Actions pipeline" |
| Docker Setup | Generates optimized Dockerfiles and docker-compose configs with health checks | "Dockerize this project" or "Create a Dockerfile" |

## Development (9 free + 1 Pro)

| Skill | What It Does | Say This to Activate |
|-------|-------------|----------------------|
| Database Architect | **[PRO]** Produces production-ready Postgres/Supabase schemas with relationships, indexes, and RLS | "Design the database for this" or "Create a schema" |
| API Designer | Produces Next.js App Router API routes with auth guards, Zod validation, and typed responses | "Design the API for this" or "Plan my endpoints" |
| Code Reviewer | Systematic code review across security, performance, maintainability, and error handling | "Review this code" or "What's wrong with this?" |
| Performance Audit | Identifies and prioritizes performance bottlenecks across frontend, backend, and network | "Why is this slow?" or "Run a performance audit" |
| Refactor Planner | Identifies refactoring targets, assesses risk, and builds incremental execution plans | "Plan a refactor for this" or "Help me clean up this code" |
| Test Writer | Generates unit, integration, and component tests with proper mocking and edge case coverage | "Write tests for this" or "Add test coverage" |
| Migration Planner | Plans safe database schema changes with zero-downtime strategies and rollback plans | "Plan a database migration" or "I need to change this table" |
| Changelog Generator | Generates a formatted CHANGELOG.md from git commit history, grouped by type and release-ready | "Generate a changelog" or "Write release notes" |
| Mentor | Narrates decisions, tradeoffs, and reasoning in plain language as you build so you learn alongside | "Teach me as you go" or "Mentor mode" or "Walk me through this" |
| Webapp Testing | Produces Playwright end-to-end tests that verify real user flows in a browser | "Write browser tests" or "Add an e2e test" or "Test this page" |

## Business (10)

| Skill | What It Does | Say This to Activate |
|-------|-------------|----------------------|
| Proposal Writer | Generates a professional project proposal with deliverables, tiered pricing, and timeline | "Write a proposal for this project" or "Draft a client proposal" |
| SOP Builder | Generates structured Standard Operating Procedures with steps, decision points, and verification | "Create an SOP for this process" or "Document this procedure" |
| Scope of Work | Generates a formal SOW with deliverables, acceptance criteria, and change request process | "Write a scope of work" or "Define the project scope" |
| Invoice Generator | Generates professional invoices with line items, tax calculations, and payment terms | "Generate an invoice" or "Bill this client" |
| Contract Template | Provides service agreements with IP ownership, payment terms, and termination clauses | "Draft a contract" or "Create a service agreement" |
| Client Onboarding | Produces welcome sequences, intake questionnaires, and setup checklists for new clients | "Set up client onboarding" or "Create a welcome sequence" |
| Financial Model | Builds monthly projections with scenario modeling for revenue, cash flow, and runway | "Build a financial model" or "Forecast my revenue" |
| Freelancer Toolkit | Produces time tracking sheets, invoice calculations, and project analytics for freelancers | "Track my billable hours" or "Freelance finances" |
| GDPR | Scans a repo for personal data, classifies sensitivity, and reports GDPR obligations and remediation | "Do I need GDPR for this repo?" or "Run a privacy audit" |
| Licensing | Audits every dependency and asset license into a per-package commercial-use verdict table | "Can I use this commercially?" or "Run a license audit" |

## Content (8)

| Skill | What It Does | Say This to Activate |
|-------|-------------|----------------------|
| Blog Post | Produces a publish-ready blog post with SEO metadata, structured sections, and internal linking | "Write a blog post about..." or "Draft an article on..." |
| Landing Page Copy | Produces structured landing page blocks — hero, problem, solution, features, proof, CTA | "Write landing page copy" or "Draft a sales page" |
| Email Sequence | Produces a multi-email sequence with subject lines, body copy, CTAs, and A/B test suggestions | "Write an email sequence" or "Create a drip campaign" |
| YouTube Script | Produces a timestamped video script with hook, retention techniques, and SEO metadata | "Write a YouTube script" or "Script a video about..." |
| Twitter Thread | Creates multi-tweet threads with hook tweets, data points, and engagement CTAs | "Write a Twitter thread" or "Draft an X thread about..." |
| TikTok Script | Creates short-form video scripts with hooks, visual cues, and captions for 15-60 second videos | "Write a TikTok script" or "Script a Reel about..." |
| Newsletter | Produces email newsletter editions with subject lines, content structure, and growth tactics | "Write a newsletter" or "Draft this week's email digest" |
| Product Description | Creates conversion-optimized product descriptions with benefit-driven headlines | "Write a product description" or "Create an Amazon listing" |

## SEO & GEO (6)

| Skill | What It Does | Say This to Activate |
|-------|-------------|----------------------|
| Site Audit | Scans pages for meta tags, broken links, image optimization, Core Web Vitals, and structured data | "Run an SEO audit" or "Check my site's SEO" |
| Keyword Research | Analyzes your niche and competitors to produce a prioritized keyword map with search intent | "Do keyword research for..." or "Find keywords for my site" |
| Meta Tag Optimizer | Scans pages for meta tag issues and generates optimized titles, descriptions, and OG tags | "Optimize my meta tags" or "Fix my title tags" |
| Schema Markup | Generates valid JSON-LD blocks verified against Google's Rich Results requirements | "Add schema markup" or "Generate structured data" |
| AI Search Visibility | Optimizes content for citation by AI search engines like ChatGPT, Perplexity, and Google AI Overview | "Optimize for AI search" or "Improve my AI visibility" |
| Local SEO | Evaluates Google Business Profile, NAP consistency, local schema, and citation health | "Audit my local SEO" or "Improve my Google Maps ranking" |

## Marketing (9)

| Skill | What It Does | Say This to Activate |
|-------|-------------|----------------------|
| Sales Funnel | Maps the complete customer journey from stranger to repeat buyer with conversion targets | "Design a sales funnel" or "Map my customer journey" |
| Facebook Ad | Creates ad copy with targeting, creative direction, and A/B test plans for Meta Ads Manager | "Write a Facebook ad" or "Create an Instagram ad" |
| Google Ad | Designs keyword groups, headlines, descriptions, and Quality Score optimization for Google Ads | "Write a Google ad" or "Set up a PPC campaign" |
| Launch Plan | Develops a day-by-day launch timeline with pre-launch, launch week, and post-launch tasks | "Plan my product launch" or "Create a go-to-market plan" |
| Competitor Analysis | Provides pricing, feature, and messaging comparisons against competitors | "Analyze my competitors" or "How do I compare to [competitor]?" |
| Pricing Strategy | Designs pricing tiers, applies pricing psychology, and plans A/B price tests | "Help me price this" or "Design my pricing tiers" |
| Lead Magnet | Creates lead capture assets with landing page copy, delivery emails, and nurture sequence | "Create a lead magnet" or "Help me grow my email list" |
| Webinar Script | Produces timestamped presentation scripts with slide notes and replay email sequence | "Write a webinar script" or "Script my live presentation" |
| Marketplace Submit | Step-by-step guide to submit a skill, plugin, or tool to a community marketplace via PR | "Submit to marketplace" or "Publish my skill" |

## Product (6)

| Skill | What It Does | Say This to Activate |
|-------|-------------|----------------------|
| PRD Writer | Generates engineering-ready PRDs with problem statements, personas, and MoSCoW features | "Write a PRD" or "Create product requirements" |
| Feature Spec | Creates detailed feature specifications with user flows, edge cases, and acceptance criteria | "Spec this feature" or "Write a detailed spec for..." |
| User Story Generator | Produces prioritized user stories with Given/When/Then criteria and story point estimates | "Generate user stories" or "Build out the backlog" |
| MVP Scoper | Defines the smallest buildable product that validates your core hypothesis | "Scope the MVP" or "What should I build first?" |
| Roadmap Builder | Creates strategic roadmaps with themes, milestones, and stakeholder-ready views | "Build a product roadmap" or "Plan the next quarter" |
| Feedback Analyzer | Categorizes and prioritizes customer feedback from tickets, reviews, or surveys | "Analyze this feedback" or "What are customers asking for?" |

## Automation (6)

| Skill | What It Does | Say This to Activate |
|-------|-------------|----------------------|
| n8n Workflow Builder | Designs visual n8n workflows with node mapping, data transformations, and error handling | "Build an n8n workflow" or "Automate this with n8n" |
| Webhook Designer | Creates secure webhook handlers with signature verification, retry logic, and dead letter queues | "Design a webhook handler" or "Set up a webhook endpoint" |
| Cron Scheduler | Builds production-grade scheduled jobs with overlap prevention and monitoring | "Set up a cron job" or "Run this every hour" |
| API Integration | Develops system-to-system connectors with auth, rate limiting, and error recovery | "Connect these two APIs" or "Sync data between services" |
| Content Pipeline | Automates end-to-end content workflows from ideation through cross-platform publishing | "Automate my content pipeline" or "Auto-publish across platforms" |
| Hosted MCP Catalog | Reference catalog of zero-setup hosted MCP servers requiring no API keys or local install | "What MCP servers are available?" or "Find an MCP for this" |

---

*MemStack™ v3.5.4 — 128 skills across 10 categories (85 free + 43 Pro-exclusive), one prompt away.*
