---
name: memstack-content-blog-post
description: "Use this skill when the user says 'write blog post', 'blog post about', 'write article', 'create blog', 'content for blog', 'write post', or is creating long-form written content for a blog or publication. Do NOT use for landing page copy, email sequences, or social media posts."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# ✍️ Blog Post — Writing SEO-optimized blog post...
*Produces a complete, publish-ready blog post with SEO metadata, structured sections, readability optimization, and internal linking suggestions.*

## Activation

When this skill activates, output:

`✍️ Blog Post — Gathering topic and audience details...`

Then execute the protocol below.

| Context | Status |
|---------|--------|
| User says "write blog post" or "blog post about" | ACTIVE |
| User says "write article" or "create blog" or "write post" | ACTIVE |
| Creating long-form content for a website or publication | ACTIVE |
| Writing landing page copy (short-form, conversion-focused) | DORMANT — use landing-page-copy |
| Writing email content | DORMANT — use email-sequence |
| Writing social media posts | DORMANT |

### Anti-patterns

| Trap | Reality Check |
|------|---------------|
| "Write about everything related to the topic" | Focus on one angle. Broad posts rank for nothing. Narrow posts rank for one keyword. |
| "The intro should provide context" | The intro should hook. Context bores. Open with a bold claim, stat, or question. |
| "Longer is better for SEO" | Comprehensive beats long. 1,500 focused words outrank 3,000 padded words. |
| "Stuff the keyword everywhere" | Use the keyword naturally 3-5 times. Search engines penalize stuffing. Readers hate it. |
| "Anyone who finds it will read it" | You have 3 seconds. If the title and intro don't hook them, the rest doesn't matter. |

## Protocol

### Step 1: Gather Topic Details

If the user hasn't provided details, ask:

> I need a few details for the blog post:
> 1. **Topic** — what's this post about?
> 2. **Target audience** — who are you writing for? (developers, business owners, beginners, etc.)
> 3. **Target keyword** — what search term should this rank for?
> 4. **Tone** — casual/conversational, professional, technical, inspirational?
> 5. **Desired length** — short (800 words), standard (1,200-1,500), long-form (2,000+)?

If the user provides partial info, infer what you can and ask only for what's missing.

### Step 2: Research and Outline

Before writing, build a structured outline:

1. **Identify 3-5 key points** the post must cover
2. **Find supporting data** — statistics, examples, or case studies that strengthen each point
3. **Note counterarguments** — addressing objections builds credibility
4. **Determine the unique angle** — what perspective makes this post different from the top 10 results?

**Outline template:**

```markdown
## Outline

**Angle:** [What makes this post different]
**Target keyword:** [primary keyword]
**Secondary keywords:** [2-3 related terms]

1. Hook intro — [opening strategy: bold claim / stat / question / story]
2. [Section H2] — [key point + supporting evidence]
3. [Section H2] — [key point + supporting evidence]
4. [Section H2] — [key point + supporting evidence]
5. [Section H2] — [key point + counterargument addressed]
6. Actionable takeaways — [summary of what to do next]
7. CTA conclusion — [what you want the reader to do]
```

Present the outline for user approval before writing the full post.

### Step 3: Write SEO Metadata

```markdown
**Title:** [60 characters max — include target keyword, power word, specific benefit]
**Meta description:** [155 characters max — summarize the value, include keyword, end with implicit CTA]
**URL slug:** [target-keyword-in-slug — lowercase, hyphens, no filler words]
```

**Title formula options:**
- Number + Adjective + Keyword + Promise: "7 Proven Ways to [Keyword] Without [Pain Point]"
- How to + Keyword + Benefit: "How to [Keyword]: A Step-by-Step Guide for [Audience]"
- Question format: "Why Does [Keyword] Matter? [Provocative Answer]"
- Contrarian: "[Common Belief] Is Wrong. Here's What [Keyword] Actually Means"

**Title rules:**
- Include target keyword within the first 40 characters
- Use a power word (proven, essential, complete, ultimate, simple)
- Promise a specific outcome (not vague "improve")
- Max 60 characters to avoid Google truncation

**Meta description rules:**
- Include target keyword naturally
- Summarize the unique value of this post
- Create curiosity or promise a benefit
- Max 155 characters to avoid truncation

### Step 4: Write the Post

#### Intro (100-150 words)

The intro must accomplish three things in three paragraphs (or fewer):

1. **Hook** — bold claim, surprising stat, relatable pain point, or provocative question
2. **Relevance** — why this matters to the reader right now
3. **Promise** — what they'll know or be able to do after reading

```markdown
[Hook sentence — bold claim or surprising stat]

[1-2 sentences connecting to reader's situation]

[Promise: "In this post, you'll learn..." or "Here's exactly how to..."]
```

