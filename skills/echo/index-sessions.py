#!/usr/bin/env python
"""
Echo Skill — Session Indexer
Indexes memory/sessions/*.md and memory/plans/*.md into a local LanceDB
vector database for semantic search.

Usage:
    python skills/echo/index-sessions.py [--force]

Requires: pip install lancedb sentence-transformers
Optional: OPENAI_API_KEY for higher-quality OpenAI embeddings (falls back to local)
"""

import hashlib
import json
import os
import re
import sys
from pathlib import Path

# Resolve project paths relative to this script
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent.parent  # memstack/
MEMORY_DIR = PROJECT_ROOT / "memory"
SESSIONS_DIR = MEMORY_DIR / "sessions"
PLANS_DIR = MEMORY_DIR / "plans"
VECTORS_DIR = MEMORY_DIR / "vectors" / "lancedb"
COLLECTION = "memstack_sessions"


# --- Embedding ---

def get_embedder():
    """Return (embed_fn, provider_name). Tries OpenAI first, falls back to local."""
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if api_key:
        try:
            import openai
            client = openai.OpenAI()
            # Quick connectivity test
            client.embeddings.create(input=["test"], model="text-embedding-3-small")

            def openai_embed(texts: list[str]) -> list[list[float]]:
                resp = client.embeddings.create(input=texts, model="text-embedding-3-small")
                return [d.embedding for d in resp.data]

            return openai_embed, "openai"
        except Exception:
            pass  # Fall through to local

    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("all-MiniLM-L6-v2")

        def local_embed(texts: list[str]) -> list[list[float]]:
            return model.encode(texts).tolist()

        return local_embed, "local"
    except ImportError:
        return None, "none"


# --- Chunking ---

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)


def chunk_markdown(text: str, source: str) -> list[dict]:
    """Split markdown by headings into chunks with metadata."""
    lines = text.split("\n")
    headings: list[tuple[int, int, str]] = []
    for i, line in enumerate(lines):
        m = _HEADING_RE.match(line)
        if m:
            headings.append((i, len(m.group(1)), m.group(2).strip()))

    sections: list[tuple[int, int, str, int]] = []
    if not headings or headings[0][0] > 0:
        end = headings[0][0] if headings else len(lines)
        sections.append((0, end, "", 0))
    for idx, (line_idx, level, title) in enumerate(headings):
        next_start = headings[idx + 1][0] if idx + 1 < len(headings) else len(lines)
        sections.append((line_idx, next_start, title, level))

    chunks = []
    # Extract date and project from filename
    stem = Path(source).stem
    parent = Path(source).parent.name
    date_match = re.match(r"(\d{4}-\d{2}-\d{2})-(.+)", stem)
    file_date = date_match.group(1) if date_match else ""
    file_project = date_match.group(2) if date_match else stem
    file_type = "plan" if parent == "plans" else "session"

    for start, end, heading, level in sections:
        content = "\n".join(lines[start:end]).strip()
        if not content or len(content) < 20:
            continue
        content_hash = hashlib.sha256(content.encode()).hexdigest()[:16]
        chunks.append({
            "id": f"{Path(source).name}:{start}:{content_hash}",
            "content": content,
            "source": source,
            "section_title": heading,
            "date": file_date,
            "project": file_project,
            "type": file_type,
            "content_hash": content_hash,
        })
    return chunks


# --- Indexing ---

def get_indexable_files() -> list[Path]:
    """Return all .md files from sessions and plans directories."""
    files = []
    for d in [SESSIONS_DIR, PLANS_DIR]:
        if d.is_dir():
            files.extend(sorted(d.glob("*.md")))
    return files


def run_index(force: bool = False) -> dict:
    """Index all session and plan markdown files into the vector DB."""
    try:
        import lancedb
    except ImportError:
        return {"ok": False, "error": "lancedb not installed. Run: pip install lancedb"}

    embed_fn, provider = get_embedder()
    if embed_fn is None:
        return {
            "ok": False,
            "error": "No embedding provider available. Install sentence-transformers or set OPENAI_API_KEY.",
        }

    files = get_indexable_files()
    if not files:
        return {"ok": True, "chunks_indexed": 0, "files_scanned": 0, "embedding": provider}

    # Collect all chunks
    all_chunks = []
    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue
        all_chunks.extend(chunk_markdown(text, str(f)))

    if not all_chunks:
        return {"ok": True, "chunks_indexed": 0, "files_scanned": len(files), "embedding": provider}

    # Connect to LanceDB
    VECTORS_DIR.mkdir(parents=True, exist_ok=True)
    db = lancedb.connect(str(VECTORS_DIR))

    # Check for existing data to skip duplicates
    existing_hashes: set[str] = set()
    table_names = db.list_tables().tables
    if not force and COLLECTION in table_names:
        table = db.open_table(COLLECTION)
        try:
            existing = table.to_pandas()
            existing_hashes = set(existing["content_hash"].tolist())
        except Exception:
            pass

    # Filter to new chunks only (unless --force)
    if not force:
        new_chunks = [c for c in all_chunks if c["content_hash"] not in existing_hashes]
    else:
        new_chunks = all_chunks

    if not new_chunks:
        return {
            "ok": True,
            "chunks_indexed": 0,
            "files_scanned": len(files),
            "embedding": provider,
            "message": "All chunks already indexed",
        }

    # Embed
    texts = [c["content"] for c in new_chunks]
    # Batch embeddings in groups of 50 to avoid API limits
    all_vectors = []
    for i in range(0, len(texts), 50):
        batch = texts[i : i + 50]
        all_vectors.extend(embed_fn(batch))

    # Build records for LanceDB
    records = []
    for chunk, vector in zip(new_chunks, all_vectors):
        records.append({
            "id": chunk["id"],
            "vector": vector,
            "content": chunk["content"],
            "source": chunk["source"],
            "section_title": chunk["section_title"],
            "date": chunk["date"],
            "project": chunk["project"],
            "type": chunk["type"],
            "content_hash": chunk["content_hash"],
        })

    # Upsert into LanceDB
    if force and COLLECTION in table_names:
        db.drop_table(COLLECTION)
        table_names = db.list_tables().tables

    if COLLECTION in table_names:
        table = db.open_table(COLLECTION)
        table.add(records)
    else:
        db.create_table(COLLECTION, records)

    # Store embedding metadata so search.py uses the same provider
    dimension = len(all_vectors[0]) if all_vectors else 0
    metadata = {"provider": provider, "dimension": dimension}
    metadata_path = VECTORS_DIR / "metadata.json"
    metadata_path.write_text(json.dumps(metadata), encoding="utf-8")

    return {
        "ok": True,
        "chunks_indexed": len(records),
        "files_scanned": len(files),
        "embedding": provider,
    }


def main():
    force = "--force" in sys.argv
    try:
        result = run_index(force=force)
    except Exception as e:
        result = {"ok": False, "error": str(e)}
    print(json.dumps(result, indent=2))
    if not result.get("ok"):
        sys.exit(1)


if __name__ == "__main__":
    main()
