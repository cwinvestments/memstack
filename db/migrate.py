#!/usr/bin/env python
"""
MemStack Migration — Import existing markdown memory into SQLite.

Reads memory/sessions/*.md and imports structured data into the database.
Safe to run multiple times (uses INSERT OR IGNORE pattern via date+project uniqueness).
"""

import json
import os
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
DB_PATH = ROOT / "db" / "memstack.db"
SESSIONS_DIR = ROOT / "memory" / "sessions"
ARCHIVE_DIR = SESSIONS_DIR / "archive"


def get_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def parse_section(text, header):
    """Extract content under a ## header until the next ## or end of text."""
    pattern = rf"^##\s+{re.escape(header)}\s*\n(.*?)(?=^##\s|\Z)"
    match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""


def parse_session_file(filepath):
    """Parse a session markdown file into structured entries."""
    text = filepath.read_text(encoding="utf-8")
    filename = filepath.stem  # e.g., "2026-02-19-docstack"

    # Extract date and project from filename
    match = re.match(r"(\d{4}-\d{2}-\d{2})-(.+)", filename)
    if not match:
        print(f"  SKIP: {filename} (doesn't match date-project pattern)")
        return []

    date = match.group(1)
    project = match.group(2)

    entries = []

    # Check for multi-session format (Session 2:, Session 3:, etc.)
    # Split on "## Session N:" headers
    session_splits = re.split(r"^(## Session \d+:.*?)$", text, flags=re.MULTILINE)

    if len(session_splits) > 1:
        # Multi-session file: first part is Session 1 (no explicit header)
        base_entry = {
            "project": project,
            "date": date,
            "accomplished": parse_section(text, "Accomplished"),
            "files_changed": parse_section(text, "Files Changed"),
            "commits": parse_section(text, "Commits"),
            "decisions": parse_section(text, "Decisions"),
            "problems": parse_section(text, "Problems and Solutions"),
            "next_steps": parse_section(text, "Next Steps"),
            "duration": "",
            "raw_markdown": text,
        }
        entries.append(base_entry)

        # Parse sub-sessions
        for i in range(1, len(session_splits), 2):
            sub_header = session_splits[i]
            sub_body = session_splits[i + 1] if i + 1 < len(session_splits) else ""
            sub_text = sub_header + "\n" + sub_body

            sub_entry = {
                "project": project,
                "date": date,
                "accomplished": parse_section(sub_text, "Accomplished"),
                "files_changed": parse_section(sub_text, "Files Changed"),
                "commits": "",
                "decisions": "",
                "problems": "",
                "next_steps": "",
                "duration": "",
                "raw_markdown": "",  # Only store full markdown on the first entry
            }
            # Merge sub-session accomplishments into the base entry
            if sub_entry["accomplished"]:
                base_entry["accomplished"] += "\n" + sub_entry["accomplished"]
            if sub_entry["files_changed"]:
                base_entry["files_changed"] += "\n" + sub_entry["files_changed"]
    else:
        # Single-session file
        entries.append({
            "project": project,
            "date": date,
            "accomplished": parse_section(text, "Accomplished"),
            "files_changed": parse_section(text, "Files Changed"),
            "commits": parse_section(text, "Commits"),
            "decisions": parse_section(text, "Decisions"),
            "problems": parse_section(text, "Problems and Solutions"),
            "next_steps": parse_section(text, "Next Steps"),
            "duration": "",
            "raw_markdown": text,
        })

    return entries


def extract_insights(entries):
    """Extract insights from session decisions."""
    insights = []
    for entry in entries:
        decisions = entry.get("decisions", "")
        if not decisions:
            continue
        for line in decisions.split("\n"):
            line = line.strip().lstrip("- ")
            if line and len(line) > 10:
                insights.append({
                    "project": entry["project"],
                    "type": "decision",
                    "content": line,
                    "context": f"Session {entry['date']}",
                    "tags": entry["project"],
                })
    return insights


