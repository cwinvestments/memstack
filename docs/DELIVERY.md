# How MemStack Reaches a Customer

**Written 2026-08-04.** Every mechanical claim below was read out of source on that date and is
cited with file and line. Nothing here is carried forward from a prior session's summary. Several
claims that earlier sessions treated as established turned out to be false when re-checked, which
is why this document exists and why section 2 lists them.

**Verified against:**

| What | Where | How |
|---|---|---|
| Plugin manifest, hooks, free skills | `C:\Projects\memstack` at `e40f2b4` (3.7.0) | read the files; `find`, `git ls-files` |
| Pro bundle server | `C:\Projects\adminstack` | read `src/lib/pro-skills-bundle.ts`, `src/app/api/skills/pro-bundle/**` |
| Loader | `C:\Projects\memstack-skill-loader` | read `src/memstack_skill_loader/**`; ran `_compute_bundle_version` and `_auto_discover_skills` |
| Counts | all three repos | ran `check_skill_drift.py` |
| Host client behaviour | code.claude.com/docs | quoted, not verified. See section 9 and U-1 |
| One live install | this machine | `~/.claude/plugins/`, 2026-08-04 |

**Citations:** this repository is public; `adminstack` and `memstack-skill-loader` are private. A
citation into either names a real file and line for a reader who holds access, not a link anyone
can follow. They are kept in that form deliberately: a reference the owner can check is worth more
than an unsourced summary nobody can. The loader's source also ships in its PyPI sdist, so its
citations resolve there at the matching package version; adminstack's does not ship anywhere.

**Scope:** how bytes get from a repo to a customer. Not what the skills do.

---

## 1. The thirty-second answer

Three artifacts ship on three independent channels. Nothing about one implies anything about
another.

| Artifact | Count | Source of truth | Delivered by | Version lever | Reaches a passive customer? |
|---|---|---|---|---|---|
| Free skills | 86 | `memstack/skills/` | Marketplace | `plugin.json` `version` | **No** |
| Hooks | 1 (`SessionStart`) | `memstack/hooks/` | Marketplace | `plugin.json` `version` | **No** |
| Plugin manifest | n/a | `memstack/.claude-plugin/` | Marketplace | itself | **No** |
| Pro skills | 44 | `adminstack/src/data/pro-skills/` | Pro bundle probe | sha256 of Pro `SKILL.md` bytes | **Yes**, within 24h |
| Loader package | n/a | PyPI `memstack-skill-loader` | `pip` | PyPI version | **No** (prints a notice) |

Counts verified 2026-08-04: `find skills -name SKILL.md | wc -l` returns 86, none of them under
`skills/_deprecated/`; `len(PRO_EXCLUSIVE_SKILLS)` returns 44, matching 44 folders in
`adminstack/src/data/pro-skills/`; `check_skill_drift.py` reports "Canonical slug set: 130
(free+pro)" and "RESULT: OK".

---

## 2. Plausible things that are false

Each of these was believed during real work and cost a source dive to disprove. They are listed
first because they are the premises a reader is most likely to arrive holding.

**"The bundle version hashes all `SKILL.md` files, so editing any skill moves it."**
False. It reads one directory, `adminstack/src/data/pro-skills/`, so it covers Pro skills only.
Settled in section 7.

**"`components` in `plugin.json` controls what the plugin ships."**
False. `components` is not in the manifest schema and is silently ignored; every component
resolves from its default location instead. Settled in section 3.

**"Bumping the plugin version delivers the change to existing customers."**
False. It makes the change *available*. Nothing in MemStack then tells anyone, and for this
marketplace no automatic fetch is known to run. Settled in sections 9 and 10.

**"A Pro customer's auto-update probe keeps their whole install current."**
False. It keeps their Pro skills current and nothing else, so their hooks and free skills can be
arbitrarily stale while the Pro half updates on schedule. Settled in sections 7 and 8.

---

## 3. Three artifacts, not two

**The plugin.** This repo: free skills, hooks, manifest. The marketplace serves it from the
repository's default branch.

**The Pro bundle.** 44 skill folders in `adminstack/src/data/pro-skills/`, zipped on demand by an
authenticated endpoint. Never in this repo.

