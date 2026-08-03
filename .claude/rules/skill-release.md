# Skill Content Changes Are a Release Obligation

A commit that changes anything under `skills/` is not finished when it is committed. It is finished when the plugin version has been bumped and `master` has been pushed. Until then the change lives only in the repo; customers do not have it.

## Why (the mechanism)

The marketplace serves the plugin straight from this repo, and clients cache the plugin by its version string. Claude Code re-pulls a plugin only when that string differs from what it already has. So content changed under a static version is invisible: the commit lands on `master`, but every installed client compares version strings, sees no change, and never fetches the new bytes. A skill edit with no version bump reaches nobody.

This is exactly how a substantive addition to a security skill once sat unversioned on `master` and reached no customer until a release was cut for it.

## The rule

- Any commit that changes `skills/` content creates a release obligation.
- The change is not customer-visible until the three canonical version surfaces bump and `master` is pushed: `.claude-plugin/plugin.json` (authoritative), `.claude-plugin/marketplace.json` (mirror), and the `README.md` version badge (mirror).
- A skill-content commit without a same-cycle version bump is unfinished work, not shipped work. Do not report it as done, and do not let it accumulate on `master` behind a static version.

The trigger is touching a skill, not deciding to release. If you edited `skills/`, you owe a release.

## How

Follow the plugin release runbook in [`RELEASING.md`](../../RELEASING.md). Bumping the version and pushing `master` is the whole publish step: there is no separate upload, and git tags are not read by the marketplace.
