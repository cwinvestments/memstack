---
name: diary
description: "Use when the user says 'save diary', 'log session', 'wrapping up', or at end of a productive session."
version: 1.0.0
---


# 📓 Diary — Logging Session...
*Document what was accomplished in each CC session for future recall.*

## Activation

When this skill activates, output:

`📓 Diary — Logging session...`

Then execute the protocol below.

## Context Guard

| Context | Status | Priority |
|---------|--------|----------|
| **User says "save diary", "log session", "write diary"** | ACTIVE — write diary | P1 |
| **User explicitly says they're done ("that's it", "wrapping up")** | ACTIVE — suggest diary if work was done | P2 |
| **Multi-agent session (Builder/Reviewer role)** | DORMANT — Manager handles diary | — |
| **Mid-session, user is actively coding** | DORMANT — don't interrupt flow | — |
| **Casual conversation, no code changes made** | DORMANT — nothing to log | — |
| **User asks to recall past sessions ("what did we do")** | DORMANT — Echo handles recall, not Diary | — |
| **User says "save project" or "handoff"** | DORMANT — Project skill handles this | — |
| **Session just started, no work yet** | DORMANT — nothing to log | — |

## When NOT to Fire

- **Do NOT fire autonomously.** Only activate when the user explicitly requests it ("save diary", "log session", "wrapping up").
- **Multi-agent sessions:** If you are operating as Builder, Reviewer, or any non-Manager agent in a multi-agent session, do NOT fire diary. Only the Manager or a standalone session should trigger diary.
- **No work done:** If no meaningful changes were made (no commits, no file edits), skip diary.

## Reminders

When the user asks to save a diary, keep these in mind:

| Temptation | Why it matters |
|---|---|
| "Nothing important happened" | Even small decisions have context worth capturing. |
| "Commits capture everything" | Commits don't capture decisions, blockers, or next steps. |
| "Skip the handoff section" | Handoffs are the most valuable part for session continuity. |

## Protocol

1. **Summarize the session:**
   - Project name and working directory
   - Date and approximate duration
   - What was built or changed
   - Key files created or modified
   - Commits made (hashes and messages)
   - Decisions made and why
   - Problems encountered and solutions

2. **Check git log** for commits:
   ```bash
   git log --oneline -10
   ```

3. **Format the diary entry:**
   ```markdown
   # Session Diary — {project} — {date}

   ## Accomplished
   - Item 1...

   ## Files Changed
   - path/to/file.ts — description

   ## Commits
   - abc1234 Message

   ## Decisions
   - Decision: reason

   ## Next Steps
   - What to do next

   ## Session Handoff
   **In Progress:** [what was actively being worked on when session ended]
   **Uncommitted Changes:** [list any unstaged/uncommitted work, or "None"]
   **Pick Up Here:** [exact instruction for next session — specific enough to start cold]
   **Session Context:** [anything important that isn't captured elsewhere — temp decisions, debugging state, gotchas discovered]
   ```

4. **Save to SQLite database** (primary storage):
   ```bash
   python C:/Projects/memstack/db/memstack-db.py add-session '{"project":"<name>","date":"<YYYY-MM-DD>","accomplished":"<bullets>","files_changed":"<bullets>","commits":"<bullets>","decisions":"<bullets>","problems":"<bullets>","next_steps":"<bullets>","duration":"<estimate>","raw_markdown":"<full text>"}'
   ```

5. **Also save decisions as insights** for cross-project search:
   ```bash
   python C:/Projects/memstack/db/memstack-db.py add-insight '{"project":"<name>","type":"decision","content":"<decision>","context":"Session <date>","tags":"<project>"}'
   ```

6. **Update project context** with last session date:
   ```bash
   python C:/Projects/memstack/db/memstack-db.py set-context '{"project":"<name>","last_session_date":"<YYYY-MM-DD>"}'
   ```

7. **Also save markdown copy** to `memory/sessions/{date}-{project}.md` (export format, human-readable backup)

## Session File Size Management

The 500-line limit on markdown files is no longer a concern since SQLite is the source of truth.
Markdown files in `memory/sessions/` are now just human-readable exports.
Old markdown files are preserved but not the primary storage.

## Inputs
- Current session context
- Project name from working directory or config.json
- Git log for commit history

## Outputs
- Session entry in SQLite database
- Insights extracted from decisions
- Markdown backup in memory/sessions/
- Brief confirmation summary

## Example Usage

**User:** "save diary"

```
📓 Diary — Logging session...

Saved: memory/sessions/2026-02-18-adminstack.md

Project: AdminStack | Duration: ~2 hours
Accomplished: Built CC Monitor page, API routes, setup guide
Commits: 4 (45b4c42, d1c7e11, f6c8e18, f0e793f)
Files changed: 8

This session is now searchable via Echo.
```

## PreCompact Hook — Automatic Compaction Diary

The diary system includes an automatic `PreCompact` hook that fires before Claude Code compresses the context window. This closes the gap where session context could be lost during long conversations.

