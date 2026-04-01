# MemStack™

[![Version: 3.3.4](https://img.shields.io/badge/Version-3.3.4-green.svg)](CHANGELOG.md)

The structured skill framework for Claude Code — **81 professional skills** for deployment, security, databases, content, marketing, and more.

Skills activate automatically when you need them. Say "deploy this to Railway" and the right skill loads on demand.

### Quick Install

```bash
git clone https://github.com/cwinvestments/memstack.git
cd memstack
```

Then link to your project — see [GETTING-STARTED.md](GETTING-STARTED.md) for full setup instructions.

### Tier Structure

| Tier | Skills | Access |
|------|--------|--------|
| **Free** | 77 skills | Included with MemStack™ base |
| **Pro** | 81 total (77 free + 4 exclusive) | Requires `MEMSTACK_PRO_LICENSE_KEY` |

**Pro-exclusive skills:** `consolidate`, `context-db`, `api-docs`, `branching` — these require an active Pro license.

**New skill rule:** All newly added skills default to Pro-exclusive. After 90 days, they drop to the free tier unless marked permanent-Pro.

**License key:** Set `MEMSTACK_PRO_LICENSE_KEY` as an environment variable or store it in `~/.memstack/license.json`. A SessionStart hook will nudge you to set up your license key if it's missing.

## Free Base (Included)

Everything from [MemStack free](https://github.com/cwinvestments/memstack):
- SQLite-backed persistent memory with semantic vector search
- Deterministic hooks (commit safety, build verification, secret scanning)
- 17 core skills (Echo, Diary, Work, Forge, Scan, Governor, etc.)
- TTS voice notifications (task complete, needs attention, error alerts)
- Headroom context compression proxy auto-start
- Always-on rules and slash commands

## All Skills (81 total — 77 free + 4 Pro-exclusive)

All 81 skills are **fully implemented** with complete protocols, context guards, activation messages, and level history. Skills load on-demand via the MCP catalog system — only the skill matching your current task is loaded, preventing context bloat. 4 skills (consolidate, context-db, api-docs, branching) are Pro-exclusive and require an active license key. Get a key at [memstack.pro](https://memstack.pro).

### Core (20 skills)

| Skill | Description |
|-------|-------------|
| `diary` | Session logging with git integration and SQLite storage |
| `echo` | Past session recall via semantic vector search + SQLite |
| `work` | Task planning and todo list management |
| `state` | Load and update project context at session start |
| `project` | Save project state and handoff context |
| `verify` | Verification before committing completed work |
| `governor` | Project maturity assessment and complexity budgeting |
| `grimoire` | Update project context files after significant changes |
| `compress` | Headroom proxy status and token savings |
| `token-optimization` | Full 3-layer token stack: Headroom + RTK + Serena |
| `humanize` | Make AI-generated text sound natural |
| `forge` | Create new MemStack™ skills |
| `familiar` | Dispatch work across parallel CC sessions |
| `scan` | Codebase complexity analysis and project estimation |
| `quill` | Generate client-facing price quotations |
| `shard` | Split and manage files over 1000 lines |
| `sight` | Visual diagrams and architecture overviews |
| `consolidate` | Weekly cross-project summaries and pattern detection |
| `context-db` | SQLite-backed facts database — query project knowledge instead of full CLAUDE.md |
| `api-docs` | Fetch current API docs via Context Hub before writing API code |

### Security (7 skills)

| Skill | Description |
|-------|-------------|
| `rls-checker` | Supabase Row Level Security policy verification |
| `rls-guardian` | RLS enforcement on new/altered database tables |
| `api-audit` | API endpoint protection verification |
| `owasp-top10` | Comprehensive web security review against OWASP Top 10 |
| `secrets-scanner` | Exposed secrets detection in source code |
| `dependency-audit` | Vulnerability scanning and abandoned package detection |
| `csp-headers` | HTTP security headers (CSP, HSTS, X-Frame-Options) |

### Deployment (6 skills)

| Skill | Description |
|-------|-------------|
| `railway-deploy` | Application deployment to Railway with env vars and domains |
| `netlify-deploy` | Static site and serverless function deployment to Netlify |
| `docker-setup` | Container optimization with Dockerfile and docker-compose |
| `ci-cd-pipeline` | Automated build, test, and deployment pipelines (GitHub Actions) |
| `domain-ssl` | DNS records, SSL certificates, and custom domain configuration |
| `hetzner-setup` | VPS provisioning, hardening, and deployment |

### Development (7 skills)

| Skill | Description |
|-------|-------------|
| `database-architect` | Supabase/Postgres table structures, relationships, and RLS |
| `api-designer` | RESTful API route design with request/response schemas |
| `code-reviewer` | Structured code quality, security, and performance reviews |
| `test-writer` | Unit, integration, and component tests with mocking |
| `migration-planner` | Safe schema evolution with zero-downtime strategies |
| `performance-audit` | Frontend and backend performance diagnosis and optimization |
| `refactor-planner` | Systematic code improvement and tech debt reduction |

### Business (7 skills)

| Skill | Description |
|-------|-------------|
| `proposal-writer` | Project proposals for client and freelance engagements |
| `scope-of-work` | Project boundaries, deliverables, and acceptance criteria |
| `contract-template` | Professional service contracts with legal clauses |
| `client-onboarding` | Structured onboarding process for new clients |
| `invoice-generator` | Professional invoices with line items and payment instructions |
| `financial-model` | Financial projections with scenario modeling and unit economics |
| `sop-builder` | Step-by-step documentation for repeatable processes |

### Content (8 skills)

| Skill | Description |
|-------|-------------|
| `blog-post` | Long-form written content for blogs and publications |
| `email-sequence` | Multi-email automated campaigns with nurture sequences |
| `landing-page-copy` | Persuasive short-form copy for product landing pages |
| `newsletter` | Newsletter editions with subject lines, content, and growth strategy |
| `product-description` | Conversion-optimized product descriptions for e-commerce |
| `tiktok-script` | Scripts with hooks and visual cues for 15–60s vertical videos |
| `twitter-thread` | Multi-tweet narratives with hooks, data points, and CTAs |
| `youtube-script` | Scripted content for YouTube with hooks, chapters, and CTAs |

### SEO & GEO (6 skills)

| Skill | Description |
|-------|-------------|
| `site-audit` | Website SEO health evaluation |
| `keyword-research` | Target keywords with search volume and difficulty |
| `meta-tag-optimizer` | HTML meta tag optimization for search visibility |
| `schema-markup` | Schema.org structured data (JSON-LD) for rich results |
| `ai-search-visibility` | Content optimization for AI-powered search engines |
| `local-seo` | Local search optimization (Google Business Profile, NAP) |

### Marketing (8 skills)

| Skill | Description |
|-------|-------------|
| `sales-funnel` | Complete customer journey from stranger to repeat buyer |
| `facebook-ad` | Social media ad copy with targeting for Meta platforms |
| `google-ad` | Keyword groups, headlines, and Quality Score optimization |
| `launch-plan` | Day-by-day launch timeline with pre/post checklists |
| `competitor-analysis` | Pricing, feature, and messaging comparisons |
| `pricing-strategy` | Pricing tiers, psychology application, and A/B testing |
| `lead-magnet` | Lead capture assets with landing page copy and nurture sequences |
| `webinar-script` | Timestamped presentation scripts with slide notes |

### Product (6 skills)

| Skill | Description |
|-------|-------------|
| `prd-writer` | Engineering-ready PRD with problem statement and personas |
| `feature-spec` | Detailed feature specifications with user flows and edge cases |
| `user-story-generator` | Prioritized stories with Given/When/Then criteria |
| `mvp-scoper` | Smallest viable build that validates product hypothesis |
| `roadmap-builder` | Strategic planning with themes, milestones, and resources |
| `feedback-analyzer` | Support ticket and review categorization and prioritization |

### Automation (5 skills)

| Skill | Description |
|-------|-------------|
| `n8n-workflow-builder` | Design automated workflows with triggers and data transformations |
| `webhook-designer` | Secure webhook receivers with validation and idempotency |
| `cron-scheduler` | Recurring background jobs with monitoring and failure handling |
| `api-integration` | Build reliable connections between systems via their APIs |
| `content-pipeline` | Automate creation, formatting, and publishing across platforms |

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

- **On-demand loading**: Skills load from the catalog only when matched — no context bloat from 81 skills
- **TTS notifications**: Voice alerts when tasks complete, questions need attention, or errors occur
- **Pre-prompt alerts**: "Claude needs your attention" plays BEFORE approval prompts so you know to return to the terminal
- **Diary webhook**: Session logs auto-POST to n8n webhook for devlog automation
- **PostToolUse observation capture**: Auto-logs every file write and bash command to `.claude/observations/` with timestamps and parsed summaries
- **SessionStart context injection**: Injects last 3 diary + observation summaries into `.claude/session-context.md` at session start for instant recall
- **Headroom integration**: Context compression proxy auto-starts with sessions

## Installation

```bash
git clone https://github.com/cwinvestments/memstack.git
cd memstack
```

Then link to your project and set up the MCP Skill Loader — see [GETTING-STARTED.md](GETTING-STARTED.md) for step-by-step instructions.

## License

Proprietary — CW Affiliate Investments LLC. Not for redistribution.
