# MemStack v2.0

A structured skill framework for Claude Code. Modular, auto-triggering skills that activate when CC detects specific keywords, conditions, or background events in your prompts.

Architecture inspired by [Developer Kaki's MemoryCore](https://github.com/Kiyoraka/Project-AI-MemoryCore).

## Quick Start

Add this line to the start of any CC session prompt:

```
Read C:\Projects\memstack\MEMSTACK.md and follow the MemStack skill framework.
```

CC reads the master index, remembers all triggers, and auto-activates skills as needed.

## How Skills Work

Each skill is a self-contained markdown file with YAML frontmatter for auto-discovery. When CC detects a trigger, it reads the skill file and follows its protocol.

### Trigger Types

| Type | Behavior | Examples |
|------|----------|---------|
| **Keyword** | Fires when specific phrases appear in prompt | "commit", "diagram", "recall" |
| **Passive** | Always-on background behavior | Monitor, Seal, Deploy |
| **Contextual** | Fires when conditions are detected | File over 1K lines, session ending, context low |

### Activation Messages

Every skill outputs a visible activation line when it fires:

```
🔒 Seal — Clean commits, every time.
📋 Work — Plan execution engaged.
📡 Monitor — Reporting to AdminStack...
```

### Leveling System

Skills evolve through levels as they're improved:

- **Lv.1** — Base capability (initial creation)
- **Lv.2** — Enhanced (YAML frontmatter, context guards, activation messages)
- **Lv.3** — Advanced (proactive behavior, deep cross-skill integration)
- **Lv.4+** — Expert (fully autonomous, handles edge cases gracefully)

## Skills

| Skill | Emoji | Type | What It Does |
|-------|-------|------|-------------|
| Familiar | 👻 | Keyword | Splits tasks across multiple CC sessions |
| Echo | 🔊 | Keyword | Recalls information from past sessions |
| Seal | 🔒 | Passive | Enforces clean git commits with build checks |
| Work | 📋 | Keyword | Plan execution with 3 modes: copy/append/resume |
| Project | 💾 | Contextual | Saves/restores project state between sessions |
| Grimoire | 📖 | Keyword | Manages CLAUDE.md files across projects |
| Scan | 🔍 | Keyword | Analyzes project scope and suggests pricing |
| Quill | ✒️ | Keyword | Generates professional client quotations |
| Forge | 🔨 | Keyword | Creates new MemStack skills |
| Diary | 📓 | Contextual | Documents session accomplishments |
| Shard | 💎 | Contextual | Refactors large files into smaller modules |
| Sight | 👁️ | Keyword | Generates Mermaid architecture diagrams |
| Monitor | 📡 | Passive | Reports session status to AdminStack CC Monitor |
| Deploy | 🚀 | Passive | Verifies builds and guards deployments |

## Work Skill — 3 Modes

The Work skill is the backbone for task management across CC sessions:

- **Copy Mode** (`"copy plan"`) — captures the entire current plan into memory. Use when starting fresh.
- **Append Mode** (`"append plan"`) — adds latest progress to existing plan. Keeps file under 1K lines by summarizing old entries.
- **Resume Mode** (`"resume plan"`) — restores plan context after CC compact or new session. Reads the saved plan and picks up where you left off.

Quick commands: `"what's next"`, `"priorities"`, `"todo"`

## Session Memory Management

Session logs have a **500-line limit**. When a log approaches the limit, Diary creates a recap summary and archives the full log to `memory/sessions/archive/`. This prevents stale context from bloating the context window.

Templates in `memory/`:
- `session-format.md` — active session state template
- `main-memory-format.md` — persistent project memory template

## Folder Structure

```
memstack/
├── MEMSTACK.md              # Master index (add to CC prompts)
├── config.json              # Projects, API keys, limits
├── skills/                  # 14 skill files with YAML frontmatter
├── memory/
│   ├── session-format.md    # Active session template
│   ├── main-memory-format.md # Project memory template
│   ├── sessions/            # Session logs (Diary)
│   │   └── archive/         # Archived logs over 500 lines
│   ├── projects/            # Project state snapshots & plans (Work, Project)
│   └── ideas/               # Idea storage
└── templates/               # Document templates (handoff, quote, snapshot)
```

## Creating New Skills

Use the **Forge** skill: say `"forge a new skill for [description]"`. Forge walks you through creation, generates the file with proper YAML frontmatter, and updates the master index.

## Configuration

Edit `config.json`:
- **projects** — directory paths, CLAUDE.md locations, deploy targets
- **cc_monitor** — AdminStack CC Monitor API URL and key
- **session_limits** — max lines for session logs (500) and plans (1000)
- **defaults** — commit format, auto-diary, auto-monitor toggles
