# Accomplish AI vs MemStack — Comparison Report

**Date:** 2026-02-20
**Accomplish version:** 0.3.8 (commit 511aa5a)
**MemStack version:** 2.0.0
**Repo:** https://github.com/accomplish-ai/accomplish

---

## Executive Summary

Accomplish and MemStack are **fundamentally different tools solving different problems**. Accomplish is a GUI-based desktop agent for end-user task automation (file management, document creation, browser tasks). MemStack is a developer-workflow framework that adds persistent memory, safety gates, and multi-session orchestration to Claude Code. They are **complementary, not competitive**.

---

## What Each Tool Does

### Accomplish AI

An open-source **Electron desktop app** that acts as an AI agent for non-developer tasks:

- **File management** — sort, rename, move files based on content or rules
- **Document creation** — write, summarize, rewrite documents
- **Browser automation** — research, form entry via Playwright/MCP
- **Custom skills** — reusable markdown prompt templates (SKILL.md format)
- **Multi-provider LLM support** — 15+ providers (OpenAI, Anthropic, Google, xAI, Ollama, etc.)
- **Permission-gated execution** — user must approve file operations via GUI dialog
- **MCP connector framework** — OAuth2-enabled integrations (Notion, Google Drive, etc.)

**Architecture:** Electron shell → React UI (Vite + Zustand) → spawns OpenCode CLI via node-pty → executes tasks. SQLite for persistence. AES-256-GCM for API key storage.

**Target user:** Non-technical or semi-technical users who want AI to automate desktop tasks.

### MemStack

A **prompt-driven skill framework** for Claude Code sessions that adds:

- **14 skills** covering workflow lifecycle (commit safety, deployment, task tracking, memory recall, session handoffs, architecture visualization, code refactoring, project scanning, quotation generation)
- **Persistent memory** — session logs, project state, plans survive across CC context compacts
- **Multi-session orchestration** — Familiar skill splits tasks across parallel CC sessions
- **Git-integrated safety** — Seal (commit guardian) + Deploy (pre-flight checks)
- **Project knowledge management** — Grimoire maintains CLAUDE.md files
- **Session continuity** — Project skill creates handoff prompts for next session

**Architecture:** Markdown skill files loaded into CC context → trigger on keywords/conditions → execute protocols within the CC session. File-based persistence in memory/ directory. No runtime, no process — pure prompt engineering.

**Target user:** Developer using Claude Code for multi-project software engineering.

---

## Feature Comparison Matrix

| Capability | Accomplish | MemStack |
|---|---|---|
| **Runtime** | Electron desktop app (GUI) | Claude Code prompt framework (CLI) |
| **Task execution** | OpenCode CLI via PTY | Claude Code native tools |
| **LLM providers** | 15+ (BYOK, Ollama local) | Claude only (via CC) |
| **Skills/prompts** | SKILL.md files, add from GitHub | 14 built-in skills + Forge for new ones |
| **Persistent memory** | SQLite (task history, messages) | Markdown files (sessions, projects, plans) |
| **Session continuity** | Task history with follow-ups | Handoff prompts + Echo recall |
| **Multi-session** | No (single app, single task queue) | Yes (Familiar dispatches to parallel CC sessions) |
| **Git integration** | None | Deep (Seal commits, Deploy pre-flight, status tracking) |
| **Commit safety** | None | Seal: build check, staging review, format enforcement |
| **Deploy safety** | None | Deploy: build verify, debug artifact scan, secrets check |
| **File management** | Core feature (sort, rename, move) | Not a focus (CC handles file ops natively) |
| **Browser automation** | MCP-based (dev-browser-mcp) | None |
| **Document creation** | Core feature | None (handled by CC directly) |
| **Permission model** | GUI dialog with approve/deny | None (CC has its own permission system) |
| **Architecture viz** | None | Sight: Mermaid diagram generation |
| **Code refactoring** | None | Shard: auto-split files > 1000 LOC |
| **Project scanning** | None | Scan: LOC counts, complexity tier, pricing |
| **Client quotations** | None | Quill: professional quote generation |
| **Session logging** | Task history in SQLite | Diary: structured session docs + auto-archive |
| **Status monitoring** | None | Monitor: real-time status to AdminStack dashboard |
| **OAuth/connectors** | MCP connectors with OAuth2/PKCE | None |
| **API key storage** | AES-256-GCM encrypted | N/A (CC manages its own keys) |
| **Task queuing** | Up to 10 concurrent tasks | N/A (CC sessions are independent) |

---

## Overlap Analysis

### Shared Concepts

1. **Skills system** — Both use markdown-based prompt files. Accomplish calls them SKILL.md, MemStack uses skill .md files with YAML frontmatter. The concept is identical: structured prompts that guide AI behavior for specific tasks.

2. **Task management** — Both track task state. Accomplish uses SQLite with full message history. MemStack uses plan files with `[ ]`/`[x]`/`[~]`/`[!]` status markers.

3. **Persistence** — Both solve the "memory across sessions" problem but differently. Accomplish stores everything in SQLite. MemStack stores everything in markdown files searchable by Echo.

### No Functional Overlap

Despite similar concepts, **they operate in completely different domains**:
- Accomplish automates desktop/file/browser tasks for end users
- MemStack automates developer workflows within Claude Code sessions

You would never use Accomplish to commit code, and you would never use MemStack to sort files on your desktop.

---

## Could They Work Together?

**Yes, and here's how:**

### Scenario 1: MemStack orchestrates, Accomplish executes desktop tasks

MemStack's Familiar skill could dispatch tasks to Accomplish for non-code work. Example: "Organize the client deliverables folder" goes to Accomplish, while "Refactor the API routes" stays in CC.

