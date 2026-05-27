# Adding a New MemStack Skill

Complete checklist for adding a skill to the MemStack catalog.

## 1. Create the Skill File

Place `SKILL.md` in the correct location:

- **Free skill**: `skills/<category>/<slug>/SKILL.md` (this repo)
- **Pro skill**: `pro-skills/<slug>/SKILL.md` (memstack-skill-loader repo)

Categories: `automation`, `business`, `content`, `deployment`, `development`, `marketing`, `product`, `security`, `seo-geo`

## 2. Required Frontmatter

```yaml
---
name: memstack-<category>-<slug>
description: "Use this skill when the user says '...'. Do NOT use for ..."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---
```

Pro skills add one additional field:

```yaml
pro_since: "3.5.0"
```

## 3. Pro Skills: Register in license.py

Add the skill slug to the `PRO_EXCLUSIVE_SKILLS` frozenset in:

```
memstack-skill-loader/src/memstack_skill_loader/license.py
```

Without this, Pro skills will be served without license validation.

## 4. Push to GitHub

| Skill type | Repository |
|------------|------------|
| Free | `cwinvestments/memstack` |
| Pro | `cwinvestments/memstack-skill-loader` |

## 5. Update Skill Counts and Catalog

Update the skill count in these files:

| File | Repository |
|------|------------|
| `src/lib/skillCounts.ts` | memstack-pro-site |
| `README.md` | memstack |
| `GETTING-STARTED.md` | memstack |
| `README.md` | memstack-skill-loader |
| `QUICKSTART.md` | memstack-skill-loader |

Add the new skill entry to the catalog data array:

| File | Repository |
|------|------------|
| `src/lib/skills.ts` | memstack-pro-site |

## 6. Reindex and Verify

After adding, run `reindex_skills` via the MCP tool, then confirm:

- Skill appears in `list_skills` output
- Skill appears in `find_skill` results for relevant queries
- Correct tier label (MemStack vs MemStack Pro)

## Troubleshooting: New Skills Not Appearing

After adding a new skill and pushing to GitHub, users need to:

1. Upgrade the skill loader: `pip install --upgrade memstack-skill-loader`
2. Run `reindex_skills` in Claude Code to rebuild the vector index
3. Restart Claude Code

If the skill still doesn't appear, check that the SKILL.md frontmatter is valid YAML and the file is in the correct directory.
