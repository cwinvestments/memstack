#!/usr/bin/env python
"""
Echo Skill — Session Indexer
Indexes memory/sessions/*.md and memory/plans/*.md into a local Milvus Lite
vector database for semantic search via MemSearch.

Usage:
    python skills/echo/index-sessions.py [--force]

Requires: pip install memsearch
Requires: OPENAI_API_KEY environment variable (for embeddings)
"""

import asyncio
import json
import sys
from pathlib import Path

# Resolve project paths relative to this script
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent.parent  # memstack/
MEMORY_DIR = PROJECT_ROOT / "memory"
SESSIONS_DIR = MEMORY_DIR / "sessions"
PLANS_DIR = MEMORY_DIR / "plans"
VECTORS_DIR = MEMORY_DIR / "vectors"
VECTOR_DB = VECTORS_DIR / "memsearch.db"


def get_indexable_paths() -> list[str]:
    """Return list of directories that exist and contain .md files."""
    paths = []
    for d in [SESSIONS_DIR, PLANS_DIR]:
        if d.is_dir() and list(d.glob("*.md")):
            paths.append(str(d))
    return paths


async def run_index(force: bool = False) -> dict:
    """Index all session and plan markdown files into the vector DB."""
    try:
        from memsearch import MemSearch
    except ImportError:
        return {
            "ok": False,
            "error": "memsearch not installed. Run: pip install memsearch",
        }

    paths = get_indexable_paths()
    if not paths:
        return {"ok": True, "chunks": 0, "message": "No markdown files found to index"}

    # Ensure vectors directory exists
    VECTORS_DIR.mkdir(parents=True, exist_ok=True)

    try:
        mem = MemSearch(
            paths=paths,
            milvus_uri=str(VECTOR_DB),
            collection="memstack_sessions",
        )
    except Exception as e:
        return {
            "ok": False,
            "error": f"MemSearch init failed: {e}",
        }

    try:
        chunks = await mem.index(force=force)
        return {
            "ok": True,
            "chunks": chunks,
            "paths": paths,
            "db": str(VECTOR_DB),
        }
    finally:
        mem.close()


def main():
    force = "--force" in sys.argv
    result = asyncio.run(run_index(force=force))
    print(json.dumps(result, indent=2))
    if not result["ok"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
