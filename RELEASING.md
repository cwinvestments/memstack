# Releasing the Plugin

The working runbook for shipping the skills bundle (the plugin) to the GitHub marketplace, for contributors working in this repo. The canonical policy is `memstack-skill-loader/VERSIONING.md` section 5; if this file and that one ever disagree, that one wins. This file exists because the loader repo is private, so a repo-only contributor needs the steps here.

The always-loaded rule that sends you here is [`.claude/rules/skill-release.md`](./.claude/rules/skill-release.md): any change to `skills/` is not shipped until a release is cut.

## What you are shipping

The plugin is distributed from this repo through the GitHub marketplace. There are two independent version tracks: the plugin (this repo) and the loader (the PyPI engine, a separate repo). They carry unrelated numbers on purpose and are never forced to match. This runbook is the plugin track only.

## How propagation works

The marketplace source is this repo with no pinned ref, so Claude Code tracks the default branch (`master`). Pushing `master` is the publish step; there is no separate upload. Clients cache the plugin by its version string and re-pull only when that string differs, so every release must bump the version, even a pure content or description refresh. Git tags and GitHub Releases are not read by the marketplace: a Release is human-facing only and is not required for customers to receive the update.

## The load gate: mandatory, and it comes first

Before any version surface moves, run:

```
npm run check:plugin-load
```

It starts a real Claude Code process against this tree with `--plugin-dir` and `--debug-file`, reads the load trace that process writes about itself, and asserts that the plugin was checked exactly once, that `skillsPaths` matches the manifest, that the Loaded lines sum to the number of `SKILL.md` files on disk under `skills/`, and that no WARN names a `SKILL.md` in this plugin. Exit 0 is PASS, exit 1 is FAIL. It takes about four seconds.

**This step is not optional and it is not satisfied by `npm run check:manifest`.** That check reads the manifest and reasons about what should register. It is a hand-written model of the loader, and 3.9.7 is the proof that a model can be wrong in the same direction as the thing it models: the manifest was edited, a check was written for it, the check passed, and the release shipped registering 18 of 86 skills. Nothing ran the real loader. The load gate is the only check here whose evidence comes from the program the customer will run.

If `claude` is not on PATH the gate FAILS rather than skipping. A release cannot be cut from a machine that cannot run it.

**The receipt is the release record's evidence.** Every run writes `.memstack/receipts/plugin-load-<timestamp>.json`, carrying the verdict, the four assertion results, the counts and the trace path. Cite that path in the release record, the changelog entry, or the commit message for the version bump. A release that claims a skill count without a PASS receipt behind it is making the same unverified claim 3.9.7 made.

The gate also runs inside `npm run check:catalogs`, so the ordinary pre-release check chain covers it. Note that this makes `check:catalogs` spawn a Claude Code process and require `claude` on PATH, which it did not before.

## Steps

1. On `dev`, run `npm run check:plugin-load` and confirm PASS. Keep the receipt path. Nothing below is safe to do until this passes.
2. Bump the three canonical version surfaces in one commit, staged by name:
   - `.claude-plugin/plugin.json` (authoritative)
   - `.claude-plugin/marketplace.json` (mirror)
   - `README.md` version badge (mirror)
3. Add a dated entry at the top of `CHANGELOG.md`. If the entry asserts a skill count, the receipt from step 1 is what backs it.
4. Run `git grep -nE "<old-version>"` and confirm no canonical surface still holds the old version. Historical `CHANGELOG.md` lines and the deliberately decoupled doc-chrome (`MEMSTACK.md`, the generated `SKILL-REFERENCE.md` footer) are expected to remain and are not drift.
5. Commit, citing the receipt path from step 1. No `Co-Authored-By` trailer: the `commit-msg` git-guard rejects it.
6. `git merge --ff-only dev` into `master`, then `git push origin master`. This push is the publish step.
7. Optional and human-facing only: cut a GitHub Release for the changelog.

## Sizing the bump

Follow SemVer as this track applies it in practice, confirmed by its own history: a new skill or a new plugin mechanism is a MINOR (3.6.0 shipped the diary FACTS block); a fix, or content added to or corrected within an existing skill, is a PATCH (3.5.5 was a content refresh). Adding a skill also triggers the count, catalog, and free/Pro gate obligations in `ADDING-SKILLS.md`, which a content edit does not.

## Version carriers

The plugin version lives in exactly the three surfaces in step 1. `config.json` and `package.json` carry unrelated numbers and are not plugin-version mirrors; leave them alone. The bare `VERSION` file was retired on purpose; do not recreate it.

## What a customer does to receive a release

Nothing happens automatically. A customer runs `/plugin marketplace update cwinvestments-memstack`, then `/plugin update memstack@cwinvestments-memstack`, then restarts the Claude Code process (the version is resolved once at startup, so a running session keeps serving the old one). `/plugin` shows the Installed version to confirm.
