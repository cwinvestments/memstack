---
name: memstack-business-sop-builder
description: "Use this skill when the user says 'create SOP', 'write SOP', 'standard operating procedure', 'document process', 'process documentation', 'runbook', 'playbook', or is creating step-by-step documentation for a repeatable process. Do NOT use for project proposals or scope documents."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# 📋 SOP Builder — Documenting standard operating procedure...
*Generates a structured Standard Operating Procedure with numbered steps, prerequisites, decision points, verification checkpoints, rollback steps, and time estimates.*

## Activation

When this skill activates, output:

`📋 SOP Builder — Identifying process and building procedure...`

Then execute the protocol below.

| Context | Status |
|---------|--------|
| User says "create SOP" or "write SOP" or "document process" | ACTIVE |
| User says "runbook" or "playbook" or "process documentation" | ACTIVE |
| Creating step-by-step instructions for a repeatable workflow | ACTIVE |
| Writing a one-time guide or tutorial | DORMANT |
| Discussing process improvement at a high level | DORMANT |

### Anti-patterns

| Trap | Reality Check |
|------|---------------|
| "The steps are obvious" | What's obvious to you is opaque to a new team member at 2 AM. Write every step. |
| "Just follow the README" | READMEs explain concepts. SOPs give exact actions in exact order. Different purpose. |
| "We'll remember the edge cases" | You won't. Decision points and rollback steps are the whole point of an SOP. |
| "This process never changes" | Every process changes. Version numbers and last-updated dates prevent stale docs from causing outages. |
| "Anyone can figure out if it worked" | Explicit verification checkpoints ("you should see X") catch failures before they cascade. |

## Protocol

### Step 1: Identify the Process

If the user hasn't specified the process, ask:

> What process should this SOP document? For example:
> - Deploying to production
> - Onboarding a new developer
> - Handling a customer bug report
> - Running a database migration
> - Publishing a release
> - Setting up a new project

Then gather:
1. **Process name** — clear, specific title
2. **Audience** — who will follow this SOP? (developer, ops, new hire, non-technical)
3. **Trigger** — what event kicks off this process? (PR merged, customer request, scheduled)
4. **Frequency** — how often is this run? (daily, weekly, per release, ad-hoc)
5. **Critical?** — does failure cause downtime, data loss, or revenue impact?

### Step 2: Define Prerequisites

List everything needed before starting:

```markdown
## Prerequisites

### Required Access
| System | Access Level | How to Request |
|--------|-------------|---------------|
| GitHub | Write access to repo | Ask team lead in #dev-access |
| Railway | Deploy permissions | Railway dashboard → Team → Invite |
| Supabase | Database admin | Supabase dashboard → Settings → Team |
| AWS S3 | Read/write to production bucket | IT ticket #aws-access |

### Required Tools
| Tool | Version | Install Command |
|------|---------|----------------|
| Node.js | 20+ | `nvm install 20` |
| Railway CLI | Latest | `npm install -g @railway/cli` |
| Git | 2.40+ | Pre-installed on most systems |

### Required Knowledge
- Familiarity with [relevant concept]
- Completed [training/onboarding step]
- Access to [documentation/wiki link]

### Before You Begin
- [ ] Verify you have all required access (test each login)
- [ ] Pull latest code from main branch
- [ ] Notify team in [channel] that you're starting this process
- [ ] Block [estimated time] on your calendar
```

**Rules:**
- Every tool, login, and permission is listed — no assumptions
- Include "how to get access" for each system (not just "you need access")
- Include a pre-flight checklist the operator runs before step 1

### Step 3: Write Numbered Steps

Each step follows a strict format:

```markdown
## Procedure

### Step 1: [Action verb] [specific thing]
**Time estimate:** ~5 minutes
**Can fail:** Yes

**Action:**
1. Navigate to [specific location]
2. Run the following command:
   ```bash
   npm run build
   ```
3. Wait for the build to complete (typically 1-3 minutes)

**Verification:**
- [ ] Build output shows "Build successful" with zero errors
- [ ] `dist/` directory contains updated files
- [ ] File count is similar to previous build (sanity check)

**If it fails:**
- Build error with dependency issue → Run `npm ci` and retry
- Build error with TypeScript type error → Fix the type error, commit, and restart from Step 1
- Build times out (> 10 minutes) → Check for infinite loops in recent changes
```

**Step writing rules:**
- Start every step title with an **action verb** (Run, Open, Navigate, Verify, Configure)
- No vague steps ("set up the environment") — every action is copy-pasteable or clickable
- Include the **exact command**, **exact URL**, or **exact menu path**
- Mark whether each step **can fail** — if yes, it needs verification and failure handling
- Time estimates help the operator know if something is taking too long

### Step 4: Add Decision Points

For steps with branching logic, use clear if/then formatting:

```markdown
### Step 4: Check migration status
**Time estimate:** ~2 minutes
**Can fail:** Yes

**Action:**
1. Run: `supabase migration list`
2. Review the output

**Decision point:**

| Situation | Action |
|-----------|--------|
| All migrations show `applied` | Continue to Step 5 |
| One migration shows `pending` | Run `supabase db push` then re-check |
| Migration shows `failed` | Stop. Go to Rollback Procedure below |
| Connection refused error | Verify VPN is connected, retry in 30 seconds |
| Unknown error | Screenshot the error, post in #dev-help, wait for response |

**Do NOT continue to Step 5 until all migrations show `applied`.**
```

