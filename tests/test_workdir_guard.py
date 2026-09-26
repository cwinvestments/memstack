"""The working-directory guard, driven the way Claude Code drives it.

Every case hands scripts/workdir_guard.py a UserPromptSubmit payload on stdin,
in a subprocess, with the key set the recon captured from a real payload:
session_id, transcript_path, cwd, scratchpad_dir, prompt_id, permission_mode,
hook_event_name, prompt. A block is asserted on BOTH the decision and the
reason text, and a pass is asserted to be silent on stdout, because stdout on
this event is injected into the model's context and a guard that chatters on
every prompt is a guard that costs every prompt.

The pasted wrapper is built exactly as the docs and the recon describe it: an
opening <pasted_content id="..."> line and a closing </pasted_content id="...">
line around the pasted text.
"""

import json
import os
import subprocess
import sys
import time

import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUARD = os.path.join(REPO_ROOT, "scripts", "workdir_guard.py")
sys.path.insert(0, os.path.join(REPO_ROOT, "scripts"))

import workdir_guard  # noqa: E402

SESSION_CWD = r"C:\Projects\memstack"
OTHER = r"C:\Projects\DeedStack"


def paste(body, before="", after=""):
    """A prompt field holding one pasted block, as Claude Code expands it."""
    return (before + '<pasted_content id="1609">\n' + body
            + '\n</pasted_content id="1609">\n' + after)


def payload(prompt, cwd=SESSION_CWD, session_id="ups-test"):
    return {
        "session_id": session_id,
        "transcript_path": r"C:\Users\x\.claude\projects\p\t.jsonl",
        "cwd": cwd,
        "scratchpad_dir": r"C:\Users\x\AppData\Local\Temp\claude\scratch",
        "prompt_id": "prompt-1",
        "permission_mode": "default",
        "hook_event_name": "UserPromptSubmit",
        "prompt": prompt,
    }


def drive(raw, env_extra=None):
    """Run the guard as the hook runs it. Returns (exit code, stdout, stderr)."""
    env = dict(os.environ)
    for name in ("MEMSTACK_REPORT_ON_TASK_PROMPTS", "MEMSTACK_REPORT_TRIGGERS"):
        env.pop(name, None)
    env.update(env_extra or {})
    proc = subprocess.run(
        [sys.executable, GUARD],
        input=raw.encode("utf-8"),
        capture_output=True,
        env=env,
        timeout=30,
        check=False,
    )
    return (proc.returncode, proc.stdout.decode("utf-8"),
            proc.stderr.decode("utf-8"))


def assert_blocks(result, declared, cwd):
    code, out, err = result
    assert code == 0, "a block is exit 0 with JSON, never exit 2"
    decision = json.loads(out)
    assert decision == {"decision": "block", "reason": decision["reason"]}
    reason = decision["reason"]
    assert "the prompt declares " + declared + " but" in reason
    assert "this session is in " + cwd + "." in reason
    assert "If this is the wrong window, paste it where it belongs." in reason
    assert "DEGRADED" not in err


def assert_passes(result):
    code, out, err = result
    assert code == 0
    assert out == "", "a pass prints nothing to stdout"
    assert "DEGRADED" not in err


def test_different_absolute_dir_blocks_and_names_both():
    prompt = paste("Working directory: " + OTHER + "\n\nFix the thing.")
    assert_blocks(drive(json.dumps(payload(prompt))), OTHER, SESSION_CWD)


def test_exact_cwd_after_normalization_passes():
    # Mixed slashes, lower-cased drive and folder, trailing slash.
    prompt = paste("Working directory: c:/projects\\MemStack/\n\nDo it.")
    assert_passes(drive(json.dumps(payload(prompt))))


def test_gitbash_form_of_cwd_passes():
    prompt = paste("Working directory: /c/Projects/memstack\n\nDo it.")
    assert_passes(drive(json.dumps(payload(prompt))))


