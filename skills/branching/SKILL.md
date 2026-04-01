---
name: branching
description: "Use when the user says 'branch', 'branching', 'dev branch', 'merge to master', 'branch strategy', 'git branch', 'feature branch', or needs to set up or follow a dev-branch workflow. Enforces dev-branch workflow: all work on dev, merge to master only after review."
---

# Branching — Dev-branch workflow for safe, reviewed releases

## Activation

When this skill activates, output:

`Branching — Enforcing dev-branch workflow...`

## Rules

1. **All new work happens on the `dev` branch.** Never commit directly to `master`.
2. **Merge to `master` only after Reviewer confirms working.** No exceptions.
3. **Commit message format for merges:** `merge: [description] dev->master`
4. **Never force-push to `master`.** If there's a conflict, resolve it on `dev` first.

## Setup (New Project)

```bash
git checkout -b dev
git push -u origin dev
```

Then set `dev` as your working branch for all sessions.

## Merge to Master (When Ready)

Only after Reviewer has confirmed the work is complete and tested:

```bash
git checkout master
git merge dev
git push
git checkout dev
```

## Context Guard

| Context | Status |
|---------|--------|
| Any git commit, push, or branch operation | ACTIVE |
| Setting up a new project's git workflow | ACTIVE |
| Reading code, debugging, or discussing architecture | DORMANT |

## Level History

- **Lv.1** — Base: Dev-branch workflow rules, setup instructions, merge protocol. (Origin: MemStack v3.3.4, Mar 2026)
