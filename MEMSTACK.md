# MemStack v1.0 — Skill Framework for Claude Code

You are running with MemStack enabled. This file is your skill index.

## How It Works

When you detect a **trigger keyword** in the user's prompt, read the corresponding skill file from `C:\Projects\memstack\skills\` and follow its instructions. Skills are self-contained — each file tells you exactly what to do.

## Global Rules

1. Always read the project's `CLAUDE.md` first if one exists
2. Never commit `node_modules/`, `.env`, or build artifacts
3. Run `npm run build` before any git push
4. Use commit format: `[ProjectName] Brief description`
5. If `cc_monitor.api_key` is set in `config.json`, activate Monitor skill automatically

## Skill Index

| #  | Skill    | Function                            | Triggers                                          |
|----|----------|-------------------------------------|---------------------------------------------------|
| 1  | Familiar | Multi-agent dispatch                | "dispatch", "send familiar", "split task"         |
| 2  | Echo     | Memory recall from past sessions    | "recall", "last session", "do you remember"       |
| 3  | Seal     | Git commit guardian                 | "commit", "push", end of any task                 |
| 4  | Work     | Plan execution & TODO tracking      | "copy plan", "what's next", "todo", "priorities"  |
| 5  | Project  | Session handoff & lifecycle         | "save project", "handoff", "context running low"  |
| 6  | Grimoire | Knowledge library & CLAUDE.md mgmt  | "save library", "update context", "update claude" |
| 7  | Scan     | Project analysis & pricing          | "scan project", "estimate", "how much to charge"  |
| 8  | Quill    | Client quotation generator          | "create quotation", "generate quote", "proposal"  |
| 9  | Forge    | Self-improvement & new skills       | "forge this", "new skill", "create enchantment"   |
| 10 | Diary    | Session documentation               | "save diary", "log session", end of session       |
| 11 | Shard    | Large file refactoring (1000+ LOC)  | "shard this", "refactor", "split file"            |
| 12 | Sight    | Architecture visualization          | "draw", "diagram", "visualize", "architecture"    |
| 13 | Monitor  | CC Monitor self-reporting           | Auto-activates if API key is configured            |
| 14 | Deploy   | Build verification & deployment     | "deploy", "ship it", before any git push           |

## Config Location

`C:\Projects\memstack\config.json` — project directories, deploy targets, CC Monitor API key.

## Paths

- Skills: `C:\Projects\memstack\skills\`
- Memory: `C:\Projects\memstack\memory\`
- Templates: `C:\Projects\memstack\templates\`