def test_forward_slash_cwd_like_claude_project_dir_passes():
    prompt = paste("Working directory: C:\\Projects\\memstack\n\nDo it.")
    assert_passes(drive(json.dumps(payload(prompt, cwd="C:/Projects/memstack"))))


def test_declared_subdirectory_of_cwd_passes():
    prompt = paste("Working directory: C:\\Projects\\memstack\\scripts\n\nGo.")
    assert_passes(drive(json.dumps(payload(prompt))))


def test_declared_parent_of_cwd_passes():
    # A worktree session, handed a prompt naming the repo root.
    cwd = r"C:\Projects\memstack\.claude\worktrees\feature-x"
    prompt = paste("Working directory: C:\\Projects\\memstack\n\nGo.")
    assert_passes(drive(json.dumps(payload(prompt, cwd=cwd))))


def test_sibling_sharing_a_name_prefix_is_not_a_child():
    # memstack-skill-loader starts with "memstack" but is not inside it.
    declared = r"C:\Projects\memstack-skill-loader"
    prompt = paste("Working directory: " + declared + "\n\nGo.")
    assert_blocks(drive(json.dumps(payload(prompt))), declared, SESSION_CWD)


def test_short_unwrapped_paste_declaring_another_dir_blocks():
    # The probe capture, byte for byte: a short paste arrives with no wrapper.
    prompt = ("Working directory: " + OTHER + "\n\nTest paste, do not act on"
              " this. Just confirming the working-directory guard fires.")
    assert_blocks(drive(json.dumps(payload(prompt))), OTHER, SESSION_CWD)


def test_short_unwrapped_paste_declaring_this_dir_passes():
    prompt = "Working directory: c:/projects\\MemStack/\n\nDo it."
    assert_passes(drive(json.dumps(payload(prompt))))


def test_blank_lines_before_a_first_line_declaration_still_count():
    prompt = "\n\n  \nWorking directory: " + OTHER + "\n\nGo."
    assert_blocks(drive(json.dumps(payload(prompt))), OTHER, SESSION_CWD)


def test_mid_prompt_reference_unwrapped_passes_silently():
    prompt = ("Why did the diary for the other repo say this?\n"
              "Working directory: " + OTHER + "\nIt looked odd.")
    assert_passes(drive(json.dumps(payload(prompt))))


def test_no_directory_line_anywhere_passes_silently():
    assert_passes(drive(json.dumps(payload("commit it and push dev"))))


def test_wrapped_declaration_wins_over_a_typed_first_line():
    # The wrapped block is checked first; a matching paste passes even when a
    # typed first line names somewhere else.
    prompt = paste("Working directory: " + SESSION_CWD + "\n\nGo.",
                   before="Working directory: " + OTHER + "\n")
    assert_passes(drive(json.dumps(payload(prompt))))


def test_wrapped_block_without_a_line_falls_back_to_the_first_line():
    prompt = paste("Traceback (most recent call last)",
                   before="Working directory: " + OTHER + "\n\n")
    assert_blocks(drive(json.dumps(payload(prompt))), OTHER, SESSION_CWD)


def test_pasted_block_without_a_directory_line_passes_silently():
    prompt = paste("Here is a stack trace:\nTraceback (most recent call last)")
    assert_passes(drive(json.dumps(payload(prompt))))


def test_unterminated_pasted_block_passes_silently():
    prompt = '<pasted_content id="1">\nWorking directory: ' + OTHER + "\n"
    assert_passes(drive(json.dumps(payload(prompt))))


DIARY_EXCERPT = (
    "# Session diary\n"
    "Working directory: C:\\Projects\\DeedStack\n"
    "Date: 2026-09-21\n"
    "Branch: dev\n\n"
    "## Accomplished\n- fixed the deed parser\n"
)


def test_diary_excerpt_for_another_project_blocks_in_the_wrong_session():
    prompt = paste(DIARY_EXCERPT, after="\nWhat did we leave open?")
    assert_blocks(drive(json.dumps(payload(prompt))), OTHER, SESSION_CWD)


