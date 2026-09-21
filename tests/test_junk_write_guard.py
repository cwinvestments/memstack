"""Controls for hooks/junk-write-guard.

Migrated from the second half of the scratchpad harness guard-controls-2.py,
with every assertion preserved.

The ledger fixtures are the point of this file. Each one is the literal text
that created a real 0-byte file in this repository's history, so the suite
fails the day the guard stops catching a defect it has already been bitten by.
"""

import json
import os
import shutil
import subprocess

import pytest

from conftest import (BACKTICK, JUNK_GUARD, REPO_ROOT, assert_verdict,
                      needs_bash, run_guard)

pytestmark = needs_bash

NO_PYTHON_PATH = "/usr/bin"
_no_python_available = any(
    os.path.exists(os.path.join(NO_PYTHON_PATH, name))
    for name in ("python", "python3", "py", "python.exe", "python3.exe"))
needs_python_free_path = pytest.mark.skipif(
    _no_python_available,
    reason="%s has a python on it, so the fail-open path cannot be reached"
           % NO_PYTHON_PATH)

# The redirection operator is built from its code point throughout this file.
# Typing one into authored text is the hazard under test, and the standing rule
# against it does not make an exception for the file that tests it.
GT = chr(62)
LT = chr(60)


def junk(command, cwd=REPO_ROOT, scratchpad=None):
    return run_guard(JUNK_GUARD, "Bash", {"command": command}, cwd=cwd,
                     scratchpad=scratchpad)


# ------------------------------------------------------------ ledger fixtures

@pytest.mark.parametrize("command,target", [
    (GT + " green-acres-client@1.0.0 build", "green-acres-client@1.0.0"),
    (GT + " react-scripts build", "react-scripts"),
    (GT + " npm run build", "npm"),
])
def test_npm_lifecycle_banner_lines_block(command, target):
    """npm prints a banner whose every line begins with a redirect operator
    followed by a token. Re-executed as shell input, that text created
    client/green-acres-client@1.0.0, client/npm and client/react-scripts:
    three 0-byte files committed on 2025-11-02, removed in 46cff0d on
    2026-08-19. No care taken while writing a command would have helped, the
    redirect was npm's."""
    rc, err = junk(command)
    assert_verdict(rc, 2, err, must_have=[
        "BLOCKED: a redirection in this command targets [%s]" % target,
        "Write tool", "add-plan-task -"])


@pytest.mark.parametrize("command,target", [
    ("echo done " + GT + " console.error", "console.error"),
    ("echo done " + GT + " s.category", "s.category"),
])
def test_identifiers_that_became_filenames_block(command, target):
    rc, err = junk(command)
    assert_verdict(rc, 2, err, must_have=[
        "BLOCKED: a redirection in this command targets [%s]" % target])


def test_a_lone_backtick_as_the_target_blocks():
    rc, err = junk("echo x " + GT + " " + BACKTICK)
    assert_verdict(rc, 2, err,
                   must_have=["BLOCKED: a redirection in this command targets"])


def test_node_e_fragment_with_an_unbalanced_quote_blocks():
    """Unbalanced quotes plus an operator is the precondition for the whole
    defect class: that is when an operator inside what looked like an argument
    is reinterpreted as a redirect."""
    rc, err = junk('node -e "const f = x =' + GT + ' x.slug')
    assert_verdict(rc, 2, err, must_have=["BLOCKED", "quotes do not balance"])


def test_an_arrow_in_a_correctly_quoted_commit_message_allows():
    """Deliberate coverage given up. Blocking this shape false-blocks more than
    forty real commands in the corpus, so the calibration allows it even though
    the standing prose rule still forbids authoring one."""
    rc, err = junk('git commit -m "refactor: map A =' + GT + ' B"')
    assert_verdict(rc, 0, err, must_not_have=["BLOCKED"])


def test_the_same_commit_message_with_the_quote_left_open_blocks():
    rc, err = junk('git commit -m "refactor: map A =' + GT + ' B')
    assert_verdict(rc, 2, err, must_have=["BLOCKED", "quotes do not balance"])


# ----------------------------------------------------------------- allow cases

