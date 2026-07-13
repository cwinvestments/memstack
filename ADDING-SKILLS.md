# Adding or Changing a MemStack Skill

The maintainer checklist for adding a new skill, or changing the skill set, across
all three repos. Follow every step — skipping one is how counts drift and how
free/Pro gating breaks. (git-guard shipped wrong because the old version of this
doc listed only two count locations and was silent on the catalog rows, the
two-tier count scheme, and the gating registry.)

> **Version bumps** (plugin vs. loader) follow a separate policy — see `memstack-skill-loader/VERSIONING.md`, the canonical two-track versioning source of truth. This doc is about skills and counts, not version numbers.

> [!DANGER] The two-tier count scheme — read this first
> There are **two** skill counts and they are not the same number:
>
> | Tier | Includes `kdp-format`? | Where it may appear |
> |------|------------------------|---------------------|
> | **Public** | **NO** | Every public-facing doc, website, marketing, manifests |
> | **Local** | YES — public **+ 1** local-only `kdp-format` | Maintainer notes only — NEVER ship this number |
>
> **Do not trust any count written in this doc as current — treat every number here as illustrative only.** The authoritative public count is whatever `memstack-skill-loader/scripts/check_skill_drift.py` computes from `.claude/rules/skill-counts.md`. **Run the drift check to get the live count before editing any count.**
>
> - `kdp-format` lives in `C:\Projects\memstack\skills\kdp-format`, is **gitignored**, and is **local-only**. It is counted in the **local** tier only — if you count free skills on disk, subtract 1 for `kdp-format` to get the public free count.
> - The public and local counts differ by exactly 1 (`kdp-format`). **Never ship the local number** (the on-disk free count) in any public-facing doc, manifest, website string, or marketing copy.
> - Adding a **public** skill bumps **both** tiers by one. Adding a local-only skill bumps only the local tier.
> - Canonical rule: `memstack-skill-loader/.claude/rules/skill-counts.md`. Canonical doc map: `memstack-skill-loader/MemStack-Documentation-Map.md`. When the totals change, update those two first, then everything below.

---

## The three distribution channels (never drop one)

A skill reaches users through one of three independent channels. Know which one your skill uses before you start — it determines where the file goes and how it ships.

| Channel | Carries | Source of truth | How the user gets it |
|---------|---------|-----------------|----------------------|
| **1. Marketplace plugin** | The **85 FREE skills** | `cwinvestments/memstack` repo, `skills/` dir | `/plugin marketplace add cwinvestments/memstack` → `/plugin install memstack@cwinvestments-memstack`. The loader reads free skills out of the installed **plugin directory**. |
| **2. AdminStack download-on-activation** | The **43 PRO skills** | `memstack-skill-loader/pro-skills/`, served as a bundle | On `activate_license(...)`, the engine downloads the Pro bundle from `admin.cwaffiliateinvestments.com/api/skills/pro-bundle` into `~/.memstack/pro-skills`. |
| **3. PyPI** | The **engine** (no skills) | `memstack-skill-loader` package | `pip install memstack-skill-loader` → `claude mcp add --scope user memstack-skills -- python -m memstack_skill_loader`. The package ships **zero** skills and is inert until registered. |

> [!WARNING] The marketplace step is REQUIRED, not optional.
> The pip package contains no skills. Free skills come **only** from the installed plugin directory (channel 1). Do not "simplify" the install by dropping the `/plugin marketplace add` + `/plugin install` steps — the loader has nothing to read without them. Full install is four ordered steps: (1) plugin marketplace add + install, (2) `pip install`, (3) `claude mcp add`, (4) restart + `activate_license`.

---

## Step 1 — Decide the skill type and put SKILL.md in the right place

| Skill type | Location | Repo | Channel |
|------------|----------|------|---------|
| **Free, categorized** | `skills/<category>/<slug>/SKILL.md` | `memstack` | 1 (marketplace) |
| **Free, core/standalone** | `skills/<slug>/SKILL.md` (top-level) | `memstack` | 1 (marketplace) |
| **Pro** | `pro-skills/<slug>/SKILL.md` | `memstack-skill-loader` | 2 (AdminStack) |

Categories: `automation`, `business`, `content`, `deployment`, `development`, `marketing`, `product`, `security`, `seo-geo`.

