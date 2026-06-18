#!/usr/bin/env python3
"""
verify_lint_tuning.py
Proof harness for the tuned SKILL.md linter (scripts/lint_skill_docs.py).

Two jobs:
  1. Golden-defect regression guard (always): assert the known-real defects
     still flag in the CURRENT linter. Exits non-zero if any is missing.
  2. Before/after suppression audit (optional, --before <old_script>): run an
     OLD copy of the linter and the current one, diff the flag sets, and prove
     that:
       - all golden defects are present in BOTH runs (caught before, survived),
       - no golden defect is in the suppressed set,
       - every suppressed item belongs to a known false-positive class
         (only UNBALANCED_QUOTES / SHELL_MISMATCH are ever removed; the
         STALE_VERSION / CODE_FENCE / SUSPICIOUS_FLAGS logic is untouched).

Read-only. Runs the linters as subprocesses; modifies nothing.

Usage:
  python scripts/verify_lint_tuning.py
  python scripts/verify_lint_tuning.py --before /path/to/lint_skill_docs.before.py
"""

import argparse
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CURRENT_LINTER = REPO_ROOT / "scripts" / "lint_skill_docs.py"

# The known-real defects that MUST keep flagging after tuning.
GOLDEN = [
    ("skills/echo/SKILL.md", 50, "UNBALANCED_QUOTES"),
    ("skills/business/licensing/SKILL.md", 181, "STALE_VERSION"),
    ("skills/deployment/hetzner-setup/SKILL.md", 202, "STALE_VERSION"),
]

# Types the tuning is allowed to suppress. Anything else removed is a regression.
SUPPRESSIBLE_TYPES = {"UNBALANCED_QUOTES", "SHELL_MISMATCH"}

FILE_RE = re.compile(r"^FILE:\s+(.+?)\s*$")
LINE_RE = re.compile(r"^\s*LINE\s+(\d+)\s+\|\s+\[(\w+)\]")
FILELVL_RE = re.compile(r"^\s*FILE-LEVEL\s*\|\s+\[(\w+)\]")


def run_linter(script: Path):
    """Run a linter script from REPO_ROOT, return set of (file, line, type)."""
    proc = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    flags = set()
    cur = None
    for ln in proc.stdout.splitlines():
        m = FILE_RE.match(ln)
        if m:
            cur = m.group(1)
            continue
        m = LINE_RE.match(ln)
        if m and cur:
            flags.add((cur, int(m.group(1)), m.group(2)))
            continue
        m = FILELVL_RE.match(ln)
        if m and cur:
            flags.add((cur, 0, m.group(1)))
    return flags


def fence_tag_at(rel_path: str, lineno: int) -> str:
    """Best-effort: the fence tag enclosing a given 1-based line (for the audit)."""
    p = REPO_ROOT / rel_path
    try:
        lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return "?"
    in_fence = False
    lang = ""
    for n, raw in enumerate(lines, start=1):
        if re.match(r"^\s*```", raw):
            if not in_fence:
                in_fence = True
                m = re.match(r"^\s*```(\w*)", raw)
                lang = (m.group(1).lower() if m and m.group(1) else "UNTAGGED")
            else:
                in_fence = False
                lang = ""
            continue
        if n == lineno:
            return lang if in_fence else "PROSE"
    return "?"


