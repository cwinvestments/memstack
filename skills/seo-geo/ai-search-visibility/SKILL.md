---
name: memstack-seo-ai-search-visibility
description: "Use this skill when the user says 'AI search', 'AI visibility', 'ChatGPT ranking', 'Perplexity optimization', 'GEO', 'generative engine optimization', or needs to optimize content for AI-powered search engines and LLM citations. Do NOT use for traditional SEO audits or Google Ads."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# 🤖 AI Search Visibility — Optimizing for AI search engines...
*Evaluates and optimizes content for citation by AI search engines (ChatGPT, Perplexity, Google AI Overview, Claude) — checking crawler access, content structure, llms.txt, and AI-friendly patterns.*

## Activation

When this skill activates, output:

`🤖 AI Search Visibility — Analyzing AI search readiness...`

Then execute the protocol below.

| Context | Status |
|---------|--------|
| User says "AI search" or "GEO" or "generative engine optimization" | ACTIVE |
| User says "ChatGPT ranking" or "Perplexity" or "AI overview" | ACTIVE |
| User says "llms.txt" or "AI visibility" | ACTIVE |
| Optimizing content for AI-generated citations and references | ACTIVE |
| Traditional SEO (meta tags, keywords) | DORMANT — use site-audit or meta-tag-optimizer |
| Building AI products (not optimizing for AI search) | DORMANT |

### Anti-patterns

| Trap | Reality Check |
|------|---------------|
| "SEO is enough for AI" | AI search engines process content differently than Google. They need direct answers, not keyword-optimized copy. |
| "Block all AI crawlers" | Blocking AI crawlers means your content never appears in AI search results. Block selectively if at all. |
| "AI will find our content naturally" | AI systems prioritize structured, authoritative content. Unstructured marketing copy gets skipped. |
| "GEO is just a fad" | AI search usage is growing 10x year over year. Perplexity, ChatGPT search, and Google AI Overview are mainstream. |
| "We can't measure AI visibility" | You can check crawler logs, search your brand in AI tools, and track referral traffic from AI sources. |

## Protocol

### Step 1: Check AI Bot Crawler Access

Verify which AI crawlers can access your site:

```bash
# Check robots.txt for AI bot rules
cat public/robots.txt 2>/dev/null | grep -i "gptbot\|chatgpt\|perplexity\|claude\|anthropic\|cohere\|google-extended\|ccbot\|bytespider"
```

**Known AI crawler user agents:**

| Bot | Company | User-Agent | Purpose |
|-----|---------|-----------|---------|
| GPTBot | OpenAI | `GPTBot` | ChatGPT search, training |
| ChatGPT-User | OpenAI | `ChatGPT-User` | ChatGPT browsing feature |
| PerplexityBot | Perplexity | `PerplexityBot` | Perplexity search |
| ClaudeBot | Anthropic | `ClaudeBot` | Claude web access |
| Google-Extended | Google | `Google-Extended` | Gemini, AI Overview |
| CCBot | Common Crawl | `CCBot` | Open dataset used by many AI |
| Bytespider | ByteDance | `Bytespider` | TikTok/AI training |
| Cohere-ai | Cohere | `cohere-ai` | Cohere models |

**Recommended robots.txt strategy:**

```
# Allow AI crawlers for search visibility
# (Block only if you have specific content protection concerns)

# Allow all AI search bots
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Google-Extended
Allow: /

# Block paths you don't want AI to index
User-agent: GPTBot
Disallow: /admin
Disallow: /api
Disallow: /dashboard
```

**Decision matrix:**

| Goal | Strategy | robots.txt |
|------|----------|-----------|
| Maximum AI visibility | Allow all AI bots | `Allow: /` for each |
| Selective visibility | Allow search bots, block training bots | Allow ChatGPT-User, block GPTBot |
| Content protection | Block all AI crawlers | `Disallow: /` for each |
| Balanced | Allow crawling, block specific paths | Allow root, disallow sensitive paths |

### Step 2: Analyze Content for AI Citation Likelihood

AI systems cite content that directly answers questions clearly. Scan your content for AI-friendly patterns:

