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
