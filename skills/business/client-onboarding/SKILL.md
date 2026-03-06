---
name: client-onboarding
description: "Use when the user says 'client onboarding', 'new client', 'onboard client', 'welcome client', 'kickoff', or wants to create a structured onboarding process for new clients."
---

# 🤝 Client Onboarding — New Client Setup System
*Design a complete onboarding package with welcome emails, intake questionnaire, access checklists, kickoff agenda, and communication protocol.*

## Activation

When this skill activates, output:

`🤝 Client Onboarding — Designing your client onboarding system...`

| Context | Status |
|---------|--------|
| **User says "client onboarding", "new client", "onboard client"** | ACTIVE |
| **User wants to set up a new client engagement** | ACTIVE |
| **User mentions kickoff meeting, intake form, or welcome email** | ACTIVE |
| **User wants to draft a contract (not onboarding)** | DORMANT — see contract-template |
| **User wants to send an invoice** | DORMANT — see invoice-generator |
| **User wants internal team onboarding (not client)** | DORMANT |

## Protocol

### Step 1: Gather Inputs

Ask the user for:
- **Service type**: What do you offer? (web dev, consulting, design, marketing, SaaS)
- **Client tier**: Is this a standard or premium engagement?
- **Project duration**: One-time project or ongoing retainer?
- **Tools used**: What platforms do you need the client on? (GitHub, Figma, Slack, etc.)
- **Team size**: Solo or team? Who interacts with the client?
- **Existing process**: Any current onboarding steps you want to keep?

### Step 2: Design Welcome Email Sequence

**Email 1 — Welcome (Day 0, immediately after signing):**
```
Subject: Welcome to [Your Company]! Here's what happens next

Hi [Client First Name],

Welcome aboard! We're excited to work with you on [project name].

Here's what to expect in the next few days:

1. You'll receive an intake questionnaire (please complete
   within 48 hours)
2. We'll set up your project tools and send access
   credentials
3. We'll schedule our kickoff meeting for [target date range]

Your primary point of contact is [Name] ([email]).
Response time: within [X] business hours.

If you have any immediate questions, reply to this email.

Looking forward to getting started!

[Your Name]
[Your Company]
```

**Email 2 — Intake Questionnaire (Day 0, sent with welcome):**
```
Subject: Quick questionnaire to kick things off — [Project Name]

Hi [Client First Name],

To make sure we hit the ground running, please fill out this
brief questionnaire:

[Link to questionnaire]

It takes about 15-20 minutes and covers:
• Project goals and success metrics
• Brand assets and guidelines
• Technical access and credentials
• Timeline preferences and deadlines

Please complete by [date — 48 hours from now].

Thanks!
[Your Name]
```

**Email 3 — Access & Setup (Day 1-2):**
```
Subject: Your project tools are ready — [Project Name]

Hi [Client First Name],

Your project environment is set up! Here's your access:

[Tool 1]: [access link/instructions]
[Tool 2]: [access link/instructions]
[Tool 3]: [access link/instructions]

Your kickoff meeting is scheduled for:
📅 [Date] at [Time] ([timezone])
📍 [Meeting link]

Agenda attached. Please review beforehand.

See you there!
[Your Name]
```

**Email 4 — Post-Kickoff Summary (Day 3-5, after kickoff):**
```
Subject: Kickoff summary + next steps — [Project Name]

Hi [Client First Name],

Great kickoff! Here's a summary of what we discussed:

Key decisions:
• [Decision 1]
• [Decision 2]
• [Decision 3]

Next steps:
• [Your team] will [action] by [date]
• [Client] will [action] by [date]

Timeline:
• Milestone 1: [date]
• Milestone 2: [date]
• Final delivery: [date]

Questions? Reply here or message us on [Slack/channel].

[Your Name]
```

### Step 3: Create Intake Questionnaire

**Section 1 — Project Overview:**
- What is the primary goal of this project?
- How will you measure success? (specific metrics if possible)
- Who is the target audience/end user?
- What's the hard deadline, if any?
- Are there any competitors or examples you admire?

