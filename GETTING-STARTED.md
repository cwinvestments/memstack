# Getting Started with MemStack™

MemStack™ gives Claude Code **128 professional skills** — deployment, security, database design, content writing, marketing, and more. Skills activate automatically when you need them.

**85 skills are free.** A Pro license key unlocks all 128 skills including 43 Pro-exclusive skills. Get a key at [memstack.pro](https://memstack.pro).

## What You'll Need

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed and working
- An existing project you want to enhance

## Install

MemStack comes in two parts — the **skills** (Claude Code plugin marketplace) and the **engine** (PyPI loader). Install both.

**Step 1: Install the free skills** — in Claude Code, run:
```
/plugin marketplace add cwinvestments/memstack
/plugin install memstack@cwinvestments-memstack
```

**Step 2: Install the engine** — in your terminal, run:
```bash
pip install memstack-skill-loader
claude mcp add --scope user memstack-skills -- python -m memstack_skill_loader
```

**Step 3: Restart Claude Code**, then type `list skills` to verify. You should see the 85 free skills. Skills auto-load based on what you're working on.

**Step 4 (Pro only):** activate your license to unlock the 43 Pro skills — see [Pro License](#pro-license-optional) below.

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

| Issue | Solution |
|-------|----------|
| Skills don't activate | Refresh the right channel, then restart Claude Code (see [Updating MemStack](#updating-memstack)): **free skills** → `/plugin marketplace update cwinvestments-memstack` + `/reload-plugins` (if a new skill is still missing, re-run `/plugin install memstack@cwinvestments-memstack`); **Pro skills** → run `refresh_pro_skills`; **engine** → `pip install --upgrade memstack-skill-loader` |
| Skills not loading | Restart Claude Code |
| Pro skills locked | In Claude Code, run `activate_license(key="your-key", email="you@example.com")` |
| Diary not saving | Say "save diary" — it requires an explicit trigger |

## Getting Help

- **Support:** https://cwaffiliateinvestments.com/contact
- **Skill issues:** Describe the problem and which skill you were using so we can reproduce it
