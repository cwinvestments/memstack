---
name: content-pipeline
description: "Use when the user says 'content pipeline', 'content automation', 'auto-publish', 'content workflow', 'repurpose content', 'blog to social', or wants to automate the creation, formatting, and publishing of content across platforms."
---


# 📡 Content Pipeline — Multi-Platform Content Automation
*Design an end-to-end content pipeline from ideation through publishing with AI integration, quality gates, and cross-platform formatting.*

## Activation

When this skill activates, output:

`📡 Content Pipeline — Designing your content automation pipeline...`

| Context | Status |
|---------|--------|
| **User says "content pipeline", "content automation", "auto-publish"** | ACTIVE |
| **User wants to repurpose content across platforms** | ACTIVE |
| **User mentions YouTube + blog + social automation** | ACTIVE |
| **User wants an n8n workflow (content is just the use case)** | Chain: content-pipeline → n8n-workflow-builder |
| **User wants a single social media post (not a pipeline)** | DORMANT |
| **User wants a launch announcement sequence** | DORMANT — see launch-plan |

## Protocol

### Step 1: Gather Inputs

Ask the user for:
- **Content type**: Blog posts, YouTube videos, podcasts, newsletters, social media, or multi-format?
- **Source material**: Where does raw content come from? (scripts, recordings, notes, ideas list)
- **Target platforms**: Where should content be published? (blog, YouTube, Twitter/X, LinkedIn, Instagram, newsletter)
- **Posting schedule**: How often? (daily, 3x/week, weekly, biweekly)
- **Team**: Solo creator or team? Who reviews before publish?
- **Existing tools**: What do you already use? (CMS, email platform, video editor)

### Step 2: Design Pipeline Stages

Map the full content lifecycle:

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│ IDEATION │──→│ CREATION │──→│  REVIEW  │──→│ FORMAT   │──→│ PUBLISH  │
│          │   │          │   │          │   │          │   │          │
│ Topics   │   │ Draft    │   │ Human QA │   │ Per-plat │   │ Schedule │
│ Research │   │ AI-assist│   │ Edit     │   │ Assets   │   │ Distribute│
│ Calendar │   │ Media    │   │ Approve  │   │ SEO      │   │ Track    │
└──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
       │              │              │              │              │
       ▼              ▼              ▼              ▼              ▼
   Ideas DB      Drafts DB     Approved DB    Assets DB    Published DB
```

**Stage tracking:**

| Stage | Status Values | Trigger to Next |
|-------|--------------|-----------------|
| Ideation | idea → researched → scheduled | Added to content calendar |
| Creation | draft_started → draft_complete | Author marks complete |
| Review | in_review → changes_requested → approved | Reviewer approves |
| Formatting | formatting → assets_ready | All platform variants generated |
| Publishing | scheduled → published → distributed | Publish date reached |

### Step 3: AI Integration Points

Identify where AI accelerates the pipeline:

| Stage | AI Task | Input | Output | Human Check? |
|-------|---------|-------|--------|-------------|
| Ideation | Topic generation | Niche + trending keywords | 10 topic ideas with angles | Yes — pick top 3 |
| Ideation | Title optimization | Working title | 5 title variants with hooks | Yes — choose one |
| Creation | First draft | Outline + key points | Blog post draft | Yes — heavy edit |
| Creation | YouTube script | Topic + talking points | Scripted sections | Yes — personalize |
| Formatting | SEO meta | Full article | Meta title, description, keywords | Light review |
| Formatting | Social posts | Article content | Twitter thread, LinkedIn post, IG caption | Yes — tone check |
| Formatting | Email subject | Newsletter content | 5 subject line variants | Yes — pick one |
| Publishing | Alt text | Images | Descriptive alt text | Light review |

**AI prompt templates for each task:**

```
── TOPIC GENERATION ───────────────────────
Input: "Generate 10 content ideas for [niche]. Target audience: [audience].
       Current trends: [trends]. Avoid topics we've covered: [recent topics].
       Format: Title | Angle | Target keyword | Estimated interest (1-10)"

── TITLE OPTIMIZATION ─────────────────────
Input: "Generate 5 title variants for: [working title].
       Optimize for: click-through, SEO keyword [keyword], accuracy.
       Style: [informational / provocative / how-to / listicle]"

