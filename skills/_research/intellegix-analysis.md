# Intellegix Code Agent Toolkit vs MemStack v3.1 — Comparison Report

**Date:** 2026-02-24
**Intellegix version:** Latest (commit from github.com/intellegix/intellegix-code-agent-toolkit)
**MemStack version:** 3.1.0
**Repo:** https://github.com/intellegix/intellegix-code-agent-toolkit
**Author:** Austin Kidwell, Intellegix (San Diego)

---

## Executive Summary

Intellegix is a **heavyweight multi-agent orchestration toolkit** with Perplexity research integration, portfolio governance, and an autonomous loop driver. MemStack is a **lightweight memory + safety framework** with persistent recall, session diaries, and business tools. They overlap on session handoffs and planning, but serve fundamentally different use cases: Intellegix targets teams running autonomous multi-agent pipelines with external research; MemStack targets solo developers who need cross-session memory and workflow safety.

The most valuable patterns to port from Intellegix are: **portfolio governance** (tier/phase constraints that prevent over-engineering), **silent context compilation** (pre-flight state gathering before research), and **MEMORY.md separation from CLAUDE.md** (behavioral rules vs learned patterns). The autonomous loop driver and Perplexity research integration are impressive but outside MemStack's zero-dependency philosophy.

---

## What Each Tool Does

### Intellegix Code Agent Toolkit

An installable `~/.claude/` configuration system providing six capabilities:

- **Automated Loop Driver** — Python script that spawns Claude Code CLI in a loop with budget enforcement, stagnation detection, model fallback (Opus to Sonnet), and session rotation (200 turns or $20/session). Writes state to `.workflow/` directory.
- **15 Slash Commands** — Research (`/research`, `/research-perplexity`, `/automate-perplexity`, `/labs-perplexity`), planning (`/smart-plan`, `/council-refine`, `/council-extract`, `/export-to-council`), development (`/implement`, `/fix-issue`, `/review`), operations (`/handoff`, `/portfolio-status`, `/cache-perplexity-session`, `/ensure-space`).
- **9 Specialized Agents** — Orchestrator (Opus), Architect (Opus), Backend/Frontend/Database/DevOps/Testing/Research (all Sonnet), plus a domain-specific Construction-BI agent.
- **Council Automation** — Multi-model synthesis via Perplexity (GPT-5.2 + Claude Sonnet 4.5 + Gemini 3 Pro) with Opus 4.6 extended thinking for plan synthesis. Browser-based ($0/query) or API-based ($0.06-0.20/query).
- **MCP Browser Bridge** — Chrome MV3 extension + WebSocket bridge + Node.js MCP server for browser automation.
- **Portfolio Governance** — Tier system (T1 Production 60% → T4 Archive 0%) with phase restrictions (Prototype → no tests/CI/auth; Maintenance → bug fixes only).

**Architecture:** Python loop driver → Claude Code CLI subprocess → streams NDJSON → state persistence + budget enforcement. Agents delegate via CC's Task tool. Perplexity research via Playwright browser automation.

**Target user:** Team or agency managing multiple projects with autonomous agent pipelines.

### MemStack v3.1

A prompt-driven skill framework adding persistent memory, safety hooks, and workflow tools to Claude Code:

- **18 skills** — Memory (Echo semantic search, Diary session logging), planning (Work SQLite-backed plans), safety (Verify pre-commit checks), workflow (State live tracking, Humanize writing cleanup), business (Scan pricing, Quill quotations, KDP Format), development (Forge skill creation, Shard refactoring, Sight diagrams), lifecycle (Project handoff, Grimoire CLAUDE.md management)
- **4 deterministic hooks** — Pre-push (build + secrets + commit format), post-commit (debug artifacts), session-start (Headroom + CLAUDE.md indexer), session-end (monitoring)
- **5 always-on rules** — Echo recall, Diary logging, Work planning, global conventions, Headroom awareness
- **SQLite + LanceDB** — Structured memory with full-text search + vector semantic search across all sessions
- **2 slash commands** — `/memstack-search` (memory search), `/memstack-headroom` (proxy stats)

**Architecture:** Markdown skills + SQLite database + LanceDB vectors + shell hooks. No runtime process, no external APIs required. Zero dependencies for core features.

