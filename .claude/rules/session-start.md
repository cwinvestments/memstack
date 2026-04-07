# Session Start — Diary-First Context Loading

When the **first message** in a fresh session references prior work, ALWAYS read the most recent diary entry before taking any other action.

## Trigger Keywords
- "finish", "continue", "pick up", "resume", "where was I", "where did we leave off"
- "Task [number]", "last session", "what was I working on"
- Any reference to ongoing or incomplete work from a previous session

## Protocol
1. Search for the most recent diary: `ls -t memory/sessions/ | head -3` (or check `memory/diary/`)
2. Read the latest entry to restore context — focus on the **Session Handoff** section
3. Summarize what was in progress and any pending items
4. Only THEN proceed with the user's request

## Why
Claude Code starts each session with a blank slate. Without reading the diary first, you will miss critical context: what was in progress, what decisions were made, what's uncommitted, and exactly where to pick up. The 30 seconds spent reading the diary prevents minutes of duplicated work or wrong-direction effort.

## Ownership
- This rule complements the Echo skill (which handles explicit "recall" / "remember" queries)
- This rule handles the implicit case: user jumps straight into work assuming you have context
