#!/usr/bin/env python
"""
Echo Skill — Session Indexer
Indexes memory/sessions/*.md and memory/plans/*.md into a local LanceDB
vector database for semantic search.

Usage:
    python skills/echo/index-sessions.py [--force] [--provider local|openai]

Requires: pip install lancedb sentence-transformers
Embeddings default to LOCAL (sentence-transformers). OpenAI is strictly opt-in:
it is used only when explicitly selected via --provider openai or the
MEMSTACK_EMBED_PROVIDER=openai environment variable, AND an OPENAI_API_KEY is set.
A bare OPENAI_API_KEY in the environment never triggers OpenAI on its own.
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

def _wants_openai(explicit: str | None = None) -> bool:
    """Whether OpenAI embeddings are explicitly opted into.

    Precedence: explicit value (e.g. --provider) > MEMSTACK_EMBED_PROVIDER env > "local".
    LOCAL is always the default; a bare OPENAI_API_KEY in the environment does NOT
    select OpenAI. OpenAI requires a deliberate "openai" opt-in.
    """
    val = (explicit or os.environ.get("MEMSTACK_EMBED_PROVIDER", "local")).strip().lower()
    return val == "openai"


def get_embedder(provider_override: str | None = None):
    """Return (embed_fn, provider_name).

    Provider precedence: provider_override (--provider) > MEMSTACK_EMBED_PROVIDER > local.
    OpenAI is strictly opt-in and never silently substituted: an explicit OpenAI opt-in
    with a missing key or a failing API call is a hard error (distinct provider_name
    sentinel), never a quiet downgrade to local.
    """
    if _wants_openai(provider_override):
        api_key = os.environ.get("OPENAI_API_KEY", "")
        if not api_key:
            return None, "openai-missing-key"
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
            return None, "openai-failed"

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
        default_title = Path(source).stem or "General"
        sections.append((0, end, default_title, 0))
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


def run_index(force: bool = False, provider_override: str | None = None) -> dict:
    """Index all session and plan markdown files into the vector DB."""
    try:
        import lancedb
    except ImportError:
        return {"ok": False, "error": "lancedb not installed. Run: pip install lancedb"}

    embed_fn, provider = get_embedder(provider_override=provider_override)
    if embed_fn is None:
        if provider == "openai-missing-key":
            return {
                "ok": False,
                "error": "OpenAI embeddings were explicitly requested "
                         "(--provider openai or MEMSTACK_EMBED_PROVIDER=openai) but OPENAI_API_KEY "
                         "is not set. Set the key, or switch to local (the default).",
            }
        if provider == "openai-failed":
            return {
                "ok": False,
                "error": "OpenAI embeddings were explicitly requested but the OpenAI API call failed "
                         "(missing 'openai' package, bad key, or network). Refusing to silently fall "
                         "back to local. Fix the key/package or switch to local.",
            }
        return {
            "ok": False,
            "error": "No embedding provider available. Install sentence-transformers "
                     "(pip install sentence-transformers).",
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
            existing = table.to_list()
            existing_hashes = set(r["content_hash"] for r in existing)
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

    # --provider local|openai (convenience override; precedence over MEMSTACK_EMBED_PROVIDER)
    provider_override = None
    if "--provider" in sys.argv:
        i = sys.argv.index("--provider")
        if i + 1 >= len(sys.argv):
            print(json.dumps({"ok": False, "error": "--provider requires a value: local or openai"}, indent=2))
            sys.exit(1)
        provider_override = sys.argv[i + 1].strip().lower()
        if provider_override not in ("local", "openai"):
            print(json.dumps(
                {"ok": False, "error": f"Invalid --provider '{provider_override}'. Use 'local' or 'openai'."},
                indent=2,
            ))
            sys.exit(1)

    try:
        result = run_index(force=force, provider_override=provider_override)
    except Exception as e:
        result = {"ok": False, "error": str(e)}
    print(json.dumps(result, indent=2))
    if not result.get("ok"):
        sys.exit(1)


if __name__ == "__main__":
    main()
