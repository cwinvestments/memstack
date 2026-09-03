#!/usr/bin/env python
"""
MemStack SQLite Memory Backend: CLI Helper
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
    import-sessions <path>        Merge another memstack.db into this store
    stats                         Show database statistics

Store location:
    The store is ~/.memstack/memstack.db, NOT a file beside this script.
    Set MEMSTACK_SESSION_DB to point somewhere else. Every command prints the
    path it used on stderr, so a caller can always confirm where it wrote.
"""

import argparse
import json
import os
import sqlite3
import sys
from pathlib import Path, PureWindowsPath

DB_DIR = Path(__file__).parent
SCHEMA_PATH = DB_DIR / "schema.sql"

# The session store deliberately does NOT live beside this script.
#
# Ten copies of this file exist on a working machine: the repo, the marketplace
# checkout, and one per cached plugin version. A script-relative store meant
# each copy wrote to its own database, so a diary save landed wherever the copy
# that happened to run had been unpacked. Two plugin-cache copies each collected
# a single stray session that never reached the canonical store, and a plugin
# update discards the cache directory holding it.
#
# The store is therefore keyed to the user, not to the script.
LEGACY_DB_PATH = DB_DIR / "memstack.db"
DEFAULT_DB_PATH = Path.home() / ".memstack" / "memstack.db"
DB_PATH = DEFAULT_DB_PATH

#: Environment override for the session store. Deliberately NOT MEMSTACK_DB_PATH,
#: which already names the skill-loader's memory.db and is read by
#: bridge_to_loader() to decide whether the insight bridge is safe to run.
DB_PATH_ENV = "MEMSTACK_SESSION_DB"


def resolve_db_path() -> Path:
    """Resolve the store path at call time, so an override applies per process."""
    override = os.environ.get(DB_PATH_ENV)
    return Path(override) if override else DEFAULT_DB_PATH


def parse_json_arg(raw: str) -> dict:
    """Parse JSON input with a clean error on failure.

    The literal argument ``-`` means "read the payload from stdin" rather than
    from the command line, following the usual Unix convention. Callers should
    prefer it for anything containing prose: on Windows, cmd.exe parses a ``>``
    in an argument as redirection and silently creates a 0-byte file named
    after the token that follows it. A payload delivered on stdin is never seen
    by the shell's parser, so its content cannot be interpreted as an operator.

    ``-`` cannot collide with real input: it is not valid JSON, so any argument
    that parses today keeps working unchanged.
    """
    if raw == "-":
        try:
            raw = sys.stdin.buffer.read().decode("utf-8-sig")
        except (UnicodeDecodeError, OSError) as e:
            print(json.dumps({
                "ok": False,
                "error": f"Invalid JSON input: could not read stdin as UTF-8: {e}",
            }))
            sys.exit(1)
        if not raw.strip():
            print(json.dumps({
                "ok": False,
                "error": "Invalid JSON input: stdin was empty (expected a JSON payload)",
            }))
            sys.exit(1)
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


CANONICAL_TYPES = frozenset(
    {"gotcha", "lesson", "pattern", "warning", "failed_approach", "decision", "architecture"}
)

# Variant spellings seen in real data, mapped to a canonical type. Canonicals map to
# themselves; anything not listed passes through unchanged.
TYPE_ALIASES = {t: t for t in CANONICAL_TYPES}
TYPE_ALIASES.update(
    {
        "bug": "gotcha",
        "bugfix": "gotcha",
        "bug-fix": "gotcha",
        "distribution-bug": "gotcha",
        "debugging": "gotcha",
        "prevention": "warning",
        "correction": "gotcha",
    }
)


def normalize_type(value: str) -> str:
    """Map a type variant to its canonical form; unknown types pass through unchanged."""
    if value is None:
        return "decision"
    stripped = str(value).strip()
    if not stripped:
        return "decision"
    return TYPE_ALIASES.get(stripped.lower(), stripped)


# Procedural insight types that mirror into the skill-loader's searchable memory.
# architecture and decision are record, not procedure: bridging 1,000+ decisions
# would drown FTS retrieval, so they are deliberately excluded.
BRIDGED_TYPES = frozenset({"gotcha", "lesson", "pattern", "warning", "failed_approach"})


