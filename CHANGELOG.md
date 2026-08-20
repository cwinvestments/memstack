# MemStack™ Changelog

## v3.7.2 - 2026-08-20 - Four hook consumers that never ran now read their input from stdin

### Fixed
- **Every hook consumer shipped with this plugin gated on `CLAUDE_TOOL_INPUT`, an environment variable Claude Code does not provide.** All four expanded it to the empty string, so none of them ever ran, not once, on any customer machine. Three were registrations in `.claude/settings.json` that piped the empty variable to `grep` and took the failing branch every time: the pre-push gate (`pre-push.sh`), the pre-commit secrets gate (`pre-commit-secrets.sh`), and the post-commit check (`post-commit.sh`). The fourth, `post-tool-monitor.sh`, read `CLAUDE_TOOL_NAME` and `CLAUDE_TOOL_INPUT` directly.
- **Both secret-scanning gates were among the four.** Anyone relying on this plugin had two staged-secret checks registered and neither had ever executed a single scan. Treat any commit made under 3.7.1 or earlier as unscanned by these hooks.
- **Measured, not inferred.** 1053 observation entries written between 2026-06-02 and 2026-08-05 each recorded `unknown` as the tool name and `unknown call` as the summary, which are exactly the empty-variable defaults.
- **The documented delivery mechanism is stdin.** Claude Code passes hook input as a single JSON document on the hook process stdin. `tool_name` is a top-level string and `tool_input` is the tool's own parameter object, so a Bash command is `tool_input.command`. No `CLAUDE_TOOL_INPUT` variable exists in any form, which was confirmed by capturing a live payload before anything was changed.
- **A new dispatcher, `.claude/hooks/gate-on-command.sh`, now owns the three gated registrations.** It reads the payload, extracts `tool_input.command` with `python`, tests it against a literal substring passed as an argument, and runs the target script only on a match. The three target scripts are untouched and still take no arguments and read no stdin.
- **`post-tool-monitor.sh` now parses the same payload directly**, keeping its existing summary logic, entry format, and 120 character clip. The observation files keep their shape and carry real tool names and real summaries in place of `unknown`.
- **Failure posture is explicit rather than silent.** A gate that cannot parse its input exits 0 and blocks nothing, and the two secret gates announce the skipped run on stderr instead of passing quietly, because a silent no-op is the exact defect being repaired.
- **No command text is written to the gate log.** A command can carry a credential, so only the matched pattern and the target script name are recorded.
- **The repo's own commit-format rule instructed every session to add a `Co-Authored-By` trailer that the machine-wide `commit-msg` guard hard-blocks**, so a session that followed the rule had its commit refused. The instruction is removed from `.claude/rules/memstack.md` and from the rule summary in `MEMSTACK.md`, and the guard's behavior is stated in its place.

### Notes
- **Every gate was proven firing live before this release, not assumed repaired.** Each one was triggered by a real tool call and left evidence: the pre-push gate ran and blocked the call with exit 2, both `git commit` gates logged a match on a real commit, and `post-tool-monitor.sh` recorded a `Write` and a `Bash` entry with real values one minute after the previous entry still said `unknown`.
- **PATCH, not MINOR.** This repairs registrations that already shipped and adds no customer-facing capability. The dispatcher is the repair itself, not a new mechanism.
- **No skill added, removed, or renamed, and the skill count is unchanged at 130 (86 free + 44 Pro).**
- **The version bump is the delivery step, not bookkeeping.** Clients cache the plugin by its version string and re-pull only when it differs, so none of this reaches an existing customer until 3.7.2 is on `master`.

## v3.7.1 - 2026-08-20 - JSON payloads move to a stdin sentinel so a shell never parses them

