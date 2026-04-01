---
name: memstack-content-youtube-script
description: "Use this skill when the user says 'YouTube script', 'video script', 'write script for YouTube', 'YouTube video outline', or is creating scripted content for a YouTube video with hooks, chapters, and CTAs. Do NOT use for TikTok/Reels short-form scripts or webinar presentations."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# 🎬 YouTube Script — Writing retention-optimized video script...
*Produces a timestamped video script with hook, retention techniques, visual directions, SEO metadata, and thumbnail concept — optimized for YouTube's algorithm.*

## Activation

When this skill activates, output:

`🎬 YouTube Script — Gathering topic and audience details...`

Then execute the protocol below.

| Context | Status |
|---------|--------|
| User says "write youtube script" or "youtube script" | ACTIVE |
| User says "video script" or "write script for video" | ACTIVE |
| Creating a scripted video for YouTube or video platform | ACTIVE |
| Writing a blog post (not video) | DORMANT — use blog-post |
| Writing a podcast outline | DORMANT |
| Discussing YouTube strategy at a high level | DORMANT |

### Anti-patterns

| Trap | Reality Check |
|------|---------------|
| "Start with an intro about who I am" | Viewers don't care who you are until you've hooked them. Identity comes after value. |
| "Cover everything about the topic" | YouTube rewards depth on one angle, not breadth across many. Pick one promise and deliver it fully. |
| "The content speaks for itself" | Retention techniques (open loops, pattern breaks) keep viewers watching. Great content with poor pacing loses to good content with great pacing. |
| "I'll figure out the visuals during editing" | Script the visuals alongside the words. B-roll and graphics are planned, not improvised. |
| "Thumbnails are just screenshots" | The thumbnail is 50% of click-through rate. Design it before filming — it shapes the video's angle. |

## Protocol

### Step 1: Gather Video Details

If the user hasn't provided details, ask:

> I need a few details for the script:
> 1. **Topic** — what's this video about?
> 2. **Target viewer** — who is watching? (beginner dev, business owner, tech enthusiast, etc.)
> 3. **Video length goal** — short (5-8 min), standard (10-15 min), long-form (20+ min)?
> 4. **CTA goal** — what should viewers do? (subscribe, click a link, watch next video, buy)
> 5. **Channel context** — is this part of a series? What's the channel about?
> 6. **Presentation style** — talking head, screencast, voiceover with visuals, mixed?

### Step 2: Write the Hook (First 30 Seconds)

The hook determines whether viewers watch or leave. Structure it as three beats:

```markdown
## HOOK [0:00 - 0:30]

### Beat 1: Pattern Interrupt [0:00 - 0:05]
**[VISUAL: [Eye-catching opening shot / bold text on screen / unexpected image]]**

[Speaker:]
"[Bold opening — a surprising stat, contrarian claim, or provocative question]"

Examples:
- Stat: "90% of startups fail because of one mistake. And you're probably making it right now."
- Contrarian: "Everything you've been taught about [topic] is wrong."
- Question: "What if I told you that [common approach] is actually hurting your [outcome]?"
- Demo: "Watch this." [Show the end result before explaining how]

### Beat 2: Promise [0:05 - 0:15]
[Speaker:]
"In this video, I'm going to show you [specific outcome].
By the end, you'll know exactly how to [tangible result]."

### Beat 3: Credibility [0:15 - 0:30]
[Speaker:]
"[Brief credibility: I've [done X] / helped [N] people / spent [time] researching this]
— and I'm going to break down [the framework / the exact steps / what actually works]."

**[VISUAL: Quick montage of proof — screenshots, results, credentials]]**
```

**Hook rules:**
- Pattern interrupt first — break expectations within 5 seconds
- Promise must be specific — "how to grow your channel" is vague; "how to get your first 1,000 subscribers in 30 days" is specific
- Credibility is 1-2 sentences max — prove you're worth listening to, then move on
- Never start with "Hey guys, welcome back to my channel" — earn the intro first
- Total hook: under 30 seconds

### Step 3: Structure with Retention Techniques

Build the body using techniques that maintain watch time:

#### Open Loops

Plant unanswered questions that pay off later:

```markdown
[Speaker:]
"Now, there are three strategies that work — but the third one is the one that
changed everything for me. I'll get to that in a minute. First, let's talk about..."
```

**Open loop placement:**
- Drop an open loop at the end of the hook (tease something coming later)
- Plant 1-2 mid-video loops before major sections
- Always close loops before the video ends — broken promises kill trust

#### Pattern Breaks

