"""add-insight stores the lesson link; correct-insight and delete-insight reach every copy.

An insight bridged by add-insight has three copies: the insights row here, the
lesson in the skill-loader's procedural_memory, and that lesson's memory_fts
entry. These tests drive the real CLI commands end to end against tmp stores,
with the real loader package doing the memory.db side.

Isolation: MEMSTACK_SESSION_DB points the insight store at a tmp file, and the
loader's module default DB_PATH is patched to a tmp file with MEMSTACK_DB_PATH
UNSET, because the bridge (correctly) refuses to run under that override. Each
test asserts both paths are tmp before it writes anything.
"""

import argparse
import importlib.util
import json
import sqlite3
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "db" / "memstack-db.py"
_spec = importlib.util.spec_from_file_location("memstack_db_cli_link", MODULE_PATH)
mdb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mdb)

memory_db = pytest.importorskip("memstack_skill_loader.memory_db")
isy = pytest.importorskip("memstack_skill_loader.insight_sync")


@pytest.fixture
def stores(tmp_path, monkeypatch):
    sess = tmp_path / "memstack.db"
    mem = tmp_path / "memory.db"
    monkeypatch.setenv("MEMSTACK_SESSION_DB", str(sess))
    # A fresh store would otherwise adopt the repo's legacy db/memstack.db.
    monkeypatch.setattr(mdb, "LEGACY_DB_PATH", tmp_path / "no-legacy.db")
    monkeypatch.delenv("MEMSTACK_DB_PATH", raising=False)
    monkeypatch.setattr(memory_db, "DB_PATH", mem)
    proj = tmp_path / "zzproj"
    proj.mkdir()
    monkeypatch.chdir(proj)  # cwd corroborates the name, so the bridge resolves it
    assert mdb.resolve_db_path() == sess
    assert memory_db._resolve_db_path() == mem
    return {"sess": sess, "mem": mem}


def run(capsys, func, **kw):
    func(argparse.Namespace(**kw))
    return json.loads(capsys.readouterr().out)


def add(capsys, content, type_="gotcha", **extra):
    payload = {"project": "zzproj", "type": type_, "content": content, **extra}
    return run(capsys, mdb.cmd_add_insight, json=json.dumps(payload))


def correct(capsys, **payload):
    return run(capsys, mdb.cmd_correct_insight, json=json.dumps(payload))


def q(path, sql, args=()):
    conn = sqlite3.connect(path)
    try:
        return conn.execute(sql, args).fetchall()
    finally:
        conn.close()


def fts(stores, lid):
    return [r[0] for r in q(stores["mem"],
                            "SELECT content FROM memory_fts WHERE source_table = "
                            "'procedural_memory' AND source_id = ?", (str(lid),))]


def search_ids(term):
    return [r["source_id"] for r in memory_db.search_memory(term, project_dir=None)
            if r["source_table"] == "procedural_memory"]


# ---------------------------------------------------------------------------

@pytest.mark.parametrize("content,context,tags", [
    ("Short.", "", ""),
    ("First sentence. Second sentence.", "ctx", "a, b,a"),
    ("x" * 300, "  padded  ", ",,"),
    ("A" * 130 + ". tail", None, None),
    ("word " * 40, "", "python"),
    ("Ends with dot.", "", ""),
    ("", "", ""),
    ("   \n\t  ", "c", "t"),
])
def test_derivation_matches_the_loader(content, context, tags):
    assert mdb.derive_lesson_title(content) == isy.derive_title(content)
    assert mdb.derive_lesson_body(content, context) == isy.derive_body(content, context)
    assert mdb.derive_lesson_tags(tags) == isy.derive_tags(tags)
    assert mdb.BRIDGED_TYPES == isy.BRIDGED_TYPES


def test_add_insight_stores_the_lesson_link(stores, capsys):
    out = add(capsys, "Bridged gotcha about ocelots.", context="why")
    lid = out["bridged"]["lesson_id"]
    assert q(stores["sess"], "SELECT lesson_id FROM insights WHERE id = ?",
             (out["id"],)) == [(lid,)]
    dec = add(capsys, "Not bridged", type_="decision")
    assert "bridged" not in dec
    assert q(stores["sess"], "SELECT lesson_id FROM insights WHERE id = ?",
             (dec["id"],)) == [(None,)]


