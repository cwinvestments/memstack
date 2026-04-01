---
name: memstack-development-refactor-planner
description: "Use this skill when the user says 'refactor', 'refactoring plan', 'code cleanup', 'reduce duplication', 'simplify code', 'tech debt', 'god class', 'tight coupling', or needs to systematically improve existing code. Identifies targets, assesses risk, and builds incremental execution plans. Do NOT use for writing new features or database migrations."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# Refactor Planner — Planning systematic code improvement...
*Identifies code smells, assesses refactoring risk, selects appropriate patterns, and builds incremental execution plans with rollback strategies and verification checkpoints.*

## Activation

When this skill activates, output:

`Refactor Planner — Planning systematic code improvement...`

Then execute the protocol below.

## Context Guard

| Context | Status |
|---------|--------|
| User says "refactor", "refactoring plan", "code cleanup" | ACTIVE |
| User says "tech debt", "god class", "tight coupling", "reduce duplication" | ACTIVE |
| User wants to improve existing code structure without changing behavior | ACTIVE |
| User wants to write a new feature | DORMANT — use Feature Spec |
| User wants to change database schema | DORMANT — use Migration Planner |

## Common Mistakes

| Mistake | Why It's Wrong |
|---------|---------------|
| "Big bang rewrite" | Rewriting everything at once introduces cascading failures. Incremental changes are safer and shippable. |
| "Refactor without tests" | No test coverage = no safety net. Add characterization tests BEFORE touching code. |
| "Refactor and add features simultaneously" | Mixing behavior changes with structural changes makes bugs impossible to isolate. Separate commits. |
| "No measurable goal" | "Clean up the code" is vague. Define metrics: reduce file from 800 to 200 lines, eliminate 5 duplicate blocks, etc. |
| "Skip the risk assessment" | A function called by 47 files is higher risk than a utility used in 2. Assess blast radius first. |

## Protocol

### Step 1: Gather Refactoring Context

If the user hasn't provided details, ask:

> 1. **Target** — what code needs refactoring? (file, module, class, or system)
> 2. **Pain point** — what's the specific problem? (hard to modify, duplicated, slow, confusing)
> 3. **Test coverage** — does the target code have tests? (yes, partial, none)
> 4. **Constraints** — any deadlines, frozen APIs, or deployment concerns?
> 5. **Language/framework** — what tech stack?

### Step 2: Identify Code Smells

Scan the target code for these smell categories:

**Bloaters (too big):**

| Smell | Detection | Severity |
|-------|----------|----------|
| **Long method** | Function >30 lines or >3 levels of nesting | Medium |
| **Large class / God object** | Class >300 lines or >10 public methods | High |
| **Long parameter list** | Function takes >4 parameters | Medium |
| **Primitive obsession** | Raw strings/numbers instead of domain types | Low |
| **Data clumps** | Same group of variables passed together repeatedly | Medium |

**Couplers (too connected):**

| Smell | Detection | Severity |
|-------|----------|----------|
| **Feature envy** | Method uses another class's data more than its own | Medium |
| **Inappropriate intimacy** | Classes access each other's private internals | High |
| **Message chains** | `a.getB().getC().getD().doThing()` — chain >2 deep | Medium |
| **Middle man** | Class delegates nearly everything to another class | Low |

**Dispensables (unnecessary):**

| Smell | Detection | Severity |
|-------|----------|----------|
| **Dead code** | Unreachable code, unused variables, commented-out blocks | Low |
| **Duplicate code** | Same logic in 2+ places (exact or structural) | High |
| **Speculative generality** | Abstractions, interfaces, or config for cases that don't exist | Medium |
| **Lazy class** | Class does too little to justify its existence | Low |

**Change preventers (hard to modify):**

| Smell | Detection | Severity |
|-------|----------|----------|
| **Divergent change** | One class changed for many different reasons | High |
| **Shotgun surgery** | One change requires edits across many files | High |
| **Parallel inheritance** | Creating a subclass in one hierarchy requires one in another | Medium |

**Code smell report:**

