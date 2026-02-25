#!/usr/bin/env python
"""
MemStack SQLite Memory Backend — CLI Helper
Repository pattern: skills call this script instead of raw file I/O.

Usage:
    python db/memstack-db.py <command> [args...]

Commands:
    init                          Initialize/migrate the database
    add-session   <json>          Add a session diary entry
    add-insight   <json>          Add an insight/decision
    search        <query> [opts]  Full-text search across all tables
    get-sessions  <project> [n]   Get recent sessions for a project
    get-insights  <project>       Get insights for a project
    get-context   <project>       Get project context
    set-context   <json>          Upsert project context
    add-plan-task <json>          Add a task to a project plan
    get-plan      <project>       Get all plan tasks for a project
    update-task   <json>          Update a plan task status
    export-md     <project>       Export project memory as markdown
    stats                         Show database statistics
"""

import argparse
import json
import os
import sqlite3
import sys
from pathlib import Path

DB_DIR = Path(__file__).parent
DB_PATH = DB_DIR / "memstack.db"
SCHEMA_PATH = DB_DIR / "schema.sql"


def parse_json_arg(raw: str) -> dict:
    """Parse JSON input with a clean error on failure."""
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(json.dumps({"ok": False, "error": f"Invalid JSON input: {e}"}))
        sys.exit(1)


def require_fields(data: dict, *fields: str) -> None:
    """Validate required fields exist in data dict."""
    for f in fields:
        if f not in data or data[f] is None:
            print(json.dumps({"ok": False, "error": f"Missing required field: {f}"}))
            sys.exit(1)


def get_db():
    """Get database connection, initializing schema if needed."""
    is_new = not DB_PATH.exists()
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("PRAGMA foreign_keys = ON")
    if is_new:
        conn.executescript(SCHEMA_PATH.read_text())
    return conn


def cmd_init(_args):
    """Initialize or re-apply schema."""
    conn = get_db()
    conn.executescript(SCHEMA_PATH.read_text())
    conn.close()
    print(json.dumps({"ok": True, "db": str(DB_PATH)}))


def cmd_add_session(args):
    """Add a session diary entry."""
    data = parse_json_arg(args.json)
    require_fields(data, "project")
    conn = get_db()
    conn.execute(
        """INSERT INTO sessions (project, date, accomplished, files_changed, commits,
           decisions, problems, next_steps, duration, raw_markdown)
           VALUES (:project, :date, :accomplished, :files_changed, :commits,
           :decisions, :problems, :next_steps, :duration, :raw_markdown)""",
        {
            "project": data["project"],
            "date": data.get("date", ""),
            "accomplished": data.get("accomplished", ""),
            "files_changed": data.get("files_changed", ""),
            "commits": data.get("commits", ""),
            "decisions": data.get("decisions", ""),
            "problems": data.get("problems", ""),
            "next_steps": data.get("next_steps", ""),
            "duration": data.get("duration", ""),
            "raw_markdown": data.get("raw_markdown", ""),
        },
    )
    conn.commit()
    row_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()
    print(json.dumps({"ok": True, "id": row_id}))


def cmd_add_insight(args):
    """Add an insight or decision."""
    data = parse_json_arg(args.json)
    require_fields(data, "content")
    conn = get_db()
    conn.execute(
        """INSERT INTO insights (project, type, content, context, tags)
           VALUES (:project, :type, :content, :context, :tags)""",
        {
            "project": data.get("project"),
            "type": data.get("type", "decision"),
            "content": data["content"],
            "context": data.get("context", ""),
            "tags": data.get("tags", ""),
        },
    )
    conn.commit()
    row_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()
    print(json.dumps({"ok": True, "id": row_id}))


def cmd_search(args):
    """Full-text search across sessions, insights, and project_context."""
    query = f"%{args.query}%"
    limit = args.limit or 10
    project_filter = args.project

    conn = get_db()
    results = []

    # Search sessions
    sql = "SELECT id, project, date, accomplished, decisions, next_steps FROM sessions WHERE "
    params = []
    conditions = ["(accomplished LIKE ? OR decisions LIKE ? OR commits LIKE ? OR next_steps LIKE ? OR problems LIKE ?)"]
    params.extend([query] * 5)
    if project_filter:
        conditions.append("project = ?")
        params.append(project_filter)
    sql += " AND ".join(conditions) + " ORDER BY date DESC LIMIT ?"
    params.append(limit)

    for row in conn.execute(sql, params):
        results.append({
            "type": "session",
            "id": row["id"],
            "project": row["project"],
            "date": row["date"],
            "accomplished": (row["accomplished"] or "")[:200],
            "decisions": (row["decisions"] or "")[:200],
        })

    # Search insights
    sql = "SELECT id, project, type, content, tags FROM insights WHERE content LIKE ?"
    params = [query]
    if project_filter:
        sql += " AND project = ?"
        params.append(project_filter)
    sql += " ORDER BY created_at DESC LIMIT ?"
    params.append(limit)

    for row in conn.execute(sql, params):
        results.append({
            "type": "insight",
            "id": row["id"],
            "project": row["project"],
            "insight_type": row["type"],
            "content": row["content"][:200],
            "tags": row["tags"],
        })

    conn.close()
    print(json.dumps({"results": results, "count": len(results)}))


