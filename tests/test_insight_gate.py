"""correct-insight and delete-insight refuse outright without a safe insight_sync.

Before 3.10.5 the plugin fell back to changing an unlinked insight's row only
when the loader was missing or older than 4.21.4, printed lesson action none
and exited 0. An unlinked insight can still have a bridged lesson (pairs saved
before insights.lesson_id existed), so that left the lesson and its memory_fts
row stale: a silent half-correction. These tests pin the refusal: exit 1, a
message naming the cause and the fix, and the session store byte for byte
unchanged, not even the insight row.

Unlike tests/test_insight_link.py this file does not need the loader, so it
runs in exactly the environment the refusal protects.
"""

import argparse
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import types
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "db" / "memstack-db.py"
_spec = importlib.util.spec_from_file_location("memstack_db_cli_gate", SCRIPT)
mdb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mdb)

UPDATE_MSG = "update memstack-skill-loader to 4.21.4 or newer"


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.fixture
def store(tmp_path, monkeypatch):
    """A real session store holding one unlinked and one linked insight."""
    sess = tmp_path / "memstack.db"
    monkeypatch.setenv("MEMSTACK_SESSION_DB", str(sess))
    monkeypatch.setattr(mdb, "LEGACY_DB_PATH", tmp_path / "no-legacy.db")
    monkeypatch.delenv("MEMSTACK_DB_PATH", raising=False)
    assert mdb.resolve_db_path() == sess
    conn = mdb.get_db()
    try:
        unlinked = conn.execute(
            "INSERT INTO insights (project, type, content, context, tags) "
            "VALUES ('zzproj', 'gotcha', 'Bridged before the link existed.', 'c', 't')"
        ).lastrowid
        linked = conn.execute(
            "INSERT INTO insights (project, type, content, lesson_id) "
            "VALUES ('zzproj', 'gotcha', 'Linked insight.', 7)"
        ).lastrowid
        conn.commit()
    finally:
        conn.close()
    return {"sess": sess, "ids": (unlinked, linked), "digest": _digest(sess)}


def _fake_sync_module(calls):
    mod = types.ModuleType("memstack_skill_loader.insight_sync")

    class InsightSyncError(Exception):
        pass

    def _called(name):
        def fn(*a, **k):
            calls.append(name)
            return {"ok": True, "lesson": {"action": "none"}}
        return fn

    mod.InsightSyncError = InsightSyncError
    mod.correct_insight = _called("correct_insight")
    mod.delete_insight = _called("delete_insight")
    mod.backfill_links = _called("backfill_links")
    return mod


def _install_loader(monkeypatch, cause, calls):
    """Make the import of memstack_skill_loader behave as `cause` describes."""
    for name in list(sys.modules):
        if name == "memstack_skill_loader" or name.startswith("memstack_skill_loader."):
            monkeypatch.delitem(sys.modules, name)
    if cause == "missing":
        monkeypatch.setitem(sys.modules, "memstack_skill_loader", None)
        return
    pkg = types.ModuleType("memstack_skill_loader")
    if cause != "no-version":
        pkg.__version__ = "4.21.3"
    if cause in ("4.21.3-with-sync", "no-version"):
        # The f426663 shape: insight_sync importable on a 4.21.3 tree.
        sync = _fake_sync_module(calls)
        pkg.insight_sync = sync
        monkeypatch.setitem(sys.modules, "memstack_skill_loader.insight_sync", sync)
    monkeypatch.setitem(sys.modules, "memstack_skill_loader", pkg)
    if cause == "no-version":
        import importlib.metadata as md

        def _no_dist(name):
            raise md.PackageNotFoundError(name)
        monkeypatch.setattr(md, "version", _no_dist)


def _refused(capsys, func, **kw):
    with pytest.raises(SystemExit) as exc:
        func(argparse.Namespace(**kw))
    assert exc.value.code == 1
    out = json.loads(capsys.readouterr().out)
    assert out["ok"] is False
    return out["error"]


CAUSES = ["missing", "4.21.3-without-sync", "4.21.3-with-sync", "no-version"]


@pytest.mark.parametrize("cause", CAUSES)
def test_correct_insight_refuses_and_changes_nothing(store, capsys, monkeypatch, cause):
    calls = []
    _install_loader(monkeypatch, cause, calls)
    for iid in store["ids"]:
        err = _refused(capsys, mdb.cmd_correct_insight,
                       json=json.dumps({"id": iid, "content": "changed"}))
        assert UPDATE_MSG in err and "Nothing was changed" in err
    assert calls == []
    assert _digest(store["sess"]) == store["digest"]