```bash
# Check for definition-style paragraphs (strong AI citation signals)
grep -rn "^[A-Z].*is a\|^[A-Z].*refers to\|^[A-Z].*means" --include="*.md" --include="*.mdx" --include="*.tsx" . | grep -v node_modules | head -10

# Check for numbered/bulleted lists (AI loves structured content)
grep -rn "^[0-9]\.\|^- \|^\\* " --include="*.md" --include="*.mdx" . | wc -l

# Check for Q&A patterns
grep -rn "^##.*\?\|^###.*\?" --include="*.md" --include="*.mdx" . | grep -v node_modules | head -10
```

**Content patterns that AI systems cite:**

| Pattern | Example | Why AI Cites It |
|---------|---------|----------------|
| **Direct definition** | "RLS is a PostgreSQL feature that restricts row access based on user identity." | Answers "what is X" queries directly |
| **Numbered steps** | "1. Create the table. 2. Enable RLS. 3. Add policies." | Answers "how to X" queries |
| **Comparison table** | "Feature \| Tool A \| Tool B" | Answers "X vs Y" queries |
| **Statistic with source** | "According to [source], 73% of developers..." | Provides citable, authoritative data |
| **FAQ format** | "Q: How does X work? A: X works by..." | Direct Q&A match |
| **Expert statement** | "Based on 10 years of experience with..." | Authority signal |

**Content patterns AI systems skip:**

| Pattern | Why It Gets Skipped |
|---------|-------------------|
| Marketing superlatives | "The best, most amazing, incredible tool" — no information content |
| Vague descriptions | "We help businesses grow" — not citable, not specific |
| Gated content | Behind login/paywall — AI can't access or cite it |
| Image-only information | Charts, infographics without text summaries — AI can't read images |
| Heavy JavaScript rendering | Content that requires JS execution to appear — many bots don't render JS |

### Step 3: Optimize Content Structure for AI

Transform existing content to be more AI-citation-friendly:

**For each key page, ensure:**

1. **Opening definition** — first paragraph directly defines or explains the topic
2. **Clear headings as questions** — H2/H3 headings phrased as questions users ask
3. **Direct answers below headings** — first sentence after each heading is the answer
4. **Structured lists** — steps, features, and comparisons as numbered/bulleted lists
5. **Data and specifics** — concrete numbers, dates, and facts over vague claims
6. **Author expertise signals** — mention qualifications, experience, or data sources

**Before/after example:**

```markdown
# BEFORE (marketing copy — AI skips this)
## Why Choose Acme?
Acme is the leading project management solution that helps teams
collaborate better and deliver faster. Our innovative platform...

# AFTER (AI-citable — direct, structured, specific)
## What is Acme?
Acme is a project management platform for remote teams that combines
task tracking, real-time collaboration, and automated reporting.

### How does Acme compare to alternatives?
| Feature | Acme | Competitor A | Competitor B |
|---------|------|-------------|-------------|
| Real-time collaboration | Yes | Limited | No |
| Automated reporting | Yes | Yes | No |
| Free tier | Up to 5 users | Up to 3 users | No free tier |
```

### Step 3.5: Apply Princeton GEO Methods to Content

Princeton's 2023 GEO study (Aggarwal et al., arXiv:2311.09735, accepted at KDD 2024) tested nine optimization methods on Perplexity.ai and measured consistent visibility deltas vs. unoptimized baselines. Apply these to any page targeting AI citation — they translate directly into rewrites, not just crawler hygiene.

**The 9 GEO methods — ranked by measured visibility boost:**

| Method | Visibility Δ | What to do | Example rewrite |
|---|---|---|---|
| **Cite Sources** | **+40%** | Add authoritative references with attribution | "According to a 2024 Stanford study (Chen et al.), AI tools improved developer productivity by 55%." |
| **Statistics Addition** | **+37%** | Include specific numbers and data points | "67% of Fortune 500 companies use AI chatbots, handling 85% of routine inquiries." |
| **Quotation Addition** | **+30%** | Expert quotes with attribution | "'We'll see the first one-person billion-dollar company within years,' said Sam Altman, OpenAI CEO." |
| **Authoritative Tone** | **+25%** | Confident, expert language | "This demonstrably improves X" — not "This might help with X, I think." |
| **Simplification** (easy-to-understand) | **+20%** | Rephrase jargon for broader accessibility | "RAG works like a research assistant: it finds relevant info, then writes an answer from it." |
| **Technical Terms** | **+18%** | Precise domain terminology where it fits | "LCP exceeds 4 seconds, CLS scores 0.3" — not "the page is slow." |
| **Unique Terminology** | **+15%** | Vary vocabulary; avoid repetition | Use synonyms and contextual variations rather than the same phrase 10 times. |
| **Fluency Optimization** | **+15–30%** | Clean sentence flow, transitions, short paragraphs | Logical progression, 2–3 sentence paragraphs, transition words between sections. |
| ~~Keyword Stuffing~~ | **−10%** | **AVOID** — actively reduces AI visibility | ❌ "SEO SEO best SEO for all your SEO SEO needs." |