def test_correct_insight_changes_all_three_copies(stores, capsys):
    out = add(capsys, "Margays climb down headfirst. Detail.", context="zoo")
    iid, lid = out["id"], out["bridged"]["lesson_id"]
    assert search_ids("Margays") == [str(lid)]
    res = correct(capsys, id=iid, content="Kinkajous hang by the tail. Detail.")
    assert res["ok"] and res["lesson"]["action"] == "updated"
    assert q(stores["sess"], "SELECT content, context FROM insights WHERE id = ?",
             (iid,)) == [("Kinkajous hang by the tail. Detail.", "zoo")]
    title, body = q(stores["mem"], "SELECT title, content FROM procedural_memory "
                    "WHERE id = ?", (lid,))[0]
    assert title == "Kinkajous hang by the tail"
    assert body == "Kinkajous hang by the tail. Detail.\n\nContext: zoo"
    assert fts(stores, lid) == [f"{title} {body}"]
    assert search_ids("Kinkajous") == [str(lid)]
    assert search_ids("Margays") == []


def test_delete_insight_removes_all_three(stores, capsys):
    out = add(capsys, "Fossas hunt lemurs.")
    other = add(capsys, "Civets are not cats.")
    iid, lid = out["id"], out["bridged"]["lesson_id"]
    res = run(capsys, mdb.cmd_delete_insight, id=iid, force=False)
    assert res["lesson"] == {"action": "deleted", "lesson_id": lid}
    assert q(stores["sess"], "SELECT COUNT(*) FROM insights WHERE id = ?", (iid,)) == [(0,)]
    assert q(stores["mem"], "SELECT COUNT(*) FROM procedural_memory WHERE id = ?",
             (lid,)) == [(0,)]
    assert fts(stores, lid) == []
    assert search_ids("Fossas") == []
    # no orphan: index rows and lessons agree, and the survivor is intact
    lessons = {str(r[0]) for r in q(stores["mem"], "SELECT id FROM procedural_memory")}
    indexed = {r[0] for r in q(stores["mem"], "SELECT source_id FROM memory_fts "
                                              "WHERE source_table = 'procedural_memory'")}
    assert lessons == indexed == {str(other["bridged"]["lesson_id"])}


def test_shared_lesson_is_forked_not_rewritten(stores, capsys):
    a = add(capsys, "Identical insight about genets.")
    b = add(capsys, "Identical insight about genets.")
    lid = a["bridged"]["lesson_id"]
    assert b["bridged"]["lesson_id"] == lid  # the loader deduped
    res = correct(capsys, id=a["id"], content="Corrected insight about binturongs.")
    assert res["lesson"]["action"] == "forked"
    assert res["lesson"]["shared_with_insights"] == [b["id"]]
    new_lid = res["lesson"]["lesson_id"]
    assert q(stores["mem"], "SELECT content FROM procedural_memory WHERE id = ?",
             (lid,)) == [("Identical insight about genets.",)]
    assert q(stores["sess"], "SELECT id, lesson_id FROM insights ORDER BY id") == \
        [(a["id"], new_lid), (b["id"], lid)]
    assert search_ids("binturongs") == [str(new_lid)]
    assert search_ids("genets") == [str(lid)]


def test_without_insight_sync_every_insight_is_refused(stores, capsys, monkeypatch):
    """No local fallback: linked or not, nothing changes and the command exits 1.

    An unlinked insight is not proof of no lesson (pairs bridged before
    lesson_id existed have one), so the old row-only fallback was a silent
    half-correction. tests/test_insight_gate.py covers the real causes.
    """
    linked = add(capsys, "Linked insight.")
    plain = add(capsys, "Plain decision.", type_="decision")
    before = q(stores["sess"], "SELECT * FROM insights ORDER BY id")
    monkeypatch.setattr(mdb, "_insight_sync_module",
                        lambda: (None, "simulated: update memstack-skill-loader"))
    for iid in (linked["id"], plain["id"]):
        with pytest.raises(SystemExit) as exc:
            correct(capsys, id=iid, content="changed")
        assert exc.value.code == 1
        assert json.loads(capsys.readouterr().out)["ok"] is False
        with pytest.raises(SystemExit) as exc:
            run(capsys, mdb.cmd_delete_insight, id=iid, force=False)
        assert exc.value.code == 1
        assert json.loads(capsys.readouterr().out)["ok"] is False
    assert q(stores["sess"], "SELECT * FROM insights ORDER BY id") == before


