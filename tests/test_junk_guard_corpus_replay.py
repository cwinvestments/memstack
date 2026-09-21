"""Replay the junk-write guard's classifier over real command history.

WHY THIS IS A TEST AND NOT A NOTE IN A CHANGELOG

The guard's rules were calibrated by replaying them over thousands of real
commands until they blocked none of them. That calibration was true on the day
it was done and had no way of staying true: the next person to tighten a rule
would have had nothing telling them they had just started blocking a shape this
project uses forty times a week. Committing the corpus and replaying it on
every run of the check chain is what converts a one-time measurement into a
standing constraint.

WHAT IS ACTUALLY UNDER TEST

Not a copy of the rules. The classifier source is read out of the shipped hook
file and the half above its REPLAY_SPLIT marker is exec'd here, so the rules
replayed are the rules customers receive. Editing the hook changes this result
on the next run, and deleting the marker fails the suite rather than silently
replaying nothing.

THE TWO CORPUS SLICES

The observation monitor truncates command text at 120 characters. A clipped
command has unbalanced quotes and a severed final token by construction, so the
guard blocking one is correct behaviour on the text it was given and says
nothing about false blocks. Only the full-text slice carries the zero-false-
block guarantee; the clipped slice is carried in the fixture for provenance and
is reported, not asserted on.

PROVENANCE OF THE FIXTURE

tests/fixtures/junk-guard-corpus.jsonl, built from this project's own session
transcripts and PostToolUse observation logs. Every record was scanned against
six credential shapes and any match was dropped whole rather than redacted,
because a redacted command is no longer the command that was run. One record
was dropped. The scan was re-run against the written file and found nothing.
"""

import io
import json
import os

import pytest

from conftest import JUNK_GUARD, REPO_ROOT

CORPUS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "fixtures", "junk-guard-corpus.jsonl")


def load_shipped_classifier():
    """Exec the classifier out of the hook file, above its REPLAY_SPLIT marker."""
    text = io.open(JUNK_GUARD, encoding="utf-8", newline="").read()

    opener = "PYSRC=\"$(cat " + chr(60) * 2 + "'PYEOF'"
    assert opener in text, (
        "the hook no longer opens its embedded classifier with the expected "
        "heredoc, so the replay cannot find the source that ships")
    assert "# REPLAY_SPLIT" in text, (
        "the REPLAY_SPLIT marker is gone from the hook. It is what tells this "
        "replay where the decision functions end; without it the replay would "
        "silently test nothing")

    start = text.index("\n", text.index(opener)) + 1
    end = text.index("# REPLAY_SPLIT")
    namespace = {"__name__": "replay_classifier"}
    exec(compile(text[start:end], JUNK_GUARD + " (embedded classifier)", "exec"),
         namespace)
    return namespace["judge_command"]


def load_corpus():
    records = []
    with io.open(CORPUS, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


@pytest.fixture(scope="module")
def judge():
    return load_shipped_classifier()


@pytest.fixture(scope="module")
def corpus():
    return load_corpus()


def test_the_corpus_fixture_is_present_and_shaped(corpus):
    assert len(corpus) > 2000, "the corpus is far smaller than it should be"
    assert {"command", "source", "truncated"} <= set(corpus[0])
    full = [r for r in corpus if not r["truncated"]]
    assert len(full) > 1500, "the full-text slice carries the guarantee"


def test_no_false_block_against_the_full_text_corpus(judge, corpus):
    """The load-bearing assertion.

    Every one of these commands was really run in this project and none of them
    created a junk file, so every block here is a false block. The failure
    message reports the count and the reasons, never a command: a historical
    command can carry a value this test has no way to recognise.
    """
    full = [r for r in corpus if not r["truncated"]]

    blocked = []
    for record in full:
        target, reason = judge(record["command"], REPO_ROOT)
        if target:
            blocked.append((reason.split(",")[0], target, record["source"]))

    if blocked:
        by_reason = {}
        for reason, target, source in blocked:
            by_reason.setdefault(reason, []).append(target)
        lines = ["%d false block(s) against %d real commands."
                 % (len(blocked), len(full)),
                 "Targets are printed; the commands they came from are not.",
                 ""]
        for reason in sorted(by_reason, key=lambda r: -len(by_reason[r])):
            targets = sorted(set(by_reason[reason]))
            lines.append("  %-34s %4d   targets: %s"
                         % (reason, len(by_reason[reason]),
                            ", ".join(targets[:8])
                            + (" ..." if len(targets) > 8 else "")))
        pytest.fail("\n".join(lines))


def test_the_clipped_slice_is_reported_not_asserted(judge, corpus, capsys):
    """The clipped slice cannot carry the guarantee, and is measured anyway.

    A sharp rise here is still a signal worth seeing, it just is not a failure:
    these commands are missing their last characters, so their quoting is
    broken by construction.
    """
    clipped = [r for r in corpus if r["truncated"]]
    blocked = sum(1 for r in clipped if judge(r["command"], REPO_ROOT)[0])
    with capsys.disabled():
        print("\n    clipped slice: %d of %d would block "
              "(expected, not asserted: these are cut at 120 characters)"
              % (blocked, len(clipped)))
    assert len(clipped) > 0, "the clipped slice vanished from the fixture"