**Do NOT:**
- Start with "In today's fast-paced world..." or any throat-clearing
- Define the obvious ("What is marketing?")
- Summarize the entire post upfront (that's what the outline is for)

#### Body Sections (3-5 H2 sections)

Each section follows this structure:

```markdown
## [H2: Keyword-rich, benefit-oriented heading]

[Opening sentence that states the section's key point]

[Supporting evidence: stat, example, case study, or expert quote]

[Practical explanation — how this applies to the reader]

[Specific example or actionable step]

> [Optional: pull quote or callout box with key insight]

[Transition sentence leading to the next section]
```

**Body writing rules:**
- Paragraphs: max 3-4 sentences each (walls of text kill readability)
- Sentences: vary length — mix short punchy sentences with longer explanatory ones
- Use H3 subheadings to break up sections longer than 300 words
- Include the target keyword in at least 2 H2 headings (naturally, not forced)
- Use bullet points or numbered lists for any set of 3+ items
- Bold key phrases for scanners (most readers scan before deciding to read)

#### Readability Targets

| Metric | Target | Why |
|--------|--------|-----|
| Flesch-Kincaid Grade | 8 or below | Accessible to 80% of readers |
| Sentence length | Average 15-20 words | Longer sentences lose readers |
| Paragraph length | Max 3-4 sentences | Short paragraphs feel faster |
| Passive voice | Below 10% | Active voice is direct and clear |
| Adverb usage | Minimal | "Ran quickly" loses to "sprinted" |
| Jargon | Define or avoid | Unless audience is technical |

### Step 5: Write Conclusion and CTA

```markdown
## [Takeaway heading — not "Conclusion"]

[Summarize the 3 most important points in 2-3 sentences]

[Restate the benefit: what the reader can now do]

**[CTA — what you want them to do next:]**
- Subscribe/newsletter: "Get [topic] tips weekly — subscribe below"
- Product: "Try [product] free — [link]"
- Share: "Found this useful? Share it with your team"
- Next post: "Read next: [related post title]"
- Comment: "What's your experience with [topic]? Drop a comment"
```

### Step 6: Add Internal Linking Suggestions

```markdown
## Internal Linking Opportunities

| Anchor Text | Link To | Location in Post |
|-------------|---------|-----------------|
| "[related concept]" | /blog/[related-post-slug] | Section 2, paragraph 3 |
| "[tool or feature mentioned]" | /features/[feature-page] | Section 4, paragraph 1 |
| "[previous post reference]" | /blog/[previous-post-slug] | Conclusion |

**External links (for credibility):**
| Anchor Text | Link To | Rationale |
|-------------|---------|-----------|
| "[stat source]" | [authoritative source URL] | Backs up claim in Section 1 |
| "[expert quote source]" | [source URL] | Attribution |
```

**Linking rules:**
- 2-4 internal links per 1,000 words (to existing site content)
- 1-2 external links to authoritative sources (studies, reports, official docs)
- Anchor text should be descriptive, not "click here"
- Open external links in new tab

### Step 7: Add Image Suggestions

```markdown
## Image Placements

| Position | Image Concept | Alt Text | Purpose |
|----------|--------------|----------|---------|
| After intro | [Relevant hero image or infographic] | "[Descriptive alt text with keyword]" | Visual hook |
| Section 2 | [Screenshot, diagram, or example] | "[Descriptive alt text]" | Illustrate concept |
| Section 4 | [Chart, comparison, or data visualization] | "[Descriptive alt text]" | Support data point |
| Before CTA | [Product shot or action image] | "[Descriptive alt text]" | Reinforce CTA |
```

**Image rules:**
- Alt text is descriptive (for accessibility), not keyword-stuffed
- Include target keyword in hero image alt text (once, naturally)
- Suggest image type (photo, screenshot, infographic, chart) not specific images
- One image per 300-500 words keeps readers engaged

### Step 8: Assemble and Output

Output the complete blog post in clean markdown:

```markdown
---
title: "[SEO title]"
description: "[Meta description]"
date: YYYY-MM-DD
author: "[Author]"
tags: ["keyword1", "keyword2", "keyword3"]
image: "/blog/[slug]/hero.jpg"
---

# [Post Title]

[Full post content with H2 sections, formatting, links]
```

**Output summary:**

```
✍️ Blog Post — Complete

Title: [title] ([character count] chars)
Meta description: [description] ([character count] chars)
Target keyword: [keyword]
Word count: [count]
Sections: [count] H2s, [count] H3s
Reading time: ~[count] minutes
Readability: Flesch-Kincaid Grade [score]

SEO checklist:
  ✅ Keyword in title (first 40 chars)
  ✅ Keyword in meta description
  ✅ Keyword in 2+ H2 headings
  ✅ Keyword in first 100 words
  ✅ Internal links: [count]
  ✅ External links: [count]
  ✅ Image alt text with keyword: [count]

Next steps:
1. Review and add personal voice/anecdotes
2. Source or create images for suggested placements
3. Add internal links to existing content
4. Publish and submit to Google Search Console
```

## Level History

- **Lv.1** — Base: Topic gathering, research/outline, SEO metadata (title 60 chars, meta 155 chars), structured sections with H2s, readability targets (Flesch-Kincaid grade 8), internal/external linking, image suggestions with alt text, publish-ready markdown output. (Origin: MemStack Pro v3.2, Mar 2026)
