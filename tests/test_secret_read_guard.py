"""Controls for hooks/secret-read-guard across its three matchers.

Migrated from two scratchpad harnesses, secret-read-guard-controls.py (Read and
Bash) and the first half of guard-controls-2.py (Grep). Every assertion from
both is preserved; what changed is that they now run inside the check chain
instead of being a thing somebody remembered to run once.
"""

import json
import os
import shutil
import subprocess

import pytest

from conftest import (SECRET_GUARD, assert_verdict, needs_bash, run_guard)

pytestmark = needs_bash

# A fragment of the redacted-copy recipe, and of its output shape. Asserting on
# these is what proves the block message teaches rather than merely refuses.
RECIPE = "python -c 'import re,sys;p=re.compile("
REDACTED = '"=[REDACTED]"'

# git-bash carries coreutils in /usr/bin and no python, which is how the
# fail-open path is reached without uninstalling anything.
NO_PYTHON_PATH = "/usr/bin"
_no_python_available = any(
    os.path.exists(os.path.join(NO_PYTHON_PATH, name))
    for name in ("python", "python3", "py", "python.exe", "python3.exe"))
needs_python_free_path = pytest.mark.skipif(
    _no_python_available,
    reason="%s has a python on it, so the fail-open path cannot be reached"
           % NO_PYTHON_PATH)


def read(path, project_dir, path_override=None):
    return run_guard(SECRET_GUARD, "Read", {"file_path": path},
                     cwd=project_dir, project_dir=project_dir,
                     path_override=path_override)


def bash(command, project_dir):
    return run_guard(SECRET_GUARD, "Bash", {"command": command},
                     cwd=project_dir, project_dir=project_dir)


def grep(tool_input, project_dir, path_override=None):
    return run_guard(SECRET_GUARD, "Grep", tool_input,
                     cwd=project_dir, project_dir=project_dir,
                     path_override=path_override)


# --------------------------------------------------------------- the Read rule

def test_read_of_env_blocks_with_the_redacted_copy_recipe(plain_repo):
    rc, err = read(plain_repo + "/.env", plain_repo)
    assert_verdict(rc, 2, err,
                   must_have=["BLOCKED: Read of .env", RECIPE, REDACTED,
                              "Then Read DST"],
                   # only the basename is ever echoed, never the caller's path
                   must_not_have=[plain_repo])


def test_read_of_env_example_allows(plain_repo):
    rc, err = read(plain_repo + "/.env.example", plain_repo)
    assert_verdict(rc, 0, err, must_not_have=["BLOCKED"])


@pytest.mark.parametrize("name", [
    ".env", ".env.local", ".env.production", "config.local.json", ".npmrc",
    ".netrc", "server.pem", "cert.pfx", "cert.p12", "id_rsa", "id_ed25519",
    "deploy_rsa", "credentials.json", "credentials-prod.json",
    "terraform.tfvars", "secrets.yml", "app.secrets.json",
])
def test_every_builtin_pattern_matches(plain_repo, name):
    """One case per pattern, so a typo in the list cannot hide behind a sibling."""
    rc, err = read(plain_repo + "/" + name, plain_repo)
    assert_verdict(rc, 2, err, must_have=["BLOCKED: Read of " + name])


def test_matching_is_case_insensitive(plain_repo):
    rc, err = read(plain_repo + "/.ENV", plain_repo)
    assert_verdict(rc, 2, err, must_have=["BLOCKED"])


@pytest.mark.parametrize("name", [
    ".env.example", ".env.sample", "secrets.example.json",
    "config.local.json.example",
])
def test_sample_counterparts_stay_readable(plain_repo, name):
    """Reading a sample is how a session learns the names without a value."""
    rc, err = read(plain_repo + "/" + name, plain_repo)
    assert_verdict(rc, 0, err, must_not_have=["BLOCKED"])


def test_the_redacted_copy_is_readable(plain_repo):
    """If the recipe's own output were refused, the recipe would be a dead end."""
    rc, err = read(plain_repo + "/env-redacted.txt", plain_repo)
    assert_verdict(rc, 0, err, must_not_have=["BLOCKED"])


