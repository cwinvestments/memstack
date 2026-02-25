#!/usr/bin/env python
"""
Echo Skill — Semantic Search
Searches indexed session/plan content using LanceDB vector similarity.

Usage:
    python skills/echo/search.py "query text" [--top-k 5] [--json]

Requires: pip install lancedb sentence-transformers
Optional: OPENAI_API_KEY for higher-quality OpenAI embeddings (falls back to local)

Output format (default):
    **[1] docstack** — 2026-02-19 (session)
      Section: Accomplished
      Score: 0.847
      Built the document pipeline with...
      Source: memory/sessions/2026-02-19-docstack.md
      ---

Output format (--json):
    [{"content": "...", "source": "...", "section_title": "...", "score": 0.85, ...}]
"""

import argparse
import json
import os
import sys
from pathlib import Path

# Fix Windows cp1252 encoding crash when printing Unicode (arrows, emojis in session data)
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8")

SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent.parent
VECTORS_DIR = PROJECT_ROOT / "memory" / "vectors" / "lancedb"
COLLECTION = "memstack_sessions"


def get_embedder(required_provider: str | None = None):
    """Return (embed_fn, provider_name). Matches index provider to avoid dimension mismatch."""
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if api_key and required_provider != "local":
        try:
            import openai
            client = openai.OpenAI()

            def openai_embed(texts: list[str]) -> list[list[float]]:
                resp = client.embeddings.create(input=texts, model="text-embedding-3-small")
                return [d.embedding for d in resp.data]

            return openai_embed, "openai"
        except Exception:
            pass

    if required_provider == "openai":
        return None, "none"

    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("all-MiniLM-L6-v2")

        def local_embed(texts: list[str]) -> list[list[float]]:
            return model.encode(texts).tolist()

        return local_embed, "local"
    except ImportError:
        return None, "none"


def run_search(query: str, top_k: int = 5) -> list[dict]:
    """Search indexed sessions/plans for semantically similar content."""
    try:
        import lancedb
    except ImportError:
        print(
            json.dumps({"ok": False, "error": "lancedb not installed. Run: pip install lancedb"}),
            file=sys.stderr,
        )
        return []

    if not VECTORS_DIR.exists():
        print(
            json.dumps({"ok": False, "error": "Vector DB not found. Run index-sessions.py first."}),
            file=sys.stderr,
        )
        return []

    # Read index metadata to match embedding provider (avoids dimension mismatch)
    required_provider = None
    metadata_path = VECTORS_DIR / "metadata.json"
    if metadata_path.exists():
        try:
            meta = json.loads(metadata_path.read_text(encoding="utf-8"))
            required_provider = meta.get("provider")
        except Exception:
            pass

    embed_fn, _provider = get_embedder(required_provider=required_provider)
    if embed_fn is None:
        msg = f"Index was built with '{required_provider}' embeddings which is unavailable. " \
              f"Re-index with: python index-sessions.py --force" if required_provider \
              else "No embedding provider. Install sentence-transformers or set OPENAI_API_KEY."
        print(json.dumps({"ok": False, "error": msg}), file=sys.stderr)
        return []

    try:
        db = lancedb.connect(str(VECTORS_DIR))
        if COLLECTION not in db.list_tables().tables:
            print(
                json.dumps({"ok": False, "error": f"Collection '{COLLECTION}' not found. Run index-sessions.py first."}),
                file=sys.stderr,
            )
            return []

        table = db.open_table(COLLECTION)

        # Embed query
        query_vector = embed_fn([query])[0]

        # Search using cosine distance for meaningful similarity scores
        results = table.search(query_vector).metric("cosine").limit(top_k).to_list()

        enriched = []
        for r in results:
            # Cosine distance: 0 = identical, 2 = opposite. Convert to 0-1 similarity.
            distance = r.get("_distance", 1.0)
            score = max(0.0, 1.0 - distance)
            enriched.append({
                "content": r.get("content", ""),
                "source": r.get("source", ""),
                "section_title": r.get("section_title", ""),
                "score": round(score, 4),
                "date": r.get("date", ""),
                "project": r.get("project", ""),
                "type": r.get("type", "session"),
            })
        return enriched

    except Exception as e:
        print(
            json.dumps({"ok": False, "error": f"Search failed: {e}"}),
            file=sys.stderr,
        )
        return []


def format_results(results: list[dict]) -> str:
    """Format results for human-readable CC output."""
    if not results:
        return "No semantic matches found."

    lines = []
    for i, r in enumerate(results, 1):
        lines.append(f"**[{i}] {r['project']}** — {r['date']} ({r['type']})")
        if r["section_title"]:
            lines.append(f"  Section: {r['section_title']}")
        lines.append(f"  Score: {r['score']}")
        content = r["content"][:300]
        if len(r["content"]) > 300:
            content += "..."
        lines.append(f"  {content}")
        lines.append(f"  Source: {r['source']}")
        lines.append("  ---")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Echo semantic search")
    parser.add_argument("query", help="Natural language search query")
    parser.add_argument("--top-k", type=int, default=5, help="Number of results (default: 5)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    results = run_search(args.query, top_k=args.top_k)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(format_results(results))


if __name__ == "__main__":
    main()
