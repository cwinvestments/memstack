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

## Known Issue: Cache Staleness

The skill-loader auto-discovers skills by scanning directories in priority order. When users run `/plugin update`, the `marketplaces/` clone is refreshed via git pull, but a separate `cache/` copy may exist from initial install or PyPI upgrade.

**Impact**: Users on a stale cache won't see newly added skills until:

1. The cache is invalidated (delete `~/.claude/plugins/cache/cwinvestments-memstack/`), or
2. The skill-loader is upgraded via PyPI (which refreshes the cache), or
3. The auto-discovery priority fix lands (marketplaces/ checked before cache/)

When communicating new skill additions, note that users may need to clear their cache if the skill doesn't appear after `/plugin update` + `reindex_skills`.
