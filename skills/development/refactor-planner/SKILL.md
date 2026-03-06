---
name: refactor-planner
description: "Use when the user says 'refactor', 'refactoring plan', 'code cleanup', 'tech debt', 'reduce duplication', or wants to systematically improve code quality without changing behavior."
---

# 🔧 Refactor Planner — Systematic Code Improvement
*Identify refactoring targets, assess risk, and build an incremental execution plan with before/after examples and regression coverage.*

## Activation

When this skill activates, output:

`🔧 Refactor Planner — Analyzing refactoring opportunities...`

| Context | Status |
|---------|--------|
| **User says "refactor", "refactoring plan", "code cleanup"** | ACTIVE |
| **User wants to reduce duplication or simplify code** | ACTIVE |
| **User mentions tech debt, god classes, or tight coupling** | ACTIVE |
| **User wants to write tests for existing code** | DORMANT — see test-writer |
| **User wants a database schema change** | DORMANT — see migration-planner |
| **User wants to plan new features (not improve existing)** | DORMANT — see feature-spec |

## Protocol

### Step 1: Gather Inputs

Ask the user for:
- **Codebase scope**: Full codebase or specific module/directory?
- **Language/framework**: What's the tech stack?
- **Pain points**: What feels wrong? (slow to change, bugs keep recurring, hard to understand)
- **Test coverage**: Do tests exist? What's the coverage level?
- **Timeline**: How much time can you dedicate to refactoring?
- **Constraints**: Any areas that can't be touched? (legacy integrations, frozen APIs)

### Step 2: Identify Refactoring Targets

Scan for common code smells and categorize:

| Category | Smell | Detection | Impact |
|----------|-------|-----------|--------|
| **Duplication** | Copy-pasted logic across files | Same pattern in 3+ places | High — bugs fixed in one place, missed in others |
| **Long Functions** | Functions > 50 lines or > 3 levels of nesting | Line count + cyclomatic complexity | Medium — hard to test, hard to understand |
| **God Classes** | Classes with 10+ methods or 500+ lines | Size + responsibility count | High — changes here ripple everywhere |
| **Tight Coupling** | Module A imports internals of Module B | Import analysis, circular deps | High — can't change one without breaking the other |
| **Dead Code** | Unused functions, unreachable branches | Static analysis, grep for references | Low — noise, but safe to remove |
| **Primitive Obsession** | Passing raw strings/numbers instead of types | Parameter lists with same types | Medium — type errors at runtime |
| **Feature Envy** | Function uses more data from another module than its own | Cross-module data access patterns | Medium — logic in the wrong place |
| **Shotgun Surgery** | One change requires edits in 5+ files | Git history — changes that always touch same files | High — slow velocity, error-prone |

For each target found, document:
```
TARGET: [file:function or class]
  Smell: [category]
  Severity: [critical / high / medium / low]
  Files affected: [count]
  Test coverage: [covered / partial / none]
  Evidence: [specific code pattern or metric]
```

### Step 3: Assess Risk Per Refactor

For each target, evaluate risk:

| Target | Files Touched | Test Coverage | Dependency Count | Frequency of Change | Risk Level |
|--------|--------------|---------------|-----------------|---------------------|------------|
| [target] | [count] | [%] | [count] | [high/med/low] | [🔴🟡🟢] |

**Risk scoring:**
- 🔴 **High risk**: Touches 5+ files, low test coverage, many dependents — needs tests BEFORE refactoring
- 🟡 **Medium risk**: Touches 2-4 files, partial coverage — refactor carefully with incremental PRs
- 🟢 **Low risk**: Isolated change, good coverage — safe to refactor immediately

**Risk mitigation rules:**
- No test coverage on affected code? → Write tests FIRST, then refactor
- Circular dependency? → Break one direction first, verify, then break the other
- Public API change? → Deprecate old, add new, migrate callers, remove old
- Database-touching code? → Coordinate with migration-planner skill

### Step 4: Prioritize by Impact

Rank refactoring targets using impact scoring:

| Target | Frequency of Change | Bug History | Developer Pain | Business Impact | Priority Score |
|--------|---------------------|-------------|----------------|-----------------|---------------|
| [target] | [high/med/low] | [bugs linked] | [complaints] | [blocks features?] | [1-10] |

**Prioritization formula:**
- Change frequency (1-3): How often does this code change? (3 = weekly)
- Bug history (1-3): How many bugs originated here? (3 = recurring)
- Developer pain (1-3): How much does the team complain? (3 = constant friction)
- Business impact (1-3): Does this block feature work? (3 = actively blocking)
- Priority Score = sum (max 12, normalize to 10)

**Priority tiers:**
- **P1 (8-10)**: Refactor this sprint — it's actively causing problems
- **P2 (5-7)**: Refactor this quarter — it slows the team down
- **P3 (1-4)**: Refactor opportunistically — improve when you're nearby

### Step 5: Design Incremental Approach

For each P1/P2 target, define the refactoring strategy:

**Strategy options:**

| Strategy | When to Use | PR Size | Risk |
|----------|-------------|---------|------|
| **Extract function** | Long function with identifiable sub-tasks | Small | Low |
| **Extract class/module** | God class with distinct responsibilities | Medium | Medium |
| **Introduce interface** | Tight coupling between modules | Small | Low |
| **Replace conditional with polymorphism** | Long if/else or switch chains | Medium | Medium |
| **Consolidate duplicates** | Same logic in 3+ places | Medium | Medium |
| **Strangler fig** | Large legacy module — replace incrementally | Small per PR | Low per step |
| **Parallel implementation** | Critical path — can't risk breaking it | Large total, but safe | Low |

