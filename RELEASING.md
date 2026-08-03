# Releasing the Plugin

The working runbook for shipping the skills bundle (the plugin) to the GitHub marketplace, for contributors working in this repo. The canonical policy is `memstack-skill-loader/VERSIONING.md` section 5; if this file and that one ever disagree, that one wins. This file exists because the loader repo is private, so a repo-only contributor needs the steps here.

The always-loaded rule that sends you here is [`.claude/rules/skill-release.md`](./.claude/rules/skill-release.md): any change to `skills/` is not shipped until a release is cut.

## What you are shipping

The plugin is distributed from this repo through the GitHub marketplace. There are two independent version tracks: the plugin (this repo) and the loader (the PyPI engine, a separate repo). They carry unrelated numbers on purpose and are never forced to match. This runbook is the plugin track only.

## How propagation works

The marketplace source is this repo with no pinned ref, so Claude Code tracks the default branch (`master`). Pushing `master` is the publish step; there is no separate upload. Clients cache the plugin by its version string and re-pull only when that string differs, so every release must bump the version, even a pure content or description refresh. Git tags and GitHub Releases are not read by the marketplace: a Release is human-facing only and is not required for customers to receive the update.

## Steps

1. On `dev`, bump the three canonical version surfaces in one commit, staged by name:
   - `.claude-plugin/plugin.json` (authoritative)
   - `.claude-plugin/marketplace.json` (mirror)
   - `README.md` version badge (mirror)
2. Add a dated entry at the top of `CHANGELOG.md`.
3. Run `git grep -nE "<old-version>"` and confirm no canonical surface still holds the old version. Historical `CHANGELOG.md` lines and the deliberately decoupled doc-chrome (`MEMSTACK.md`, the generated `SKILL-REFERENCE.md` footer) are expected to remain and are not drift.
4. Commit. No `Co-Authored-By` trailer: the `commit-msg` git-guard rejects it.
5. `git merge --ff-only dev` into `master`, then `git push origin master`. This push is the publish step.
6. Optional and human-facing only: cut a GitHub Release for the changelog.

## Sizing the bump

Follow SemVer as this track applies it in practice, confirmed by its own history: a new skill or a new plugin mechanism is a MINOR (3.6.0 shipped the diary FACTS block); a fix, or content added to or corrected within an existing skill, is a PATCH (3.5.5 was a content refresh). Adding a skill also triggers the count, catalog, and free/Pro gate obligations in `ADDING-SKILLS.md`, which a content edit does not.

## Version carriers

The plugin version lives in exactly the three surfaces in step 1. `config.json` and `package.json` carry unrelated numbers and are not plugin-version mirrors; leave them alone. The bare `VERSION` file was retired on purpose; do not recreate it.

## What a customer does to receive a release

Nothing happens automatically. A customer runs `/plugin marketplace update cwinvestments-memstack`, then `/plugin update memstack@cwinvestments-memstack`, then restarts the Claude Code process (the version is resolved once at startup, so a running session keeps serving the old one). `/plugin` shows the Installed version to confirm.