def test_diary_excerpt_passes_in_the_matching_session():
    prompt = paste(DIARY_EXCERPT, after="\nWhat did we leave open?")
    assert_passes(drive(json.dumps(payload(prompt, cwd=OTHER))))


def test_two_directory_lines_the_first_one_decides():
    # Documented: the first line is the declaration. A later one, such as a
    # quoted diary inside the task, never overrides it.
    body = ("Working directory: " + OTHER + "\n\nContext:\n"
            "Working directory: " + SESSION_CWD + "\n")
    assert_blocks(drive(json.dumps(payload(paste(body)))), OTHER, SESSION_CWD)
    assert_passes(drive(json.dumps(payload(paste(body), cwd=OTHER))))


def test_decorated_path_parses_to_the_path():
    rest = r"C:\Projects\x (dev branch)"
    primary, _ = workdir_guard.declared_candidates(rest)
    assert primary == r"C:\Projects\x"
    prompt = paste("Working directory: " + rest + "\n\nGo.")
    assert_blocks(drive(json.dumps(payload(prompt))), r"C:\Projects\x",
                  SESSION_CWD)
    assert_passes(drive(json.dumps(payload(prompt, cwd=r"C:\Projects\x"))))


def test_quoted_and_backticked_paths_unwrap():
    for wrapped in ('"C:\\Projects\\memstack"', "`C:\\Projects\\memstack`"):
        prompt = paste("Working directory: " + wrapped + "\n\nGo.")
        assert_passes(drive(json.dumps(payload(prompt))))


def test_unquoted_path_with_a_space_can_only_match():
    cwd = r"C:\Program Files\tool"
    prompt = paste("Working directory: C:\\Program Files\\tool\n\nGo.")
    assert_passes(drive(json.dumps(payload(prompt, cwd=cwd))))


@pytest.mark.parametrize("rest", [
    "",                       # empty
    "   ",                    # blank
    "scripts",                # relative
    "./memstack",             # relative with dot
    "..\\DeedStack",          # relative parent
    "C:\\Projects\\..\\DeedStack",  # dot segment: ambiguous
    "\\\\server\\share\\x",   # UNC: not compared
    "C:\\Projects\\a|b",      # metacharacter
    "the repo root",          # prose
])
def test_malformed_relative_or_empty_declared_path_passes_silently(rest):
    prompt = paste("Working directory: " + rest + "\n\nGo.")
    assert_passes(drive(json.dumps(payload(prompt))))


@pytest.mark.parametrize("cwd", ["", "relative/dir", None, 7])
def test_unusable_cwd_passes_silently(cwd):
    prompt = paste("Working directory: " + OTHER + "\n\nGo.")
    body = payload(prompt)
    body["cwd"] = cwd
    assert_passes(drive(json.dumps(body)))


def test_missing_prompt_passes_silently():
    body = payload("x")
    del body["prompt"]
    assert_passes(drive(json.dumps(body)))


@pytest.mark.parametrize("raw", ["", "not json {", "[1, 2]"])
def test_unreadable_payload_fails_open_and_says_degraded(raw):
    code, out, err = drive(raw)
    assert code == 0
    assert out == ""
    assert err.startswith("workdir-guard: DEGRADED")
    assert len(err.strip().splitlines()) == 1


def test_an_exception_inside_the_decision_fails_open_and_says_degraded(
        monkeypatch):
    def broken(_payload):
        raise RuntimeError("boom")
    monkeypatch.setattr(workdir_guard, "decide", broken)
    prompt = paste("Working directory: " + OTHER + "\n\nGo.")
    out, err = workdir_guard.run(json.dumps(payload(prompt)))
    assert out == ""
    assert err.startswith("workdir-guard: DEGRADED (RuntimeError: boom)")


# --------------------------------------------------------------------------
# the report marker a blocked prompt would have armed
# --------------------------------------------------------------------------

