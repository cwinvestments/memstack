---
name: humanize
description: "Use when the user says 'humanize', 'clean up writing', 'make it sound natural', or wants text to not sound AI-generated."
---


# ✍️ Humanize — Rewriting for Natural Voice...
*Remove AI tells and rewrite content to sound like a human wrote it.*

## Activation

When this skill activates, output:

`✍️ Humanize — Rewriting for natural voice...`

Then execute the protocol below.

## Context Guard

| Context | Status | Priority |
|---------|--------|----------|
| **User says "humanize", "make it sound human/natural"** | ACTIVE — rewrite content | P1 |
| **User says "clean up this writing", "remove AI tone"** | ACTIVE — rewrite content | P1 |
| **User says "rewrite for blog/social/client"** | ACTIVE — rewrite with audience in mind | P2 |
| **User is writing code or technical docs (API refs, JSDoc)** | DORMANT — technical writing is fine as-is | — |
| **User is writing commit messages or changelogs** | DORMANT — these have their own format | — |

## Protocol

### Step 1: Identify AI Patterns

Scan the content for these common AI writing tells:

**Words to eliminate or replace:**
| AI Pattern | Replace With |
|------------|-------------|
| "delve", "delve into" | "explore", "look at", "dig into" |
| "leverage" | "use", "take advantage of" |
| "utilize" | "use" |
| "facilitate" | "help", "make easier" |
| "comprehensive" | (often removable, or "thorough", "complete") |
| "robust" | "solid", "strong", "reliable" |
| "streamline" | "simplify", "speed up" |
| "moreover", "furthermore" | (cut entirely or use "also", "and") |
| "it's important to note" | (cut — just state the thing) |
| "in conclusion" | (cut — the reader knows it's the end) |
| "in today's [X] landscape" | (cut entirely) |
| "game-changer" | (be specific about the benefit) |
| "navigate" (non-literal) | "deal with", "handle", "work through" |
| "paradigm" | (use a concrete noun instead) |
| "synergy" | "overlap", "combination", "fit" |

**Structural patterns to fix:**
- **Excessive hedging**: "It might be worth considering that perhaps..." → Just say the thing
- **Hollow transitions**: "Now, let's turn our attention to..." → Cut, or use a heading
- **Overlong intros**: "In the ever-evolving world of..." → Start with the point
- **Bullet-point-itis**: Every section as bullets → Mix in short paragraphs
- **Triple emphasis**: "truly remarkable and incredibly powerful" → Pick one adjective
- **Sycophantic openings**: "Great question!" → Don't; just answer
- **Unnecessary qualifiers**: "very", "really", "quite", "rather" → Usually cuttable

### Step 2: Rewrite

Apply these principles:
1. **Lead with the point** — Don't build up to it
2. **Shorter sentences** — If a sentence has a comma and an "and", consider splitting it
3. **Active voice** — "The team built X" not "X was built by the team"
4. **Concrete over abstract** — Specific examples beat general claims
5. **Vary rhythm** — Mix short punchy sentences with longer ones. Not all the same length.
6. **Cut the filler** — If removing a word doesn't change the meaning, remove it
7. **Read it aloud** — If it sounds like a press release, rewrite it

### Step 3: Preserve

Do NOT change:
- Technical accuracy or meaning
- Code examples or technical terms
- Proper nouns, brand names, acronyms
- Intentional formatting (headings, lists where appropriate)
- The author's actual opinions or arguments

### Step 4: Present

Show the rewritten version. If the changes are substantial, briefly note what was changed:
- "Removed hedging and filler from intro"
- "Replaced passive voice throughout"
- "Cut 40% — mostly redundant transitions"

## Inputs
- Text content to humanize (from user's prompt, clipboard, or a file)
- Optional: target audience (blog readers, clients, social media)

## Outputs
- Rewritten content with AI patterns removed
- Brief summary of changes made

## Example Usage

**User:** "Humanize this paragraph"

> In today's rapidly evolving digital landscape, it's important to note that leveraging comprehensive AI solutions can facilitate robust workflow optimization. Moreover, these game-changing tools enable organizations to navigate complex challenges and streamline their operations.

```
✍️ Humanize — Rewriting for natural voice...

AI tools speed up your workflow. They handle the repetitive stuff so your
team can focus on work that actually matters.

Changes: Cut filler intro, replaced "leverage/facilitate/robust/streamline"
with plain language, removed empty transitions, reduced from 41 words to 22.
```

## Level History

- **Lv.1** — Base: AI pattern detection and rewrite protocol. Curated replacement table, structural fixes, voice guidelines. (Origin: MemStack v3.1, Feb 2026)
