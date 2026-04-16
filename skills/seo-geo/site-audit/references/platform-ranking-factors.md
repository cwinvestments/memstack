# Platform Ranking Factors — Reference

How the major AI search engines and the traditional Google index actually discover, rank, and cite content in late 2025 / early 2026. Stats in this document come from public research (Princeton GEO 2023, SE Ranking 129K-domain study 2024, Profound 400K-page content-answer fit study 2024, Google official docs). Where numbers come from commercial analyses rather than peer-reviewed work they're noted as such — directional, not gospel. Re-verify anything load-bearing before you rebuild a content strategy around it.

---

## Summary table

| Platform | Primary index | Core selection basis | Freshness bias | Must-have technical signal |
|---|---|---|---|---|
| ChatGPT Search | Web (Bing-backed + live fetch) | Content-Answer fit + domain authority | 30-day content is cited 3.2× more | Strong backlink profile |
| Perplexity | Own crawl + Google + Bing | Semantic relevance + 3-layer reranker | Time-decay on most queries | FAQ schema + PDF-friendly pages |
| Google AI Overview | Google | E-E-A-T + LLM re-ranking on traditional results | Recent updates favored for news/YMYL | Schema markup + topical authority |
| Microsoft Copilot | Bing | Bing index rank + MS ecosystem signals | Varies (IndexNow for fast push) | Bing indexing + page speed < 2s |
| Claude Search | Brave Search | Factual density + structural clarity | Query-dependent | Brave indexing + ClaudeBot allowed |
| Google (traditional) | Google | Backlinks + E-E-A-T + Core Web Vitals | Varies by query class | HTTPS + mobile + CWV in good range |

---

## 1. ChatGPT Search

### How it discovers content

ChatGPT runs a **two-phase retrieval system**:

1. **Pre-training knowledge** — what the base model learned during training (static until the next model release)
2. **Real-time retrieval** — live web fetch, backed primarily by **Bing's index** plus ChatGPT's own user-agent crawls (`GPTBot` for training, `ChatGPT-User` for live browsing)

Pages must be in Bing's index to be retrievable for live queries, and crawlable by `GPTBot` / `ChatGPT-User` to be considered during training cycles.

### Ranking weights (SE Ranking 129K-domain study, 2024)

| Factor | Weight | Notes |
|---|---|---|
| Authority & credibility | ~40% | Branded domains preferred over third-party coverage |
| Content quality & utility | ~35% | Clear structure, comprehensive answers, direct phrasing |
| Platform trust | ~25% | Wikipedia, Reddit, Forbes, academic sources are inherently weighted |

### Citation patterns (measured)

| Signal | Observed effect |
|---|---|
| Referring domains | Strongest single predictor. Sites with >350K referring domains average **8.4 citations per query context** |
| Domain trust score | 91–96 trust score → ~6 citations average; 97–100 → ~8.4 citations average |
| Content recency | Content updated within **30 days gets cited 3.2× more** than older content |
| Branded vs. third-party | Branded official sites cited **11.1 points more** than third-party coverage of the same brand |

### Top citation sources (share of all ChatGPT citations)

| Rank | Source | % of citations |
|---|---|---|
| 1 | Wikipedia | 7.8% |
| 2 | Reddit | 1.8% |
| 3 | Forbes | 1.1% |
| 4+ | Brand official sites + academic / institutional domains | variable |

### Content-answer fit (Profound 400K-page study, 2024)

| Factor | Relevance to citation |
|---|---|
| Content-answer fit (does the page directly answer the query?) | **55%** — most important single factor |
| On-page structure (headings, formatting) | 14% |
| Domain authority (helps retrieval, not direct citation) | 12% |
| Query relevance (intent match) | 12% |
| Content consensus (agreement with other sources) | 7% |

### Format preferences

- Direct, answer-first prose — avoid marketing hedging
- Clean H1 / H2 / H3 hierarchy
- Verifiable statistics with citation
- ChatGPT's conversational response style rewards content written in a similar register