REPORT_PHRASE = "Report per memstack:report"


def _marker_for(prompt, session_id="ups-test", epoch=None):
    return json.dumps({
        "session_id": session_id,
        "requested_at_epoch": time.time() if epoch is None else epoch,
        "prompt_head": " ".join(prompt.split())[:200],
    }).encode("utf-8")


def _scratch_repo(tmp_path):
    """A repo of its own, so no case can reach this repo's real marker. The
    payload cwd points here, and both the guard and verify.py resolve the
    marker path from that cwd."""
    repo = tmp_path / "repo"
    (repo / ".git").mkdir(parents=True)
    (repo / ".memstack").mkdir()
    return repo, repo / ".memstack" / "report-required.json"


def _neutralize(repo, marker, prompt, prior, wait_s):
    return workdir_guard.neutralize_report_marker(
        payload(prompt, cwd=str(repo)), time.time(), marker, prior,
        wait_s=wait_s)


def test_block_on_a_non_arming_prompt_leaves_the_marker_alone(tmp_path):
    repo, marker = _scratch_repo(tmp_path)
    marker.write_bytes(b"prior")
    prompt = paste("Working directory: " + OTHER + "\n\nGo.")
    assert _neutralize(repo, marker, prompt, b"prior", 0.2) == "not-armed"
    assert marker.read_bytes() == b"prior"


def test_block_restores_the_prior_marker_after_the_parallel_write(tmp_path):
    repo, marker = _scratch_repo(tmp_path)
    prompt = paste("Working directory: " + OTHER + "\n\n" + REPORT_PHRASE)
    # report-marker's write, landing after the guard's snapshot of "prior".
    marker.write_bytes(_marker_for(prompt))
    assert _neutralize(repo, marker, prompt, b"prior", 1.0) == "restored"
    assert marker.read_bytes() == b"prior"


def test_block_removes_a_marker_that_did_not_exist_before(tmp_path):
    repo, marker = _scratch_repo(tmp_path)
    prompt = paste("Working directory: " + OTHER + "\n\n" + REPORT_PHRASE)
    marker.write_bytes(_marker_for(prompt))
    assert _neutralize(repo, marker, prompt, None, 1.0) == "removed"
    assert not marker.exists()


def test_marker_written_before_the_snapshot_is_removed(tmp_path):
    # The documented residual: the earlier marker it replaced is gone.
    repo, marker = _scratch_repo(tmp_path)
    prompt = paste("Working directory: " + OTHER + "\n\n" + REPORT_PHRASE)
    early = _marker_for(prompt)
    marker.write_bytes(early)
    assert _neutralize(repo, marker, prompt, early, 0.2) == "removed-early"
    assert not marker.exists()


def test_another_sessions_or_older_marker_is_never_touched(tmp_path):
    repo, marker = _scratch_repo(tmp_path)
    prompt = paste("Working directory: " + OTHER + "\n\n" + REPORT_PHRASE)
    for foreign in (_marker_for(prompt, session_id="someone-else"),
                    _marker_for(prompt, epoch=time.time() - 3600),
                    _marker_for("a different prompt entirely")):
        marker.write_bytes(foreign)
        assert _neutralize(repo, marker, prompt, foreign, 0.2) == "not-seen"
        assert marker.read_bytes() == foreign


def test_early_snapshot_finds_the_marker_from_a_subdirectory(tmp_path):
    repo, marker = _scratch_repo(tmp_path)
    (repo / "sub").mkdir()
    marker.write_bytes(b"prior")
    path, prior = workdir_guard.early_marker_snapshot(
        payload("x", cwd=str(repo / "sub")))
    assert path == marker.resolve()
    assert prior == b"prior"


