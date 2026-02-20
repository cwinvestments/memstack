-- MemStack v2.1 — SQLite Memory Backend
-- Replaces flat markdown files with structured, queryable storage.

PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

-- Sessions: diary entries from each CC session
CREATE TABLE IF NOT EXISTS sessions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    project     TEXT    NOT NULL,
    date        TEXT    NOT NULL,               -- YYYY-MM-DD
    accomplished TEXT,                           -- bullet list
    files_changed TEXT,                          -- bullet list
    commits     TEXT,                            -- bullet list
    decisions   TEXT,                            -- bullet list
    problems    TEXT,                            -- bullet list
    next_steps  TEXT,                            -- bullet list
    duration    TEXT,                            -- e.g. "~2 hours"
    raw_markdown TEXT,                           -- full original markdown for export
    created_at  TEXT    DEFAULT (datetime('now'))
);

-- Insights: key learnings, decisions, and patterns
CREATE TABLE IF NOT EXISTS insights (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    project     TEXT,                            -- NULL = global insight
    type        TEXT    NOT NULL DEFAULT 'decision', -- decision, pattern, bug-fix, architecture, tool
    content     TEXT    NOT NULL,
    context     TEXT,                            -- what prompted this insight
    tags        TEXT,                            -- comma-separated
    created_at  TEXT    DEFAULT (datetime('now'))
);

-- Project context: current state of each managed project
CREATE TABLE IF NOT EXISTS project_context (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    project                 TEXT    NOT NULL UNIQUE,
    status                  TEXT    DEFAULT 'active',  -- active, paused, completed
    current_branch          TEXT,
    last_session_date       TEXT,
    architecture_decisions  TEXT,
    known_issues            TEXT,
    backlog                 TEXT,
    updated_at              TEXT    DEFAULT (datetime('now'))
);

-- Plans: task lists with status tracking
CREATE TABLE IF NOT EXISTS plans (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    project     TEXT    NOT NULL,
    task_number INTEGER NOT NULL,
    description TEXT    NOT NULL,
    status      TEXT    DEFAULT 'pending',       -- pending, in_progress, completed, blocked
    blocked_reason TEXT,
    created_at  TEXT    DEFAULT (datetime('now')),
    updated_at  TEXT    DEFAULT (datetime('now')),
    UNIQUE(project, task_number)
);

-- Schema version tracking
CREATE TABLE IF NOT EXISTS schema_version (
    version     INTEGER PRIMARY KEY,
    applied_at  TEXT    DEFAULT (datetime('now'))
);

INSERT OR IGNORE INTO schema_version (version) VALUES (1);

-- Indexes for fast querying
CREATE INDEX IF NOT EXISTS idx_sessions_project     ON sessions(project);
CREATE INDEX IF NOT EXISTS idx_sessions_date        ON sessions(date);
CREATE INDEX IF NOT EXISTS idx_insights_project     ON insights(project);
CREATE INDEX IF NOT EXISTS idx_insights_type        ON insights(type);
CREATE INDEX IF NOT EXISTS idx_plans_project        ON plans(project);
CREATE INDEX IF NOT EXISTS idx_plans_status         ON plans(status);