### Fixed
- **All seven `memstack-db.py` call sites across four skills now pass their JSON payload on stdin** rather than as a single-quoted command-line argument. The sites are `add-session`, `add-insight`, and `set-context` in the diary skill; `set-context` in the project skill; `set-context` in the quill skill; and `add-plan-task` and `update-task` in the work skill. Each writes the payload to a file and pipes it in with the literal `-` argument.
- **Why it mattered:** on Windows, `cmd.exe` does not treat single quotes as quoting characters. A redirection operator anywhere inside a quoted payload was therefore executed rather than passed through, silently creating a 0-byte file named after the token that followed it. Prose composed by a session routinely contains one, in an arrow or a comparison.
- **Confirmed by evidence, not theorized:** a 0-byte file named `parses` appeared in `memory/sessions/`. Database row 689 holds the text `=> parses` while none of that diary's markdown files do, so the string reached the database by travelling on the command line, and the shell acted on the operator on the way past.
- **`db/memstack-db.py` gained the sentinel** (commit `f5fa4b1`). The literal argument `-` makes `parse_json_arg` read the payload from stdin instead. It cannot collide with real input, because `-` is not valid JSON, so every argument that parsed before still parses unchanged.
- **The diary skill's Protocol rule was rewritten to match.** It previously said to always use Bash because PowerShell mangles JSON arguments. That named the wrong mechanism and the wrong shell: the hazard is cmd.exe redirection rather than JSON mangling, and PowerShell, which does treat single quotes as quoting, is the shell that would have survived it. The rule now states what the examples below it actually do.

### Notes
- **PATCH, not MINOR:** instructions inside existing skills were corrected. No new skill and no new mechanism ships, which is how this track has sized a content fix before (3.5.5, 3.6.2).
- **All seven sites moved, including the three that carry only metadata.** A rule with exceptions is a rule that gets applied wrongly, and the sentinel costs nothing on a small payload.
- **No skill added, removed, or renamed, and the skill count is unchanged at 130 (86 free + 44 Pro).**
- **The version bump is the delivery step, not bookkeeping.** Clients cache the plugin by its version string and re-pull only when that string differs, so none of these fixes reach an existing customer until 3.7.1 is on `master`.

## v3.7.0 - 2026-08-03 - Secrets rule ships with every session; diary ingest docs corrected

### Added
- **A secrets output policy now ships in the SessionStart hook's `additionalContext`**, so it reaches every session without a customer pasting anything into their own CLAUDE.md. It states the rule directly: never print a secret's value (env var, credential, API key, token, password, or capability URL), inspect `.env` by names only, allowlist names rather than denylist value patterns, verify by property (length, fingerprint, boolean) instead of by printing, redact before running rather than after, and treat rotation as mandatory if a value escapes.
- **This is guidance the assistant is instructed to follow, not an enforcement mechanism.** Nothing in the hook inspects, filters, or blocks a command or its output. It cannot prevent a secret from being printed; it only tells the assistant not to print one. Treat it as a standing instruction, not as a control, and do not let its presence substitute for redaction at the point where output is actually produced.
- **Measured cost:** the hook's static `additionalContext` grows from **301 tokens to 501 tokens (+200)**, 1,372 to 2,249 characters, charged once per session at startup (cl100k_base; Claude's tokenizer will differ slightly).

### Fixed
- **The diary skill's FACTS ingest step no longer documents behavior the ingester stopped having.** It described the step as fire-and-forget, claimed it **always exits 0**, and said malformed lines are skipped with only a stderr note, which invited treating a silent run as a successful one. The ingester (on the loader's `master`, not yet in a published release, see Notes) prints an `N ingested, M duplicate, K skipped` summary on stdout with one indented reason per skipped line, and classifies the outcome by exit code: **0** nothing lost, **1** total loss (lines present, none ingested), **2** store failure (aborted at the first bad row). The step now instructs reading that summary, and re-running after fixing skipped lines, which is safe because facts dedupe on source + subject + claim. A non-zero exit still never means the diary failed to save; the markdown and SQLite row are already written by then.

