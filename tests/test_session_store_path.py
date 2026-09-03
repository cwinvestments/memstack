"""The diary session store lives in the user's home, not beside the script.

Ten copies of db/memstack-db.py exist on a working machine (the repo, the
marketplace checkout, and one per cached plugin version). While the store was
Path(__file__).parent / "memstack.db", each copy wrote to its own database and a
diary save landed wherever the copy that happened to run had been unpacked. Two
plugin-cache copies each collected a session that never reached the canonical
store, and a plugin update discards the cache directory holding it.

These tests pin the three properties that stop it recurring: the default is the
home path, an explicit override still wins, and the one-time adoption of an old
script-relative store copies rather than moves and can never overwrite a live
store. The fourth pins import-sessions as re-runnable, since a merge that
duplicated on every run would be worse than no merge at all.

Nothing here touches the real ~/.memstack/memstack.db: every test that opens a
connection sets MEMSTACK_SESSION_DB to a tmp_path first, and the one test that
asserts the real default is a pure path comparison that performs no IO.
"""

import importlib.util
import sqlite3
from pathlib import Path
from types import SimpleNamespace

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "db" / "memstack-db.py"
_spec = importlib.util.spec_from_file_location("memstack_db_cli", MODULE_PATH)
mdb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mdb)

SCHEMA_SQL = (Path(__file__).resolve().parents[1] / "db" / "schema.sql").read_text(
    encoding="utf-8"
)


def _make_store(path, sessions=(), insights=()):
    """Create a schema-complete store holding the supplied rows."""
    conn = sqlite3.connect(str(path))
    conn.executescript(SCHEMA_SQL)
    for project, date, accomplished, created_at in sessions:
        conn.execute(
            "INSERT INTO sessions (project, date, accomplished, created_at) "
            "VALUES (?, ?, ?, ?)",
            (project, date, accomplished, created_at),
        )
    for project, type_value, content, created_at in insights:
        conn.execute(
            "INSERT INTO insights (project, type, content, created_at) "
            "VALUES (?, ?, ?, ?)",
            (project, type_value, content, created_at),
        )
    conn.commit()
    conn.close()


def _sessions_in(path):
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    try:
        return conn.execute(
            "SELECT project, date, accomplished FROM sessions ORDER BY id"
        ).fetchall()
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# 1. The default is the home path
# ---------------------------------------------------------------------------

def test_default_store_is_in_the_user_home(monkeypatch):
    """With no override set, the store resolves under the user's home."""
    monkeypatch.delenv(mdb.DB_PATH_ENV, raising=False)
    assert mdb.resolve_db_path() == Path.home() / ".memstack" / "memstack.db"


def test_default_store_is_not_beside_the_script(monkeypatch):
    """The regression itself: the store must not sit next to this script copy."""
    monkeypatch.delenv(mdb.DB_PATH_ENV, raising=False)
    beside_script = MODULE_PATH.parent / "memstack.db"
    assert mdb.resolve_db_path() != beside_script
    assert mdb.LEGACY_DB_PATH == beside_script


# ---------------------------------------------------------------------------
# 2. An explicit override wins
# ---------------------------------------------------------------------------

def test_override_wins(tmp_path, monkeypatch):
    target = tmp_path / "elsewhere" / "memstack.db"
    monkeypatch.setenv(mdb.DB_PATH_ENV, str(target))
    assert mdb.resolve_db_path() == target


def test_override_is_read_at_call_time(tmp_path, monkeypatch):
    """Resolution happens per call, so a test can redirect an already-imported module."""
    first = tmp_path / "one.db"
    second = tmp_path / "two.db"
    monkeypatch.setenv(mdb.DB_PATH_ENV, str(first))
    assert mdb.resolve_db_path() == first
    monkeypatch.setenv(mdb.DB_PATH_ENV, str(second))
    assert mdb.resolve_db_path() == second