def _known_project_dirs(memory_db, project) -> list:
    """Directories the loader's store already associates with ``project``.

    Prefers find_project_dirs_by_name, which distinguishes "never seen" (0) from
    "collides with another project" (2+). Older loaders only have
    resolve_project_dir_by_name, which collapses both to None, there we fall
    back and simply cannot report ambiguity, which is no worse than before.
    """
    finder = getattr(memory_db, "find_project_dirs_by_name", None)
    if finder is not None:
        return list(finder(project))
    single = memory_db.resolve_project_dir_by_name(project)
    return [single] if single else []


def resolve_project_dir(memory_db, project) -> dict:
    """Decide which project_dir an insight belongs to, or why it cannot bridge.

    Returns {"project_dir": path} on success (plus "autoregistered": path when
    the project is entering the store for the first time), or {"reason": str}
    describing exactly which of the three failure modes applied.

    Auto-registration is deliberately gated on the CURRENT WORKING DIRECTORY
    agreeing with the supplied name. The diary invokes this script from the
    project root, so cwd is the project, but a name that does NOT match cwd is
    almost always an ad-hoc label ("general", "test", "SnowTrack+LawnTrack")
    rather than a real repo, and registering those would pollute cross-project
    recall permanently. Requiring corroboration from the filesystem the process
    is actually running in means a project cannot be typo'd into existence.
    """
    known = _known_project_dirs(memory_db, project)
    if len(known) == 1:
        return {"project_dir": known[0]}
    if len(known) > 1:
        return {
            "reason": "ambiguous project {!r}: {} known paths ({}): refusing "
                      "to guess".format(project, len(known), ", ".join(known))
        }

    name = (project or "").strip()
    if not name:
        return {"reason": "unknown project: no project name supplied"}

    try:
        cwd = os.getcwd()
    except OSError as exc:
        return {"reason": f"unknown project {name!r}: cwd unavailable ({exc})"}

    canonical = getattr(memory_db, "canonical_project_dir", None)
    cwd = canonical(cwd) if canonical else cwd
    cwd_name = PureWindowsPath(cwd).name

    if cwd_name.lower() != name.lower():
        return {
            "reason": "unrecognized project {!r}: not in the memory store, and "
                      "cwd basename is {!r}: not auto-registering".format(name, cwd_name)
        }
    return {"project_dir": cwd, "autoregistered": cwd}


def bridge_to_loader(project, type_value, content, context, tags, created_at) -> dict:
    """Mirror a procedural insight into the skill-loader's memory.db; never raises."""
    try:
        # 1. Procedural filter: only the five procedure types bridge.
        if type_value not in BRIDGED_TYPES:
            return {}
        # 2. A redirected loader DB would auto-create and silently diverge. Skip.
        if os.environ.get("MEMSTACK_DB_PATH"):
            return {"bridge_skipped": "MEMSTACK_DB_PATH is set"}
        # 3. Guarded import: a machine without the loader is a no-op, not an error.
        try:
            from memstack_skill_loader import memory_db
        except Exception:
            return {}
        # 4. Resolve the name against paths the store already knows.
        #
        # A name can fail for three different reasons, and they are NOT
        # interchangeable, reporting all of them as "unknown project" sent a
        # real investigation looking for a missing registration when the actual
        # fault was a duplicate. Report each honestly, and auto-register only
        # the one case where the filesystem corroborates the name.
        resolution = resolve_project_dir(memory_db, project)
        project_dir = resolution.get("project_dir")
        if project_dir is None:
            return {"bridge_skipped": resolution["reason"]}
        autoregistered = resolution.get("autoregistered")

        # 5. Derive a title (procedural_memory.title is NOT NULL; insights has none).
        text = content or ""
        idx = text.find(". ")
        if idx != -1 and idx < 120:
            title = text[:idx]
        else:
            title = text[:90]
        title = title.strip()
        if title.endswith("."):
            title = title[:-1]
        title = " ".join(title.split())
        if len(title) > 90:
            cut = title[:90]
            if " " in cut:
                cut = cut[:cut.rfind(" ")]
            title = cut.rstrip() + "..."
        if not title:
            title = text[:60]

        # 6. Content: append operative context (procedural_memory has no context col).
        body = content or ""
        if context and context.strip():
            body = body + "\n\nContext: " + context.strip()

        # 7. Tags: comma-separated string -> ordered unique list; empty -> None.
        tag_list = []
        for tag in (tags or "").split(","):
            tag = tag.strip()
            if tag and tag not in tag_list:
                tag_list.append(tag)
        stack_tags = tag_list or None

        # 8-9. created_at passed through verbatim (keyword-only). None -> failure.
        lesson_id = memory_db.insert_lesson(
            title,
            body,
            type_value,
            project_dir=project_dir,
            stack_tags=stack_tags,
            created_at=created_at,
        )
        if lesson_id is None:
            return {"bridge_failed": True}
        result = {"bridged": {"project_dir": project_dir, "lesson_id": lesson_id}}
        if autoregistered:
            # Surface it: the project just entered cross-project memory for the
            # first time, and a wrong path here is worth noticing immediately.
            result["project_autoregistered"] = autoregistered
        return result
    except Exception as exc:  # 10. Never raise into the diary save.
        return {"bridge_error": str(exc)}