**Section 2 — Brand & Assets:**
- Do you have brand guidelines? (attach or link)
- Logo files (SVG, PNG, or vector preferred)
- Brand colors (hex codes if known)
- Preferred fonts
- Tone of voice: formal, casual, playful, authoritative?
- Existing content to incorporate (copy, images, videos)

**Section 3 — Technical Access:**
- Domain registrar login (or who manages DNS)
- Hosting provider and credentials
- CMS access (WordPress, Webflow, Shopify admin)
- Analytics accounts (Google Analytics, Search Console)
- Social media accounts (if relevant)
- API keys or third-party service credentials
- Repository access (GitHub org invite)

**Section 4 — Communication Preferences:**
- Preferred communication channel: Email, Slack, Teams?
- Best times for meetings (timezone + availability)
- Who is the primary decision-maker?
- Who else needs to review/approve deliverables?
- How often do you want progress updates? (daily, weekly, bi-weekly)

### Step 4: Tool/Platform Access Checklist

| Tool | Purpose | Access Type | Status |
|------|---------|-------------|--------|
| **GitHub** | Code repository | Org invite or repo collaborator | ☐ |
| **Figma** | Design files | Team invite | ☐ |
| **Slack** | Communication | Channel or shared workspace | ☐ |
| **Vercel/Netlify** | Hosting | Team member or transfer | ☐ |
| **Google Analytics** | Analytics | Viewer or editor access | ☐ |
| **Stripe** | Payments | Dashboard access or API keys | ☐ |
| **CMS** | Content | Admin or editor role | ☐ |
| **Email provider** | Marketing | API key or team access | ☐ |
| **Domain registrar** | DNS | Login or DNS record access | ☐ |
| **Cloud provider** | Infrastructure | IAM role or service account | ☐ |

**Access request template:**
```
Hi [Client Name],

To get your project set up, I need access to the following:

1. [Tool] — [specific access level needed]
   How to grant: [step-by-step instructions]

2. [Tool] — [specific access level needed]
   How to grant: [step-by-step instructions]

My email for invites: [your email]
My GitHub username: [username]

Please share credentials via [secure method — 1Password,
encrypted email, or dedicated credentials channel].

⚠️ Never send passwords in plain email. Use [recommended
secure sharing tool].
```

### Step 5: Kickoff Meeting Agenda

```
── KICKOFF MEETING AGENDA ─────────────────
Duration: 60 minutes
Attendees: [list]
Date: [date]

0:00 — Introductions (5 min)
  • Team introductions and roles
  • Client stakeholders and decision authority

0:05 — Project Overview (10 min)
  • Review project goals and success metrics
  • Confirm scope from questionnaire responses
  • Identify any gaps or open questions

0:15 — Timeline & Milestones (10 min)
  • Walk through project phases
  • Confirm key dates and deadlines
  • Identify dependencies on client (content, feedback, approvals)

0:25 — Communication & Process (10 min)
  • Communication channels and response times
  • Meeting cadence (weekly standups, bi-weekly reviews)
  • Feedback and approval process
  • How to request changes (change order process)

0:35 — Technical Discussion (15 min)
  • Review technical requirements
  • Confirm tool access and environment setup
  • Discuss integrations and third-party dependencies
  • Address technical risks or constraints

0:50 — Q&A (5 min)
  • Open floor for questions
  • Clarify any concerns

0:55 — Next Steps (5 min)
  • Confirm immediate action items (with owners + dates)
  • Schedule next meeting
  • Share meeting notes within 24 hours
```

### Step 6: Communication Protocol

