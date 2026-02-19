# MemStack

A structured skill framework for Claude Code. Modular, auto-triggering skills that activate when CC detects specific keywords in your prompts.

## What Is This?

MemStack is CLAUDE.md on steroids. Instead of one big context file, you have **14 modular skills** that activate on demand. Each skill is a self-contained markdown file with trigger keywords, step-by-step instructions, and examples.

When CC sees a trigger keyword in your prompt (like "commit", "recall", or "diagram"), it reads the corresponding skill file and follows its instructions automatically.

## Quick Start

Add this line to the start of any CC session prompt:

```
Read C:\Projects\memstack\MEMSTACK.md and follow the MemStack skill framework.
```

That's it. CC will read the master index and auto-activate skills as needed.

## Skills

| Skill    | What It Does                                    | Trigger Examples                    |
|----------|-------------------------------------------------|-------------------------------------|
| Familiar | Splits tasks across multiple CC sessions        | "dispatch", "send familiar"         |
| Echo     | Recalls information from past sessions          | "recall", "do you remember"         |
| Seal     | Enforces clean git commits with build checks    | "commit", "push"                    |
| Work     | Manages task lists and tracks progress           | "what's next", "todo"               |
| Project  | Saves/restores project state between sessions    | "save project", "handoff"           |
| Grimoire | Manages CLAUDE.md files across projects          | "update context", "save library"    |
| Scan     | Analyzes project scope and suggests pricing      | "scan project", "estimate"          |
| Quill    | Generates professional client quotations         | "create quotation", "proposal"      |
| Forge    | Creates new MemStack skills                      | "forge this", "new skill"           |
| Diary    | Documents session accomplishments                | "save diary", "log session"         |
| Shard    | Refactors large files into smaller modules       | "shard this", "split file"          |
| Sight    | Generates Mermaid architecture diagrams          | "draw", "diagram", "visualize"      |
| Monitor  | Reports session status to AdminStack CC Monitor  | Auto-activates if configured        |
| Deploy   | Verifies builds and guards deployments           | "deploy", "ship it"                 |

## Folder Structure

```
memstack/
├── MEMSTACK.md              # Master index — add this to CC prompts
├── skills/                  # Skill files (one per skill)
│   ├── familiar.md
│   ├── echo.md
│   └── ...
├── memory/
│   ├── sessions/            # Auto-saved session logs (Diary)
│   ├── projects/            # Project state snapshots (Project)
│   └── ideas/               # Idea storage
├── templates/               # Reusable document templates
│   ├── handoff.md
│   ├── project-snapshot.md
│   └── client-quote.md
└── config.json              # Project directories, API keys, defaults
```

## Creating New Skills

Use the **Forge** skill. Say "forge a new skill for [description]" and CC will walk you through the creation process, generate the skill file, and add it to the master index.

Or create one manually following the format in any existing skill file:

```markdown
# [Skill Name] — MemStack Skill

## Trigger Keywords
## Purpose
## Instructions
## Inputs
## Outputs
## Example Usage
```

## Configuration

Edit `config.json` to set:
- **projects** — directory paths, CLAUDE.md locations, deploy targets
- **cc_monitor** — AdminStack CC Monitor API key for auto-reporting
- **defaults** — commit format, auto-diary, auto-monitor toggles

## How Triggers Work

1. You paste `MEMSTACK.md` path into your CC session prompt
2. CC reads the skill index and remembers all trigger keywords
3. When your prompt contains a trigger keyword, CC reads that skill file
4. CC follows the skill's instructions step-by-step
5. Multiple skills can activate in the same session

Skills don't conflict — they're designed to compose. Seal activates after Work finishes. Diary captures what Work accomplished. Monitor reports throughout.