def cmd_get_sessions(args):
    """Get recent sessions for a project."""
    conn = get_db()
    limit = args.limit or 5
    rows = conn.execute(
        """SELECT id, project, date, accomplished, files_changed, commits,
           decisions, problems, next_steps, duration
           FROM sessions WHERE project = ? ORDER BY date DESC LIMIT ?""",
        (args.project, limit),
    ).fetchall()
    conn.close()
    sessions = [dict(r) for r in rows]
    print(json.dumps({"sessions": sessions, "count": len(sessions)}))


def cmd_get_insights(args):
    """Get insights for a project."""
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM insights WHERE project = ? OR project IS NULL ORDER BY created_at DESC",
        (args.project,),
    ).fetchall()
    conn.close()
    print(json.dumps({"insights": [dict(r) for r in rows], "count": len(rows)}))


def cmd_get_context(args):
    """Get project context."""
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM project_context WHERE project = ?", (args.project,)
    ).fetchone()
    conn.close()
    if row:
        print(json.dumps(dict(row)))
    else:
        print(json.dumps({"project": args.project, "status": "no context saved"}))


def cmd_set_context(args):
    """Upsert project context."""
    data = parse_json_arg(args.json)
    require_fields(data, "project")
    conn = get_db()
    conn.execute(
        """INSERT INTO project_context (project, status, current_branch, last_session_date,
           architecture_decisions, known_issues, backlog, updated_at)
           VALUES (:project, :status, :current_branch, :last_session_date,
           :architecture_decisions, :known_issues, :backlog, datetime('now'))
           ON CONFLICT(project) DO UPDATE SET
           status = COALESCE(:status, status),
           current_branch = COALESCE(:current_branch, current_branch),
           last_session_date = COALESCE(:last_session_date, last_session_date),
           architecture_decisions = COALESCE(:architecture_decisions, architecture_decisions),
           known_issues = COALESCE(:known_issues, known_issues),
           backlog = COALESCE(:backlog, backlog),
           updated_at = datetime('now')""",
        {
            "project": data["project"],
            "status": data.get("status"),
            "current_branch": data.get("current_branch"),
            "last_session_date": data.get("last_session_date"),
            "architecture_decisions": data.get("architecture_decisions"),
            "known_issues": data.get("known_issues"),
            "backlog": data.get("backlog"),
        },
    )
    conn.commit()
    conn.close()
    print(json.dumps({"ok": True, "project": data["project"]}))


def cmd_add_plan_task(args):
    """Add a task to a project plan."""
    data = parse_json_arg(args.json)
    require_fields(data, "project", "task_number", "description")
    conn = get_db()
    conn.execute(
        """INSERT INTO plans (project, task_number, description, status, blocked_reason)
           VALUES (:project, :task_number, :description, :status, :blocked_reason)
           ON CONFLICT(project, task_number) DO UPDATE SET
           description = :description, status = :status,
           blocked_reason = :blocked_reason, updated_at = datetime('now')""",
        {
            "project": data["project"],
            "task_number": data["task_number"],
            "description": data["description"],
            "status": data.get("status", "pending"),
            "blocked_reason": data.get("blocked_reason"),
        },
    )
    conn.commit()
    conn.close()
    print(json.dumps({"ok": True}))


def cmd_get_plan(args):
    """Get all plan tasks for a project."""
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM plans WHERE project = ? ORDER BY task_number",
        (args.project,),
    ).fetchall()
    conn.close()
    tasks = [dict(r) for r in rows]
    done = sum(1 for t in tasks if t["status"] == "completed")
    print(json.dumps({"project": args.project, "tasks": tasks, "done": done, "total": len(tasks)}))


def cmd_update_task(args):
    """Update a plan task's status."""
    data = parse_json_arg(args.json)
    require_fields(data, "project", "task_number", "status")
    conn = get_db()
    cur = conn.execute(
        """UPDATE plans SET status = :status, blocked_reason = :blocked_reason,
           updated_at = datetime('now')
           WHERE project = :project AND task_number = :task_number""",
        {
            "project": data["project"],
            "task_number": data["task_number"],
            "status": data["status"],
            "blocked_reason": data.get("blocked_reason"),
        },
    )
    conn.commit()
    conn.close()
    if cur.rowcount == 0:
        print(json.dumps({"ok": False, "error": f"Task not found: {data['project']} #{data['task_number']}"}))
    else:
        print(json.dumps({"ok": True}))