@pytest.mark.parametrize("cause", CAUSES)
def test_delete_insight_refuses_and_changes_nothing(store, capsys, monkeypatch, cause):
    calls = []
    _install_loader(monkeypatch, cause, calls)
    for iid in store["ids"]:
        err = _refused(capsys, mdb.cmd_delete_insight, id=iid, force=False)
        assert UPDATE_MSG in err and "Nothing was changed" in err
    assert calls == []
    assert _digest(store["sess"]) == store["digest"]


@pytest.mark.parametrize("cause", CAUSES)
def test_link_lessons_refuses_on_an_unsafe_loader(store, capsys, monkeypatch, cause):
    calls = []
    _install_loader(monkeypatch, cause, calls)
    err = _refused(capsys, mdb.cmd_link_lessons, apply=True, since=None)
    assert UPDATE_MSG in err
    assert calls == []
    assert _digest(store["sess"]) == store["digest"]


def test_messages_name_the_found_version(monkeypatch):
    calls = []
    monkeypatch.delenv("MEMSTACK_DB_PATH", raising=False)
    _install_loader(monkeypatch, "4.21.3-with-sync", calls)
    sync, reason = mdb._insight_sync_module()
    assert sync is None and "found 4.21.3" in reason
    _install_loader(monkeypatch, "missing", calls)
    sync, reason = mdb._insight_sync_module()
    assert sync is None and "not installed" in reason


def test_memstack_db_path_override_refuses_and_changes_nothing(store, capsys, monkeypatch):
    monkeypatch.setenv("MEMSTACK_DB_PATH", str(store["sess"].parent / "elsewhere.db"))
    for iid in store["ids"]:
        err = _refused(capsys, mdb.cmd_correct_insight,
                       json=json.dumps({"id": iid, "content": "changed"}))
        assert "unset MEMSTACK_DB_PATH" in err
        err = _refused(capsys, mdb.cmd_delete_insight, id=iid, force=False)
        assert "unset MEMSTACK_DB_PATH" in err
    assert _digest(store["sess"]) == store["digest"]


@pytest.mark.parametrize("version,ok", [
    ("4.21.4", True), ("4.21.10", True), ("4.22.0", True), ("5.0.0", True),
    ("4.21.4.dev1", True), ("4.21.3", False), ("4.20.9", False), ("3.99.99", False),
    ("4.21", False), ("garbage", False),
])
def test_version_floor(version, ok):
    parsed = mdb._version_tuple(version)
    assert (parsed is not None and parsed >= mdb.MIN_LOADER_FOR_INSIGHT_SYNC) is ok


def test_cli_exit_code_on_an_older_loader(store, tmp_path):
    """The real CLI, with a 4.21.3 loader that has insight_sync first on the path."""
    fake = tmp_path / "fakeloader" / "memstack_skill_loader"
    fake.mkdir(parents=True)
    marker = tmp_path / "sync-was-called"
    (fake / "__init__.py").write_text('__version__ = "4.21.3"\n', encoding="utf-8")
    (fake / "insight_sync.py").write_text(
        "from pathlib import Path\n"
        "class InsightSyncError(Exception):\n    pass\n"
        "def _mark(*a, **k):\n"
        f"    Path({str(marker)!r}).write_text('called')\n"
        "    return {'ok': True}\n"
        "correct_insight = delete_insight = backfill_links = _mark\n",
        encoding="utf-8",
    )
    env = dict(os.environ)
    env.pop("MEMSTACK_DB_PATH", None)
    env["MEMSTACK_SESSION_DB"] = str(store["sess"])  # exists, so no legacy adoption
    env["PYTHONPATH"] = str(fake.parent)
    unlinked = store["ids"][0]
    for argv in (["correct-insight", json.dumps({"id": unlinked, "content": "changed"})],
                 ["delete-insight", str(unlinked)]):
        proc = subprocess.run([sys.executable, str(SCRIPT), *argv], env=env,
                              capture_output=True, text=True, cwd=str(tmp_path))
        assert proc.returncode == 1, proc.stderr
        err = json.loads(proc.stdout)["error"]
        assert UPDATE_MSG in err and "found 4.21.3" in err
    assert not marker.exists()
    assert _digest(store["sess"]) == store["digest"]