```
── COMMUNICATION PROTOCOL ─────────────────

CHANNELS:
  Primary: [Slack / Email]
  Urgent: [Phone / SMS — for emergencies only]
  Meetings: [Zoom / Google Meet] — always recorded if agreed
  Documents: [Notion / Google Docs / Confluence]
  Files: [Google Drive / Dropbox / Figma]

RESPONSE TIMES:
  Email: Within [4-8] business hours
  Slack: Within [2-4] business hours
  Urgent: Within [1] hour during business hours

MEETING CADENCE:
  Weekly standup: [day] at [time] — 15 min (async option)
  Bi-weekly review: [day] at [time] — 30 min
  Monthly retrospective: [day] at [time] — 30 min (retainer only)

FEEDBACK PROCESS:
  1. Deliverable shared → Client has [48 hours] to review
  2. Feedback collected in [tool/format]
  3. One round of revisions included
  4. Additional revision rounds billed at [rate]

ESCALATION:
  Level 1: Project lead ([name]) — [email]
  Level 2: Account manager ([name]) — [email]
  Level 3: Owner ([name]) — [email]

STATUS UPDATES:
  Frequency: [weekly]
  Format: [brief email / Slack message / shared dashboard]
  Content: What was done, what's next, any blockers
```

### Step 7: Project Setup Checklist

```
── PROJECT SETUP CHECKLIST ────────────────

REPOSITORY:
  ☐ Create repo from template/boilerplate
  ☐ Set up branch protection rules
  ☐ Add client as collaborator (if applicable)
  ☐ Create initial README with project overview
  ☐ Set up .env.example with required variables

ENVIRONMENTS:
  ☐ Development environment configured
  ☐ Staging environment deployed
  ☐ Production environment provisioned (not deployed)
  ☐ Environment variables set per environment

CI/CD:
  ☐ Build pipeline configured
  ☐ Test pipeline configured
  ☐ Auto-deploy to staging on merge to develop
  ☐ Manual deploy to production on release tag

MONITORING:
  ☐ Error tracking set up (Sentry)
  ☐ Analytics configured (GA4, Mixpanel, PostHog)
  ☐ Uptime monitoring (optional for MVP)
  ☐ Log aggregation (optional for MVP)

PROJECT MANAGEMENT:
  ☐ Project board created (Linear, GitHub Projects, Notion)
  ☐ Milestones mapped to board
  ☐ Client given view access (if shared board)
  ☐ First sprint/iteration planned
```

### Step 8: Output

Present the complete onboarding package:

```
━━━ CLIENT ONBOARDING: [Client Name] ━━━━━━

── WELCOME SEQUENCE ───────────────────────
Email 1 (Day 0): Welcome + expectations
Email 2 (Day 0): Intake questionnaire
Email 3 (Day 1-2): Access & setup
Email 4 (Day 3-5): Post-kickoff summary

── INTAKE QUESTIONNAIRE ───────────────────
[4 sections: overview, brand, technical, communication]

── ACCESS CHECKLIST ───────────────────────
[tool access table with status]

── KICKOFF AGENDA ─────────────────────────
[60-min structured agenda]

── COMMUNICATION PROTOCOL ─────────────────
[channels, response times, meeting cadence, escalation]

── PROJECT SETUP ──────────────────────────
[repo, environments, CI/CD, monitoring checklists]

── TIMELINE ───────────────────────────────
Day 0: Contract signed → Welcome emails sent
Day 0-2: Questionnaire completed, access granted
Day 3-5: Kickoff meeting
Day 5-7: Project environment set up
Week 2: First deliverable/milestone
```

## Inputs
- Service type and client tier
- Project duration and scope
- Tools and platforms used
- Team structure and roles
- Existing onboarding process (optional)

## Outputs
- 4-email welcome sequence with copy templates
- Intake questionnaire (project, brand, technical, communication sections)
- Tool/platform access checklist with request template
- 60-minute kickoff meeting agenda
- Communication protocol (channels, response times, escalation)
- Project setup checklist (repo, environments, CI/CD, monitoring)
- Complete onboarding timeline (Day 0 through Week 2)

## Level History

- **Lv.1** — Base: 4-email welcome sequence, 4-section intake questionnaire, tool access checklist with secure credential sharing, 60-min kickoff agenda, communication protocol with escalation ladder, project setup checklist (repo/environments/CI-CD/monitoring), onboarding timeline. (Origin: MemStack v3.2, Mar 2026)
