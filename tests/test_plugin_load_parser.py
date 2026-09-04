"""Parser tests for the plugin load gate.

The gate in scripts/check-plugin-load.mjs spawns a real Claude Code process.
These tests do not. They drive the same parser and the same assertions through
scripts/_plugin-load-parse.mjs against fixture traces captured from real runs,
so the rules can be tested in the ordinary suite without a process spawn, a
network call, or a working credential.

The fixtures are real line shapes, trimmed. trace-397 was captured against the
tree at 4c53ac5, trace-398 against the tree at febca9b, and the WARN line in
trace-398-with-frontmatter-warn was captured against a scratch copy of febca9b
carrying the 3.9.7-era code-reviewer escape.

The third fixture is the one that matters most. Its Loaded lines still sum to
86, and the loader still printed "Total plugin skills loaded: 86", because a
skill with unparseable frontmatter is counted and then dropped. Only the WARN
line records the loss. A gate asserting on the sum alone passes that trace.
"""

import json
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
PARSER = REPO_ROOT / "scripts" / "_plugin-load-parse.mjs"
FIXTURES = Path(__file__).resolve().parent / "fixtures" / "plugin-load"

# The manifest shape the fixtures were captured against: 10 declared entries,
# the first consumed as the default skillsPath, so 9 skillsPaths, and 86
# SKILL.md on disk.
MANIFEST_ENTRIES = 10
EXPECTED_SKILLS_PATHS = 9
ON_DISK = 86


def run_parser(fixture_name, plugin_root="-", expected_paths=EXPECTED_SKILLS_PATHS,
               entries=MANIFEST_ENTRIES, on_disk=ON_DISK):
    """Drive the real parser over a fixture and return its JSON report.

    node is required rather than optional. The parser is the thing under test
    and there is no Python copy of it; a skip here would assert nothing while
    reporting something other than failure, which is the exact defect shape the
    gate this parser belongs to exists to catch.
    """
    node = shutil.which("node")
    assert node is not None, (
        "node is not on PATH, so the plugin-load parser cannot be tested. "
        "This repo already requires node for its catalog checks."
    )
    assert PARSER.is_file(), "missing parser module at %s" % PARSER
    fixture = FIXTURES / fixture_name
    assert fixture.is_file(), "missing fixture %s" % fixture

    proc = subprocess.run(
        [node, str(PARSER), str(fixture), "memstack", plugin_root,
         str(expected_paths), str(entries), str(on_disk)],
        capture_output=True, text=True, timeout=60,
    )
    assert proc.returncode == 0, "parser exited %s: %s" % (proc.returncode, proc.stderr[-800:])
    return json.loads(proc.stdout)


def failing(report):
    return {r["name"] for r in report["results"] if r["status"] == "FAIL"}


# ---------------------------------------------------------------------------
# 3.9.7 shape: the skills array was nested under components, so the loader
# never saw it, fell back to the default skills root and registered 18 of 86.
# ---------------------------------------------------------------------------

def test_397_nested_components_fails():
    report = run_parser("trace-397-nested-components.log")
    assert report["verdict"] == "FAIL"
    assert report["parsed"]["skillsPaths"] == 0
    assert report["parsed"]["loadedSum"] == 18
    assert report["parsed"]["loadedLines"] == 1
    assert "Loaded lines sum to SKILL.md on disk" in failing(report)


def test_397_failure_names_the_unregistered_count():
    report = run_parser("trace-397-nested-components.log")
    detail = next(r["detail"] for r in report["results"]
                  if r["name"] == "Loaded lines sum to SKILL.md on disk")
    assert "18" in detail and "86" in detail
    assert "68 skill(s) shipped to disk and were never registered" in detail


# ---------------------------------------------------------------------------
# 3.9.8 shape: skills declared at the top level, all 86 registered.
# ---------------------------------------------------------------------------

def test_398_top_level_skills_passes():
    report = run_parser("trace-398-top-level-skills.log")
    assert report["verdict"] == "PASS"
    assert report["parsed"]["checkedCount"] == 1
    assert report["parsed"]["skillsPaths"] == EXPECTED_SKILLS_PATHS
    assert report["parsed"]["loadedLines"] == EXPECTED_SKILLS_PATHS + 1
    assert report["parsed"]["loadedSum"] == ON_DISK
    assert failing(report) == set()


