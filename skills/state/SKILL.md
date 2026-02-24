---
name: state
description: "Maintain a living STATE.md document tracking current task, decisions, blockers, and next steps. Auto-reads at session start. Triggers on update state, project state, where was I."
---


# 📍 State — Updating Project State...
*Maintain a living document of where you are right now in a project.*

## Activation

When this skill activates, output:

`📍 State — Updating project state...`

Then execute the protocol below.

## Context Guard

| Context | Status | Priority |
|---------|--------|----------|
| **User says "update state", "save state", "project state"** | ACTIVE — update STATE.md | P1 |
| **User says "where was I", "where did I leave off"** | ACTIVE — read and present STATE.md | P1 |
| **User starts a session and STATE.md exists** | ACTIVE — read silently, use as context | P2 |
| **User says "save diary" or "log session"** | DORMANT — Diary handles full session logs | — |
| **User says "save project" or "handoff"** | DORMANT — Project skill handles lifecycle | — |
| **User asks to recall past sessions** | DORMANT — Echo handles historical recall | — |

## Protocol

### Reading State (session start or "where was I")

1. **Check for STATE.md** in the current project's `.claude/` directory:
   ```
   {project_dir}/.claude/STATE.md
   ```
2. If found, read it and present a brief summary:
   - What was being worked on
   - Any blockers
   - The immediate next step
3. If not found, say: "No STATE.md exists yet. I can create one after we start working."

### Writing/Updating State

1. **Gather current state:**
   - What task/phase is actively being worked on right now
   - Decisions made during this session (with rationale)
   - Open blockers or unanswered questions
   - Explicit next steps (not vague — specific enough to resume cold)
   - Key files modified recently

2. **Check git status** for uncommitted work:
   ```bash
   git status --short
   ```

3. **Write STATE.md** to the project's `.claude/` directory:
   ```markdown
   # Project State
   *Last updated: {YYYY-MM-DD HH:MM}*

   ## Currently Working On
   {Active task or phase — be specific}

   ## Decisions Made
   - {Decision}: {Rationale}

   ## Blockers
   - [ ] {Blocker description}

   ## Next Steps
   1. {Immediate next action — specific enough to start cold}
   2. {Following action}

   ## Recently Modified Files
   - {file path} — {what changed}

   ## Uncommitted Changes
   {List any unstaged/uncommitted work, or "None — clean working tree"}
   ```

4. **Confirm** with a brief summary of what was saved.

## Deconfliction

| Skill | What it tracks | When |
|-------|---------------|------|
| **State** | Current snapshot — where you are *right now* | During session, living document |
| **Diary** | Historical log — what you *did* in a session | End of session, append-only |
| **Project** | Project lifecycle — handoff between sessions | Session boundaries |
| **Work** | Task list — what *needs to be done* | When planning/tracking todos |

State is the **present tense** complement to Diary's **past tense**. State tells you where to resume; Diary tells you what happened.

## Inputs
- Current working context (project, files, git status)
- User's description of current state (or auto-detected from session)

## Outputs
- `{project_dir}/.claude/STATE.md` — updated living document
- Brief confirmation summary

## Example Usage

**User:** "update state"

```
📍 State — Updating project state...

Saved: C:\Projects\AdminStack\.claude\STATE.md

Currently: Building CC Monitor notification system
Blockers: None
Next: Wire up WebSocket events to notification dropdown

This will auto-load next session for seamless pickup.
```

## Level History

- **Lv.1** — Base: Living STATE.md creation and update protocol. Session-start auto-read. Deconfliction with Diary/Project/Work. (Origin: MemStack v3.1, Feb 2026)