### Scenario 2: Accomplish as a MCP connector for MemStack

Accomplish's MCP connector framework could theoretically expose its file management and browser automation capabilities as tools accessible from Claude Code — giving CC sessions the ability to manage files on the desktop without leaving the terminal.

### Scenario 3: Shared skills format

Both use markdown-based skills. A unified skill format could allow skills to work in both environments, with environment-specific sections.

### Practical reality

Integration would require custom development. Today, they are separate tools with no interop. The most realistic near-term combo is simply **using both**: MemStack for dev work in CC, Accomplish for desktop automation when needed.

---

## Features Accomplish Has That MemStack Could Add

| Accomplish Feature | MemStack Opportunity | Priority |
|---|---|---|
| **Multi-provider LLM support** | Not applicable — MemStack runs inside CC which is Claude-only | N/A |
| **MCP connectors** | Could add MCP server integration for external tools (Notion, Google Drive) via CC's MCP support | Medium |
| **Browser automation** | Could add a browser research skill leveraging CC's Playwright MCP | Low |
| **Permission dialogs** | MemStack could add explicit approval gates for destructive operations (beyond Seal/Deploy) | Low |
| **Task history with threading** | MemStack's Diary + Echo already covers this, but a structured DB would be more searchable | Medium |
| **GUI dashboard** | MemStack's Monitor already reports to AdminStack — could expand this into a full session dashboard | Medium |
| **Concurrent task queue** | Familiar already handles multi-session dispatch, which is more powerful than Accomplish's single-machine queue | N/A |

### Most valuable steal: **Structured storage**

Accomplish's SQLite-backed task history with full message threading, attachments, and search is more robust than MemStack's flat markdown files. If MemStack's memory grew large, migrating to a lightweight DB (or structured JSON) would improve Echo's recall speed and accuracy.

---

## Features MemStack Has That Accomplish Lacks

| MemStack Feature | Gap in Accomplish |
|---|---|
| **Git integration** (Seal, Deploy) | Accomplish has zero git awareness — no commit safety, no deploy checks |
| **Multi-session orchestration** (Familiar) | Accomplish runs single tasks sequentially; no parallel dispatch |
| **Session handoffs** (Project) | Accomplish keeps history but has no explicit handoff prompts for continuity |
| **Architecture visualization** (Sight) | No diagramming capability |
| **Code refactoring** (Shard) | Not a code tool — not applicable |
| **Project scanning** (Scan) | No project analysis or estimation |
| **Client quotations** (Quill) | No business document generation |
| **Context-aware activation** (Context Guards) | Accomplish skills activate by command only, not by contextual detection |
| **Real-time status reporting** (Monitor) | No external dashboard integration |
| **Skill creation framework** (Forge) | Users can add skills but there's no guided creation workflow |
| **Plan persistence across compacts** (Work) | N/A — Accomplish doesn't face context window limits (tasks are fresh) |

### Most valuable steal for Accomplish: **Context Guards**

MemStack's context guard system (active/dormant conditions per skill) prevents false activation. Accomplish's skills activate only by explicit command, missing the opportunity for intelligent auto-activation based on what the user is doing.

---

## Verdict: Competitor, Complement, or Irrelevant?

### **Complement** — with caveats.

| Dimension | Assessment |
|---|---|
| **Same user?** | Partially — a developer might use both |
| **Same problem?** | No — desktop automation vs developer workflow |
| **Competitive threat?** | None — completely different domains |
| **Integration potential?** | Moderate — MCP could bridge them |
| **Learning value?** | High — Accomplish's architecture is well-engineered |

**Bottom line:** Accomplish is an AI desktop assistant for everyone. MemStack is a developer-workflow brain for Claude Code. They solve different problems for overlapping users. Use both when appropriate — Accomplish for desktop tasks, MemStack for code work.

The most interesting takeaway is architectural: Accomplish's **SQLite + repository pattern** for structured persistence is something MemStack could adopt to replace flat markdown files as memory scales. And Accomplish could learn from MemStack's **context guard system** for smarter skill activation.

---

## Appendix: Accomplish Tech Stack

```
Monorepo (pnpm workspaces)
├── apps/desktop     — Electron (main + preload + renderer)
├── apps/web         — React (Vite + React Router + Zustand + Tailwind + shadcn/ui)
└── packages/
    └── agent-core   — Core logic (ESM, TypeScript)
        ├── internal/classes/  — TaskManager, OpenCodeAdapter, SkillsManager, SecureStorage
        ├── factories/         — Public API (createTaskManager, createStorage, etc.)
        ├── storage/           — SQLite + migrations + repositories
        ├── providers/         — 15 LLM providers with validation
        ├── connectors/        — MCP OAuth2 integration
        ├── services/          — Permission handler, speech, summarizer
        └── mcp-tools/         — 7 MCP servers (start-task, complete-task, ask-user, etc.)
```

## Appendix: MemStack Skill Index

| # | Skill | Type | Domain |
|---|---|---|---|
| 1 | Familiar | Keyword | Multi-session dispatch |
| 2 | Echo | Keyword | Memory recall |
| 3 | Seal | Passive | Commit safety |
| 4 | Work | Keyword | Task/plan management |
| 5 | Project | Contextual | Session handoffs |
| 6 | Grimoire | Keyword | CLAUDE.md management |
| 7 | Scan | Keyword | Project analysis |
| 8 | Quill | Keyword | Client quotations |
| 9 | Forge | Keyword | Skill creation |
| 10 | Diary | Contextual | Session logging |
| 11 | Shard | Contextual | Code refactoring |
| 12 | Sight | Keyword | Architecture diagrams |
| 13 | Monitor | Passive | Status reporting |
| 14 | Deploy | Passive | Deployment safety |