**Target user:** Solo developer using Claude Code across multiple projects who needs persistent memory and workflow safety.

---

## Feature Comparison Matrix

| Capability | Intellegix | MemStack | Notes |
|------------|-----------|----------|-------|
| **Runtime** | Python loop driver + Node.js MCP server | Pure prompt framework + shell hooks | Intellegix requires running processes |
| **Persistent memory** | MEMORY.md files (markdown) | SQLite + LanceDB vectors + markdown | MemStack's is structured and searchable |
| **Cross-session recall** | Manual MEMORY.md reading | Echo semantic + keyword search | MemStack's is automated and ranked |
| **Session diaries** | None | Diary skill (structured logging + insight extraction) | MemStack unique |
| **Session handoffs** | `/handoff` command (structured markdown) | Diary Lv.5 Session Handoff section + Project skill | Both strong, different approaches |
| **Task planning** | `/smart-plan` (4-phase with ADR) | Work skill (SQLite-backed status tracking) | Intellegix is more structured upfront |
| **Plan persistence** | Files only | SQLite (survives context compaction) | MemStack persists across sessions |
| **Agents** | 9 specialized (Orchestrator, Architect, Backend, etc.) | None (Familiar deprecated) | Intellegix far ahead |
| **Multi-agent orchestration** | Orchestrator delegates sequential + concurrent via Task tool | None | Intellegix unique |
| **Autonomous loop** | loop_driver.py with budget/stagnation/fallback | None | Intellegix unique |
| **Research integration** | Perplexity (browser $0/query or API $0.06-0.20) | None | Intellegix unique |
| **Multi-model council** | GPT-5.2 + Claude + Gemini → Opus synthesis | None | Intellegix unique |
| **Portfolio governance** | Tier system (T1-T4) + phase restrictions + anti-patterns | None | Intellegix unique — high value |
| **Commit safety** | Pre-commit checklist in patterns | Pre-push hook (deterministic, blocks push) | MemStack is deterministic |
| **Secrets scanning** | Security checklist (manual) | Pre-push hook (automated grep) | MemStack is automated |
| **Build verification** | Mentioned in patterns | Pre-push hook (enforced) | MemStack is enforced |
| **Code review** | `/review` command (6-step) | None (Verify is pre-commit only) | Intellegix more complete |
| **Pattern references** | 8 pattern files (Python, TS, API, Testing, Security, MCP, Browser) | None (patterns in CLAUDE.md) | Intellegix more organized |
| **Path-scoped rules** | 4 rules with `paths:` frontmatter | 5 rules (no path scoping) | Intellegix more targeted |
| **Browser automation** | Full MCP bridge (Chrome ext + WebSocket + Node.js server) | None | Intellegix unique |
| **Business tools** | None | Scan (pricing), Quill (quotations), KDP Format | MemStack unique |
| **Architecture diagrams** | None | Sight skill (Mermaid generation) | MemStack unique |
| **Code refactoring** | None | Shard skill (auto-split 1000+ LOC files) | MemStack unique |
| **Context compression** | None | Headroom proxy integration (34% savings) | MemStack unique |
| **Semantic vector search** | None | LanceDB + sentence-transformers | MemStack unique |
| **Skill creation** | None | Forge skill (guided creation) | MemStack unique |
| **Writing cleanup** | None | Humanize skill (AI pattern removal) | MemStack unique |
| **Live state tracking** | None | State skill (STATE.md) | MemStack unique |
| **Dependency count** | pydantic, playwright, anthropic, openai, google-generativeai, ws, better-sqlite3, Chrome ext | Zero (core) / lancedb + sentence-transformers (optional) | MemStack far leaner |
| **CI/CD** | 4 GitHub Actions (CI, CodeQL, dependency review, scorecard) | None | Intellegix more professional |
| **Tests** | 220+ (pytest, integration, end-to-end) | None | Intellegix far ahead |

---

## Overlap Analysis

### Shared Concepts

1. **Session handoffs** — Both formalize handoff documents. Intellegix uses `/handoff` (generates structured markdown in `.claude/handoffs/`). MemStack uses Diary's Session Handoff section (in SQLite + markdown). Different storage, same goal.

2. **Task planning** — Intellegix's `/smart-plan` is a 4-phase workflow with ADR creation. MemStack's Work skill tracks tasks in SQLite with status persistence. Intellegix is better at *creating* plans; MemStack is better at *persisting* them across sessions.

