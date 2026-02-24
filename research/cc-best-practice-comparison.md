# Claude Code Native Capabilities vs MemStack v2.1 — Comparison Report

**Date:** 2026-02-22
**Source:** https://github.com/shanraisshan/claude-code-best-practice
**MemStack version:** 2.1.0

---

## Executive Summary

Claude Code has evolved significantly since MemStack was built. CC now natively supports skills, agents, hooks, persistent memory, rules, MCP integration, and a plugin system with marketplaces. Several MemStack skills duplicate functionality that CC handles natively, while other MemStack capabilities (SQLite memory, session diaries, pricing tools) remain unique. The biggest opportunity is **converting MemStack into a CC plugin** that leverages native infrastructure instead of fighting it.

---

## 1. Features CC Natively Supports That MemStack Duplicates

### 1a. Skills System — MemStack's Core Architecture is Now Redundant

| Aspect | MemStack v2.1 | CC Native |
|--------|--------------|-----------|
| **Skill format** | `skills/*.md` with YAML frontmatter | `.claude/skills/*/SKILL.md` with YAML frontmatter |
| **Discovery** | Manual — user pastes `Read MEMSTACK.md` into prompt | Automatic — CC reads `description` fields and activates on intent match |
| **Invocation** | Keyword matching via context guards | Slash command (`/skill-name`) + auto-discovery + agent preload |
| **Trigger control** | Context guards (active/dormant tables) | `disable-model-invocation`, `user-invocable` frontmatter flags |
| **Deconfliction** | Manual ownership table in MEMSTACK.md | Priority ordering: Enterprise > Personal > Project > Plugin |
| **Supporting files** | Not supported | Subdirectory files alongside SKILL.md are accessible |

**Verdict:** MemStack's skill discovery (paste-MEMSTACK.md-into-prompt) is a hack that CC's native auto-discovery eliminates. CC's skills also support `$ARGUMENTS`, shell command substitution (`` !`command` ``), and model overrides — none of which MemStack has.

### 1b. Agents — Familiar Skill Reinvents CC's Task Tool

| Aspect | MemStack Familiar | CC Native Agents |
|--------|------------------|-----------------|
| **Multi-agent dispatch** | Generates paste-able prompts for separate CC windows | Task tool spawns real subagents with isolated contexts |
| **Coordination** | Manual — user pastes prompts and manages order | Built-in — agents share tool results, can chain via Task() |
| **Parallel execution** | User opens multiple CC sessions manually | Multiple Task() calls in parallel, same session |
| **Agent config** | None — each session is a fresh CC instance | `.claude/agents/*.md` with tools, model, permissions, hooks, memory |
| **Agent Teams** | Not supported | `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` for real multi-agent |

**Verdict:** Familiar is the most obsolete MemStack skill. CC's native Task tool + agents do everything Familiar does, but actually in-process rather than requiring manual session management.

### 1c. Memory — CC Has 4 Memory Layers Now

| Aspect | MemStack | CC Native |
|--------|----------|-----------|
| **Project context** | SQLite `project_context` table | `CLAUDE.md` (committed) + `.claude/CLAUDE.local.md` (personal) |
| **Session memory** | SQLite `sessions` table + Diary skill | Auto-memory at `~/.claude/projects/<hash>/memory/` |
| **Agent memory** | Not supported | `memory: project\|user\|local` in agent frontmatter → persistent `MEMORY.md` |
| **Cross-session recall** | Echo skill searches SQLite | Auto-memory loaded at session start; `/memory` command for manual |
| **Hierarchical loading** | Flat — one MEMSTACK.md | Ancestor walking (root→cwd) + lazy descendant loading |

**Key difference:** CC's auto-memory is markdown-based and unstructured. MemStack's SQLite memory is structured and searchable with full-text search across sessions, insights, and plans. This is MemStack's strongest differentiator.

### 1d. Rules — MEMSTACK.md Global Rules → .claude/rules/

| Aspect | MemStack | CC Native |
|--------|----------|-----------|
| **Global rules** | MEMSTACK.md "Global Rules" section (5 rules) | `.claude/rules/*.md` — modular, one file per topic |
| **Path scoping** | Not supported | Frontmatter `globs:` for path-specific rules |
| **Hierarchy** | Single file | User-level + project-level with override |

