# MemStack v3.0

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE) [![Version: 3.0-rc](https://img.shields.io/badge/Version-3.0--rc-green.svg)](CHANGELOG.md)

A structured skill framework for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) with SQLite-backed persistent memory, deterministic hooks, always-on rules, and slash commands.

## What It Does

MemStack gives Claude Code **persistent memory** across sessions, **automated safety checks** on every commit and push, and **context compression** to make your sessions last longer.

## Prerequisites

- **Claude Code** — Install guide: https://docs.anthropic.com/en/docs/claude-code
- **Python 3.10+** — Download: https://www.python.org/downloads/
- **Git** — Download: https://git-scm.com/downloads

## Quick Start

### Step 1: Clone the repo
```bash
git clone https://github.com/cwinvestments/memstack.git
cd memstack
```

### Step 2: Create your local config
```bash
cp config.json config.local.json
```

Open `config.local.json` and edit the `projects` section with your actual paths:

Windows: `"path": "C:\\Projects\\my-app"`

Mac/Linux: `"path": "/home/user/projects/my-app"`

Everything else works with defaults.

### Step 3: Initialize the database
```bash
python db/memstack-db.py init
```

### Step 4: Use it

Add this to the start of every Claude Code prompt:

Windows: `Read C:\Projects\memstack\MEMSTACK.md and follow the MemStack skill framework.`

Mac/Linux: `Read /home/user/memstack/MEMSTACK.md and follow the MemStack skill framework.`

### Step 5 (Optional): Install Headroom

[Headroom](https://github.com/chopratejas/headroom) compresses tool outputs by ~34%, making sessions last longer.
```bash
pip install headroom-ai
```

MemStack auto-detects and auto-starts it. To make permanent:

Windows: `setx ANTHROPIC_BASE_URL http://127.0.0.1:8787`

Mac/Linux: `echo 'export ANTHROPIC_BASE_URL=http://127.0.0.1:8787' >> ~/.bashrc && source ~/.bashrc`

## Three-Layer Architecture

MemStack v3.0 uses three layers with increasing reliability:

```
MemStack v3.0
├── Hooks (deterministic)        — Shell scripts, CC lifecycle events
│   ├── pre-push.sh              — Build check, secrets scan, blocks bad pushes
│   ├── post-commit.sh           — Debug artifacts, format validation
│   ├── session-start.sh         — Headroom auto-start + CLAUDE.md indexer + API monitor
│   └── session-end.sh           — Report "completed" to monitoring API
├── Rules (always-loaded)        — Markdown files, loaded every session
│   ├── memstack.md              — Global conventions, deprecated skill guard
│   ├── echo.md                  — Memory recall protocol
│   ├── diary.md                 — Session logging protocol
│   ├── work.md                  — Task planning protocol
│   └── headroom.md              — Compression proxy awareness
├── Commands (slash)             — Quick-access utilities
│   ├── memstack-search.md       — /memstack-search <query>
│   └── memstack-headroom.md     — /memstack-headroom (proxy stats)
└── Skills (context-aware)       — Markdown protocols, keyword triggers
    ├── Echo, Diary, Work        — SQLite-backed memory (Lv.4)
    ├── Project, Grimoire        — Session lifecycle (Lv.2-3)
    ├── Scan, Quill              — Business tools (Lv.2)
    └── Forge, Shard, Sight      — Dev tools (Lv.2)
```

**Hooks** always fire (deterministic, zero tokens). **Rules** always load (persistent awareness). **Skills** fire on keyword/condition match.

## Slash Commands

| Command | What It Does |
|---------|-------------|
| `/memstack-search <query>` | Search SQLite memory for past sessions, insights, and project context |
| `/memstack-headroom` | Check Headroom proxy status and token savings |

## Skills

| Skill | Emoji | Level | What It Does |
|-------|-------|-------|-------------|
| Echo | 🔊 | **Lv.4** | Recalls information from past sessions via SQLite search |
| Work | 📋 | **Lv.4** | Plan execution with SQLite-backed task tracking |
| Diary | 📓 | **Lv.4** | Documents sessions to SQLite + auto-extracts insights |
| Project | 💾 | **Lv.3** | Saves/restores project state via SQLite context |
| Grimoire | 📖 | Lv.2 | Manages CLAUDE.md files across projects |
| Familiar | 👻 | Lv.2 | Splits tasks across multiple CC sessions |
| Scan | 🔍 | Lv.2 | Analyzes project scope and suggests pricing |
| Quill | ✒️ | Lv.2 | Generates professional client quotations |
| Forge | 🔨 | Lv.2 | Creates new MemStack skills |
| Shard | 💎 | Lv.2 | Refactors large files into smaller modules |
| Sight | 👁️ | Lv.2 | Generates Mermaid architecture diagrams |

Deprecated skills (Seal, Deploy, Monitor) have been replaced by deterministic hooks that always fire — no LLM required.

## Storage

All memory is stored in SQLite (`db/memstack.db`) with WAL mode:
```bash
python db/memstack-db.py search "authentication"     # Search everything
python db/memstack-db.py get-sessions my-app          # Recent sessions
python db/memstack-db.py get-insights my-app          # Decisions and patterns
python db/memstack-db.py stats                        # Database overview
```

| Table | Purpose |
|-------|---------|
| `sessions` | Session diary entries (written by Diary, read by Echo) |
| `insights` | Extracted decisions and patterns |
| `project_context` | Current state of each project (auto-indexed from CLAUDE.md) |
| `plans` | Task lists with per-task status |

## Configuration Reference

`config.local.json` sections:

| Section | Required | Purpose |
|---------|----------|---------|
| `projects` | Yes | Your project paths and CLAUDE.md locations |
| `headroom` | No | Context compression settings (port, auto-start) |
| `cc_monitor` | No | External dashboard API URL and key |
| `session_limits` | No | Max lines for session log exports (default: 500) |
| `defaults` | No | Commit format, auto-diary, auto-monitor toggles |

## Upgrading from v2.x
```bash
git pull
python db/memstack-db.py init      # Update database schema
python db/migrate.py               # Import existing markdown files (safe to re-run)
python db/memstack-db.py stats     # Verify migration
```

## Creating Custom Skills

Use the **Forge** skill: say `"forge a new skill for [description]"` in any CC session. Forge generates the file with YAML frontmatter and registers it in the master index.

## Troubleshooting

**"Python was not found"** — Install Python 3.10+ and make sure "Add Python to PATH" is checked during install. Restart your terminal after installing.

**CC sessions not using Headroom** — Run `headroom proxy` in a separate terminal first, then launch CC. Or install permanently with `setx ANTHROPIC_BASE_URL http://127.0.0.1:8787` (Windows).

**Hook errors on push** — The pre-push hook blocks pushes that contain secrets or fail build checks. Fix the issue it reports, then push again.

**"Database locked" errors** — Close any other process accessing `db/memstack.db`, or delete the `.db-wal` and `.db-shm` files and retry.

## License

MIT — see [LICENSE](LICENSE) for details.

Copyright (c) 2026 CW Affiliate Investments LLC
