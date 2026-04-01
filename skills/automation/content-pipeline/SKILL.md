---
name: memstack-automation-content-pipeline
description: "Use this skill when the user says 'content pipeline', 'content automation', 'auto-publish', 'repurpose content', 'multi-platform publishing', or needs end-to-end content workflow from ideation through cross-platform formatting and publishing. Do NOT use for single social media posts or individual blog posts."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# Content Pipeline — Automating content workflow...
*Automates end-to-end content workflows from ideation through draft, review, approval, cross-platform formatting, scheduling, and publishing with CMS integration and image optimization.*

## Activation

When this skill activates, output:

`Content Pipeline — Automating content workflow...`

Then execute the protocol below.

## Context Guard

| Context | Status |
|---------|--------|
| User says "content pipeline", "content automation", "auto-publish" | ACTIVE |
| User says "repurpose content" or "multi-platform publishing" | ACTIVE |
| User wants to automate content creation through distribution | ACTIVE |
| User wants a single blog post | DORMANT — use Blog Post |
| User wants a single social media post | DORMANT — use Twitter Thread or TikTok Script |

## Common Mistakes

| Mistake | Why It's Wrong |
|---------|---------------|
| "Same content on every platform" | Each platform has its own format, tone, and audience expectations. Repurpose, don't copy-paste. |
| "Automate quality away" | Automation handles formatting and scheduling, not editorial judgment. Keep human review in the loop. |
| "No content calendar" | Publishing without a schedule leads to feast-or-famine posting. Consistency beats volume. |
| "Skip image optimization" | Unoptimized images slow page load and fail platform size requirements. Automate resizing. |
| "Publish and forget" | Monitor engagement within 24-48 hours. Boost winners, learn from underperformers. |

## Protocol

### Step 1: Gather Pipeline Requirements

If the user hasn't provided details, ask:

> 1. **Content types** — what do you produce? (blog, newsletter, social, video, podcast)
> 2. **Platforms** — where do you publish? (website, Twitter/X, LinkedIn, Instagram, YouTube, email)
> 3. **Frequency** — how often? (daily, 3x/week, weekly)
> 4. **Team** — who's involved? (writer, editor, designer, social manager)
> 5. **CMS** — what do you use? (WordPress, Ghost, Notion, Webflow, headless CMS)
> 6. **Current process** — what's manual today that should be automated?

### Step 2: Design Pipeline Stages

```
[Ideation] → [Draft] → [Review] → [Approve] → [Format] → [Schedule] → [Publish] → [Monitor]
```

**Stage definitions:**

| Stage | Owner | Input | Output | Automation Level |
|-------|-------|-------|--------|-----------------|
| **Ideation** | Content lead | Keyword research, trending topics, audience questions | Content brief | Semi-auto (AI-assisted topic generation) |
| **Draft** | Writer | Content brief | Raw draft (Markdown/Docs) | Manual (AI-assisted) |
| **Review** | Editor | Raw draft | Edited draft with feedback | Manual |
| **Approve** | Content lead | Edited draft | Approved for publishing | Manual (checklist-gated) |
| **Format** | Pipeline | Approved content | Platform-specific versions | Fully automated |
| **Schedule** | Pipeline | Formatted content | Queued posts with dates/times | Fully automated |
| **Publish** | Pipeline | Scheduled posts | Live content across platforms | Fully automated |
| **Monitor** | Marketing | Published content | Engagement metrics | Semi-auto (dashboard) |

### Step 3: Content Repurposing Matrix

Define how one piece of content becomes many:

| Source | → Blog Post | → Twitter Thread | → LinkedIn | → Newsletter | → Instagram |
|--------|-----------|-----------------|-----------|-------------|------------|
| **Blog post** | Original | Key points (5-10 tweets) | Summary + insights | Featured article | Quote card + carousel |
| **Video** | Transcript → post | Key quotes | Behind-the-scenes | Recap + link | Clips (15-60s) |
| **Podcast** | Show notes | Soundbite quotes | Episode summary | Weekly roundup | Audiogram |
| **Newsletter** | Expanded article | Thread from section | Cross-post | Original | Highlight card |

**Repurposing rules:**
- Each platform version should feel native (not like a cross-post)
- Adjust tone: Twitter (punchy, direct), LinkedIn (professional, storytelling), Instagram (visual, emotional)
- Adjust length: Twitter (280 chars/tweet), LinkedIn (1300 chars optimal), Instagram (2200 chars max)
- Add platform-specific elements: hashtags (Instagram), mentions (Twitter), links (LinkedIn)

### Step 4: Image Optimization Pipeline

**Platform image specs:**

| Platform | Size | Aspect Ratio | Max File Size | Format |
|----------|------|-------------|--------------|--------|
| Blog (hero) | 1200×630 | 1.91:1 | 200KB | WebP (JPEG fallback) |
| Twitter | 1200×675 | 16:9 | 5MB | PNG/JPEG |
| LinkedIn | 1200×627 | 1.91:1 | 5MB | PNG/JPEG |
| Instagram (feed) | 1080×1080 | 1:1 | 8MB | JPEG |
| Instagram (story) | 1080×1920 | 9:16 | 8MB | JPEG |
| Newsletter | 600×300 | 2:1 | 100KB | PNG/JPEG |
| Open Graph | 1200×630 | 1.91:1 | 200KB | PNG/JPEG |