```markdown
## Code Smell Report — [Target]

| # | Smell | Location | Severity | Lines Affected |
|---|-------|----------|----------|---------------|
| 1 | [Smell name] | [file:line] | High/Med/Low | [X] |
| 2 | [Smell name] | [file:line] | High/Med/Low | [X] |
| ... | | | | |

**Summary:** [X] smells found ([X] high, [X] medium, [X] low)
**Estimated scope:** [X] files, [X] lines affected
```

### Step 3: Assess Risk

For each refactoring target, evaluate:

**Risk matrix:**

| Factor | Low Risk | Medium Risk | High Risk |
|--------|----------|------------|-----------|
| **Dependents** | 0-2 callers | 3-10 callers | 10+ callers |
| **Test coverage** | >80% covered | 40-80% covered | <40% covered |
| **Complexity** | Simple extraction | Cross-file changes | Architectural change |
| **Reversibility** | Easy to revert | Requires migration | Data format changes |
| **Blast radius** | Single file | Single module | Cross-module |

**Risk score per target:**

```markdown
| Target | Dependents | Coverage | Complexity | Reversibility | Blast Radius | Risk Score |
|--------|-----------|----------|-----------|---------------|-------------|------------|
| [File/Class] | [X] callers | [X]% | Low/Med/High | Easy/Med/Hard | File/Module/System | Low/Med/High |
```

**Risk-based ordering rule:**
1. Start with LOW risk, HIGH value targets (quick wins)
2. Then MEDIUM risk targets (with tests added first)
3. HIGH risk targets last (with comprehensive test coverage first)
4. Never refactor HIGH risk targets without >80% test coverage

### Step 4: Select Refactoring Patterns

Match each smell to the appropriate pattern:

**Extraction patterns:**

| Pattern | Use When | Before → After |
|---------|---------|----------------|
| **Extract Method** | Long method, duplicated logic block | Inline code → Named function |
| **Extract Class** | God class, divergent change | One class → Two focused classes |
| **Extract Interface** | Tight coupling, testing difficulty | Concrete dependency → Interface + implementation |
| **Extract Variable** | Complex expression, magic numbers | `if (a > 86400 && b < 3)` → `if (isExpired && belowRetryLimit)` |

**Simplification patterns:**

| Pattern | Use When | Before → After |
|---------|---------|----------------|
| **Replace Conditional with Polymorphism** | Long switch/if chains on type | Switch statement → Strategy pattern |
| **Replace Parameter with Method** | Parameter that callee can compute | `calc(getX(), getY())` → `calc()` (fetches internally) |
| **Introduce Parameter Object** | Long parameter list, data clumps | `fn(x, y, z, w)` → `fn(config)` |
| **Replace Temp with Query** | Temp variable used once after calculation | `temp = calc(); use(temp)` → `use(calc())` |

**Structural patterns:**

| Pattern | Use When | Before → After |
|---------|---------|----------------|
| **Move Method/Field** | Feature envy, misplaced responsibility | Method in wrong class → Move to correct class |
| **Inline Class** | Lazy class, middle man | Useless wrapper → Merge into user |
| **Replace Inheritance with Composition** | Fragile base class, deep hierarchy | `extends Base` → `has Base` with delegation |
| **Introduce Facade** | Complex subsystem, shotgun surgery | Direct subsystem calls → Facade mediates |

**Pattern selection table:**

```markdown
| # | Smell | Pattern | Target | Estimated Effort |
|---|-------|---------|--------|-----------------|
| 1 | [Smell] | [Pattern] | [file:line] | [X] hours |
| 2 | [Smell] | [Pattern] | [file:line] | [X] hours |
```

### Step 5: Build Execution Plan

Structure the refactoring into safe, incremental phases:

**Phase template:**