**Verdict:** MemStack's global rules (commit format, .env exclusion, build-before-push) would be better as individual `.claude/rules/` files with glob scoping.

### 1e. Hooks — Passive Skills Are Prompt-Based Hooks

| Aspect | MemStack Passive Skills | CC Native Hooks |
|--------|------------------------|-----------------|
| **Monitor** (session reporting) | Prompt-based — CC remembers to curl at milestones | `SessionStart` + `Stop` hooks — deterministic, runs every time |
| **Seal** (commit safety) | Prompt-based — CC follows protocol when triggered | `PreToolUse` hook on `Bash(git commit)` — can block commits |
| **Deploy** (push safety) | Prompt-based — CC follows protocol when triggered | `PreToolUse` hook on `Bash(git push)` — can block pushes |
| **Reliability** | Depends on CC remembering the prompt | Deterministic — shell scripts execute on every matching event |
| **Exit codes** | N/A | `0`=continue, `1`=error, `2`=block operation |

**Verdict:** MemStack's passive skills (Monitor, Seal, Deploy) are the most fragile part of the framework because they rely on the LLM remembering to follow the protocol. CC hooks are deterministic — they always fire. The build-before-push check should be a `PreToolUse` hook, not a prompt instruction.

### 1f. Grimoire — CC Already Manages CLAUDE.md

| Aspect | MemStack Grimoire | CC Native |
|--------|------------------|-----------|
| **CLAUDE.md management** | Grimoire skill reads/updates CLAUDE.md | `/memory` command opens CLAUDE.md for editing |
| **Auto-detection** | Grimoire detects what changed and updates sections | CC doesn't auto-update CLAUDE.md (manual) |
| **Cross-project** | config.json maps projects to CLAUDE.md paths | Each project has its own `.claude/CLAUDE.md` |

**Verdict:** Partial overlap. CC's `/memory` is simpler but doesn't auto-detect changes. Grimoire's auto-update protocol is genuinely useful and worth keeping as a skill.

---

## 2. Features MemStack Has That CC Doesn't Cover

### 2a. SQLite Structured Memory (Echo, Diary, Work, Project)

CC's auto-memory is markdown-based and unstructured. MemStack's SQLite backend provides:

- **Full-text search** across sessions, insights, and plans (`search` command)
- **Structured schema** — sessions have date, project, accomplished, decisions fields
- **Auto-extracted insights** — Diary pulls decisions from sessions into a searchable `insights` table
- **Plan tracking** — Work skill tracks per-task status (pending/in-progress/done) in `plans` table
- **Cross-project queries** — search insights across all projects at once

**This is MemStack's most valuable feature.** CC has no equivalent for structured, queryable, cross-session memory.

### 2b. Session Diary with Insight Extraction

CC's auto-memory saves whatever the model decides is important. MemStack's Diary skill:
- Captures structured session data (accomplished, files changed, commits, decisions, problems)
- Auto-extracts decisions as reusable insights
- Links insights to projects for cross-project pattern discovery

### 2c. Plan Execution Across Sessions (Work Skill)

CC has built-in `TaskCreate`/`TaskUpdate`/`TaskList` tools for in-session task tracking, but these **do not persist across sessions**. MemStack's Work skill with SQLite-backed plans enables:
- `copy plan` — parse a plan into DB tasks
- `resume plan` — reload plan in a new session with progress
- `append plan` — update task statuses

### 2d. Project Scanning & Pricing (Scan + Quill)

Domain-specific business tools:
- **Scan**: LOC counting, complexity assessment, three-tier pricing for client projects
- **Quill**: Professional quotation generation with templates

CC has no built-in equivalent — these are freelancer/agency workflow tools.

### 2e. Context Guards with Negative Patterns

MemStack's context guards include **explicit negative patterns** (e.g., Echo won't fire on "memory" as a code concept, Seal defers "push" to Deploy). CC's native skill discovery relies on description matching, which lacks this level of deconfliction control.

### 2f. Skill Leveling System

MemStack tracks skill evolution (Lv.1→Lv.4+) with a changelog per skill. CC has no equivalent — skills are versioned only via git.

### 2g. Architecture Visualization (Sight)

Mermaid diagram generation based on codebase analysis. CC can do this on request but doesn't have a structured skill for it.

### 2h. Large File Refactoring (Shard)

