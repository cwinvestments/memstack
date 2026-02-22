# MemStack v3.0-rc — Skill Framework for Claude Code

You are running with MemStack enabled. Skills in `C:\Projects\memstack\skills\` activate on keyword/contextual triggers. Hooks in `.claude/hooks/` fire deterministically on CC lifecycle events. Rules in `.claude/rules/` are always loaded at session start.

## Global Rules
See `.claude/rules/memstack.md` for the full rule set. Summary:
1. Read the project's `CLAUDE.md` first if one exists
2. Commit format: `[ProjectName] Brief description` — Co-authored-by Claude
3. Always build before push (enforced by hook)
4. Document decisions in CLAUDE.md
5. Skill chain: Work → Seal (hook) → Diary → Monitor (hook)

## Architecture (v3.0-rc)

MemStack v3.0-rc uses **three layers**:

| Layer | What | How | Examples |
|-------|------|-----|---------|
| **Hooks** | Deterministic safety gates | Shell scripts fired by CC lifecycle events | Seal (pre-push), Deploy (post-commit), Monitor + Headroom + CLAUDE.md indexer (session start/end) |
| **Rules** | Always-on behavioral guidance | Markdown files loaded every session | Echo recall, Diary logging, Work planning, global conventions |
| **Skills** | Context-aware workflows | Markdown protocols activated by keywords/conditions | Echo, Diary, Work, Project, Scan, Quill, Forge, Sight, Shard |

Hooks **always fire** — deterministic. Rules **always load** — persistent behavioral layer. Skills fire when CC detects matching triggers.

### Hook Configuration

Hooks are wired in `.claude/settings.json`:

| Hook Script | CC Event | Behavior |
|-------------|----------|----------|
| `pre-push.sh` | `PreToolUse` (git push) | Build check, secrets scan, commit format — **blocks push on failure** |
| `post-commit.sh` | `PostToolUse` (git commit) | Debug artifact scan, secrets check — **warns after commit** |
| `session-start.sh` | `SessionStart` | **Headroom auto-start** + **CLAUDE.md auto-index** + reports "working" to API |
| `session-end.sh` | `Stop` | Reports "completed" status to monitoring API |

### Rules Configuration

Rules in `.claude/rules/` are loaded automatically every session:

| Rule File | Skill Enhanced | Behavior |
|-----------|---------------|----------|
| `memstack.md` | Global | Commit format, build safety, no secrets, deprecated skill guard |
| `echo.md` | Echo (Lv.4) | Always-on memory recall protocol — search SQLite first |
| `diary.md` | Diary (Lv.4) | Always-on session logging awareness — log after task completion |
| `work.md` | Work (Lv.4) | Always-on task planning protocol — activate on plan/todo/task |
| `headroom.md` | Headroom | Compression proxy awareness — troubleshooting, stats check |

### Slash Commands

| Command | File | Behavior |
|---------|------|----------|
| `/memstack-search <query>` | `.claude/commands/memstack-search.md` | Quick memory search — runs `memstack-db.py search` |
| `/memstack-headroom` | `.claude/commands/memstack-headroom.md` | Headroom proxy status and token savings |

### Hook Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success — continue |
| `1` | Error (logged, continues) |
| `2` | **Block the operation** |

## Trigger Types
- **Keyword** — fires when specific phrases appear in prompt
- **Passive** — always-on background behavior (now hooks in v3.0)
- **Contextual** — fires when conditions are detected (file size, session state)

## Skill Index

| #  | Skill    | Emoji | Type       | Level    | Function                          | Key Triggers                                       |
|----|----------|-------|------------|----------|-----------------------------------|----------------------------------------------------|
| 1  | Familiar | 👻    | Keyword    | Lv.2     | Multi-agent dispatch              | "dispatch", "send familiar", "split task"          |
| 2  | Echo     | 🔊    | Keyword    | **Lv.4** | Memory recall from past sessions  | "recall", "last session", "do you remember" + rule |
| 3  | ~~Seal~~ | 🔒    | ~~Passive~~| **Hook** | ~~Git commit guardian~~ →`.claude/hooks/pre-push.sh` | Deterministic on git push |
| 4  | Work     | 📋    | Keyword    | **Lv.4** | Plan execution (copy/append/resume) | "copy plan", "append plan", "resume plan", "todo" + rule |
| 5  | Project  | 💾    | Contextual | **Lv.3** | Session handoff & lifecycle       | "save project", "handoff", "context running low"   |
| 6  | Grimoire | 📖    | Keyword    | Lv.2     | CLAUDE.md management              | "update context", "update claude", "save library"  |
| 7  | Scan     | 🔍    | Keyword    | Lv.2     | Project analysis & pricing        | "scan project", "estimate", "how much to charge"   |
| 8  | Quill    | ✒️    | Keyword    | Lv.2     | Client quotation generator        | "create quotation", "generate quote", "proposal"   |
| 9  | Forge    | 🔨    | Keyword    | Lv.2     | New skill creation                | "forge this", "new skill", "create enchantment"    |
| 10 | Diary    | 📓    | Contextual | **Lv.4** | Session documentation             | "save diary", "log session", end of session + rule |
| 11 | Shard    | 💎    | Contextual | Lv.2     | Large file refactoring (1000+ LOC)| "shard this", "split file", files over 1K lines    |
| 12 | Sight    | 👁️    | Keyword    | Lv.2     | Architecture visualization        | "draw", "diagram", "visualize", "architecture"     |
| 13 | ~~Monitor~~ | 📡 | ~~Passive~~| **Hook** | ~~CC Monitor self-reporting~~ →`.claude/hooks/session-*.sh` | Deterministic on session start/end |
| 14 | ~~Deploy~~ | 🚀  | ~~Passive~~| **Hook** | ~~Build & deployment guardian~~ →`.claude/hooks/post-commit.sh` | Deterministic on git commit |
| 15 | KDP Format | 📚  | Keyword    | Lv.2     | Markdown → KDP-ready .docx (local only) | "kdp", "format for kdp", "book format", "manuscript" |

## Skill Deconfliction
When multiple skills could activate on the same prompt, use these ownership rules:
- **"commit"** →post-commit hook fires automatically
- **"push" / "ship it" / "deploy"** →pre-push hook blocks if checks fail
- **"build"** →Neither — just run the build command directly
- **"recall" / "remember"** →Echo only (not Diary or Project)
- **"save diary" / "log session"** →Diary only (not Project)
- **"save project" / "handoff"** →Project only (not Diary)
- **"todo" / "plan"** →Work only
- **"/memstack-search"** →Slash command (quick search, no full Echo activation)

## Storage
- **Database (primary):** `C:\Projects\memstack\db\memstack.db` — SQLite with WAL mode
- **DB Helper:** `python C:/Projects/memstack/db/memstack-db.py <command>` — repository pattern CLI
- **Commands:** `init`, `add-session`, `add-insight`, `search`, `get-sessions`, `get-insights`, `get-context`, `set-context`, `add-plan-task`, `get-plan`, `update-task`, `export-md`, `stats`

## Paths
- Skills: `C:\Projects\memstack\skills\` | Hooks: `.claude/hooks/` | Rules: `.claude/rules/` | Commands: `.claude/commands/` | DB: `C:\Projects\memstack\db\` | Config: `config.json`

*Architecture inspired by Developer Kaki's MemoryCore (github.com/Kiyoraka/Project-AI-MemoryCore)*