def cmd_export_md(args):
    """Export all memory for a project as markdown."""
    conn = get_db()
    lines = [f"# Memory Export — {args.project}\n"]

    # Sessions
    sessions = conn.execute(
        "SELECT * FROM sessions WHERE project = ? ORDER BY date DESC",
        (args.project,),
    ).fetchall()
    if sessions:
        lines.append("## Sessions\n")
        for s in sessions:
            lines.append(f"### {s['date']}")
            if s["accomplished"]:
                lines.append(f"**Accomplished:**\n{s['accomplished']}")
            if s["commits"]:
                lines.append(f"**Commits:**\n{s['commits']}")
            if s["decisions"]:
                lines.append(f"**Decisions:**\n{s['decisions']}")
            if s["next_steps"]:
                lines.append(f"**Next Steps:**\n{s['next_steps']}")
            lines.append("")

    # Insights
    insights = conn.execute(
        "SELECT * FROM insights WHERE project = ? ORDER BY created_at DESC",
        (args.project,),
    ).fetchall()
    if insights:
        lines.append("## Insights\n")
        for i in insights:
            lines.append(f"- **[{i['type']}]** {i['content']}")
        lines.append("")

    # Context
    ctx = conn.execute(
        "SELECT * FROM project_context WHERE project = ?", (args.project,)
    ).fetchone()
    if ctx:
        lines.append("## Project Context\n")
        lines.append(f"- **Status:** {ctx['status']}")
        if ctx["known_issues"]:
            lines.append(f"- **Known Issues:**\n{ctx['known_issues']}")
        if ctx["backlog"]:
            lines.append(f"- **Backlog:**\n{ctx['backlog']}")

    conn.close()
    print("\n".join(lines))


def cmd_stats(_args):
    """Show database statistics."""
    conn = get_db()
    sessions = conn.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
    insights = conn.execute("SELECT COUNT(*) FROM insights").fetchone()[0]
    projects = conn.execute("SELECT COUNT(*) FROM project_context").fetchone()[0]
    plans = conn.execute("SELECT COUNT(*) FROM plans").fetchone()[0]

    by_project = conn.execute(
        "SELECT project, COUNT(*) as cnt FROM sessions GROUP BY project ORDER BY cnt DESC"
    ).fetchall()

    conn.close()
    print(json.dumps({
        "sessions": sessions,
        "insights": insights,
        "projects": projects,
        "plan_tasks": plans,
        "sessions_by_project": {r["project"]: r["cnt"] for r in by_project},
        "db_path": str(DB_PATH),
        "db_size_kb": round(DB_PATH.stat().st_size / 1024, 1) if DB_PATH.exists() else 0,
    }))


def main():
    parser = argparse.ArgumentParser(description="MemStack SQLite Memory Backend")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("init")

    p = sub.add_parser("add-session")
    p.add_argument("json")

    p = sub.add_parser("add-insight")
    p.add_argument("json")

    p = sub.add_parser("search")
    p.add_argument("query")
    p.add_argument("--project", default=None)
    p.add_argument("--limit", type=int, default=10)

    p = sub.add_parser("get-sessions")
    p.add_argument("project")
    p.add_argument("--limit", type=int, default=5)

    p = sub.add_parser("get-insights")
    p.add_argument("project")

    p = sub.add_parser("get-context")
    p.add_argument("project")

    p = sub.add_parser("set-context")
    p.add_argument("json")

    p = sub.add_parser("add-plan-task")
    p.add_argument("json")

    p = sub.add_parser("get-plan")
    p.add_argument("project")

    p = sub.add_parser("update-task")
    p.add_argument("json")

    p = sub.add_parser("export-md")
    p.add_argument("project")

    sub.add_parser("stats")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    cmd_map = {
        "init": cmd_init,
        "add-session": cmd_add_session,
        "add-insight": cmd_add_insight,
        "search": cmd_search,
        "get-sessions": cmd_get_sessions,
        "get-insights": cmd_get_insights,
        "get-context": cmd_get_context,
        "set-context": cmd_set_context,
        "add-plan-task": cmd_add_plan_task,
        "get-plan": cmd_get_plan,
        "update-task": cmd_update_task,
        "export-md": cmd_export_md,
        "stats": cmd_stats,
    }
    cmd_map[args.command](args)


if __name__ == "__main__":
    main()
