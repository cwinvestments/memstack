# MemStack v2.1 — Skill Framework for Claude Code

You are running with MemStack enabled. Read the matching skill file from `C:\Projects\memstack\skills\` when triggered.

## Global Rules
1. Read the project's `CLAUDE.md` first if one exists
2. Never commit `node_modules/`, `.env`, or build artifacts — run `npm run build` before any push
3. Commit format: `[ProjectName] Brief description` — Co-authored-by Claude
4. If `cc_monitor.api_key` is set in `config.json`, Monitor activates automatically
5. Skill chain: Work → Seal → Diary → Monitor

## Trigger Types
- **Keyword** — fires when specific phrases appear in prompt
- **Passive** — always-on background behavior, no explicit trigger
- **Contextual** — fires when conditions are detected (file size, session state)

## Skill Index

| #  | Skill    | Emoji | Type       | Function                          | Key Triggers                                       |
|----|----------|-------|------------|-----------------------------------|----------------------------------------------------|
| 1  | Familiar | 👻    | Keyword    | Multi-agent dispatch              | "dispatch", "send familiar", "split task"          |
| 2  | Echo     | 🔊    | Keyword    | Memory recall from past sessions  | "recall", "last session", "do you remember"        |
| 3  | Seal     | 🔒    | Passive    | Git commit guardian               | "commit", "push", end of any task                  |
| 4  | Work     | 📋    | Keyword    | Plan execution (copy/append/resume) | "copy plan", "append plan", "resume plan", "todo"|
| 5  | Project  | 💾    | Contextual | Session handoff & lifecycle       | "save project", "handoff", "context running low"   |
| 6  | Grimoire | 📖    | Keyword    | CLAUDE.md management              | "update context", "update claude", "save library"  |
| 7  | Scan     | 🔍    | Keyword    | Project analysis & pricing        | "scan project", "estimate", "how much to charge"   |
| 8  | Quill    | ✒️    | Keyword    | Client quotation generator        | "create quotation", "generate quote", "proposal"   |
| 9  | Forge    | 🔨    | Keyword    | New skill creation                | "forge this", "new skill", "create enchantment"    |
| 10 | Diary    | 📓    | Contextual | Session documentation             | "save diary", "log session", end of session        |
| 11 | Shard    | 💎    | Contextual | Large file refactoring (1000+ LOC)| "shard this", "split file", files over 1K lines    |
| 12 | Sight    | 👁️    | Keyword    | Architecture visualization        | "draw", "diagram", "visualize", "architecture"     |
| 13 | Monitor  | 📡    | Passive    | CC Monitor self-reporting         | Auto-activates if API key configured               |
| 14 | Deploy   | 🚀    | Passive    | Build & deployment guardian       | "deploy", "ship it", before any git push           |

## Leveling: Lv.1=Base, Lv.2=Enhanced, Lv.3=Advanced, Lv.4+=Expert. Core skills (Echo, Diary, Work, Project) at Lv.3. Others at Lv.2.

## Skill Deconfliction
When multiple skills could activate on the same prompt, use these ownership rules:
- **"commit"** → Seal only (not Deploy)
- **"push" / "ship it" / "deploy"** → Deploy only (Deploy invokes Seal as sub-step if needed)
- **"build"** → Neither — just run the build command directly
- **"recall" / "remember"** → Echo only (not Diary or Project)
- **"save diary" / "log session"** → Diary only (not Project)
- **"save project" / "handoff"** → Project only (not Diary)
- **"todo" / "plan"** → Work only

## Storage
- **Database (primary):** `C:\Projects\memstack\db\memstack.db` — SQLite with WAL mode
- **DB Helper:** `python C:/Projects/memstack/db/memstack-db.py <command>` — repository pattern CLI
- **Commands:** `init`, `add-session`, `add-insight`, `search`, `get-sessions`, `get-insights`, `get-context`, `set-context`, `add-plan-task`, `get-plan`, `update-task`, `export-md`, `stats`

## Paths
- Skills: `C:\Projects\memstack\skills\` | Memory (legacy): `C:\Projects\memstack\memory\` | DB: `C:\Projects\memstack\db\` | Config: `config.json`

*Architecture inspired by Developer Kaki's MemoryCore (github.com/Kiyoraka/Project-AI-MemoryCore)*