def test_override_is_not_the_loader_env_var(tmp_path, monkeypatch):
    """MEMSTACK_DB_PATH already means the loader's memory.db and must not redirect this."""
    monkeypatch.delenv(mdb.DB_PATH_ENV, raising=False)
    monkeypatch.setenv("MEMSTACK_DB_PATH", str(tmp_path / "wrong.db"))
    assert mdb.resolve_db_path() == Path.home() / ".memstack" / "memstack.db"


# ---------------------------------------------------------------------------
# 3. The one-time adoption copies, happens once, and never overwrites
# ---------------------------------------------------------------------------

def test_first_run_copies_legacy_store_and_leaves_source_in_place(
    tmp_path, monkeypatch, capsys
):
    legacy = tmp_path / "legacy" / "memstack.db"
    legacy.parent.mkdir()
    _make_store(legacy, sessions=[("proj-a", "2026-09-02", "carried across", "2026-09-02 21:42:29")])

    home = tmp_path / "home" / "memstack.db"
    monkeypatch.setenv(mdb.DB_PATH_ENV, str(home))
    monkeypatch.setattr(mdb, "LEGACY_DB_PATH", legacy)

    conn = mdb.get_db()
    conn.close()

    assert home.exists(), "the adopted store should exist at the home path"
    assert _sessions_in(home) == [("proj-a", "2026-09-02", "carried across")]
    # Copy, never move.
    assert legacy.exists(), "the source must be left exactly where it was"
    assert _sessions_in(legacy) == [("proj-a", "2026-09-02", "carried across")]

    assert "copied existing store" in capsys.readouterr().err


def test_adoption_happens_exactly_once(tmp_path, monkeypatch, capsys):
    """A second run must not re-copy, which would silently discard newer rows."""
    legacy = tmp_path / "legacy" / "memstack.db"
    legacy.parent.mkdir()
    _make_store(legacy, sessions=[("proj-a", "2026-09-02", "original", "2026-09-02 21:42:29")])

    home = tmp_path / "home" / "memstack.db"
    monkeypatch.setenv(mdb.DB_PATH_ENV, str(home))
    monkeypatch.setattr(mdb, "LEGACY_DB_PATH", legacy)

    mdb.get_db().close()
    capsys.readouterr()

    # A row written after adoption stands in for all later work.
    conn = sqlite3.connect(str(home))
    conn.execute(
        "INSERT INTO sessions (project, date, accomplished, created_at) "
        "VALUES (?, ?, ?, ?)",
        ("proj-b", "2026-09-03", "written after adoption", "2026-09-03 09:00:00"),
    )
    conn.commit()
    conn.close()

    mdb.get_db().close()

    rows = _sessions_in(home)
    assert ("proj-b", "2026-09-03", "written after adoption") in rows, (
        "a second adoption would have overwritten the post-adoption row"
    )
    assert len(rows) == 2
    assert "copied existing store" not in capsys.readouterr().err


def test_adoption_never_overwrites_an_existing_home_store(tmp_path, monkeypatch, capsys):
    """If a home store already exists, the legacy file is left entirely alone."""
    legacy = tmp_path / "legacy" / "memstack.db"
    legacy.parent.mkdir()
    _make_store(legacy, sessions=[("legacy-proj", "2026-01-01", "must not appear", "2026-01-01 00:00:00")])

    home = tmp_path / "home" / "memstack.db"
    home.parent.mkdir()
    _make_store(home, sessions=[("home-proj", "2026-09-03", "the live store", "2026-09-03 10:00:00")])

    monkeypatch.setenv(mdb.DB_PATH_ENV, str(home))
    monkeypatch.setattr(mdb, "LEGACY_DB_PATH", legacy)

    mdb.get_db().close()

    assert _sessions_in(home) == [("home-proj", "2026-09-03", "the live store")]
    assert "copied existing store" not in capsys.readouterr().err


