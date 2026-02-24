# Echo Skill Upgrade Plan — Vector-Powered Semantic Recall

> **Migration Note (2026-02-24):** Originally designed for MemSearch/Milvus Lite. Swapped to **LanceDB + sentence-transformers** because milvus-lite and ChromaDB both lack Python 3.14 builds. LanceDB is Apache Arrow-based, zero-config, and Python 3.14 compatible. The architecture below reflects the original design; the actual implementation uses LanceDB.

## Overview

Upgrade Echo from keyword-based `LIKE` search (Lv.4) to **semantic vector search** (Lv.5) using **LanceDB** with sentence-transformers embeddings (OpenAI optional). This adds semantic similarity matching across all session logs and plans while keeping the existing SQLite search as a fallback.

## Architecture

```
Current (Lv.4):
  User query → memstack-db.py search (LIKE '%keyword%') → SQLite results

Upgraded (Lv.5):
  User query → search.py (MemSearch semantic) → Vector results (ranked by similarity)
           ↘ memstack-db.py search (LIKE) → SQLite results (fallback)
```

### Data Flow — Indexing

```
memory/sessions/*.md ─┐
memory/plans/*.md    ──┤──→ index-sessions.py ──→ MemSearch.index()
                       │         │                     │
                       │    Chunks by ## heading   Embed + upsert
                       │         │                     │
                       │         ▼                     ▼
                       │    SHA-256 dedup         memory/vectors/memsearch.db
                       │    (skip unchanged)       (Milvus Lite local)
```

### Data Flow — Search

```
User: "recall Railway cost optimization"
  │
  ▼
search.py --query "Railway cost optimization" --top-k 5
  │
  ├─→ MemSearch.search() ──→ Hybrid (dense cosine + BM25 + RRF reranking)
  │       │
  │       ▼
  │   Top 5 chunks with:
  │     - content (text)
  │     - source (file path)
  │     - heading (section title)
  │     - score (0.0 - 1.0 similarity)
  │
  └─→ If MemSearch unavailable → fallback to memstack-db.py search
```

## Components

### 1. `skills/echo/index-sessions.py`
- **Purpose**: Index session and plan markdown files into the vector DB
- **Input**: Scans `memory/sessions/*.md` and `memory/plans/*.md`
- **Chunking**: MemSearch's built-in heading-based chunker (splits on `##` headers)
- **Metadata per chunk**: `{source, heading, start_line, end_line, content_hash}`
- **Dedup**: SHA-256 content hashing — unchanged chunks are auto-skipped
- **Output**: Vector DB at `memory/vectors/memsearch.db` (Milvus Lite)
- **Embedding**: OpenAI `text-embedding-3-small` (default) or configurable via `.memsearch.toml`
- **CLI**: `python skills/echo/index-sessions.py [--force]`

### 2. `skills/echo/search.py`
- **Purpose**: Semantic search across indexed session/plan content
- **Input**: Natural language query string
- **Output**: JSON array of top-K results with `{content, source, heading, score}`
- **Formatting**: Extracts date and project from file path for CC-friendly output
- **CLI**: `python skills/echo/search.py "query text" [--top-k 5] [--json]`

### 3. Updated `skills/echo/SKILL.md`
- New protocol: try vector search first, SQLite second
- New activation message: `🔊 Echo — Semantic search activated...`
- Level bump to **Lv.5** with vector search capability

### 4. Project-level config: `.memsearch.toml` (in memstack root)
```toml
[milvus]
uri = "memory/vectors/memsearch.db"
collection = "memstack_sessions"

[embedding]
provider = "openai"
# model = "text-embedding-3-small"  # default

[chunking]
max_chunk_size = 1500
overlap_lines = 2
```

## Storage

- **Vector DB**: `memory/vectors/memsearch.db` (Milvus Lite — single file, zero config)
- **Added to .gitignore**: `memory/vectors/` (derived index, rebuildable from markdown)
- **Source of truth**: Markdown files in `memory/sessions/` and `memory/plans/` remain the canonical data

## Dependencies

- `memsearch` (pip install memsearch) — semantic search engine
- `OPENAI_API_KEY` environment variable — for embedding generation
- Python 3.10+ (already required by MemStack)

## Fallback Strategy

If MemSearch is unavailable (not installed, no API key, vector DB missing):
1. Log a warning: "MemSearch unavailable, falling back to SQLite keyword search"
2. Execute current Lv.4 protocol: `memstack-db.py search` → `get-sessions` → `get-insights`
3. No user-facing error — graceful degradation

## Level History Addition

- **Lv.5** — Semantic: MemSearch vector-powered recall with hybrid search (dense + BM25 + RRF). Auto-indexes sessions/plans, semantic similarity across all logs, SQLite fallback. (Origin: MemStack v3.1, Feb 2026)
