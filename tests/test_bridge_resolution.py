"""Diary insight bridge: which project_dir an insight bridges to, or why not.

The bridge mirrors procedural insights into the skill-loader's memory.db. It
used to report every resolution failure as "unknown project", which conflated
three different faults and hid a real one (a project whose basename collided
with itself via a drive-letter case variant read as "unknown", sending an
investigation after a missing registration that was never missing).

These tests pin the three reasons apart, and pin the auto-registration guard:
cwd must corroborate the name, so an ad-hoc label cannot mint a project.
"""

import importlib.util
import os
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "db" / "memstack-db.py"
_spec = importlib.util.spec_from_file_location("memstack_db_cli", MODULE_PATH)
mdb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mdb)


class FakeLoader:
    """Stand-in for memstack_skill_loader.memory_db."""

    def __init__(self, known=None, legacy=False):
        self._known = known or {}
        if legacy:
            # Older loader: no find_project_dirs_by_name at all.
            del self.find_project_dirs_by_name

    def find_project_dirs_by_name(self, name):
        return list(self._known.get((name or "").strip().lower(), []))

    def resolve_project_dir_by_name(self, name):
        hits = list(self._known.get((name or "").strip().lower(), []))
        return hits[0] if len(hits) == 1 else None

    @staticmethod
    def canonical_project_dir(path):
        if not isinstance(path, str) or len(path) < 2 or path[1] != ":":
            return path
        return path[0].upper() + path[1:].replace("/", "\\")


class LegacyLoader(FakeLoader):
    """Loader predating find_project_dirs_by_name."""

    find_project_dirs_by_name = None

    def __init__(self, known=None):
        FakeLoader.__init__(self, known)


@pytest.fixture
def in_dir(tmp_path, monkeypatch):
    """chdir into a directory with a chosen basename."""
    def _cd(name):
        target = tmp_path / name
        target.mkdir(exist_ok=True)
        monkeypatch.chdir(target)
        return target
    return _cd


# ── success: already known ────────────────────────────────────────────────────

def test_known_project_resolves_without_autoregistering():
    loader = FakeLoader({"adminstack": ["C:\\Projects\\adminstack"]})
    out = mdb.resolve_project_dir(loader, "adminstack")
    assert out["project_dir"] == "C:\\Projects\\adminstack"
    assert "autoregistered" not in out


def test_known_project_lookup_is_case_insensitive_on_the_name():
    loader = FakeLoader({"adminstack": ["C:\\Projects\\adminstack"]})
    assert mdb.resolve_project_dir(loader, "AdminStack")["project_dir"]


# ── the guard: cwd must corroborate the name ──────────────────────────────────

def test_unknown_project_autoregisters_when_cwd_basename_matches(in_dir):
    target = in_dir("foreman")
    out = mdb.resolve_project_dir(FakeLoader(), "foreman")
    assert out["autoregistered"] == out["project_dir"]
    assert Path(out["project_dir"]).name.lower() == "foreman"
    assert str(target).lower().endswith("foreman")


def test_autoregister_name_match_is_case_insensitive(in_dir):
    in_dir("Foreman")
    out = mdb.resolve_project_dir(FakeLoader(), "foreman")
    assert out.get("autoregistered")


def test_junk_name_is_refused_when_cwd_disagrees(in_dir):
    in_dir("memstack")
    out = mdb.resolve_project_dir(FakeLoader(), "general")
    assert "project_dir" not in out
    assert "unrecognized project 'general'" in out["reason"]
    assert "cwd basename is 'memstack'" in out["reason"]


@pytest.mark.parametrize(
    "junk", ["general", "test", "SnowTrack+LawnTrack", "adminstack+memstack-pro",
             "TokenStack (memstack-skill-loader)"]
)
def test_ad_hoc_labels_never_autoregister(in_dir, junk):
    in_dir("some-real-repo")
    out = mdb.resolve_project_dir(FakeLoader(), junk)
    assert "project_dir" not in out
    assert "not auto-registering" in out["reason"]


def test_empty_name_is_refused(in_dir):
    in_dir("whatever")
    for name in (None, "", "   "):
        out = mdb.resolve_project_dir(FakeLoader(), name)
        assert "project_dir" not in out
        assert "unknown project" in out["reason"]


# ── ambiguity is reported as ambiguity, not as "unknown" ──────────────────────

def test_true_collision_reports_ambiguous_with_path_count(in_dir):
    in_dir("twin")
    loader = FakeLoader({"twin": ["C:\\Projects\\Twin", "D:\\Work\\Twin"]})
    out = mdb.resolve_project_dir(loader, "twin")
    assert "project_dir" not in out
    assert "ambiguous project 'twin'" in out["reason"]
    assert "2 known paths" in out["reason"]
    assert "C:\\Projects\\Twin" in out["reason"] and "D:\\Work\\Twin" in out["reason"]


def test_ambiguous_never_autoregisters_even_if_cwd_matches(in_dir):
    """cwd corroboration must not override a genuine collision — picking one
    would silently attach the insight to the wrong project."""
    in_dir("twin")
    loader = FakeLoader({"twin": ["C:\\Projects\\Twin", "D:\\Work\\Twin"]})
    out = mdb.resolve_project_dir(loader, "twin")
    assert "project_dir" not in out
    assert "autoregistered" not in out


def test_the_three_reasons_are_distinguishable(in_dir):
    in_dir("real-repo")
    unknown = mdb.resolve_project_dir(FakeLoader(), "")["reason"]
    mismatch = mdb.resolve_project_dir(FakeLoader(), "general")["reason"]
    ambiguous = mdb.resolve_project_dir(
        FakeLoader({"twin": ["C:\\A\\Twin", "D:\\B\\Twin"]}), "twin")["reason"]
    assert len({unknown, mismatch, ambiguous}) == 3
    assert "unknown project" in unknown
    assert "unrecognized project" in mismatch
    assert "ambiguous project" in ambiguous


# ── old loaders still work ────────────────────────────────────────────────────

def test_legacy_loader_without_find_still_resolves_known_projects():
    loader = LegacyLoader({"adminstack": ["C:\\Projects\\adminstack"]})
    assert mdb._known_project_dirs(loader, "adminstack") == ["C:\\Projects\\adminstack"]


def test_legacy_loader_without_find_still_autoregisters(in_dir):
    in_dir("foreman")
    out = mdb.resolve_project_dir(LegacyLoader(), "foreman")
    assert out.get("autoregistered")


def test_legacy_loader_reports_collision_as_unrecognized_not_ambiguous(in_dir):
    """An old loader collapses 0 and 2+ to None, so ambiguity is unreportable.
    That is the pre-existing limitation, not a regression — but it must still
    refuse rather than guess."""
    in_dir("elsewhere")
    loader = LegacyLoader({"twin": ["C:\\A\\Twin", "D:\\B\\Twin"]})
    out = mdb.resolve_project_dir(loader, "twin")
    assert "project_dir" not in out
    assert "not auto-registering" in out["reason"]