**The loader.** The `memstack-skill-loader` pip package providing the `memstack-skills` MCP
server. Published to PyPI. Not shipped by the plugin: `.mcp.json` at this repo's root is
untracked (`git ls-files .mcp.json` returns nothing) and is absent from the installed plugin
tree.

The loader records why the plugin and loader share no version coupling, at `license.py:424-431`:

> `plugin_version` is intentionally absent. The Claude Code skills-bundle plugin is a separate
> marketplace artifact; its version lives in `.claude-plugin/plugin.json` inside Claude Code's
> plugin cache. This loader's MCP server is registered standalone ... so the process never
> receives `CLAUDE_PLUGIN_ROOT` or any handle to that cache, and the two artifacts share no
> version coupling.

A consequence worth stating: **we cannot tell which plugin version any customer runs**, even in
aggregate, because that field is deliberately not collected.

---

## 4. Path A, the marketplace path

### What is fetched, from where

`.claude-plugin/marketplace.json:12-16` declares the source:

```json
"source": { "source": "github", "repo": "cwinvestments/memstack" },
"version": "3.7.0"
```

`/plugin marketplace add cwinvestments/memstack` git-clones the repo to
`~/.claude/plugins/marketplaces/cwinvestments-memstack/`. Verified on this machine: that
directory contains a real `.git`, and its HEAD is `7590d15`, the 3.6.2 release commit.

`/plugin install` and `/plugin update` copy the tree into a version-keyed directory,
`~/.claude/plugins/cache/cwinvestments-memstack/memstack/<version>/`. Verified: this machine has
`.../memstack/3.6.2/`, and `installed_plugins.json` records `"version": "3.6.2"`.

### What determines out of date

The version string, used as a cache key. Per the plugins reference:

> Claude Code uses the plugin's version as the cache key that determines whether an update is
> available. When you run `/plugin update` or auto-update fires, Claude Code computes the current
> version and skips the update if it matches what's already installed.
>
> The version is resolved from the first of these that is set:
> 1. The `version` field in the plugin's `plugin.json`
> 2. The `version` field in the plugin's marketplace entry in `marketplace.json`
> 3. The git commit SHA of the plugin's source ...

MemStack sets `version` in both (`plugin.json:3`, `marketplace.json:16`), so rule 1 applies and
the commit SHA is never consulted. `installed_plugins.json` does store a `gitCommitSha`, but on
this machine it holds `ef4caff6`, which `git log` resolves to an unrelated older commit. It is
stale bookkeeping, not the update key.

> If you set `version` in `plugin.json`, you must bump it every time you want users to receive
> changes. Pushing new commits alone is not enough.

### What triggers it

See section 9. For a default install: a human typing two commands.

### Where it lands, and the split that matters

Two locations, written by two different commands:

| Path | Written by | Read by |
|---|---|---|
| `~/.claude/plugins/marketplaces/cwinvestments-memstack/` | `/plugin marketplace update` | the **MCP loader** |
| `~/.claude/plugins/cache/cwinvestments-memstack/memstack/<version>/` | `/plugin update` | **Claude Code** (hooks, namespaced skills) |

The loader does not read the versioned cache first. `config.py:92-98` lists the marketplace clone
as candidate 1:

```python
candidates = [
    home / ".claude" / "plugins" / "marketplaces" / "cwinvestments-memstack" / "skills",
    home / ".claude" / "plugins" / "cache" / "cwinvestments-memstack" / "memstack",
    ...
```

Confirmed by running `_auto_discover_skills()` on this machine:

```
Auto-detected skills at: C:\Users\claud\.claude\plugins\marketplaces\cwinvestments-memstack\skills (86 skills found)
```

**Consequence:** `/plugin marketplace update` alone refreshes the content that `find_skill` and
`get_skill` serve, while Claude Code keeps running the old hook and the old `/memstack:*` skills
until `/plugin update` also runs. Order matters, because `/plugin update` on its own reads a
stale clone. The two copies are byte-identical on this machine (same sha256 for
`hooks/session-start`), but they are independently updatable and can diverge. See G-4.

### What it carries

The entire tracked repo tree, not a filtered component set. Verified in the installed copy:
`hooks/` (`hooks.json`, `run-hook.cmd`, `session-start`), `skills/` (86 `SKILL.md`), plus
`CLAUDE.md`, `README.md`, `scripts/`, `templates/`, and the rest.