**Incremental PR plan:**
```
Refactor: [Target Name]

PR 1: Add tests for current behavior
  Files: [test files]
  Risk: None — no behavior change
  Review: Quick

PR 2: Extract [component/function]
  Files: [source files]
  Risk: Low — behavior preserved, tests verify
  Review: Standard

PR 3: Update callers to use new abstraction
  Files: [caller files]
  Risk: Medium — multiple files changing
  Review: Careful

PR 4: Remove old code
  Files: [cleanup files]
  Risk: Low — dead code removal
  Review: Quick
```

### Step 6: Before/After Examples

For each refactoring target, provide concrete code examples:

```
── BEFORE ─────────────────────────────────

// [file path]
[current code showing the problem]

── AFTER ──────────────────────────────────

// [file path]
[refactored code showing the improvement]

── WHY BETTER ─────────────────────────────
• [specific improvement 1: e.g., "testable in isolation"]
• [specific improvement 2: e.g., "single responsibility"]
• [specific improvement 3: e.g., "reusable across modules"]
```

Guidelines for before/after:
- Show real patterns from the codebase, not generic examples
- Keep examples focused — show the essence, not the full file
- Explain WHY the after is better, not just HOW it's different
- If the refactor changes an API, show the caller migration too

### Step 7: Regression Test Plan

For each refactoring step, define what to test:

| Refactor Step | Tests to Write Before | Tests to Verify After | Regression Risk |
|---------------|----------------------|----------------------|-----------------|
| Extract function | Unit tests for current behavior | Same tests pass against extracted version | Low |
| Change interface | Integration tests for all callers | All caller tests still pass | Medium |
| Remove dead code | Verify no references exist | Smoke test full app | Low |
| Consolidate duplicates | Tests for each duplicate's behavior | Single test covers consolidated version | Medium |

**Test strategy per risk level:**
- 🟢 **Low risk**: Existing tests + visual verification
- 🟡 **Medium risk**: Add targeted tests before refactoring, run full suite after
- 🔴 **High risk**: Full characterization tests before, integration tests after, manual QA on critical paths

**Regression checklist per refactor PR:**
- [ ] All existing tests pass
- [ ] New tests written for untested affected code
- [ ] No behavior change in public APIs (unless intentional)
- [ ] Performance not degraded (benchmark if applicable)
- [ ] No new circular dependencies introduced
- [ ] Linting/type checking passes

### Step 8: Execution Order

Define the sequence that minimizes risk:

```
── REFACTORING ROADMAP ────────────────────

Phase 1: Foundation (Week 1)
  1. [Low-risk refactor] — builds confidence, establishes pattern
  2. [Test backfill] — increases coverage for Phase 2 targets
  Milestone: Coverage on critical paths ≥ 80%

Phase 2: Core Improvements (Weeks 2-3)
  3. [High-impact refactor A] — most painful code smell
  4. [High-impact refactor B] — second most painful
  Milestone: Velocity improvement measurable

Phase 3: Cleanup (Week 4)
  5. [Dead code removal] — reduce noise
  6. [Final consolidation] — merge remaining duplicates
  Milestone: Codebase health metrics improved
```

**Execution rules:**
- Never refactor two tightly coupled modules simultaneously
- Complete one refactor before starting the next
- If a refactor reveals more work, add it to the backlog — don't scope-creep
- Ship each PR independently — no "refactor mega-PR"
- Pair refactoring with feature work when possible (boy scout rule)

### Step 9: Output

Present the complete refactoring roadmap:

```
━━━ REFACTORING ROADMAP ━━━━━━━━━━━━━━━━━━

── TARGETS IDENTIFIED ─────────────────────
[target list with severity and smell type]

── RISK ASSESSMENT ────────────────────────
[risk table per target]

── PRIORITY RANKING ───────────────────────
P1: [targets to fix this sprint]
P2: [targets to fix this quarter]
P3: [targets to fix opportunistically]

── INCREMENTAL PR PLAN ────────────────────
[per-target PR sequence]

── BEFORE/AFTER EXAMPLES ──────────────────
[code examples per target]

── REGRESSION TEST PLAN ───────────────────
[test strategy per refactor step]

── EXECUTION PHASES ───────────────────────
Phase 1: [timeline + targets + milestone]
Phase 2: [timeline + targets + milestone]
Phase 3: [timeline + targets + milestone]

── METRICS TO TRACK ───────────────────────
• Cyclomatic complexity (before/after)
• Test coverage % (before/after)
• Lines of duplicated code (before/after)
• Average PR review time (should decrease)
• Bug rate in refactored modules (should decrease)
```

## Inputs
- Codebase scope and tech stack
- Known pain points and problem areas
- Current test coverage level
- Available timeline for refactoring
- Constraints (frozen areas, public APIs)

## Outputs
- Categorized refactoring targets with severity ratings
- Risk assessment per target (files touched, coverage, dependencies)
- Priority ranking by impact (change frequency, bug history, developer pain)
- Incremental PR plan per refactor (no big-bang rewrites)
- Before/after code examples for each target
- Regression test plan per refactor step
- Phased execution roadmap with milestones and metrics

## Level History

- **Lv.1** — Base: 8-category code smell detection, risk assessment per refactor (files × coverage × dependencies), impact-based prioritization (change frequency × bug history × dev pain), incremental PR strategy (extract → migrate → remove), before/after code examples, regression test plan per step, phased execution roadmap with metrics tracking. (Origin: MemStack v3.2, Mar 2026)
