# MemStack v2.1

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A structured skill framework for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) with SQLite-backed persistent memory. Modular, auto-triggering skills that activate when Claude Code detects specific keywords, conditions, or background events in your prompts.

Architecture inspired by [Developer Kaki's MemoryCore](https://github.com/Kiyoraka/Project-AI-MemoryCore). SQLite backend inspired by [Accomplish AI](https://github.com/accomplish-ai/accomplish) research.

## Quick Start

1. Clone this repo somewhere on your machine
2. Copy `config.json` and fill in your project paths and (optional) API keys
3. Add this line to the start of any Claude Code session prompt:

```
Read /path/to/memstack/MEMSTACK.md and follow the MemStack skill framework.
```

Claude Code reads the master index, remembers all triggers, and auto-activates skills as needed.

4. Initialize the SQLite database:

```bash
python db/memstack-db.py init
```

## How Skills Work

Each skill is a self-contained markdown file with YAML frontmatter for auto-discovery. When CC detects a trigger, it reads the skill file and follows its protocol.

### Trigger Types

| Type | Behavior | Examples |
|------|----------|---------|
| **Keyword** | Fires when specific phrases appear in prompt | "commit", "diagram", "recall" |
| **Passive** | Always-on background behavior | Monitor, Seal, Deploy |
| **Contextual** | Fires when conditions are detected | File over 1K lines, session ending, context low |

### Skill Deconfliction

When multiple skills could activate on the same prompt, ownership rules apply:

| Trigger | Owner | Not |
|---------|-------|-----|
| "commit" | Seal | Deploy |
| "push" / "ship it" / "deploy" | Deploy | Seal |
| "build" | Neither | Just run the command |
| "recall" / "remember" | Echo | Diary, Project |
| "save diary" / "log session" | Diary | Project |
| "save project" / "handoff" | Project | Diary |
| "todo" / "plan" | Work | — |

### Activation Messages

Every skill outputs a visible activation line when it fires:

```
🔒 Seal — Clean commits, every time.
📋 Work — Plan execution engaged.
📡 Monitor — Reporting status...
```

### Leveling System

Skills evolve through levels as they're improved:

- **Lv.1** — Base capability (initial creation)
- **Lv.2** — Enhanced (YAML frontmatter, context guards, activation messages)
- **Lv.3** — Advanced (SQLite backend, proactive behavior, deep cross-skill integration)
- **Lv.4+** — Expert (fully autonomous, handles edge cases gracefully)

Core skills (Echo, Diary, Work, Project) are at **Lv.3**. Others at Lv.2.

## Skills

| Skill | Emoji | Type | Level | What It Does |
|-------|-------|------|-------|-------------|
| Familiar | 👻 | Keyword | Lv.2 | Splits tasks across multiple CC sessions |
| Echo | 🔊 | Keyword | **Lv.3** | Recalls information from past sessions via SQLite search |
| Seal | 🔒 | Passive | Lv.2 | Enforces clean git commits with build checks |
| Work | 📋 | Keyword | **Lv.3** | Plan execution with SQLite-backed task tracking |
| Project | 💾 | Contextual | **Lv.3** | Saves/restores project state via SQLite context |
| Grimoire | 📖 | Keyword | Lv.2 | Manages CLAUDE.md files across projects |
| Scan | 🔍 | Keyword | Lv.2 | Analyzes project scope and suggests pricing |
| Quill | ✒️ | Keyword | Lv.2 | Generates professional client quotations |
| Forge | 🔨 | Keyword | Lv.2 | Creates new MemStack skills |
| Diary | 📓 | Contextual | **Lv.3** | Documents sessions to SQLite + auto-extracts insights |
| Shard | 💎 | Contextual | Lv.2 | Refactors large files into smaller modules |
| Sight | 👁️ | Keyword | Lv.2 | Generates Mermaid architecture diagrams |
| Monitor | 📡 | Passive | Lv.2 | Reports session status to external dashboard |
| Deploy | 🚀 | Passive | Lv.2 | Verifies builds and guards deployments |

## Storage Architecture

### SQLite Database (Primary — v2.1+)

All memory is stored in `db/memstack.db` using SQLite with WAL mode. Skills access it via the repository pattern CLI:

```bash
python db/memstack-db.py <command> [args...]
```

**Tables:**

| Table | Purpose | Used By |
|-------|---------|---------|
| `sessions` | Session diary entries | Diary (write), Echo (read) |
| `insights` | Extracted decisions and patterns | Diary (write), Echo (read) |
| `project_context` | Current state of each project | Project (read/write) |
| `plans` | Task lists with per-task status | Work (read/write) |

**Commands:**

| Command | Description |
|---------|-------------|
| `init` | Initialize or migrate the database |
| `add-session <json>` | Add a session diary entry |
| `add-insight <json>` | Add an insight or decision |
| `search <query>` | Full-text search across all tables |
| `get-sessions <project>` | Get recent sessions for a project |
| `get-insights <project>` | Get insights for a project |
| `get-context <project>` | Get project context |
| `set-context <json>` | Upsert project context |
| `add-plan-task <json>` | Add a task to a project plan |
| `get-plan <project>` | Get all plan tasks for a project |
| `update-task <json>` | Update a plan task status |
| `export-md <project>` | Export project memory as markdown |
| `stats` | Show database statistics |

### Markdown (Legacy Fallback + Export)

Markdown files in `memory/` are preserved as human-readable backups and for backwards compatibility. SQLite is the source of truth; markdown is the export format.

- `memory/sessions/` — Session diary exports (written by Diary alongside SQLite)
- `memory/projects/` — Project handoffs and plans (written by Project/Work alongside SQLite)

## Work Skill — 3 Modes

The Work skill is the backbone for task management across CC sessions, now backed by SQLite:

- **Copy Mode** (`"copy plan"`) — parses plan into individual tasks, saves each to the `plans` table
- **Append Mode** (`"append plan"`) — updates individual task statuses in the database
- **Resume Mode** (`"resume plan"`) — loads plan from SQLite and shows progress summary

Quick commands: `"what's next"`, `"priorities"`, `"todo"`

## Folder Structure

```
memstack/
├── MEMSTACK.md              # Master index (add to CC prompts)
├── config.json              # Projects, API keys, limits
├── CHANGELOG.md             # Version history
├── README.md                # This file
├── db/
│   ├── memstack.db          # SQLite database (primary storage)
│   ├── schema.sql           # Database schema (4 tables)
│   ├── memstack-db.py       # Repository pattern CLI helper
│   └── migrate.py           # Markdown → SQLite migration (idempotent)
├── skills/                  # 14 skill files with YAML frontmatter
├── memory/
│   ├── session-format.md    # Active session template
│   ├── main-memory-format.md # Project memory template
│   ├── sessions/            # Session diary exports (legacy + backup)
│   │   └── archive/         # Archived logs
│   ├── projects/            # Project handoffs & plans (legacy + backup)
│   └── ideas/               # Idea storage
├── templates/               # Document templates (handoff, quote, snapshot)
└── research/                # Research reports (e.g., Accomplish comparison)
```

## Creating New Skills

Use the **Forge** skill: say `"forge a new skill for [description]"`. Forge walks you through creation, generates the file with proper YAML frontmatter, and updates the master index.

## Configuration

Copy `config.json` and customize for your setup:
- **projects** — directory paths, CLAUDE.md locations, deploy targets
- **cc_monitor** — optional dashboard API URL and key (for Monitor skill)
- **session_limits** — max lines for session log exports (500) and plan exports (1000)
- **defaults** — commit format, auto-diary, auto-monitor toggles

Keep your real config in `config.local.json` (gitignored) — `config.json` is the template.

## Migration from v2.0

If upgrading from MemStack v2.0 (markdown-only):

```bash
python db/memstack-db.py init      # Create the database
python db/migrate.py               # Import existing markdown files (idempotent)
python db/memstack-db.py stats     # Verify migration
```

Existing markdown files are preserved. Skills will use SQLite as primary and fall back to markdown if the database entry is missing.

## License

MIT — see [LICENSE](LICENSE) for details.