Auto-triggers when files exceed 1000 LOC. CC has no built-in equivalent for proactive refactoring suggestions.

---

## 3. Upgrade Opportunities — Integrating CC Native Capabilities

### Priority 1: Convert to CC Plugin

**What:** Package MemStack as a proper CC plugin with `plugin.json`, distributable via marketplace.

**Structure:**
```
memstack-plugin/
├── plugin.json
├── skills/
│   ├── echo/SKILL.md
│   ├── diary/SKILL.md
│   ├── work/SKILL.md
│   ├── scan/SKILL.md
│   ├── quill/SKILL.md
│   ├── sight/SKILL.md
│   ├── shard/SKILL.md
│   └── forge/SKILL.md
├── agents/
│   ├── familiar.md        # Replaces Familiar skill with real agent
│   └── monitor.md         # Background monitoring agent
├── hooks/
│   └── settings.json      # PreToolUse hooks for Seal/Deploy
├── .mcp.json              # Optional: MCP server for SQLite memory
└── db/
    ├── memstack-db.py
    └── schema.sql
```

**Why:** Eliminates the "paste MEMSTACK.md into your prompt" hack. Skills auto-discover. Hooks fire deterministically. Agents dispatch properly.

### Priority 2: Replace Passive Skills with Hooks

| MemStack Skill | Replace With | Hook Event |
|----------------|-------------|------------|
| **Seal** (commit safety) | `PreToolUse` hook on `Bash` matching `git commit` | Runs build check script, exit 2 to block |
| **Deploy** (push safety) | `PreToolUse` hook on `Bash` matching `git push` | Runs build + secrets check, exit 2 to block |
| **Monitor** (session reporting) | `SessionStart` + `Stop` + `PostToolUse` hooks | Curl to monitoring API deterministically |

