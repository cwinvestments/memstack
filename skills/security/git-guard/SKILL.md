---
name: git-guard
description: "Use when the user says 'git-guard', 'check git protection', 'is this repo protected', 'verify gitleaks', 'set up git hooks', 'install git-guard', or wants to confirm a repo blocks secrets and internal files before commit. This is an installer and verifier, NOT a scanner (gitleaks does the actual scanning). Do NOT use for deep secret audits or RLS work."
version: 1.0.0
---


# 🛡️ Git-Guard: Verifying Repo Protection...
*Install and verify the machine-wide secret-blocking setup on a repo. Confirms the global pre-commit hook, .gitignore coverage, a non-neutered gitleaks config, and a reachable gitleaks binary.*

## Activation

When this skill activates, output:

`🛡️ Git-Guard: Verifying Repo Protection...`

Then execute the protocol below.

## What This Skill Is (and Is Not)

Git-Guard is an **installer and verifier**, not a scanner. It does not grep for
secret patterns itself. Its job is to confirm that the protection layers are
present, wired up, and actually armed, so that when a secret IS introduced,
gitleaks (run by the pre-commit hook) catches it.

The single most dangerous failure this skill exists to catch is a gitleaks
config that LOOKS protective but detects nothing (see Check 3). A scanner that
silently scans zero rules is worse than no scanner, because it produces a green
checkmark while leaving the door open.

## Context Guard

| Context | Status |
|---------|--------|
| **User asks "is this repo protected?"** | ACTIVE: run all 4 checks |
| **User says "set up / install git-guard"** | ACTIVE: run checks, offer fixes |
| **User says "verify gitleaks" / "check git hooks"** | ACTIVE: run all 4 checks |
| **New repo, before first commit** | ACTIVE: install gitignore + verify config |
| **User wants a deep secret/history audit** | DORMANT: defer to secrets-scanner |
| **User is mid-commit and just wants it to pass** | DORMANT: do not loosen protection to unblock |

## Protocol

Run all four checks (Steps 1 to 4), then produce the status report in Step 5.
Step 5 is the report itself, not a fifth check. Never silently run a setup or
fix command: show the exact command and let the user run it (or confirm first).
The one exception is the additive .gitignore append in Check 2, which is safe
and reversible and may be applied after showing the diff.

### Locating the files shipped with this plugin

Two checks reference files that ship INSIDE this plugin: the `pre-commit` hook
and `gitignore-template.txt`, both under the plugin's `scripts/` directory.
After install, those files live in the Claude Code plugin cache, NOT in any
fixed location, and NOT in the customer's own project. Resolve `<plugin-root>`
as the plugin folder this `SKILL.md` was loaded from, walking up out of
`skills/security/git-guard/` to the folder that contains `scripts/`.

On a typical install, `<plugin-root>` looks like this (ILLUSTRATIVE ONLY: the
exact path differs per machine and per marketplace):

```text
%USERPROFILE%\.claude\plugins\<marketplace>\cwinvestments-memstack\
```

To find the real path on the current machine, search the plugin cache:

```cmd
dir /s /b "%USERPROFILE%\.claude\plugins\gitignore-template.txt"
```

Substitute the actual resolved `<plugin-root>` wherever it appears in the
commands below. Everything that refers to `.gitignore`, `.gitleaks.toml`, or the
current repo is relative to the customer's own repo (the current directory), not
the plugin.

### Step 1: Verify the global pre-commit hook is installed (Check 1)

The pre-commit hook is installed machine-wide via `core.hooksPath`, so one hook
covers every repo on the machine. Confirm it is set AND points at a real
directory that contains a `pre-commit` file.

```cmd
git config --global core.hooksPath
```

Then confirm the directory and hook file exist (using the resolved
`<plugin-root>` from the locating note above):

```cmd
dir "<plugin-root>\scripts\hooks\pre-commit"
```

Evaluate:

- **OK** if `core.hooksPath` is set AND the directory exists AND it contains a
  `pre-commit` file.
- **GAP** if `core.hooksPath` is empty, points at a missing directory, or the
  directory has no `pre-commit` file.