def test_every_command_reports_the_store_path_on_stderr(tmp_path, monkeypatch, capsys):
    home = tmp_path / "home" / "memstack.db"
    monkeypatch.setenv(mdb.DB_PATH_ENV, str(home))
    monkeypatch.setattr(mdb, "LEGACY_DB_PATH", tmp_path / "absent" / "memstack.db")

    mdb.get_db().close()

    assert str(home) in capsys.readouterr().err


# ---------------------------------------------------------------------------
# 4. import-sessions is re-runnable
# ---------------------------------------------------------------------------

def _import(source, capsys):
    mdb.cmd_import_sessions(SimpleNamespace(path=str(source)))
    import json
    return json.loads(capsys.readouterr().out)


def test_import_sessions_imports_then_dedupes_on_a_second_run(
    tmp_path, monkeypatch, capsys
):
    source = tmp_path / "stray" / "memstack.db"
    source.parent.mkdir()
    _make_store(
        source,
        sessions=[
            ("memstack-skill-loader", "2026-09-02", "stray one", "2026-09-02 21:42:29"),
            ("parceltoplan", "2026-09-03", "stray two", "2026-09-03 08:00:00"),
        ],
        insights=[("memstack-skill-loader", "gotcha", "an insight", "2026-09-02 21:42:30")],
    )

    home = tmp_path / "home" / "memstack.db"
    monkeypatch.setenv(mdb.DB_PATH_ENV, str(home))
    monkeypatch.setattr(mdb, "LEGACY_DB_PATH", tmp_path / "absent" / "memstack.db")

    first = _import(source, capsys)
    assert first["ok"] is True
    assert first["tables"]["sessions"] == {"imported": 2, "skipped": 0}
    assert first["tables"]["insights"] == {"imported": 1, "skipped": 0}

    second = _import(source, capsys)
    assert second["tables"]["sessions"] == {"imported": 0, "skipped": 2}
    assert second["tables"]["insights"] == {"imported": 0, "skipped": 1}

    assert len(_sessions_in(home)) == 2, "a re-run must not duplicate rows"


def test_import_sessions_assigns_fresh_ids_and_never_touches_the_source(
    tmp_path, monkeypatch, capsys
):
    """Two stores whose sequences both start at 1 must merge without collision."""
    source = tmp_path / "stray" / "memstack.db"
    source.parent.mkdir()
    _make_store(source, sessions=[("parceltoplan", "2026-09-03", "id one here", "2026-09-03 08:00:00")])

    home = tmp_path / "home" / "memstack.db"
    home.parent.mkdir()
    _make_store(home, sessions=[("memstack", "2026-09-03", "also id one", "2026-09-03 07:00:00")])

    monkeypatch.setenv(mdb.DB_PATH_ENV, str(home))
    monkeypatch.setattr(mdb, "LEGACY_DB_PATH", tmp_path / "absent" / "memstack.db")

    result = _import(source, capsys)
    assert result["tables"]["sessions"] == {"imported": 1, "skipped": 0}

    conn = sqlite3.connect(f"file:{home}?mode=ro", uri=True)
    try:
        ids = [r[0] for r in conn.execute("SELECT id FROM sessions ORDER BY id")]
    finally:
        conn.close()
    assert ids == [1, 2], "the imported row should take a fresh id, not collide"

    # The source is opened read-only and must be untouched.
    assert source.exists()
    assert _sessions_in(source) == [("parceltoplan", "2026-09-03", "id one here")]


def test_import_sessions_refuses_a_missing_source(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv(mdb.DB_PATH_ENV, str(tmp_path / "home" / "memstack.db"))
    monkeypatch.setattr(mdb, "LEGACY_DB_PATH", tmp_path / "absent" / "memstack.db")
    with pytest.raises(SystemExit):
        mdb.cmd_import_sessions(SimpleNamespace(path=str(tmp_path / "nope.db")))