def _adopt_legacy_store(db_path: Path) -> None:
    """One time only: adopt a store an older version left beside this script.

    Copies, never moves. The source stays exactly where it is, so rolling back
    to an earlier plugin version still finds its data and nothing is destroyed
    if this copy turns out to be the wrong one. Returns silently when the
    destination already exists, which is what makes this happen exactly once
    and keeps it from ever overwriting a live store.

    The copy goes through SQLite's own backup API rather than a file copy: the
    store runs in WAL mode, so committed transactions can still be sitting in a
    sidecar -wal file that a plain file copy would leave behind.
    """
    if db_path.exists():
        return
    legacy = LEGACY_DB_PATH
    if not legacy.is_file():
        return
    try:
        if legacy.resolve() == db_path.resolve():
            return
    except OSError:
        return
    src = sqlite3.connect(f"file:{legacy}?mode=ro", uri=True)
    try:
        dst = sqlite3.connect(str(db_path))
        try:
            with dst:
                src.backup(dst)
        finally:
            dst.close()
    finally:
        src.close()
    print(
        f"memstack-db: copied existing store from {legacy} to {db_path} "
        "(one time; the source was left in place)",
        file=sys.stderr,
    )


def get_db():
    """Get database connection, initializing schema if needed."""
    db_path = resolve_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    _adopt_legacy_store(db_path)
    is_new = not db_path.exists()
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("PRAGMA foreign_keys = ON")
    if is_new:
        conn.executescript(SCHEMA_PATH.read_text())
    print(f"memstack-db: store {db_path}", file=sys.stderr)
    return conn


def cmd_init(_args):
    """Initialize or re-apply schema."""
    conn = get_db()
    conn.executescript(SCHEMA_PATH.read_text())
    conn.close()
    print(json.dumps({"ok": True, "db": str(resolve_db_path())}))


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
    raw_type = data.get("type")
    type_value = normalize_type(raw_type)
    conn = get_db()
    conn.execute(
        """INSERT INTO insights (project, type, content, context, tags)
           VALUES (:project, :type, :content, :context, :tags)""",
        {
            "project": data.get("project"),
            "type": type_value,
            "content": data["content"],
            "context": data.get("context", ""),
            "tags": data.get("tags", ""),
        },
    )
    conn.commit()
    row_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    # Read the stored timestamp back so the bridge mirrors the ACTUAL created_at.
    created_at = conn.execute(
        "SELECT created_at FROM insights WHERE id = ?", (row_id,)
    ).fetchone()[0]
    conn.close()
    response = {"ok": True, "id": row_id}
    if raw_type is not None and str(raw_type).strip():
        if type_value in CANONICAL_TYPES:
            if type_value != str(raw_type).strip().lower():
                response["type_normalized"] = f"{raw_type} -> {type_value}"
        else:
            response["type_unknown"] = type_value
    # Dual-write procedural insights into the skill-loader's searchable memory.
    # memstack.db is already committed and closed; the bridge is guarded and
    # never raises, so a failure here cannot disturb the diary save.
    response.update(
        bridge_to_loader(
            data.get("project"),
            type_value,
            data["content"],
            data.get("context", ""),
            data.get("tags", ""),
            created_at,
        )
    )
    print(json.dumps(response))


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
    lines = [f"# Memory Export: {args.project}\n"]

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
        if ctx["current_branch"]:
            lines.append(f"- **Current Branch:** {ctx['current_branch']}")
        if ctx["architecture_decisions"]:
            lines.append(f"- **Architecture Decisions:**\n{ctx['architecture_decisions']}")
        if ctx["known_issues"]:
            lines.append(f"- **Known Issues:**\n{ctx['known_issues']}")
        if ctx["backlog"]:
            lines.append(f"- **Backlog:**\n{ctx['backlog']}")

    conn.close()
    print("\n".join(lines))