> [!WARNING] Free skills live in **two** structural locations.
> Categorized free skills sit in `skills/<category>/<slug>/`; core/standalone free skills sit in top-level `skills/<slug>/`. A count that scans only one location will miss skills. **Never count by scanning a single location — `memstack-skill-loader/scripts/check_skill_drift.py` is the count authority** (it walks the canonical free set and cross-checks it against `skill-counts.md`).

---

## Step 2 — Frontmatter: two conventions

There are **two** valid frontmatter shapes. Pick by where the skill lives.

**A. Categorized skill** (in `skills/<category>/...` or a Pro skill in `pro-skills/`):
```yaml
---
name: memstack-<category>-<slug>   # category-prefixed
description: "Use this skill when the user says '...'. Do NOT use for ..."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"  # required on Pro; optional/cosmetic on free
---
```
- **Pro** categorized skill → **include** the `license` line above. This is the correct label for a Pro skill.
- **Free** categorized skill (e.g. `git-guard` → `memstack-security-git-guard`) → same prefixed name; the `license` field is **optional**. It does **not** determine free/Pro status — the `PRO_EXCLUSIVE_SKILLS` frozenset (Step 3) does — so its presence or absence on a free skill is purely cosmetic and not load-bearing. **Most existing free categorized skills carry this field** (historical convention); newer ones (like `git-guard`) omit it. Either is acceptable. Do not add or strip it to "fix" anything — it gates nothing.

**B. Core / standalone skill** (top-level `skills/<slug>/`, e.g. `echo`):
```yaml
---
name: <slug>   # bare, no prefix
description: "Use when the user says '...'."
version: 1.0.0
---
```
- No `license` field.

> The frontmatter `license` field is a **label only**. It does **not** gate access. The actual free/Pro gate is the `PRO_EXCLUSIVE_SKILLS` registry in Step 3 — the two are independent. A free skill with the `license` field is still free; a free skill without it is still free. Status is decided solely by membership in the frozenset, never by this field.

---

## Step 3 — Register Pro skills in the gate (`PRO_EXCLUSIVE_SKILLS`)

The real free/Pro boundary is a frozenset in:
```
memstack-skill-loader/src/memstack_skill_loader/license.py
```
```python
PRO_EXCLUSIVE_SKILLS = frozenset({"advanced-security", "api-docs", ..., "web-scraper"})
```
- The check is `skill_name.lower() in PRO_EXCLUSIVE_SKILLS`, keyed on the **bare slug** (not the prefixed name).
- **Adding a Pro skill:** add its bare slug here, or it will be served to free users without validation.
- **Adding a free skill:** do **nothing** here. A free skill in a category folder (like `git-guard`) gets the prefixed name and is simply absent from this set. The frontmatter `license` field and this frozenset are independent — set the field per Step 2, set membership here.

---

## Step 4 — Add the CATALOG ROW (not just the count)

Bumping a number is not enough — the skill must appear as a **row/entry** in every per-skill catalog, or it won't render/list even though the total went up.

> [!IMPORTANT] Required regeneration order (source → loader → memstack → site)
> The category/description data has **one source of truth: the loader** (`memstack-skill-loader`). `memstack` and `memstack-pro-site` **vendor** from it — they never define categories. Do these in this exact order; reordering causes drift:
>
> 1. **Edit SOURCE** (hand-edit): loader `src/memstack_skill_loader/categories.py` (category) + `src/memstack_skill_loader/skill_descriptions.json` (`what`/`not_for`); the skill's `SKILL.md` in `memstack`; Pro tier in loader `license.py` (`PRO_EXCLUSIVE_SKILLS`).
> 2. **Loader — regenerate + verify:** `python scripts/export_public_skills.py` (rewrites `skills.public.json`), then `python scripts/check_skill_drift.py` → must PASS.
> 3. **memstack — vendor + regenerate + verify:** `npm run vendor:skills` → `npm run gen:catalogs` → `npm run check:catalogs` (Step 4b).
> 4. **site (`memstack-pro-site`) — vendor + regenerate + verify:** `npm run vendor:skills` → `npm run gen:skills` → `npm run check:skills` (`skillCounts.ts` auto-derives).
> 5. **Verify all three agree** on the skill's category and the total count.
>
> **RULE — never hand-edit generated files.** `skills.public.json` (loader), `memstack/scripts/_generated/*`, `memstack-pro-site/src/data/skills.ts`, and `skillCounts.ts` are generated/vendored. Hand edits revert on the next regenerate and fail `check:*`. Edit the **source** and regenerate.

