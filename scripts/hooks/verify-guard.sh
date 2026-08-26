#!/usr/bin/env bash
#
# GIT-GUARD per-repo verification recipe
# -------------------------------------------------------------------------
# Proves that the pre-commit secrets guard ACTUALLY BLOCKS in THIS repo.
#
#   Usage:  bash C:/Projects/memstack/scripts/hooks/verify-guard.sh [repo-dir]
#           (defaults to the current directory)
#
# WHY THIS EXISTS
#   On 2026-08-22 the guard printed "COMMIT BLOCKED - SECRET DETECTED" in
#   AlgoStack and created the commit anyway. Root cause: when the guard's
#   stderr is a pipe that closes early (`git commit ... 2>&1 | head -5`), the
#   shell is killed by SIGPIPE before reaching `exit 1` - and Git for Windows
#   reports a signal-killed hook as exit status 0, i.e. "allow".
#
#   Whether it triggers is a WRITE/READ RACE, so it is timing- and
#   repo-dependent: a clean result in one repo proves NOTHING about another.
#   Hence this script - run it in every repo that relies on the guard.
#
# SAFETY
#   - Refuses to run if anything is already staged (never entangles your work).
#   - Stages ONLY its own probe file.
#   - Never runs `git reset --hard`; undoes any commit it provokes with
#     `reset --soft` and verifies HEAD is back where it started.
#   - Exits non-zero if the guard failed, if cleanup did not fully restore, OR if
#     the probe never reached the index (a run that cannot arm its probe proves
#     nothing and must not report a pass).
# -------------------------------------------------------------------------

set -uo pipefail

REPO="${1:-$PWD}"
PROBE="_gitguard_verify_probe.py"
# Fabricated, non-credential value shaped to match gitleaks' generic-api-key.
# Assembled from fragments at runtime so this source file holds no token-shaped
# literal of its own; as one, it would be flagged by the very guard it verifies,
# blocking the commit that ships this harness. The bytes written to the probe
# file are identical either way, so what is tested is unchanged.
PROBE_NAME="session_token"
PROBE_VALUE="abcdef012345"
PROBE_LINE="$PROBE_NAME = \"$PROBE_VALUE\""

cd "$REPO" || { echo "VERIFY: cannot cd to $REPO"; exit 2; }

if ! git rev-parse --git-dir >/dev/null 2>&1; then
    echo "VERIFY: $REPO is not a git repository"; exit 2
fi

REPO_TOP="$(git rev-parse --show-toplevel)"
START_HEAD="$(git rev-parse HEAD 2>/dev/null || echo NONE)"

if [ "$START_HEAD" = "NONE" ]; then
    echo "VERIFY: repo has no commits yet - make one first"; exit 2
fi

if [ -n "$(git diff --cached --name-only)" ]; then
    echo "VERIFY: REFUSING - you have staged changes. Commit or unstage first."
    exit 2
fi

if [ -e "$PROBE" ]; then
    echo "VERIFY: REFUSING - $PROBE already exists in $REPO_TOP"; exit 2
fi

echo "GIT-GUARD verification"
echo "  repo : $REPO_TOP"
echo "  HEAD : $START_HEAD"
echo ""

FAILURES=0
PASSES=0

attempt() {
    # $1 = human label, $2 = "" for unpiped or a head -N line count
    local label="$1" n="$2" out rc before after saw_guard

    printf '%s\n' "$PROBE_LINE" > "$PROBE"
    # -f because a deny-by-default .gitignore (an allowlist rooted at `/*`) would
    # otherwise make `git add` refuse the probe. The probe is this harness's own
    # temporary file, staged and removed inside this function, so forcing it past
    # ignore rules changes nothing the repo cares about.
    git add -f -- "$PROBE" >/dev/null 2>&1

    # A verification that cannot prove its probe was armed must fail, not pass.
    # Without this, an add that silently refuses leaves nothing staged, `git commit`
    # returns 1 for "nothing to commit", HEAD is unchanged - and every check below
    # reads that as the guard blocking. That is a green run with the guard never
    # invoked. -f closes the known ignore hole; this closes every unknown refusal
    # mode of the same shape.
    if [ -z "$(git diff --cached --name-only -- "$PROBE")" ]; then
        echo ""
        echo "  VERIFY: PROBE NEVER STAGED - $PROBE is not in the index after 'git add -f'."
        echo "  VERIFY: This run proves NOTHING about the guard; it was never invoked."
        echo "  VERIFY: at attempt: $label"
        rm -f -- "$PROBE"
        echo ""
        echo "RESULT: FAIL - harness could not arm its probe."
        exit 2
    fi

    before="$(git rev-parse HEAD)"

    if [ -z "$n" ]; then
        out="$(git commit -m "gitguard verify probe" 2>&1)"
        rc=$?
    else
        # The exact shape that exposed the SIGPIPE defect.
        out="$(git commit -m "gitguard verify probe" 2>&1 | head -"$n")"
        rc=${PIPESTATUS[0]}
    fi

    after="$(git rev-parse HEAD)"
    saw_guard="no"
    case "$out" in *"GIT-GUARD"*) saw_guard="yes";; esac

    if [ "$before" != "$after" ]; then
        echo "  FAIL  $label - COMMIT WAS CREATED (git rc=$rc, guard msg=$saw_guard)"
        git reset --soft "$before" >/dev/null 2>&1
        FAILURES=$((FAILURES + 1))
    elif [ "$saw_guard" = "no" ] && [ -n "$n" ] && [ "$n" -ge 4 ]; then
        # Blocked, but silently - the user would not know why.
        echo "  WARN  $label - blocked (rc=$rc) but no GIT-GUARD message visible"
        PASSES=$((PASSES + 1))
    else
        echo "  ok    $label - blocked (git rc=$rc, guard msg=$saw_guard)"
        PASSES=$((PASSES + 1))
    fi

    git reset -q -- "$PROBE" >/dev/null 2>&1
    rm -f -- "$PROBE"
}

attempt "unpiped                " ""
for n in 1 2 3 4 5 6 8 20; do
    attempt "piped through head -$(printf '%-2s' "$n")" "$n"
done

echo ""
# ---- cleanup / restoration assertions -----------------------------------
END_HEAD="$(git rev-parse HEAD)"
LEFTOVER="no"
[ -e "$PROBE" ] && LEFTOVER="yes"
STILL_STAGED="$(git diff --cached --name-only -- "$PROBE")"

echo "  HEAD unchanged      : $([ "$START_HEAD" = "$END_HEAD" ] && echo yes || echo "NO - was $START_HEAD now $END_HEAD")"
echo "  probe file removed  : $([ "$LEFTOVER" = "no" ] && echo yes || echo NO)"
echo "  probe unstaged      : $([ -z "$STILL_STAGED" ] && echo yes || echo NO)"
echo ""

if [ "$FAILURES" -gt 0 ]; then
    echo "RESULT: FAIL - the guard did NOT block $FAILURES of $((PASSES + FAILURES)) attempts."
    exit 1
fi
if [ "$START_HEAD" != "$END_HEAD" ] || [ "$LEFTOVER" = "yes" ] || [ -n "$STILL_STAGED" ]; then
    echo "RESULT: FAIL - cleanup did not fully restore the repo."
    exit 1
fi

echo "RESULT: PASS - guard blocked all $PASSES attempts; repo restored."
exit 0
