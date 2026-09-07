"""scripts/doctor.py reports what MemStack pieces are installed and whether they
agree. These tests call its check functions directly with injected root, env,
home and probe arguments, the same style as test_session_store_path.py, so no
test ever touches the real machine, the real registry or a real import.

Three cases are pinned: a healthy install where every record is OK or WARN and
the exit code is 0, a missing loader where the probe fails without raising and
the exit code stays 0, and a skill count mismatch where that one record is
FAIL and the exit code is 1. A fourth test pins the one property the doctor
exists to guarantee for secrets: the environment check ships names and
set-or-unset only, never a value.
"""

import importlib.util
import json
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "doctor.py"
_spec = importlib.util.spec_from_file_location("memstack_doctor", MODULE_PATH)
doctor = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(doctor)


def _write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data), encoding="utf-8")


def _build_healthy_repo(tmp_path):
    """A minimal repo tree where the manifest and the skills on disk agree."""
    root = tmp_path / "repo"
    for skill in ("foo", "bar"):
        skill_dir = root / "skills" / skill
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(skill, encoding="utf-8")

    _write_json(root / ".claude-plugin" / "plugin.json",
                {"skills": ["skills/foo", "skills/bar"]})
    _write_json(root / "hooks" / "hooks.json", {
        "hooks": {
            "SessionStart": [
                {"hooks": [{"command": "echo hello"}]},
            ],
        },
    })
    (root / "memory" / "sessions").mkdir(parents=True)
    return root


def _installed_plugins_path(tmp_path, version="3.9.11"):
    path = tmp_path / "config" / "installed_plugins.json"
    _write_json(path, {
        "plugins": {
            "memstack@cwinvestments-memstack": {
                "version": version,
                "installPath": str(tmp_path / "cache" / "memstack"),
            },
        },
    })
    return path


def _good_probe():
    return (True, "4.18.0", None)


def _run_healthy(tmp_path, probe):
    root = _build_healthy_repo(tmp_path)
    plugins_path = _installed_plugins_path(tmp_path)
    report_dir = tmp_path / "reports"
    report_dir.mkdir()
    home = tmp_path / "home"
    home.mkdir()
    env = {"MEMSTACK_REPORT_DIR": str(report_dir)}

    return doctor.run_checks(
        root=root,
        env=env,
        home=home,
        candidates=[plugins_path],
        probe=probe,
    )


# ---------------------------------------------------------------------------
# 1. Healthy install
# ---------------------------------------------------------------------------

def test_healthy_install_reports_ok_or_warn_and_exit_zero(tmp_path):
    records = _run_healthy(tmp_path, _good_probe)

    assert records, "expected at least one record"
    for record in records:
        assert record.status in (doctor.OK, doctor.WARN), (
            record.name, record.status, record.detail,
        )
    assert doctor.exit_code(records) == 0


# ---------------------------------------------------------------------------
# 2. Missing loader
# ---------------------------------------------------------------------------

def test_missing_loader_reports_warn_without_raising(tmp_path, monkeypatch):
    def raising_find_spec(name):
        raise ImportError("no module named " + name)

    monkeypatch.setattr(importlib.util, "find_spec", raising_find_spec)

    present, version, reason = doctor.default_loader_probe()
    assert present is False
    assert version is None
    assert reason

    loader_record = doctor.check_loader(probe=doctor.default_loader_probe)
    assert loader_record.status == doctor.WARN

    records = _run_healthy(tmp_path, doctor.default_loader_probe)
    assert doctor.exit_code(records) == 0
    by_name = {record.name: record for record in records}
    assert by_name["loader"].status == doctor.WARN


# ---------------------------------------------------------------------------
# 3. Skill count mismatch
# ---------------------------------------------------------------------------

def test_skill_count_mismatch_reports_fail_and_exit_one(tmp_path):
    root = _build_healthy_repo(tmp_path)
    unregistered = root / "skills" / "baz"
    unregistered.mkdir()
    (unregistered / "SKILL.md").write_text("baz", encoding="utf-8")

    plugins_path = _installed_plugins_path(tmp_path)
    report_dir = tmp_path / "reports"
    report_dir.mkdir()
    home = tmp_path / "home"
    home.mkdir()
    env = {"MEMSTACK_REPORT_DIR": str(report_dir)}

    records = doctor.run_checks(
        root=root,
        env=env,
        home=home,
        candidates=[plugins_path],
        probe=_good_probe,
    )

    by_name = {record.name: record for record in records}
    assert by_name["skill count"].status == doctor.FAIL
    assert doctor.exit_code(records) == 1


# ---------------------------------------------------------------------------
# 4. Environment check never leaks a value
# ---------------------------------------------------------------------------

def test_environment_check_never_prints_values():
    sentinel = "sk-do-not-print-this-12345"
    env = {name: sentinel for name in doctor.ENV_NAMES}

    record = doctor.check_environment(env=env)

    assert record.status == doctor.OK
    assert sentinel not in record.detail
    for name in doctor.ENV_NAMES:
        assert (name + " set") in record.detail

    output = doctor.format_records([record])
    assert sentinel not in output


# ---------------------------------------------------------------------------
# 5. Loader source version versus metadata version
# ---------------------------------------------------------------------------

def test_loader_versions_agreeing_reports_one_version_no_warning():
    def probe():
        return doctor.default_loader_probe(
            source=lambda: "4.21.0", metadata=lambda: "4.21.0",
        )

    present, version, reason = probe()
    assert present is True
    assert version == "4.21.0"
    assert reason is None

    record = doctor.check_loader(probe=probe)
    assert record.status == doctor.OK
    assert "4.21.0" in record.detail


def test_loader_versions_disagreeing_reports_warn_naming_both():
    def probe():
        return doctor.default_loader_probe(
            source=lambda: "4.21.0", metadata=lambda: "4.18.1",
        )

    present, version, reason = probe()
    assert present is True
    assert version == "4.21.0"
    assert reason

    record = doctor.check_loader(probe=probe)
    assert record.status == doctor.WARN
    assert "4.21.0" in record.detail
    assert "4.18.1" in record.detail


def test_loader_absent_package_returns_without_raising():
    def probe():
        return doctor.default_loader_probe(
            source=lambda: None, metadata=lambda: "4.18.1",
        )

    present, version, reason = probe()
    assert present is False
    assert version is None
    assert reason

    record = doctor.check_loader(probe=probe)
    assert record.status == doctor.WARN
