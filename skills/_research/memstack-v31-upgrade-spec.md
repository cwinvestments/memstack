# MemStack™ v3.1 Upgrade Spec
## For Claude Code execution — read this file and implement all tasks

## Overview
Add new skills and upgrade existing ones based on competitive analysis (GSD framework) and community tools (blader/humanizer). Maintain MemStack™'s core philosophy: zero-friction, auto-loading, framework-agnostic.

## Working Directory
C:\Projects\memstack

## Pre-Flight
- Read MEMSTACK.md to understand current skill structure and naming conventions
- Review .claude/ folder structure for how skills are defined
- Check current skill numbering (should be 14 skills currently)

---

## TASK 1: Add Humanizer Skill (#15)
**Source:** github.com/blader/humanizer (6.6K stars)
**Purpose:** Remove signs of AI-generated writing from text output

### What it does:
- Takes AI-generated content and rewrites it to sound natural/human
- Removes common AI tells: "delve", "leverage", "it's important to note", "in conclusion", excessive hedging, robotic transitions
- Preserves meaning while improving readability and voice
- Useful for: blog posts, documentation, course content, social media, client deliverables

### Implementation:
- Add as Skill #15 "Humanize" in the skills list
- Invocation: `Use the Humanize skill to clean up this content`
- Reference blader/humanizer's SKILL.md for their approach, adapt to MemStack™ format
- The skill should provide instructions for Claude to rewrite content removing AI patterns

---

## TASK 2: Add State Skill (#16)
**Inspired by:** GSD framework's STATE.md pattern
**Purpose:** Maintain a living "where am I right now" document across sessions

### What it does:
- Creates/updates a STATE.md file in .claude/ that tracks:
  - Current task/phase being worked on
  - Active decisions made this session
  - Open blockers or questions
  - Next steps (explicit, not vague)
  - Key files modified recently
- Auto-reads at session start (alongside other context)
- Auto-updates at session end or when invoking the skill

### Implementation:
- Add as Skill #16 "State" in the skills list
- Invocation: `Use the State skill to update project state`
- STATE.md template:
```markdown
# Project State
*Last updated: [timestamp]*

## Currently Working On
[Active task or phase]

## Decisions Made
- [Decision 1]: [Rationale]
- [Decision 2]: [Rationale]

## Blockers
- [ ] [Blocker description]

## Next Steps
1. [Immediate next action]
2. [Following action]

## Recently Modified Files
- [file path] — [what changed]
```

---

## TASK 3: Add Verify Skill (#17)
**Inspired by:** GSD framework's verify-work pattern
**Purpose:** Check completed work against stated goals before committing

### What it does:
- Reviews what was just built/changed against the original task requirements
- Checks for:
  - Does the code compile/run without errors?
  - Are all stated requirements met?
  - Any regressions or broken existing functionality?
  - Missing edge cases?
  - Tests passing (if applicable)?
- Outputs a verification report
- If issues found, lists them as actionable fix items

### Implementation:
- Add as Skill #17 "Verify" in the skills list
- Invocation: `Use the Verify skill to check this work`
- Should work with any project type (not just Node/React)
- Output format:
```markdown
# Verification Report
*[timestamp]*

## Task: [what was being built]

## Checks
- [x] Code compiles/runs
- [x] Requirement 1 met
- [ ] Requirement 2 — ISSUE: [description]
- [x] No regressions detected

## Issues Found
1. [Issue description] → [Suggested fix]

## Verdict: PASS / NEEDS FIX
```

---

## TASK 4: Upgrade Seal Skill — Atomic Commit Format
**Inspired by:** GSD's structured commit naming
**Purpose:** Add optional phase-task numbering to commit messages

### Current behavior:
- Seal analyzes staged changes and generates descriptive commit messages

### Upgrade:
- Add support for structured commit format: `type(scope): description`
- Types: feat, fix, docs, refactor, style, test, chore
- Optional phase-task numbering when working on phased projects: `feat(03-02): add user registration flow`
- Keep backward compatible — if no phase context exists, use standard format
- Auto-detect type from the changes (new files = feat, modifications = fix/refactor, .md files = docs)

---

## TASK 5: Upgrade Diary Skill — Structured Handoff
**Inspired by:** GSD's pause-work/resume-work pattern
**Purpose:** Better session-end handoff for seamless pickup next session

### Current behavior:
- Diary logs what was accomplished during a session

### Upgrade:
- Add a "handoff" section to diary entries that includes:
  - What was in progress (not just what was completed)
  - Any uncommitted changes and why
  - Exact next step to pick up (not vague "continue working on X")
  - Any context that would be lost between sessions (temp decisions, debugging state)
- Format:
```markdown
## Session Handoff
**In Progress:** [what was actively being worked on when session ended]
**Uncommitted Changes:** [list any unstaged/uncommitted work]
**Pick Up Here:** [exact instruction for next session to start with]
**Session Context:** [anything important that isn't captured elsewhere]
```

---

## TASK 6: Update MEMSTACK.md
- Update the main MEMSTACK.md to reflect all new/upgraded skills
- Update skill count from 14 to 17
- Add descriptions for new skills (#15 Humanize, #16 State, #17 Verify)
- Note upgrades to Seal and Diary
- Update version to v3.1

---

## TASK 7: Update README.md
- Update the GitHub repo README with new skill descriptions
- Add a "What's New in v3.1" section
- Mention GSD comparison (position MemStack™ as lightweight alternative)
- Update skill count in all relevant places

---

## Git Workflow
After all tasks complete:
1. Stage all changes
2. Use the upgraded Seal skill format: `feat(v3.1): add Humanize, State, Verify skills; upgrade Seal and Diary`
3. Push to main

---

## Notes
- Maintain existing skill naming convention (capitalized verb names)
- Keep all skills framework-agnostic
- Don't add npm dependencies — MemStack™ is pure markdown/instructions
- Test each skill's invocation instruction for clarity
- Reference: MemStack™ repo at github.com/cwinvestments/memstack
