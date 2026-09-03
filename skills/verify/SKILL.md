---
name: verify
description: "Runs this project's check chain through scripts/verify.py and reads the receipt it writes. Fires when tracked changes are finished, when the user asks whether work passes, before a commit, and before reporting a task done. Stays dormant in repositories with no detectable check chain, during read-only audits, and for edits that leave no tracked change behind."
version: 2.0.0
---


# ✅ Verify: Checking Work...
*Run the project's checks, write a receipt, read what it says.*

## Activation

When this skill activates, output:

`✅ Verify: running the check chain...`

Then follow the protocol below.

## Context Guard

| Context | Status | Priority |
|---------|--------|----------|
| **Tracked changes are finished and about to be reported done** | ACTIVE, run the chain | P1 |
| **User asks "does it pass", "verify this", "is this ready"** | ACTIVE, run the chain | P1 |
| **About to commit** | ACTIVE, a receipt costs less before the commit than after | P1 |
| **User is mid-task, still editing** | DORMANT, a receipt for a half-finished tree ages out the moment the next edit lands | n/a |
| **Read-only audit or investigation** | DORMANT, nothing changed, so there is nothing to verify | n/a |
| **Edits left no tracked change (new untracked files only)** | DORMANT, the gate does not see untracked files and neither does the chain | n/a |
| **Repo where `verify list` detects nothing** | DORMANT, but read NOTHING_DETECTED below before concluding this | n/a |

## What the CLI actually detects

`scripts/verify.py` detects three families and nothing else. Anything outside this list goes unchecked, so a passing receipt is not a claim that the project is sound:

| Family | Detected when | Runs |
|--------|---------------|------|
| npm | `package.json` has a `scripts` entry named `test`, `lint`, `typecheck` or `build` | `npm run <script>`, one check per script, in that order |
| pytest | `pytest.ini`, or `pyproject.toml` with a `[tool.pytest]` section, or a `tests/` directory | `python -m pytest -q` |
| ruff | `ruff.toml`, `.ruff.toml`, or `pyproject.toml` with a `[tool.ruff]` section | `ruff check .` |

A detected check that cannot run becomes a SKIP carrying its reason: npm missing from PATH, `node_modules` absent, pytest not importable, ruff not installed. A SKIP is not a pass, because nothing ran.

Run `python scripts/verify.py list` to see the chain without executing it.

## Protocol

### Step 1: Run the chain

```bash
python scripts/verify.py run --task-id <session-id>
```

Use the session id as the task id. The receipt is named after it, so one session overwrites its own receipt on a re-run instead of littering the directory, and the Stop gate's block message names this exact command with this exact id.

Each check gets 900 seconds before it is recorded as a FAIL with a timeout note.

### Step 2: Read the receipt

It lands at `.memstack/receipts/<task-id>.json` under the repo root. That directory writes a `.gitignore` holding `*` the first time it is created, so the evidence never asks to be committed and never appears in `git status`.

The receipt is evidence, not paperwork. Read these fields before saying anything about the outcome:

- **verdict**: PASS, FAIL or NOTHING_DETECTED for the chain as a whole.
- **checks**: one record per check, each with its `status`, `exit` code, duration, and the last 2000 characters of combined output. The failing output is in here, so quote it rather than paraphrasing it.
- **dirty**: true when tracked changes exist on top of HEAD. Untracked files are excluded, so this matches what the gate measures.
- **untracked_count**: how many untracked files the tree carries, recorded separately so a pile of backups stays visible without being mistaken for work.
- **tree_fingerprint**: sha256 over HEAD plus every tracked-change line. This is the receipt's identity, and it is what the gate compares.
- **can_fail_demonstrated**: true only when the selftest has passed against this exact copy of `verify.py`, matched by file hash. When it is false the receipt comes from a verify that has never been shown to report a failure, so a PASS from it carries less weight. Re-earn it with `python scripts/verify.py selftest`.

### Step 3: Act on the verdict

