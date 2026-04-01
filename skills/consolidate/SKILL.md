---
name: consolidate
description: "Use when the user says 'consolidate', 'weekly summary', 'cross-project patterns', 'consolidate diaries', 'what patterns this week', or wants a compressed summary of recent work across all projects."
version: 1.0.0
---


# 🗜️ Consolidate — Running Cross-Project Consolidation...
*Compress a week of diary entries into actionable insights across all projects.*

## Activation

When this skill activates, output:

`🗜️ Consolidate — Running cross-project consolidation...`

Then execute the protocol below.

## Context Guard

| Context | Status | Priority |
|---------|--------|----------|
| User says "consolidate", "weekly summary", "cross-project patterns" | **ACTIVE** — run full protocol | Highest |
| User asks "what did I work on this week" across multiple projects | **ACTIVE** — run full protocol | High |
| User asks about a single project's history | DORMANT — use Echo instead | — |
| User is mid-task, not reviewing work | DORMANT — do not interrupt | — |

## Protocol

### Step 1: Gather diary entries (past 7 days)

Read the project list from `config.json` (or `config.local.json` if present):

```bash
python C:/Projects/memstack/db/memstack-db.py get-sessions --all --days 7
```

If the database query returns no results, fall back to reading markdown files:

```bash
ls -t C:/Projects/memstack/memory/sessions/ | head -20
```

Read each diary file from the past 7 days. Collect:
- Project name
- Date
- Accomplishments
- Decisions made
- Session handoff state
- Next steps

### Step 2: Send to Claude Haiku for consolidation

Using the gathered diary content, send a single prompt to Claude Haiku (`claude-haiku-4-5-20251001`) via the Anthropic API or by composing the analysis yourself:

**Consolidation prompt:**
> You are analyzing a week of development diary entries across multiple projects. Extract:
> 1. **Key decisions** — architectural choices, tool selections, trade-offs made
> 2. **Cross-project connections** — shared patterns, reusable solutions, dependencies between projects
> 3. **Recurring patterns** — repeated problems, common workflows, things that keep coming up
> 4. **Open questions** — unresolved items, blocked work, decisions deferred
> 5. **Velocity summary** — commits per project, tasks completed vs planned
>
> Output as structured markdown with clear section headers.

If the Anthropic API is not available, perform the consolidation analysis directly using your own reasoning.

### Step 3: Write weekly consolidation

Save the compressed summary:

```bash
# Format: diary/weekly-consolidation-YYYY-MM-DD.md
```

Write to `C:/Projects/memstack/diary/weekly-consolidation-[date].md` with this structure:

```markdown
# Weekly Consolidation — [start date] to [end date]

## Projects Active
- [list with commit counts]

## Key Decisions
- [decision]: [project] — [rationale]

## Cross-Project Connections
- [pattern or shared solution]

## Recurring Patterns
- [pattern]: [frequency] — [suggestion]

## Open Questions
- [question]: [project] — [context]

## Velocity
| Project | Commits | Tasks Done | Tasks Planned |
|---------|---------|------------|---------------|
```

### Step 4: Index insights for Echo

For each key decision and cross-project connection, add it to the insights database:

```bash
python C:/Projects/memstack/db/memstack-db.py add-insight '{"project":"cross-project","content":"[insight]","tags":"consolidation,weekly"}'
```

This makes consolidated insights discoverable via Echo's semantic search in future sessions.

### Step 5: Report summary

Output the consolidation to the user with:
- Number of projects analyzed
- Number of diary entries processed
- Date range covered
- Top 3 insights discovered
- Any open questions that need attention

## Example Usage

**User:** "Consolidate my diaries from this week"

**Output:**
```
🗜️ Consolidate — Running cross-project consolidation...

Analyzed 12 diary entries across 4 projects (Mar 1–7):

Projects: memstack-pro (5 entries), connectstack (3), epstein-scan (2), memstack-pro-site (2)

Top insights:
1. OS-level fd redirect pattern used in both memstack-skill-loader and connectstack for suppressing C extension output
2. Session Memory pattern (diary → load → echo) is now consistent across memstack-pro marketing and actual implementation
3. TTS config pattern (JSON config read by both hooks and rules) could be generalized to other hook configurations

Open questions:
- PR #170 at VoltAgent/awesome-agent-skills still pending review
- Netlify deploy verification for marketing site not confirmed

Saved: diary/weekly-consolidation-2026-03-07.md
Indexed: 5 new cross-project insights
```

## Ownership

- "consolidate" / "weekly summary" / "cross-project" = Consolidate only
- Single-project recall = Echo (not Consolidate)
- Session logging = Diary (not Consolidate)
- Task planning = Work (not Consolidate)

## Level History

- **Lv.1** — Base: Cross-project diary consolidation with Haiku analysis, insight indexing, weekly summary output. (Origin: MemStack Pro v3.2.3, Mar 2026)