```markdown
## Refactoring Plan — [Target]

### Phase 0: Safety Net (do this first)
- [ ] Add characterization tests for current behavior
- [ ] Verify all existing tests pass
- [ ] Create a feature branch: `refactor/[target-name]`
- [ ] Document current behavior snapshot

### Phase 1: Quick Wins (low risk, high value)
**Target:** [Smell → Pattern]
- [ ] Step 1: [Specific action]
- [ ] Step 2: [Specific action]
- [ ] Verify: Run tests, confirm no behavior change
- [ ] Commit: `refactor: [description]`

### Phase 2: Core Improvements (medium risk)
**Target:** [Smell → Pattern]
- [ ] Step 1: [Specific action]
- [ ] Step 2: [Specific action]
- [ ] Verify: Run tests, confirm no behavior change
- [ ] Commit: `refactor: [description]`

### Phase 3: Structural Changes (higher risk)
**Target:** [Smell → Pattern]
- [ ] Step 1: [Specific action]
- [ ] Step 2: [Specific action]
- [ ] Verify: Run full test suite + manual smoke test
- [ ] Commit: `refactor: [description]`

### Verification Checkpoints
After each phase:
1. All tests pass (unit + integration)
2. No behavior change (same inputs → same outputs)
3. Metrics improved (lines reduced, complexity lowered)
4. Code review approved (if team)
```

**Effort estimation guide:**

| Pattern | Typical Effort | Risk Level |
|---------|---------------|-----------|
| Extract Variable | 5-15 min | Very Low |
| Extract Method | 15-30 min | Low |
| Introduce Parameter Object | 30-60 min | Low |
| Extract Class | 1-3 hours | Medium |
| Replace Conditional with Polymorphism | 2-4 hours | Medium |
| Replace Inheritance with Composition | 3-6 hours | High |
| Extract Interface + Dependency Injection | 2-5 hours | Medium-High |
| Architectural restructure (module boundaries) | 1-3 days | High |

### Step 6: Define Rollback Strategy

For each phase, document how to reverse:

```markdown
## Rollback Strategy

| Phase | Rollback Method | Time to Revert |
|-------|----------------|---------------|
| Phase 1 | `git revert [commit]` | <5 min |
| Phase 2 | `git revert [commit]` | <5 min |
| Phase 3 | `git revert [commit]` + re-run migrations if applicable | <15 min |

**Abort criteria (stop refactoring if):**
- Test failures that can't be explained within 30 minutes
- Performance regression >10% on critical paths
- Deadline pressure requires shipping current work
- Discovery of architectural issues requiring design discussion
```

### Step 7: Measure Results

Define before/after metrics:

```markdown
## Refactoring Metrics

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Lines of code (target) | [X] | [X] | -[X]% |
| Cyclomatic complexity | [X] | [X] | -[X]% |
| Number of methods | [X] | [X] | [+/-X] |
| Average method length | [X] lines | [X] lines | -[X]% |
| Duplicate code blocks | [X] | [X] | -[X] |
| Test coverage | [X]% | [X]% | +[X]% |
| Number of dependencies | [X] | [X] | -[X] |
```

## Output Format

```markdown
# Refactoring Plan — [Target]

## Code Smell Report
[From Step 2 — smells identified with severity and location]

## Risk Assessment
[From Step 3 — risk matrix for each target]

## Pattern Selection
[From Step 4 — matched patterns with estimated effort]

## Execution Plan
[From Step 5 — phased plan with verification checkpoints]

## Rollback Strategy
[From Step 6 — revert method per phase + abort criteria]

## Success Metrics
[From Step 7 — before/after targets]
```

## Completion

```
Refactor Planner — Complete!

Target: [Target name]
Smells found: [X] ([X] high, [X] medium, [X] low)
Phases: [X]
Estimated effort: [X] hours
Risk level: [Overall Low/Medium/High]
Patterns applied: [List]

Next steps:
1. Add characterization tests for current behavior (Phase 0)
2. Create feature branch: refactor/[target-name]
3. Execute Phase 1 (quick wins) and verify tests pass
4. Continue through phases, committing after each
5. Measure before/after metrics and document improvements
```

## Level History

- **Lv.1** — Base: 4 code smell categories (bloaters, couplers, dispensables, change preventers) with 16 specific smells, 5-factor risk matrix, 12 refactoring patterns in 3 groups (extraction, simplification, structural), phased execution plan template, rollback strategy with abort criteria, before/after metrics tracking. (Origin: MemStack Pro v3.2, Mar 2026)
