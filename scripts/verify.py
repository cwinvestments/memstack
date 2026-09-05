#!/usr/bin/env python
"""verify: run this project's own check chain and write a receipt.

Judgment happens in the session. Determinism happens in the gate that reads
these receipts. This file only detects, executes, and records, honestly.

Usage:
    python scripts/verify.py list
    python scripts/verify.py run [--task-id ID]
    python scripts/verify.py selftest
    python scripts/verify.py gate      # reads a Stop hook payload on stdin
    python scripts/verify.py report-marker   # reads a UserPromptSubmit payload

Exit codes:
    0  PASS / ALLOW       every detected check passed, or the gate allows
    1  FAIL               at least one detected check failed
    2  BLOCK              gate only: no PASS receipt matches the tree
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
    worth blocking on. The fingerprint names tracked CONTENT, not the commit
    that content happens to sit on, so committing verified work does not
    invalidate its receipt.

  - Untracked files are excluded from the fingerprint, and inherently so: the
    fingerprint is a git tree object, and a tree holds only what the index
    holds. A scratch file, a backup, or an editor artifact is not unverified
    work, and a gate that treats it as such gets disarmed by its owner within
    a day.

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

# The report requirement. A prompt carrying this exact phrase asks the session
# to write its final report to a file. The marker is what carries that request
# across the turn boundary: the Stop gate cannot see the prompt, and a session
# that forgot the request is precisely the session that will not remember it
# unprompted either.
REPORT_PHRASE = "Report per memstack:report"
REPORT_MARKER_NAME = "report-required.json"
REPORT_DIR_ENV = "MEMSTACK_REPORT_DIR"

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

def _git(root: Path, args: list[str],
         env: dict[str, str] | None = None) -> tuple[int, str] | None:
    """Run a git command and capture stdout. None if git is unavailable.

    Every caller but one is read-only. The exception is tree_fingerprint,
    which runs `add -u` against a COPY of the index named by GIT_INDEX_FILE in
    `env`; the repository's own index is never the target. env=None inherits
    the process environment, which is what every read-only caller wants.
    """
    git = shutil.which("git")
    if not git:
        return None
    try:
        proc = subprocess.run(
            [git] + args,
            cwd=str(root),
            capture_output=True,
            timeout=60,
            env=env,
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
    """sha256 over the git tree object for the working tree's tracked content.

    This is the identity of a tree state as far as verification is concerned:
    the CONTENT of every tracked file, and nothing else. Two trees with the
    same tracked content have the same fingerprint regardless of which commit
    they sit on, which is why committing verified work does not require
    re-verifying it: the commit moves content that was already checked, and
    moving it changes nothing the checks looked at. Any edit to a tracked
    file, staged or not, does change the content and so changes the
    fingerprint, which is what keeps a stale receipt from clearing new work.

    The work happens against a COPY of the index, so the repository's own
    index is never touched: locate the real one, copy it, then run `add -u`
    and `write-tree` with GIT_INDEX_FILE pointing at the copy. `add -u`
    folds in tracked modifications and deletions; files already staged are
    in the copy to begin with.

    The copy must be indistinguishable from the original, mtime included,
    which is why it is made with copy2 rather than copyfile. Git decides
    whether to trust an index entry's cached stat data using its racy-clean
    rule: an entry whose mtime is not older than the index file's own mtime
    is treated as possibly stale and re-read from disk, while an older entry
    is trusted on stat alone. copyfile stamps the copy with a fresh mtime,
    which makes every entry look older than its index and so trusted. A file
    edited within the same second as the last index write, to content of the
    same byte length, still matches on the fields git compares, so git
    serialises its HEAD content instead of what is on disk and the
    fingerprint silently describes the wrong tree. That is not a rare corner:
    a 200 iteration probe of one selftest case hit it 33 times, plus 33 more
    where both computations were wrong in the same direction and agreed.
    copy2 carries the original mtime across so the rule sees exactly what it
    would have seen against the real index. The mtime is asserted afterwards
    and set explicitly with os.utime when a filesystem truncates it.

    Untracked files are excluded, and inherently rather than by a filter:
    write-tree serialises the index, `add -u` only ever updates paths git
    already tracks, and a path git has never heard of is in neither. There is
    no rule here that could be forgotten or mis-scoped.

    None whenever git cannot answer: git absent, not a repository, unmerged
    entries that write-tree refuses to serialise, or no temp directory. The
    temp index is deleted on every path.
    """
    located = _git(root, ["rev-parse", "--git-path", "index"])
    if located is None or located[0] != 0:
        return None
    raw = located[1].strip()
    if not raw:
        return None
    real_index = Path(raw)
    if not real_index.is_absolute():
        real_index = root / real_index

    tmpdir = None
    try:
        if not real_index.is_file():
            return None
        tmpdir = tempfile.mkdtemp(prefix="memstack-verify-index-")
        copy = Path(tmpdir) / "index"
        # copy2, not copyfile: the mtime travels with the bytes. See the
        # docstring. A fresh mtime here is a silently wrong fingerprint.
        shutil.copy2(real_index, copy)
        original_stat = os.stat(real_index)
        copied_stat = os.stat(copy)
        if copied_stat.st_mtime_ns != original_stat.st_mtime_ns:
            # Some filesystems truncate what copy2 sets. Say it in nanoseconds
            # rather than trust the copy to have carried it.
            os.utime(copy, ns=(original_stat.st_atime_ns,
                               original_stat.st_mtime_ns))

        env = dict(os.environ)
        # Forward slashes: git for Windows accepts either, this accepts fewer
        # ways to be wrong.
        env["GIT_INDEX_FILE"] = copy.as_posix()

        staged = _git(root, ["add", "-u"], env=env)
        if staged is None or staged[0] != 0:
            return None
        written = _git(root, ["write-tree"], env=env)
        if written is None or written[0] != 0:
            return None
        tree = written[1].strip()
        if not tree:
            return None
        return hashlib.sha256(("tree:" + tree).encode("utf-8")).hexdigest()
    except OSError:
        return None
    finally:
        if tmpdir is not None:
            shutil.rmtree(tmpdir, ignore_errors=True)


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
        # What that fingerprint MEANS. Receipts written before 3.9.2 carry a
        # fingerprint computed a different way and no key saying so, and the
        # gate refuses those rather than risking a match across two schemes.
        "fingerprint_kind": "tree",
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
# Reads a Stop hook payload on stdin and decides whether a PASS receipt
# matches the tree. All of the logic lives here rather than in the hook, so
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
    """Only a PASSing `run` receipt carrying a tree fingerprint can clear the gate.

    A selftest receipt is explicitly NOT eligible even though its verdict is
    PASS. Selftest proves this file can report FAIL; it never runs the
    project's own checks, so honouring it would let a green result from a chain
    that never examined the project unlock the project's work. That is the
    exact failure this tool exists to prevent, one level up.

    A receipt with no `kind` predates the gate and carries no fingerprint. It
    is ineligible too, which errs toward blocking rather than toward allowing.

    A receipt with no `fingerprint_kind`, or one naming anything other than
    "tree", predates 3.9.2. Its tree_fingerprint is a hash of HEAD plus
    porcelain status lines, which is a different claim about a different
    thing that happens to live in the same field and have the same shape.
    Comparing the two schemes could only ever match by accident, and an
    accidental match would clear the gate on work nothing had verified, so
    such a receipt is ineligible. The cost is one verify run after upgrading.
    """
    return (receipt.get("verdict") == "PASS"
            and receipt.get("kind") == "run"
            and receipt.get("fingerprint_kind") == "tree")


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


def _payload_root(payload: dict,
                  fallback_cwd: Path | None) -> tuple[Path, Path]:
    """(cwd, repo root) from a hook payload. Never raises, always answers.

    Shared by the Stop gate and the report marker so the two can never disagree
    about which repository one payload is talking about.
    """
    raw_cwd = payload.get("cwd")
    start = None
    if isinstance(raw_cwd, str) and raw_cwd.strip():
        candidate = Path(raw_cwd)
        if candidate.is_dir():
            start = candidate
    if start is None:
        start = fallback_cwd or Path.cwd()
    start = start.resolve()
    return start, repo_root(start)


def _payload_session(payload: dict) -> str:
    """The session id, or a stable stand-in. Never empty, because it is a key."""
    session_id = payload.get("session_id")
    if not isinstance(session_id, str) or not session_id.strip():
        return "unknown-session"
    return session_id


# --------------------------------------------------------------------------
# the report requirement
#
# A UserPromptSubmit hook records a request; the Stop gate enforces it. The two
# halves live here together because they share one file format and one set of
# rules about where a report is allowed to be, and splitting them across a hook
# script and this file is how the two drift apart.
# --------------------------------------------------------------------------

def report_dir() -> Path:
    """Where reports land: MEMSTACK_REPORT_DIR, else ~/.memstack/reports.

    Outside the repository on purpose. A report written into a working tree is
    one more untracked file to explain, and eventually one more file caught by
    somebody's blanket git add.
    """
    raw = os.environ.get(REPORT_DIR_ENV) or ""
    if raw.strip():
        return Path(raw.strip()).expanduser()
    return Path.home() / ".memstack" / "reports"


def report_marker_path(root: Path) -> Path:
    return root / MEMSTACK_SUBDIR / REPORT_MARKER_NAME


def report_prefix(project: str, day: str) -> str:
    """The part of a report's name that is knowable before it is written. The
    time suffix is not: it is the local clock at the moment of writing, which
    is why nothing here predicts it."""
    return project + "-" + day + "-"


def newest_report(directory: Path, prefix: str, after: float) -> Path | None:
    """A file named for this prefix, written after `after`. None when there is
    none, and None on any error: the gate must never block a session because it
    could not read a directory."""
    try:
        entries = sorted(directory.iterdir())
    except OSError:
        return None
    for entry in entries:
        if not entry.name.startswith(prefix):
            continue
        try:
            if entry.is_file() and entry.stat().st_mtime > after:
                return entry
        except OSError:
            continue
    return None


def report_marker_decide(payload: dict,
                         fallback_cwd: Path | None = None) -> Path | None:
    """Record a report request from a UserPromptSubmit payload.

    Returns the marker path when the prompt carried the phrase, and None,
    having written nothing, for every other prompt. Writing nothing is the
    overwhelmingly common case: this runs on every prompt of every session, so
    anything it does unasked it does thousands of times.

    The expected prefix is computed HERE and not at Stop time. The local date
    can roll over mid-session, and the file the session was asked for is the
    one named for the day the request was made.
    """
    prompt = payload.get("prompt")
    if not isinstance(prompt, str) or REPORT_PHRASE not in prompt:
        return None

    start, root = _payload_root(payload, fallback_cwd)
    project = start.name or root.name or "session"
    now = datetime.now(timezone.utc)
    marker = {
        "session_id": _payload_session(payload),
        "requested_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        # The epoch copy exists so the gate compares an mtime against a number
        # rather than parsing its own timestamp format back out of text.
        "requested_at_epoch": now.timestamp(),
        "expected_prefix": report_prefix(project,
                                         datetime.now().strftime("%Y-%m-%d")),
        "report_dir": str(report_dir()),
        "phrase": REPORT_PHRASE,
    }
    path = report_marker_path(root)
    ensure_memstack_ignored(root)
    _write_json(path, marker)
    return path


def report_marker_from_text(raw: str,
                            fallback_cwd: Path | None = None) -> Path | None:
    """Parse a payload and record. Never raises: see cmd_report_marker."""
    try:
        payload = json.loads(raw) if raw.strip() else None
        if not isinstance(payload, dict):
            return None
        return report_marker_decide(payload, fallback_cwd)
    except Exception:  # noqa: BLE001 - deliberate, same reasoning as the gate.
        return None


def report_decision(root: Path, session_id: str) -> tuple[int, str]:
    """Block while a report this session was asked for is still not on disk.

    Keyed on the session id because the request belongs to one session's
    prompt: a marker another session left behind must not hold this one's turn,
    and a marker this session left behind must outlive its own turns until it
    is satisfied.
    """
    path = report_marker_path(root)
    marker = _load_json(path)
    if marker is None:
        return EXIT_PASS, ""
    if marker.get("session_id") != session_id:
        return EXIT_PASS, ""

    prefix = marker.get("expected_prefix")
    if not isinstance(prefix, str) or not prefix:
        # A marker that cannot say what it is waiting for can never be
        # satisfied, and an unsatisfiable block is an obstacle, not a gate.
        return EXIT_PASS, ""

    raw_dir = marker.get("report_dir")
    directory = (Path(raw_dir) if isinstance(raw_dir, str) and raw_dir.strip()
                 else report_dir())
    raw_epoch = marker.get("requested_at_epoch")
    after = float(raw_epoch) if isinstance(raw_epoch, (int, float)) else 0.0

    if newest_report(directory, prefix, after) is not None:
        # Satisfied. Retire the marker: a requirement that keeps firing after
        # it has been met is indistinguishable from a gate that is simply
        # broken, and the second one gets deleted by its owner.
        try:
            path.unlink()
        except OSError:
            pass
        return EXIT_PASS, ""

    count = gate_record_block(root, session_id + "::report",
                              str(marker.get("requested_at") or ""))
    if count >= GATE_MAX_BLOCKS:
        return EXIT_PASS, (
            "verify gate: YIELDING on the report requirement after "
            + str(GATE_MAX_BLOCKS - 1) + " blocked rounds. Write the report"
            + " yourself, or delete " + str(path) + ".")

    return EXIT_GATE_RESERVED, (
        "verify gate: BLOCKED. A report was requested; write it per"
        " memstack:report to " + str(directory) + " and finish.")


def receipt_decision(root: Path, session_id: str) -> tuple[int, str]:
    """Does a PASS receipt match this exact tree. The original gate, moved out
    of gate_decide unchanged so the report requirement can be a second decision
    rather than another branch inside this one."""
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
        "verify gate: BLOCKED. No PASS receipt matches this tree state; run  "
        + command + "  and finish only when it passes.")


def gate_decide(payload: dict, fallback_cwd: Path | None = None) -> tuple[int, str]:
    """(exit_code, message). 0 allows, 2 blocks. Message may be empty."""
    if payload.get("stop_hook_active"):
        # The recursion guard. Whatever else is true, a hook that keeps firing
        # into its own re-entry is worse than an unverified tree.
        return EXIT_PASS, ""

    _, root = _payload_root(payload, fallback_cwd)
    session_id = _payload_session(payload)

    code, message = receipt_decision(root, session_id)
    if code != EXIT_PASS:
        return code, message

    # The report requirement is a second, independent gate, consulted only
    # where the receipt logic would already have allowed, so one turn is never
    # blocked for two reasons at once. It arms itself from its own marker
    # rather than from .verify-required: the prompt that asked for a report is
    # the opt-in, and a repository that never armed the receipt gate still owes
    # the report somebody asked it for.
    report_code, report_message = report_decision(root, session_id)
    if report_code != EXIT_PASS:
        return report_code, report_message
    # Either half may allow with something to say. The report half speaks only
    # when it yields, which is precisely the moment somebody needs to read it,
    # so its note wins where both have one.
    return EXIT_PASS, report_message or message


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


def cmd_report_marker() -> int:
    """Always 0, always silent, whatever happens.

    Two properties of UserPromptSubmit make that the only defensible contract.
    Exit 2 on this event blocks the prompt and ERASES it, which is not a price
    a bookkeeping hook may charge its user. And stdout on this event is
    injected into the model's context, so anything printed here is printed into
    every prompt of every session forever.
    """
    try:
        raw = sys.stdin.read()
    except (OSError, UnicodeDecodeError):
        return EXIT_PASS
    report_marker_from_text(raw)
    return EXIT_PASS


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
                        fingerprint: str | None,
                        fingerprint_kind: str | None = "tree") -> None:
    """Write a PASS receipt by hand. fingerprint_kind=None omits the key
    entirely, which is exactly the shape of a receipt written before 3.9.2."""
    receipt = {
        "task_id": task_id,
        "started": _now_iso(),
        "finished": _now_iso(),
        "cwd": str(repo),
        "kind": kind,
        "head": git_head(repo),
        "dirty": True,
        "tree_fingerprint": fingerprint,
        "fingerprint_kind": fingerprint_kind,
        "checks": [],
        "verdict": "PASS",
        "can_fail_demonstrated": True,
    }
    if fingerprint_kind is None:
        del receipt["fingerprint_kind"]
    _write_json(repo / RECEIPTS_SUBDIR / (task_id + ".json"), receipt)


def _write_report_marker(repo: Path, session_id: str, prefix: str,
                         directory: Path, age_s: float = 2.0) -> Path:
    """A report marker written by hand, dated `age_s` seconds in the past.

    The backdating is deliberate. A report file written moments later has to be
    unambiguously newer than the request, and mtime resolution is a whole
    second on some filesystems, so a marker stamped "now" would make an
    immediate report look simultaneous rather than subsequent.
    """
    requested = time.time() - age_s
    path = report_marker_path(repo)
    _write_json(path, {
        "session_id": session_id,
        "requested_at": datetime.fromtimestamp(
            requested, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "requested_at_epoch": requested,
        "expected_prefix": prefix,
        "report_dir": str(directory),
        "phrase": REPORT_PHRASE,
    })
    return path


def _payload(repo: Path, session_id: str, stop_hook_active: bool = False) -> dict:
    return {
        "session_id": session_id,
        "cwd": str(repo),
        "hook_event_name": "Stop",
        "stop_hook_active": stop_hook_active,
    }


def _gate_cases(base: Path) -> list[dict]:
    """Thirteen controls over the gate. Each asserts an exit code AND its message.

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
        ok = (code == EXIT_GATE_RESERVED
              and "No PASS receipt matches this tree state" in message)
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
        ok = (code == EXIT_GATE_RESERVED
              and "No PASS receipt matches this tree state" in message)
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

    # 8. A receipt written before 3.9.2 carries no fingerprint_kind, and its
    #    tree_fingerprint was computed a different way. It must not clear the
    #    gate. The control comes first and is asserted before the result
    #    counts: the SAME receipt, same fingerprint string, same everything,
    #    WITH the key does clear the gate. Without that control this case
    #    would also pass if the receipt were being rejected for some unrelated
    #    reason, or if the gate had simply stopped allowing anything.
    repo, reason = dirty_armed_repo("gate-old-format")
    if reason:
        cases.append(_case("old-format-receipt-is-ineligible",
                           "fabricated git repo", False, reason))
    else:
        fingerprint = tree_fingerprint(repo)
        _write_gate_receipt(repo, "same-receipt", "run", fingerprint)
        control_code, control_message = gate_decide(_payload(repo, "s-old-control"))
        # Same path, same fingerprint. The only difference is the key.
        _write_gate_receipt(repo, "same-receipt", "run", fingerprint,
                            fingerprint_kind=None)
        code, message = gate_decide(_payload(repo, "s-old"))
        ok = (
            control_code == EXIT_PASS
            and control_message == ""
            and code == EXIT_GATE_RESERVED
            and "No PASS receipt matches this tree state" in message
        )
        cases.append(_case(
            "old-format-receipt-is-ineligible",
            "armed dirty repo whose only PASS run receipt predates fingerprint_kind",
            ok,
            "control_exit=" + repr(control_code)
            + " exit=" + repr(code) + " message=" + repr(message),
        ))

    # 9. A report was requested and has not been written: BLOCK, on a tree the
    #    receipt logic is entirely happy with. The control is asserted first
    #    and is load-bearing: the SAME repo, the SAME receipt, with no marker,
    #    allows silently. Without it this case would also pass against a gate
    #    that had simply started blocking everything it was shown.
    repo, reason = dirty_armed_repo("report-block")
    if reason:
        cases.append(_case("report-request-blocks-until-the-report-exists",
                           "fabricated git repo", False, reason))
    else:
        _write_gate_receipt(repo, "match", "run", tree_fingerprint(repo))
        control_code, control_message = gate_decide(_payload(repo, "s-report"))
        reports = base / "reports-block"
        reports.mkdir(parents=True, exist_ok=True)
        _write_report_marker(repo, "s-report", "proj-2026-01-01-", reports)
        code, message = gate_decide(_payload(repo, "s-report"))
        ok = (
            control_code == EXIT_PASS
            and control_message == ""
            and code == EXIT_GATE_RESERVED
            and "A report was requested" in message
            and str(reports) in message
        )
        cases.append(_case(
            "report-request-blocks-until-the-report-exists",
            "armed repo, matching PASS receipt, one unmet report request",
            ok,
            "control_exit=" + repr(control_code)
            + " control_message=" + repr(control_message)
            + " exit=" + repr(code) + " message=" + repr(message),
        ))

    # 10. Writing the report clears the block and retires the marker. The
    #     control is the block asserted BEFORE the file is written, in this
    #     same repo: a gate that had stopped reading the marker at all would
    #     otherwise sail through the allowing half.
    repo, reason = dirty_armed_repo("report-clear")
    if reason:
        cases.append(_case("writing-the-report-clears-the-block",
                           "fabricated git repo", False, reason))
    else:
        _write_gate_receipt(repo, "match", "run", tree_fingerprint(repo))
        reports = base / "reports-clear"
        reports.mkdir(parents=True, exist_ok=True)
        prefix = "proj-2026-01-01-"
        marker = _write_report_marker(repo, "s-clear", prefix, reports)
        before_code, before_message = gate_decide(_payload(repo, "s-clear"))
        with open(reports / (prefix + "142530.txt"), "w",
                  encoding="utf-8", newline="\n") as handle:
            handle.write("the session says what it did\n")
        after_code, after_message = gate_decide(_payload(repo, "s-clear"))
        ok = (
            before_code == EXIT_GATE_RESERVED
            and "A report was requested" in before_message
            and after_code == EXIT_PASS
            and after_message == ""
            and not marker.exists()
        )
        cases.append(_case(
            "writing-the-report-clears-the-block",
            "the same request, before and after the file exists",
            ok,
            "control_before_exit=" + repr(before_code)
            + " after_exit=" + repr(after_code)
            + " after_message=" + repr(after_message)
            + " marker_retired=" + repr(not marker.exists()),
        ))

    # 11. The hook writes a marker for a prompt carrying the phrase, and
    #     nothing at all for one that does not. The quiet half is asserted
    #     first and is the control: this hook runs on every prompt ever
    #     submitted, so writing nothing is the behaviour that has to hold
    #     thousands of times a day, and a hook that wrote a marker
    #     unconditionally would satisfy the other half on its own.
    hook_repo = base / "report-hook"
    reason = _init_repo(hook_repo, {"src/app.py": "VALUE = 1\n"})
    if reason:
        cases.append(_case("report-hook-writes-only-for-the-phrase",
                           "fabricated git repo", False, reason))
    else:
        marker = report_marker_path(hook_repo)
        quiet = report_marker_from_text(json.dumps({
            "session_id": "s-hook",
            "cwd": str(hook_repo),
            "hook_event_name": "UserPromptSubmit",
            "prompt": "Summarise what changed and report back in the terminal.",
        }), hook_repo)
        control_wrote_nothing = quiet is None and not marker.exists()
        written = report_marker_from_text(json.dumps({
            "session_id": "s-hook",
            "cwd": str(hook_repo),
            "hook_event_name": "UserPromptSubmit",
            "prompt": "Do the work.\n\nReport per memstack:report\n",
        }), hook_repo)
        data = _load_json(marker) or {}
        prefix = str(data.get("expected_prefix") or "")
        ok = (
            control_wrote_nothing
            and written is not None
            and marker.is_file()
            and data.get("session_id") == "s-hook"
            and prefix.startswith(hook_repo.name + "-")
            and prefix.endswith("-")
            and len(prefix) == len(hook_repo.name) + len("-YYYY-MM-DD-")
            and bool(data.get("requested_at"))
            and isinstance(data.get("requested_at_epoch"), float)
        )
        cases.append(_case(
            "report-hook-writes-only-for-the-phrase",
            "one prompt without the phrase, then one with it",
            ok,
            "control_wrote_nothing=" + repr(control_wrote_nothing)
            + " marker=" + repr(marker.is_file())
            + " prefix=" + repr(prefix)
            + " session_id=" + repr(data.get("session_id")),
        ))

    # 12. The report requirement honours the same repair cap as the receipt
    #     half, and it SAYS SO when it yields. The message is asserted, not
    #     just the code: the first draft of this returned the yield with the
    #     other half's empty message, so the gate went quiet on the third round
    #     with nothing to distinguish it from a satisfied requirement. A silent
    #     allow and a yielding allow are the same exit code and opposite facts.
    repo, reason = dirty_armed_repo("report-cap")
    if reason:
        cases.append(_case("report-cap-yields-with-a-note",
                           "fabricated git repo", False, reason))
    else:
        _write_gate_receipt(repo, "match", "run", tree_fingerprint(repo))
        reports = base / "reports-cap"
        reports.mkdir(parents=True, exist_ok=True)
        _write_report_marker(repo, "s-cap-report", "proj-2026-01-01-", reports)
        rounds = [gate_decide(_payload(repo, "s-cap-report")) for _ in range(3)]
        codes = [c for c, _ in rounds]
        ok = (
            codes == [EXIT_GATE_RESERVED, EXIT_GATE_RESERVED, EXIT_PASS]
            and "YIELDING" in rounds[2][1]
            and "report" in rounds[2][1]
        )
        cases.append(_case(
            "report-cap-yields-with-a-note",
            "three Stop events, same session, one unmet report request",
            ok,
            "exits=" + repr(codes) + " third=" + repr(rounds[2][1]),
        ))

    # 13. stop_hook_active short-circuits the report requirement too. The
    #     control is the same repo and the same marker WITHOUT the flag, which
    #     must block: otherwise this case would pass against a gate that had
    #     stopped enforcing reports altogether.
    repo, reason = dirty_armed_repo("report-recursion")
    if reason:
        cases.append(_case("report-allows-when-stop-hook-active",
                           "fabricated git repo", False, reason))
    else:
        _write_gate_receipt(repo, "match", "run", tree_fingerprint(repo))
        reports = base / "reports-recursion"
        reports.mkdir(parents=True, exist_ok=True)
        _write_report_marker(repo, "s-loop-report", "proj-2026-01-01-", reports)
        control_code, _ = gate_decide(_payload(repo, "s-loop-report"))
        code, message = gate_decide(
            _payload(repo, "s-loop-report", stop_hook_active=True))
        ok = (control_code == EXIT_GATE_RESERVED
              and code == EXIT_PASS
              and message == "")
        cases.append(_case(
            "report-allows-when-stop-hook-active",
            "the same unmet report request, with stop_hook_active true",
            ok,
            "control_exit=" + repr(control_code)
            + " exit=" + repr(code) + " message=" + repr(message),
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

        # 7. Committing content that is already in the working tree must not
        #    change the fingerprint. This is the whole point of 3.9.2: a
        #    receipt earned on verified work survives the commit of that work.
        #    The control is asserted first and is load-bearing: the edit
        #    itself MUST have moved the fingerprint. Without it, a
        #    tree_fingerprint that returned a constant, or None, would sail
        #    through this case looking like a success.
        commit_repo = base / "fingerprint-commit"
        reason = _init_repo(commit_repo, {"src/app.py": "VALUE = 1\n"})
        if reason:
            cases.append(_case("commit-does-not-change-fingerprint",
                               "fabricated git repo", False, reason))
        else:
            clean = tree_fingerprint(commit_repo)
            with open(commit_repo / "src" / "app.py", "w",
                      encoding="utf-8", newline="\n") as handle:
                handle.write("VALUE = 2\n")
            before = tree_fingerprint(commit_repo)
            failed = None
            for step in [["add", "--", "src/app.py"],
                         ["commit", "-q", "-m", "same content, now committed"]]:
                result = _git(commit_repo, step)
                if result is None or result[0] != 0:
                    failed = "git " + step[0] + " failed"
                    break
            after = None if failed else tree_fingerprint(commit_repo)
            control_edit_moved_it = (clean is not None and before is not None
                                     and before != clean)
            ok = (
                failed is None
                and control_edit_moved_it
                and after is not None
                and after == before
            )
            cases.append(_case(
                "commit-does-not-change-fingerprint",
                "tracked edit, then a commit of that exact content",
                ok,
                "control_edit_moved_it=" + repr(control_edit_moved_it)
                + " clean=" + repr(clean[:12] if clean else clean)
                + " before_commit=" + repr(before[:12] if before else before)
                + " after_commit=" + repr(after[:12] if after else after)
                + (" failed=" + repr(failed) if failed else ""),
            ))

        # 8. Staging a new file must move the fingerprint; leaving the same
        #    file untracked must not. Both halves are asserted, and the
        #    untracked half is the control: a fingerprint that ignored the
        #    index entirely would satisfy it on its own, so it proves nothing
        #    unless the staged half is checked alongside it.
        staged_repo = base / "fingerprint-staged"
        reason = _init_repo(staged_repo, {"src/app.py": "VALUE = 1\n"})
        if reason:
            cases.append(_case("staged-new-file-changes-fingerprint",
                               "fabricated git repo", False, reason))
        else:
            clean = tree_fingerprint(staged_repo)
            with open(staged_repo / "src" / "new.py", "w",
                      encoding="utf-8", newline="\n") as handle:
                handle.write("NEW = 1\n")
            untracked_fp = tree_fingerprint(staged_repo)
            result = _git(staged_repo, ["add", "--", "src/new.py"])
            failed = None if (result and result[0] == 0) else "git add failed"
            staged_fp = None if failed else tree_fingerprint(staged_repo)
            control_untracked_invisible = (clean is not None
                                           and untracked_fp == clean)
            ok = (
                failed is None
                and control_untracked_invisible
                and staged_fp is not None
                and staged_fp != clean
            )
            cases.append(_case(
                "staged-new-file-changes-fingerprint",
                "one new file, first untracked and then staged",
                ok,
                "control_untracked_invisible=" + repr(control_untracked_invisible)
                + " clean=" + repr(clean[:12] if clean else clean)
                + " untracked=" + repr(untracked_fp[:12] if untracked_fp else untracked_fp)
                + " staged=" + repr(staged_fp[:12] if staged_fp else staged_fp)
                + (" failed=" + repr(failed) if failed else ""),
            ))

        # 9. Git's racy-clean rule trusts an index entry's cached stat data
        #    once that entry is older than the index file itself. The temp
        #    index copy must therefore carry the ORIGINAL index's mtime; with
        #    a fresh one every entry reads as trusted, and an edit made in the
        #    same second as the last index write, to content of the same byte
        #    length, serialises as its HEAD content. This case sets exactly
        #    that trap and asserts the fingerprint is correct and identical on
        #    every computation across second boundaries. The control reverts
        #    the fix in place and requires the trap to actually spring: a
        #    green result here would otherwise prove only that the trap was
        #    never armed.
        def racy_fixture(name: str) -> tuple[Path, str | None, bool]:
            """Commit N bytes, then overwrite with N different bytes, inside
            one second. Returns (repo, reason, landed_in_the_same_second)."""
            repo = base / name
            for _ in range(12):
                if repo.exists():
                    shutil.rmtree(repo, ignore_errors=True)
                # Begin at the top of a second so init, commit and the edit
                # all fall inside the same one.
                time.sleep(max(0.0, 1.0 - (time.time() % 1.0)))
                reason = _init_repo(repo, {"src/app.py": "VALUE = 1\n"})
                if reason:
                    return repo, reason, False
                edited = repo / "src" / "app.py"
                with open(edited, "w", encoding="utf-8", newline="\n") as handle:
                    handle.write("VALUE = 2\n")
                located = _git(repo, ["rev-parse", "--git-path", "index"])
                if located is None or located[0] != 0:
                    return repo, "git could not locate the index", False
                index_path = Path(located[1].strip())
                if not index_path.is_absolute():
                    index_path = repo / index_path
                try:
                    if int(index_path.stat().st_mtime) == int(edited.stat().st_mtime):
                        return repo, None, True
                except OSError as exc:
                    return repo, "stat failed: " + repr(exc), False
            return repo, None, False

        def fingerprint_loop(repo: Path) -> tuple[list[str | None], int]:
            """50 fingerprints of an unchanging tree, spread over enough wall
            clock to cross at least two second boundaries."""
            values: list[str | None] = []
            seconds = set()
            for _ in range(50):
                values.append(tree_fingerprint(repo))
                seconds.add(int(time.time()))
                time.sleep(0.02)
            return values, len(seconds)

        def head_tree_fingerprint(repo: Path) -> str | None:
            """What a stale answer looks like: the committed tree."""
            result = _git(repo, ["rev-parse", "HEAD^{tree}"])
            if result is None or result[0] != 0 or not result[1].strip():
                return None
            return hashlib.sha256(
                ("tree:" + result[1].strip()).encode("utf-8")).hexdigest()

        racy_repo, racy_reason, racy_armed = racy_fixture("fingerprint-racy")
        control_repo, control_reason, control_armed = racy_fixture(
            "fingerprint-racy-control")
        trap_reason = racy_reason or control_reason
        if trap_reason:
            cases.append(_case("same-second-edit-fingerprints-consistently",
                               "fabricated git repo", False, repr(trap_reason)))
        elif not (racy_armed and control_armed):
            cases.append(_case(
                "same-second-edit-fingerprints-consistently",
                "same-second same-length edit under git's racy-clean rule",
                False,
                "trap NOT ARMED: the edit never landed in the index's own"
                " second (racy=" + repr(racy_armed)
                + " control=" + repr(control_armed) + ")",
            ))
        else:
            stale_fp = head_tree_fingerprint(racy_repo)
            values, distinct_seconds = fingerprint_loop(racy_repo)

            # The oracle is independent of the copy logic under test: stage
            # the modification into the repo's REAL index and serialise that.
            added = _git(racy_repo, ["add", "-u"])
            written = (_git(racy_repo, ["write-tree"])
                       if added is not None and added[0] == 0 else None)
            expected = None
            if written is not None and written[0] == 0 and written[1].strip():
                expected = hashlib.sha256(
                    ("tree:" + written[1].strip()).encode("utf-8")).hexdigest()

            # Control: put the bug back. copyfile drops the mtime, and the
            # os.utime correction that backs copy2 up is neutralised too, so
            # this is the pre-3.9.4 code path exactly. Both are restored in
            # the finally regardless of what the loop does.
            real_copy2, real_utime = shutil.copy2, os.utime
            try:
                shutil.copy2 = shutil.copyfile
                os.utime = lambda *a, **k: None
                control_values, _ = fingerprint_loop(control_repo)
            finally:
                shutil.copy2, os.utime = real_copy2, real_utime
            control_stale_fp = head_tree_fingerprint(control_repo)
            control_demonstrated = (
                control_stale_fp is not None
                and any(v == control_stale_fp for v in control_values))

            all_equal = len(set(values)) == 1
            correct = expected is not None and values[0] == expected
            distinct_from_head = expected is not None and expected != stale_fp
            ok = (all_equal and correct and distinct_from_head
                  and distinct_seconds >= 3 and control_demonstrated)
            cases.append(_case(
                "same-second-edit-fingerprints-consistently",
                "same-second same-length edit under git's racy-clean rule",
                ok,
                "control=" + ("DEMONSTRATED, the reverted fix produced "
                              + str(sum(1 for v in control_values
                                        if v == control_stale_fp))
                              + "/50 stale values"
                              if control_demonstrated
                              else "NOT DEMONSTRATED, the reverted fix produced"
                                   " no stale value so this case proves nothing")
                + " | distinct_fingerprints=" + str(len(set(values)))
                + "/50 seconds_spanned=" + str(distinct_seconds)
                + " matches_edited_content=" + repr(correct)
                + " differs_from_HEAD_tree=" + repr(distinct_from_head)
                + " fp=" + repr(values[0][:12] if values[0] else values[0])
                + " expected=" + repr(expected[:12] if expected else expected)
                + " HEAD_tree_fp=" + repr(stale_fp[:12] if stale_fp else stale_fp),
            ))

        # 10-22. The gate's own controls, against real fabricated git repos.
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
        "fingerprint_kind": "tree",
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
    sub.add_parser("report-marker",
                   help="read a UserPromptSubmit payload on stdin and record"
                        " a report request")

    args = parser.parse_args(argv)
    root = Path.cwd().resolve()

    if args.command == "list":
        return cmd_list(root)
    if args.command == "run":
        return cmd_run(root, args.task_id)
    if args.command == "selftest":
        return cmd_selftest(root)
    if args.command == "report-marker":
        return cmd_report_marker()
    if args.command == "gate":
        return cmd_gate()
    return EXIT_USAGE


if __name__ == "__main__":
    sys.exit(main())