### Notes
- **MINOR, not patch:** a new always-loaded block shipping to every session is a new mechanism, and this track versions a new mechanism as MINOR (3.4.0, 3.5.0, 3.6.0). A content fix inside an existing skill stays a PATCH (3.5.5, 3.6.2).
- This content was briefly published as **3.6.3** (commit `101b14f`) before the version was re-cut as 3.7.0. The two are byte-identical in content; 3.6.3 is superseded and carries nothing 3.7.0 lacks. Anyone who updated in that window is not missing anything, but should update again so the cached version string matches.
- **No skill added, removed, or renamed, and the skill count is unchanged at 130 (86 free + 44 Pro)**, verified against the loader's `check_skill_drift.py`, which is the count authority.
- **The corrected exit-code behavior is not in a published loader yet.** It is committed on the loader's `master` (`555e707`) but sits in that repo's `## Unreleased` section: the `v4.15.1` tag points at `6c0ef7b`, five commits earlier, and **4.15.1 is still the newest version on PyPI**. No published release contains it.
- **This means the diary skill's step 8 documents behavior an installed loader does not have.** On 4.15.1 the ingester prints no summary and exits 0 on every path. A user who follows the corrected doc, sees no `N ingested, M duplicate, K skipped` line, and concludes their install is broken is a likely outcome, not an edge case. The doc is accurate about where the ingester is going, not about today; it becomes true when the loader cuts its next release. Until then a silent ingest on 4.15.1 is normal, not a fault.

## v3.6.2 - 2026-08-02 - Ship the stranded secrets-scanner guidance

### Fixed
- **Customers on 3.6.1 were running a secrets-scanner skill that reads as a working control, without the section stating it is not one.** The 106-line block (committed `1d956de`, 2026-07-31) that opens with "Enforcement lives in CLAUDE.md, not here" plus the safe-inspection how-to (allowlist-names redaction, verify-without-revealing via length / character class / sha256 fingerprint, atomic byte-mode `.env` editing, capability-URL handling) landed on `master` under the static 3.6.1 version string. Clients cache the plugin by version string and never re-pull under a static version, so it reached no one. This release bumps the version, which is the only thing that makes the marketplace serve content that was already sitting on `master`.
- **The diary skill no longer emits em dashes** into published diary bodies (the "Session Diary" title and the "Files Changed" bullet format), also stranded on `master` since `2803169`.

### Notes
- Content bump; skill count unchanged, no skill added or removed. The stranding root cause is now guarded by `.claude/rules/skill-release.md` (a `skills/` change is unshipped until a version bump and `master` push) and documented in `RELEASING.md`.

## v3.6.1 — 2026-07-31 — Bridge: cwd-corroborated auto-registration

### Fixed
- **Diary saves in projects the loader's memory store had never seen no longer vanish.** A project with no prior rows had no way to enter the store, so it stayed skipped forever and its insights never reached cross-project memory. The bridge now falls back to the current working directory — which is the project root, since the diary invokes the script from there — and auto-registers. Registration is gated on cwd's basename matching the supplied name, which is the entire safety story: a project cannot be typo'd into existence, because the typo would not match the directory the process is running in. A genuine ambiguous collision is never auto-registered either, even when cwd matches, since picking one side would silently attach the insight to the wrong project. First-time registration is surfaced as `project_autoregistered` so a wrong path is noticeable immediately rather than months later.
- **The bridge stops calling every failure "unknown project."** `resolve_project_dir_by_name` returns `None` for both "never seen" and "this basename belongs to two different directories", and the bridge reported both identically — wording that sent one investigation looking for a registration that was never missing. Three distinct reasons are now reported: unknown (no name / no cwd), ambiguous (with the colliding path count), and unrecognized-with-cwd-basename.

### Notes
- Prefers the loader's `find_project_dirs_by_name` (**memstack-skill-loader 4.14.0+**) and degrades to `resolve_project_dir_by_name` on older loaders, where ambiguity simply stays unreportable — no worse than before, and it still refuses rather than guesses.
- The fix itself landed in `27c3e86` **under the static 3.6.0 version string**, which meant clients holding a cached 3.6.0 would never re-pull it (see `VERSIONING.md` §5). This version bump is what actually serves it.

## v3.6.0 — 2026-07-23 — Diary Lv.8: FACTS block (cross-session memory)