3. **MEMORY.md / memory separation** — Both maintain memory files separate from CLAUDE.md. Intellegix uses `~/.claude/agent-memory/{agent}/MEMORY.md` per agent + project MEMORY.md. MemStack uses `~/.claude/projects/<hash>/memory/MEMORY.md` (CC auto-memory) + SQLite + LanceDB vectors. MemStack's is more searchable; Intellegix's is more organized per agent.

4. **Code review** — Intellegix has `/review` (6-step with portfolio compliance). MemStack has no equivalent (Verify is pre-commit verification, not code review).

5. **Rules** — Both use `.claude/rules/` with markdown files. Intellegix adds `paths:` frontmatter for file-type scoping. MemStack's rules are globally scoped.

### No Functional Overlap

| Intellegix Unique | MemStack Unique |
|---|---|
| Autonomous loop driver | SQLite + vector semantic memory |
| Multi-agent orchestration (9 agents) | Cross-session recall (Echo) |
| Perplexity research integration | Session diaries with insight extraction |
| Multi-model council synthesis | Deterministic safety hooks |
| Portfolio governance (tier/phase) | Business tools (Scan, Quill, KDP) |
| MCP browser bridge | Architecture diagrams (Sight) |
| Pattern reference library (8 files) | Context compression (Headroom) |
| Construction industry domain agent | Code refactoring (Shard) |

---

## Patterns Worth Porting to MemStack

### Priority 1: Portfolio Governance (HIGH VALUE)

Intellegix's tier/phase system prevents over-engineering — the #1 waste of time in AI-assisted development. Key concepts:

**Tier system** — forces explicit resource allocation:
| Tier | Effort | What's allowed |
|------|--------|---------------|
| T1 Production | 60% | Full stack, monitoring, CI/CD |
| T2 Strategic | 30% | Active dev, basic testing |
| T3 Experimental | 10% | Working code only, minimal investment |
| T4 Archive | 0% | Do not touch |

**Phase restrictions** — hard limits on what's allowed per project maturity:
- Prototype → NO tests, CI, types, monitoring, auth, infra
- Development → Unit tests, basic types, simple error handling
- Hardening → Integration tests, CI, validation, logging (feature freeze)
- Maintenance → Bug fixes and security patches only

**Anti-patterns list** (10 items) — explicit "don't do this for small projects":
- No Sentry for <10 users
- No rate limiting for <10 users
- No CI/CD for prototype-phase projects
- No auth for single-user tools
- >4h estimate → break down or question scope

**MemStack integration:** Create a Portfolio skill or extend State skill. Store tier/phase in SQLite per project. Check at session start and before `/implement`-equivalent operations. Would directly improve MemStack's workflow for managing multiple freelance projects.

### Priority 2: Silent Context Compilation (MEDIUM VALUE)

Four Intellegix commands share a mandatory "Step 0" that silently gathers context before any research or planning:

```
1. Read MEMORY.md
2. git log --oneline -10
3. git diff --stat
4. Check TaskList
5. Synthesize internal "current state" paragraph
→ DO NOT present findings, DO NOT ask questions
```

This eliminates the friction of Claude asking "what are you working on?" when it could figure it out. The "DO NOT present findings" directive is key — it prevents wasted tokens on state summaries the user already knows.

**MemStack integration:** Add Step 0 to Echo and Work skill protocols. Before searching memory or loading a plan, silently gather git status + recent commits + active tasks. Present only relevant findings, not a full state dump.

### Priority 3: MEMORY.md Separation from CLAUDE.md (MEDIUM VALUE)

