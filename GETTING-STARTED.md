# Getting Started with MemStack™

MemStack™ gives Claude Code **112 professional skills** — deployment, security, database design, content writing, marketing, and more. Skills activate automatically when you need them.

**83 skills are free.** A Pro license key unlocks all 112 skills including 29 Pro-exclusive skills. Get a key at [memstack.pro](https://memstack.pro).

## What You'll Need

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed and working
- An existing project you want to enhance

## Install as a Claude Code Plugin

Run these commands inside Claude Code (not your regular terminal):

**Step 1: Add the marketplace**
```
/plugin marketplace add cwinvestments/memstack
```

**Step 2: Install the plugin**
```
/plugin install memstack@cwinvestments-memstack
```

That's it. Skills auto-load based on what you're working on. No configuration needed.

## Verify It Works

Open your project in Claude Code and try one of these:

- `"Run an RLS audit on this project"` — activates the rls-checker skill
- `"Deploy this to Railway"` — activates railway-deploy
- `"Write a PRD for user authentication"` — activates prd-writer

If Claude responds with a structured protocol (activation message, context guard, checklist), MemStack™ is working.

## Pro License (Optional)

A Pro license unlocks all 112 skills including 29 Pro-exclusive skills.

1. Get a key at [memstack.pro](https://memstack.pro)
2. Set it permanently as an environment variable:

**Windows:**
```bat
setx MEMSTACK_PRO_LICENSE_KEY "MSPRO-XXXXXXXX-XXXX"
```

**Mac / Linux:**
```bash
echo 'export MEMSTACK_PRO_LICENSE_KEY="MSPRO-XXXXXXXX-XXXX"' >> ~/.bashrc && source ~/.bashrc
```

This saves your key permanently so you never have to set it again.

> **Note:** After running this command, close and reopen your terminal for it to take effect.

## What's Included

### Skill Categories (112 total: 83 free + 29 Pro)

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
- **TTS notifications** — voice alerts for task completion, errors, and attention-needed events

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
| Skills don't activate | Reinstall the plugin: `/plugin install memstack@cwinvestments-memstack` |
| Skills not loading | Restart Claude Code |
| Pro skills locked | Set `MEMSTACK_PRO_LICENSE_KEY` environment variable |
| Diary not saving | Say "save diary" — it requires an explicit trigger |

## Getting Help

- **Support:** https://cwaffiliateinvestments.com/contact
- **Skill issues:** Describe the problem and which skill you were using so we can reproduce it