This needs stating because `plugin.json:9-11` looks like it restricts delivery:

```json
"components": {
  "skills": ["skills/"]
},
```

**`components` is not a field in the plugin manifest schema.** It appears zero times in the
plugins reference. The real schema uses top-level `skills`, `hooks`, `commands`, `agents` and so
on for custom paths, and:

> Claude Code ignores top-level fields it does not recognize.

So `components` is discarded and every component resolves from its default location.
`hooks/hooks.json` is the documented default for hooks, which is why `hooks/session-start` ships
despite never being declared. It works because the field is ignored, not because anything
declares it. `claude plugin validate` reports unrecognized fields as warnings. See G-3.

What it does not carry: Pro skills (not in this repo), and the MCP loader (`.mcp.json` untracked,
absent from the install).

---

## 5. Path B, the Pro bundle path

### What is fetched, from where

`server.py:107-111`:

```python
PRO_BUNDLE_URL = os.environ.get("MEMSTACK_PRO_BUNDLE_URL", "https://admin.cwaffiliateinvestments.com/api/skills/pro-bundle")
PRO_BUNDLE_VERSION_URL = os.environ.get("MEMSTACK_PRO_BUNDLE_VERSION_URL", PRO_BUNDLE_URL.rstrip("/") + "/version")
```

Two endpoints, one shared gatekeeper. Both call `authenticateLicenseKey`
(`pro-skills-bundle.ts:64-120`), which decides authentication and entitlement in one place, so the
two endpoints' access rules cannot drift apart: a key that can read the version can also download
the bundle, and a key refused one is refused the other. A request is admitted only if the key
exists, is active, is unexpired, and carries a tier in an explicit allowlist of entitled tiers
(`pro-skills-bundle.ts:36`). The allowlist names what is entitled rather than what is excluded, so
an unknown, misspelled, or newly introduced tier is refused rather than admitted by default.
Refusals are deliberately distinguishable: a dead credential returns 401, while a live key whose
plan does not include this content returns 403 with `reason: "tier_not_entitled"`
(`pro-skills-bundle.ts:95-116`).

The zip endpoint (`pro-bundle/route.ts`) walks `PRO_SKILLS_DIR` (`pro-skills-bundle.ts:12`, which
is `adminstack/src/data/pro-skills/`), gates inclusion on a folder having a `SKILL.md`
(`route.ts:69`), and ships every file in each qualifying folder recursively
(`route.ts:41-56, 77-81`). It returns the fingerprint in an `X-Bundle-Version` header
(`route.ts:96, 106`).

### What determines out of date

A sha256 over Pro `SKILL.md` files. `pro-skills-bundle.ts:80-112`, mirrored byte for byte in
`server.py:147-189`:

1. per skill, `sha256(utf8(slug) + 0x00 + SKILL.md bytes)`
2. sort the pairs by slug
3. `version = sha256( for each pair: utf8(slug) + 0x00 + utf8(perHash) + 0x0a )`

Content, not mtime. One level deep. Supporting files ride along in the zip but do not contribute,
which the route says itself at `route.ts:71-76`:

> computeBundleVersion still fingerprints SKILL.md ONLY ... the extra files ride along and a
> SKILL.md content edit remains the sole version lever.

Computed live per request, never stamped at release: `version/route.ts:23` calls
`computeBundleVersion()` on each GET and returns `Cache-Control: no-store`
(`version/route.ts:33`). It therefore reflects adminstack's last deploy, not any memstack tag.

### What triggers it

`_maybe_update_pro_skills` (`server.py:300-399`), called at startup from `run()`
(`server.py:1947-1953`) under a 90 second ceiling. Gates, in order:

- `MEMSTACK_NO_AUTO_UPDATE` kill switch, return (`server.py:316-321`)
- no `.complete` sentinel, return; the first download belongs to the activate path
  (`server.py:324-325`)
- TTL guard: skip the network if checked within `BUNDLE_VERSION_TTL_DEFAULT = 86400` seconds
  (`server.py:122`, guard at `server.py:332-338`), cached in
  `~/.memstack/pro-bundle-version-check.json` (`server.py:121`)