Change the visual or audio rhythm every 60-90 seconds to reset attention:

| Break Type | When to Use | Example |
|-----------|------------|---------|
| B-roll cut | Every 30-60 seconds of talking head | Show the thing being discussed |
| On-screen text | Key stats, definitions, lists | Bold text highlighting the main point |
| Camera angle change | Every 2-3 minutes | Switch between close-up and medium shot |
| Music shift | Section transitions | Background music changes mood |
| Direct address | When making a key point | Look directly at camera, pause, then speak |
| Screen recording | Tutorial/demo sections | Switch from talking head to screen |

#### Visual Cues

Script what appears on screen alongside dialogue:

```markdown
[Speaker:] "There are three types of content that perform on YouTube."

**[ON SCREEN: "3 Content Types" in bold text]**

[Speaker:] "Number one: tutorials."

**[ON SCREEN: "1. Tutorials" with icon]**
**[B-ROLL: Quick clips of tutorial-style content]**
```

### Step 4: Write Body Sections

Each section follows a retention-optimized structure:

```markdown
## SECTION 1: [Topic] [1:00 - 4:00]

### Transition In
[Speaker:]
"[Bridge from previous section — use a question or callback]
So now that you understand [previous concept], let's talk about [this section]."

**[VISUAL: Section title card or transition graphic]**

### Content
[Speaker:]
"[Key point — state it directly in one sentence]

[Explanation — break down why this matters, 2-3 sentences]

[Example — specific, concrete illustration]

**[ON SCREEN: [Visual that supports the example — screenshot, diagram, code]]**

[Actionable step — what the viewer should do with this information]"

### Open Loop / Transition Out
[Speaker:]
"[Tease next section or callback to open loop]
But here's where it gets interesting — in the next section,
I'll show you [what makes this 10x more effective]."

**[VISUAL: Quick preview of next section's visual]**
```

**Body section writing rules:**
- State the key point first, then explain — don't build up to it
- One idea per section — don't combine multiple concepts
- Include a specific example for every abstract concept
- Script visual cues inline — don't leave visuals to post-production guesswork
- End every section with a transition that pulls viewers into the next

**Pacing by video length:**

| Video Length | Sections | Time per Section | Pattern Breaks |
|-------------|----------|-----------------|---------------|
| 5-8 minutes | 3 | 1.5-2 min each | Every 45-60 sec |
| 10-15 minutes | 4-5 | 2-3 min each | Every 60-90 sec |
| 20+ minutes | 6-8 | 2.5-3.5 min each | Every 60-90 sec |

### Step 5: Write Section Transitions

Transitions keep viewers watching through section boundaries (where most drop-off happens):

**Transition formulas:**

| Type | Template | When to Use |
|------|----------|-------------|
| **Question bridge** | "So [recap] — but you might be wondering, [question]?" | After explaining a concept |
| **Contrast bridge** | "That was [method A]. But [method B] takes it further." | Between two related ideas |
| **Stakes bridge** | "If you skip this next part, [negative consequence]." | Before the most important section |
| **Curiosity bridge** | "This next technique is the one most people get wrong." | Before a counterintuitive point |
| **Progress bridge** | "We've covered [X and Y]. Now for the final piece: [Z]." | After the midpoint of the video |

**Transition rules:**
- Never use "Moving on..." or "Next, let's talk about..." — these signal a stopping point
- Every transition should create a reason to keep watching (question, promise, stakes)
- Transitions are 1-2 sentences max — long transitions lose momentum

### Step 6: Write CTA and Outro

```markdown
## CTA + OUTRO [final 30-60 seconds]

### Payoff / Summary
[Speaker:]
"[Close any remaining open loops — deliver what was promised]

So to recap: [3 bullet points summarizing the actionable takeaways]"

**[ON SCREEN: Summary graphic with 3 key points]**

### Call to Action
[Speaker:]
"[Primary CTA — one specific action:]"

- Subscribe: "If this helped you, hit subscribe. I post [frequency] about [topic]."
- Link: "I put together a [resource] — the link is in the description below."
- Next video: "If you want to go deeper on [topic], watch this video next."
  **[ON SCREEN: End screen card pointing to next video]**

"[Secondary CTA — lower commitment:]"
- "Drop a comment below: what's your biggest challenge with [topic]?"
- "Like this video if you learned something — it helps more people find it."

### Outro
[Speaker:]
"Thanks for watching. See you in the next one."

**[VISUAL: End screen with subscribe button and recommended video, 15-20 seconds]**
```