# --------------------------------------------------------------- the Bash rule

def test_cat_of_env_blocks_with_all_three_safe_recipes(plain_repo):
    rc, err = bash("cat .env", plain_repo)
    assert_verdict(rc, 2, err, must_have=[
        "BLOCKED: this Bash command reads .env whole.",
        "A. Analysis, on a redacted copy",
        "B. Presence check",
        "grep -n -o PATTERN SRC",
        "C. Value comparison",
        "sha256sum SRC",
        RECIPE,
    ])


@pytest.mark.parametrize("verb,command", [
    ("cat", "cat .env"),
    ("type", "type .env"),
    ("head", "head -5 .env"),
    ("tail", "tail -n 20 .env"),
    ("more", "more .env"),
    ("less", "less .env"),
    ("strings", "strings .env"),
    ("sed", "sed -n 1,5p .env"),
    ("awk", "awk '{print}' .env"),
])
def test_every_blocked_verb(plain_repo, verb, command):
    rc, err = bash(command, plain_repo)
    assert_verdict(rc, 2, err, must_have=["BLOCKED"])


def test_cat_of_an_ordinary_file_allows(plain_repo):
    rc, err = bash("cat ordinary.txt", plain_repo)
    assert_verdict(rc, 0, err, must_not_have=["BLOCKED"])


def test_grep_whole_line_blocks(plain_repo):
    rc, err = bash("grep SENDGRID .env", plain_repo)
    assert_verdict(rc, 2, err, must_have=["BLOCKED"])


def test_grep_only_matching_allows(plain_repo):
    """The -o form prints the match, not the line, so it cannot carry a value."""
    rc, err = bash("grep -n -o SENDGRID .env", plain_repo)
    assert_verdict(rc, 0, err, must_not_have=["BLOCKED"])


def test_hashing_pipeline_allows(plain_repo):
    rc, err = bash("cat .env | sha256sum", plain_repo)
    assert_verdict(rc, 0, err, must_not_have=["BLOCKED"])


@pytest.mark.parametrize("command", [
    "wc -l .env", "stat .env", "ls -la .env", "test -f .env",
    "sha256sum .env", "shasum -a 256 .env",
])
def test_property_only_verbs_allow(plain_repo, command):
    rc, err = bash(command, plain_repo)
    assert_verdict(rc, 0, err, must_not_have=["BLOCKED"])


def test_the_approved_fingerprint_pipeline_allows(plain_repo):
    """The secrets policy's own per-variable fingerprint recipe must survive."""
    rc, err = bash(
        "grep '^API_KEY=' .env | cut -d= -f2- | tr -d '\"' | sha256sum | cut -c1-8",
        plain_repo)
    assert_verdict(rc, 0, err, must_not_have=["BLOCKED"])


def test_names_only_inspection_allows(plain_repo):
    rc, err = bash("cut -d= -f1 .env | grep -vE '^#|^$' | sort", plain_repo)
    assert_verdict(rc, 0, err, must_not_have=["BLOCKED"])


def test_tee_defeats_the_hash_allowance(plain_repo):
    """tee copies the bytes to stdout on the way past, so the pipeline prints."""
    rc, err = bash("cat .env | tee copy.txt | sha256sum", plain_repo)
    assert_verdict(rc, 2, err, must_have=["BLOCKED"])


def test_a_trailing_segment_is_judged_separately(plain_repo):
    rc, err = bash("cat .env | sha256sum ; cat .env", plain_repo)
    assert_verdict(rc, 2, err, must_have=["BLOCKED"])


@pytest.mark.parametrize("command", [
    "echo API_KEY=x > .env",
    "printf 'x\\n' >> .env",
])
def test_writing_to_the_path_is_not_reading_it(plain_repo, command):
    rc, err = bash(command, plain_repo)
    assert_verdict(rc, 0, err, must_not_have=["BLOCKED"])