- otherwise GET the version endpoint with a 5 second timeout. Any exception fails open and keeps
  the existing skills (`server.py:371-384`)
- re-download only when `remote_version != local_version` (`server.py:386-392`)

This is the only automatic delivery mechanism anywhere in MemStack.

### Where it lands

`~/.memstack/pro-skills/` (`server.py:112-114`), with `.complete` and `.version` sentinels.

The swap is guarded: zip-slip rejection (`server.py:240-244`), refusal to install an empty set
(`server.py:254-259`), and an integrity check requiring the locally recomputed hash to equal the
server's `X-Bundle-Version` (`server.py:261-269`). Only then does it `rmtree` and `os.rename`
(`server.py:272-277`), then write `.complete` before `.version` (`server.py:285-286`), so that a
crash between the two leaves a versionless install which is safely re-downloaded once.

### What it carries

The 44 Pro skill folders, whole. Not free skills, hooks, or the plugin manifest. None of those
are in `adminstack/src/data/pro-skills/`, and the hash function only ever reads that directory.

---

## 6. Path C, the loader package

Published to PyPI as `memstack-skill-loader`, installed and upgraded with `pip`. At startup
`run()` calls `check_for_updates()` (`server.py:1937-1938`), which compares the installed version
against `https://pypi.org/pypi/memstack-skill-loader/json` (`version_check.py:9`), caches the
answer for 24 hours (`version_check.py:10-11`), and on a mismatch prints to stderr
(`version_check.py:58-62, 78-82`):

```
[memstack] Update available: {remote} (you have {local}). Run: pip install memstack-skill-loader --upgrade
```

Never automatic. Section 9 covers whether anyone sees that line.

---

## 7. Version levers

| Lever | Governs | Where it lives | Moves when |
|---|---|---|---|
| Plugin version string | free skills, hooks, manifest | `plugin.json:3` (authoritative), mirrored at `marketplace.json:16` and the `README.md:3` badge | a human bumps it |
| Pro bundle fingerprint | Pro skills | computed live, never stored in a repo | any Pro `SKILL.md` byte changes |
| PyPI version | loader | loader's `pyproject.toml` | a human bumps it |

### The Pro fingerprint is a Pro content channel and nothing else

`computeBundleVersion` reads exactly one directory, `adminstack/src/data/pro-skills/`
(`pro-skills-bundle.ts:12`, used at lines 81, 85, 90). It never sees this repo.

Therefore none of the following move it:

- editing a free skill
- editing a hook
- bumping the plugin version
- editing a Pro skill's supporting file rather than its `SKILL.md`

Stated plainly: **the auto-update probe delivers Pro skill content and nothing else.** It is not
a general update channel, and no amount of releasing on the plugin track will cause it to fire.
The name `computeBundleVersion` reads repository-wide and is the likely source of the recurring
confusion; `computeProBundleVersion` would be accurate.

The already-documented corollary remains true and lives in
`memstack-skill-loader/ARCHITECTURE_DISTRIBUTION.md`: a change confined to a Pro skill's
supporting files moves no fingerprint and reaches existing customers never, which that document
calls "not a delay, it is a permanent miss." The remedy is to touch that skill's `SKILL.md` in
the same change, or to have the user run the `refresh_pro_skills` MCP tool, which forces a
download past both the version check and the TTL (`server.py:1447-1454`).

---

## 8. What three customers have after any release

Take a release that changes a free skill, a hook, and a Pro skill.

| | Accepts an update prompt | Never updates, holds a Pro licence | Fresh install today |
|---|---|---|---|
| Free skills | new | old | new |
| Hooks | new | old | new |
| Plugin manifest | new | old | new |
| Pro skills | new (probe, within 24h) | new (probe, within 24h) | new |
| Loader | unchanged unless they run `pip install --upgrade` | unchanged | whatever `pip` resolved at install |

**The passive Pro customer is the case to remember.** Their Pro skills stay current
automatically and indefinitely, while their hooks and free skills are frozen at whatever version
they installed. Nothing about the working Pro channel signals that the other half is stale, and
the visibly updating half implies the whole thing updates.

Verified instance of exactly that state, this machine, 2026-08-04:

```
installed plugin version:                    3.6.2   (origin/master is 3.7.0)
marketplace clone HEAD:                      7590d15 (the 3.6.2 release commit)
installed hooks/session-start:               4628 bytes, sha256 7b08f20a...
repo HEAD hooks/session-start:               5523 bytes, sha256 6432aeb4...
"SECRETS OUTPUT POLICY" in installed hook:   0 matches
"SECRETS OUTPUT POLICY" in repo HEAD hook:   1 match
```

The clone was last updated `2026-08-03T02:19:30Z`; `e40f2b4` (3.7.0) was committed
`2026-08-03 14:29:27Z`. The machine has simply never fetched since.

---

## 9. What prompts a user

**Nothing in MemStack's own software tells a user that a plugin update exists.** Verified:

- `version_check.py:48-84` checks PyPI for the loader package only. It says nothing about the
  plugin, and it writes to stderr, which for an MCP stdio server goes to the server log rather
  than the user's terminal. Treat this notice as effectively invisible in normal use.
- The dashboard's `_VERSION` is `importlib.metadata.version("memstack-skill-loader")`
  (`dashboard.py:17-20`), surfaced at `/api/version` (`dashboard.py:1109-1110`). That is the
  loader package again. No plugin version is displayed anywhere.
- `license.py:424-431` deliberately omits `plugin_version` from telemetry, so the server cannot
  detect or report a stale plugin either.
- The Pro probe's own messages (`server.py:380-383, 388`) also go to stderr, and concern Pro
  skills only.

**On the host client, stated at the limit of what we know.** Anthropic's documentation describes
a per-marketplace auto-update feature: Claude Code checks after session start with a random delay
of up to ten minutes, and "If any plugins were updated, you'll see a notification prompting you
to run `/reload-plugins`." The same page states:

> Official Anthropic marketplaces have auto-update enabled by default. Third-party and local
> development marketplaces have auto-update disabled by default.

`cwinvestments-memstack` is third party.

What we actually verified: on one machine, `known_marketplaces.json` carries no `autoUpdate` key
for this marketplace, no settings file sets one, and neither `DISABLE_AUTOUPDATER` nor
`FORCE_AUTOUPDATE_PLUGINS` is set. That machine is two versions behind.

What we did not verify: that the documented default is what the client actually does, that
absence of the key means disabled, or that the notification appears when it is enabled. One
machine's configuration plus one machine's staleness is consistent with the documented default
but does not establish it. See U-1.

So a customer who has not enabled auto-update has no signal at all that a release happened,
from us or, as far as we can tell, from the client. Advising them to enable it once, via
`/plugin` then Marketplaces then Enable auto-update, is the cheapest available fix and would
convert every future release into automatic delivery.

---

## 10. Known gaps

**G-1. Hooks and free skills have no push mechanism to a passive customer.** The only automatic
channel is the Pro bundle probe, and section 7 establishes that it is structurally incapable of
carrying them. A customer who never runs `/plugin marketplace update` and `/plugin update`, and
who has not enabled client auto-update, never receives a hook fix or a free-skill fix. Not
slowly. Never.

**G-2. A version bump notifies nobody.** Publishing completes when `master` is pushed, but
delivery depends on a manual action the customer has no signal to take (section 9). The release
runbook treats the push as the finish line; for existing customers it is not.

**G-3. `components` in `plugin.json:9-11` is dead config.** It is not in the schema and is
silently ignored. It reads as though hooks are excluded from delivery, and is the likeliest seed
of the recurring confusion this document exists to end. Delete it, or replace it with the real
top-level keys. Deleting changes nothing functionally, since everything already resolves from
default locations.

**G-4. Two copies of the free skills, updated by different commands.** Section 4: Claude Code
reads the versioned cache, the loader reads the marketplace clone. They can diverge silently and
no check compares them.

**G-5. No published-versus-repository content check.** The existing drift check compares skill
counts and slug sets (`check_skill_drift.py`). A change to the content of an existing file is
invisible to all of them.

**G-6. Entitlement changes do not propagate to a running install.** This is a correctness gap, not
a security one.

The server-side half is closed. Both Pro bundle endpoints decide entitlement at the server, on an
allowlist of entitled tiers that refuses anything unrecognised; section 5 describes that gatekeeper
and is its permanent home. Verified against production in both directions on 2026-08-04: an active
free-tier key receives 403, a Pro key receives 200. Entitlement does not depend on the client
asking honestly.