| Catalog | Repo | What to add |
|---------|------|-------------|
| `README.md` — catalog tables + Pro-exclusive list | `memstack` | **GENERATED — do not hand-edit.** Lives between `<!-- BEGIN/END GENERATED … -->` markers; regenerate via Step 4b. |
| `SKILL-REFERENCE.md` — full skill list | `memstack` | **GENERATED — do not hand-edit.** Fully regenerated via Step 4b. |
| `pro-skills.md` / Pro skill list | (Pro docs) | A row, **Pro skills only** |
| `src/data/skills.ts` — catalog array | `memstack-pro-site` | **GENERATED** from vendored data + overlay (`npm run gen:skills`); add the overlay entry, not the array object |
| `src/memstack_skill_loader/skill_descriptions.json` | `memstack-skill-loader` | A `what`/`not_for` entry for the new slug — **source** for the loader AND the memstack/site catalogs |
| `src/memstack_skill_loader/categories.py` `CATEGORY_MAP` | `memstack-skill-loader` | The skill's category — **authoritative source** (F-3 blocks if missing) |

> [!IMPORTANT] The memstack catalogs are now single-sourced from the loader.
> `README.md`'s catalog tables, its Pro-exclusive list, and **all of `SKILL-REFERENCE.md`** are **generated** from the loader's authoritative data — the same single-source pipeline the website uses. Never hand-edit them: hand edits are overwritten on the next regenerate and will fail `check:catalogs`. You edit the **sources** (above); the catalogs follow via Step 4b.

### Step 4a — Re-export the loader's public data (before 4b)

The loader is the source; `skills.public.json` is **generated** from `categories.py` + the skill's `SKILL.md` version + the Pro gate. After editing the sources (Step 4 rows), regenerate it in `memstack-skill-loader`:

```bash
python scripts/export_public_skills.py   # regenerate skills.public.json (fail-loud on count / category / overlap)
python scripts/check_skill_drift.py      # must PASS: counts consistent, every slug has a category
```

Do **not** hand-edit `skills.public.json`. Only after this passes, run Step 4b in `memstack`.

### Step 4b — Regenerate the memstack catalogs (after editing the sources)

Once the loader sources are updated (category in `categories.py`, tier in `PRO_EXCLUSIVE_SKILLS`, `what`/`not_for` in `skill_descriptions.json`) and `skills.public.json` is **re-exported** (Step 4a), regenerate in `memstack`:

```bash
npm run vendor:skills    # byte-for-byte copy loader sources -> scripts/_generated/ (+ SOURCE.md provenance)
npm run gen:catalogs     # regenerate README regions + SKILL-REFERENCE.md from the vendored data
npm run check:catalogs   # must exit 0 (committed == regenerated); EOL-robust, safe in CI / fresh checkout
```

`gen:catalogs` is **fail-loud**: it aborts if the data isn't exactly the expected public total (the free/Pro counts asserted in the generator and kept in sync by the drift check — never trust a number written here, verify live), any skill has no `what`, a category is unknown, or the local-only `kdp-format` leaks in. Per-category counts **and every count in the generated docs are derived** — there is nothing to hand-bump inside the generated regions.

> [!NOTE] Moving a skill between categories shifts per-category subtotals.
> Recategorizing (e.g. Development → Core) changes each affected category's subtotal (one −1, one +1) even though the **total** is unchanged. Those subtotals are **derived** by the generators/section headers — they are **not** tracked in `skill-counts.md` (which holds only total / free / Pro). So a category move is still a full source-edit-then-regenerate: change `categories.py`, re-run `export_public_skills.py`, regenerate the memstack + site catalogs, and re-run `check_skill_drift.py` so the derived subtotals update everywhere.

---

## Step 5 — Bump EVERY count location

When the public total changes, update **all** of these. Grouped by repo. (Old doc listed 2 of these; there are ~14.)

