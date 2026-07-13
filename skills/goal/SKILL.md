---
name: goal
description: "Use when the user says 'goal', 'set a goal', 'define the goal', 'plan this properly', or starts a task that needs a clear finish line and verification. Structures work into TASK / WHY / OUTCOME / CONSTRAINTS / VERIFICATION before execution begins."
version: 1.0.0
---


# 🎯 Goal — Finish Line Defined
*Define what "done" looks like and how you'll prove it — before you write a line of code.*

## Activation

When this skill activates, output:

`🎯 Goal — Finish line defined.`

Then walk the user through the five fields in order, one prompt at a time or as a single template — whichever fits the flow. Fill in what the request already tells you; ask only for what's missing. Put the most weight on **VERIFICATION**: it is the field that is required, the field that is skipped most often, and the field that turns "I think it's done" into "I can show it's done." Do not let a goal close without a concrete, checkable verification criterion.

## Context Guard

| Context | Status |
|---------|--------|
| **User says "goal", "set a goal", "define the goal", "plan this properly"** | ACTIVE — structure the five fields |
| **User is starting a non-trivial task with a fuzzy finish line** | ACTIVE — offer to define the goal first |
| **User asks "how will we know this is done?" / "what's the definition of done?"** | ACTIVE — VERIFICATION-first |
| **User is mid-execution and just wants the next step** | DORMANT — use `work`, not `goal` |
| **The goal is already clearly stated with a checkable outcome** | DORMANT — don't re-litigate a good goal |
| **Casual question, chit-chat, or a one-line lookup** | DORMANT — do not activate |

## The Five Fields

A goal is a task with a finish line you can stand on. Five fields:

1. **TASK** — *what to do.* The concrete action, in one sentence. Required.
2. **WHY** — *why it matters / who it's for.* Optional, but it keeps scope honest and kills gold-plating. Skip it if it's obvious.
3. **OUTCOME** — *the exact finished result — the definition of done.* Not "improve X" but the specific end state that exists when you're finished. Required.
4. **CONSTRAINTS** — *what must or must not be done.* Boundaries: no new dependencies, don't change the public API, stay under budget. Optional; list as many as apply.
5. **VERIFICATION** — *how you'll PROVE the outcome is complete.* A concrete, observable, checkable criterion — a command to run, an output to see, a behavior to reproduce. **Required, and load-bearing.**

> A goal without a concrete VERIFICATION criterion is **incomplete**, not merely unpolished. "It works," "done," and "tests pass" are not verification — they assert success without naming what you'd observe to confirm it. That gap is exactly how a green build ships the wrong behavior. State the check, not the vibe.

## How It Works

The skill shells out to the **goal engine** for parsing and validation — the same engine the Architect stage uses — so a drafted goal is checked the same way everywhere.

```bash
# Print the blank five-field template
python -m memstack_skill_loader.goal template

# Validate a drafted goal (reads the labeled text, reports errors + warnings)
python -m memstack_skill_loader.goal validate
```

`validate` enforces the rules: TASK, OUTCOME, and VERIFICATION must be present; a present-but-vacuous VERIFICATION (e.g. "it works") comes back as a warning telling you to state a concrete, checkable criterion. Errors mean the goal isn't ready to execute; warnings mean tighten it before you trust it.

> **Note:** the engine module (`goal_engine.py`) exists today; the thin CLI entry (`python -m memstack_skill_loader.goal`) is wired in a later registration step. If the command isn't callable yet, don't block — guide the user through the five fields by hand and show the template inline (below). The discipline is the point; the CLI is a convenience.

Inline template (fallback when the CLI isn't available):

```
TASK: (what to do)
WHY: (why it matters / who it's for - optional)
OUTCOME: (the exact finished result - what 'done' looks like)
CONSTRAINTS: (what must or must not be done - optional, one per line)
VERIFICATION: (how you'll prove the outcome is complete - a concrete, checkable criterion)
```

## Quick Commands

- **/goal** — start structuring a goal from the current request
- **/goal template** — show the blank five-field template
- **"set a goal" / "define the goal" / "plan this properly"** — natural-language triggers that open the same flow

## Example Usage

**User:** "make the scanner better"

That's a wish, not a goal — there's no finish line and no way to prove success. Structured:

```
🎯 Goal — Finish line defined.

TASK: Improve the site scanner's transport-security scoring
WHY: Users trust the score to flag insecure sites; today HTTP and HTTPS
     sites can score the same, which is misleading
OUTCOME: The scan assigns a strictly lower security score to a plain-HTTP
         site than to the same site served over HTTPS
CONSTRAINTS:
  - no new dependencies
  - don't change the score scale or the JSON output shape
VERIFICATION: run the scanner against http://example.test and
              https://example.test (same content) and confirm the HTTP
              scan's numeric score is lower than the HTTPS scan's
```

Why this matters: a vague version ("scanner feels better," "tests pass") could ship with the HTTP and HTTPS scores still identical and every existing test still green — the build passes while the behavior is wrong. The VERIFICATION line makes that failure impossible to miss: two scans, one comparison, a criterion you either meet or you don't. Define that line *before* execution, and "done" stops being a matter of opinion.

## Inputs
- The user's raw request or task description
- Optional: a drafted goal in the five-field labeled format (for `validate`)
- Engine: `python -m memstack_skill_loader.goal` (template / validate)

## Outputs
- A structured goal with all five fields, VERIFICATION concrete and checkable
- Validation results: errors (not ready) and warnings (tighten before trusting)
- A finish line that execution and review can both be measured against

## Level History

- **Lv.1** — Base: Five-field goal structuring (TASK / WHY / OUTCOME / CONSTRAINTS / VERIFICATION) with a required, checkable VERIFICATION criterion; backed by the shared goal engine (`goal_engine.py`) used by both this skill and the Architect stage. (Origin: MemStack, Jul 2026)
