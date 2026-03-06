---
name: launch-plan
description: "Use when the user says 'launch plan', 'product launch', 'launch strategy', 'go-to-market', 'GTM plan', 'launch calendar', or is planning a product or feature release."
---


# 🚀 Launch Plan — Go-to-Market Calendar
*Build a day-by-day launch calendar from pre-launch through post-launch with task checklists and contingency plans.*

## Activation

When this skill activates, output:

`🚀 Launch Plan — Building your go-to-market calendar...`

| Context | Status |
|---------|--------|
| **User says "launch plan", "product launch", "go-to-market"** | ACTIVE |
| **User wants a launch calendar or timeline** | ACTIVE |
| **User is planning a release and needs sequenced tasks** | ACTIVE |
| **User wants ongoing funnel design (not a time-bound launch)** | DORMANT — see sales-funnel |
| **User wants ad copy only** | DORMANT — see facebook-ad or google-ad |

## Protocol

### Step 1: Gather Inputs

Ask the user for:
- **Product/service**: What are you launching?
- **Launch date**: When is the target launch?
- **Audience size**: Email list, social following, existing customers
- **Available channels**: Email, social platforms, paid ads, PR, partnerships, podcast, blog
- **Team size**: Solo or team? Who handles what?
- **Budget**: Marketing budget for the launch window

### Step 2: Pre-Launch Phase (Weeks -4 to -1)

**Week -4: Foundation**
- [ ] Define launch messaging: one-liner, elevator pitch, value proposition
- [ ] Create landing page / waitlist page
- [ ] Set up email sequences (warm-up, announcement, follow-up)
- [ ] Plan content calendar for teasers

**Week -3: Audience Building**
- [ ] Start teaser content on social channels
- [ ] Publish "behind the scenes" content
- [ ] Reach out to affiliates/partners for launch support
- [ ] Begin waitlist promotion

**Week -2: Content Creation**
- [ ] Write launch emails (minimum 3: announcement, reminder, last chance)
- [ ] Create ad creatives for paid campaigns
- [ ] Prepare social media posts for launch week (batch create)
- [ ] Record demo/walkthrough video

**Week -1: Final Prep**
- [ ] Test purchase/sign-up flow end to end
- [ ] Send "launching soon" email to waitlist
- [ ] Schedule all social posts
- [ ] Brief any partners/affiliates with assets
- [ ] Set up tracking: UTMs, conversion pixels, analytics dashboards

### Step 3: Launch Week (Days 1-7)

**Day 1 — Launch Day:**
- [ ] Send launch announcement email (segment: most engaged first)
- [ ] Publish all social announcements
- [ ] Activate paid ad campaigns
- [ ] Post in relevant communities (with value, not spam)
- [ ] Monitor: sales, traffic, email metrics hourly

**Day 2 — Social Proof:**
- [ ] Share first customer reactions/testimonials
- [ ] Respond to all comments and questions
- [ ] Send email #2 to non-openers (different subject line)

**Day 3 — Overcome Objections:**
- [ ] Publish FAQ or objection-handling content
- [ ] Send targeted email to clickers-but-not-buyers
- [ ] Review ad performance, pause underperformers

**Day 4-5 — Case Studies:**
- [ ] Share detailed use case or customer story
- [ ] Guest post or podcast appearance (if arranged)
- [ ] Adjust ad targeting based on Day 1-3 data

**Day 6-7 — Urgency Close:**
- [ ] Send "closing soon" or "bonus expiring" email
- [ ] Final social push with urgency angle
- [ ] Last-chance retargeting ads to warm audiences

### Step 4: Post-Launch Phase (Weeks +1 to +2)

**Week +1: Capitalize**
- [ ] Collect and publish testimonials/case studies
- [ ] Send "thank you" email to buyers with next steps
- [ ] Analyze launch metrics: total revenue, conversion rate, CAC, top channels
- [ ] Begin retargeting campaign for non-converters

**Week +2: Optimize**
- [ ] Publish launch retrospective (internal)
- [ ] Set up evergreen funnel from launch assets
- [ ] Plan follow-up offers or upsells
- [ ] Gather customer feedback for product improvement

### Step 5: Define Owners and Deadlines

Present a RACI-style task table:

| Task | Owner | Deadline | Status |
|------|-------|----------|--------|
| Landing page | [name] | Week -4 | Pending |
| Email sequences | [name] | Week -2 | Pending |
| Ad creatives | [name] | Week -2 | Pending |
| Social content | [name] | Week -1 | Pending |
| ... | ... | ... | ... |

### Step 6: Contingency Plan

If launch underperforms (< 50% of target by Day 3):
1. **Diagnose**: Check traffic (awareness problem) vs conversion rate (offer problem)
2. **Traffic low**: Increase ad spend, do a flash collaboration, email blast to cold list
3. **Conversion low**: Add urgency (limited bonus), add proof (live testimonial), simplify offer
4. **Both low**: Extend launch window, pivot messaging, consider soft re-launch with adjusted positioning
5. **Nuclear option**: Pause, gather feedback, reposition, re-launch in 30 days

### Step 7: Metrics Dashboard

Track daily during launch:

| Metric | Day 1 | Day 2 | Day 3 | Day 4 | Day 5 | Day 6 | Day 7 |
|--------|-------|-------|-------|-------|-------|-------|-------|
| Site visits | | | | | | | |
| Email opens | | | | | | | |
| Email clicks | | | | | | | |
| Sales/sign-ups | | | | | | | |
| Revenue | | | | | | | |
| Ad spend | | | | | | | |
| ROAS | | | | | | | |

### Step 8: Output

Present the complete launch plan as a day-by-day calendar:

```
━━━ LAUNCH PLAN: [Product Name] ━━━━━━━━━━━
Launch Date: [date]
Revenue Target: $[amount]
Channels: [list]

── PRE-LAUNCH ─────────────────────────────
Week -4: [tasks]
Week -3: [tasks]
Week -2: [tasks]
Week -1: [tasks]

── LAUNCH WEEK ────────────────────────────
Day 1: [tasks with times]
Day 2-7: [daily tasks]

── POST-LAUNCH ────────────────────────────
Week +1: [tasks]
Week +2: [tasks]

── CONTINGENCY ────────────────────────────
[if/then decision tree]

── METRICS TRACKER ────────────────────────
[empty dashboard template]
```

## Inputs
- Product/service description
- Launch date
- Audience size and channels
- Team members and roles
- Budget

## Outputs
- 4-week pre-launch task calendar
- Day-by-day launch week schedule with checklists
- 2-week post-launch optimization plan
- Owner/deadline task table
- Contingency plan with decision triggers
- Daily metrics dashboard template

## Level History

- **Lv.1** — Base: 7-week launch calendar (4 pre + 1 launch + 2 post), daily task checklists with owners, contingency decision tree, metrics dashboard template, multi-channel coordination (email, social, paid, partnerships). (Origin: MemStack v3.2, Mar 2026)