**Website (`memstack-pro-site`) — start here, it's the source:**
| File | What holds the count |
|------|----------------------|
| `src/config/skillCounts.ts` | **THE single source** — `{ free, pro, total, categories }`. Everything else on the site renders from this. |
| `src/data/skills.ts` | The catalog array (Step 4) + a **vestigial `CATEGORIES` count** — keep it in sync. |
| `src/components/sections/FrameworkArtifact.jsx` | Skill count renders dynamically from `SKILL_COUNTS.total` (no edit needed). **Caveat — categories, not skills:** line 314 **hardcodes** the category count (`10`) instead of `{SKILL_COUNTS.categories}`. Not a skill-count issue, but if you ever **change the category set**, fix this line too. |

**`memstack` repo:**
| File | What holds the count |
|------|----------------------|
| `README.md` | **Per-category headers are GENERATED** (Step 4b) — do not edit them. Still hand-edit the prose totals **outside** the markers: the `## All Skills (N total …)` heading, the **Tier Structure** table, and the intro paragraph. |
| `SKILL-REFERENCE.md` | **Fully GENERATED** (Step 4b) — title, intro, per-section, and footer counts all self-derive. Nothing to hand-edit. |
| `GETTING-STARTED.md` | Total |
| `MEMSTACK.md` | Total |
| `.claude-plugin/plugin.json` | Count in description/metadata |
| `.claude-plugin/marketplace.json` | Count in description/metadata |

**`memstack-skill-loader` repo:**
| File | What holds the count |
|------|----------------------|
| `.claude/rules/skill-counts.md` | **Canonical rule** — update the math here first |
| `MemStack-Documentation-Map.md` | **Canonical doc tracker** — update here first; keep it in sync (see note below) |
| `README.md` | Total |
| `QUICKSTART.md` | Total |
| `QUICK-REFERENCE.md` | Total |
| `TROUBLESHOOTING.md` | Total |
| `ARCHITECTURE_DISTRIBUTION.md` | Total |
| `src/memstack_skill_loader/server.py` | Runtime messages — verify (may be dynamic `len(...)`; correct if hardcoded) |

> Reminder from the top of this doc: every number above is the **public** count. Never write 129 / 86-free anywhere in this table.

> [!NOTE] Keep `MemStack-Documentation-Map.md` in sync.
> It is the canonical tracker of every documentation location and must reflect the current count. Its header is current, but its **§3 (website-audit) body and footer currently lag** (they still describe a pre-128 state) — a separate cleanup. Refresh the §3 "What It Shows" rows to the live count; leave the dated audit-log footer as-is (it is a historical record — append a new dated line rather than rewriting it).

---

## Step 6 — Push to the right repo(s)

| Skill type | Repo to push |
|------------|--------------|
| Free | `cwinvestments/memstack` (public) |
| Pro | `cwinvestments/memstack-skill-loader` (private) |
| Count/catalog edits on the site | `memstack-pro-site` |

Follow repo git hygiene: stage specific paths, never `git add -A`, build before push.

> [!NOTE] One skill change = commits in **multiple** repos.
> Adding or moving a skill is never a single-repo commit. Expect commits in: **`memstack-skill-loader`** (source edit in `categories.py` / `skill_descriptions.json` / `license.py` + regenerated `skills.public.json`, plus engine/CLI if the skill has one), **`memstack`** (the `SKILL.md` + regenerated `_generated/*`, README regions, `SKILL-REFERENCE.md`), and **`memstack-pro-site`** (regenerated `skills.ts` + `skillCounts.ts`-derived counts). Commit them together as a set — landing one and forgetting the others is how the channels drift.

---

## Step 7 — Reindex and verify

1. Run `reindex_skills` (MCP tool) to rebuild the vector index.
2. Confirm the skill appears in `list_skills`.
3. Confirm it appears in `find_skill` for relevant queries.
4. Confirm the correct tier label (MemStack vs MemStack Pro).
5. For a Pro skill: confirm a **free** license does **not** receive it (gate works), and a Pro license downloads it into `~/.memstack/pro-skills`.

---

## Troubleshooting: new skill not appearing

Users must:
1. `pip install --upgrade memstack-skill-loader` (engine)
2. Ensure the plugin is installed (free skills come from the plugin dir — channel 1)
3. Run `reindex_skills`
4. Restart Claude Code

If it still doesn't show: validate the SKILL.md frontmatter is well-formed YAML, the file is in the correct directory for its type (Step 1), and — for Pro — that the slug is in `PRO_EXCLUSIVE_SKILLS` (Step 3).