| Exit | Verdict | What it means for the session |
|------|---------|-------------------------------|
| 0 | PASS | At least one check ran and none failed. Safe to report the work done and to commit. |
| 1 | FAIL | A check failed. The session is not done. Fix it and re-run rather than narrating around it. |
| 3 | NOTHING_DETECTED | Nothing was detected, or everything detected was skipped. Nothing was verified, so nothing is confirmed. Say that plainly instead of calling it a pass. |
| 64 | usage error | The command line was wrong. Fix the invocation and re-run. |

Exit 2 never comes from `run`. It belongs to the gate alone, so a 2 always means a Stop event was blocked, not that a check failed.

## The Stop gate

The same file runs as a Stop hook, deciding once per turn whether unverified work is sitting in the tree.

- **Armed only by `.verify-required`** at the repo root, found from the git toplevel. Without that file the gate allows silently every turn, because a note on a session that never asked for a gate is noise. The marker stays untracked on purpose: committing it would arm every clone.
- **Honors one kind of receipt.** The newest receipt whose `verdict` is PASS and whose `kind` is `run`, and only when its `tree_fingerprint` equals the tree's fingerprint right now. A selftest receipt is refused even though it says PASS, because selftest proves the tool works and never runs the project's checks.
- **Allows when there is nothing to verify.** No tracked changes plus a receipt for this same HEAD means no unverified edit exists.
- **Blocks with exit 2** and a message naming the exact run command that clears it.
- **Yields after two blocks.** It counts consecutive blocks per session against one unchanged fingerprint, and on the third it allows with a YIELDING note instead. A block that has repeated twice has stopped carrying information.
- **Allows on its own failures.** Unparseable payload, git unable to describe the tree, internal error: each one allows, loudly where there is something worth saying. A gate that kills the session it protects gets deleted.

Editing a tracked file changes the fingerprint, which is what stops a stale receipt from clearing new work.

## The repair cap

After a FAIL, take two rounds of fixing. If a third round is still not producing a passing receipt, stop and tell the user what is failing and what has been tried.

This mirrors the gate's own cap, for the same reason: by the third round the evidence says the problem is not the one being fixed, and further rounds spend the user's tokens confirming that.

## Known Gotchas

| Gotcha | Why it matters |
|--------|----------------|
| Untracked files never count | The fingerprint drops every `??` line, so a pile of `.bak` files is not why a block happened. Look at the tracked changes instead of tidying scratch files. |
| A FAIL that predates the edits is still the session's to surface | The receipt records what the chain reports now. A pre-existing failure gets reported, not skipped, because the user cannot act on a problem nobody mentioned. |
| NOTHING_DETECTED is not a pass | It is exit 3 precisely so it cannot be mistaken for exit 0. It means nothing was verified, which is a different claim from nothing being wrong. |
| A SKIP with a reason is not a pass either | A chain where everything skipped resolves to NOTHING_DETECTED for the same reason: an unrun check confirms nothing. |
| A selftest receipt cannot clear the gate | Selftest never touches the project's own checks, so honoring it would let a green result from a chain that never read the project unlock the project's work. |
| `can_fail_demonstrated: false` weakens a PASS | It marks a verify that has not proven it can report failure against this exact file. Run the selftest before leaning on that receipt. |
| Doc-only edits to tracked files still arm the gate | No check reads prose, so the chain has nothing to say about it, but the fingerprint changed and a run receipt is still what clears it. |

## Inputs
- The repository at the current working directory
- The session id, used as the receipt's task id

## Outputs
- A receipt at `.memstack/receipts/<task-id>.json`
- A verdict and an exit code, reported to the user as they came back

## Level History

- **Lv.1** Base: Pre-commit verification with automated + manual checks, structured report output, framework-agnostic detection. (Origin: MemStack v3.1, Feb 2026)
- **Lv.2** CLI and gate: Rewritten around `scripts/verify.py`. Detection is bounded and named, results are receipts carrying a tree fingerprint, and a Stop gate blocks unverified tracked work when armed. (Origin: MemStack Session 2, Sep 2026)