### Bot access required

```
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /
```

---

## 2. Perplexity

### How it discovers content

Perplexity uses **Retrieval-Augmented Generation (RAG)** over its own crawl plus Google and Bing result blending. Its own bot is `PerplexityBot`.

### The 3-layer reranker

| Layer | Purpose |
|---|---|
| **L1 — Basic relevance** | Cheap lexical/semantic retrieval over a large candidate set |
| **L2 — Traditional ranking** | Scores candidates using standard SEO-style factors (authority, freshness, structure) |
| **L3 — ML quality evaluation** | Can **discard entire result sets** if they don't meet quality thresholds — a page that survives L2 can still be dropped here |

### Source selection criteria

| Signal | How Perplexity uses it |
|---|---|
| Authoritative domain lists | Amazon, GitHub, academic / institutional domains get an inherent boost — manually curated |
| Freshness | Time-decay algorithm; new pages evaluated for citation eligibility within hours, not weeks |
| Semantic relevance | Similarity to query intent is weighted heavier than exact keyword match |
| Topical weighting | Tech / AI / science topics get visibility multipliers |
| User engagement | Click-through rates on cited sources feed back into ranking |
| FAQ schema | Pages with FAQ blocks get cited at a measurably higher rate |
| PDF documents | Publicly hosted PDFs prioritized — Perplexity treats them as high-trust data sources |

### Format preferences

- **Atomic paragraphs** — one idea per paragraph, easy to extract
- **FAQ schema (JSON-LD)** — correlates strongly with citation
- Clear semantic payloads — definitions, comparisons, procedures clearly marked
- YouTube titles matching trending queries get an indirect boost via Perplexity's video-aware retrieval

### Bot access required

```
User-agent: PerplexityBot
Allow: /

# Sitemap helps Perplexity discover new pages quickly
Sitemap: https://YOUR_DOMAIN.com/sitemap.xml
```

---

## 3. Google AI Overview (formerly SGE — Search Generative Experience)

### How it discovers content

Google AI Overview reuses **Google's main index** and layers an LLM synthesis pipeline on top. Underlying models: **Gemini** (primary reasoning), **MUM** (multimodal), **PaLM2** legacy.

### 5-stage source prioritization pipeline

1. **Retrieval** — identify candidate sources from the main index
2. **Semantic ranking** — score topical relevance
3. **LLM re-ranking** — Gemini re-evaluates contextual fit
4. **E-E-A-T evaluation** — Experience / Expertise / Authoritativeness / Trustworthiness filter (especially for YMYL — Your Money Your Life topics like health, finance, legal)
5. **Data fusion** — synthesize answer from multiple sources with citation links

### Measured stats (2025)

| Metric | Value |
|---|---|
| Share of searches with an AI Overview | ~85% (varies by query class) |
| Overlap between AI Overview citations and traditional Top 10 | **~15%** — being in the blue-link top 10 is not sufficient |
| Weight on traditional SEO factors | ~62% |
| Weight on novel AI signals (semantic fit, LLM quality score) | ~38% |
| Observed visibility lift for SGE-optimized pages | ~340% |
| Visibility lift from adding authoritative citations | +132% |
| Visibility lift from shifting to an authoritative tone | +89% |

### Format preferences

- Comprehensive schema markup (Article, FAQPage, HowTo, Organization)
- Author bios with credentials (E-E-A-T signal)
- Knowledge-graph entity clarity (linked Wikipedia / Wikidata helps)
- Multimedia — images and video surface in multi-modal responses
- Clear topical clusters with internal linking

### Freshness

Time-sensitive query classes (news, product launches, financial) prioritize recent content; evergreen queries don't penalize older pages if they maintain `dateModified` signals.

---

## 4. Microsoft Copilot

### How it discovers content

Copilot is deeply integrated into Microsoft Edge, Windows 11, Microsoft 365, and Bing Search. It uses **Bing's index** as its primary data source — being absent from Bing effectively means invisibility to Copilot.