def test_end_to_end_block_neutralizes_the_real_report_marker(tmp_path):
    """The two real hooks, in parallel, on one payload, in a scratch repo."""
    repo = tmp_path / "repo"
    (repo / ".git").mkdir(parents=True)
    (repo / ".memstack").mkdir()
    marker = repo / ".memstack" / "report-required.json"
    marker.write_bytes(b'{"prior": true}\n')
    prompt = paste("Working directory: " + OTHER + "\n\n" + REPORT_PHRASE)
    raw = json.dumps(payload(prompt, cwd=str(repo))).encode("utf-8")

    guard = subprocess.Popen([sys.executable, GUARD], stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    reporter = subprocess.Popen(
        [sys.executable, os.path.join(REPO_ROOT, "scripts", "verify.py"),
         "report-marker"], stdin=subprocess.PIPE)
    # Both get the payload before either is waited on, as Claude Code does.
    for proc in (guard, reporter):
        proc.stdin.write(raw)
        proc.stdin.close()
    reporter.wait(timeout=30)
    out = guard.stdout.read()
    guard.wait(timeout=30)

    assert json.loads(out.decode("utf-8"))["decision"] == "block"
    assert marker.read_bytes() == b'{"prior": true}\n'


# --------------------------------------------------------------------------
# the shipped path: kill switch, report-marker deferral, run-hook.cmd dispatch
# --------------------------------------------------------------------------

import shutil  # noqa: E402

import verify  # noqa: E402

RUN_HOOK = os.path.join(REPO_ROOT, "hooks", "run-hook.cmd")
MISMATCH = paste("Working directory: " + OTHER + "\n\nGo.")
MATCH = "Working directory: c:/projects/MemStack/\n\nGo."


def test_kill_switch_skips_before_reading_and_says_so():
    code, out, err = drive(json.dumps(payload(MISMATCH)),
                           {"MEMSTACK_NO_WORKDIR_GUARD": "1"})
    assert code == 0
    assert out == ""
    assert err.strip() == ("workdir-guard: SKIPPED, MEMSTACK_NO_WORKDIR_GUARD=1"
                           " is set, so this prompt was NOT examined")


@pytest.mark.parametrize("value", ["0", "true", ""])
def test_kill_switch_takes_only_the_value_one(value):
    assert_blocks(drive(json.dumps(payload(MISMATCH)),
                        {"MEMSTACK_NO_WORKDIR_GUARD": value}),
                  OTHER, SESSION_CWD)


def test_would_block_honours_the_kill_switch(monkeypatch):
    monkeypatch.delenv("MEMSTACK_NO_WORKDIR_GUARD", raising=False)
    assert workdir_guard.would_block(payload(MISMATCH)) is True
    assert workdir_guard.would_block(payload(MATCH)) is False
    monkeypatch.setenv("MEMSTACK_NO_WORKDIR_GUARD", "1")
    assert workdir_guard.would_block(payload(MISMATCH)) is False


def _arm(repo, declared, monkeypatch, tmp_path):
    monkeypatch.setenv("MEMSTACK_REPORT_DIR", str(tmp_path / "reports"))
    prompt = paste("Working directory: " + declared + "\n\n" + REPORT_PHRASE)
    return verify.report_marker_decide(payload(prompt, cwd=str(repo)))


def test_report_marker_arms_nothing_for_a_prompt_the_guard_blocks(
        tmp_path, monkeypatch):
    monkeypatch.delenv("MEMSTACK_NO_WORKDIR_GUARD", raising=False)
    repo, marker = _scratch_repo(tmp_path)
    assert _arm(repo, OTHER, monkeypatch, tmp_path) is None
    assert not marker.exists()


def test_report_marker_still_arms_for_a_prompt_the_guard_passes(
        tmp_path, monkeypatch):
    monkeypatch.delenv("MEMSTACK_NO_WORKDIR_GUARD", raising=False)
    repo, marker = _scratch_repo(tmp_path)
    assert _arm(repo, str(repo), monkeypatch, tmp_path) is not None
    assert marker.exists()


def test_report_marker_arms_when_the_guard_is_switched_off(
        tmp_path, monkeypatch):
    monkeypatch.setenv("MEMSTACK_NO_WORKDIR_GUARD", "1")
    repo, marker = _scratch_repo(tmp_path)
    assert _arm(repo, OTHER, monkeypatch, tmp_path) is not None
    assert marker.exists()


def test_guard_does_not_wait_when_report_marker_is_its_own_sibling(
        tmp_path, monkeypatch):
    monkeypatch.setenv("CLAUDE_PLUGIN_ROOT", REPO_ROOT)
    repo, marker = _scratch_repo(tmp_path)
    prompt = paste("Working directory: " + OTHER + "\n\n" + REPORT_PHRASE)
    started = time.monotonic()
    assert _neutralize(repo, marker, prompt, None, 5.0) == "deferred"
    assert time.monotonic() - started < 2.0


def test_hooks_json_registers_the_guard_once_beside_report_marker():
    with open(os.path.join(REPO_ROOT, "hooks", "hooks.json"),
              encoding="utf-8") as fh:
        hooks = json.load(fh)["hooks"]["UserPromptSubmit"]
    commands = [h["command"] for entry in hooks for h in entry["hooks"]]
    assert sum(c.endswith(" workdir-guard") for c in commands) == 1
    assert sum(c.endswith(" report-marker") for c in commands) == 1
    for command in commands:
        assert ".py" not in command and ".sh" not in command


def _git_bash():
    for candidate in (r"C:\Program Files\Git\bin\bash.exe",
                      r"C:\Program Files (x86)\Git\bin\bash.exe"):
        if os.path.exists(candidate):
            return candidate
    return None if os.name == "nt" else shutil.which("bash")


def _dispatchers():
    found = []
    if os.name == "nt":
        found.append(pytest.param(["cmd.exe", "/d", "/c", RUN_HOOK], id="cmd"))
    bash = _git_bash()
    if bash:
        found.append(pytest.param([bash, RUN_HOOK], id="bash"))
    return found


def _dispatch(argv, prompt, env_extra=None):
    env = dict(os.environ)
    for name in ("MEMSTACK_REPORT_ON_TASK_PROMPTS", "MEMSTACK_REPORT_TRIGGERS",
                 "MEMSTACK_NO_WORKDIR_GUARD", "MEMSTACK_CR_STRIPPED"):
        env.pop(name, None)
    env["CLAUDE_PLUGIN_ROOT"] = REPO_ROOT
    env.update(env_extra or {})
    proc = subprocess.run(argv + ["workdir-guard"],
                          input=json.dumps(payload(prompt)).encode("utf-8"),
                          capture_output=True, env=env, timeout=60,
                          check=False)
    return (proc.returncode, proc.stdout.decode("utf-8"),
            proc.stderr.decode("utf-8"))


@pytest.mark.parametrize("argv", _dispatchers())
def test_shipped_dispatch_forwards_the_decision_json_on_stdout(argv):
    # stdout must be the decision object and nothing else, or Claude Code
    # cannot parse it and the block is decorative.
    assert_blocks(_dispatch(argv, MISMATCH), OTHER, SESSION_CWD)


@pytest.mark.parametrize("argv", _dispatchers())
def test_shipped_dispatch_is_silent_on_a_pass(argv):
    assert_passes(_dispatch(argv, MATCH))


@pytest.mark.parametrize("argv", _dispatchers())
def test_shipped_dispatch_honours_the_kill_switch(argv):
    code, out, err = _dispatch(argv, MISMATCH,
                               {"MEMSTACK_NO_WORKDIR_GUARD": "1"})
    assert (code, out) == (0, "")
    assert "workdir-guard: SKIPPED" in err


@pytest.mark.parametrize("argv", _dispatchers())
def test_shipped_dispatch_without_the_script_degrades_loudly(argv, tmp_path):
    code, out, err = _dispatch(argv, MISMATCH,
                               {"CLAUDE_PLUGIN_ROOT": str(tmp_path)})
    assert (code, out) == (0, "")
    assert "workdir-guard: DEGRADED" in err
