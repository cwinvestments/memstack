# Familiar — MemStack Skill

## Trigger Keywords
- dispatch, send familiar, multi-session, split task

## Purpose
Break a large task into sub-tasks and generate separate CC prompts for parallel execution across multiple sessions.

## Instructions

1. **Analyze the task** — identify independent sub-tasks that can run in parallel
2. **Determine session count** — split into 2-6 sessions based on complexity
3. **For each sub-task, generate a complete CC prompt** that includes:
   - Working directory path
   - Full task description with acceptance criteria
   - Any shared context (database schema, API contracts, types)
   - MemStack activation line: `Read C:\Projects\memstack\MEMSTACK.md`
   - CC Monitor reporting snippet (if configured)
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

**User prompt:** "dispatch — build the new dashboard page, API routes, and database migration for the analytics feature"

**Familiar activates and produces:**

```
## Session 1 — Database & Types
Working directory: C:\Projects\AdminStack
Task: Create database migration for analytics tables and TypeScript types...

## Session 2 — API Routes
Working directory: C:\Projects\AdminStack
Task: Build /api/analytics endpoints. Types will be committed by Session 1...

## Session 3 — Frontend Page
Working directory: C:\Projects\AdminStack
Task: Build the analytics dashboard page at /analytics...

Merge order: Session 1 → Session 2 → Session 3
Conflicts to avoid: Session 2 and 3 should not modify database/ or types/
```