### Added
- **The diary skill now appends a `## FACTS` block** — atomic, machine-parsed cross-session knowledge, one fact per line as `subject | claim | method [| entities]`. Only facts worth remembering across sessions; verified over reported; corrections of prior beliefs are the highest-value entries. New protocol step 8 ingests the block into the Memory Engine via `python -m memstack_skill_loader.diary_ingest` — fail-open and dedupe-safe, mirroring the devlog-webhook by-path pattern.

### Notes
- Requires the companion loader release (**memstack-skill-loader 4.13.0** on PyPI) for the `diary_ingest` module step 8 calls and the SessionStart living-memory injection that reads the facts back. Diary SKILL.md is now version 1.1.0.
- Content bump so the marketplace serves the updated diary skill (the plugin ships `skills/` verbatim from the version-keyed cache).

## v3.5.7 — 2026-07-16 — Diary Step 5: deliberate insight types

### Changed
- **The diary skill's Step 5 no longer hardcodes `"type":"decision"`.** It now lists the seven canonical insight types — `gotcha`, `lesson`, `pattern`, `warning`, `failed_approach`, `architecture`, `decision` — each with when-to-use guidance, and states the procedural-vs-record distinction: the first five are **procedural** (an agent can act on them at retrieval time), while `architecture` and `decision` are **record**. Previously every insight was filed as `decision`, collapsing the vocabulary that cross-project search depends on.

### Notes
- Content-only bump. `skills/` ships verbatim, so `d0c04d2` changed what 3.5.6 served without moving its version; 3.5.7 restores the invariant that shipped content and version advance together. Skill count is unchanged.

## Skills — 2026-07-11 — video-review Pro skill

### Added
- **video-review Pro skill** — Claude Code watches an existing video (YouTube URL or local file), downloads it, extracts frames, pulls a transcript, and reviews what is actually on screen. Built for demos, UI walkthroughs, screen recordings, and content clips.
  - Engine vendored from **bradautomates/claude-video** (MIT, attributed in-skill).
  - Windows-hardened: platform-aware install hints, UTF-8 console self-defense, preflight probes for `deno` and `curl_cffi` (now required by yt-dlp for YouTube downloads).

### Notes
- **Skill count: 129 total** (85 free + 44 Pro-exclusive).
- **Pro users** — delivered automatically within 24 hours, or instantly via `refresh_pro_skills`.
- **Loader release** — `memstack-skill-loader` **4.8.0** on PyPI.

## v3.5.6 — 2026-07-09 — Hooks Execute-Bit Fix (Linux/macOS SessionStart)

### Fixed
- **SessionStart hook now runs on Linux/macOS.** `hooks/run-hook.cmd` shipped without the execute bit (mode `100644`) from its introduction on 2026-04-07 (`b7d09fa`). Because the plugin invokes the wrapper directly as a command, Unix shells rejected it with "Permission denied" — so the SessionStart context injection (the "call `find_skill` first" priming) **silently never ran on Linux/macOS**, and skill auto-loading never fired for Mac/Linux users. Both `hooks/run-hook.cmd` and `hooks/session-start` are now marked executable (`100755`).
- Windows was unaffected — its `cmd.exe` branch does not require the execute bit.