def migrate():
    if not DB_PATH.exists():
        print("ERROR: Database not found. Run 'python db/memstack-db.py init' first.")
        sys.exit(1)

    conn = get_db()
    imported_sessions = 0
    imported_insights = 0
    skipped = 0

    # Process session files
    if SESSIONS_DIR.exists():
        for md_file in sorted(SESSIONS_DIR.glob("*.md")):
            if md_file.name in ("session-format.md", "main-memory-format.md"):
                continue

            print(f"Processing: {md_file.name}")
            entries = parse_session_file(md_file)

            for entry in entries:
                # Check for existing entry (same project + date)
                existing = conn.execute(
                    "SELECT id FROM sessions WHERE project = ? AND date = ?",
                    (entry["project"], entry["date"]),
                ).fetchone()

                if existing:
                    print(f"  EXISTS: {entry['project']} {entry['date']} (id={existing['id']})")
                    skipped += 1
                    continue

                conn.execute(
                    """INSERT INTO sessions (project, date, accomplished, files_changed,
                       commits, decisions, problems, next_steps, duration, raw_markdown)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        entry["project"],
                        entry["date"],
                        entry["accomplished"],
                        entry["files_changed"],
                        entry["commits"],
                        entry["decisions"],
                        entry["problems"],
                        entry["next_steps"],
                        entry["duration"],
                        entry["raw_markdown"],
                    ),
                )
                imported_sessions += 1

                # Extract and import insights from decisions
                for insight in extract_insights([entry]):
                    conn.execute(
                        """INSERT INTO insights (project, type, content, context, tags)
                           VALUES (?, ?, ?, ?, ?)""",
                        (
                            insight["project"],
                            insight["type"],
                            insight["content"],
                            insight["context"],
                            insight["tags"],
                        ),
                    )
                    imported_insights += 1

    # Process archive too
    if ARCHIVE_DIR.exists():
        for md_file in sorted(ARCHIVE_DIR.glob("*.md")):
            print(f"Processing archive: {md_file.name}")
            entries = parse_session_file(md_file)
            for entry in entries:
                existing = conn.execute(
                    "SELECT id FROM sessions WHERE project = ? AND date = ?",
                    (entry["project"], entry["date"]),
                ).fetchone()
                if existing:
                    skipped += 1
                    continue
                conn.execute(
                    """INSERT INTO sessions (project, date, accomplished, files_changed,
                       commits, decisions, problems, next_steps, duration, raw_markdown)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        entry["project"],
                        entry["date"],
                        entry["accomplished"],
                        entry["files_changed"],
                        entry["commits"],
                        entry["decisions"],
                        entry["problems"],
                        entry["next_steps"],
                        entry["duration"],
                        entry["raw_markdown"],
                    ),
                )
                imported_sessions += 1

                # Extract and import insights from archived sessions
                for insight in extract_insights([entry]):
                    conn.execute(
                        """INSERT INTO insights (project, type, content, context, tags)
                           VALUES (?, ?, ?, ?, ?)""",
                        (
                            insight["project"],
                            insight["type"],
                            insight["content"],
                            insight["context"],
                            insight["tags"],
                        ),
                    )
                    imported_insights += 1

    # Seed project context from config.json
    config_path = ROOT / "config.json"
    if config_path.exists():
        config = json.loads(config_path.read_text())
        for name, info in config.get("projects", {}).items():
            existing = conn.execute(
                "SELECT id FROM project_context WHERE project = ?", (name,)
            ).fetchone()
            if not existing:
                conn.execute(
                    """INSERT INTO project_context (project, status, updated_at)
                       VALUES (?, 'active', datetime('now'))""",
                    (name,),
                )
                print(f"  Added project context: {name}")

    conn.commit()
    conn.close()

    print(f"\nMigration complete:")
    print(f"  Sessions imported: {imported_sessions}")
    print(f"  Insights extracted: {imported_insights}")
    print(f"  Skipped (existing): {skipped}")
    print(f"  Database: {DB_PATH}")


if __name__ == "__main__":
    migrate()