── SOCIAL REPURPOSING ─────────────────────
Input: "Repurpose this article into platform-specific posts:
       Article: [full text]
       Platforms: Twitter (thread, 280 chars/tweet), LinkedIn (professional tone),
       Instagram (casual, emoji-friendly, hashtags)"
```

### Step 4: Multi-Platform Formatting

Define format specifications per platform:

| Platform | Format | Length | Media | Unique Requirements |
|----------|--------|--------|-------|-------------------|
| **Blog** | HTML/Markdown | 1500-3000 words | Header image, inline images | SEO meta, schema markup, internal links |
| **YouTube** | Video | 8-15 min | Thumbnail 1280x720 | Title (60 chars), description (5000 chars), tags, chapters |
| **Twitter/X** | Thread | 3-10 tweets, 280 chars each | 1 image per tweet optional | Hook tweet, numbered, CTA in last tweet |
| **LinkedIn** | Post | 1300 chars (pre-fold: 210) | 1 image or document carousel | Professional tone, line breaks, no hashtag spam |
| **Instagram** | Carousel or Reel | Caption: 2200 chars | 1080x1080 images or 9:16 video | 20-30 hashtags, alt text, call to action |
| **Newsletter** | Email | 500-1000 words | Inline images | Subject line, preview text, unsubscribe link, CTA button |

**Content atomization** — from one source, generate:

```
Blog Post (source of truth)
  ├── YouTube video script (expand key points, add examples)
  ├── Twitter thread (extract key insights, 1 per tweet)
  ├── LinkedIn post (professional summary + personal take)
  ├── Instagram carousel (visual key points, 5-7 slides)
  ├── Newsletter (summary + personal commentary + CTA)
  └── Pinterest pin (infographic of key stats/steps)
```

### Step 5: Content Calendar & Scheduling

Design the publishing schedule:

```
── WEEKLY CONTENT CALENDAR ────────────────

