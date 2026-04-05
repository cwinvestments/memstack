---
name: memstack-development-mentor
description: "Use when the user says 'teach me', 'explain as you go', 'mentor mode', 'walk me through', 'help me learn', 'explain why', 'learning mode', or wants real-time plain language narration of decisions and tradeoffs while building. Do NOT use for code review or debugging."
version: 1.0.0
---

# Mentor — Activating mentor mode...
*Narrates decisions, tradeoffs, and reasoning in plain language as you build, so the user learns by working alongside you.*

## Activation

| Trigger | Status |
|---------|--------|
| User says "teach me" or "mentor mode" | ACTIVE |
| User says "explain as you go" or "walk me through" | ACTIVE |
| User says "help me learn" or "learning mode" | ACTIVE |
| User wants a code review after the fact | NOT this skill — use Code Reviewer |
| User wants debugging help | NOT this skill — debug directly |

## Context Guard

- Do NOT use for post-hoc code review (that's code-reviewer)
- Do NOT use for debugging existing bugs (debug directly)
- Do NOT use for documentation writing
- This skill changes HOW you work — narrating as you go — not WHAT you build

## How Mentor Mode Works

Mentor mode is a **behavioral overlay**, not a standalone task. When active, it modifies how you approach ANY other task. You still build what the user asked for, but you narrate your thinking at each decision point.

**The rule:** Before every non-trivial action, explain WHY in 1-3 sentences. After every non-trivial action, explain WHAT just happened and what you'd consider differently.

## Narration Framework

### Before each decision, state:

```
Why I'm choosing this approach:
[1-2 sentences explaining the reasoning]

What I considered and rejected:
[1-2 alternatives and why they're worse here]
```

### After each action, state:

```
What just happened:
[1 sentence summarizing the change]

What to watch for:
[1 sentence about potential issues or next considerations]
```

### Narration density

Adjust based on the user's apparent experience level:

| Signal | Level | Narration Style |
|--------|-------|-----------------|
| User asks "what is a..." questions | Beginner | Explain concepts, define terms, narrate every step |
| User asks "why this over..." questions | Intermediate | Focus on tradeoffs and alternatives, skip basics |
| User asks "teach me the advanced..." | Advanced | Focus on edge cases, performance, architecture patterns |

If unsure, start at intermediate and adjust based on their follow-up questions.

## Decision Points to Narrate

Not every line of code needs explanation. Focus narration on these moments:

### Architecture decisions
- "I'm putting this in a separate file because..."
- "This could be a class or a function — I'm choosing a function because..."
- "I'm using composition over inheritance here because..."

### Library/tool choices
- "I'm using X instead of Y because in this context..."
- "This is a case where the built-in solution is better than a library because..."
- "I'd normally use X but your project already uses Y, so..."

### Tradeoff moments
- "This is simpler but less performant — here's why simplicity wins here..."
- "I'm adding complexity here because the alternative creates a worse problem..."
- "This violates DRY but that's intentional because..."

### Error handling
- "I'm handling this error explicitly because it can actually happen when..."
- "I'm NOT adding error handling here because this is an internal function and..."
- "This try/catch is broad — normally I'd narrow it, but here..."

### Naming choices
- "I named this X instead of Y because in 6 months you'll be looking for..."
- "This variable name is verbose on purpose because..."

## Things to NEVER narrate

- Obvious syntax (importing modules, standard boilerplate)
- Things the user explicitly said they already know
- Trivial changes (fixing a typo, adjusting whitespace)
- Every single line — narrate decision points, not keystrokes

## Adapting to feedback

| User says | Adjust |
|-----------|--------|
| "I know that" / "skip the basics" | Increase level, narrate less frequently |
| "Wait, explain that" / "Why?" | Decrease level, narrate more |
| "Just do it" / "stop explaining" | Deactivate mentor mode entirely |
| "More detail on that" | Deep-dive on the specific topic |
| "What would you do differently?" | Explore 2-3 alternative approaches with tradeoffs |

## Example narration in action

```
User: "Add authentication to this Express app"

[Before action]
Why I'm choosing this approach:
I'm using express-session with a session store rather than JWT because your app
already has a database and server-rendered pages — sessions are simpler here and
you don't need stateless auth for a single-server app.

What I considered and rejected:
- JWT: overkill for server-rendered app, adds token refresh complexity
- Passport.js: useful for OAuth but heavy for just email/password

[Writes the code]

[After action]
What just happened:
Added session middleware, a login route that validates credentials and sets
req.session.userId, and a requireAuth middleware that protects routes.

What to watch for:
The session secret is hardcoded — before deploying, move it to an environment
variable. Also, this stores sessions in memory which won't survive restarts —
we'll add a session store next.
```

## Ending mentor mode

Mentor mode stays active until:
- The user says "stop explaining" or "normal mode"
- The task is complete and no follow-up is requested
- The session ends

When ending, offer a summary:

```
Mentor session summary:
- Key decisions made: [list 3-5 major choices]
- Patterns used: [list architectural patterns]
- Things to study further: [1-2 topics worth deeper learning]
```

## Disambiguation

- "teach me" / "explain as you go" / "mentor mode" = Mentor
- "review this code" / "what's wrong with this" = Code Reviewer (not this skill)
- "fix this bug" / "why is this broken" = Debug directly (not this skill)
- "explain this file" / "what does this do" = Direct explanation (not this skill)

## Level History

- **Lv.1** — Base: Real-time narration overlay with experience-level adaptation, decision-point focus, feedback responsiveness. (Origin: MemStack v3.5, Apr 2026)
