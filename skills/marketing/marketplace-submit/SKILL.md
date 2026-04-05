---
name: memstack-marketing-marketplace-submit
description: "Use when the user says 'submit to marketplace', 'publish my skill', 'share this skill', 'list on marketplace', 'submit plugin', 'publish to community', or needs to submit a skill or plugin to a community marketplace via PR. Do NOT use for building skills or writing plugin code."
version: 1.0.0
---

# Marketplace Submit — Preparing marketplace submission...
*Step-by-step guide to submit skills, plugins, or tools to community marketplaces via pull request.*

## Activation

| Trigger | Status |
|---------|--------|
| User says "submit to marketplace" or "publish my skill" | ACTIVE |
| User says "share this skill" or "list on marketplace" | ACTIVE |
| User says "submit plugin" or "publish to community" | ACTIVE |
| User wants to build a skill | NOT this skill — use Forge |
| User wants to write plugin code | NOT this skill — use standard development |

## Context Guard

- Do NOT use for skill creation (that's Forge)
- Do NOT use for plugin development
- Do NOT use for npm publishing (different workflow)
- This skill ONLY handles marketplace submission via PR

## Target Marketplaces

| Marketplace | URL | Format | Submission |
|-------------|-----|--------|------------|
| buildwithclaude | github.com/davepoon/buildwithclaude | Skills/plugins directory | Fork + PR |
| awesome-mcp-servers | github.com/punkpeye/awesome-mcp-servers | Awesome list | Fork + PR |
| Smithery | smithery.ai | MCP registry | Web submission |
| Glama MCP | glama.ai/mcp/servers | MCP directory | Fork + PR |
| awesome-claude-code | Community repos | Various | Fork + PR |

## Steps

### Step 1: Prepare the submission package

Verify the skill/plugin is ready:

| Check | How to verify |
|-------|---------------|
| SKILL.md exists and is complete | Read the file, confirm frontmatter + body |
| Name and description are clear | Description explains what it does in one sentence |
| Trigger words are specific | No vague triggers that overlap with other skills |
| No proprietary/Pro content | Confirm this is a free skill or has permission |
| Works locally | User has tested it in their own CC session |

```bash
# Verify the skill file exists and has frontmatter
head -10 skills/<category>/<name>/SKILL.md
```

### Step 2: Fork the target repository

```bash
# Fork via GitHub CLI
gh repo fork <owner>/<repo> --clone

# Or fork via web UI at github.com/<owner>/<repo>/fork
```

### Step 3: Create a submission branch

```bash
cd <forked-repo>
git checkout -b add-<skill-name>
```

### Step 4: Add your content

Each marketplace has its own structure. Follow the existing patterns:

**For buildwithclaude (skill directory):**
```bash
# Create your skill folder
mkdir -p <skill-name>
# Copy your SKILL.md
cp /path/to/your/SKILL.md <skill-name>/SKILL.md
# Add a README if required
```

**For awesome lists (link addition):**
```markdown
<!-- Add to the appropriate section in README.md -->
- [Skill Name](link) - One-line description of what it does
```

### Step 5: Write the PR description

Follow this template:

```markdown
## Add [Skill Name]

### What it does
[1-2 sentences explaining the skill's purpose]

### Trigger keywords
[List the activation triggers]

### Category
[e.g., Development, Automation, Marketing]

### Testing
- [ ] Tested locally in Claude Code
- [ ] Follows repository's contribution guidelines
- [ ] No duplicate of existing entries

### Author
[Your name/handle]
```

### Step 6: Submit the PR

```bash
# Stage and commit
git add .
git commit -m "Add <skill-name> skill"

# Push to your fork
git push origin add-<skill-name>

# Create the PR
gh pr create --title "Add <skill-name>" --body "$(cat <<'PREOF'
## Add [Skill Name]

### What it does
[description]

### Trigger keywords
[triggers]

### Testing
- [x] Tested locally in Claude Code
- [x] Follows contribution guidelines
- [x] No duplicate of existing entries
PREOF
)"
```

### Step 7: Track submission status

```bash
# Check PR status
gh pr status

# View PR checks
gh pr checks
```

## Output Template

```
Marketplace Submission Checklist:
- Target: [marketplace name]
- Skill: [skill name]
- Branch: add-[skill-name]
- PR: [URL when created]

Status: [ready to submit / submitted / merged]
```

## Multi-Marketplace Strategy

For maximum visibility, submit to multiple marketplaces in sequence:
1. Primary marketplace first (e.g., buildwithclaude)
2. Wait for merge
3. Submit to secondary marketplaces with link to primary

Do NOT submit proprietary or Pro skills to public marketplaces.

## Disambiguation

- "submit to marketplace" / "publish my skill" = Marketplace Submit
- "build a skill" / "create a skill" = Forge (not this skill)
- "npm publish" / "publish package" = npm workflow (not this skill)
- "share on Slack" = Direct sharing (not this skill)

## Level History

- **Lv.1** — Base: Multi-marketplace submission guide with PR templates, fork workflow, tracking. (Origin: MemStack v3.5, Apr 2026)