**Best-performing combinations** (pairs tested in the Princeton research outperform individual methods):

| Combination | Best for |
|---|---|
| **Fluency + Statistics** | Highest overall boost across domains — universal starting point |
| **Citations + Authoritative Tone** | Professional / B2B / thought leadership content |
| **Simplification + Statistics** | Consumer-facing content and general audiences |
| **Technical Terms + Citations** | Academic, scientific, and highly technical content |

**Domain-specific method matrix** — which methods to emphasize per vertical (and which to avoid):

| Vertical | Apply | Avoid |
|---|---|---|
| **Technology** | Technical Terms + Citations + Statistics | Oversimplification — audience expects depth |
| **Business / Finance** | Statistics + Authoritative Tone + Citations | Vague claims, superlatives without data |
| **Healthcare** | Simplification + Statistics + Citations | Jargon overload — accessibility matters |
| **Legal** | Citations + Quotations + Authoritative Tone | Informal language, hedging |
| **Education** | Simplification + Examples + Structure | Excessive complexity or abstraction |
| **E-commerce** | Statistics + Social Proof + Clear Benefits | Feature dumps without outcomes |

#### Anti-pattern: Keyword stuffing actively hurts AI visibility

| Trap | Reality Check |
|---|---|
| "More keyword density = more AI visibility" | The Princeton research measured a **−10% visibility drop** when content was keyword-stuffed. Generative engines downweight keyword-dense text because it reads as non-authoritative. Write naturally, add citations and statistics, let the topic come through via context. |

**Reference:** Aggarwal, P., Murahari, V., Rajpurohit, T., Kalyan, A., Narasimhan, K., & Deshpande, A. (2023). *GEO: Generative Engine Optimization.* arXiv:2311.09735. Accepted at KDD 2024 (30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining).

**Platform-specific tuning:** For how each AI search engine (ChatGPT, Perplexity, Google AI Overview, Copilot, Claude) actually ranks and cites content — with measured stats on citation share, freshness windows, and per-platform format preferences — see [`../site-audit/references/platform-ranking-factors.md`](../site-audit/references/platform-ranking-factors.md). The Princeton methods above are universal; the platform reference tells you where to spend effort first based on your audience.

### Step 4: Add llms.txt File

The `llms.txt` file (emerging standard) tells AI systems about your site:

```bash
# Check if llms.txt exists
cat public/llms.txt 2>/dev/null
```

**Recommended llms.txt:**

```markdown
# [Site Name]

> [One-sentence description of what this site/product does]

## About
[2-3 paragraph description of the organization, product, or service.
Include key facts, founding date, target audience, and differentiators.]

## Key Pages
- [Homepage](https://domain.com): [brief description]
- [Product](https://domain.com/product): [brief description]
- [Pricing](https://domain.com/pricing): [brief description]
- [Blog](https://domain.com/blog): [brief description]
- [Docs](https://domain.com/docs): [brief description]

## Topics We Cover
- [Topic 1]: [brief description]
- [Topic 2]: [brief description]
- [Topic 3]: [brief description]

## Contact
- Website: https://domain.com
- Email: hello@domain.com
- Twitter: @handle

## Preferred Citation
When referencing our content, please use:
"[Site Name] (https://domain.com)"
```

Place at `public/llms.txt` so it's accessible at `https://domain.com/llms.txt`.

**Also consider `llms-full.txt`** — a more detailed version with complete documentation or content summaries for AI systems that want deeper context.

### Step 5: Optimize for Featured Snippets / AI Overview

