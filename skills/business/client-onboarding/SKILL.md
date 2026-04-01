---
name: memstack-business-client-onboarding
description: "Use this skill when the user says 'client onboarding', 'new client', 'onboard client', 'kickoff meeting', 'intake form', 'welcome email', or needs welcome sequences, questionnaires, and setup checklists for new clients. Do NOT use for contracts or invoicing."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# Client Onboarding — Setting up new client...
*Produces a complete client onboarding package with welcome email, intake questionnaire, kickoff meeting agenda, access provisioning checklist, expectations document, and 30/60/90-day check-in schedule.*

## Activation

When this skill activates, output:

`Client Onboarding — Setting up new client...`

Then execute the protocol below.

## Context Guard

| Context | Status |
|---------|--------|
| User says "client onboarding", "new client", "onboard client" | ACTIVE |
| User says "kickoff meeting", "intake form", "welcome email" | ACTIVE |
| User just signed a new client and needs to set up the engagement | ACTIVE |
| User wants a contract or agreement | DORMANT — use Contract Template |
| User wants to send an invoice | DORMANT — use Invoice Generator |

## Common Mistakes

| Mistake | Why It's Wrong |
|---------|---------------|
| "Start working immediately" | Without intake and alignment, you'll waste the first 2 weeks on rework. |
| "Skip the expectations document" | Unclear expectations cause 80% of client conflicts. Document everything upfront. |
| "No single point of contact" | Multiple client contacts = conflicting feedback. Designate one decision-maker. |
| "Forget access provisioning" | Waiting for logins and credentials delays the project by days or weeks. |
| "No check-in schedule" | Without scheduled touchpoints, small issues become big surprises. |

## Protocol

### Step 1: Gather Client Information

If the user hasn't provided details, ask:

> 1. **Client** — company name, primary contact, industry
> 2. **Project** — what was sold? (service type, scope, deliverables)
> 3. **Timeline** — start date, key milestones, end date
> 4. **Communication** — preferred channel (email, Slack, calls)?
> 5. **Access needed** — what systems, accounts, or assets do you need from them?

### Step 2: Send Welcome Email

**Welcome email template:**

```
Subject: Welcome aboard! Here's what happens next — [Your Company]

Hi [Client Name],

Welcome to [Your Company]! We're excited to work with you on [Project Name].

Here's what to expect in the next few days:

1. **Intake questionnaire** (attached / linked below) — please complete
   by [date, 2-3 business days]. This helps us understand your goals,
   preferences, and current setup.

2. **Access provisioning** — we'll need a few logins and assets from you
   (details in the questionnaire). The sooner we have access, the sooner
   we can start.

3. **Kickoff call** — I've sent a calendar invite for [date/time].
   This is a [30/60]-minute call where we align on goals, timeline, and
   communication cadence.

Your primary point of contact is [Name] ([email]). For anything urgent,
you can also reach us at [phone/Slack].

If you have any questions before the kickoff, just reply to this email.

Looking forward to getting started!

[Your Name]
[Title]
[Company]
[Phone]
```

### Step 3: Intake Questionnaire

**Standard intake questions:**

```markdown
## Client Intake Questionnaire

### About Your Business
1. What does your business do? (One paragraph)
2. Who is your target audience?
3. What makes you different from competitors?
4. What's your brand voice? (Professional, casual, technical, friendly)

### About This Project
5. What's the #1 goal for this project?
6. What does success look like? How will you measure it?
7. Are there specific deadlines we should know about?
8. What have you tried before? What worked and what didn't?

### Design & Brand
9. Do you have brand guidelines? (colors, fonts, logo files)
10. Share 3 examples of [websites/designs/content] you admire
11. Share 3 examples of what you DON'T want

### Technical
12. What platforms/tools do you currently use? (CMS, email, analytics, etc.)
13. Do you have Google Analytics / Search Console set up?
14. Who manages your domain and hosting?

### Access (we'll need these before kickoff)
15. [ ] Website admin login (URL + credentials)
16. [ ] Google Analytics / Search Console access (add [email] as editor)
17. [ ] Social media account access (or manager role)
18. [ ] Brand assets (logo files, brand guide, fonts)
19. [ ] Any existing content or copy documents
20. [ ] Current customer list or CRM access (if applicable)

### Communication Preferences
21. Preferred communication channel: Email / Slack / Phone / Other
22. Best time for meetings (timezone + availability)
23. Who is the primary decision-maker on your side?
24. Who else needs to approve deliverables?
```

### Step 4: Kickoff Meeting Agenda

**Kickoff meeting template (60 minutes):**