What remains is that the client's own state lags a tier change. After a tier changes, the loader
keeps acting on its last license answer: the validation response authorizes a 30 day offline cache
(`validate/route.ts:252`) and the loader adds a fixed 7 day safety extension on top
(`GRACE_EXTENSION_DAYS`, `license.py:43`), so a stale tier can persist locally for roughly 37 days.
Separately, the auto-update path decides whether to probe at all from a local `.complete` sentinel
rather than from a fresh entitlement decision (`server.py:324-325`). The consequence is that a
customer whose tier changed keeps using the Pro skills already on their disk until that window
expires. It is a correctness gap because the server no longer relies on the client's belief: a
non-entitled key gets no bundle bytes from either endpoint regardless of what the loader thinks.
Closing it means treating a tier change as a cache invalidation event instead of waiting the
window out.

Deliberately not detailed here: this document ships inside the plugin to every customer's disk,
so the pre-fix behaviour and its reproduction live in the adminstack repo instead. Do not
re-add them to this file.

---

## 11. Unverified

Honest unknowns. Each names what would settle it.

**U-1. Host client auto-update default and notification behaviour.** We have Anthropic's
documentation and one machine's configuration state. *Settle it:* enable auto-update on a test
install pinned to an older version, restart, wait past the delay, and observe whether the plugin
updates and whether a `/reload-plugins` prompt appears. Until then section 9's client-side claims
are documentation plus one consistent observation, not verification.

**U-2. Retired 2026-08-04, answered.** It asked whether the server independently enforces
entitlement. It does, and both endpoints were exercised against production under an entitled and a
non-entitled credential. The finding now lives in G-6, which records the enforcement and the one
half of the gap that is still open. The number is left in place rather than reused, so that
references to U-1 and U-3 through U-5 stay stable.

**U-3. Whether any real customer has auto-update enabled.** Unknowable from here, because we
collect no plugin version (`license.py:424-431`). *Settle it:* telemetry we deliberately chose
not to collect, or asking customers directly.

**U-4. What fraction of customers are stale, and by how much.** Same cause and same remedy as
U-3.

**U-5. Whether the marketplace clone and the versioned cache have ever diverged in the field
(G-4).** Only one machine was inspected, and there they matched. *Settle it:* a check comparing
the two trees, or a support-time diagnostic.

---

## 12. Re-verify this document

Run these rather than trusting the prose. If any disagree, this document is wrong.

```bash
# plugin version surfaces (all three must match)
grep -o '"version"[^,]*' .claude-plugin/plugin.json .claude-plugin/marketplace.json
grep -n "Version-" README.md | head -1

# what the plugin actually ships
git ls-files hooks/ .claude-plugin/ | tr '\n' ' '
find skills -name SKILL.md | wc -l

# what a customer has on disk
cat ~/.claude/plugins/installed_plugins.json     # look for memstack@cwinvestments-memstack
git -C ~/.claude/plugins/marketplaces/cwinvestments-memstack log --oneline -1
ls ~/.claude/plugins/cache/cwinvestments-memstack/memstack/

# is the installed hook current?
diff ~/.claude/plugins/cache/cwinvestments-memstack/memstack/*/hooks/session-start hooks/session-start

# the Pro fingerprint, over the directory it actually reads
python -c "import sys;sys.path.insert(0,'C:/Projects/memstack-skill-loader/src');\
from memstack_skill_loader.server import _compute_bundle_version as f;from pathlib import Path;\
print(f(Path('C:/Projects/adminstack/src/data/pro-skills')))"

# counts across all three repos
python C:/Projects/memstack-skill-loader/scripts/check_skill_drift.py
```

---

## See also

- [`RELEASING.md`](../RELEASING.md), the plugin release runbook, meaning the how of a version bump
- [`.claude/rules/skill-release.md`](../.claude/rules/skill-release.md), the standing rule that a
  skill-content change owes a release
- [`ADDING-SKILLS.md`](../ADDING-SKILLS.md), the checklist for adding, removing, or renaming a skill
- `memstack-skill-loader/ARCHITECTURE_DISTRIBUTION.md`, Pro bundle internals: the two-copies
  invariant, the supporting-files trap, and the drift-check