### Ranking factors

| Factor | Notes |
|---|---|
| Bing index presence | Non-negotiable. Use Bing Webmaster Tools to verify |
| Microsoft ecosystem signals | LinkedIn activity, GitHub presence, and Microsoft Learn mentions provide lift |
| Crawlability | `Bingbot` and (legacy) `msnbot` must have access |
| Page speed | Under 2 seconds is the informal target for Copilot retrieval |
| Schema markup | Helps Copilot understand entity relationships |
| Entity clarity | Clear, unambiguous definitions of people, products, concepts |

### Format preferences

- Same structural signals that help Bing ranking help Copilot
- Entity pages (product, person, place) with clear structured data
- IndexNow protocol for pushing new content changes fast (Microsoft-backed standard)

### Bot access required

```
User-agent: Bingbot
Allow: /

User-agent: msnbot
Allow: /
```

---

## 5. Claude Search

### How it discovers content

Claude's web search is backed by **Brave Search**, not Google or Bing — a crucial architectural difference. Claude also runs its own crawlers: `ClaudeBot` (general web access) and `anthropic-ai` (training).

Claude decides whether to search based on:
- Query freshness requirements (does this need current info?)
- Specificity (does Claude's trained knowledge already answer this?)
- User intent (explicit "search for X" vs. implicit recall)

When it does search, Claude rewrites the query before issuing it to Brave, so long-tail content that matches natural-language phrasing tends to surface better than keyword-dense pages.

### Source selection criteria

| Signal | How Claude treats it |
|---|---|
| Brave Search indexing | Non-negotiable prerequisite — sites absent from Brave are invisible |
| Factual density | Data-rich content preferred over opinion / marketing |
| Structural clarity | Clearly labeled sections (definitions, tables, step lists) survive extraction better |
| Source authority | Well-sourced content with inline citations favored |
| Query rewriting compatibility | Content that reads like natural answers, not keyword lists |

### Crawl-to-refer ratio

Public Anthropic data indicates a **crawl-to-refer ratio of ~38,065:1** — Claude's bots consume enormous amounts of content but cite very selectively. Implication: raw crawl frequency doesn't translate to citation; quality gating is heavy.

### Format preferences

- High **factual density** (numbers, named entities, verifiable claims)
- **Extractable structure** — tables, numbered steps, Q&A pairs
- Inline citations / data sources
- Clear definitions at the top of relevant sections

### Bot access required

```
User-agent: ClaudeBot
Allow: /

User-agent: anthropic-ai
Allow: /
```

---

## 6. Google Traditional (baseline for comparison)

### How it discovers content

Googlebot crawls the open web; URLs enter the main index after passing spam and quality filters. Sitemap submission via Search Console accelerates discovery. IndexNow is **not** used by Google.

### Core ranking systems

| System | Purpose |
|---|---|
| PageRank | Link-based authority propagation — still live, not deprecated |
| BERT | Natural-language query understanding |
| RankBrain | ML-based ranking signal |
| Helpful Content System | Rewards people-first content, demotes thin / AI-generated-at-scale content |
| Spam Detection | Filters low-quality, duplicate, and manipulative content |

### Top 10 ranking factors

| Rank | Factor | Notes |
|---|---|---|
| 1 | Backlinks | Quality of referring domains; core ranking system |
| 2 | E-E-A-T | Especially load-bearing for YMYL topics |
| 3 | Content quality | Original, comprehensive, satisfies search intent |
| 4 | Page experience | Core Web Vitals + mobile usability |
| 5 | Mobile-first | Mobile version is the ranking version |
| 6 | Search intent match | Content-query-intent alignment |
| 7 | Content freshness | Query-dependent — some queries expect recency, others don't |
| 8 | Technical SEO | Crawlability, indexability, HTTPS |
| 9 | User signals | Dwell time, CTR, bounce rate (debated but present) |
| 10 | Structured data | Schema markup for rich-result eligibility |

### Core Web Vitals targets

| Metric | Good | Needs improvement | Poor |
|---|---|---|---|
| LCP (Largest Contentful Paint) | < 2.5s | 2.5–4.0s | > 4.0s |
| INP (Interaction to Next Paint) — replaced FID in 2024 | < 200ms | 200–500ms | > 500ms |
| CLS (Cumulative Layout Shift) | < 0.1 | 0.1–0.25 | > 0.25 |

### E-E-A-T signals

| Signal | How to demonstrate |
|---|---|
| Experience | First-hand case studies, photos, authenticated dates |
| Expertise | Author credentials, detailed specialist knowledge |
| Authoritativeness | Backlinks from topical authorities, mentions, citations |
| Trustworthiness | Accurate info, transparent sourcing, HTTPS, privacy policy, clear ownership |

---

## Cross-platform takeaways

### Universal best practices (do these regardless of target platform)

1. **Allow all major bots in `robots.txt`** — `Googlebot`, `Bingbot`, `GPTBot`, `ChatGPT-User`, `PerplexityBot`, `ClaudeBot`, `anthropic-ai`, `Google-Extended`
2. **Implement core schema markup** — `Organization`, `WebSite`, `FAQPage` (where appropriate), `Article` on content
3. **Build authoritative backlinks** — still the single biggest correlated factor across Google traditional, ChatGPT, and AI Overview
4. **Update content regularly** — `dateModified` signals matter everywhere; 30-day-freshness amplification measured on ChatGPT
5. **Use clear semantic structure** — H1 / H2 / H3 hierarchy, bullets for lists, tables for comparisons
6. **Include verifiable statistics with citation** — aligns with Princeton GEO findings (+37% from stats, +40% from citations)
7. **Keep page speed under 2 seconds** — passes Google CWV, Copilot preference, and improves Perplexity/Claude extraction reliability
8. **Mobile-first, responsive design** — Google ranks the mobile version; most AI retrieval operates on rendered HTML
9. **Verify index presence per platform** — Google Search Console, Bing Webmaster Tools, Brave Search submission (separate per-platform workflows)
10. **Track AI citation appearances manually** — no unified analytics yet; check monthly with brand-name queries in each tool

### What differs per platform

| If your audience primarily uses... | Focus on... |
|---|---|
| ChatGPT Search | Backlink quality, 30-day freshness, content-answer fit, branded domain authority |
| Perplexity | FAQ schema, PDF resources, topical authority, atomic paragraphs |
| Google AI Overview | E-E-A-T signals, schema markup, topical clusters, authoritative citations |
| Microsoft Copilot | Bing indexing, IndexNow submissions, Microsoft ecosystem presence (LinkedIn, GitHub) |
| Claude Search | Brave Search indexing, factual density, extractable structure, inline citations |
| Google traditional | Backlinks, Core Web Vitals, E-E-A-T, mobile experience, content depth |

---

## Sources

- Aggarwal, P. et al. (2023). *GEO: Generative Engine Optimization.* arXiv:2311.09735. KDD 2024.
- SE Ranking (2024). AI Search Optimization Study — 129K-domain analysis of ChatGPT citations.
- Profound (2024). Content-Answer Fit Study — 400K-page analysis of ChatGPT Search behavior.
- Google Search Central. *Core Web Vitals.* developers.google.com/search/docs/essentials
- Google Search Central. *E-E-A-T and Quality Rater Guidelines.*
- Anthropic. Claude's web search behavior — public documentation and crawl statistics.
- Microsoft Bing Webmaster Tools documentation.
- Brave Search documentation.

Commercial AI-visibility platforms worth monitoring for continued research (Profound, Otterly.ai, Peec AI, SE Ranking AI Toolkit, Semrush AI Visibility, Scrunch AI) publish updated stats regularly — revisit this document annually since generative-engine ranking mechanics shift faster than traditional SEO did.
