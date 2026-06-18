#!/usr/bin/env python3
"""
lint_skill_docs.py
Read-only audit of every SKILL.md under skills/.

Checks (shell/quote checks are keyed off the fence tag):
  1. UNBALANCED_QUOTES -- odd count of delimiter double-quotes in a SHELL fence
                          (escaped \\" and '...'-quoted " are discounted)
  2. CODE_FENCE        -- unclosed or odd-count fence markers
  3. SHELL_MISMATCH    -- a cross-shell contradiction: bash-only token in a
                          PowerShell/CMD block, or a PS-only cmdlet in a bash block
  4. SUSPICIOUS_FLAGS  -- unusually complex --flags (low confidence, human review)
  5. STALE_VERSION     -- version strings / skill counts (human review)
  6. UNTAGGED_FENCE    -- shell-like content in an untagged fence (tag it; low severity)

No files are modified. Pure Python 3 stdlib. No network. No writes.
"""

import re
import sys
from collections import defaultdict
from pathlib import Path

SKILLS_ROOT = Path("skills")

# Issue type labels
T_QUOTES = "UNBALANCED_QUOTES"
T_FENCE  = "CODE_FENCE"
T_SHELL  = "SHELL_MISMATCH"
T_FLAGS  = "SUSPICIOUS_FLAGS"
T_STALE  = "STALE_VERSION"
T_UNTAGGED = "UNTAGGED_FENCE"

ALL_TYPES = [T_QUOTES, T_FENCE, T_SHELL, T_FLAGS, T_STALE, T_UNTAGGED]

# ---------------------------------------------------------------------------
# Pattern definitions
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Fence-tag categories
# ---------------------------------------------------------------------------
# A quote/shell defect only has meaning relative to the fence's declared
# language, so every shell/quote check below is keyed off the fence tag:
#   - shell-family tag   -> the block is explicitly shell; only a CROSS-shell
#                           contradiction (a bash-only token in a PS/CMD block,
#                           or a PS-only cmdlet in a bash block) is a real bug.
#   - non-shell language -> $VAR / && / || / quotes are that language's own
#                           syntax (yaml, nginx, js, ts, dockerfile, ...);
#                           suppress shell checks entirely.
#   - untagged           -> if the line carries a strong shell signal, emit a
#                           low-severity UNTAGGED_FENCE advisory ("tag it").

BASH_FAMILY_TAGS = {"bash", "sh", "zsh", "shell", "console", "shell-session"}
PS_FAMILY_TAGS   = {"powershell", "pwsh", "ps1", "ps"}
CMD_FAMILY_TAGS  = {"cmd", "bat", "batch"}
SHELL_BLOCK_TAGS = BASH_FAMILY_TAGS | PS_FAMILY_TAGS | CMD_FAMILY_TAGS

# Unambiguous PowerShell-only tokens (wrong inside a bash-family block).
# NOTE: $? and trailing-backtick are intentionally EXCLUDED -- both are valid
# in bash, so they cannot signal a cross-shell mismatch.
PS_ONLY_PATTERNS = [
    (r"\$env:",            "PowerShell $env: variable syntax"),
    (r"\bSet-Variable\b",  "PowerShell Set-Variable cmdlet"),
    (r"\bGet-ChildItem\b", "PowerShell Get-ChildItem cmdlet"),
    (r"\bWrite-Host\b",    "PowerShell Write-Host cmdlet"),
    (r"\bNew-Item\b",      "PowerShell New-Item cmdlet"),
    (r"\bRemove-Item\b",   "PowerShell Remove-Item cmdlet"),
]

# Unambiguous bash-only tokens (wrong inside a PowerShell/CMD block).
BASH_ONLY_PATTERNS = [
    (r"2>/dev/null",      "bash 2>/dev/null redirect (CMD/PS use 2>$null)"),
    (r"#!/",              "bash shebang line"),
    (r"\bexport\s+\w+=",  "bash export VAR=value (CMD uses SET, PS uses $env:)"),
    (r"^\s*\$\s+\S",      "bash $ prompt prefix"),
]

# Known shell command binaries -- used only to gate the untagged-fence advisory.
SHELL_CMDS = (
    r"\b(git|grep|egrep|fgrep|curl|wget|npm|npx|pnpm|yarn|node|python3?|pip3?|"
    r"cd|echo|cat|sed|awk|chmod|chown|mkdir|rmdir|rm|cp|mv|ls|export|source|"
    r"sudo|apt|apt-get|yum|brew|docker|kubectl|ssh|scp|tar|unzip|systemctl|service)\b"
)
SHELL_OPS = r"(\|\||&&|\s\|\s|>>|2>|<<)"


def _odd_shell_quotes(line: str) -> bool:
    """True if the line has an odd number of *delimiter* double-quotes.

    Escaped \\" and any " inside single-quoted '...' spans are literals, not
    delimiters, so they are removed before counting. This keeps a genuinely
    dropped quote (e.g. echo/SKILL.md:50) flagged while clearing grep patterns
    that legitimately carry " inside '...' or as \\".
    """
    s = line.replace('\\"', "")
    s = re.sub(r"'[^']*'", "", s)
    return s.count('"') % 2 != 0