**CTA rules:**
- One primary CTA — don't ask for subscribe AND like AND comment AND click the link
- Place CTA after delivering value, not before (reciprocity)
- The "next video" CTA feeds YouTube's session watch time metric — use it
- End screens must be planned in the script — they require 20 seconds of screen time

### Step 7: Write SEO Metadata

```markdown
## SEO Metadata

### Title (60 characters max)
[Primary keyword + promise + hook element]

Title formulas:
- "How to [Outcome] in [Timeframe] ([Year])"
- "[Number] [Topic] Mistakes You're Making Right Now"
- "I Tried [Thing] for [Duration] — Here's What Happened"
- "[Topic] Explained in [Time] Minutes"

### Description (first 2 lines visible without expand)
Line 1: [Restate the video promise — what they'll learn]
Line 2: [CTA — link to resource, timestamps below]

[Line break]

Timestamps:
0:00 — Intro
0:30 — [Section 1 title]
[X:XX] — [Section 2 title]
[X:XX] — [Section 3 title]
[X:XX] — [Final section / CTA]

[Line break]

[Links to resources mentioned in the video]
[Social media links]
[Related videos]

### Tags (10-15)
[Primary keyword], [variation 1], [variation 2], [related topic 1],
[related topic 2], [channel name], [series name if applicable]
```

**SEO rules:**
- Title: include primary keyword in first 40 characters
- Description: first 2 lines are visible in search — front-load the value
- Timestamps create chapters in YouTube — use them for videos over 5 minutes
- Tags help YouTube understand the topic — use your primary keyword and variations

### Step 8: Thumbnail Concept

```markdown
## Thumbnail Concept

**Layout:** [Describe the visual composition]
**Text:** [3-5 words max on the thumbnail — large, readable at mobile size]
**Emotion:** [What expression/mood — surprise, curiosity, excitement, concern]
**Colors:** [High contrast — avoid YouTube's red/white/black to stand out]

**Thumbnail rules:**
- Must be readable at 120x68 pixels (mobile size)
- Max 3-5 words of text — if you need more, the concept isn't clear enough
- Face with emotion outperforms no-face by 30%+ CTR
- High contrast between background, text, and subject
- Avoid red/white/black (YouTube's brand colors) — use complementary colors
- The thumbnail should tell a different story than the title (complement, don't repeat)

**Example concept:**
[Face showing surprise/curiosity] + [Bold text: "STOP DOING THIS"] + [Relevant object/screenshot]
```

### Step 9: Output Complete Script

```markdown
# YouTube Script: [Video Title]

**Topic:** [topic]
**Target viewer:** [audience]
**Video length:** ~[minutes] minutes
**Style:** [talking head / screencast / mixed]

---

## HOOK [0:00 - 0:30]
[Hook content]

## SECTION 1: [Title] [0:30 - X:XX]
[Section content with visual directions]

## SECTION 2: [Title] [X:XX - X:XX]
[Section content with visual directions]

## SECTION 3: [Title] [X:XX - X:XX]
[Section content with visual directions]

## CTA + OUTRO [X:XX - X:XX]
[CTA and outro content]

---

## SEO Metadata
[Title, description with timestamps, tags]

## Thumbnail Concept
[Visual description]

---
```

**Output summary:**

```
🎬 YouTube Script — Complete

Title: [title] ([character count] chars)
Length: ~[minutes] minutes ([word count] words at 150 wpm)
Sections: [count] + hook + outro
Open loops: [count] planted, [count] closed
Pattern breaks: [count] scripted
B-roll suggestions: [count]

SEO:
  ✅ Title under 60 chars with keyword
  ✅ Description with timestamps
  ✅ Tags: [count]
  ✅ Thumbnail concept defined

Retention techniques used:
  ✅ Pattern interrupt hook (first 5 sec)
  ✅ Open loops across sections
  ✅ Pattern breaks every 60-90 sec
  ✅ Transition bridges between sections
  ✅ End screen CTA with next video

Next steps:
1. Rehearse the hook — nail the first 30 seconds
2. Design the thumbnail before filming
3. Prepare B-roll and screen recordings
4. Film, edit, upload with metadata
5. Publish at peak time for your audience
```

## Level History

- **Lv.1** — Base: Topic gathering, 30-second hook (pattern interrupt / promise / credibility), retention techniques (open loops, pattern breaks, visual cues), section transitions, CTA with end screen, SEO metadata (60 char title, timestamps, tags), thumbnail concept. Based on YouTube Growth Guide N.I.C.E.R. framework. (Origin: MemStack Pro v3.2, Mar 2026)
