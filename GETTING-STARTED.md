# Getting Started with MemStack Pro

You now have access to **81 battle-tested skills** for Claude Code (77 free + 4 Pro-exclusive).

## Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed and working
- Git installed
- An existing project you want to enhance

## Accept Your GitHub Invitations

Your purchase gives you access to **two repos**:

1. **memstack** — Skills, rules, hooks, and the launcher bat file
2. **memstack-skill-loader** — MCP vector search server for on-demand skill loading

Check your email for invites from **@cwinvestments** for both repos. Click "View invitation" and accept to get access.

If you didn't receive an invite, contact support: https://cwaffiliateinvestments.com/contact

## Quick Install (One Command)

Run from your project directory. Clones memstack, links rules and hooks, auto-propagates updates.

**Windows:**
```bat
curl -o install.bat https://raw.githubusercontent.com/cwinvestments/memstack/master/scripts/install.bat && install.bat
```

**macOS / Linux:**
```bash
curl -sO https://raw.githubusercontent.com/cwinvestments/memstack/master/scripts/install.sh && bash install.sh
```

That's it. Skills, rules, and hooks are installed via junctions (Windows) or symlinks (macOS/Linux). Updates propagate automatically when you `git pull` inside `.claude/memstack`.

## Advanced: Manual Setup

If you prefer to manage the clone location yourself:

```bash
git clone https://github.com/cwinvestments/memstack.git
git clone https://github.com/cwinvestments/memstack-skill-loader.git
cd memstack
```

Then link into your project:

**Windows (NTFS Junction):**
```bat
start-memstack.bat link C:\Projects\YourProject
```

**macOS / Linux (Symlink):**
```bash
ln -s /path/to/memstack/.claude/rules /path/to/YourProject/.claude/rules
ln -s /path/to/memstack/.claude/hooks /path/to/YourProject/.claude/hooks
```

**Manual Copy (any OS — no auto-updates):**
```bash
cp -r .claude/ /path/to/your/project/.claude/
```

## Verify It's Working

1. Open a Claude Code session in your project
2. Skills auto-load from `.claude/rules/` — no setup or import needed
3. Try any of these:
   - `"Run an RLS audit on this project"`
   - `"Write a PRD for this feature"`
   - `"Generate a deployment checklist"`

If Claude responds with the skill's activation message (e.g., `🔒 RLS Checker — Auditing your Row Level Security...`), you're set.

## Skill Catalog

See `pro-skills.md` for the full list of 81 skills across 10 categories:

| Category | Skills | Examples |
|----------|--------|----------|
| Security | 7 | rls-checker, rls-guardian, owasp-top10, secrets-scanner |
| Deployment | 6 | railway-deploy, netlify-deploy, ci-cd-pipeline |
| Development | 7 | database-architect, test-writer, migration-planner |
| Business | 7 | invoice-generator, contract-template, financial-model |
| Content | 8 | blog-post, newsletter, product-description |
| SEO/GEO | 6 | site-audit, keyword-research, schema-markup |
| Marketing | 8 | sales-funnel, facebook-ad, launch-plan |
| Product | 6 | prd-writer, mvp-scoper, roadmap-builder |
| Automation | 5 | n8n-workflow-builder, webhook-designer, cron-scheduler |

## Usage Examples

You don't need to reference skill names. Describe what you need and the matching skill fires automatically.

```
"Run an OWASP Top 10 scan on this codebase"
→ activates owasp-top10

"Deploy this to Railway"
→ activates railway-deploy

"Write a blog post about this feature"
→ activates blog-post

"Analyze my competitor's pricing"
→ activates competitor-analysis

"Write a PRD for this product"
→ activates prd-writer

"Build an n8n workflow for this process"
→ activates n8n-workflow-builder
```

## MCP Skill Loader (Semantic Skill Search)

MemStack Pro includes a vector search MCP server that lets Claude Code find the right skill for any task on demand.

**What it does:** Instead of loading all 81 skills into every session, CC calls `find_skill("deploy to Railway")` and gets only the relevant skill. Saves context tokens, scales to any number of skills.

**Pro license:** Set `MEMSTACK_PRO_LICENSE_KEY` as an environment variable to unlock 4 Pro-exclusive skills (consolidate, context-db, api-docs, branching). 77 free + 4 Pro-exclusive = 81 total. A SessionStart hook will remind you if it's not set. Get a key at [memstack.pro](https://memstack.pro).

**Setup:** Automatic. When you run `start-memstack.bat link C:\Projects\YourProject`, v4 of the bat file creates the MCP config (`.mcp.json`) automatically.

**Requirements:**
- Python 3.12+ installed
- Clone the skill loader repo: `git clone https://github.com/cwinvestments/memstack-skill-loader.git C:\Projects\memstack-skill-loader`
- Install dependencies: `cd C:\Projects\memstack-skill-loader && pip install -r requirements.txt`
- Build the index: `set PYTHONPATH=src && python scripts/index_skills.py`

**Verify:** Start a CC session in any linked project, type `/mcp`, confirm `memstack-skills` shows as connected.

**After adding or editing skills:** Rebuild the index:
```bash
cd C:\Projects\memstack-skill-loader && set PYTHONPATH=src && python scripts/index_skills.py
```

## Customizing Voice Notifications

MemStack uses text-to-speech to notify you when Claude needs approval or finishes a task. Customize the phrases in `.claude/tts-config.json`:

```json
{
  "enabled": true,
  "voice": "default",
  "messages": {
    "approval_prompt": "Claude needs your attention",
    "task_complete": "Task complete",
    "error": "Something went wrong"
  }
}
```

- **Change phrases:** Edit the `messages` values to whatever you want Claude to say
- **Disable TTS entirely:** Set `"enabled": false`
- The hook and rule both read from this file — no need to edit shell scripts

## Staying Updated

```bash
cd memstack
git pull
```

New skills and improvements are pushed regularly. If you used Option A (NTFS junction), updates auto-deploy to all linked projects. If you used Option B (manual copy), re-copy `.claude/` after pulling.

## Best Practices

- **Save a diary at the end of each session** — say "save diary" or "wrapping up" before closing Claude Code. This logs your accomplishments, decisions, and handoff state so your next session can pick up exactly where you left off.
- **Save a diary after major implementations** — even mid-session, if you just completed a big feature or made important decisions, log it so nothing is lost.
- **Use Echo to recall past work** — say "what did we do last time?" or "recall [topic]" to search across all your diary entries.

## Getting Help

- **Support:** https://cwaffiliateinvestments.com/contact
- **Skill issues:** Describe the problem and which skill you were using so we can reproduce it