def counts_by_type(flags):
    c = Counter(t for _, _, t in flags)
    return c


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--before", help="path to the pre-tuning linter for a before/after audit")
    args = ap.parse_args()

    failures = []

    after = run_linter(CURRENT_LINTER)

    # ---- Job 1: golden-defect assertions against the current linter --------
    print("=" * 70)
    print("GOLDEN-DEFECT ASSERTIONS (current linter)")
    print("=" * 70)
    for g in GOLDEN:
        ok = g in after
        print(f"  [{'PASS' if ok else 'FAIL'}] {g[2]:18s} {g[0]}:{g[1]}")
        if not ok:
            failures.append(f"golden defect missing after tuning: {g}")
    print()

    # ---- Job 2: before/after suppression audit -----------------------------
    if args.before:
        before_path = Path(args.before).resolve()
        if not before_path.exists():
            print(f"ERROR: --before script not found: {before_path}", file=sys.stderr)
            sys.exit(2)
        before = run_linter(before_path)

        suppressed = before - after
        added = after - before

        bc, ac = counts_by_type(before), counts_by_type(after)
        all_types = sorted(set(bc) | set(ac))

        print("=" * 70)
        print("PER-CLASS COUNTS  (before -> after)")
        print("=" * 70)
        print(f"  {'TYPE':20s} {'BEFORE':>7s} {'AFTER':>7s} {'DELTA':>7s}")
        for t in all_types:
            b, a = bc.get(t, 0), ac.get(t, 0)
            print(f"  {t:20s} {b:>7d} {a:>7d} {a - b:>+7d}")
        print(f"  {'-'*20} {'-'*7} {'-'*7} {'-'*7}")
        print(f"  {'TOTAL':20s} {len(before):>7d} {len(after):>7d} {len(after) - len(before):>+7d}")
        print()

        # Assertion A: golden defects present in BOTH runs.
        print("ASSERTION: golden defects caught before AND survived after")
        for g in GOLDEN:
            in_b, in_a = g in before, g in after
            ok = in_b and in_a
            print(f"  [{'PASS' if ok else 'FAIL'}] before={in_b} after={in_a}  {g[2]} {g[0]}:{g[1]}")
            if not ok:
                failures.append(f"golden defect not in both before/after: {g}")
        print()

        # Assertion B: no golden defect was suppressed.
        print("ASSERTION: no golden defect in the suppressed set")
        gold_suppressed = [g for g in GOLDEN if g in suppressed]
        if gold_suppressed:
            for g in gold_suppressed:
                print(f"  [FAIL] suppressed golden defect: {g}")
                failures.append(f"golden defect suppressed: {g}")
        else:
            print("  [PASS] none of the golden defects were suppressed")
        print()

        # Assertion C: every suppressed item is a known FP class.
        print("ASSERTION: every suppressed flag is a suppressible FP class")
        bad = [s for s in suppressed if s[2] not in SUPPRESSIBLE_TYPES]
        if bad:
            for s in sorted(bad):
                print(f"  [FAIL] non-FP type suppressed: {s[2]} {s[0]}:{s[1]}")
                failures.append(f"non-FP type suppressed: {s}")
        else:
            print(f"  [PASS] all {len(suppressed)} suppressed flags are in {sorted(SUPPRESSIBLE_TYPES)}")
        print()

        # Assertion D: untouched checks did not lose anything.
        print("ASSERTION: STALE_VERSION / CODE_FENCE / SUSPICIOUS_FLAGS unchanged")
        for t in ("STALE_VERSION", "CODE_FENCE", "SUSPICIOUS_FLAGS"):
            ok = bc.get(t, 0) == ac.get(t, 0)
            print(f"  [{'PASS' if ok else 'FAIL'}] {t:18s} {bc.get(t,0)} -> {ac.get(t,0)}")
            if not ok:
                failures.append(f"untouched check changed: {t}")
        print()

        # Breakdown: suppressed flags grouped by class, bucketed by fence tag.
        print("=" * 70)
        print("SUPPRESSED BREAKDOWN  (by issue type x enclosing fence tag)")
        print("=" * 70)
        for t in sorted(SUPPRESSIBLE_TYPES):
            items = [s for s in suppressed if s[2] == t]
            if not items:
                continue
            tagc = Counter(fence_tag_at(f, n) if n else "FILE-LEVEL" for f, n, _ in items)
            print(f"  {t}  ({len(items)} suppressed)")
            for tag, cnt in sorted(tagc.items(), key=lambda x: -x[1]):
                print(f"      {cnt:4d}  fence tag = {tag}")
        print()

        if added:
            print("=" * 70)
            print(f"NEW FLAGS introduced by tuning ({len(added)})")
            print("=" * 70)
            for f, n, t in sorted(added):
                print(f"  {t:18s} {f}:{n}")
            print()

    # ---- Verdict -----------------------------------------------------------
    print("=" * 70)
    if failures:
        print(f"RESULT: FAIL ({len(failures)} problem(s))")
        for msg in failures:
            print(f"  - {msg}")
        sys.exit(1)
    print("RESULT: PASS -- all golden defects survived; no real defect suppressed")
    print("=" * 70)


if __name__ == "__main__":
    main()
