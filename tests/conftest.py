"""Shared fixtures for the hook guard suites.

These were two standalone scripts in a session scratchpad. The probe method is
unchanged and is the reason they are python rather than shell: every command
under test is a string inside a JSON document on the hook's stdin, so a
redirection operator or an unbalanced quote in a test case is never parsed by
the shell running the tests. A shell harness would have executed half of them.

Both guards are addressed at their shipped path under hooks/, which is the file
customers receive. Nothing here reads the old .claude/hooks copies; they no
longer exist.
"""

import json
import os
import shutil
import subprocess

import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_GUARD = os.path.join(REPO_ROOT, "hooks", "secret-read-guard")
JUNK_GUARD = os.path.join(REPO_ROOT, "hooks", "junk-write-guard")

# Planted in the fixture repo so a leak has something recognisable to be. It is
# not a credential and never was: it is a literal written here.
PLANTED = "FAKE-not-a-real-key-0000"

# A lone backtick names one of the junk files in the ledger. It is built from
# its code point rather than typed, because authoring one is itself the hazard
# the junk guard exists to catch.
BACKTICK = chr(96)

needs_bash = pytest.mark.skipif(
    shutil.which("bash") is None,
    reason="these guards are bash hooks and there is no bash on PATH",
)


def run_guard(guard, tool, tool_input, cwd=REPO_ROOT, project_dir=REPO_ROOT,
              path_override=None, scratchpad=None):
    """Hand the guard a PreToolUse payload the way Claude Code does.

    Returns (exit code, stderr). Exit 2 is a block; stderr carries the message
    that teaches the session what to do instead, and both are asserted on.
    Exit code alone would not be enough: a guard that blocked everything with
    an empty message would pass an exit-code-only test while teaching nothing.
    """
    payload = {
        "hook_event_name": "PreToolUse",
        "tool_name": tool,
        "tool_input": tool_input,
        "cwd": cwd,
        "session_id": "controls",
        "tool_use_id": "controls",
    }
    if scratchpad:
        payload["scratchpad_dir"] = scratchpad
    env = dict(os.environ)
    env["CLAUDE_PROJECT_DIR"] = project_dir
    # A kill switch left set in the developer's environment would turn every
    # block assertion below into a silent pass.
    env.pop("MEMSTACK_NO_SECRET_GUARD", None)
    env.pop("MEMSTACK_NO_JUNK_GUARD", None)
    if path_override is not None:
        env["PATH"] = path_override
    proc = subprocess.run(
        ["bash", guard],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        env=env,
    )
    return proc.returncode, proc.stderr


def assert_verdict(got_rc, want_rc, stderr, must_have=(), must_not_have=()):
    """Assert the exit code, the message content, and the absence of leaks."""
    problems = []
    if got_rc != want_rc:
        problems.append("exit %s, wanted %s" % (got_rc, want_rc))
    for needle in must_have:
        if needle not in stderr:
            problems.append("stderr missing: %r" % needle)
    for needle in must_not_have:
        if needle in stderr:
            problems.append("stderr leaked: %r" % needle)
    if PLANTED in stderr:
        problems.append("stderr carried the planted value")
    assert not problems, "\n".join(problems) + "\n--- stderr ---\n" + stderr


@pytest.fixture(scope="session")
def plain_repo(tmp_path_factory):
    """A project with a secret-bearing file and its documented counterparts.

    Built here rather than committed: a tracked .env would be refused by this
    repo's own .gitignore, and a fixture tree containing one is exactly what
    the guard exists to keep out of a repository.
    """
    root = tmp_path_factory.mktemp("repo-plain")
    (root / ".env").write_text(
        "# fixture\nAPI_KEY=%s\nSENDGRID_API_KEY_PROD=%s\n" % (PLANTED, PLANTED),
        encoding="utf-8")
    (root / ".env.example").write_text(
        "API_KEY=your-key-here\nSENDGRID_API_KEY_PROD=\n", encoding="utf-8")
    (root / "ordinary.txt").write_text("nothing secret here\n", encoding="utf-8")
    (root / "vault-token.conf").write_text(
        "token = %s\n" % PLANTED, encoding="utf-8")
    return str(root).replace("\\", "/")


@pytest.fixture(scope="session")
def ext_repo(tmp_path_factory):
    """A project that extends the pattern list with its own .secretpaths."""
    root = tmp_path_factory.mktemp("repo-ext")
    (root / ".secretpaths").write_text(
        "# per-repo additions, one glob per line\nvault-*.conf\n", encoding="utf-8")
    (root / "vault-token.conf").write_text(
        "token = %s\n" % PLANTED, encoding="utf-8")
    return str(root).replace("\\", "/")
