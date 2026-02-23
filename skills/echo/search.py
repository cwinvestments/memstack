#!/usr/bin/env python
"""
Echo Skill — Semantic Search
Searches indexed session/plan content using MemSearch vector similarity.

Usage:
    python skills/echo/search.py "query text" [--top-k 5] [--json]

Requires: pip install memsearch
Requires: OPENAI_API_KEY environment variable (for embeddings)

Output format (default):
    Source: memory/sessions/2026-02-19-docstack.md
    Section: Accomplished
    Score: 0.847
    Content: Built the document pipeline with...
    ---

Output format (--json):
    [{"source": "...", "heading": "...", "score": 0.85, "content": "...", ...}]
"""

import asyncio
import argparse
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent.parent
VECTORS_DIR = PROJECT_ROOT / "memory" / "vectors"
VECTOR_DB = VECTORS_DIR / "memsearch.db"


def extract_metadata(source: str) -> dict:
    """Extract date and project name from session file path.

    Example: memory/sessions/2026-02-19-docstack.md
           → {date: "2026-02-19", project: "docstack", type: "session"}
    """
    name = Path(source).stem  # e.g. "2026-02-19-docstack"
    parent = Path(source).parent.name  # e.g. "sessions" or "plans"

    meta = {"type": "plan" if parent == "plans" else "session"}

    # Try to extract date and project from filename pattern: YYYY-MM-DD-project
    match = re.match(r"(\d{4}-\d{2}-\d{2})-(.+)", name)
    if match:
        meta["date"] = match.group(1)
        meta["project"] = match.group(2)
    else:
        meta["date"] = ""
        meta["project"] = name

    return meta


async def run_search(query: str, top_k: int = 5) -> list[dict]:
    """Search indexed sessions/plans for semantically similar content."""
    try:
        from memsearch import MemSearch
    except ImportError:
        print(
            json.dumps({"ok": False, "error": "memsearch not installed"}),
            file=sys.stderr,
        )
        return []

    if not VECTOR_DB.exists():
        print(
            json.dumps({"ok": False, "error": "Vector DB not found. Run index-sessions.py first."}),
            file=sys.stderr,
        )
        return []

    try:
        mem = MemSearch(
            paths=[],  # no paths needed for search-only
            milvus_uri=str(VECTOR_DB),
            collection="memstack_sessions",
        )
    except Exception as e:
        print(
            json.dumps({"ok": False, "error": f"MemSearch init failed: {e}"}),
            file=sys.stderr,
        )
        return []

    try:
        results = await mem.search(query, top_k=top_k)
        # Enrich results with extracted metadata
        enriched = []
        for r in results:
            meta = extract_metadata(r.get("source", ""))
            enriched.append({
                "content": r.get("content", ""),
                "source": r.get("source", ""),
                "heading": r.get("heading", ""),
                "score": round(r.get("score", 0.0), 4),
                "date": meta.get("date", ""),
                "project": meta.get("project", ""),
                "type": meta.get("type", "session"),
            })
        return enriched
    finally:
        mem.close()


def format_results(results: list[dict]) -> str:
    """Format results for human-readable CC output."""
    if not results:
        return "No semantic matches found."

    lines = []
    for i, r in enumerate(results, 1):
        lines.append(f"**[{i}] {r['project']}** — {r['date']} ({r['type']})")
        if r["heading"]:
            lines.append(f"  Section: {r['heading']}")
        lines.append(f"  Score: {r['score']}")
        # Truncate content for display
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

    results = asyncio.run(run_search(args.query, top_k=args.top_k))

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(format_results(results))


if __name__ == "__main__":
    main()