def test_searching_the_tree_for_the_string_env_allows(plain_repo):
    """The false positive that would have made the gate unusable."""
    rc, err = bash("grep -rn '\\.env' src/", plain_repo)
    assert_verdict(rc, 0, err, must_not_have=["BLOCKED"])


def test_absolute_posix_path_blocks(plain_repo):
    rc, err = bash("cat " + plain_repo + "/.env", plain_repo)
    assert_verdict(rc, 2, err, must_have=["BLOCKED"])


def test_windows_shaped_path_blocks(plain_repo):
    rc, err = bash("cat C:\\Projects\\somewhere\\.env", plain_repo)
    assert_verdict(rc, 2, err, must_have=["BLOCKED"])


def test_an_unmodelled_verb_allows(plain_repo):
    """The documented boundary: a deliberate gap, not a silent block."""
    rc, err = bash("node scripts/load-config.js .env", plain_repo)
    assert_verdict(rc, 0, err, must_not_have=["BLOCKED"])


# ------------------------------------------------------- the .secretpaths hook

def test_custom_name_allows_without_secretpaths(plain_repo):
    """The positive half of the pair.

    Without it, a guard that blocked every unknown name would look exactly
    like a working extension mechanism.
    """
    rc, err = bash("cat vault-token.conf", plain_repo)
    assert_verdict(rc, 0, err, must_not_have=["BLOCKED"])


def test_secretpaths_entry_extends_the_bash_rule(ext_repo):
    rc, err = bash("cat vault-token.conf", ext_repo)
    assert_verdict(rc, 2, err, must_have=[
        "BLOCKED: this Bash command reads vault-token.conf whole."])


def test_secretpaths_entry_extends_the_read_rule(ext_repo):
    rc, err = read(ext_repo + "/vault-token.conf", ext_repo)
    assert_verdict(rc, 2, err,
                   must_have=["BLOCKED: Read of vault-token.conf"])


# --------------------------------------------------------------- the Grep rule

def test_grep_content_mode_on_env_blocks_with_all_three_recipes(plain_repo):
    rc, err = grep({"pattern": "KEY", "path": plain_repo + "/.env",
                    "output_mode": "content"}, plain_repo)
    assert_verdict(rc, 2, err, must_have=[
        "BLOCKED: this Grep would print matching lines out of .env.",
        'output_mode: "files_with_matches"',
        "A. Analysis, on a redacted copy",
        "B. Presence check",
        "C. Value comparison",
        RECIPE,
    ])


@pytest.mark.parametrize("mode", ["files_with_matches", "count"])
def test_grep_non_content_modes_allow(plain_repo, mode):
    """Names and counts cannot carry a value, so they are always allowed."""
    rc, err = grep({"pattern": "KEY", "path": plain_repo + "/.env",
                    "output_mode": mode}, plain_repo)
    assert_verdict(rc, 0, err, must_not_have=["BLOCKED"])


def test_grep_with_output_mode_absent_allows(plain_repo):
    """The load-bearing finding from the payload probe.

    output_mode is ABSENT from the payload when the caller omits it, rather
    than arriving as its default. A rule written as output_mode == "content"
    is correct only because absence is resolved first.
    """
    rc, err = grep({"pattern": "KEY", "path": plain_repo + "/.env"}, plain_repo)
    assert_verdict(rc, 0, err, must_not_have=["BLOCKED"])


def test_grep_content_mode_aimed_by_glob_at_env_blocks(plain_repo):
    rc, err = grep({"pattern": "KEY", "glob": "**/.env",
                    "output_mode": "content"}, plain_repo)
    assert_verdict(rc, 2, err, must_have=[
        "BLOCKED: this Grep would print matching lines out of .env."])


def test_grep_content_mode_aimed_by_glob_at_pem_blocks(plain_repo):
    rc, err = grep({"pattern": "KEY", "glob": "*.pem",
                    "output_mode": "content"}, plain_repo)
    assert_verdict(rc, 2, err, must_have=["BLOCKED"])


