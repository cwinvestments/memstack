---
name: memstack-development-changelog-generator
description: "Use when the user says 'generate changelog', 'update changelog', 'what changed', 'release notes', 'write changelog', or needs a formatted CHANGELOG.md from git commit history. Do NOT use for diary entries, git log viewing, or commit message writing."
version: 1.0.0
---

# Changelog Generator — Generating changelog...
*Produces a formatted CHANGELOG.md from git commit history, grouped by type and ready for release.*

## Activation

| Trigger | Status |
|---------|--------|
| User says "generate changelog" or "update changelog" | ACTIVE |
| User says "what changed" or "release notes" | ACTIVE |
| User says "write changelog" or "changelog since" | ACTIVE |
| User wants to view git log only | NOT this skill — use git commands directly |
| User wants a diary entry | NOT this skill — use Diary |

## Context Guard

- Do NOT use for session logging (that's Diary)
- Do NOT use for commit message writing (that's a git workflow)
- Do NOT use for PR descriptions (that's a git workflow)
- This skill ONLY produces CHANGELOG.md content from existing commits

## Steps

### Step 1: Determine the range

Ask the user or infer from context:

| Parameter | Default | Example |
|-----------|---------|---------|
| Since tag/date | Last tag or last 7 days | `v3.3.0`, `2026-03-01` |
| Until | HEAD | `v3.4.0`, `HEAD` |
| Format | Keep a Changelog | Conventional, custom |

```bash
# Find the last tag
git describe --tags --abbrev=0 2>/dev/null || echo "No tags found"

# Get commits since last tag (or date)
git log --oneline --no-merges $(git describe --tags --abbrev=0 2>/dev/null || echo "HEAD~50")..HEAD
```

### Step 2: Categorize commits

Parse each commit message and classify by prefix:

| Prefix | Category | Changelog Section |
|--------|----------|-------------------|
| `feat:` / `feature:` | Features | ### Added |
| `fix:` / `bugfix:` | Bug Fixes | ### Fixed |
| `docs:` | Documentation | ### Changed |
| `refactor:` | Refactoring | ### Changed |
| `perf:` | Performance | ### Changed |
| `test:` | Tests | (omit unless user requests) |
| `chore:` / `build:` / `ci:` | Maintenance | (omit unless user requests) |
| `BREAKING CHANGE` or `!:` | Breaking | ### Breaking Changes |
| No prefix | Uncategorized | ### Other |

### Step 3: Generate the changelog entry

Follow [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
## [version] - YYYY-MM-DD

### Breaking Changes
- Description of breaking change ([commit-hash])

### Added
- New feature description ([commit-hash])

### Fixed
- Bug fix description ([commit-hash])

### Changed
- Refactor/improvement description ([commit-hash])
```

**Writing rules:**
1. Rewrite technical commit messages into user-facing language
2. Group related commits into single entries where sensible
3. Lead with the impact, not the implementation ("Users can now..." not "Added handler for...")
4. Include short commit hash as reference
5. Skip merge commits, version bumps, and trivial chores unless requested
6. Order: Breaking Changes > Added > Fixed > Changed > Removed > Other

### Step 4: Handle existing CHANGELOG.md

```bash
# Check if CHANGELOG.md exists
ls CHANGELOG.md 2>/dev/null
```

- If exists: prepend the new entry after the title line, before existing entries
- If not exists: create with header:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [version] - YYYY-MM-DD
...
```

### Step 5: Present for review

```
Changelog entry for [version] ([date]):
- [N] features added
- [N] bugs fixed
- [N] changes
- [N] breaking changes

Ready to write to CHANGELOG.md? (prepend / overwrite / clipboard only)
```

## Disambiguation

- "generate changelog" / "update changelog" / "release notes" = Changelog Generator
- "save diary" / "log session" = Diary (not Changelog Generator)
- "what did we do" / "last session" = Echo (not Changelog Generator)
- "git log" / "show commits" = Direct git commands (not Changelog Generator)

## Level History

- **Lv.1** — Base: Git-to-changelog with Keep a Changelog format, commit categorization by conventional commits prefix, user-facing rewriting, existing file handling. (Origin: MemStack v3.5, Apr 2026)
