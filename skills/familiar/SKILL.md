---
name: familiar
description: "Multi-agent task dispatch. Generates ready-to-paste prompts for parallel CC sessions. Triggers on dispatch, send familiar, split task."
---


# 👻 Familiar — Dispatching Sub-Agents...
*Break large tasks into coordinated CC session prompts for parallel execution.*

## Activation

When this skill activates, output:

`👻 Familiar — Dispatching sub-agents...`

Then execute the protocol below.

## Protocol

1. **Analyze the task** — identify independent sub-tasks that can run in parallel
2. **Determine session count** — split into 2-6 sessions based on complexity
3. **For each sub-task, generate a complete CC prompt** that includes:
   - Working directory path
   - Full task description with acceptance criteria
   - Any shared context (database schema, API contracts, types)
   - MemStack activation line: `Read C:\Projects\memstack\MEMSTACK.md`
   - CC Monitor reporting snippet (if configured in config.json)
4. **Add coordination notes** — specify what each session should NOT touch to avoid conflicts
5. **Define merge order** — which session's work should be committed first

## Inputs
- The large task description
- Project directory from config.json
- Number of available CC sessions (default: 3)

## Outputs
- Numbered list of sub-task prompts, each ready to paste into a new CC session
- Coordination notes explaining dependencies and merge order

## Example Usage

**User:** "dispatch — build the analytics dashboard, API routes, and database migration"

**Familiar activates:**

```
👻 Familiar — Dispatching sub-agents...

Session 1 — Database & Types
Working directory: C:\Projects\AdminStack
Task: Create migration + TypeScript types for analytics...

Session 2 — API Routes
Working directory: C:\Projects\AdminStack
Task: Build /api/analytics endpoints (types from Session 1)...

Session 3 — Frontend Page
Working directory: C:\Projects\AdminStack
Task: Build /analytics dashboard page...

Merge order: Session 1 → Session 2 → Session 3
```

## Level History

- **Lv.1** — Base: Multi-agent dispatch with coordinated prompts. (Origin: MemStack v1.0, Feb 2026)
- **Lv.2** — Enhanced: Added YAML frontmatter, activation message, merge ordering. (Origin: MemStack v2.0 MemoryCore merge, Feb 2026)