Intellegix enforces a hard boundary:
- **CLAUDE.md** = behavioral rules (how to work)
- **MEMORY.md** = learned patterns, gotchas, session discoveries (what you've learned)
- **memory/*.md** = detailed implementation notes per topic
- Hard cap: MEMORY.md < 150 lines, CLAUDE.md < 100 lines

MemStack already has this conceptually (CLAUDE.md for project config, SQLite for memory), but the explicit file-size discipline and the `memory/*.md` topic files pattern are worth adopting for projects that don't use MemStack's full SQLite stack.

### Priority 4: Pattern Reference Library (MEDIUM VALUE)

Intellegix organizes coding patterns into 8 standalone reference files:
- `PYTHON_PATTERNS.md` — Result pattern, Pydantic, async, logging
- `TYPESCRIPT_PATTERNS.md` — Zod, React Query, Zustand
- `API_PATTERNS.md` — Response envelope, FastAPI routes, rate limiting
- `TESTING_PATTERNS.md` — AAA pattern, mocking, React Testing Library
- `SECURITY_CHECKLIST.md` — Pre-commit security checklist
- Plus 3 more (MCP, Browser, Security-MCP)

These are anchor-linked from CLAUDE.md and agents — Claude loads them on demand, not upfront.

**MemStack integration:** Could create a `patterns/` directory with project-agnostic reference files. Grimoire could auto-link relevant patterns based on project tech stack. Lower priority since MemStack's focus is memory, not coding standards.

### Priority 5: Path-Scoped Rules (LOW VALUE)

Intellegix rules use `paths:` frontmatter to scope rules to specific file types:
```yaml
paths:
  - "**/*.py"
  - src/**/*.py
```

MemStack's rules are globally scoped. CC natively supports `globs:` frontmatter for path scoping.

**MemStack integration:** Already identified in the CC best-practice comparison as Priority 5. Low effort but low impact for MemStack's current use case.

---

## Patterns to Skip

### Autonomous Loop Driver — SKIP

The loop_driver.py is impressive engineering (budget enforcement, stagnation detection, model fallback, session rotation), but it requires:
- Python 3.11+ running as a separate process
- `--dangerously-skip-permissions` flag (security concern)
- `.workflow/` directory per project
- Complex configuration (model timeouts, budget caps, stagnation windows)

This contradicts MemStack's zero-dependency philosophy. The loop is designed for autonomous multi-hour runs where the human walks away — MemStack is designed for interactive sessions where the human is present.

### Multi-Agent Orchestration — SKIP (for now)

Intellegix's 9 specialized agents with cross-boundary flagging and sequential/concurrent delegation is architecturally sophisticated, but:
- MemStack deprecated Familiar (its only multi-agent feature) because CC's native Task tool handles it
- The orchestrator pattern adds significant complexity
- Solo developers rarely need 9 specialized agents

**Revisit if:** MemStack ever targets team workflows or if a user requests multi-agent support.

### Perplexity Research Integration — SKIP

The council automation (multi-model synthesis via browser automation) is the most unique Intellegix feature, but:
- Requires Perplexity Pro/Max subscription
- Depends on brittle CSS selectors that break with Perplexity UI changes
- The browser bridge requires Node.js + Chrome extension installation
- $0/query is clever but fragile (session cookies, rate limits, DOM scraping)

This is a specialized research workflow, not a general-purpose enhancement. MemStack users who need multi-model research can use Perplexity directly.

### MCP Browser Bridge — SKIP

Full Chrome extension + WebSocket + MCP server stack for browser automation. Too heavyweight for MemStack's scope. CC already has Playwright MCP support for users who need browser automation.

### Construction-BI Agent — SKIP

Domain-specific to Intellegix's construction industry clients. Not applicable to MemStack.

---

## Feature Matrix: Port, Skip, or Adapt

| Intellegix Feature | Action | Reasoning |
|---------------------|--------|-----------|
| **Portfolio governance (tiers/phases)** | **Port** | Prevents over-engineering; directly useful for freelance multi-project management |
| **Silent context compilation (Step 0)** | **Port** | Reduces friction; improves Echo and Work skill startup |
| **MEMORY.md separation discipline** | **Adapt** | MemStack already separates via SQLite; adopt the file-size discipline and topic files |
| **Pattern reference library** | **Adapt** | Create optional patterns/ directory; let Grimoire auto-link |
| **Path-scoped rules** | **Adapt** | Use CC's native `globs:` frontmatter on existing rules |
| **Handoff command** | **Skip** | MemStack's Diary handoff section already covers this |
| **Smart-plan workflow** | **Skip** | MemStack's Work skill + SQLite persistence is better for cross-session planning |
| **Agent specialization (9 agents)** | **Skip** | Overkill for solo developer; CC's Task tool suffices |
| **Autonomous loop driver** | **Skip** | Contradicts interactive session philosophy; requires running process |
| **Perplexity research integration** | **Skip** | Too many external dependencies; brittle DOM automation |
| **Multi-model council synthesis** | **Skip** | Niche feature; users can use Perplexity directly |
| **MCP browser bridge** | **Skip** | Heavyweight; CC has Playwright MCP natively |
| **Code review command** | **Consider** | MemStack lacks code review; Verify only does pre-commit checks |
| **Anti-patterns list** | **Port** | Explicit "don't over-engineer" list is universally useful |
| **CI/CD + CodeQL** | **Consider** | MemStack has no CI; would be needed for marketplace publishing |

---

## Architecture Comparison

```
Intellegix Architecture:
  Loop Driver (Python) ──→ Claude Code CLI (subprocess)
       │                        │
       ├─ Budget enforcement    ├─ 9 Agents (Task tool delegation)
       ├─ Stagnation detection  ├─ 15 Slash Commands
       ├─ Model fallback        ├─ 4 Path-scoped Rules
       └─ Session rotation      ├─ Portfolio Governance (PORTFOLIO.md)
                                └─ MCP Browser Bridge (Chrome ext ↔ WebSocket ↔ Node.js)
                                        │
                                        └─ Perplexity Council (browser automation)

MemStack Architecture:
  MEMSTACK.md (entry point) ──→ Claude Code (in-session)
       │                            │
       ├─ 18 Skills (SKILL.md)      ├─ SQLite Memory (sessions, insights, plans, context)
       ├─ 4 Hooks (shell scripts)   ├─ LanceDB Vectors (semantic search)
       ├─ 5 Rules (always-on)       ├─ Markdown Backup (memory/sessions/)
       └─ 2 Commands (slash)        └─ Shell Hooks (pre-push, post-commit, session start/end)
```

**Key difference:** Intellegix is **infrastructure-heavy** (Python process, Node.js server, Chrome extension, Playwright). MemStack is **infrastructure-light** (markdown + SQLite + shell scripts). Intellegix assumes you'll invest in setup for long-running autonomous pipelines. MemStack assumes you want to start a CC session and immediately benefit from persistent memory.

---

## Unique Insights from Intellegix

### 1. The "Complexity Budget" Concept

Intellegix maps allowed complexity to project tier:

| Tier | Tests | CI | Monitoring | Docs |
|------|-------|----|------------|------|
| T1 Production | Full suite + integration | Required | Required | Full API + architecture |
| T2 Strategic | Unit + key integration | Recommended | Optional | API docs |
| T3 Experimental | None required | None | None | README only |
| T4 Archive | N/A | N/A | N/A | N/A |

This is powerful because it makes "don't write tests for this prototype" an explicit, governed decision rather than a rationalization.

### 2. Two-Tier Plan Structure

Every research command produces a two-tier plan:
- **Tier 1 (Master Plan):** Table of contents with dependency arrows between phases
- **Tier 2 (Sub-Plans):** Per-phase details with file paths, code changes, acceptance criteria

The final two phases are ALWAYS: "Update MEMORY.md" + "Commit & Push". This ensures memory hygiene and code persistence are never forgotten.

### 3. Model Selection Clarity

Intellegix is explicit: "Sonnet is the recommended default (performs within ~1.5% of Opus on coding benchmarks at lower cost/rate-limit pressure). Opus is reserved for complex architectural decisions, novel algorithm design — rarely worth the tradeoff."

### 4. CLAUDE.md Size Discipline

Hard cap of 100 lines per project CLAUDE.md (target 60-80). Architecture goes in ARCHITECTURE.md. Patterns stay in `~/.claude/patterns/`. This prevents the CLAUDE.md bloat that degrades CC performance.

### 5. Agent Cross-Boundary Flagging

Every specialized agent has an explicit section: "when changes in your domain affect another domain, flag for the responsible agent." This creates lightweight contracts without full-blown microservice architecture.

---

## Combined Adoption Roadmap

| Priority | Pattern | MemStack Integration | Effort |
|----------|---------|---------------------|--------|
| **P1** | Portfolio tier/phase governance | New skill or extend State | Medium |
| **P1** | Anti-patterns list (10 items) | Add to `.claude/rules/memstack.md` | Low |
| **P2** | Silent context compilation (Step 0) | Add to Echo and Work protocols | Low |
| **P2** | MEMORY.md < 150 lines discipline | Add to Grimoire protocol | Low |
| **P2** | Two-tier plan structure | Add to Work skill plan creation | Medium |
| **P3** | Pattern reference library | Create optional `patterns/` directory | Medium |
| **P3** | Code review command | New skill or extend Verify | Medium |
| **P3** | CLAUDE.md < 100 lines discipline | Add to Grimoire protocol | Low |
| **P4** | Path-scoped rules | Add `globs:` to existing rules | Low |
| **P4** | Agent cross-boundary flagging | Revisit if multi-agent support is added | — |

---

## Verdict: Competitor, Complement, or Irrelevant?

### **Complement** — different weight classes, same ecosystem.

| Dimension | Assessment |
|-----------|-----------|
| **Same user?** | Partially — both target CC power users, but Intellegix targets teams |
| **Same problem?** | Partially — both improve CC workflows, but different aspects |
| **Competitive threat?** | Low — different philosophies (heavyweight vs lightweight) |
| **Integration potential?** | Low — architecturally incompatible (process-based vs prompt-based) |
| **Learning value?** | High — portfolio governance, anti-patterns, plan structure |

**Bottom line:** Intellegix is a full-stack agent orchestration platform for teams running autonomous pipelines. MemStack is a lightweight memory framework for solo developers. A power user could theoretically use both (Intellegix for autonomous loop runs, MemStack for interactive session memory), but the setup complexity would be high. The most valuable takeaway is the **portfolio governance system** — explicit tier/phase constraints that prevent the #1 CC waste: over-engineering small projects.

---

## Appendix: Intellegix Component Inventory

| Category | Count | Components |
|----------|-------|-----------|
| **Commands** | 15 | research, research-perplexity, automate-perplexity, labs-perplexity, smart-plan, council-refine, council-extract, export-to-council, cache-perplexity-session, ensure-space, fix-issue, implement, review, handoff, portfolio-status |
| **Agents** | 9 | Orchestrator, Architect, Backend, Frontend, Database, DevOps, Testing, Research, Construction-BI |
| **Pattern files** | 8 | Python, TypeScript, API, Testing, Security, Security-MCP, MCP, Browser Automation |
| **Rules** | 4 | api-routes, python-scripts, react-components, tests |
| **Portfolio docs** | 3 | PORTFOLIO.md.example, DECISIONS.md, PROJECT_TEMPLATE.md |
| **Loop modules** | 6 | loop_driver, config, ndjson_parser, research_bridge, state_tracker, log_redactor |
| **Council modules** | 8 | council_browser, council_config, council_query, council_metrics, council_providers, session_context, refresh_session, show_usage |
| **MCP bridge** | 12+ | server.js, websocket-bridge, Chrome extension (6 scripts), config, health, metrics, rate-limiter, validator |
| **Tests** | 220+ | Unit, integration, end-to-end across loop, council, and MCP |

## Appendix: MemStack v3.1 Skill Index (for reference)

| # | Skill | Level | Function |
|---|-------|-------|----------|
| 1 | Familiar | Lv.2 | Multi-agent dispatch (deprecated) |
| 2 | Echo | **Lv.5** | Semantic recall (LanceDB + SQLite) |
| 3 | ~~Seal~~ | **Hook** | Pre-push safety gate |
| 4 | Work | **Lv.4** | SQLite-backed plan tracking |
| 5 | Project | **Lv.3** | Session handoff + lifecycle |
| 6 | Grimoire | Lv.2 | CLAUDE.md management |
| 7 | Scan | Lv.2 | Project analysis + pricing |
| 8 | Quill | Lv.2 | Client quotation generation |
| 9 | Forge | Lv.2 | New skill creation |
| 10 | Diary | **Lv.5** | Session logging + structured handoff |
| 11 | Shard | Lv.2 | Large file refactoring |
| 12 | Sight | Lv.2 | Architecture visualization |
| 13 | ~~Monitor~~ | **Hook** | Session status reporting |
| 14 | ~~Deploy~~ | **Hook** | Post-commit safety |
| 15 | KDP Format | Lv.2 | Markdown to KDP .docx |
| 16 | Humanize | Lv.1 | AI writing pattern removal |
| 17 | State | Lv.1 | Living STATE.md tracking |
| 18 | Verify | Lv.1 | Pre-commit verification |
