# Getting Started with MemStack™

MemStack™ gives Claude Code **100 professional skills** — deployment, security, database design, content writing, marketing, and more. Skills activate automatically when you need them.

**77 skills are free.** A Pro license key unlocks 23 additional exclusive skills. Get a key at [memstack.pro](https://memstack.pro).

## What You'll Need

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed and working
- Python 3.10 or higher
- Git installed
- An existing project you want to enhance

## Step 1: Clone MemStack™

Open a terminal and run:

```bash
git clone https://github.com/cwinvestments/memstack.git
```

This downloads the skills, rules, and hooks to your machine.

## Step 2: Link MemStack™ to Your Project

MemStack™ works by linking its `.claude/rules` and `.claude/hooks` folders into your project.

**Windows:**

```bat
cd memstack
start-memstack.bat link C:\Projects\YourProject
```

Replace `C:\Projects\YourProject` with the actual path to your project.

**Mac / Linux:**

```bash
cd memstack
ln -s "$(pwd)/.claude/rules" /path/to/YourProject/.claude/rules
ln -s "$(pwd)/.claude/hooks" /path/to/YourProject/.claude/hooks
```

Replace `/path/to/YourProject` with the actual path to your project.

## Step 3: Verify It Works

Open your project in Claude Code and try one of these:

- `"Run an RLS audit on this project"` — activates the rls-checker skill
- `"Deploy this to Railway"` — activates railway-deploy
- `"Write a PRD for user authentication"` — activates prd-writer

If Claude responds with a structured protocol (activation message, context guard, checklist), MemStack™ is working.

## Step 4: Set Up the MCP Skill Loader (Recommended)

The MCP Skill Loader connects MemStack™ skills to Claude Code so they activate automatically when you need them. Instead of loading all 100 skills into every session, Claude Code searches for and loads only the relevant skill on demand.

For the full setup guide, see [memstack.pro/docs/getting-started](https://memstack.pro/docs/getting-started).

**Install dependencies:**

```bash
cd memstack/skills
pip install -r requirements.txt
```

**Build the search index:**

```bash
python build_index.py
```

You should see: `Done! 100 skills indexed`

**Register the MCP server with Claude Code:**

```bash
claude mcp add memstack-skills -- python skills/mcp_server.py
```

**Verify it works:**

In Claude Code, run `/mcp` and confirm `memstack-skills` shows as connected.


## Step 5: Pro License (Optional)

A Pro license unlocks 4 additional skills: **consolidate**, **context-db**, **api-docs**, and **branching**.

1. Get a key at [memstack.pro](https://memstack.pro)
2. Set it permanently as an environment variable:

**Windows:**
```bat
setx MEMSTACK_PRO_LICENSE_KEY your-key-here
```

**Mac / Linux:**
```bash
echo 'export MEMSTACK_PRO_LICENSE_KEY=your-key-here' >> ~/.bashrc && source ~/.bashrc
```

This saves your key permanently so you never have to set it again.

> **Note:** After running this command, close and reopen your terminal for it to take effect.

## What's Included

### Skill Categories (100 total)

| Category | Skills | Examples |
|----------|--------|----------|
| Security | 7 | rls-checker, api-audit, secrets-scanner, owasp-top10 |
| Deployment | 6 | railway-deploy, netlify-deploy, docker-setup, ci-cd-pipeline |
| Development | 7 | database-architect, api-designer, code-reviewer, test-writer |
| Business | 7 | proposal-writer, invoice-generator, contract-template |
| Content | 8 | blog-post, email-sequence, youtube-script, newsletter |
| SEO & GEO | 6 | site-audit, keyword-research, schema-markup |
| Marketing | 8 | sales-funnel, facebook-ad, google-ad, launch-plan |
| Product | 6 | prd-writer, feature-spec, mvp-scoper, roadmap-builder |
| Automation | 5 | n8n-workflow-builder, webhook-designer, cron-scheduler |
| Core | 13 | diary, echo, work, compress, humanize, sight, verify |

### Key Features

- **On-demand loading** — only the skill matching your current task is loaded, saving context tokens
- **Diary system** — logs your accomplishments, decisions, and handoff state between sessions
- **Echo recall** — search across past diary entries to recall decisions and context
- **TTS notifications** — voice alerts for task completion, errors, and attention-needed events
- **Hooks** — automated pre-commit checks, secrets scanning, and session context loading

## Tips for Best Results

- **Say what you want to do, not which skill to use.** Claude Code finds the right skill automatically. Say "deploy this to Railway" instead of "use the railway-deploy skill."
- **Save a diary at the end of each session** — say "save diary" or "wrapping up" before closing Claude Code. This logs your work so the next session can pick up where you left off.
- **Save a diary after major implementations** — even mid-session, if you completed a big feature or made important decisions, log it.
- **Use Echo to recall past work** — say "what did we do last time?" or "recall [topic]" to search across all your diary entries.

## Filtering Skills Per Project

Not every project needs every skill. You can hide irrelevant skills to reduce token usage and keep search results focused.

### Using `manage_skills` (recommended)

Disable a skill directly from Claude Code:

```
manage_skills action="disable" skill="facebook-ad"
```

Re-enable it later:

```
manage_skills action="enable" skill="facebook-ad"
```

See what's currently disabled:

```
manage_skills action="list_disabled"
```

### Using `.memstack-ignore` (manual method)

Create a `.memstack-ignore` file in your project root with one skill name per line:

```
facebook-ad
google-ad
webinar-script
tiktok-script
```

- Lines starting with `#` are comments
- Blank lines are ignored
- Skills are hidden from `find_skill`, `list_skills`, and `get_skill` — but not deleted
- The file only affects the project it's in

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Skills don't activate | Check that `.claude/rules` is linked in your project directory |
| MCP Skill Loader errors | Run `pip install -r requirements.txt` in the skills directory |
| "No skills indexed" | Rebuild the index (see Step 4) |
| Pro skills locked | Set `MEMSTACK_PRO_LICENSE_KEY` environment variable |
| Diary not saving | Say "save diary" — it requires an explicit trigger |

## Getting Help

- **Support:** https://cwaffiliateinvestments.com/contact
- **Skill issues:** Describe the problem and which skill you were using so we can reproduce it
