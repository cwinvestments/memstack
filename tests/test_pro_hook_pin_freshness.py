"""Does memstack-pro's derivation pin still describe this repo's hook tree?

memstack-pro does not author `.claude/hooks/`. It carries a byte copy of THIS
repo's tree at a pinned commit, recorded in its tracked `hooks-derived-from.txt`,
with exactly one sanctioned difference: `session-start.sh`, which adds the Pro
license nudge.

memstack-pro already guards its half of that contract. `scripts/check-hook-derivation.sh`
there asks whether Pro's copy still matches the pinned commit, and it turns red
when somebody edits a derived file in Pro or adds a file the pin does not have.

What nothing asked, until this file, is whether the PIN IS STILL CURRENT. That
guard compares Pro against memstack at 194f7ef; it never compares 194f7ef
against memstack now. Fix a hook here, commit it, leave the pin alone, and Pro
still matches the commit it names: the downstream guard prints its green line,
and the copy customers receive is stale with nothing anywhere saying so. That is
the direction the drift actually ran the last time, when it was found five
months late.

So the check belongs HERE, in the repo where the divergence originates, and it
fires on the commit that causes it rather than waiting for someone to push the
repo that suffers it. The repair is still downstream, and the failure message
says so in those words.

`session-start.sh` is excluded because it is the sanctioned delta: it differs in
Pro by design, and the downstream guard owns its bounds (no skill-loader block,
no DevLog webhook). This file asserts nothing about it.

Skips are honest, not convenient. A customer clone has no memstack-pro beside
it and has nothing to compare, so it skips with a reason; a missing or malformed
pin file and an unresolvable pinned commit likewise. What it must never do is
pass while checking nothing, which is why the file list is asserted non-empty
before any comparison: if `.claude/hooks` is ever renamed or moved out from under
this test, two empty lists would otherwise compare equal and report success.
"""

import os
import re
import subprocess

import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# memstack-pro sits beside this repo on the maintainer machine. The environment
# variable is the override, mirroring MEMSTACK_CANONICAL_REPO which the guard on
# the other side already uses to find this one.
PRO_REPO = os.environ.get(
    "MEMSTACK_PRO_REPO",
    os.path.join(os.path.dirname(REPO_ROOT), "memstack-pro"),
)

PIN_FILE = os.path.join(PRO_REPO, "hooks-derived-from.txt")

HOOKS_PREFIX = ".claude/hooks"

# The sanctioned Pro delta. Named once, here.
ALLOWED_DIFF = "session-start.sh"

_SHA_RE = re.compile(r"\A[0-9a-f]{40}\Z")


def _git(*args, binary=False):
    """Run git in this repo. Returns (returncode, stdout).

    stdout stays bytes for blob reads: a hook is compared byte for byte, and
    decoding it first would make the comparison depend on a codec rather than
    on the file.
    """
    proc = subprocess.run(
        ("git", "-C", REPO_ROOT) + args,
        capture_output=True,
        check=False,
    )
    out = proc.stdout if binary else proc.stdout.decode("utf-8", "replace")
    return proc.returncode, out


def _hook_names(rev):
    """Base names under .claude/hooks at rev, minus the sanctioned delta."""
    rc, out = _git("ls-tree", "-r", "--name-only", rev, "--", HOOKS_PREFIX)
    if rc != 0:
        return None
    names = set()
    for line in out.splitlines():
        line = line.strip()
        if not line.startswith(HOOKS_PREFIX + "/"):
            continue
        name = line[len(HOOKS_PREFIX) + 1:]
        if name and name != ALLOWED_DIFF:
            names.add(name)
    return names


def _blob(rev, name):
    """Bytes of .claude/hooks/<name> at rev, or None when it is not there.

    Read through `git show` on both sides on purpose: the object database holds
    LF regardless of what `core.autocrlf` did to the working tree, so both sides
    arrive normalized and nothing here has to strip a CR. A working-tree compare
    would be red on every file on this machine, where memstack checks out CRLF
    and memstack-pro pins `*.sh text eol=lf`.
    """
    rc, out = _git("show", "%s:%s/%s" % (rev, HOOKS_PREFIX, name), binary=True)
    return out if rc == 0 else None