# ---------------------------------------------------------------------------
# The case the sum cannot see: a skill counted, then dropped.
# ---------------------------------------------------------------------------

def test_frontmatter_warn_fails_even_though_the_sum_is_right():
    report = run_parser("trace-398-with-frontmatter-warn.log")
    # The sum is correct and the path assertion is correct. Only the WARN fails.
    assert report["parsed"]["loadedSum"] == ON_DISK
    assert report["parsed"]["skillsPaths"] == EXPECTED_SKILLS_PATHS
    assert report["verdict"] == "FAIL"
    assert failing(report) == {"no WARN names a SKILL.md in this plugin"}
    assert len(report["parsed"]["warnFrontmatter"]) == 1
    assert "code-reviewer" in report["parsed"]["warnFrontmatter"][0]


def test_frontmatter_warn_detail_explains_why_the_sum_is_not_enough():
    report = run_parser("trace-398-with-frontmatter-warn.log")
    detail = next(r["detail"] for r in report["results"]
                  if r["name"] == "no WARN names a SKILL.md in this plugin")
    assert "dropped before it was offered" in detail


# ---------------------------------------------------------------------------
# Scoping: a WARN about some other plugin's skill must not fail this tree.
# ---------------------------------------------------------------------------

def test_warn_for_another_plugin_is_not_attributed_here(tmp_path):
    src = (FIXTURES / "trace-398-top-level-skills.log").read_text(encoding="utf-8")
    foreign = (
        "2026-09-04T20:40:28.774Z [WARN] Failed to parse YAML frontmatter in "
        "C:\\Other\\plugins\\somebody-else\\skills\\thing\\SKILL.md: "
        "YAML Parse error: Unexpected character\n"
    )
    mixed = tmp_path / "mixed.log"
    mixed.write_text(src + foreign, encoding="utf-8")

    node = shutil.which("node")
    assert node is not None
    proc = subprocess.run(
        [node, str(PARSER), str(mixed), "memstack", "-",
         str(EXPECTED_SKILLS_PATHS), str(MANIFEST_ENTRIES), str(ON_DISK)],
        capture_output=True, text=True, timeout=60,
    )
    assert proc.returncode == 0, proc.stderr[-800:]
    report = json.loads(proc.stdout)
    assert report["parsed"]["warnFrontmatter"] == []
    assert report["verdict"] == "PASS"


# ---------------------------------------------------------------------------
# A trace that never mentions the plugin proves nothing and must not pass.
# ---------------------------------------------------------------------------

def test_absent_plugin_fails(tmp_path):
    empty = tmp_path / "no-plugin.log"
    empty.write_text(
        "2026-09-04T20:40:28.500Z [DEBUG] Error log sink initialized\n",
        encoding="utf-8",
    )
    node = shutil.which("node")
    assert node is not None
    proc = subprocess.run(
        [node, str(PARSER), str(empty), "memstack", "-",
         str(EXPECTED_SKILLS_PATHS), str(MANIFEST_ENTRIES), str(ON_DISK)],
        capture_output=True, text=True, timeout=60,
    )
    assert proc.returncode == 0, proc.stderr[-800:]
    report = json.loads(proc.stdout)
    assert report["verdict"] == "FAIL"
    assert "plugin was checked by the loader" in failing(report)


# ---------------------------------------------------------------------------
# Two plugins of the same name would double every count.
# ---------------------------------------------------------------------------

def test_double_checked_plugin_fails(tmp_path):
    src = (FIXTURES / "trace-398-top-level-skills.log").read_text(encoding="utf-8")
    doubled = tmp_path / "doubled.log"
    doubled.write_text(src + src, encoding="utf-8")

    node = shutil.which("node")
    assert node is not None
    proc = subprocess.run(
        [node, str(PARSER), str(doubled), "memstack", "-",
         str(EXPECTED_SKILLS_PATHS), str(MANIFEST_ENTRIES), str(ON_DISK)],
        capture_output=True, text=True, timeout=60,
    )
    assert proc.returncode == 0, proc.stderr[-800:]
    report = json.loads(proc.stdout)
    assert report["parsed"]["checkedCount"] == 2
    assert report["parsed"]["loadedSum"] == ON_DISK * 2
    assert report["verdict"] == "FAIL"
    assert "plugin was checked by the loader" in failing(report)