Monday:    Blog post published (written prev week)
Tuesday:   Twitter thread (repurposed from blog)
Wednesday: YouTube video live (filmed prev week)
Thursday:  LinkedIn post (professional angle on blog topic)
Friday:    Newsletter sent (weekly roundup + personal note)
Saturday:  Instagram carousel (visual summary of week's content)
Sunday:    Ideation session for next week
```

**Automated scheduling:**
- **Buffer/Hootsuite/Typefully**: Schedule social posts
- **n8n workflow**: Trigger format conversion and scheduling
- **CMS scheduled publish**: Blog posts via WordPress/Ghost/Notion API
- **Email platform**: ConvertKit/Mailchimp scheduled sends

**Calendar management:**
```
Content Calendar Table:
  id | topic | status | blog_date | youtube_date | social_date | newsletter_date | notes
```

### Step 6: Quality Gates

Define human review checkpoints:

```
── QUALITY GATES ──────────────────────────

Gate 1: CONTENT APPROVAL
  When: After AI draft is complete
  Who: Content creator / editor
  Checks:
    □ Factually accurate
    □ Brand voice consistent
    □ No AI artifacts (robotic phrasing, hallucinated facts)
    □ Clear structure and flow
    □ CTA present and relevant
  Action: Approve → auto-format for all platforms
          Reject → return to creation with notes

Gate 2: VISUAL REVIEW
  When: After platform formatting + asset generation
  Who: Content creator / designer
  Checks:
    □ Images appropriate and licensed
    □ Thumbnail compelling
    □ Social posts read well standalone
    □ Links working
  Action: Approve → schedule for publish
          Reject → return to formatting

Gate 3: POST-PUBLISH CHECK
  When: 1 hour after publishing
  Who: Automated + content creator
  Checks:
    □ All links resolve (automated)
    □ Images loading (automated)
    □ No broken formatting (manual spot check)
    □ Comments/responses monitored
  Action: Fix issues if found
```

**Automation-friendly gates:**
- Use a Notion/Airtable status column that the pipeline checks
- n8n workflow waits for status change from "in_review" to "approved"
- Slack notification when content is ready for review with one-click approve

### Step 7: Analytics & Feedback Loop

Track performance to improve future content:

**Per-piece metrics:**

| Platform | Metric | Source | Track |
|----------|--------|--------|-------|
| Blog | Page views, time on page, bounce rate | Google Analytics | Daily for 7 days |
| YouTube | Views, watch time, CTR, retention | YouTube Studio | Daily for 14 days |
| Twitter/X | Impressions, engagements, link clicks | Twitter Analytics | 48 hours |
| LinkedIn | Impressions, reactions, comments | LinkedIn Analytics | 48 hours |
| Instagram | Reach, saves, shares | Instagram Insights | 48 hours |
| Newsletter | Open rate, click rate, unsubscribes | Email platform | 72 hours |

**Feedback into ideation:**
- Top-performing topics → create more in same category
- High-engagement formats → prioritize that format
- Low performers → analyze why (topic, timing, headline, format?)
- Comment themes → new content ideas from audience questions

**Content scorecard:**
```
Content: "[Title]"
Published: [date]
Score: [1-10 composite]
  Blog:       [X] views, [X]% bounce
  YouTube:    [X] views, [X]% retention
  Social:     [X] impressions, [X]% engagement
  Newsletter: [X]% open, [X]% click
Verdict: [Scale / Iterate / Retire]
```

### Step 8: Tooling & Integration Map

**Core tools:**

| Function | Tool | Integration Method |
|----------|------|-------------------|
| Workflow orchestration | n8n | Self-hosted or cloud |
| Content drafting | Claude API / GPT API | API call from n8n |
| Blog publishing | WordPress / Ghost / Notion | REST API |
| Video production | Remotion / Descript | CLI or API |
| Email newsletter | SendGrid / ConvertKit | API |
| Social scheduling | Buffer API / Twitter API / LinkedIn API | OAuth + API |
| Asset storage | Cloudinary / S3 | Upload API |
| Analytics | Google Analytics / platform native | Reporting API |
| Content calendar | Notion / Airtable | API |

**n8n workflow design:**

```
Workflow 1: DAILY CONTENT CHECK
  Schedule Trigger (9 AM) → Check calendar for today's content
  → IF content ready → Format for platform → Schedule/publish
  → ELSE → Send "nothing scheduled" alert

Workflow 2: CONTENT REPURPOSING
  Webhook (blog published) → Fetch full article
  → AI: Generate Twitter thread → Schedule via Buffer
  → AI: Generate LinkedIn post → Schedule via Buffer
  → AI: Generate newsletter section → Queue for weekly send
  → AI: Generate Instagram caption → Send to Slack for manual post

Workflow 3: WEEKLY ANALYTICS
  Schedule Trigger (Monday 8 AM) → Pull analytics from all platforms
  → Compile scorecard per piece → Store in Notion/Airtable
  → Generate weekly report → Send to Slack/email
```

### Step 9: Output

Present the complete pipeline specification:

```
━━━ CONTENT PIPELINE: [Name] ━━━━━━━━━━━━━

── PIPELINE STAGES ────────────────────────
[5-stage flow diagram]

── AI INTEGRATION ─────────────────────────
[AI tasks per stage with prompt templates]

── PLATFORM FORMATS ───────────────────────
[format specs per platform]

── CONTENT CALENDAR ───────────────────────
[weekly schedule template]

── QUALITY GATES ──────────────────────────
[3 checkpoints with checklists]

── ANALYTICS ──────────────────────────────
[per-piece metrics + scorecard template]

── TOOL MAP ───────────────────────────────
[tools + integration methods]

── N8N WORKFLOWS ──────────────────────────
[workflow designs for automation]
```

## Inputs
- Content type and format
- Source material type
- Target platforms
- Posting schedule
- Team / review process
- Existing tools

## Outputs
- 5-stage pipeline design (ideation → creation → review → format → publish)
- AI integration points with prompt templates
- Multi-platform format specifications
- Content calendar with scheduling automation
- Quality gates with review checklists
- Analytics tracking with content scorecard
- Tool and integration map
- n8n workflow designs for orchestration

## Level History

- **Lv.1** — Base: 5-stage content pipeline, AI integration at 8 touch points with prompt templates, multi-platform format specs (blog, YouTube, Twitter, LinkedIn, Instagram, newsletter), content calendar with atomization strategy, 3-tier quality gates, analytics feedback loop with content scorecard, n8n workflow designs for daily publishing and weekly analytics. (Origin: MemStack v3.2, Mar 2026)
