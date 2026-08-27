#!/usr/bin/env python
"""verify: run this project's own check chain and write a receipt.

Judgment happens in the session. Determinism happens in the gate that reads
these receipts. This file only detects, executes, and records, honestly.

Usage:
    python scripts/verify.py list
    python scripts/verify.py run [--task-id ID]
    python scripts/verify.py selftest

Exit codes:
    0  PASS               every detected check ran and passed
    1  FAIL               at least one detected check failed
    2  reserved           for the gate; never emitted by this file
    3  NOTHING_DETECTED   no check was detected, or every one was skipped
    64 usage error        argparse's own default is 2, which would collide

Design notes that are load-bearing, not decoration:

  - A missing tool is SKIP with a reason. It is never omitted and never
    counted as a pass. A skip that reads as a pass is how a check chain
    reports green while never having run.

  - A run where every detected check skipped verified nothing, so it is
    NOTHING_DETECTED rather than PASS. Same reasoning.

  - Every file is read with Python's own open(), never through a shell tool,
    so CRLF and encoding are handled here rather than by whatever the shell
    happens to do.

  - The `cmd` field in a receipt is a DISPLAY STRING. It is never re-executed
    by anything, here or downstream. Captured text fed back to a shell is how
    stray redirect operators get executed.

Stdlib only. No machine-specific paths. Windows first, but portable.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

EXIT_PASS = 0
EXIT_FAIL = 1
EXIT_GATE_RESERVED = 2  # deliberately never returned from this file
EXIT_NOTHING_DETECTED = 3
EXIT_USAGE = 64

OUTPUT_TAIL_CHARS = 2000
CHECK_TIMEOUT_S = 900

# Bounded on purpose. v1 detects these and nothing else.
NPM_SCRIPT_NAMES = ("test", "lint", "typecheck", "build")

RECEIPTS_SUBDIR = Path(".memstack") / "receipts"
MARKER_NAME = "verify-selftest.json"

_SAFE_ID = re.compile(r"[^A-Za-z0-9._-]+")


# --------------------------------------------------------------------------
# small helpers
# --------------------------------------------------------------------------

def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _read_text(path: Path) -> str | None:
    """Read a file as UTF-8, tolerating CRLF and a BOM. None if unreadable."""
    try:
        return path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeDecodeError):
        return None


def _has_toml_section(path: Path, prefix: str) -> bool:
    """True if any line begins a TOML table whose name starts with `prefix`.

    Deliberately a line scan and not a TOML parse: tomllib does not exist
    before Python 3.11 and the answer is only ever used as a boolean.
    """
    text = _read_text(path)
    if text is None:
        return False
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("[") and line[1:].lstrip().startswith(prefix):
            return True
    return False


def _tail(text: str) -> str:
    """Last OUTPUT_TAIL_CHARS characters, newlines normalized to \\n."""
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    if len(normalized) <= OUTPUT_TAIL_CHARS:
        return normalized
    return normalized[-OUTPUT_TAIL_CHARS:]


def _display(argv: list[str]) -> str:
    """Human-readable form of a command. Never parsed, never re-executed."""
    parts = []
    for arg in argv:
        parts.append('"' + arg + '"' if " " in arg else arg)
    return " ".join(parts)


def _safe_task_id(raw: str) -> str:
    """Make a task id safe as a filename without silently losing identity."""
    cleaned = _SAFE_ID.sub("_", raw).strip("._-")
    return cleaned or "task"


def _sha256_file(path: Path) -> str | None:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


# --------------------------------------------------------------------------
# git facts
# --------------------------------------------------------------------------

def _git(root: Path, args: list[str]) -> tuple[int, str] | None:
    """Run a read-only git command. None if git is unavailable."""
    git = shutil.which("git")
    if not git:
        return None
    try:
        proc = subprocess.run(
            [git] + args,
            cwd=str(root),
            capture_output=True,
            timeout=60,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    return proc.returncode, proc.stdout.decode("utf-8", errors="replace")


def git_facts(root: Path) -> tuple[str | None, bool | None]:
    """(head, dirty). Either may be None when git cannot answer.

    dirty is None rather than False when unknown. False would assert a clean
    tree we never observed.
    """
    head = None
    dirty = None
    result = _git(root, ["rev-parse", "HEAD"])
    if result and result[0] == 0:
        head = result[1].strip() or None
    status = _git(root, ["status", "--porcelain"])
    if status and status[0] == 0:
        dirty = bool(status[1].strip())
    return head, dirty


# --------------------------------------------------------------------------
# detection
# --------------------------------------------------------------------------

def _plan(name: str, argv: list[str] | None, skip_reason: str | None) -> dict:
    return {
        "name": name,
        "argv": argv,
        "cmd": _display(argv) if argv else name,
        "skip_reason": skip_reason,
    }


def _detect_npm(root: Path) -> list[dict]:
    pkg_path = root / "package.json"
    if not pkg_path.is_file():
        return []
    text = _read_text(pkg_path)
    if text is None:
        return []
    try:
        pkg = json.loads(text)
    except json.JSONDecodeError as exc:
        return [_plan("npm", None, "package.json is not valid JSON: " + str(exc))]
    scripts = pkg.get("scripts")
    if not isinstance(scripts, dict):
        return []

    present = [n for n in NPM_SCRIPT_NAMES if isinstance(scripts.get(n), str)]
    if not present:
        return []

    npm = shutil.which("npm")
    has_modules = (root / "node_modules").is_dir()

    plans = []
    for script in present:
        if npm is None:
            reason = "npm is not on PATH"
        elif not has_modules:
            reason = "node_modules is absent; run npm install before this check can run"
        else:
            reason = None
        argv = None if reason else [npm, "run", script]
        plans.append(_plan("npm run " + script, argv, reason))
    return plans


def _detect_pytest(root: Path) -> list[dict]:
    reasons = []
    if (root / "pytest.ini").is_file():
        reasons.append("pytest.ini")
    pyproject = root / "pyproject.toml"
    if pyproject.is_file() and _has_toml_section(pyproject, "tool.pytest"):
        reasons.append("pyproject [tool.pytest]")
    if (root / "tests").is_dir():
        reasons.append("tests/ directory")
    if not reasons:
        return []

    try:
        import importlib.util
        available = importlib.util.find_spec("pytest") is not None
    except (ImportError, ValueError):
        available = False

    if not available:
        return [_plan("pytest", None,
                      "pytest is not importable by " + sys.executable)]
    return [_plan("pytest", [sys.executable, "-m", "pytest", "-q"], None)]


def _detect_ruff(root: Path) -> list[dict]:
    found = False
    if (root / "ruff.toml").is_file() or (root / ".ruff.toml").is_file():
        found = True
    pyproject = root / "pyproject.toml"
    if not found and pyproject.is_file() and _has_toml_section(pyproject, "tool.ruff"):
        found = True
    if not found:
        return []

    ruff = shutil.which("ruff")
    if ruff is None:
        return [_plan("ruff", None, "ruff is configured but not on PATH")]
    return [_plan("ruff", [ruff, "check", "."], None)]


def detect_checks(root: Path) -> list[dict]:
    """The whole detectable surface in v1. Nothing else."""
    return _detect_npm(root) + _detect_pytest(root) + _detect_ruff(root)


# --------------------------------------------------------------------------
# execution
# --------------------------------------------------------------------------

def execute_check(plan: dict, root: Path) -> dict:
    if plan["skip_reason"] is not None:
        return {
            "name": plan["name"],
            "cmd": plan["cmd"],
            "exit": None,
            "duration_s": 0.0,
            "status": "SKIP",
            "skip_reason": plan["skip_reason"],
            "output_tail": "",
        }

    started = time.monotonic()
    try:
        proc = subprocess.run(
            plan["argv"],
            cwd=str(root),
            capture_output=True,
            timeout=CHECK_TIMEOUT_S,
        )
    except subprocess.TimeoutExpired:
        return {
            "name": plan["name"],
            "cmd": plan["cmd"],
            "exit": None,
            "duration_s": round(time.monotonic() - started, 3),
            "status": "FAIL",
            "skip_reason": None,
            "output_tail": "timed out after " + str(CHECK_TIMEOUT_S) + " seconds",
        }
    except OSError as exc:
        # Could not launch at all. Reported FAIL rather than SKIP: an
        # unlaunchable check is a broken check chain, and the safe direction
        # is never toward a silent pass.
        return {
            "name": plan["name"],
            "cmd": plan["cmd"],
            "exit": None,
            "duration_s": round(time.monotonic() - started, 3),
            "status": "FAIL",
            "skip_reason": None,
            "output_tail": "could not launch: " + str(exc),
        }

    duration = round(time.monotonic() - started, 3)
    combined = (proc.stdout or b"").decode("utf-8", errors="replace")
    stderr = (proc.stderr or b"").decode("utf-8", errors="replace")
    if stderr:
        combined = combined + ("\n" if combined and not combined.endswith("\n") else "") + stderr

    return {
        "name": plan["name"],
        "cmd": plan["cmd"],
        "exit": proc.returncode,
        "duration_s": duration,
        "status": "PASS" if proc.returncode == 0 else "FAIL",
        "skip_reason": None,
        "output_tail": _tail(combined),
    }


def verdict_for(checks: list[dict]) -> str:
    if not checks:
        return "NOTHING_DETECTED"
    if any(c["status"] == "FAIL" for c in checks):
        return "FAIL"
    if all(c["status"] == "SKIP" for c in checks):
        # Detected but nothing ran, so nothing was verified. Reporting PASS
        # here is the exact shape of a green result from a guard that was
        # never invoked.
        return "NOTHING_DETECTED"
    return "PASS"


def exit_code_for(verdict: str) -> int:
    if verdict == "PASS":
        return EXIT_PASS
    if verdict == "FAIL":
        return EXIT_FAIL
    return EXIT_NOTHING_DETECTED


# --------------------------------------------------------------------------
# the demonstrated-failure marker
# --------------------------------------------------------------------------

def marker_path() -> Path:
    """Per-installation, outside every repo, so no receipt tree carries it."""
    return Path.home() / ".memstack" / MARKER_NAME


def self_path() -> Path:
    return Path(__file__).resolve()


def can_fail_demonstrated() -> bool:
    """True only if selftest passed against THIS exact verify.py.

    Binding the marker to the file's own hash means an edited verify keeps no
    credential it has not re-earned. A gate can then refuse a receipt from a
    verify that has never been shown to fail.
    """
    text = _read_text(marker_path())
    if text is None:
        return False
    try:
        marker = json.loads(text)
    except json.JSONDecodeError:
        return False
    return bool(marker.get("verify_sha256")) and marker.get("verify_sha256") == _sha256_file(self_path())


def write_marker() -> Path:
    path = marker_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "verify_sha256": _sha256_file(self_path()),
        "verify_path": str(self_path()),
        "selftest_passed_at": _now_iso(),
    }
    _write_json(path, payload)
    return path


# --------------------------------------------------------------------------
# receipts
# --------------------------------------------------------------------------

def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(payload, indent=2, ensure_ascii=False))
        handle.write("\n")


def build_receipt(task_id: str, started: str, root: Path, checks: list[dict]) -> dict:
    head, dirty = git_facts(root)
    return {
        "task_id": task_id,
        "started": started,
        "finished": _now_iso(),
        "cwd": str(root),
        "head": head,
        "dirty": dirty,
        "checks": checks,
        "verdict": verdict_for(checks),
        "can_fail_demonstrated": can_fail_demonstrated(),
    }


def write_receipt(root: Path, receipt: dict) -> Path:
    path = root / RECEIPTS_SUBDIR / (_safe_task_id(receipt["task_id"]) + ".json")
    _write_json(path, receipt)
    return path


# --------------------------------------------------------------------------
# commands
# --------------------------------------------------------------------------

def cmd_list(root: Path) -> int:
    plans = detect_checks(root)
    print("cwd: " + str(root))
    if not plans:
        print("no checks detected")
        print("verdict would be: NOTHING_DETECTED")
        return EXIT_NOTHING_DETECTED
    for plan in plans:
        if plan["skip_reason"]:
            print("  SKIP  " + plan["name"] + "  (" + plan["skip_reason"] + ")")
        else:
            print("  RUN   " + plan["name"] + "  ->  " + plan["cmd"])
    if all(p["skip_reason"] for p in plans):
        print("every detected check would skip; verdict would be: NOTHING_DETECTED")
        return EXIT_NOTHING_DETECTED
    print("can_fail_demonstrated: " + str(can_fail_demonstrated()).lower())
    return EXIT_PASS


def cmd_run(root: Path, task_id: str | None) -> int:
    started = _now_iso()
    resolved_id = task_id if task_id else _stamp()
    plans = detect_checks(root)
    checks = [execute_check(plan, root) for plan in plans]
    receipt = build_receipt(resolved_id, started, root, checks)
    path = write_receipt(root, receipt)
    print(json.dumps(receipt, indent=2, ensure_ascii=False))
    print("receipt: " + str(path))
    return exit_code_for(receipt["verdict"])


# --------------------------------------------------------------------------
# selftest: the positive control
# --------------------------------------------------------------------------

def _fabricate(base: Path, name: str, files: dict[str, str]) -> Path:
    repo = base / name
    for rel, body in files.items():
        target = repo / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        with open(target, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(body)
    repo.mkdir(parents=True, exist_ok=True)
    return repo


def _case(name: str, description: str, ok: bool, detail: str) -> dict:
    return {
        "name": name,
        "cmd": description,
        "exit": 0 if ok else 1,
        "duration_s": 0.0,
        "status": "PASS" if ok else "FAIL",
        "skip_reason": None,
        "output_tail": detail,
    }


def _run_case(repo: Path) -> dict:
    """Drive the real detection and execution path against a fabricated repo."""
    plans = detect_checks(repo)
    checks = [execute_check(plan, repo) for plan in plans]
    return build_receipt("selftest-case", _now_iso(), repo, checks)


def cmd_selftest(root: Path) -> int:
    started = _now_iso()
    cases: list[dict] = []

    with tempfile.TemporaryDirectory(prefix="memstack-verify-selftest-") as tmp:
        base = Path(tmp)

        # 1. A check that deliberately fails must be recorded as FAIL.
        fail_repo = _fabricate(base, "failing", {
            "tests/test_deliberate.py": "def test_deliberate_failure():\n    assert False\n",
        })
        r = _run_case(fail_repo)
        names = [c["name"] for c in r["checks"]]
        fail_checks = [c for c in r["checks"] if c["name"] == "pytest"]
        ok = (
            r["verdict"] == "FAIL"
            and len(fail_checks) == 1
            and fail_checks[0]["status"] == "FAIL"
            and isinstance(fail_checks[0]["exit"], int)
            and fail_checks[0]["exit"] != 0
            and exit_code_for(r["verdict"]) == EXIT_FAIL
        )
        cases.append(_case(
            "deliberate-failure-is-recorded-as-FAIL",
            "fabricated repo with a failing pytest test",
            ok,
            "verdict=" + r["verdict"]
            + " checks=" + repr(names)
            + " exit=" + repr(fail_checks[0]["exit"] if fail_checks else None),
        ))

        # 2. A missing tool must be SKIP with a reason, never omitted, never a pass.
        skip_repo = _fabricate(base, "skipping", {
            "package.json": json.dumps(
                {"name": "fab", "version": "0.0.0", "scripts": {"test": "exit 0"}},
                indent=2,
            ) + "\n",
        })
        r = _run_case(skip_repo)
        skip_checks = [c for c in r["checks"] if c["name"] == "npm run test"]
        ok = (
            len(skip_checks) == 1
            and skip_checks[0]["status"] == "SKIP"
            and bool(skip_checks[0]["skip_reason"])
            and skip_checks[0]["status"] != "PASS"
            and r["verdict"] == "NOTHING_DETECTED"
        )
        cases.append(_case(
            "missing-tool-is-SKIP-with-reason-and-not-a-pass",
            "fabricated repo with an npm test script and no node_modules",
            ok,
            "verdict=" + r["verdict"]
            + " status=" + repr(skip_checks[0]["status"] if skip_checks else None)
            + " reason=" + repr(skip_checks[0]["skip_reason"] if skip_checks else None),
        ))

        # 3. A passing check must be recorded as PASS.
        pass_repo = _fabricate(base, "passing", {
            "tests/test_ok.py": "def test_ok():\n    assert True\n",
        })
        r = _run_case(pass_repo)
        pass_checks = [c for c in r["checks"] if c["name"] == "pytest"]
        ok = (
            r["verdict"] == "PASS"
            and len(pass_checks) == 1
            and pass_checks[0]["status"] == "PASS"
            and pass_checks[0]["exit"] == 0
            and exit_code_for(r["verdict"]) == EXIT_PASS
        )
        cases.append(_case(
            "passing-check-is-recorded-as-PASS",
            "fabricated repo with a passing pytest test",
            ok,
            "verdict=" + r["verdict"]
            + " exit=" + repr(pass_checks[0]["exit"] if pass_checks else None),
        ))

        # 4. A repo with nothing detectable is exit 3, distinct from pass and fail.
        empty_repo = _fabricate(base, "empty", {})
        r = _run_case(empty_repo)
        ok = (
            r["checks"] == []
            and r["verdict"] == "NOTHING_DETECTED"
            and exit_code_for(r["verdict"]) == EXIT_NOTHING_DETECTED
        )
        cases.append(_case(
            "nothing-detected-is-exit-3",
            "fabricated empty repo",
            ok,
            "verdict=" + r["verdict"] + " checks=" + repr(r["checks"]),
        ))

    passed = all(c["status"] == "PASS" for c in cases)
    if passed:
        marker = write_marker()
    else:
        marker = None

    head, dirty = git_facts(root)
    receipt = {
        "task_id": "selftest-" + _stamp(),
        "started": started,
        "finished": _now_iso(),
        "cwd": str(root),
        "head": head,
        "dirty": dirty,
        "checks": cases,
        "verdict": "PASS" if passed else "FAIL",
        "can_fail_demonstrated": can_fail_demonstrated(),
    }
    path = write_receipt(root, receipt)
    print(json.dumps(receipt, indent=2, ensure_ascii=False))
    print("receipt: " + str(path))
    if marker:
        print("marker:  " + str(marker))
    return EXIT_PASS if passed else EXIT_FAIL


# --------------------------------------------------------------------------
# entry point
# --------------------------------------------------------------------------

class _Parser(argparse.ArgumentParser):
    """argparse exits 2 on a usage error. 2 is reserved for the gate."""

    def error(self, message: str) -> None:  # type: ignore[override]
        self.print_usage(sys.stderr)
        sys.stderr.write(self.prog + ": error: " + message + "\n")
        raise SystemExit(EXIT_USAGE)


def main(argv: list[str] | None = None) -> int:
    parser = _Parser(prog="verify", description="Run this project's check chain and write a receipt.")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list", help="show the detected chain, run nothing")

    run_parser = sub.add_parser("run", help="run the detected chain and write a receipt")
    run_parser.add_argument("--task-id", dest="task_id", default=None,
                            help="identifier for the receipt; defaults to a UTC timestamp")

    sub.add_parser("selftest", help="prove this verify can report FAIL and SKIP")

    args = parser.parse_args(argv)
    root = Path.cwd().resolve()

    if args.command == "list":
        return cmd_list(root)
    if args.command == "run":
        return cmd_run(root, args.task_id)
    if args.command == "selftest":
        return cmd_selftest(root)
    return EXIT_USAGE


if __name__ == "__main__":
    sys.exit(main())