If there is a GAP, show the one-time setup command, pointing at this plugin's
hooks directory. Do NOT run it silently:

```cmd
git config --global core.hooksPath "<plugin-root>\scripts\hooks"
```

> This is a global setting. Confirm the user wants machine-wide coverage before
> they run it. If they already use a different hooks manager (Husky, lefthook,
> pre-commit framework), note the conflict instead of overwriting it.

### Step 2: Verify .gitignore covers the standard offenders (Check 2)

A repo without a proper .gitignore will happily stage `.env`, `node_modules/`,
build output, and MemStack session/memory files. Compare the repo's .gitignore
against the shipped template.

Check the file exists, then look for the high-value offender patterns:

```cmd
type .gitignore | findstr /C:".env" /C:"node_modules" /C:"memory/" /C:".serena" /C:"dist/"
```

The canonical offender list lives in the template shipped with this plugin:

```cmd
type "<plugin-root>\scripts\gitignore-template.txt"
```

Evaluate:

- **OK** if .gitignore exists and covers, at minimum: `.env` / `.env.*`,
  `node_modules/`, build output (`dist/`, `build/`, `.next/`), and the MemStack
  internal dirs (`memory/`, `.claude/sessions/`, `.serena/`, `.agent-bridge/`).
- **GAP** if .gitignore is missing entirely, or any of those categories is not
  covered.

If there is a GAP, offer to **append** the missing lines from the template.
This MUST be additive and de-duplicated: never overwrite the existing
.gitignore, and never add a pattern that is already present (exact-line match).

Procedure for the additive append:
1. Read both the repo `.gitignore` and `<plugin-root>\scripts\gitignore-template.txt`.
2. Compute the set of template lines (ignoring blank lines and comments) that
   are not already present as exact lines in the repo file.
3. Show the user the exact lines that will be added.
4. Append only those lines, under a clearly labeled section header such as
   `# --- Added by git-guard ---`, preserving the existing content untouched.

For a brand-new repo with no .gitignore at all, offer to copy the template
verbatim as the starting point:

```cmd
copy "<plugin-root>\scripts\gitignore-template.txt" .gitignore
```

### Step 3: Verify .gitleaks.toml actually detects something (Check 3) [CRITICAL]

This is the most important check. A `.gitleaks.toml` can be present and
syntactically valid yet detect **zero** secrets. This exact silent hole has
shipped live and undetected in real production repos: the config looks
deliberate and protective, so nobody re-checks it.

**The neutering pattern:** gitleaks builds its active ruleset from (a) any
`[[rules]]` blocks defined in the config, plus (b) its built-in default rules,
but ONLY when `[extend] useDefault = true` is set. A config that has an
`[allowlist]` section but NO `[[rules]]` blocks and NO `[extend] useDefault =
true` loads zero rules. The allowlist then filters an already-empty result.
Gitleaks runs, exits 0, reports nothing, and detects NOTHING. It looks
protective. It is not.

Inspect the config:

```cmd
type .gitleaks.toml
```

Then check for the three signals:

```cmd
findstr /C:"useDefault" /C:"[extend]" /C:"[[rules]]" .gitleaks.toml
```

Evaluate:

- **OK (no config):** No `.gitleaks.toml` exists at all. Gitleaks falls back to
  its built-in default ruleset, which detects secrets. This is safe. Note it,
  do not flag it.
- **OK (armed config):** `.gitleaks.toml` exists AND has at least one of:
  `[extend]` with `useDefault = true`, OR one or more `[[rules]]` blocks.
  Detection is active.
- **CRITICAL GAP (NEUTERED):** `.gitleaks.toml` exists, has content such as an
  `[allowlist]`, but has NO `[[rules]]` block AND NO `useDefault = true`.
  Detection is silently disabled.

If NEUTERED, flag it loudly in the report and give the one-line fix. Add this
block near the top of `.gitleaks.toml`:

```toml
[extend]
useDefault = true
```

State plainly: until this line is added, every commit passes the secret scan
because the scan has no rules to apply. This is a silent hole, not a warning.