Reported by **ahpoblete** (issue #12). Thank you!

## Security — 2026-07-07 — Diary devlog webhook remediation (disclosure timeline documented)

Documents, in response to a good-faith disclosure (issue #10), a resolved data-exfiltration issue in this repository's own project-level agent rules, and corrects a prior inaccurate public statement about it.

### What happened
- From **2026-03-01** (commit `fc2f38e`) to **2026-04-06** (commit `4bcca79`), the project-level agent rules file `.claude/rules/diary.md` contained an **unconditional, hardcoded POST** that sent the full session journal to a personal n8n webhook. There was no environment-variable gate and no key check. It was a leftover from a personal development setup.

### Scope
- The webhook existed **only** in `.claude/rules/diary.md` (this repository's own project rules), **never** in the distributed plugin. The plugin ships `skills/` only; the webhook never appeared in `skills/diary/SKILL.md`. This is verifiable: the endpoint URL appears in exactly two commits (`fc2f38e` and `4bcca79`), both touching only that rules file.
- **Marketplace-plugin installs were never affected.** The only exposure surface was environments running Claude Code inside a clone of this repository during that window.

### Remediation
- `4bcca79` (**2026-04-06**) replaced the hardcoded POST with an opt-in, `MEMSTACK_DEVLOG_WEBHOOK` env-gated version — no data leaves the machine unless that variable is explicitly set.
- `43a9dd0` (**2026-05-27**) later removed the rules file entirely.

### Correction of record
- A prior public statement cited the wrong commit (`446f6d0`, which hardened a **separate** hook mechanism) and incorrectly stated that an empty-API-key check protected the diary POST. That is inaccurate: the diary POST had **no** key check and was **unconditional** during the window above. This entry corrects the record.

### Data
- The only journal data that reached the endpoint was the maintainer's own. No third-party data was transmitted, because the webhook was never present in the shipped plugin.

## v3.5.5 — 2026-06-29 — TokenStack Skill Refresh

### Changed
- **token-optimization skill** — description and content refreshed to center **TokenStack™** as the sole built-in compression proxy; dropped the retired Headroom / RTK / Serena three-layer framing. Skill-content/description refresh only — **no new skills**; total stays **128** (85 free + 43 Pro-exclusive).

### Notes
- Plugin-track patch (Option A): plugin → **3.5.5**, loader unchanged at **4.5.1**. Republished so the marketplace bundle refreshes — the version-string bump is what forces clients to re-pull the corrected skill (`/plugin marketplace update` keys on the version *differing*, not on semver ordering). GitHub Releases are human-facing only and not required for propagation.

## v3.5.4 — 2026-06-23 — Documentation Alignment + Skill-Change Guardrails

### Added
- **git-guard skill** (free) — installer + verifier for the secret-blocking git setup (gitleaks + pre-commit/pre-push hooks). Added to all skill catalogs with conformed naming.
- **ADDING-SKILLS.md** — canonical maintainer checklist for adding, removing, renaming, or re-counting skills: 16 count locations, the two-tier free/Pro scheme, and the 3-channel update architecture (marketplace plugin, PyPI loader, Pro site).
- **CLAUDE.md pointer** — mandatory reference to ADDING-SKILLS.md before any skill add/remove/rename/recount, so the checklist can't be skipped.

### Changed
- **Skill counts corrected to 128** — 128 total (85 free + 43 Pro-exclusive) across README, MEMSTACK, SKILL-REFERENCE, and catalogs.
- **Install docs** — restored the marketplace install step and documented the 3-channel update path.
- **Compression proxy** — removed deprecated Headroom; TokenStack™ is now the sole context-compression proxy.
- **Doc version alignment** — README badge, MEMSTACK title + changes-line, and SKILL-REFERENCE footer set to v3.5.4 (see versioning note below).
- **Version bumps** — plugin manifests advanced to 3.5.2, then 3.5.3.
- **Skill-count drift enforcement** (cross-repo) — `check_skill_drift.py` now fails on skill-count drift. Primary changelog entry lives in the memstack-skill-loader repo; noted here because it guards this repo's counts.

---

> **Versioning note.** The entry below was originally labeled **v4.3.0**, but the plugin manifest read **3.5.0** on 2026-05-27 — the "4.3.0" was an aspirational label that never shipped. It has been re-homed as **v3.5.0-docs** with its body preserved verbatim (including the now-superseded "plugin install" and "all docs updated to v4.3.0" lines) as the honest record of that day's documentation audit. No separate changelog entries exist for v3.5.1–v3.5.3 (release-only version bumps); versioning resumes at v3.5.4 above.

## v3.5.0-docs — 2026-05-27 — Documentation Audit

### Changed
- **Skill counts updated** — 127 total (84 free + 43 Pro-exclusive). `database-architect` moved to Pro.
- **Install method** — Removed deprecated `plugin install` references. Install is now `pip install memstack-skill-loader` + `claude mcp add`.
- **TokenStack™ branding** — All Headroom references updated to TokenStack™ across README, GETTING-STARTED, SKILL-REFERENCE, and MEMSTACK.
- **Version bumps** — All docs updated to v4.3.0.
- **Pro skill list** — Updated to 43 skills (added `database-architect`).

---

## v3.3.4 — 2026-03-28 — Git Audit + Docs Update

### Added
- **Branching skill** (`skills/branching/SKILL.md`) — Enforces dev-branch workflow: all work on `dev`, merge to `master` only after Reviewer confirms.
- **Dev branch** — Created `dev` branch as default working branch. All new work happens here; `master` is release-only.
- **SessionStart license nudge** — Hook fires at session start when `MEMSTACK_PRO_LICENSE_KEY` is not set, guiding users through Pro setup.
- **Tier structure documentation** — All docs now document the free/Pro tier split: 78 free skills, 81 total (78 free + 3 Pro-exclusive: consolidate, context-db, api-docs).
- **90-day graduation rule** — All new skills default to Pro-exclusive and drop to the free tier after 90 days unless marked permanent-Pro.

### Changed
- **Full git audit** — Verified entire git history and working tree are clean: no secrets, no .env files, no grace period files, no hardcoded keys. Repo is safe for public visibility.
- **Delivery model updated** — Removed private GitHub repo references. New model: one public repo + `MEMSTACK_PRO_LICENSE_KEY` activation. Customer pays Stripe ($29) -> gets key via email -> sets env var -> Pro skills unlock.
- **Docs updated** — README.md, GETTING-STARTED.md, SKILL-REFERENCE.md, MEMSTACK.md, and docs/MARKETPLACE-PREP.md updated with current version (3.3.4), accurate skill counts (81 total), and Pro tier info.

---

## v3.3.3 — 2026-03-24 — Production-Grade Secrets Scanning

### Added
- **Pre-commit secrets hook** (`pre-commit-secrets.sh`) — Scans all staged files before every `git commit` using production-grade detection covering 700+ credential formats across every major cloud provider and API service. Blocks commits containing secrets with redacted output. Falls back to built-in regex scan if production scanner is not installed.
- **`.gitleaks.toml`** — Project-level scanner configuration excluding test fixtures, example files, `.claude/diary/`, and `.claude/observations/` directories from scanning.

### Changed
- **Pre-push hook** (`pre-push.sh`) — Upgraded from 5-keyword regex scan to production-grade detection (700+ credential formats). Full working-tree scan before every push. Silent fallback to regex if scanner is not installed.
- **secrets-scanner skill (Lv.3)** — Documented automated hook coverage, fallback behavior, and relationship between manual audits and automated scanning.

---

## v3.3.2 — 2026-03-16 — PostToolUse Observations + SessionStart Context Injection

### Added
- **PostToolUse observation hook** (`post-tool-monitor.sh`) — Captures lightweight observations after every Write, Edit, MultiEdit, and Bash tool call. Logs timestamp, tool name, parsed input summary, and working directory to `.claude/observations/YYYY-MM-DD.md` (daily file, append-only). Uses Python JSON parsing with grep fallback.
- **SessionStart context loader** (`session-context-load.sh`) — On every new CC session, reads last 3 diary entries and last 3 observation files, writes a condensed summary to `.claude/session-context.md` (max 200 lines). Idempotent — overwrites previous context on each session start. Checks both `.claude/diary/` and `memory/sessions/` for diary sources.

### Changed
- **settings.json** — Added two new independent hook entries (PostToolUse observation monitor, SessionStart context loader) following Option B architecture — each with its own timeout budget, separate from existing hooks.

---

## v3.3.1 — 2026-03-12 — PreCompact Auto-Diary

### Added
- **PreCompact hook** — Automatically saves a diary snapshot before Claude Code context compaction runs. Captures uncommitted changes, recent commits, shell history, and modified files. Entries saved to `.claude/diary/{date}-compaction.md` with `COMPACTION_INTERRUPTED` flag. Multiple compactions in one day append to the same file. Fully automatic — no user input required.

### Changed
- **Diary skill (Lv.6)** — Documented PreCompact hook behavior, comparison with manual diary, and session resume guidance.

---

## v3.3.0 — 2026-03-12 — Context DB & API Docs Skills

### Added
- **context-db** — New Core skill: SQLite-backed facts database per project (`.claude/context.db`). Stores structured knowledge as key/value pairs across 5 categories (decisions, patterns, components, config, gotchas). CC queries only relevant facts instead of reading full CLAUDE.md — estimates and logs token savings to `.claude/context-db-stats.json`. Includes inbox watcher for auto-ingestion and CLAUDE.md seeding. Inspired by Google ADK Always-On Memory Agent.
- **api-docs** — New Core skill: fetches current API documentation via Context Hub (`chub`) before CC writes code that calls external APIs. Supports 13 APIs (Supabase, Stripe, SendGrid, Railway, Netlify, Anthropic, OpenAI, Vercel, Cloudflare, Firebase, Resend, Twilio, GitHub). Graceful fallback when chub is not installed. Built on Context Hub by Andrew Ng / AISuite team.

---

## v3.2.2 — 2026-03-01 — Documentation Audit, TTS Notifications, Diary Webhook

### Added
- **rls-guardian** — New Security skill (7th): auto-generates RLS policies for every new `CREATE TABLE` or `ALTER TABLE` statement, enforcing row-level security by default

### Changed
- **notify.md** — Pre-prompt voice notification: TTS "Claude needs your attention" now fires BEFORE approval prompts and questions, not just after task completion
- **diary.md** — Added devlog webhook (step 7): POSTs diary content to n8n endpoint after markdown backup is saved. Fire-and-forget with `.catch()` so webhook failure never blocks diary save
- **README.md** — Complete rewrite: removed "DRAFT stubs" status (all 75+ skills are implemented), added Key Features section, documented on-demand loading, TTS, webhook, templates breakdown (8 starters + 3 utilities)
- **MEMSTACK.md** — Version bump to v3.2.2, updated v3.2 changes description
- **package.json** — Version bump to 3.2.2
- **CHANGELOG.md** — Full history backfill from project inception

---

## v3.2.1-templates — 2026-03-01 — Starter Templates

### Added: 8 Starter Templates
- `nextjs-supabase` — Next.js + Supabase full-stack starter
- `react-node-postgres` — React + Node.js + PostgreSQL starter
- `saas-starter` — SaaS boilerplate with auth, billing, dashboard
- `landing-page` — Marketing landing page with conversion optimization
- `api-backend` — REST/GraphQL API backend starter
- `chrome-extension` — Chrome extension with Manifest V3
- `electron-app` — Desktop app with Electron
- `mobile-react-native` — Mobile app with React Native

---

## v3.2.1-catalog — 2026-03-01 — On-Demand Skill Loading

### Changed: Architecture Overhaul
- Moved all 59 Pro skills from `.claude/rules/` (always-loaded) to `skills/` (on-demand)
- Created `pro-skills.md` catalog rule — skills load only when a task matches their triggers
- Prevents context window bloat from loading 59 skill protocols at session start
- Upgraded notification system from chime to cross-platform TTS (Windows, macOS, Linux)

---

## v3.2.1-skills — 2026-02-28 to 2026-03-01 — All 59 Skills Implemented

### Security (6 skills)
- `rls-checker` — Row Level Security policy auditor for Supabase (first production Pro skill)
- `api-audit` — API endpoint security analysis
- `secrets-scanner` — Leaked credentials and env file auditor
- `owasp-top10` — OWASP Top 10 vulnerability checker
- `dependency-audit` — Package dependency vulnerability scanner
- `csp-headers` — Content Security Policy header generator

All 4 security skills (rls-checker, api-audit, secrets-scanner, owasp-top10) were refined based on AdminStack audit feedback.

### Deployment (6 skills)
- `railway-deploy` — Railway platform deployment guide
- `netlify-deploy` — Netlify deployment and configuration
- `domain-ssl` — Domain DNS and SSL/HTTPS setup
- `hetzner-setup` — Hetzner VPS provisioning and configuration
- `ci-cd-pipeline` — CI/CD pipeline design and setup
- `docker-setup` — Docker containerization guide

### Development (7 skills)
- `database-architect` — Database schema design and optimization
- `api-designer` — REST/GraphQL API architecture
- `code-reviewer` — Systematic code review protocol
- `performance-audit` — Application performance analysis
- `refactor-planner` — Systematic code improvement planning
- `test-writer` — Comprehensive test generation (unit, integration, component)
- `migration-planner` — Safe database schema evolution

### Business (7 skills)
- `proposal-writer` — Professional proposal and pitch generation
- `sop-builder` — Standard operating procedure documentation
- `scope-of-work` — Project scope definition and boundaries
- `invoice-generator` — Professional invoice builder with calculations
- `contract-template` — Service agreement generator with legal clauses
- `client-onboarding` — New client setup system with welcome sequence
- `financial-model` — Business financial projections and unit economics

### Content (8 skills)
- `blog-post` — SEO-optimized blog article writer
- `landing-page-copy` — Conversion-focused landing page copy
- `email-sequence` — Automated email drip sequence builder
- `youtube-script` — Long-form video script with chapters
- `twitter-thread` — Viral thread builder with hook formulas
- `tiktok-script` — Short-form video script with timestamped cues
- `newsletter` — Email newsletter builder with growth tactics
- `product-description` — E-commerce listing copy optimizer

### SEO & GEO (6 skills)
- `site-audit` — Technical SEO site health analysis
- `keyword-research` — Keyword strategy and opportunity mapping
- `meta-tag-optimizer` — Meta title/description optimization
- `schema-markup` — JSON-LD structured data generator
- `ai-search-visibility` — AI search engine optimization (ChatGPT, Perplexity, etc.)
- `local-seo` — Local business SEO strategy

### Marketing (8 skills)
- `sales-funnel` — Full-funnel conversion architecture
- `facebook-ad` — Meta ads copy and targeting strategy
- `google-ad` — Search campaign builder with RSA format
- `launch-plan` — Go-to-market calendar with contingencies
- `competitor-analysis` — Competitive intelligence report
- `pricing-strategy` — Revenue-optimized pricing design
- `lead-magnet` — Opt-in asset and delivery system
- `webinar-script` — Teach-to-sell presentation script

### Product (6 skills)
- `prd-writer` — Product requirements document generator
- `feature-spec` — Detailed feature specification with acceptance criteria
- `user-story-generator` — Backlog-ready story builder with Given/When/Then
- `mvp-scoper` — Minimum viable product definition
- `roadmap-builder` — Strategic Now/Next/Later roadmap
- `feedback-analyzer` — Customer feedback intelligence and prioritization

### Automation (5 skills)
- `n8n-workflow-builder` — Visual automation workflow design
- `webhook-designer` — Secure webhook handler with HMAC verification
- `cron-scheduler` — Scheduled job design with overlap prevention
- `api-integration` — System-to-system API connector
- `content-pipeline` — Multi-platform content automation

---

## v3.2.1-init — 2026-02-28 — Project Initialization

### Added
- Initialized MemStack Pro repository with complete free MemStack base
- Created premium skill directory structure across 9 categories
- Added 3 utility templates: `client-quote`, `handoff`, `project-snapshot`
- Headroom startup command fix in rules
- All free base skills, hooks, rules, commands, and database infrastructure included

### Architecture
```
MemStack Pro v3.2.2
├── Free Base (complete MemStack)
│   ├── Hooks (deterministic)      — pre-push, post-commit, session-start/end
│   ├── Rules (always-loaded)      — memstack, echo, diary, work, notify, headroom, pro-skills catalog
│   ├── Commands (slash)           — /memstack-search
│   └── Skills (19 core)           — Echo, Diary, Work, Forge, Scan, Governor, etc.
├── Pro Skills (59, on-demand)     — Loaded via catalog when task matches triggers
│   ├── Security (6)
│   ├── Deployment (6)
│   ├── Development (7)
│   ├── Business (7)
│   ├── Content (8)
│   ├── SEO & GEO (6)
│   ├── Marketing (8)
│   ├── Product (6)
│   └── Automation (5)
└── Templates (11)
    ├── Starter (8)                — nextjs-supabase, react-node-postgres, saas-starter, etc.
    └── Utility (3)                — client-quote, handoff, project-snapshot
```