def test_grep_content_mode_over_ordinary_source_allows(plain_repo):
    rc, err = grep({"pattern": "KEY", "glob": "**/*.ts",
                    "output_mode": "content"}, plain_repo)
    assert_verdict(rc, 0, err, must_not_have=["BLOCKED"])


def test_grep_content_mode_on_env_example_allows(plain_repo):
    rc, err = grep({"pattern": "KEY", "path": plain_repo + "/.env.example",
                    "output_mode": "content"}, plain_repo)
    assert_verdict(rc, 0, err, must_not_have=["BLOCKED"])


def test_grep_content_mode_on_a_directory_allows(plain_repo):
    """A documented hole, asserted so it stays documented rather than becoming
    a surprise the day somebody widens the rule."""
    rc, err = grep({"pattern": "KEY", "path": plain_repo,
                    "output_mode": "content"}, plain_repo)
    assert_verdict(rc, 0, err, must_not_have=["BLOCKED"])


def test_grep_glob_naming_no_shape_allows(plain_repo):
    """The other documented hole."""
    rc, err = grep({"pattern": "KEY", "glob": "**/*",
                    "output_mode": "content"}, plain_repo)
    assert_verdict(rc, 0, err, must_not_have=["BLOCKED"])


# ------------------------------------------------------------------- posture

def test_another_tool_is_untouched(plain_repo):
    rc, err = run_guard(SECRET_GUARD, "Write",
                        {"file_path": plain_repo + "/.env", "content": "x"},
                        cwd=plain_repo, project_dir=plain_repo)
    assert_verdict(rc, 0, err, must_not_have=["BLOCKED"])


def test_an_unparseable_payload_fails_open_loudly(plain_repo):
    proc = subprocess.run(["bash", SECRET_GUARD], input="not json at all",
                          capture_output=True, text=True,
                          env=dict(os.environ, CLAUDE_PROJECT_DIR=plain_repo))
    assert_verdict(proc.returncode, 0, proc.stderr,
                   must_have=["secret-read-guard: DEGRADED", "did NOT run"])


@needs_python_free_path
def test_no_python_emits_the_degraded_warning_and_allows(plain_repo):
    rc, err = read(plain_repo + "/.env", plain_repo,
                   path_override=NO_PYTHON_PATH)
    assert_verdict(rc, 0, err,
                   must_have=["secret-read-guard: DEGRADED",
                              "no python interpreter", "did NOT run"],
                   must_not_have=["BLOCKED"])


@needs_python_free_path
def test_grep_matcher_fails_open_loudly_with_no_python(plain_repo):
    rc, err = grep({"pattern": "x", "path": plain_repo + "/.env",
                    "output_mode": "content"}, plain_repo,
                   path_override=NO_PYTHON_PATH)
    assert_verdict(rc, 0, err,
                   must_have=["secret-read-guard: DEGRADED", "did NOT run"],
                   must_not_have=["BLOCKED"])


# --------------------------------------------------------------- kill switch

def test_kill_switch_skips_the_guard_entirely(plain_repo):
    """MEMSTACK_NO_SECRET_GUARD=1 allows a call the guard would have blocked,
    and says so, so a disabled guard is never mistaken for a clean pass."""
    payload = json.dumps({
        "hook_event_name": "PreToolUse",
        "tool_name": "Read",
        "tool_input": {"file_path": plain_repo + "/.env"},
        "cwd": plain_repo,
    })
    env = dict(os.environ, CLAUDE_PROJECT_DIR=plain_repo,
               MEMSTACK_NO_SECRET_GUARD="1")
    proc = subprocess.run(["bash", SECRET_GUARD], input=payload,
                          capture_output=True, text=True, env=env)
    assert_verdict(proc.returncode, 0, proc.stderr,
                   must_have=["secret-read-guard: SKIPPED",
                              "MEMSTACK_NO_SECRET_GUARD=1",
                              "NOT examined"],
                   must_not_have=["BLOCKED"])
    assert len(proc.stderr.strip().splitlines()) == 1, "the note is one line"