**Config in plugin's settings.json:**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{
          "type": "command",
          "command": "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/seal-check.sh"
        }]
      }
    ],
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/monitor-start.sh"
      }]
    }],
    "Stop": [{
      "hooks": [{
        "type": "command",
        "command": "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/monitor-stop.sh"
      }]
    }]
  }
}
```

**Why:** Hooks are deterministic. MemStack's prompt-based approach means Seal/Deploy only work if the LLM remembers to follow the protocol. Hooks fire every time, even if the model forgets.

### Priority 3: Replace Familiar with Native Agent

**Current:** Familiar generates prompts for the user to paste into separate CC windows.

**Upgrade:** Create a proper `.claude/agents/familiar.md`:
```yaml
---
name: familiar
description: Use PROACTIVELY when task requires parallel work streams. Dispatches subtasks to subagents.
tools: Read, Glob, Grep, Bash, Task
model: sonnet
maxTurns: 15
---
Break the task into independent sub-tasks and dispatch each via the Task tool.
Each Task call runs in an isolated context with its own tools.
```

**Why:** Real subagent dispatch > copy-paste prompts.

### Priority 4: Expose SQLite Memory as MCP Server

**What:** Wrap `memstack-db.py` as an MCP server so CC can access memory via native tool calls instead of `python ... | parse JSON`.

**Benefits:**
- Memory queries become first-class CC tools
- Other plugins/agents can access MemStack memory
- CC's MCP tool search auto-discovers memory commands

### Priority 5: Move Global Rules to .claude/rules/

**What:** Convert MEMSTACK.md's 5 global rules into individual rule files:
```
.claude/rules/
├── commit-format.md          # [ProjectName] message format
├── no-secrets.md             # Never commit .env, node_modules
├── build-before-push.md      # Always run build
└── skill-chain.md            # Work → Seal → Diary → Monitor
```

**Why:** Path-scoping via `globs:` frontmatter. Better modularity. Follows CC conventions.

### Priority 6: Use Agent Memory for Echo/Diary

**What:** Give the Echo and Diary agents persistent `memory: project` so they can maintain their own `MEMORY.md` files alongside the SQLite database.

**Why:** CC automatically loads 200 lines of agent memory into the system prompt. Echo could maintain a "recent recalls" summary; Diary could maintain a "key insights" summary.

### Priority 7: Convert Grimoire to Leverage /memory

**What:** Keep Grimoire's auto-detection of what changed, but use CC's native `/memory` integration for the actual editing.

---

## Feature Matrix: What to Keep, Replace, or Hybrid

| MemStack Feature | Action | Reasoning |
|------------------|--------|-----------|
| **MEMSTACK.md master index** | **Replace** with plugin auto-discovery | CC auto-discovers skills from descriptions |
| **Skill files (14)** | **Convert** to `.claude/skills/*/SKILL.md` format | Same content, native format |
| **Context guards** | **Keep** in skill descriptions | Translate to better `description` fields |
| **Skill deconfliction** | **Keep** as rules file | `.claude/rules/skill-deconfliction.md` |
| **Leveling system** | **Keep** in Level History sections | Unique to MemStack |
| **SQLite memory** | **Keep + upgrade** to MCP server | MemStack's strongest differentiator |
| **Echo (recall)** | **Keep** as skill + MCP | SQLite search has no CC equivalent |
| **Diary (session log)** | **Keep** as skill + `Stop` hook | Hybrid: hook triggers, skill formats |
| **Work (plans)** | **Keep** as skill | Persistent plans across sessions > CC's in-session TaskCreate |
| **Project (handoff)** | **Hybrid** — CC auto-memory + SQLite context | CC handles some, SQLite handles structured state |
| **Seal (commits)** | **Replace** with `PreToolUse` hook | Deterministic > prompt-based |
| **Deploy (push)** | **Replace** with `PreToolUse` hook | Deterministic > prompt-based |
| **Monitor (reporting)** | **Replace** with `SessionStart`/`Stop` hooks | Deterministic > prompt-based |
| **Familiar (dispatch)** | **Replace** with native agent + Task tool | Real subagents > paste-able prompts |
| **Grimoire (CLAUDE.md)** | **Hybrid** — auto-detect + `/memory` | Keep the smart part, use native editing |
| **Scan (analysis)** | **Keep** as skill | No CC equivalent |
| **Quill (quotes)** | **Keep** as skill | No CC equivalent |
| **Forge (new skills)** | **Keep** but update to generate CC-native format | Update templates for SKILL.md |
| **Shard (refactor)** | **Keep** as skill | No CC equivalent |
| **Sight (diagrams)** | **Keep** as skill | No CC equivalent |
| **config.json** | **Replace** with `.claude/settings.json` + plugin config | Follow CC conventions |

---

## Summary

| Category | Count |
|----------|-------|
| Features to **replace** with CC native | 5 (Seal, Deploy, Monitor, Familiar, MEMSTACK.md) |
| Features to **keep** (unique to MemStack) | 8 (SQLite memory, Echo, Diary, Work, Scan, Quill, Shard, Sight) |
| Features to **hybrid** (combine both) | 3 (Project, Grimoire, Forge) |
| **Biggest win** | Converting to CC plugin — eliminates the paste-MEMSTACK.md hack |
| **Most valuable asset** | SQLite structured memory — CC has nothing comparable |
| **Most obsolete feature** | Familiar — CC's Task tool + agents does this natively |

---

## Recommended Upgrade Path

1. **v3.0** — Convert to CC plugin format. Move skills to SKILL.md. Add hooks for Seal/Deploy/Monitor. Replace Familiar with native agent.
2. **v3.1** — Expose SQLite memory as MCP server. Move rules to `.claude/rules/`. Add agent memory to Echo/Diary.
3. **v3.2** — Publish to marketplace. Add install/setup commands. Community skills via Forge generating SKILL.md format.

---

## Superpowers Comparison

**Date:** 2026-02-24
**Superpowers version:** 4.3.1
**Repo:** https://github.com/obra/superpowers
**Author:** Jesse Vincent

### What Superpowers Is

A CC plugin focused on **developer discipline enforcement** — structured workflows for brainstorming, TDD, debugging, code review, and multi-agent task execution. Unlike MemStack (which adds memory + safety + business tools), Superpowers adds **process rigor** to Claude Code's creative work.

### Philosophy Difference

| Dimension | MemStack | Superpowers |
|-----------|----------|-------------|
| **Core problem** | Claude forgets context across sessions | Claude skips process discipline within sessions |
| **Approach** | Persistent memory + safety gates + business tools | Anti-rationalization skill design + mandatory workflows |
| **What it adds** | Data (sessions, insights, plans, vectors) | Behavior (TDD, brainstorming, verification, review loops) |
| **Architecture metaphor** | Database + recall engine | Behavioral guardrails + decision flowcharts |
| **Skill count** | 18 skills (diverse domains) | 14 skills (all process/workflow) |
| **Agents** | None (Familiar deprecated) | 1 (code-reviewer) + subagent templates |
| **Hooks** | 4 (pre-push, post-commit, session-start/end) | 1 (session-start — injects meta-skill into context) |
| **Persistence** | SQLite + LanceDB vectors + markdown | None — stateless, pure behavior |
| **Business tools** | Yes (Scan, Quill, KDP Format) | No — exclusively developer workflow |
| **Target** | Multi-project freelancer/agency workflow | Single-project development discipline |

### Feature Overlap

| Capability | MemStack | Superpowers | Winner |
|------------|----------|-------------|--------|
| **Session memory** | SQLite + LanceDB vectors + markdown diaries | None | MemStack |
| **Cross-session recall** | Echo (semantic + keyword search) | None | MemStack |
| **Commit safety** | Pre-push hook (build, secrets, format) | Verification-before-completion skill | MemStack (deterministic) |
| **Task planning** | Work skill (SQLite-backed plan tracking) | Writing-plans + executing-plans skills | Superpowers (more structured process) |
| **Code review** | None | code-reviewer agent + 2-stage review (spec then quality) | Superpowers |
| **Multi-agent dispatch** | Familiar (deprecated, manual paste) | Subagent-driven-development (real Task tool dispatch) | Superpowers |
| **TDD enforcement** | None | test-driven-development skill with rationalization tables | Superpowers |
| **Debugging workflow** | None | systematic-debugging skill | Superpowers |
| **Brainstorming** | None | brainstorming skill with HARD-GATE blocking implementation | Superpowers |
| **Git worktree isolation** | None | using-git-worktrees (mandatory before feature work) | Superpowers |
| **Architecture diagrams** | Sight skill (Mermaid) | None | MemStack |
| **Business tools** | Scan, Quill, KDP Format | None | MemStack |
| **Session handoffs** | Diary Lv.5 (structured handoff section) | None | MemStack |
| **State tracking** | State skill (STATE.md) | None | MemStack |

**Verdict:** Near-zero functional overlap. MemStack = memory + safety + business. Superpowers = discipline + process + review. They solve orthogonal problems.

### Unique Patterns Worth Adopting

#### 1. Anti-Rationalization Tables (HIGH VALUE)

Superpowers' most distinctive pattern. Every discipline-enforcing skill includes a two-column table mapping Claude's known excuses to rebuttals:

| Claude thinks... | Reality |
|---|---|
| "This is too simple for TDD" | Simple things become complex. Use it. |
| "I already manually tested it" | Ad-hoc ≠ systematic. No record, can't re-run. |
| "Let me explore the codebase first" | Skills tell you HOW to explore. Check first. |

These tables were built empirically from baseline testing (watching Claude fail without the skill, logging its rationalizations, then pre-empting them in the skill text).

**MemStack opportunity:** Add rationalization tables to Echo, Diary, and Verify skills. Example for Diary: counter "Nothing important happened this session" and "I'll remember this for next time."

#### 2. The Description Trap Discovery (HIGH VALUE)

Superpowers v4.0.0 discovered that **skill descriptions that summarize the workflow cause Claude to follow the short description instead of reading the full skill content**. When subagent-driven-development's description mentioned "code review between tasks," Claude did ONE review instead of TWO (as the full skill specified).

**Rule:** Descriptions must say ONLY when to invoke the skill, never what the skill does.

**MemStack opportunity:** Audit all 18 SKILL.md descriptions. Several (Echo, Diary, Work) include workflow summaries that may cause Claude to shortcut the full protocol.

#### 3. DOT/GraphViz Flowcharts as Specifications (MEDIUM VALUE)

Instead of prose instructions that Claude can paraphrase or skip steps from, Superpowers embeds raw DOT flowcharts as the authoritative process definition. The prose becomes supporting context. This is unique in the CC plugin ecosystem.

**MemStack opportunity:** Convert Echo's search protocol (vector → SQLite → markdown fallback) and Diary's logging protocol into DOT flowcharts for more reliable execution.

#### 4. Two-Stage Review Loop (MEDIUM VALUE)

Superpowers separates code review into two mandatory stages with enforced ordering:
1. **Spec compliance** — Does the code match requirements? (skeptical reviewer prompt: "The implementer finished suspiciously quickly")
2. **Code quality** — Is the code well-written?

Code quality review is explicitly blocked until spec compliance passes.

**MemStack opportunity:** Verify skill currently does a single-pass check. Could adopt the two-stage pattern: requirements check first, then quality check.

#### 5. Session-Start Context Injection via Hook (MEDIUM VALUE)

Superpowers' `using-superpowers` meta-skill is injected into every session via a SessionStart hook, not loaded on demand. This ensures the skill routing logic is present from the very first message. The content is wrapped in `<EXTREMELY_IMPORTANT>` tags.

**MemStack already does this** partially (session-start.sh runs Headroom + CLAUDE.md indexer), but doesn't inject a meta-skill. Could inject a "MemStack routing" context that tells Claude about available skills without requiring the user to paste `Read MEMSTACK.md`.

#### 6. `disable-model-invocation: true` on Commands (LOW VALUE)

Prevents Claude from calling slash commands via the Skill tool (user-only invocation). Added after observing Claude calling commands that just redirect to skills, creating loops.

**MemStack opportunity:** Add this flag to `/memstack-search` and `/memstack-headroom` commands if loop behavior is observed.

#### 7. Polyglot CMD/Bash Hook Wrapper (LOW VALUE — ALREADY SOLVED)

Cross-platform hook that's simultaneously valid CMD batch and bash script. Clever but MemStack already solves this with `.sh` scripts that work under Git Bash on Windows.

#### 8. Subagent Task Text Extraction (LOW VALUE)

Superpowers reads the plan file once, extracts all task text, and passes full task text to each subagent — avoiding per-task file reads. This is an efficiency optimization for multi-agent workflows.

**MemStack opportunity:** If Familiar is ever rebuilt as a real agent, adopt this pattern.

### Patterns MemStack Has That Superpowers Lacks

| MemStack Pattern | Gap in Superpowers |
|---|---|
| **Persistent structured memory** (SQLite + vectors) | No persistence — every session starts fresh |
| **Cross-session recall** (Echo semantic search) | No way to search past sessions |
| **Deterministic safety hooks** (pre-push, post-commit) | Only 1 hook (session-start); safety is skill-based (non-deterministic) |
| **Session diaries with insight extraction** | No session logging |
| **Skill leveling system** (Lv.1→Lv.5) | Skills are versioned only via git |
| **Context guards with negative patterns** | Relies on description matching only |
| **Business domain tools** (Scan, Quill, KDP Format) | Exclusively developer workflow |
| **Commit format enforcement** (hook-based) | No commit format conventions |

### Intellegix

> **Note:** No prior analysis of Intellegix exists in MemStack's research files or session history. If Intellegix is a CC plugin or framework, it hasn't been evaluated yet. A separate comparison would require cloning/accessing the Intellegix repo and analyzing its architecture.

### Combined Adoption Roadmap

| Priority | Pattern from Superpowers | MemStack Integration Point | Effort |
|----------|--------------------------|---------------------------|--------|
| **P1** | Anti-rationalization tables | Add to Echo, Diary, Verify SKILL.md files | Low |
| **P1** | Description Trap audit | Review all 18 SKILL.md descriptions — remove workflow summaries | Low |
| **P2** | DOT flowcharts for protocols | Convert Echo search + Diary logging to DOT specs | Medium |
| **P2** | Session-start meta-skill injection | Inject MemStack routing context via hook (eliminate paste-MEMSTACK.md) | Medium |
| **P3** | Two-stage review in Verify | Split Verify into spec compliance + code quality stages | Medium |
| **P3** | Brainstorming gate | Add brainstorming skill before Work skill plan creation | Medium |
| **P4** | Subagent task extraction | Apply if Familiar is rebuilt as native agent | Low |

### Bottom Line

**Superpowers and MemStack are perfect complements.** Superpowers enforces *how* you work (discipline). MemStack remembers *what* you worked on (memory). A developer using both gets structured workflows AND persistent cross-session recall — neither provides the other's core value.

The most valuable steal is **anti-rationalization tables** — a pattern born from empirical testing that directly improves skill compliance rates. The Description Trap discovery is equally important as an architectural invariant to adopt immediately.