def test_memstack_db_path_override_disables_lesson_sync(monkeypatch):
    monkeypatch.setenv("MEMSTACK_DB_PATH", "elsewhere.db")
    sync, reason = mdb._insight_sync_module()
    assert sync is None and "MEMSTACK_DB_PATH" in reason


def test_the_installed_loader_passes_the_gate():
    assert mdb._insight_sync_module() == (isy, None)


def test_unlinked_insight_still_goes_through_insight_sync(stores, capsys):
    """With insight_sync available, an unlinked insight is the loader's call."""
    plain = add(capsys, "Plain decision.", type_="decision")
    res = correct(capsys, id=plain["id"], content="Better decision.")
    assert res["ok"] and res["lesson"]["action"] == "none"
    assert q(stores["sess"], "SELECT content FROM insights WHERE id = ?",
             (plain["id"],)) == [("Better decision.",)]
    res = run(capsys, mdb.cmd_delete_insight, id=plain["id"], force=False)
    assert res["ok"]
    assert q(stores["sess"], "SELECT COUNT(*) FROM insights WHERE id = ?",
             (plain["id"],)) == [(0,)]


def test_get_db_adds_the_link_column_to_an_older_store(tmp_path, monkeypatch):
    sess = tmp_path / "old.db"
    monkeypatch.setenv("MEMSTACK_SESSION_DB", str(sess))
    monkeypatch.setattr(mdb, "LEGACY_DB_PATH", tmp_path / "no-legacy.db")
    conn = sqlite3.connect(sess)
    conn.executescript(mdb.SCHEMA_PATH.read_text()
                       .replace("    lesson_id   INTEGER                          "
                                "-- bridged lesson in the loader's memory.db\n", "")
                       .replace("created_at  TEXT    DEFAULT (datetime('now')),\n);",
                                "created_at  TEXT    DEFAULT (datetime('now'))\n);")
                       .replace("CREATE INDEX IF NOT EXISTS idx_insights_lesson      "
                                "ON insights(lesson_id);\n", ""))
    conn.execute("INSERT INTO insights (project, type, content) VALUES ('p', 'gotcha', 'x')")
    conn.commit()
    cols = [r[1] for r in conn.execute("PRAGMA table_info(insights)")]
    conn.close()
    assert "lesson_id" not in cols
    mdb.get_db().close()
    conn = sqlite3.connect(sess)
    cols = [r[1] for r in conn.execute("PRAGMA table_info(insights)")]
    rows = conn.execute("SELECT content, lesson_id FROM insights").fetchall()
    idx = [r[1] for r in conn.execute("PRAGMA index_list(insights)")]
    conn.close()
    assert "lesson_id" in cols and rows == [("x", None)]
    assert "idx_insights_lesson" in idx
    mdb.get_db().close()  # idempotent


def test_link_lessons_cli(stores, capsys):
    a = add(capsys, "Linked at write time.")
    # Simulate an insight bridged before the column existed.
    conn = sqlite3.connect(stores["sess"])
    conn.execute("UPDATE insights SET lesson_id = NULL WHERE id = ?", (a["id"],))
    conn.commit()
    conn.close()
    dry = run(capsys, mdb.cmd_link_lessons, apply=False, since=None)
    assert dry["ok"] and dry["exact"] == 1 and dry["written"] == 0
    assert q(stores["sess"], "SELECT lesson_id FROM insights") == [(None,)]
    done = run(capsys, mdb.cmd_link_lessons, apply=True, since=None)
    assert done["written"] == 1
    assert q(stores["sess"], "SELECT lesson_id FROM insights") == \
        [(a["bridged"]["lesson_id"],)]


def test_import_sessions_does_not_carry_the_link():
    cols = dict((t, c) for t, c, _ in mdb.IMPORT_TABLES)
    assert "lesson_id" not in cols["insights"]