def _moved_by(pin, name):
    """The commits that touched this hook between the pin and HEAD."""
    rc, out = _git("log", "--oneline", "%s..HEAD" % pin, "--",
                   "%s/%s" % (HOOKS_PREFIX, name))
    if rc != 0 or not out.strip():
        return ["(no commit range available)"]
    return [line.rstrip() for line in out.splitlines() if line.strip()]


def _read_pin():
    """The pinned sha, or a reason it cannot be read."""
    if not os.path.isdir(PRO_REPO):
        return None, ("memstack-pro is not present at %s, so there is no "
                      "derivation pin to check; this is the expected result on "
                      "a machine that was never given that repo" % PRO_REPO)
    if not os.path.isfile(PIN_FILE):
        return None, ("memstack-pro has no hooks-derived-from.txt at %s, so the "
                      "pin it should record is missing" % PIN_FILE)
    with open(PIN_FILE, "r", encoding="utf-8") as fh:
        pin = fh.read().strip()
    if not _SHA_RE.match(pin):
        return None, ("hooks-derived-from.txt at %s does not hold a 40 character "
                      "commit sha, so the pin cannot be resolved" % PIN_FILE)
    return pin, None


def test_pro_derivation_pin_still_matches_this_repos_hook_tree():
    """Canonical must not advance past the commit memstack-pro derives from.

    Red here means the copy shipped to Pro customers is behind this repo. The
    repair is in memstack-pro, not in this file.
    """
    pin, why_not = _read_pin()
    if pin is None:
        pytest.skip(why_not)

    rc, _ = _git("rev-parse", "--verify", "--quiet", "%s^{commit}" % pin)
    if rc != 0:
        pytest.skip(
            "memstack-pro pins commit %s, which does not resolve in this repo; "
            "the pin may name a rewritten or unfetched commit" % pin)

    pinned = _hook_names(pin)
    current = _hook_names("HEAD")
    assert pinned is not None and current is not None, (
        "could not list %s at %s or at HEAD" % (HOOKS_PREFIX, pin))

    # A check over nothing is worse than no check: two empty sets compare equal
    # and report success. If this tree is ever moved, say so instead.
    assert pinned or current, (
        "%s holds no files at either %s or HEAD, so this test would have "
        "compared nothing and passed. If the hook tree moved, move this test "
        "with it." % (HOOKS_PREFIX, pin))

    problems = []
    for name in sorted(pinned | current):
        at_pin = _blob(pin, name)
        at_head = _blob("HEAD", name)
        if at_pin == at_head:
            continue
        if at_pin is None:
            what = "added here after the pin"
        elif at_head is None:
            what = "deleted here after the pin"
        else:
            what = "changed here after the pin"
        problems.append("  %s: %s" % (name, what))
        for line in _moved_by(pin, name):
            problems.append("      %s" % line)

    rc, head = _git("rev-parse", "--short", "HEAD")
    head = head.strip() if rc == 0 else "HEAD"

    assert not problems, (
        "CANONICAL HOOKS HAVE ADVANCED PAST THE PRO DERIVATION PIN\n"
        "\n"
        "  pin       %s\n"
        "  recorded  %s\n"
        "  this repo %s (HEAD)\n"
        "\n"
        "%s\n"
        "\n"
        "memstack-pro ships a byte copy of this tree taken at the pinned commit,\n"
        "so every file above is a fix customers of Pro are not receiving. The\n"
        "obligation is downstream and it is two steps: re-derive the changed\n"
        "files into memstack-pro/.claude/hooks, then move the sha in\n"
        "memstack-pro/hooks-derived-from.txt to this repo's HEAD. Its own\n"
        "scripts/check-hook-derivation.sh will confirm the result.\n"
        "\n"
        "%s is excluded from this comparison and always will be: it is the\n"
        "sanctioned Pro delta carrying the license nudge.\n"
        "\n"
        "Do not edit this test to make it pass. If a hook here is deliberately\n"
        "not going to Pro, that decision belongs in memstack-pro's CLAUDE.md and\n"
        "in its guard's allow list, where the next reader will find it."
        % (pin, PIN_FILE, head, "\n".join(problems), ALLOWED_DIFF))
