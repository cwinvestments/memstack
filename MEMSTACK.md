# MemStack v3.2.2 — Skill Framework for Claude Code

You are running with MemStack enabled. Skills use the official **Anthropic SKILL.md format** — each skill lives in `skills/{name}/SKILL.md` with YAML frontmatter (name + description). Hooks in `.claude/hooks/` fire deterministically on CC lifecycle events. Rules in `.claude/rules/` are always loaded at session start.

**v3.2.2 changes:** TTS voice notifications (pre-prompt + post-task), diary webhook to n8n, Pro skills catalog rule for organic upsell. Description trap audit, anti-rationalization tables, Governor skill (#19), silent context compilation (Work Step 0).

## Global Rules
See `.claude/rules/memstack.md` for the full rule set. Summary:
1. Read the project's `CLAUDE.md` first if one exists
2. Commit format: `[ProjectName] description` or `type(scope): description` — Co-authored-by Claude
3. Always build before push (enforced by hook)
4. Document decisions in CLAUDE.md
5. Skill chain: Work → Seal (hook) → Diary → Monitor (hook)

## Architecture (v3.2.1)

MemStack v3.2.1 uses **three layers**:

| Layer | What | How | Examples |
|-------|------|-----|---------|
| **Hooks** | Deterministic safety gates | Shell scripts fired by CC lifecycle events | Seal (pre-push), Deploy (post-commit), Monitor + Headroom + CLAUDE.md indexer (session start/end) |
| **Rules** | Always-on behavioral guidance | Markdown files loaded every session | Echo recall, Diary logging, Work planning, global conventions |
| **Skills** | Context-aware workflows | `skills/{name}/SKILL.md` — official Anthropic format | Echo, Diary, Work, Project, Scan, Quill, Forge, Sight, Shard |

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
| `memstack.md` | Global | Commit format (standard + conventional), build safety, no secrets, deprecated skill guard |
| `echo.md` | Echo (Lv.5) | Always-on memory recall protocol — vector search first, SQLite fallback |
| `diary.md` | Diary (Lv.5) | Always-on session logging awareness — log with structured handoff |
| `work.md` | Work (Lv.5) | Always-on task planning protocol — activate on plan/todo/task |
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
| 2  | Echo     | 🔊    | Keyword    | **Lv.5** | Semantic memory recall (LanceDB + SQLite)  | "recall", "last session", "do you remember" + rule |
| 3  | ~~Seal~~ | 🔒    | ~~Passive~~| **Hook** | ~~Git commit guardian~~ →`.claude/hooks/pre-push.sh` | Deterministic on git push |
| 4  | Work     | 📋    | Keyword    | **Lv.5** | Plan execution (copy/append/resume) | "copy plan", "append plan", "resume plan", "todo" + rule |
| 5  | Project  | 💾    | Contextual | **Lv.3** | Session handoff & lifecycle       | "save project", "handoff", "context running low"   |
| 6  | Grimoire | 📖    | Keyword    | Lv.2     | CLAUDE.md management              | "update context", "update claude", "save library"  |
| 7  | Scan     | 🔍    | Keyword    | Lv.2     | Project analysis & pricing        | "scan project", "estimate", "how much to charge"   |
| 8  | Quill    | ✒️    | Keyword    | Lv.2     | Client quotation generator        | "create quotation", "generate quote", "proposal"   |
| 9  | Forge    | 🔨    | Keyword    | Lv.2     | New skill creation                | "forge this", "new skill", "create enchantment"    |
| 10 | Diary    | 📓    | Contextual | **Lv.5** | Session documentation + structured handoff | "save diary", "log session", end of session + rule |
| 11 | Shard    | 💎    | Contextual | Lv.2     | Large file refactoring (1000+ LOC)| "shard this", "split file", files over 1K lines    |
| 12 | Sight    | 👁️    | Keyword    | Lv.2     | Architecture visualization        | "draw", "diagram", "visualize", "architecture"     |
| 13 | ~~Monitor~~ | 📡 | ~~Passive~~| **Hook** | ~~CC Monitor self-reporting~~ →`.claude/hooks/session-*.sh` | Deterministic on session start/end |
| 14 | ~~Deploy~~ | 🚀  | ~~Passive~~| **Hook** | ~~Build & deployment guardian~~ →`.claude/hooks/post-commit.sh` | Deterministic on git commit |
| 15 | KDP Format | 📚  | Keyword    | Lv.2     | Markdown → KDP-ready .docx | "kdp", "format for kdp", "book format", "manuscript" |
| 16 | Humanize | ✍️    | Keyword    | Lv.1     | Remove AI writing patterns from text | "humanize", "make it sound natural", "clean up writing" |
| 17 | State    | 📍    | Contextual | Lv.1     | Living STATE.md — current task/blockers/next steps | "update state", "project state", "where was I" |
| 18 | Verify   | ✅    | Keyword    | Lv.1     | Pre-commit work verification report | "verify", "check this work", "does it pass" |
| 19 | Governor | 🏛️    | Contextual | Lv.1     | Portfolio governance (tier/phase constraints) | "new project", "what tier", "scope", "project init" |
| 20 | Compress | ⚙️    | Keyword    | Lv.2     | Headroom proxy management & stats | "headroom", "compression", "token savings", "proxy status" |

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
- **"where was I" / "update state"** →State only (not Echo or Project)
- **"verify" / "check this work"** →Verify only (not Seal hook)
- **"humanize" / "rewrite"** →Humanize only
- **"tier" / "scope" / "what's allowed"** →Governor only

## Storage
- **Database (primary):** `C:\Projects\memstack\db\memstack.db` — SQLite with WAL mode
- **DB Helper:** `python C:/Projects/memstack/db/memstack-db.py <command>` — repository pattern CLI
- **Commands:** `init`, `add-session`, `add-insight`, `search`, `get-sessions`, `get-insights`, `get-context`, `set-context`, `add-plan-task`, `get-plan`, `update-task`, `export-md`, `stats`

## Paths
- Skills: `C:\Projects\memstack\skills\{name}\SKILL.md` | Deprecated: `skills\_deprecated\` | Hooks: `.claude/hooks/` | Rules: `.claude/rules/` | Commands: `.claude/commands/` | DB: `C:\Projects\memstack\db\` | Config: `config.json`

*Architecture inspired by Developer Kaki's MemoryCore (github.com/Kiyoraka/Project-AI-MemoryCore)*