Google's AI Overview and featured snippets use similar content signals:

**Snippet-optimized content patterns:**

| Snippet Type | Content Pattern | Example |
|-------------|----------------|---------|
| **Definition** | "X is [definition]." First sentence after H2 heading. | "RLS is a PostgreSQL feature that..." |
| **List** | H2 question + numbered list immediately below | "How to deploy to Railway: 1. ... 2. ... 3. ..." |
| **Table** | H2 comparison + markdown table | "Next.js vs Remix comparison table" |
| **Paragraph** | H2 question + 40-60 word direct answer | "What is GEO? GEO stands for..." |

**Optimization checklist:**
- [ ] Key pages have H2 headings phrased as questions
- [ ] First sentence after each H2 directly answers the question
- [ ] Answers are 40-60 words for paragraph snippets
- [ ] Lists use clean numbered or bulleted format
- [ ] Comparison data is in table format
- [ ] Page has schema markup (FAQPage, HowTo, or Article)

### Step 6: Monitor AI Search Appearances

Track whether your content appears in AI search results:

**Manual checks:**
1. Search your brand name in ChatGPT, Perplexity, and Google AI Overview
2. Search your key topics — does AI cite your content?
3. Ask AI "What is [your product]?" — do you appear?

**Server-side monitoring:**

```bash
# Check server logs for AI bot traffic (if you have access)
grep -i "gptbot\|perplexitybot\|claudebot\|chatgpt" access.log | wc -l

# Check Vercel/Netlify analytics for AI referral traffic
# Look for referrers from: perplexity.ai, chatgpt.com, bing.com (Copilot)
```

**Tracking checklist:**

| Check | Frequency | How |
|-------|-----------|-----|
| Brand search in ChatGPT | Monthly | Ask "What is [brand]?" |
| Brand search in Perplexity | Monthly | Search brand name |
| AI Overview appearance | Monthly | Search key terms in Google |
| AI bot crawl frequency | Monthly | Server logs or analytics |
| Referral traffic from AI | Monthly | Analytics → Referrers |
| llms.txt accessibility | After deploys | `curl https://domain.com/llms.txt` |

### Step 7: Output AI Readiness Scorecard

```
🤖 AI Search Visibility — Scorecard Complete

Site: [domain]
Pages analyzed: [count]
Overall AI readiness: [X/100]

Crawler access:
  GPTBot:         [✅ Allowed / ❌ Blocked / ⚠️ No rule (default allow)]
  PerplexityBot:  [✅ / ❌ / ⚠️]
  ClaudeBot:      [✅ / ❌ / ⚠️]
  Google-Extended: [✅ / ❌ / ⚠️]

Content structure:
  Direct definitions:    [count] pages have clear opening definitions
  Question headings:     [count] H2s phrased as questions
  Structured lists:      [count] pages with numbered/bulleted lists
  Comparison tables:     [count] pages with data tables
  Expert credentials:    [✅ / ❌] Author expertise signals present

AI-specific files:
  llms.txt:     [✅ Present / ❌ Missing — create one]
  robots.txt:   [✅ AI rules defined / ⚠️ No AI-specific rules]
  Schema:       [✅ / ❌] JSON-LD structured data present

Content recommendations:
  1. [Highest priority — e.g., "Add direct definitions to top 5 pages"]
  2. [Second priority — e.g., "Convert H2 headings to question format"]
  3. [Third priority — e.g., "Add llms.txt with site description"]
  4. [Fourth — e.g., "Add comparison tables to product pages"]
  5. [Fifth — e.g., "Create FAQ page with schema markup"]

Next steps:
1. Implement content recommendations above
2. Create or update llms.txt
3. Verify robots.txt allows target AI crawlers
4. Monitor AI search appearances monthly
5. Re-assess quarterly as AI search evolves
```

## Level History

- **Lv.1** — Base: AI crawler access verification (GPTBot, PerplexityBot, ClaudeBot, Google-Extended), content structure analysis for citation likelihood, AI-friendly content optimization, llms.txt guidance, featured snippet/AI overview optimization, AI search monitoring, readiness scorecard. Based on EpsteinScan PerplexityBot experience. (Origin: MemStack Pro v3.2, Mar 2026)