### Step 4: Verify gitleaks is installed and reachable (Check 4)

The hook scans with gitleaks when present and degrades to a weaker regex
fallback when it is not. Confirm the real binary is reachable.

```cmd
where gitleaks
gitleaks version
```

Evaluate:

- **OK** if `where gitleaks` resolves a path AND `gitleaks version` prints a
  version.
- **GAP** if gitleaks is not found. The pre-commit hook still runs and falls
  back to its built-in regex scan, but coverage is far weaker (a handful of
  patterns vs. gitleaks' full ruleset). Recommend installing it.

If there is a GAP, show install options without running them:

```cmd
winget install gitleaks
```

or, if Scoop is in use:

```cmd
scoop install gitleaks
```

### Step 5: Report status

Produce a single status table covering all four checks, then list specific
fixes for each gap. Lead with the overall verdict.

```
🛡️ Git-Guard Report
Repo: <repo-name>
Branch: <current-branch>

Overall: <PROTECTED / GAPS FOUND / CRITICAL GAP>

| # | Check                         | Status        | Detail                                  |
|---|-------------------------------|---------------|-----------------------------------------|
| 1 | Global pre-commit hook        | ✅ OK          | core.hooksPath set, pre-commit present  |
| 2 | .gitignore coverage           | ⚠️ GAP         | Missing: memory/, .serena/              |
| 3 | gitleaks config armed         | 🔴 CRITICAL    | NEUTERED: no rules, no useDefault       |
| 4 | gitleaks installed            | ✅ OK          | gitleaks 8.x at C:\...\gitleaks.exe     |

## Fixes
1. (Check 2) Append missing patterns to .gitignore:
   <show exact lines>
2. (Check 3) [CRITICAL] Arm gitleaks. Add to top of .gitleaks.toml:
       [extend]
       useDefault = true
   Until then, the secret scan applies zero rules and detects nothing.

## Verdict
<one or two sentences: is this repo safe to commit to right now, and what is the
single most important thing to fix>
```

Verdict rules:
- **CRITICAL GAP** overrides everything else: if Check 3 is NEUTERED, the repo
  is NOT protected even if the hook is installed and gitleaks is present, and
  the report must say so. A neutered config is the worst case because it hides
  behind a passing scan.
- **GAPS FOUND** if any non-critical check is a GAP.
- **PROTECTED** only when all four checks are OK.

## Status Levels

| Level | Meaning | Action |
|-------|---------|--------|
| 🔴 CRITICAL | gitleaks config is neutered: scanning is silently off | Add `[extend] useDefault = true` immediately |
| ⚠️ GAP | A protection layer is missing or weakened | Apply the shown fix before relying on protection |
| ✅ OK | Layer present and armed | No action needed |

## How the Layers Fit Together

| Layer | Role | What happens if it is missing |
|-------|------|-------------------------------|
| `core.hooksPath` + pre-commit | Runs the scan on every commit, every repo | No commit is scanned at all |
| `.gitignore` | Stops obvious files (.env, memory/) being staged | Sensitive files get staged and reach the scanner |
| `.gitleaks.toml` | Configures WHAT gitleaks detects | If neutered, the scanner detects nothing |
| `gitleaks` binary | Does the actual deep detection | Hook degrades to a weak regex fallback |

Git-Guard verifies all four. gitleaks does the scanning. They are different
jobs: never reach for git-guard to find secrets, and never assume an installed
hook means detection is on. Check 3 is why.

## Related Skills

- **secrets-scanner** (Pro): deep secret audit, git history analysis, client-side exposure, remediation planning
- **rls-checker** / **rls-guardian**: Supabase Row Level Security auditing and enforcement
- **api-audit**: API route auth/authz review

## Level History

- **Lv.1:** Base installer/verifier. Four-check protocol plus a status report: global pre-commit hook (core.hooksPath), .gitignore coverage with additive append from the shipped template, gitleaks config neutering detection (the silent allowlist-only hole that has shipped live in real production repos), and gitleaks binary reachability, followed by a consolidated report with a CRITICAL-overrides verdict. (Origin: MemStack, Jun 2026)