```markdown
## Kickoff Meeting — [Client Name] × [Your Company]
**Date:** [Date] | **Time:** [Time] | **Duration:** 60 min

### Attendees
- [Your team: names and roles]
- [Client team: names and roles]

### Agenda

**1. Introductions (5 min)**
- Who's on each team and their role in this project

**2. Project overview (10 min)**
- Recap: what we're building and why
- Confirm scope and deliverables (reference SOW/contract)
- Confirm timeline and key milestones

**3. Goals & success metrics (10 min)**
- Review client's #1 goal (from intake questionnaire)
- Agree on measurable success criteria
- Identify any risks or concerns early

**4. Communication & process (10 min)**
- Communication channel (email / Slack / project tool)
- Meeting cadence: [weekly / biweekly] check-ins on [day] at [time]
- How to submit feedback (one document, not scattered emails)
- Turnaround times: our deliverables [X days], your feedback [X days]

**5. Review intake questionnaire (10 min)**
- Walk through answers, clarify anything unclear
- Confirm access items are provided or in progress

**6. Immediate next steps (10 min)**
- [ ] [Action item 1] — [Owner] — by [Date]
- [ ] [Action item 2] — [Owner] — by [Date]
- [ ] [Action item 3] — [Owner] — by [Date]

**7. Questions & close (5 min)**
- Open floor for any questions
- Confirm next meeting date
```

### Step 5: Access Provisioning Checklist

**Access checklist (customize per project):**

| # | Item | Status | Owner | Notes |
|---|------|--------|-------|-------|
| 1 | Website CMS login | [ ] Pending | Client | [URL] |
| 2 | Google Analytics (Editor access) | [ ] Pending | Client | Add [email] |
| 3 | Google Search Console | [ ] Pending | Client | Add [email] |
| 4 | Social media accounts | [ ] Pending | Client | [Platforms] |
| 5 | Email marketing platform | [ ] Pending | Client | [Platform] |
| 6 | Brand assets (logo, fonts, guide) | [ ] Pending | Client | Shared drive link |
| 7 | Hosting / DNS access | [ ] Pending | Client | [Provider] |
| 8 | Payment processor (if applicable) | [ ] Pending | Client | [Stripe, etc.] |
| 9 | Project management tool invite | [ ] Pending | You | Add client to [tool] |
| 10 | Slack / Teams channel setup | [ ] Pending | You | Create shared channel |

### Step 6: Expectations Document

```markdown
## Working Agreement — [Client Name] × [Your Company]

### Communication
- **Primary channel:** [Email / Slack]
- **Response time:** We respond within [1 business day / 4 hours]
- **Meeting cadence:** [Weekly / Biweekly] on [Day] at [Time]
- **Urgent issues:** [Phone / text to [number]]

### Deliverable Process
1. We deliver [drafts/designs/builds] by the agreed date
2. You provide feedback within [3-5 business days]
3. Feedback should be consolidated (one person collects all feedback)
4. We incorporate feedback and deliver the revision
5. [2-3] revision rounds are included; additional rounds at $[X]/hour

### What We Need From You
- Timely responses to questions and feedback requests
- Access to all required systems (see provisioning checklist)
- One designated decision-maker for approvals
- Content and assets delivered by agreed deadlines

### What You Can Expect From Us
- Transparent progress updates at every check-in
- Proactive communication about any delays or blockers
- Professional, high-quality deliverables on schedule
- No scope changes without written agreement and revised estimate

### Revision Policy
- [2] rounds of revisions included per deliverable
- Revisions must be requested within [5 business days] of delivery
- Out-of-scope changes require a change order

### Escalation Path
If anything feels off, reach out early:
1. Contact your project lead: [Name, email]
2. If unresolved: Contact [Manager/Owner name, email]
```

### Step 7: 30/60/90-Day Check-In Schedule

| Checkpoint | When | Focus | Format |
|-----------|------|-------|--------|
| **Week 1** | Day 5 | Quick pulse — any blockers? Access complete? | 15-min call or Slack |
| **30 days** | Day 30 | Progress review, milestone check, feedback loop | 30-min call |
| **60 days** | Day 60 | Mid-project review, scope check, quality audit | 30-min call |
| **90 days** | Day 90 | Results review, project wrap-up or renewal | 45-min call |

**Check-in agenda (30/60/90):**
1. Progress update: what's been completed, what's next
2. Metrics review: are we hitting the success criteria?
3. Client satisfaction: what's working, what could improve?
4. Scope check: any changes needed? (change order if yes)
5. Action items for next period

## Output Format

```markdown
# Client Onboarding Package — [Client Name]

## Welcome Email
[From Step 2]

## Intake Questionnaire
[From Step 3]

## Kickoff Meeting Agenda
[From Step 4]

## Access Provisioning Checklist
[From Step 5]

## Working Agreement
[From Step 6]

## Check-In Schedule
[From Step 7]
```

## Completion

```
Client Onboarding — Complete!

Client: [Name]
Project: [Project name]
Kickoff date: [Date]
Check-in cadence: [Weekly / Biweekly]
Documents prepared: 6 (welcome email, questionnaire, kickoff agenda,
  access checklist, expectations doc, check-in schedule)

Next steps:
1. Send the welcome email today
2. Attach/link the intake questionnaire
3. Send kickoff meeting calendar invite
4. Follow up on access provisioning within 48 hours
5. Share the working agreement at the kickoff meeting
```

## Level History

- **Lv.1** — Base: Welcome email template, 24-question intake questionnaire, 60-minute kickoff meeting agenda, 10-item access provisioning checklist, working agreement (communication, deliverables, revisions, escalation), 30/60/90-day check-in schedule with agendas. (Origin: MemStack Pro v3.2, Mar 2026)