@pytest.mark.parametrize("command", [
    "ls -la 2" + GT + "/dev/null",
    "grep -rn KEY src/ 2" + GT + "&1 | head -5",
    "npm run build " + GT + " build.log",
    "python scripts/verify.py run " + GT + GT + " verify.log",
    "git diff " + GT + " /tmp/patch.diff",
    "echo x " + GT + " notes.txt",
    "cat a.txt " + GT + " b.txt",
    "printf 'x' " + GT + " .gitignore",
    "printf 'x' " + GT + " .secretpaths",
    "sed 's/a" + GT + "b/c/' file.txt",
    "echo 'a " + GT + " b' ",
    "python -c \"print('x " + GT + " y')\"",
    "node -e \"const f = x =" + GT + " x * 2; console.log(f(2))\"",
    "curl -s -o out.json -w '%{http_code}\\n' https://example.com",
    "awk '{ if ($1 " + GT + " 5) print }' data.txt",
    "echo hi " + GT + " $OUTFILE",
    "cat report.txt " + GT + " \"$SP/copy.txt\"",
    "git status --porcelain " + GT + " .memstack/status.txt",
])
def test_real_shapes_that_must_not_be_blocked(command):
    rc, err = junk(command)
    assert_verdict(rc, 0, err, must_not_have=["BLOCKED"])


def test_a_heredoc_body_is_never_scanned():
    """A heredoc body is never parsed by the shell for redirections, which is
    why the standing rule names it the safe way to pass multi-line text.
    Scanning it would block the recipe this guard exists to teach."""
    body = ("cat " + LT + LT + "'EOF' " + GT + " notes.md\n"
            "the session's map: A =" + GT + " B, x " + GT + " y\nEOF")
    rc, err = junk(body)
    assert_verdict(rc, 0, err, must_not_have=["BLOCKED"])


def test_a_target_inside_the_payload_scratchpad_dir_allows(tmp_path):
    """The scratchpad is where extensionless throwaway files belong, and the
    payload carries its path, so the guard can tell one from a fragment."""
    scratch = str(tmp_path).replace("\\", "/")
    rc, err = junk("echo x " + GT + " " + scratch + "/anything-at-all",
                   scratchpad=scratch)
    assert_verdict(rc, 0, err, must_not_have=["BLOCKED"])


# ----------------------------------------------------------------- block cases

@pytest.mark.parametrize("command,target", [
    ("echo x " + GT + " fragment", "fragment"),
    ("echo x " + GT + " s.category=1", "s.category=1"),
    ("echo x " + GT + " console.log(x)", "console.log(x)"),
    ("echo x " + GT + " out.weirdext", "out.weirdext"),
    ("echo x " + GT + " nosuchdir/marker", "nosuchdir/marker"),
])
def test_fragment_shaped_targets_block(command, target):
    rc, err = junk(command)
    assert_verdict(rc, 2, err, must_have=[
        "BLOCKED: a redirection in this command targets [%s]" % target])


def test_the_block_message_never_carries_the_command_text():
    rc, err = junk("echo SUPERSECRETVALUE " + GT + " fragment")
    assert_verdict(rc, 2, err, must_have=["BLOCKED"],
                   must_not_have=["SUPERSECRETVALUE", "echo"])


# ------------------------------------------------------------------- posture

def test_a_tool_with_no_command_is_ignored():
    rc, err = run_guard(JUNK_GUARD, "Read", {"file_path": "x"})
    assert_verdict(rc, 0, err, must_not_have=["BLOCKED"])


def test_an_unparseable_payload_fails_open_loudly():
    proc = subprocess.run(["bash", JUNK_GUARD], input="not json",
                          capture_output=True, text=True, env=dict(os.environ))
    assert_verdict(proc.returncode, 0, proc.stderr,
                   must_have=["junk-write-guard: DEGRADED"])


@needs_python_free_path
def test_no_python_fails_open_loudly():
    rc, err = run_guard(JUNK_GUARD, "Bash",
                        {"command": "echo x " + GT + " fragment"},
                        path_override=NO_PYTHON_PATH)
    assert_verdict(rc, 0, err,
                   must_have=["junk-write-guard: DEGRADED", "did NOT run"],
                   must_not_have=["BLOCKED"])


# --------------------------------------------------------------- kill switch

def test_kill_switch_skips_the_guard_entirely():
    """MEMSTACK_NO_JUNK_GUARD=1 allows a command the guard would have blocked,
    and says so, so a disabled guard is never mistaken for a clean pass."""
    payload = json.dumps({
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "tool_input": {"command": "echo x " + GT + " fragment"},
        "cwd": REPO_ROOT,
    })
    env = dict(os.environ, MEMSTACK_NO_JUNK_GUARD="1")
    env.pop("MEMSTACK_NO_SECRET_GUARD", None)
    proc = subprocess.run(["bash", JUNK_GUARD], input=payload,
                          capture_output=True, text=True, env=env)
    assert_verdict(proc.returncode, 0, proc.stderr,
                   must_have=["junk-write-guard: SKIPPED",
                              "MEMSTACK_NO_JUNK_GUARD=1",
                              "NOT examined"],
                   must_not_have=["BLOCKED"])
    assert len(proc.stderr.strip().splitlines()) == 1, "the note is one line"
