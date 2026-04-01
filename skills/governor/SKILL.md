---
name: governor
description: "Use when the user says 'new project', 'project init', 'what tier', 'scope', or discusses project maturity, complexity budget, or what's appropriate to build."
version: 1.0.0
---


# 🏛️ Governor — Portfolio Governance

*Enforce tier-appropriate complexity. Prevent over-engineering the #1 waste of time in AI-assisted development.*

## Activation

When this skill activates, output:

`🏛️ Governor — Checking project tier constraints...`

Then execute the protocol below.

## Context Guard

| Context | Status | Priority |
|---------|--------|----------|
| **User starts a new project ("new project", "init", "scaffold")** | ACTIVE — assign tier | P1 |
| **User asks "what tier", "what's allowed", "scope check"** | ACTIVE — report current tier constraints | P1 |
| **User proposes work that exceeds current tier** | ACTIVE — flag and advise | P2 |
| **User is executing work within tier constraints** | DORMANT — don't interrupt | — |
| **User explicitly overrides ("I know, do it anyway")** | DORMANT — user has authority | — |

## Anti-Rationalization

If you're thinking any of these, STOP — you're about to let scope creep happen:

| You're thinking... | Reality |
|---|---|
| "Adding tests is always good practice" | Not for prototypes. Tests for throwaway code waste time. |
| "This needs proper auth" | Single-user tools don't need auth. Add it when there are users. |
| "Let me add CI/CD while I'm at it" | CI/CD for a prototype is gold-plating. Ship first. |
| "Error handling should be comprehensive" | Prototype error handling = crash and log. That's it. |
| "I should add monitoring" | < 10 users? Console.log is your monitoring. |
| "This should be configurable" | Hardcode it. Make it configurable when someone asks. |

## Protocol

### Step 1: Determine Project Tier

Ask or infer the project tier from context:

| Tier | Description | Effort Allocation |
|------|-------------|-------------------|
| **Prototype** | Exploring an idea. May be thrown away. | Minimal — working code only |
| **MVP** | Validated idea, building for first users. | Moderate — basic quality gates |
| **Production** | Serving real users, needs reliability. | Full — complete quality stack |

If tier is unclear, default to **Prototype** and escalate only when evidence suggests otherwise.

### Step 2: Apply Tier Constraints

#### Prototype — Move Fast, Break Things

| Allowed | NOT Allowed |
|---------|-------------|
| Working code that demonstrates the idea | Unit tests |
| Hardcoded config values | CI/CD pipelines |
| Console.log for debugging | Type systems / strict typing |
| Single-file scripts | Monitoring / alerting |
| README with setup instructions | Authentication / authorization |
| | Infrastructure-as-code |
| | Rate limiting |
| | Database migrations (use SQLite) |

**Prototype rule:** If it works in a demo, ship it.

#### MVP — Prove It Works

| Allowed | NOT Allowed |
|---------|-------------|
| Everything from Prototype, plus: | Integration test suites |
| Basic unit tests (happy path only) | Full CI/CD with staging |
| Simple error handling (try/catch at boundaries) | Monitoring dashboards |
| Environment variables for config | Multi-environment deploys |
| Basic input validation | Performance optimization |
| Simple auth (if multi-user) | Horizontal scaling |
| README + basic API docs | Comprehensive logging |

**MVP rule:** If the first 10 users can use it reliably, ship it.

#### Production — Reliability Matters

| Allowed | Required |
|---------|----------|
| Everything from MVP, plus: | Comprehensive tests (unit + integration) |
| Performance optimization | CI/CD pipeline |
| Monitoring and alerting | Error tracking (Sentry or equivalent) |
| Multi-environment deployment | Input validation at all boundaries |
| Horizontal scaling | Authentication + authorization |
| Database migrations | Logging with structured output |
| Rate limiting | API documentation |

**Production rule:** If it breaks at 3 AM, someone gets paged.

### Step 3: Report Constraints

Output a brief summary:

```
🏛️ Project: {name}
   Tier: {Prototype | MVP | Production}
   Allowed: {brief list}
   NOT allowed: {brief list of key restrictions}
```

### Step 4: Flag Violations

When the user proposes work that exceeds the tier, flag it:

```
🏛️ Governor — Scope check:
   You're proposing {X}, but this is a {Tier} project.
   {X} is a {higher tier} concern. Current tier doesn't require it.
   Want to proceed anyway, or skip it for now?
```

Always defer to the user if they override. Governor advises, doesn't block.

## Anti-Patterns by Tier

### Prototype Anti-Patterns — DON'T DO THIS

1. **Writing tests for throwaway code** — If the prototype proves the idea wrong, those tests are wasted
2. **Adding auth to single-user tools** — You're the only user. Skip it
3. **Setting up CI/CD** — You're not deploying to production. `git push` is your CI
4. **Using TypeScript for a quick script** — JavaScript is fine for prototypes
5. **Adding rate limiting** — You have 0 users. Rate limit when you have 10
6. **Creating database migrations** — SQLite + direct schema changes. Migrate when you scale
7. **Building admin dashboards** — Database GUI tool (TablePlus, DBeaver) is your admin panel
8. **Over-abstracting** — 3 similar lines > 1 premature abstraction
9. **Adding comprehensive error handling** — Crash and read the stack trace. That's debugging
10. **Monitoring and alerting** — Console output is your monitoring

### MVP Anti-Patterns — DON'T DO THIS

1. **Integration test suites** — Happy-path unit tests are enough at MVP
2. **Multi-environment deploys** — One environment. Dev IS production
3. **Performance optimization** — Make it work, make it right, THEN make it fast. You're at step 2
4. **Horizontal scaling** — Vertical scale (bigger server) until proven insufficient
5. **Comprehensive logging** — Log errors and key events. Not every function call

### Production Anti-Patterns — DON'T DO THIS

1. **Skipping tests to "move faster"** — You'll move slower when bugs hit production
2. **Manual deployments** — CI/CD exists for a reason. Set it up
3. **No error tracking** — If you can't see errors, you can't fix them
4. **Ignoring security** — Production code faces the internet. Act like it

## Inputs
- Project name and context
- Current tier (from user, STATE.md, or project CLAUDE.md)
- Proposed work scope

## Outputs
- Tier assignment with constraint summary
- Violation flags when scope exceeds tier
- Anti-pattern warnings

## Level History

- **Lv.1** — Base: 3-tier governance system with phase constraints, anti-patterns list, and scope violation flagging. Inspired by Intellegix portfolio governance. (Origin: MemStack v3.2, Feb 2026)