**Automated image processing:**

```bash
# Using sharp (Node.js) or ImageMagick
# From one source image, generate all platform variants:

sharp(sourceImage)
  .resize(1200, 630, { fit: 'cover' })
  .webp({ quality: 80 })
  .toFile('blog-hero.webp');

sharp(sourceImage)
  .resize(1080, 1080, { fit: 'cover' })
  .jpeg({ quality: 85 })
  .toFile('instagram-square.jpg');

sharp(sourceImage)
  .resize(1080, 1920, { fit: 'cover' })
  .jpeg({ quality: 85 })
  .toFile('instagram-story.jpg');
```

### Step 5: Scheduling Strategy

**Optimal posting times (general — adjust to your analytics):**

| Platform | Best Days | Best Times (ET) | Frequency |
|----------|----------|----------------|-----------|
| Blog | Tue-Thu | 10 AM | 1-3x/week |
| Twitter/X | Mon-Fri | 8 AM, 12 PM, 5 PM | 1-3x/day |
| LinkedIn | Tue-Thu | 7-8 AM, 12 PM | 3-5x/week |
| Instagram | Mon, Wed, Fri | 11 AM, 1 PM | 3-5x/week |
| Newsletter | Tue or Thu | 9-10 AM | 1x/week |
| YouTube | Thu-Sat | 2-4 PM | 1-2x/week |

**Content calendar template:**

```markdown
## Week of [Date]

| Day | Blog | Twitter | LinkedIn | Newsletter | Instagram |
|-----|------|---------|----------|-----------|-----------|
| Mon | — | [Thread from Friday's blog] | — | — | [Quote card] |
| Tue | [New post: Topic] | [3 promo tweets] | [Post: summary] | [Weekly send] | — |
| Wed | — | [Engagement thread] | — | — | [Carousel] |
| Thu | — | [Tips thread] | [Article share] | — | [Behind-scenes] |
| Fri | [New post: Topic] | [3 promo tweets] | [Post: summary] | — | [Quote card] |
```

### Step 6: CMS Integration Patterns

**Headless CMS workflow (API-based):**

```typescript
// Publish to CMS via API
async function publishToCMS(content: {
  title: string;
  body: string;
  slug: string;
  featuredImage: string;
  tags: string[];
  publishAt?: Date;
}): Promise<string> {
  const response = await cmsClient.post('/posts', {
    title: content.title,
    content: content.body,
    slug: content.slug,
    featured_image: content.featuredImage,
    tags: content.tags,
    status: content.publishAt ? 'scheduled' : 'published',
    published_at: content.publishAt?.toISOString(),
  });
  return response.data.url;
}
```

**Social media scheduling (via Buffer/Hootsuite API or native):**

```typescript
async function scheduleToSocial(posts: SocialPost[]): Promise<void> {
  for (const post of posts) {
    await bufferClient.post('/updates/create', {
      profile_ids: [post.profileId],
      text: post.content,
      media: post.imageUrl ? { photo: post.imageUrl } : undefined,
      scheduled_at: post.scheduledAt.toISOString(),
    });
  }
}
```

### Step 7: Monitoring & Optimization

**Engagement tracking (24-48 hours post-publish):**

| Metric | Blog | Twitter | LinkedIn | Newsletter |
|--------|------|---------|----------|-----------|
| Views/Impressions | Page views | Impressions | Impressions | Opens |
| Engagement | Time on page | Likes + replies | Reactions + comments | Click rate |
| Conversion | CTA clicks | Link clicks | Link clicks | Reply rate |
| Share/Viral | Social shares | Retweets | Reposts | Forwards |

**Content scoring formula:**

```
Score = (Engagement Rate × 40%) + (Conversion Rate × 40%) + (Shares × 20%)
```

- **A-tier (top 20%):** Repurpose aggressively, boost with ads, create sequel content
- **B-tier (middle 60%):** Standard distribution, note what worked
- **C-tier (bottom 20%):** Analyze why it underperformed, adjust future topics

## Output Format

```markdown
# Content Pipeline — [Brand/Product Name]

## Pipeline Stages
[Stage diagram and definitions from Step 2]

## Repurposing Matrix
[From Step 3 — source → platform transformations]

## Image Specs
[Platform-specific sizes from Step 4]

## Content Calendar
[Weekly template from Step 5]

## CMS & Social Integration
[API patterns from Step 6]

## Monitoring Dashboard
[Metrics and scoring from Step 7]
```

## Completion

```
Content Pipeline — Complete!

Platforms: [Count] ([list])
Content types: [Count]
Pipeline stages: 8 (ideation → monitor)
Publishing frequency: [X pieces/week across platforms]
Automation level: [X/8 stages automated]

Next steps:
1. Set up CMS API access and social scheduling tool
2. Create image templates for each platform
3. Build the first week's content calendar
4. Automate the Format → Schedule → Publish stages
5. Review engagement data weekly and adjust
```

## Level History

- **Lv.1** — Base: 8-stage pipeline (ideation through monitoring), content repurposing matrix (blog/video/podcast → 5 platforms), platform image specs with automated processing, optimal posting times, content calendar template, CMS integration patterns (headless API, social scheduling), engagement monitoring with content scoring formula. (Origin: MemStack Pro v3.2, Mar 2026)
