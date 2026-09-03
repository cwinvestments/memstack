#!/usr/bin/env python
"""verify: run this project's own check chain and write a receipt.

Judgment happens in the session. Determinism happens in the gate that reads
these receipts. This file only detects, executes, and records, honestly.

Usage:
    python scripts/verify.py list
    python scripts/verify.py run [--task-id ID]
    python scripts/verify.py selftest
    python scripts/verify.py gate      # reads a Stop hook payload on stdin

Exit codes:
    0  PASS / ALLOW       every detected check passed, or the gate allows
    1  FAIL               at least one detected check failed
    2  BLOCK              gate only: unverified tracked changes exist
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

  - The gate compares TREE FINGERPRINTS, not timestamps. A receipt proves a
    verdict about one exact tree state and nothing else. "A check ran recently"
    is not the same claim as "this code passed", and only the second one is
    worth blocking on.

  - Untracked files are excluded from the fingerprint. A scratch file, a
    backup, or an editor artifact is not unverified work, and a gate that
    treats it as such gets disarmed by its owner within a day.

  - The gate never blocks unless it is armed by a .verify-required file at the
    repo root. Absent that file this subcommand is inert, which is what makes
    it safe to ship before anyone has opted in.

  - Every internal failure of the gate is an ALLOW with a note on stderr. A
    guard that can break the session it guards will be removed, and a removed
    guard verifies nothing.

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
# Returned only by gate_decide, and only on a block. Never returned by the
# run, list or selftest commands, whose outcomes are 0, 1 and 3.
EXIT_GATE_RESERVED = 2
EXIT_NOTHING_DETECTED = 3
EXIT_USAGE = 64

OUTPUT_TAIL_CHARS = 2000
CHECK_TIMEOUT_S = 900

# Bounded on purpose. v1 detects these and nothing else.
NPM_SCRIPT_NAMES = ("test", "lint", "typecheck", "build")

MEMSTACK_SUBDIR = Path(".memstack")
RECEIPTS_SUBDIR = MEMSTACK_SUBDIR / "receipts"
MARKER_NAME = "verify-selftest.json"

# The gate's arming marker. Untracked, it arms one machine. Committed, it would
# arm every clone: that promotion is a deliberate decision, not a default.
ARM_MARKER_NAME = ".verify-required"
GATE_STATE_NAME = "gate-state.json"

# The repair cap. Two blocked rounds on one unchanged tree, then the gate
# yields: at that point the block has stopped being information and started
# being an obstacle, and a human should look instead.
GATE_MAX_BLOCKS = 3

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


def git_facts(root: Path) -> tuple[str | None, bool | None, int | None]:
    """(head, dirty, untracked_count). Any of the three may be None when git
    cannot answer.

    dirty means exactly what the fingerprint means. It is True only when
    tracked_changes is non-empty and False when that list is empty, so the
    two facts a receipt records about a tree can never disagree about it.
    An untracked file is not a tracked change: a tree carrying nothing but
    backups, scratch scripts and editor artifacts is clean here and
    fingerprints identically to the same tree without them.

    Untracked files are reported separately as untracked_count, so that
    information is kept rather than folded into a boolean the gate would
    then have to ignore.

    None is used rather than False or 0 when git cannot answer, because
    either would assert a clean tree that was never observed.
    """
    changes = tracked_changes(root)
    dirty = None if changes is None else bool(changes)
    return git_head(root), dirty, untracked_count(root)


def git_head(root: Path) -> str | None:
    result = _git(root, ["rev-parse", "HEAD"])
    if result and result[0] == 0:
        return result[1].strip() or None
    return None


def tracked_changes(root: Path) -> list[str] | None:
    """Porcelain lines for TRACKED changes only. None if git cannot answer.

    Untracked (??) entries are dropped. A backup file, a scratch script or an
    editor artifact is not work that needs verifying, and counting it as such
    would make the gate fire on things its owner has no intention of shipping.
    None is returned rather than [] when git cannot answer, because [] would
    assert a clean tree that was never observed.
    """
    status = _git(root, ["status", "--porcelain"])
    if status is None or status[0] != 0:
        return None
    return [line for line in status[1].splitlines()
            if line.strip() and not line.startswith("??")]


def untracked_count(root: Path) -> int | None:
    """How many untracked porcelain lines the tree carries, or None if git
    cannot answer.

    The counterpart to tracked_changes: exactly what that function drops,
    counted instead of discarded. Recorded on receipts so an untracked pile
    stays visible without ever reaching the fingerprint or the gate.
    """
    status = _git(root, ["status", "--porcelain"])
    if status is None or status[0] != 0:
        return None
    return sum(1 for line in status[1].splitlines()
               if line.startswith("??"))


def tree_fingerprint(root: Path) -> str | None:
    """sha256 over HEAD plus every tracked-change line. None if git is mute.

    This is the whole identity of a tree state as far as verification is
    concerned: which commit, plus exactly what is modified on top of it. Two
    trees with the same fingerprint have the same code, so a PASS on one is a
    PASS on the other. Any edit to a tracked file changes it, which is what
    makes a stale receipt unable to clear new work.
    """
    lines = tracked_changes(root)
    if lines is None:
        return None
    head = git_head(root)
    payload = "head:" + (head or "NONE") + "\n" + "\n".join(lines) + "\n"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def repo_root(start: Path) -> Path:
    """The git top level containing `start`, or `start` itself if git is mute."""
    result = _git(start, ["rev-parse", "--show-toplevel"])
    if result and result[0] == 0:
        top = result[1].strip()
        if top:
            return Path(top)
    return start


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


def ensure_memstack_ignored(root: Path) -> None:
    """Write root/.memstack/.gitignore holding a single "*" if it is absent.

    Receipts and gate state are evidence, not source. A customer repo that
    installs this plugin must never be asked to commit them, and must never
    have to notice them in git status to avoid it: the directory ignores
    itself from the moment it first exists. Doing it here rather than in a
    shipped .gitignore edit means it holds in any repo, including one whose
    .gitignore this plugin has never touched.

    An existing file is left exactly as it is, and a write that fails is
    swallowed: neither a receipt nor a gate decision may fail over this.
    """
    path = root / MEMSTACK_SUBDIR / ".gitignore"
    if path.exists():
        return
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as handle:
            handle.write("*\n")
    except OSError:
        pass


def build_receipt(task_id: str, started: str, root: Path, checks: list[dict],
                  kind: str = "run") -> dict:
    head, dirty, untracked = git_facts(root)
    return {
        "task_id": task_id,
        "started": started,
        "finished": _now_iso(),
        "cwd": str(root),
        "kind": kind,
        "head": head,
        "dirty": dirty,
        "untracked_count": untracked,
        "tree_fingerprint": tree_fingerprint(root),
        "checks": checks,
        "verdict": verdict_for(checks),
        "can_fail_demonstrated": can_fail_demonstrated(),
    }


def write_receipt(root: Path, receipt: dict) -> Path:
    path = root / RECEIPTS_SUBDIR / (_safe_task_id(receipt["task_id"]) + ".json")
    ensure_memstack_ignored(root)
    _write_json(path, receipt)
    return path


# --------------------------------------------------------------------------
# the gate
#
# Reads a Stop hook payload on stdin and decides whether unverified tracked
# work exists. All of the logic lives here rather than in the hook script, so
# the hook stays a one-line invocation and this file stays the single portable
# artifact that can be reasoned about, tested, and moved between projects.
# --------------------------------------------------------------------------

def _load_json(path: Path) -> dict | None:
    text = _read_text(path)
    if text is None:
        return None
    try:
        loaded = json.loads(text)
    except json.JSONDecodeError:
        return None
    return loaded if isinstance(loaded, dict) else None


def gate_eligible(receipt: dict) -> bool:
    """Only a PASSing `run` receipt can clear the gate.

    A selftest receipt is explicitly NOT eligible even though its verdict is
    PASS. Selftest proves this file can report FAIL; it never runs the
    project's own checks, so honouring it would let a green result from a chain
    that never examined the project unlock the project's work. That is the
    exact failure this tool exists to prevent, one level up.

    A receipt with no `kind` predates the gate and carries no fingerprint. It
    is ineligible too, which errs toward blocking rather than toward allowing.
    """
    return receipt.get("verdict") == "PASS" and receipt.get("kind") == "run"


def newest_gate_receipt(root: Path) -> dict | None:
    """The most recent gate-eligible receipt, by finish time then mtime."""
    directory = root / RECEIPTS_SUBDIR
    try:
        entries = sorted(directory.glob("*.json"))
    except OSError:
        return None

    best = None
    best_key = None
    for entry in entries:
        receipt = _load_json(entry)
        if receipt is None or not gate_eligible(receipt):
            continue
        try:
            mtime = entry.stat().st_mtime
        except OSError:
            mtime = 0.0
        # ISO-8601 Z strings sort correctly as text, so no parsing is needed.
        key = (str(receipt.get("finished") or ""), mtime)
        if best_key is None or key > best_key:
            best, best_key = receipt, key
    return best


def gate_state_path(root: Path) -> Path:
    return root / MEMSTACK_SUBDIR / GATE_STATE_NAME


def gate_record_block(root: Path, session_id: str, fingerprint: str) -> int:
    """Count consecutive blocks for one (session, tree) pair. Returns the count.

    The count resets when the fingerprint changes, because a changed tree is
    new work and new work deserves enforcement from scratch. A state file that
    cannot be written degrades to a permanent count of 1, which keeps blocking
    rather than yielding: failing toward the safe side of a cap that exists
    only for comfort.
    """
    path = gate_state_path(root)
    state = _load_json(path) or {}
    sessions = state.get("sessions")
    if not isinstance(sessions, dict):
        sessions = {}

    entry = sessions.get(session_id)
    if isinstance(entry, dict) and entry.get("fingerprint") == fingerprint:
        count = int(entry.get("blocks") or 0) + 1
    else:
        count = 1

    sessions[session_id] = {
        "fingerprint": fingerprint,
        "blocks": count,
        "last_seen": _now_iso(),
    }
    # Keep the file small without ever dropping the session being counted.
    if len(sessions) > 50:
        ordered = sorted(sessions.items(),
                         key=lambda kv: str(kv[1].get("last_seen") or ""))
        for stale_id, _ in ordered[:len(sessions) - 50]:
            if stale_id != session_id:
                sessions.pop(stale_id, None)

    try:
        ensure_memstack_ignored(root)
        _write_json(path, {"sessions": sessions})
    except OSError:
        pass
    return count


def gate_decide(payload: dict, fallback_cwd: Path | None = None) -> tuple[int, str]:
    """(exit_code, message). 0 allows, 2 blocks. Message may be empty."""
    if payload.get("stop_hook_active"):
        # The recursion guard. Whatever else is true, a hook that keeps firing
        # into its own re-entry is worse than an unverified tree.
        return EXIT_PASS, ""

    raw_cwd = payload.get("cwd")
    start = None
    if isinstance(raw_cwd, str) and raw_cwd.strip():
        candidate = Path(raw_cwd)
        if candidate.is_dir():
            start = candidate
    if start is None:
        start = fallback_cwd or Path.cwd()
    root = repo_root(start.resolve())

    if not (root / ARM_MARKER_NAME).is_file():
        # Unarmed. This is the shipped-but-inert state, and it is silent on
        # purpose: a note here would be noise on every turn of every session
        # that never asked for a gate.
        return EXIT_PASS, ""

    fingerprint = tree_fingerprint(root)
    if fingerprint is None:
        return EXIT_PASS, ("verify gate: git could not describe the tree at "
                           + str(root) + "; allowing.")

    receipt = newest_gate_receipt(root)
    if receipt is not None and receipt.get("tree_fingerprint") == fingerprint:
        return EXIT_PASS, ""

    changes = tracked_changes(root)
    if not changes:
        # Nothing is modified on top of HEAD. Either no verification has ever
        # happened here, or the last one was of this same commit; both mean
        # there is no unverified edit sitting in the tree.
        if receipt is None:
            return EXIT_PASS, ""
        head = git_head(root)
        if head is not None and receipt.get("head") == head:
            return EXIT_PASS, ""

    session_id = payload.get("session_id")
    if not isinstance(session_id, str) or not session_id.strip():
        session_id = "unknown-session"

    count = gate_record_block(root, session_id, fingerprint)
    if count >= GATE_MAX_BLOCKS:
        return EXIT_PASS, (
            "verify gate: YIELDING after " + str(GATE_MAX_BLOCKS - 1)
            + " blocked rounds on the same unverified tree (tree "
            + fingerprint[:12] + "). The gate will not block again until the"
            + " tree changes. Look at this yourself: two repair rounds did not"
            + " produce a passing receipt.")

    command = "python scripts/verify.py run --task-id " + session_id
    return EXIT_GATE_RESERVED, (
        "verify gate: BLOCKED. Unverified tracked changes exist; run  "
        + command + "  and finish only when it passes.")


def gate_from_text(raw: str, fallback_cwd: Path | None = None) -> tuple[int, str]:
    """Parse a payload and decide. Never raises, never blocks on its own bugs."""
    try:
        payload = json.loads(raw) if raw.strip() else None
        if not isinstance(payload, dict):
            return EXIT_PASS, ("verify gate: stdin was not a JSON object;"
                               " allowing.")
        return gate_decide(payload, fallback_cwd)
    except json.JSONDecodeError:
        return EXIT_PASS, "verify gate: could not parse stdin as JSON; allowing."
    except Exception as exc:  # noqa: BLE001 - deliberate: see the note below.
        # A gate that raises would fail the session it is supposed to protect,
        # and the first thing anyone does with a hook that breaks their session
        # is delete it. Allowing loudly is strictly better than dying.
        return EXIT_PASS, ("verify gate: internal error ("
                           + type(exc).__name__ + ": " + str(exc)
                           + "); allowing.")


def cmd_gate() -> int:
    try:
        raw = sys.stdin.read()
    except (OSError, UnicodeDecodeError) as exc:
        sys.stderr.write("verify gate: could not read stdin ("
                         + type(exc).__name__ + "); allowing.\n")
        return EXIT_PASS
    code, message = gate_from_text(raw)
    if message:
        sys.stderr.write(message + "\n")
    return code


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


# --------------------------------------------------------------------------
# gate controls: fabricate real git repos, drive the real decision function
# --------------------------------------------------------------------------

def _init_repo(repo: Path, tracked: dict[str, str]) -> str | None:
    """git init + commit `tracked`. Returns None on success, else a reason.

    Hooks are pointed at an empty directory inside the fabrication, so a
    machine-wide core.hooksPath cannot reach in and run somebody's pre-commit
    guard against a throwaway repo. Files are added by explicit path: `git add`
    with a blanket -A is exactly how unintended content gets staged.
    """
    git = shutil.which("git")
    if git is None:
        return "git is not on PATH, so the gate cannot be controlled"

    repo.mkdir(parents=True, exist_ok=True)
    hooks_dir = repo / "nohooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)
    for rel, body in tracked.items():
        target = repo / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        with open(target, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(body)

    steps: list[list[str]] = [
        ["init", "-q"],
        ["config", "core.hooksPath", str(hooks_dir)],
        ["config", "user.email", "selftest@example.invalid"],
        ["config", "user.name", "verify selftest"],
        ["config", "commit.gpgsign", "false"],
        ["add", "--"] + sorted(tracked),
        ["commit", "-q", "-m", "selftest baseline"],
    ]
    for step in steps:
        result = _git(repo, step)
        if result is None or result[0] != 0:
            return "git " + step[0] + " failed in the fabricated repo"
    if git_head(repo) is None:
        return "fabricated repo has no HEAD after commit"
    return None


def _write_gate_receipt(repo: Path, task_id: str, kind: str,
                        fingerprint: str | None) -> None:
    _write_json(repo / RECEIPTS_SUBDIR / (task_id + ".json"), {
        "task_id": task_id,
        "started": _now_iso(),
        "finished": _now_iso(),
        "cwd": str(repo),
        "kind": kind,
        "head": git_head(repo),
        "dirty": True,
        "tree_fingerprint": fingerprint,
        "checks": [],
        "verdict": "PASS",
        "can_fail_demonstrated": True,
    })


def _payload(repo: Path, session_id: str, stop_hook_active: bool = False) -> dict:
    return {
        "session_id": session_id,
        "cwd": str(repo),
        "hook_event_name": "Stop",
        "stop_hook_active": stop_hook_active,
    }


def _gate_cases(base: Path) -> list[dict]:
    """Seven controls over the gate. Each asserts an exit code AND its message.

    Asserting only the code would pass a gate that blocks for the wrong reason
    or blocks silently, and a block with no message is indistinguishable from a
    crash to whoever receives it.
    """
    cases: list[dict] = []

    def dirty_armed_repo(name: str) -> tuple[Path, str | None]:
        repo = base / name
        reason = _init_repo(repo, {"src/app.py": "VALUE = 1\n"})
        if reason:
            return repo, reason
        # A tracked modification: this is the only thing the gate cares about.
        with open(repo / "src" / "app.py", "w", encoding="utf-8", newline="\n") as h:
            h.write("VALUE = 2\n")
        # An untracked file too, which must NOT count as unverified work.
        with open(repo / "scratch.tmp", "w", encoding="utf-8", newline="\n") as h:
            h.write("ignore me\n")
        with open(repo / ARM_MARKER_NAME, "w", encoding="utf-8", newline="\n") as h:
            h.write("armed by selftest\n")
        return repo, None

    # 1. Armed, tracked modifications, no receipt at all: must BLOCK.
    repo, reason = dirty_armed_repo("gate-block")
    if reason:
        cases.append(_case("gate-blocks-armed-dirty-tree", "fabricated git repo",
                           False, reason))
    else:
        code, message = gate_decide(_payload(repo, "s-block"))
        ok = code == EXIT_GATE_RESERVED and "Unverified tracked changes" in message
        cases.append(_case(
            "gate-blocks-armed-dirty-tree",
            "armed repo, tracked modification, no receipt",
            ok,
            "exit=" + repr(code) + " message=" + repr(message),
        ))

    # 2. A matching PASS run receipt clears exactly that tree.
    repo, reason = dirty_armed_repo("gate-allow")
    if reason:
        cases.append(_case("gate-allows-matching-pass-receipt", "fabricated git repo",
                           False, reason))
    else:
        _write_gate_receipt(repo, "match", "run", tree_fingerprint(repo))
        code, message = gate_decide(_payload(repo, "s-allow"))
        ok = code == EXIT_PASS and message == ""
        cases.append(_case(
            "gate-allows-matching-pass-receipt",
            "armed dirty repo with a PASS run receipt for this exact tree",
            ok,
            "exit=" + repr(code) + " message=" + repr(message),
        ))

    # 3. A PASS SELFTEST receipt must NOT clear the gate. Selftest never runs
    #    the project's checks, so it cannot vouch for the project's code.
    repo, reason = dirty_armed_repo("gate-selftest-receipt")
    if reason:
        cases.append(_case("gate-ignores-passing-selftest-receipt", "fabricated git repo",
                           False, reason))
    else:
        _write_gate_receipt(repo, "selftest-shaped", "selftest", tree_fingerprint(repo))
        code, message = gate_decide(_payload(repo, "s-selftest"))
        ok = code == EXIT_GATE_RESERVED and "Unverified tracked changes" in message
        cases.append(_case(
            "gate-ignores-passing-selftest-receipt",
            "armed dirty repo whose only PASS receipt is a selftest",
            ok,
            "exit=" + repr(code) + " message=" + repr(message),
        ))

    # 4. stop_hook_active short-circuits everything. Never risk the loop.
    repo, reason = dirty_armed_repo("gate-recursion")
    if reason:
        cases.append(_case("gate-allows-when-stop-hook-active", "fabricated git repo",
                           False, reason))
    else:
        code, message = gate_decide(_payload(repo, "s-loop", stop_hook_active=True))
        ok = code == EXIT_PASS and message == ""
        cases.append(_case(
            "gate-allows-when-stop-hook-active",
            "the same blocking tree, with stop_hook_active true",
            ok,
            "exit=" + repr(code) + " message=" + repr(message),
        ))

    # 5. Unarmed: the shipped-but-inert state, silent as well as permissive.
    repo, reason = dirty_armed_repo("gate-unarmed")
    if reason:
        cases.append(_case("gate-allows-when-unarmed", "fabricated git repo",
                           False, reason))
    else:
        (repo / ARM_MARKER_NAME).unlink()
        code, message = gate_decide(_payload(repo, "s-unarmed"))
        ok = code == EXIT_PASS and message == ""
        cases.append(_case(
            "gate-allows-when-unarmed",
            "the same blocking tree with no .verify-required marker",
            ok,
            "exit=" + repr(code) + " message=" + repr(message),
        ))

    # 6. The repair cap yields on the third encounter of one unchanged tree.
    repo, reason = dirty_armed_repo("gate-cap")
    if reason:
        cases.append(_case("gate-cap-yields-on-third-round", "fabricated git repo",
                           False, reason))
    else:
        rounds = [gate_decide(_payload(repo, "s-cap")) for _ in range(3)]
        codes = [c for c, _ in rounds]
        ok = (
            codes == [EXIT_GATE_RESERVED, EXIT_GATE_RESERVED, EXIT_PASS]
            and "YIELDING" in rounds[2][1]
        )
        cases.append(_case(
            "gate-cap-yields-on-third-round",
            "three Stop events, same session, same unchanged tree",
            ok,
            "exits=" + repr(codes) + " third=" + repr(rounds[2][1]),
        ))

    # 7. Malformed stdin allows, with a note. The gate's own failure is never
    #    the session's failure.
    code, message = gate_from_text("{ this is not json", base)
    ok = code == EXIT_PASS and "verify gate:" in message and "JSON" in message
    cases.append(_case(
        "gate-allows-on-malformed-stdin-with-a-note",
        "unparseable stdin fed to the real entry point",
        ok,
        "exit=" + repr(code) + " message=" + repr(message),
    ))

    return cases


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

        # 5. An untracked file is not a tracked change. A clean HEAD plus one
        #    untracked file must report dirty false, count that file, and
        #    fingerprint identically to the same tree without it. This is the
        #    control on the receipt field the gate does not read.
        untracked_repo = base / "untracked-only"
        reason = _init_repo(untracked_repo, {"src/app.py": "VALUE = 1\n"})
        if reason:
            cases.append(_case("untracked-file-does-not-make-a-tree-dirty",
                               "fabricated git repo", False, reason))
        else:
            clean = tree_fingerprint(untracked_repo)
            with open(untracked_repo / "scratch.tmp", "w",
                      encoding="utf-8", newline="\n") as handle:
                handle.write("ignore me\n")
            r = build_receipt("selftest-untracked", _now_iso(),
                              untracked_repo, [])
            ok = (
                r["dirty"] is False
                and r["untracked_count"] == 1
                and clean is not None
                and r["tree_fingerprint"] == clean
            )
            cases.append(_case(
                "untracked-file-does-not-make-a-tree-dirty",
                "git repo with a clean HEAD and one untracked file",
                ok,
                "dirty=" + repr(r["dirty"])
                + " untracked_count=" + repr(r["untracked_count"])
                + " fingerprint_matches_clean="
                + repr(r["tree_fingerprint"] == clean),
            ))

        # 6. Writing a receipt must leave .memstack ignoring itself. A repo
        #    that installs this plugin should never be asked to commit
        #    evidence, nor to notice it in git status in order to decline.
        ignore_repo = _fabricate(base, "receipt-ignore", {})
        written = write_receipt(ignore_repo, build_receipt(
            "selftest-ignore", _now_iso(), ignore_repo, []))
        ignore_file = ignore_repo / MEMSTACK_SUBDIR / ".gitignore"
        content = (ignore_file.read_text(encoding="utf-8")
                   if ignore_file.is_file() else None)
        ok = written.is_file() and content is not None and content.strip() == "*"
        cases.append(_case(
            "receipt-write-leaves-memstack-self-ignoring",
            "fresh fabricated repo, one receipt written",
            ok,
            "receipt=" + repr(written.is_file())
            + " gitignore=" + repr(ignore_file.is_file())
            + " content=" + repr(content),
        ))

        # 7-13. The gate's own controls, against real fabricated git repos.
        cases.extend(_gate_cases(base))

    passed = all(c["status"] == "PASS" for c in cases)
    if passed:
        marker = write_marker()
    else:
        marker = None

    head, dirty, untracked = git_facts(root)
    receipt = {
        "task_id": "selftest-" + _stamp(),
        "started": started,
        "finished": _now_iso(),
        "cwd": str(root),
        # Marked selftest so the gate will not accept it. This receipt says
        # "verify.py works", never "this project's checks passed".
        "kind": "selftest",
        "head": head,
        "dirty": dirty,
        "untracked_count": untracked,
        "tree_fingerprint": tree_fingerprint(root),
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

    sub.add_parser("gate", help="read a Stop hook payload on stdin and allow or block")

    args = parser.parse_args(argv)
    root = Path.cwd().resolve()

    if args.command == "list":
        return cmd_list(root)
    if args.command == "run":
        return cmd_run(root, args.task_id)
    if args.command == "selftest":
        return cmd_selftest(root)
    if args.command == "gate":
        return cmd_gate()
    return EXIT_USAGE


if __name__ == "__main__":
    sys.exit(main())