def _has_strong_shell_signal(line: str) -> bool:
    """True if an untagged-fence line looks like a real shell command.

    Deliberately conservative so prose placeholders ([Flat fee: $X], a bare
    $MEMSTACK_PATH in a sentence) do NOT trip it: it requires a recognizable
    command binary combined with a shell operator or flag, an explicit '$ '
    prompt, or a bash-only redirect.
    """
    if re.match(r"^\s*\$\s+\S", line):
        return True
    if re.search(r"2>/dev/null|2>&1", line):
        return True
    if re.search(SHELL_CMDS, line) and (
        re.search(SHELL_OPS, line) or re.search(r"\s--?\w", line)
    ):
        return True
    return False

# Stale version / skill-count patterns (checked outside front matter)
STALE_PATTERNS = [
    (r"\bv\d+\.\d+\.\d+\b",                "version string -- verify against VERSION file"),
    (r"\b\d{2,}\+?\s+skills?\b",            "skill count -- verify against actual catalog size"),
    (r"\b\d{2,}\s+professional\s+skills?\b","professional skill count -- verify against catalog"),
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def is_fence_marker(line: str) -> bool:
    return bool(re.match(r"^\s*```", line))


def get_fence_lang(line: str) -> str:
    m = re.match(r"^\s*```(\w*)", line)
    return m.group(1).lower() if m else ""


def extract_inline_code_spans(line: str):
    """Return list of text strings found inside single-backtick `...` spans."""
    spans = []
    i = 0
    while i < len(line):
        if line[i] == "`":
            j = i + 1
            while j < len(line) and line[j] != "`":
                j += 1
            if j < len(line):
                spans.append(line[i + 1 : j])
                i = j + 1
            else:
                i += 1
        else:
            i += 1
    return spans


def make_issue(file_rel, lineno, itype, offending, explanation):
    text = offending.rstrip()
    if len(text) > 120:
        text = text[:117] + "..."
    return {
        "file": file_rel,
        "line": lineno,
        "issue_type": itype,
        "offending_text": text,
        "explanation": explanation,
    }


# ---------------------------------------------------------------------------
# Per-file lint
# ---------------------------------------------------------------------------

def lint_file(path: Path):
    file_rel = path.as_posix()
    issues = []

    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return [make_issue(file_rel, 0, T_FENCE, "", f"Cannot read file: {exc}")]

    lines = text.splitlines()

    # -- Check 2 (whole-file fence count) -----------------------------------
    fence_count = sum(1 for ln in lines if is_fence_marker(ln))
    if fence_count % 2 != 0:
        issues.append(make_issue(
            file_rel, 0, T_FENCE,
            f"Total ``` markers: {fence_count}",
            f"Odd number of code-fence markers ({fence_count}) -- at least one fence unclosed",
        ))

    # -- Determine front-matter extent (first --- ... --- block) ------------
    fm_start, fm_end = -1, -1
    if lines and lines[0].strip() == "---":
        fm_start = 0
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                fm_end = i
                break

    def in_front_matter(idx):
        return fm_start <= idx <= fm_end

    # -- Per-line scan -------------------------------------------------------
    in_fence = False
    fence_lang = ""
    fence_open_line = 0

    for lineno, raw in enumerate(lines, start=1):
        idx = lineno - 1

        # Skip front matter
        if in_front_matter(idx):
            continue

        # Track code fence state
        if is_fence_marker(raw):
            if not in_fence:
                in_fence = True
                fence_lang = get_fence_lang(raw)
                fence_open_line = lineno
            else:
                in_fence = False
                fence_lang = ""
                fence_open_line = 0
            continue  # skip the fence delimiter line itself

        # -- Check 1: unbalanced quotes (shell fences only) ----------------
        # A dropped quote is only a real defect inside a shell command. In
        # prose, content templates, YAML, dialogue, etc. an odd " count is
        # normal punctuation, so the check is scoped to shell-tagged fences
        # and uses an escaped-/single-quote-aware counter.
        if in_fence and fence_lang in SHELL_BLOCK_TAGS:
            if _odd_shell_quotes(raw):
                issues.append(make_issue(
                    file_rel, lineno, T_QUOTES, raw,
                    "Odd count of delimiter double-quotes in shell command -- likely missing or extra quote",
                ))

        # -- Check 3: shell mismatch / untagged fence ----------------------
        # Keyed off the fence tag (see category notes above):
        #   untagged         -> low-severity UNTAGGED_FENCE advisory when the
        #                       line carries a strong shell signal
        #   bash-family tag  -> flag a PowerShell-only cmdlet (cross-shell bug)
        #   PS/CMD tag       -> flag a bash-only token (cross-shell bug)
        #   non-shell tag    -> suppress (native syntax of that language)
        if in_fence:
            if fence_lang == "":
                if _has_strong_shell_signal(raw):
                    issues.append(make_issue(
                        file_rel, lineno, T_UNTAGGED, raw,
                        "Shell-like content in an untagged fence -- add a language tag (e.g. ```bash)",
                    ))
            elif fence_lang in BASH_FAMILY_TAGS:
                for pat, label in PS_ONLY_PATTERNS:
                    if re.search(pat, raw):
                        issues.append(make_issue(
                            file_rel, lineno, T_SHELL, raw,
                            f"{label} inside a {fence_lang}-tagged block -- cross-shell mismatch",
                        ))
                        break
            elif fence_lang in (PS_FAMILY_TAGS | CMD_FAMILY_TAGS):
                for pat, label in BASH_ONLY_PATTERNS:
                    if re.search(pat, raw):
                        issues.append(make_issue(
                            file_rel, lineno, T_SHELL, raw,
                            f"{label} inside a {fence_lang}-tagged block -- cross-shell mismatch",
                        ))
                        break
            # else: declared non-shell language -> no shell check

        # -- Check 4: suspicious flags (code blocks only, low confidence) --
        # Only flag real --flag-name patterns (must contain at least one letter/digit word).
        # Markdown table separators like |------|------| are excluded because each
        # hyphen-only token has no alphanumeric characters in any word part.
        if in_fence:
            for m in re.finditer(r"--([a-z0-9][a-z0-9-]*)", raw, re.IGNORECASE):
                flag_name = m.group(1)
                parts = [p for p in flag_name.split("-") if p]  # skip empty from leading/trailing -
                # Require 4+ non-empty word parts AND each part must have a letter or digit
                if len(parts) >= 4 and all(re.search(r"[a-z0-9]", p, re.IGNORECASE) for p in parts):
                    issues.append(make_issue(
                        file_rel, lineno, T_FLAGS, raw,
                        f"[LOW CONFIDENCE] Complex flag '--{flag_name}' ({len(parts)} parts) -- verify it still exists",
                    ))
                    break  # one per line

        # -- Check 5: stale version/count strings (anywhere except FM) -----
        for pat, label in STALE_PATTERNS:
            m = re.search(pat, raw, re.IGNORECASE)
            if m:
                issues.append(make_issue(
                    file_rel, lineno, T_STALE, raw,
                    f"Stale candidate '{m.group()}' -- {label}",
                ))
                break  # one stale issue per line

    # Fence never closed
    if in_fence:
        issues.append(make_issue(
            file_rel, fence_open_line, T_FENCE,
            f"Fence opened at line {fence_open_line} (lang: {fence_lang or 'untagged'})",
            "Code fence opened but never closed before end of file",
        ))

    return issues


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    # Force UTF-8 output so emoji/Unicode in skill text does not crash on cp1252 terminals.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    if not SKILLS_ROOT.exists():
        print(f"ERROR: directory not found: {SKILLS_ROOT.resolve()}", file=sys.stderr)
        sys.exit(1)

    skill_files = sorted(SKILLS_ROOT.rglob("SKILL.md"))
    total_scanned = len(skill_files)

    all_issues = []
    files_with_issues = set()

    for sp in skill_files:
        file_issues = lint_file(sp)
        all_issues.extend(file_issues)
        if file_issues:
            files_with_issues.add(sp.as_posix())

    # Counts by type
    type_counts = {t: 0 for t in ALL_TYPES}
    for iss in all_issues:
        t = iss["issue_type"]
        if t in type_counts:
            type_counts[t] += 1

    total_issues = len(all_issues)
    skills_affected = len(files_with_issues)

    SEP  = "=" * 70
    SEP2 = "-" * 60

    print(SEP)
    print("SKILL.md LINT REPORT")
    print(SEP)
    print(f"Total SKILL.md files scanned : {total_scanned}")
    print(f"Skills with >= 1 issue       : {skills_affected}")
    print(f"Total issues found           : {total_issues}")
    print()
    print("Breakdown by issue type:")
    print(f"  [1] UNBALANCED_QUOTES : {type_counts[T_QUOTES]}")
    print(f"  [2] CODE_FENCE        : {type_counts[T_FENCE]}")
    print(f"  [3] SHELL_MISMATCH    : {type_counts[T_SHELL]}  (cross-shell contradiction)")
    print(f"  [4] SUSPICIOUS_FLAGS  : {type_counts[T_FLAGS]}  (low confidence -- human review only)")
    print(f"  [5] STALE_VERSION     : {type_counts[T_STALE]}  (human review vs VERSION file)")
    print(f"  [6] UNTAGGED_FENCE    : {type_counts[T_UNTAGGED]}  (low severity -- add a language tag)")
    print(SEP)
    print()

    if not all_issues:
        print("No issues found.")
        return

    # Punch list grouped by file
    by_file = defaultdict(list)
    for iss in all_issues:
        by_file[iss["file"]].append(iss)

    for fpath in sorted(by_file.keys()):
        print(f"FILE: {fpath}")
        print(SEP2)
        for iss in sorted(by_file[fpath], key=lambda x: x["line"]):
            line_label = f"LINE {iss['line']:>4}" if iss["line"] > 0 else "FILE-LEVEL "
            print(f"  {line_label} | [{iss['issue_type']}]")
            print(f"             Text : {iss['offending_text']}")
            print(f"             Why  : {iss['explanation']}")
        print()


if __name__ == "__main__":
    main()