# Tables import-sessions merges, as (table, columns to carry, dedupe key).
#
# "id" is absent from every column list on purpose: rows are inserted with fresh
# ids so that two stores which both start their sequence at 1 can be merged
# without collision. created_at IS carried, because it is half of what identifies
# a row as one already seen.
IMPORT_TABLES = (
    (
        "sessions",
        ("project", "date", "accomplished", "files_changed", "commits", "decisions",
         "problems", "next_steps", "duration", "raw_markdown", "created_at"),
        ("created_at", "project", "accomplished"),
    ),
    (
        "insights",
        ("project", "type", "content", "context", "tags", "created_at"),
        ("created_at", "project", "content"),
    ),
    (
        # project_context is UNIQUE(project), so the row identity IS the project.
        "project_context",
        ("project", "status", "current_branch", "last_session_date",
         "architecture_decisions", "known_issues", "backlog", "updated_at"),
        ("project",),
    ),
    (
        # plans is UNIQUE(project, task_number), likewise.
        "plans",
        ("project", "task_number", "description", "status", "blocked_reason",
         "created_at", "updated_at"),
        ("project", "task_number"),
    ),
)


def cmd_import_sessions(args):
    """Merge another memstack.db into this store, skipping rows already present.

    The source is opened read-only and is never written to, moved or deleted.
    """
    source = Path(args.path)
    if not source.is_file():
        print(json.dumps({"ok": False, "error": f"Source database not found: {source}"}))
        sys.exit(1)

    dest = get_db()
    if source.resolve() == resolve_db_path().resolve():
        dest.close()
        print(json.dumps({"ok": False, "error": "Source and destination are the same file"}))
        sys.exit(1)
    try:
        src = sqlite3.connect(f"file:{source}?mode=ro", uri=True)
    except sqlite3.Error as exc:
        dest.close()
        print(json.dumps({"ok": False, "error": f"Cannot open source read-only: {exc}"}))
        sys.exit(1)
    src.row_factory = sqlite3.Row

    src_tables = {r[0] for r in src.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table'")}

    report = {}
    try:
        for table, columns, key_cols in IMPORT_TABLES:
            if table not in src_tables:
                report[table] = {"imported": 0, "skipped": 0, "note": "absent in source"}
                continue
            imported = 0
            skipped = 0
            # IFNULL on both sides so that two NULLs compare equal: SQL's NULL
            # would otherwise make a row with a null project never match itself
            # and import again on every run.
            where = " AND ".join(f"IFNULL({c}, '') = IFNULL(?, '')" for c in key_cols)
            insert_sql = "INSERT INTO {} ({}) VALUES ({})".format(
                table, ", ".join(columns), ", ".join("?" for _ in columns))
            for row in src.execute(f"SELECT * FROM {table}"):
                present = set(row.keys())
                key_vals = [row[c] if c in present else None for c in key_cols]
                if dest.execute(
                    f"SELECT 1 FROM {table} WHERE {where} LIMIT 1", key_vals
                ).fetchone():
                    skipped += 1
                    continue
                dest.execute(insert_sql,
                             [row[c] if c in present else None for c in columns])
                imported += 1
            report[table] = {"imported": imported, "skipped": skipped}
        dest.commit()
    finally:
        src.close()
        dest.close()

    print(json.dumps({
        "ok": True,
        "source": str(source),
        "destination": str(resolve_db_path()),
        "tables": report,
        "imported_total": sum(t["imported"] for t in report.values()),
        "skipped_total": sum(t["skipped"] for t in report.values()),
    }))


def cmd_stats(_args):
    """Show database statistics."""
    db_path = resolve_db_path()
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
        "db_path": str(db_path),
        "db_size_kb": round(db_path.stat().st_size / 1024, 1) if db_path.exists() else 0,
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

    p = sub.add_parser("import-sessions")
    p.add_argument("path")

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
        "import-sessions": cmd_import_sessions,
        "stats": cmd_stats,
    }
    cmd_map[args.command](args)


if __name__ == "__main__":
    main()
