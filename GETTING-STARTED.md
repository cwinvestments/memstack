# Getting Started with MemStack™

MemStack™ gives Claude Code **128 professional skills** — deployment, security, database design, content writing, marketing, and more. Skills activate automatically when you need them.

**85 skills are free.** A Pro license key unlocks all 128 skills including 43 Pro-exclusive skills. Get a key at [memstack.pro](https://memstack.pro).

## What You'll Need

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed and working
- An existing project you want to enhance

## Install

MemStack comes in two parts — the **skills** (Claude Code plugin marketplace) and the **engine** (PyPI loader). Install both — the loader reads skill files from the installed marketplace plugin. Every command below is labeled **(in Claude Code)** or **(in terminal)**; running one in the wrong place is the most common setup mistake.

**Step 1 — Install the free skills · (in Claude Code):**
```
/plugin marketplace add cwinvestments/memstack
/plugin install memstack@cwinvestments-memstack
```
Run both commands. This unlocks the 85 free skills right away.

> **SSH error?** ("Host key verification failed" on a fresh server that's never used GitHub over SSH.)
> **Default fix · (in terminal)** — rewrite GitHub to HTTPS, then retry Step 1:
> ```bash
> git config --global url."https://github.com/".insteadOf "git@github.com:"
> ```
> **Backup fix · (in terminal)** — add GitHub's host key, then retry Step 1:
> ```bash
> mkdir -p ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts
> ```

**Step 2 — Install the engine · (in terminal):**

Windows:
```bash
pip install memstack-skill-loader
```

Linux / Mac — use the explicit interpreter (the same one you register in Step 3):
```bash
/usr/bin/python3 -m pip install memstack-skill-loader --break-system-packages
```
Find yours with `which python3` and substitute it if it isn't `/usr/bin/python3`. The `--break-system-packages` flag is required on newer externally-managed Python. No pip for that interpreter? Run `sudo apt install python3-pip` first (Debian/Ubuntu).

**Step 3 — Register the MCP server · (in terminal):** register against the **same interpreter you installed onto in Step 2.**

Windows:
```bash
claude mcp add --scope user memstack-skills -- python -m memstack_skill_loader
```

Linux / Mac:
```bash
claude mcp add --scope user memstack-skills -- /usr/bin/python3 -m memstack_skill_loader
```
If this doesn't match Step 2's interpreter, the server won't launch (you'll see a "failed to reconnect" error and `activate_license` will be missing).

**Step 4 — Activate your license · (in Claude Code, after a full restart):** fully quit and reopen Claude Code first so it picks up the new MCP server, then run:
```
activate_license(key="your-key", email="you@example.com")
```
This unlocks the 43 Pro-exclusive skills (85 free + 43 Pro = 128 total). Free-tier users can skip this step — type `list skills` to verify the 85 free skills loaded.

## Verify It Works

Open your project in Claude Code and try one of these:

- `"Run an RLS audit on this project"` — activates the rls-checker skill
- `"Deploy this to Railway"` — activates railway-deploy
- `"Write a PRD for user authentication"` — activates prd-writer

If Claude responds with a structured protocol (activation message, context guard, checklist), MemStack™ is working.

## Pro License (Optional)

A Pro license unlocks all 128 skills including 43 Pro-exclusive skills.

1. Get a key at [memstack.pro](https://memstack.pro)
2. Complete the Install steps above first (marketplace + engine)
3. Restart Claude Code and activate your license:
   ```
   activate_license(key="MSPRO-XXXXXXXX-XXXX", email="you@example.com")
   ```
4. Pro skills download automatically from our server to `~/.memstack/pro-skills` (no separate marketplace step for Pro). You should see all 128 skills (85 free + 43 Pro).

> **Advanced Alternative:** You can also set the `MEMSTACK_PRO_LICENSE_KEY` environment variable instead of using `activate_license`. Use `setx` on Windows or add to `~/.bashrc` on Mac/Linux, then restart your terminal and Claude Code.

## Updating MemStack

MemStack has three parts that update independently. Restart Claude Code after any update.

| Part | What it covers | How to update |
|------|----------------|---------------|
| **Free skills** | the 85 free skills, including new releases | In Claude Code: `/plugin marketplace update cwinvestments-memstack`, then `/reload-plugins` (or restart) |
| **Pro skills** | the 43 Pro skills | Auto-updates within 24h; force an immediate refresh by running the `refresh_pro_skills` tool |
| **Engine** | the skill loader itself | In terminal: `pip install --upgrade memstack-skill-loader` |

**If a new free skill doesn't show up** after a marketplace update (version detection can be unreliable), re-run `/plugin install memstack@cwinvestments-memstack`. As a last resort, clear the cached plugin and reinstall it.

## What's Included

### Skill Categories (128 total: 85 free + 43 Pro)

| Category | Skills | Examples |
|----------|--------|----------|
| Security | 7 | rls-checker, rls-guardian, owasp-top10, secrets-scanner |
| Deployment | 6 | railway-deploy, netlify-deploy, docker-setup, ci-cd-pipeline |
| Development | 7 | database-architect, api-designer, code-reviewer, test-writer |
| Business | 7 | proposal-writer, sop-builder, scope-of-work, financial-model |
| Content | 8 | blog-post, landing-page-copy, email-sequence, youtube-script |
| SEO & GEO | 6 | site-audit, keyword-research, schema-markup, ai-search-visibility |
| Marketing | 8 | sales-funnel, facebook-ad, google-ad, launch-plan |
| Product | 6 | prd-writer, feature-spec, mvp-scoper, roadmap-builder |
| Automation | 5 | n8n-workflow-builder, webhook-designer, cron-scheduler |
| Core | 13 | diary, echo, work, compress, humanize, sight, verify |

### Key Features

- **On-demand loading** — only the skill matching your current task is loaded, saving context tokens
- **Diary system** — logs your accomplishments, decisions, and handoff state between sessions
- **Echo recall** — search across past diary entries to recall decisions and context
- **TTS notifications (opt-in)** — voice alerts for task completion, errors, and attention-needed events. Enable with: `setx MEMSTACK_ENABLE_TTS true` (Windows) or `export MEMSTACK_ENABLE_TTS=true` (Mac/Linux)

## Tips for Best Results

- **Be specific when asking Claude** — say "deploy this to Railway" not "help me deploy". Specific phrases trigger the right skill.
- **Save a diary at the end of each session** — say "save diary" or "wrapping up" before closing Claude Code. This logs your accomplishments, decisions, and handoff state so your next session can pick up exactly where you left off.
- **Save a diary after major implementations** — even mid-session, if you completed a big feature or made important decisions, log it.
- **Use Echo to recall past work** — say "what did we do last time?" or "recall [topic]" to search across all your diary entries.

## Filtering Skills Per Project

You can enable or disable skills per project:

```
manage_skills action="disable" skill="facebook-ad"
```

This creates a `.memstack/disabled_skills` file in your project. Disabled skills won't appear in searches or suggestions.

To re-enable:
```
manage_skills action="enable" skill="facebook-ad"
```

To see disabled skills:
```
manage_skills action="list_disabled"
```

The disable file only affects the project it's in.

## Troubleshooting

### Install issues

**`error: externally-managed-environment` (during Step 2)** — pip refuses to install on a system-managed Python. Add `--break-system-packages` · (in terminal):
```bash
/usr/bin/python3 -m pip install memstack-skill-loader --break-system-packages
```

**Plugin clone fails: "Host key verification failed" (during Step 1)** — a fresh server that's never connected to GitHub over SSH. **Default fix · (in terminal):** `git config --global url."https://github.com/".insteadOf "git@github.com:"` then retry Step 1. **Backup fix · (in terminal):** `mkdir -p ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts` then retry Step 1.

**`activate_license` not found, or MCP "failed to reconnect (-32000)"** — the loader was installed onto a **different Python interpreter** than the one Claude Code launches (the classic bare-`python` mismatch on Linux/Mac). Check · (in terminal):
```bash
/usr/bin/python3 -c "import memstack_skill_loader; print('ok')"
```
If it prints `ok`, make sure Step 3 registered that exact path, then fully restart Claude Code. If it errors with `ModuleNotFoundError`, reinstall onto the explicit interpreter and re-register against that same path · (in terminal):
```bash
/usr/bin/python3 -m pip install memstack-skill-loader --break-system-packages
claude mcp add --scope user memstack-skills -- /usr/bin/python3 -m memstack_skill_loader
```
Then fully restart Claude Code. Rule of thumb: whatever interpreter you `import`-check as `ok` is the path that must appear in your `claude mcp add` command.

**`No module named pip` (during Step 2)** — that interpreter ships without pip (common on minimal Debian/Ubuntu server images). Install it, then retry the Step 2 install · (in terminal):
```bash
sudo apt install python3-pip
```

### Runtime issues

| Issue | Solution |
|-------|----------|
| Skills don't activate | Refresh the right channel, then restart Claude Code (see [Updating MemStack](#updating-memstack)): **free skills** → `/plugin marketplace update cwinvestments-memstack` + `/reload-plugins` (if a new skill is still missing, re-run `/plugin install memstack@cwinvestments-memstack`); **Pro skills** → run `refresh_pro_skills`; **engine** → `pip install --upgrade memstack-skill-loader` |
| Skills not loading | Restart Claude Code |
| Pro skills locked | In Claude Code, run `activate_license(key="your-key", email="you@example.com")` |
| Diary not saving | Say "save diary" — it requires an explicit trigger |

## Getting Help

- **Support:** https://cwaffiliateinvestments.com/contact
- **Skill issues:** Describe the problem and which skill you were using so we can reproduce it