### Behavior
- **Trigger:** Fires automatically before every CC context compaction — no user action required
- **Output:** `.claude/diary/{date}-compaction.md` — one file per day, appends on multiple compactions
- **Flag:** Every entry includes `COMPACTION_INTERRUPTED` so the next session knows context was cut
- **Timeout:** 15 seconds — fast enough to never block compaction

### What It Captures
| Data | Source |
|------|--------|
| Uncommitted changes | `git status --short` |
| Recent commits | `git log --oneline -5` |
| Recent shell commands | Shell history (last 5) |
| Recently modified files | Files modified since last git operation |
| Branch and project | Git branch + directory name |

### How It Differs from Manual Diary
| | Manual Diary | PreCompact Diary |
|---|---|---|
| **Trigger** | User says "save diary" | Automatic before compaction |
| **Content** | Full narrative with decisions, handoff | Snapshot of working state |
| **Storage** | SQLite + `memory/sessions/` | `.claude/diary/` only |
| **Purpose** | Session documentation | Context recovery after compaction |

### Session Resume
When resuming after compaction, check `.claude/diary/` for entries with today's date. The `COMPACTION_INTERRUPTED` flag signals that the previous context was truncated and these files contain the lost state.

### Configuration
Hook is registered in `.claude/settings.json` under `PreCompact`. Script lives at `.claude/hooks/pre-compact.sh`. Always exits 0 — must never block compaction.

## Full Hook System (v3.3.2)

The Diary skill is part of a broader hook system that automates session lifecycle, security, and observability. All hooks follow the same defensive pattern: `set -uo pipefail`, `SCRIPT_DIR` resolution, all external commands wrapped with fallbacks, guaranteed `exit 0`.

### Hook Registry — 7 hooks across 5 events

| Event | Script | Matcher | Timeout | Purpose |
|-------|--------|---------|---------|---------|
| **PreToolUse** | `pre-tool-notify.sh` | `Write\|Edit\|MultiEdit\|Bash` | 10s | TTS voice alert before approval prompts |
| **PreToolUse** | `pre-push.sh` | `Bash` (git push) | 60s | Build verification + secrets scan before push |
| **PostToolUse** | `post-commit.sh` | `Bash` (git commit) | 10s | Debug artifact + secrets scan after commit |
| **PostToolUse** | `post-tool-monitor.sh` | `Write\|Edit\|MultiEdit\|Bash` | 10s | Observation capture — logs tool calls to `.claude/observations/` |
| **SessionStart** | `session-start.sh` | *(all)* | 10s | Headroom proxy start, CLAUDE.md indexing, monitoring ping |
| **SessionStart** | `session-context-load.sh` | *(all)* | 15s | Context injection — last 3 diary + observation summaries → `.claude/session-context.md` |
| **Stop** | `session-end.sh` | *(all)* | 10s | Monitoring API session-complete ping |
| **PreCompact** | `pre-compact.sh` | *(all)* | 15s | Auto-save diary snapshot before context compaction |

### Architecture Notes

- Each hook is registered as an **independent entry** (Option B) in `settings.json`, giving it its own timeout budget
- PreToolUse hooks can **block** tool execution (exit 2 = block). All other hooks are non-blocking
- PostToolUse observation monitor writes to `.claude/observations/YYYY-MM-DD.md` — daily files, append-only
- SessionStart context loader is **idempotent** — overwrites `.claude/session-context.md` on each new session
- Both `.claude/observations/` and `.claude/session-context.md` are in `.gitignore` (ephemeral runtime output)
- All scripts live in `.claude/hooks/` and use `${CLAUDE_PROJECT_DIR}` for portable path resolution

## Level History

- **Lv.1** — Base: Session logging with git integration. (Origin: MemStack v1.0, Feb 2026)
- **Lv.2** — Enhanced: Added YAML frontmatter, context guard, 500-line limit with archive, activation message. (Origin: MemStack v2.0 MemoryCore merge, Feb 2026)
- **Lv.3** — Advanced: SQLite as primary storage, auto-extract insights from decisions, markdown as backup export. (Origin: MemStack v2.1 Accomplish-inspired upgrade, Feb 2026)
- **Lv.4** — Native: CC rules integration (`.claude/rules/diary.md`), always-on session logging awareness without skill file read. (Origin: MemStack v3.0-beta, Feb 2026)
- **Lv.5** — Handoff: Added structured Session Handoff section — in-progress work, uncommitted changes, exact pickup instructions, session context preservation. (Origin: MemStack v3.1, Feb 2026)
- **Lv.6** — PreCompact: Added automatic PreCompact hook — saves working state snapshot before CC context compaction, captures uncommitted changes, recent commands, and modified files with COMPACTION_INTERRUPTED flag. (Origin: MemStack v3.3.1, Mar 2026)
- **Lv.7** — Hook System: Documented full 7-hook system across 5 CC lifecycle events — PreToolUse (TTS + pre-push), PostToolUse (post-commit + observation monitor), SessionStart (Headroom + context injection), Stop, PreCompact. (Origin: MemStack v3.3.2, Mar 2026)
