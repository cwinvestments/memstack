---
name: verify
description: "Check completed work against stated goals before committing. Runs build, tests, and requirement checks. Triggers on verify, check this work, does it pass."
---


# ✅ Verify — Checking Work...
*Review completed work against requirements before committing.*

## Activation

When this skill activates, output:

`✅ Verify — Checking work against requirements...`

Then execute the protocol below.

## Context Guard

| Context | Status | Priority |
|---------|--------|----------|
| **User says "verify", "check this work", "does it pass"** | ACTIVE — run verification | P1 |
| **User says "is this done", "ready to commit"** | ACTIVE — run verification | P1 |
| **User is mid-task, still actively coding** | DORMANT — let them finish first | — |
| **User asks to commit or push** | DORMANT — Seal hook handles pre-push checks | — |
| **User asks to review someone else's code** | DORMANT — not a code review tool | — |

## Protocol

### Step 1: Identify the Task

Determine what was being built by checking:
- Recent conversation context (what the user asked for)
- Git diff for uncommitted changes
- Recent commits if already committed

Summarize: "**Task:** [what was being built/changed]"

### Step 2: Run Automated Checks

Run whatever applies to the current project:

**Build check:**
```bash
# Detect and run the project's build command
npm run build    # Node.js
make build       # Makefile
python -m py_compile <file>  # Python
```

**Test check:**
```bash
# Detect and run the project's test command
npm test         # Node.js
pytest           # Python
make test        # Makefile
```

**Lint check (if available):**
```bash
npm run lint     # Node.js
```

If no build/test tooling exists, skip and note "No automated checks configured."

### Step 3: Manual Requirement Check

Compare the completed work against the original requirements:
- List each requirement from the original task
- Check whether it was implemented
- Flag any gaps, missing edge cases, or regressions

### Step 4: Check for Common Issues

- **Uncommitted debug code**: `console.log`, `print()`, `debugger`, `TODO` markers left behind
- **Hardcoded values**: Magic numbers, hardcoded URLs, temp credentials
- **Missing error handling**: Unhandled promises, missing try/catch at boundaries
- **Incomplete cleanup**: Unused imports, dead code from earlier attempts

### Step 5: Generate Report

```markdown
## Verification Report
*{YYYY-MM-DD}*

### Task: {what was being built}

### Automated Checks
- [x] Build: passes / [ ] fails — {error}
- [x] Tests: passes / [ ] fails — {error}
- [x] Lint: passes / [ ] N/A

### Requirements
- [x] {Requirement 1} — implemented in {file}
- [x] {Requirement 2} — implemented in {file}
- [ ] {Requirement 3} — MISSING: {what's needed}

### Issues Found
1. {Issue} → {Suggested fix}

### Verdict: PASS / NEEDS FIX
```

### Step 6: Recommend Action

- **PASS**: "Looks good. Ready to commit."
- **NEEDS FIX**: List specific fixes needed, prioritized by severity.

## Inputs
- Current working context (project, recent changes)
- Original task requirements (from conversation or plan)
- Git diff / status for change analysis

## Outputs
- Verification report with pass/fail checklist
- Specific fix recommendations if issues found

## Example Usage

**User:** "verify this work"

```
✅ Verify — Checking work against requirements...

## Verification Report
Task: Add user registration API endpoint

### Automated Checks
- [x] Build: passes
- [x] Tests: 14/14 passing
- [x] Lint: clean

### Requirements
- [x] POST /api/register endpoint — server/routes/auth.ts
- [x] Email validation — uses zod schema
- [x] Password hashing — bcrypt with salt rounds=12
- [ ] Rate limiting — MISSING: no rate limiter on registration endpoint

### Issues Found
1. No rate limiting on /api/register → Add express-rate-limit middleware

### Verdict: NEEDS FIX (1 issue)
```

## Level History

- **Lv.1** — Base: Pre-commit verification with automated + manual checks, structured report output, framework-agnostic detection. (Origin: MemStack v3.1, Feb 2026)