**Decision point rules:**
- Every `can fail: Yes` step gets a decision table
- Cover the 3-5 most common failure modes (not just happy path)
- Include "unknown error" row — operators need to know what to do when nothing matches
- Use bold warnings for steps where continuing on failure causes cascading damage

### Step 5: Add Verification Checkpoints

Major milestones get dedicated verification steps:

```markdown
### Checkpoint A: Pre-deployment verification
**Time estimate:** ~3 minutes

Before proceeding to deployment, verify ALL of the following:

| Check | How to Verify | Expected Result |
|-------|--------------|-----------------|
| Build passes | `npm run build` exits cleanly | Exit code 0, no errors |
| Tests pass | `npm test` exits cleanly | All tests green |
| Env vars set | Railway dashboard → Variables | All vars from .env.example present |
| Database ready | `supabase status` | Database is running, migrations applied |
| Branch is clean | `git status` | No uncommitted changes |

**All checks must pass.** If any check fails, resolve it before continuing.
Do not skip checks "because it worked last time."
```

**Checkpoint rules:**
- Place checkpoints before irreversible actions (deployment, data migration, public release)
- Every check has a specific command or action to run and an expected result
- Emphasize that ALL checks must pass — no skipping

### Step 6: Include Rollback Steps

For any step that modifies state (deployment, data changes, config updates):

```markdown
## Rollback Procedure

Use this procedure if deployment fails or causes issues in production.

### Rollback Step 1: Revert deployment
**Time estimate:** ~2 minutes

1. Open Railway dashboard → Deployments
2. Find the last successful deployment (green checkmark)
3. Click the three-dot menu → "Rollback to this deploy"
4. Wait for rollback to complete (typically 30-60 seconds)

**Verification:**
- [ ] Railway shows the previous deployment as active
- [ ] Health check endpoint returns 200: `curl https://[app].up.railway.app/health`
- [ ] Users can access the application

### Rollback Step 2: Revert database migration (if applicable)
**Time estimate:** ~5 minutes

1. Run the rollback migration:
   ```bash
   supabase db execute --file supabase/migrations/[number]_rollback.sql
   ```
2. Verify the schema matches the previous state

**WARNING:** Database rollbacks may cause data loss if the forward migration added columns that received data. Assess the risk before proceeding.

### Rollback Step 3: Notify team
1. Post in #incidents: "Rolled back [deployment name]. Investigating [brief issue]."
2. Update status page if customer-facing
3. Create incident ticket for post-mortem
```

**Rollback rules:**
- Every deployment/migration step needs a corresponding rollback
- Rollback steps are just as detailed as forward steps
- Include data loss warnings where applicable
- Always end rollback with team notification

### Step 7: Add Time Estimates

Summarize the total time at the top of the document:

```markdown
## Time Summary

| Phase | Estimated Time |
|-------|---------------|
| Prerequisites check | 5 minutes |
| Steps 1-3 (preparation) | 15 minutes |
| Steps 4-6 (execution) | 20 minutes |
| Steps 7-8 (verification) | 10 minutes |
| **Total (happy path)** | **~50 minutes** |
| **Total (with 1 failure + rollback)** | **~75 minutes** |

**Schedule buffer:** Block 1.5x the happy path time on your calendar.
```

**Time estimate rules:**
- Include happy path total AND failure path total
- Recommend 1.5x calendar buffer
- Individual step estimates help operators identify if a step is taking too long

### Step 8: Assemble Final Document

Output the complete SOP:

```markdown
# SOP: [Process Name]

| Field | Value |
|-------|-------|
| **Version** | 1.0 |
| **Last updated** | YYYY-MM-DD |
| **Author** | [Name] |
| **Audience** | [Who follows this SOP] |
| **Trigger** | [When to run this process] |
| **Frequency** | [How often] |
| **Estimated time** | [Happy path total] |
| **Critical** | [Yes/No — does failure cause downtime?] |

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Procedure](#procedure)
   - Step 1: [title]
   - Step 2: [title]
   - ...
   - Checkpoint A: [title]
   - Step N: [title]
3. [Rollback Procedure](#rollback-procedure)
4. [Time Summary](#time-summary)
5. [Change Log](#change-log)

---

[Prerequisites section]

[Procedure section with steps, decision points, checkpoints]

[Rollback Procedure section]

[Time Summary section]

---

## Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | YYYY-MM-DD | [Name] | Initial version |
```

**Output summary:**

```
📋 SOP Builder — Complete

Process: [name]
Audience: [who]
Steps: [count] steps, [count] decision points, [count] checkpoints
Rollback: [count] rollback steps
Estimated time: [happy path] / [with failure]

Document: [word count] words

Next steps:
1. Review steps with someone who runs this process
2. Do a dry run following the SOP exactly
3. Store in team wiki/docs and link from relevant README
4. Schedule quarterly review to keep it current
```

## Level History

- **Lv.1** — Base: Process identification, prerequisites with access/tools, numbered steps with action verbs, decision point tables, verification checkpoints, rollback procedures, time estimates, versioned final document with change log. (Origin: MemStack Pro v3.2, Mar 2026)
