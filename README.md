# MemStack v3.0

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE) [![Version: 3.0-rc](https://img.shields.io/badge/Version-3.0--rc-green.svg)](CHANGELOG.md)

A structured skill framework for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) with SQLite-backed persistent memory, deterministic hooks, always-on rules, and slash commands.

Architecture inspired by [Developer Kaki's MemoryCore](https://github.com/Kiyoraka/Project-AI-MemoryCore). SQLite backend inspired by [Accomplish AI](https://github.com/accomplish-ai/accomplish) research. CC native features informed by [claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice).

## Installation

### Manual Setup (Current)

```bash
git clone https://github.com/cwinvestments/memstack.git
cd memstack
cp config.json config.local.json   # Edit with your real paths and API keys
python db/memstack-db.py init      # Initialize SQLite database
```

Add to any CC session prompt:

```
Read /path/to/memstack/MEMSTACK.md and follow the MemStack skill framework.
```

### Package Install (Future)

```bash
npx skills add cwinvestments/memstack
```

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

**Hooks** always fire (deterministic). **Rules** always load (persistent). **Skills** fire on keyword/condition match.

## Slash Commands

| Command | What It Does |
|---------|-------------|
| `/memstack-search <query>` | Search SQLite memory for past sessions, insights, and project context |
| `/memstack-headroom` | Check Headroom proxy status and token savings |

## Skills

| Skill | Emoji | Level | What It Does |
|-------|-------|-------|-------------|
| Familiar | 👻 | Lv.2 | Splits tasks across multiple CC sessions |
| Echo | 🔊 | **Lv.4** | Recalls information from past sessions via SQLite search |
| Work | 📋 | **Lv.4** | Plan execution with SQLite-backed task tracking |
| Project | 💾 | **Lv.3** | Saves/restores project state via SQLite context |
| Grimoire | 📖 | Lv.2 | Manages CLAUDE.md files across projects |
| Scan | 🔍 | Lv.2 | Analyzes project scope and suggests pricing |
| Quill | ✒️ | Lv.2 | Generates professional client quotations |
| Forge | 🔨 | Lv.2 | Creates new MemStack skills |
| Diary | 📓 | **Lv.4** | Documents sessions to SQLite + auto-extracts insights |
| Shard | 💎 | Lv.2 | Refactors large files into smaller modules |
| Sight | 👁️ | Lv.2 | Generates Mermaid architecture diagrams |

Deprecated skills (Seal, Deploy, Monitor) are replaced by deterministic hooks.

## Headroom Integration

MemStack auto-detects and auto-starts the [Headroom](https://github.com/nicobailon/headroom) context compression proxy on session start:

1. **Checks** if Headroom is already running at `localhost:8787`
2. **Auto-starts** it if the `headroom` command is installed but not running
3. **Exports** `ANTHROPIC_BASE_URL` so CC routes through the proxy
4. **Skips silently** if Headroom isn't installed — never blocks session start

Headroom compresses tool outputs by ~34%, extending effective context window. Check status with `/memstack-headroom`.

## Storage

All memory is stored in SQLite (`db/memstack.db`) with WAL mode. CLI access:

```bash
python db/memstack-db.py search "authentication"     # Search everything
python db/memstack-db.py get-sessions AdminStack      # Recent sessions
python db/memstack-db.py get-insights AdminStack      # Decisions and patterns
python db/memstack-db.py stats                        # Database overview
```

| Table | Purpose |
|-------|---------|
| `sessions` | Session diary entries (written by Diary, read by Echo) |
| `insights` | Extracted decisions and patterns |
| `project_context` | Current state of each project (auto-indexed from CLAUDE.md) |
| `plans` | Task lists with per-task status |

## Configuration

Copy `config.json` to `config.local.json` and customize:

- **projects** — directory paths, CLAUDE.md locations, deploy targets
- **cc_monitor** — optional dashboard API URL and key
- **headroom** — auto-start toggle and port (default: 8787)
- **session_limits** — max lines for exports
- **defaults** — commit format, auto-diary, auto-monitor toggles

`config.local.json` is gitignored. `config.json` is the template.

## Migration

From MemStack v2.x:

```bash
python db/memstack-db.py init      # Create/update database
python db/migrate.py               # Import existing markdown files (idempotent)
python db/memstack-db.py stats     # Verify migration
```

## Creating Skills

Use the **Forge** skill: say `"forge a new skill for [description]"`. Forge generates the file with YAML frontmatter and updates the master index.

## License

MIT — see [LICENSE](LICENSE) for details.

Copyright (c) 2026 CW Affiliate Investments LLC
