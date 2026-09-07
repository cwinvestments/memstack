#!/usr/bin/env python
"""doctor: report which MemStack pieces are installed here and whether they agree.

MemStack ships as three separable parts: the marketplace plugin, the PyPI
loader, and Pro. Nothing on a customer's machine reports which of them is
present or whether their versions belong together, so every disagreement so far
has been found by counting by hand. A plugin shipped 87 skills while a session
registered 18. A dashboard reported a version eight months stale. A plugin
update did not take effect until a restart. All three were invisible until
somebody looked.

Usage:
    python scripts/doctor.py
    python scripts/doctor.py --json

Exit codes:
    0  every record is OK or WARN
    1  at least one record is FAIL
    64 usage error, because argparse's own default of 2 collides with the
       verify gate's reserved code and these two scripts are read together

Design notes that are load-bearing, not decoration:

  - Environment variables are reported by NAME, followed by "set" or "unset"
    and nothing else. Never a value, never a prefix of one, never a length,
    never a fingerprint. No .env file is read, opened or parsed anywhere in
    this file. A diagnostic that people run when something is broken and paste
    into a chat window is the last place a credential should be able to reach.

  - Output is ASCII only. The Windows console is cp1252, and a status glyph
    would raise UnicodeEncodeError on exactly the machine that most needs to
    run this. Every detail string is forced through an ASCII pass before it
    is printed.

  - A missing piece is WARN, not FAIL. A plugin-only install with no loader is
    a supported install, and a doctor that fails on a supported install teaches
    people to ignore its output. FAIL is reserved for two pieces that are both
    present and contradict each other, plus a file that exists but cannot be
    read as what it claims to be.

  - Every check takes its inputs as keyword arguments with defaults. No check
    function reads os.environ, Path.home or a module global directly, so the
    tests can inject a fake home, a fake environment, a fake repo root and a
    fake import probe without touching the machine they run on.

  - The declared skill count is derived exactly the way
    scripts/check-manifest-skills.mjs derives it: one level deep from each
    directory the manifest declares. A second, independently invented notion of
    "how many skills there are" is how the counts drifted in the first place.
"""

from __future__ import annotations

import argparse
import importlib
import importlib.metadata
import importlib.util
import json
import os
import re
import sys
import tempfile
from pathlib import Path, PurePosixPath
from typing import NamedTuple

EXIT_OK = 0
EXIT_FAIL = 1
EXIT_USAGE = 64

OK = "OK"
WARN = "WARN"
FAIL = "FAIL"

REPO_ROOT = Path(__file__).resolve().parents[1]

PLUGIN_NAME = "memstack"
MANIFEST_REL = ".claude-plugin/plugin.json"
HOOKS_REL = "hooks/hooks.json"
SKILLS_REL = "skills"
DEPRECATED_REL = SKILLS_REL + "/_deprecated"
SESSIONS_REL = "memory/sessions"

REPORT_DIR_ENV = "MEMSTACK_REPORT_DIR"
CONFIG_DIR_ENV = "CLAUDE_CONFIG_DIR"

# Known-good pairings, keyed by the plugin's major.minor series and holding the
# oldest loader that series works with. Seeded with the 3.9 series, which is
# where plugin.json stands as this file is written, paired against the 4.18
# loader that ships alongside it.
#
# This table earns its keep by hand because there is nothing to derive it
# from: the plugin and the loader live in separate repos, versioned on
# separate tracks that RELEASING.md says are deliberately never forced to
# match. Whether a given loader version actually works with a given plugin
# series is a fact somebody checked by running them together, not something
# either version number implies by itself.
#
# Add or update a row here, in this file, at the same time a release bumps
# either the plugin's minor series (RELEASING.md) or the loader's own
# version (memstack-skill-loader/VERSIONING.md), whenever that bump changes
# which pairing is actually known good.
#
# A pair the table does not mention is WARN, not FAIL. The table is a record of
# what somebody has actually checked, and treating silence as a verdict would
# make every future release start out broken.
KNOWN_GOOD_PAIRS = {
    "3.9": "4.18.0",
}

# The loader's importable module name and its PyPI distribution name. These
# are the same two strings default_loader_probe has always used; hoisted here
# so the source and metadata readings share one spelling of each.
LOADER_MODULE = "memstack_skill_loader"
LOADER_DISTRIBUTION = "memstack-skill-loader"

# Reported by name only. Adding a name here is safe; nothing in this file ever
# reads one of these values into a string that gets printed.
ENV_NAMES = (
    "MEMSTACK_REPORT_DIR",
    "MEMSTACK_ENABLE_TTS",
    "MEMSTACK_DEVLOG_WEBHOOK",
    "DEVLOG_KEY",
    "ANTHROPIC_BASE_URL",
    "CLAUDE_CONFIG_DIR",
)

# A hook command names its script through the plugin root placeholder. This
# pulls the path out of the command string without running anything: captured
# text is never handed back to a shell here.
_PLUGIN_ROOT_TOKEN = re.compile(r"\$\{?CLAUDE_PLUGIN_ROOT\}?([^\"'\s]*)")


class Record(NamedTuple):
    """One check's verdict: a status, a stable name, and a one-line reason."""

    status: str
    name: str
    detail: str


def _ascii(text: str) -> str:
    """ASCII, one line. Paths and exception text can carry neither safely."""
    flat = " ".join(str(text).split())
    return flat.encode("ascii", "replace").decode("ascii")


def _record(status: str, name: str, detail: str) -> Record:
    return Record(status, name, _ascii(detail))


def _read_json(path: Path):
    """Parsed JSON, or a reason string explaining why not."""
    try:
        return json.loads(path.read_text(encoding="utf-8-sig")), None
    except FileNotFoundError:
        return None, "file not found"
    except OSError as exc:
        return None, "unreadable: " + exc.__class__.__name__
    except ValueError as exc:
        return None, "not valid JSON: " + str(exc)


def _version_tuple(text: str) -> tuple:
    """Split a dotted version into integers. No third-party parser involved.

    A component that is not purely numeric contributes its leading digits, so
    a pre-release suffix sorts with its own release rather than crashing.
    """
    parts = []
    for chunk in str(text).strip().split("."):
        digits = ""
        for ch in chunk:
            if not ch.isdigit():
                break
            digits += ch
        parts.append(int(digits) if digits else 0)
    return tuple(parts)


def _series(text: str) -> str:
    """The major.minor series of a version, which is what the table keys on."""
    parts = str(text).strip().split(".")
    return ".".join(parts[:2]) if len(parts) >= 2 else str(text).strip()


# --------------------------------------------------------------------------
# 1. plugin install
# --------------------------------------------------------------------------

def plugin_config_candidates(*, env=None, home=None) -> list:
    """Every path installed_plugins.json could occupy, most specific first."""
    env = os.environ if env is None else env
    home = Path.home() if home is None else Path(home)

    out = []
    raw = (env.get(CONFIG_DIR_ENV) or "").strip()
    if raw:
        base = Path(raw).expanduser()
        out.append(base / "plugins" / "installed_plugins.json")
        out.append(base / "installed_plugins.json")
    out.append(home / ".claude" / "plugins" / "installed_plugins.json")
    return out


def installed_plugin_info(*, env=None, home=None, candidates=None,
                          plugin_name=PLUGIN_NAME) -> dict:
    """Locate and read the plugin registry. Never raises.

    Returns a dict with keys: path, error, version, install_path, probed.
    The record builder and the version-pairing check both read this, so the
    registry is located and parsed exactly once per run.
    """
    paths = (list(candidates) if candidates is not None
             else plugin_config_candidates(env=env, home=home))
    info = {"path": None, "error": None, "version": None,
            "install_path": None, "probed": [str(p) for p in paths]}

    found = None
    for candidate in paths:
        try:
            if Path(candidate).is_file():
                found = Path(candidate)
                break
        except OSError:
            continue

    if found is None:
        return info
    info["path"] = str(found)

    data, why = _read_json(found)
    if why is not None:
        info["error"] = why
        return info
    if not isinstance(data, dict):
        info["error"] = "not valid JSON: top level is not an object"
        return info

    plugins = data.get("plugins")
    if not isinstance(plugins, dict):
        info["error"] = "no plugins object in installed_plugins.json"
        return info

    for key, value in plugins.items():
        if str(key).split("@")[0] != plugin_name:
            continue
        entries = value if isinstance(value, list) else [value]
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            info["version"] = str(entry.get("version") or "") or None
            info["install_path"] = str(entry.get("installPath") or "") or None
            return info
    return info


def check_plugin_install(*, info=None, env=None, home=None,
                         candidates=None, plugin_name=PLUGIN_NAME) -> Record:
    if info is None:
        info = installed_plugin_info(env=env, home=home, candidates=candidates,
                                     plugin_name=plugin_name)
    name = "plugin install"

    if info["path"] is None:
        return _record(
            WARN, name,
            "no installed_plugins.json found at any probed path ("
            + str(len(info["probed"])) + " probed, first "
            + (info["probed"][0] if info["probed"] else "none") + ")",
        )
    if info["error"] is not None:
        return _record(FAIL, name,
                       info["path"] + " " + info["error"])
    if info["version"] is None:
        return _record(WARN, name,
                       "registry at " + info["path"] + " lists no "
                       + plugin_name + " plugin, so nothing is installed from"
                       " the marketplace")
    return _record(OK, name,
                   "version " + info["version"] + " cached at "
                   + (info["install_path"] or "an unrecorded path"))


# --------------------------------------------------------------------------
# 2. skill count
# --------------------------------------------------------------------------

def _normalise_declared(raw: str) -> str:
    """"./skills/" and "skills" both become "skills"; "." becomes "".

    Copied in behaviour from check-manifest-skills.mjs on purpose. Two
    normalisers that disagree would produce two counts that disagree.
    """
    text = str(raw).replace("\\", "/").strip()
    if text.startswith("./"):
        text = text[2:]
    while text.endswith("/"):
        text = text[:-1]
    return "" if text == "." else text


def skill_files_on_disk(*, root=REPO_ROOT) -> list:
    """Every SKILL.md under skills/, excluding the deprecated shelf."""
    skills_root = Path(root) / SKILLS_REL
    if not skills_root.is_dir():
        return []
    out = []
    for path in sorted(skills_root.rglob("SKILL.md")):
        rel = path.relative_to(Path(root)).as_posix()
        if rel.startswith(DEPRECATED_REL + "/"):
            continue
        out.append(rel)
    return out


def skill_files_registered(*, root=REPO_ROOT, declared=()) -> set:
    """The SKILL.md files the manifest actually registers.

    Claude Code scans each declared directory one level deep: SKILL.md in the
    directory itself, and SKILL.md in each immediate subdirectory. Nothing
    below that is reachable, which is why the count is derived rather than
    read from a number somebody typed.
    """
    root = Path(root)
    hits = set()
    for entry in declared:
        rel_dir = _normalise_declared(entry)
        base = root if rel_dir == "" else root / rel_dir
        if not base.is_dir():
            continue
        prefix = "" if rel_dir == "" else rel_dir + "/"
        if (base / "SKILL.md").is_file():
            hits.add(prefix + "SKILL.md")
        try:
            children = sorted(base.iterdir())
        except OSError:
            continue
        for child in children:
            if child.is_dir() and (child / "SKILL.md").is_file():
                hits.add(prefix + child.name + "/SKILL.md")
    return {h for h in hits if not h.startswith(DEPRECATED_REL + "/")}


def check_skill_count(*, root=REPO_ROOT) -> Record:
    root = Path(root)
    name = "skill count"

    manifest_path = root / MANIFEST_REL
    manifest, why = _read_json(manifest_path)
    if why is not None:
        return _record(FAIL, name, MANIFEST_REL + " " + why)
    if not isinstance(manifest, dict) or not isinstance(manifest.get("skills"), list):
        return _record(FAIL, name,
                       MANIFEST_REL + " has no top-level skills array, so the"
                       " manifest declares nothing")

    on_disk = skill_files_on_disk(root=root)
    if not on_disk:
        return _record(FAIL, name,
                       "no SKILL.md found under " + SKILLS_REL + "/")

    registered = skill_files_registered(root=root, declared=manifest["skills"])
    if len(on_disk) == len(registered):
        return _record(OK, name,
                       str(len(on_disk)) + " SKILL.md on disk and the manifest"
                       " registers all " + str(len(registered)))

    missing = sorted(set(on_disk) - registered)
    extra = sorted(registered - set(on_disk))
    detail = ("disk holds " + str(len(on_disk)) + " SKILL.md but the manifest"
              " registers " + str(len(registered)))
    if missing:
        detail += "; unregistered: " + ", ".join(missing[:3])
        if len(missing) > 3:
            detail += " and " + str(len(missing) - 3) + " more"
    if extra:
        detail += "; registered but not counted: " + ", ".join(extra[:3])
    return _record(FAIL, name, detail)


# --------------------------------------------------------------------------
# 3. loader
# --------------------------------------------------------------------------

def _loader_source_version(*, module=LOADER_MODULE):
    """The loader's own __version__, read from the package the interpreter
    actually imports. This is the version that will run, and it does not
    depend on separately-installed dist-info metadata staying in sync with it.

    Returns None if the package is absent, uninstalled, or has no __version__
    attribute. Never raises.
    """
    try:
        spec = importlib.util.find_spec(module)
        if spec is None:
            return None
        return importlib.import_module(module).__version__
    except (ImportError, AttributeError):
        return None


def _loader_metadata_version(*, distribution=LOADER_DISTRIBUTION):
    """The version recorded in installed dist-info metadata. Diagnostic only:
    an editable install whose dist-info is never recreated after a version
    bump leaves this stale while the imported source keeps moving.

    Returns None if the distribution has no metadata registered here. Never
    raises.
    """
    try:
        return importlib.metadata.version(distribution)
    except (ImportError, AttributeError, importlib.metadata.PackageNotFoundError):
        return None


def default_loader_probe(*, source=_loader_source_version,
                         metadata=_loader_metadata_version) -> tuple:
    """Probe the PyPI loader. Returns (present, version, reason). Never raises.

    The reported version is always the source reading, because that is the
    code that will actually run. The metadata reading is diagnostic only: it
    exists so a stale editable install, which reports one version while
    running another, gets caught here instead of on a customer machine.
    """
    source_version = source()
    if source_version is None:
        return (False, None, "not installed")

    metadata_version = metadata()
    if metadata_version is None or metadata_version == source_version:
        return (True, source_version, None)

    return (True, source_version,
            "installed dist-info metadata says " + metadata_version
            + " but the imported package is " + source_version
            + "; the installed metadata is stale, reinstall the package"
            " (a pip editable reinstall) to fix it")


def check_loader(*, probe=default_loader_probe) -> Record:
    name = "loader"
    present, version, reason = probe()

    if not present:
        return _record(WARN, name,
                       "memstack_skill_loader is " + (reason or "not installed")
                       + "; a plugin-only install is valid, so this is not a"
                       " failure")
    if not version:
        return _record(WARN, name, reason or "version unknown")
    if reason:
        return _record(WARN, name, reason)
    return _record(OK, name, "memstack_skill_loader " + version + " importable")


# --------------------------------------------------------------------------
# 4. version pairing
# --------------------------------------------------------------------------

def check_version_pair(*, plugin_version=None, loader_version=None,
                       pairs=KNOWN_GOOD_PAIRS) -> Record:
    name = "version pair"

    if not plugin_version:
        return _record(WARN, name,
                       "no installed plugin version to pair, so nothing was"
                       " compared")
    if not loader_version:
        return _record(WARN, name,
                       "no loader version to pair with plugin "
                       + str(plugin_version) + ", so nothing was compared")

    series = _series(plugin_version)
    minimum = pairs.get(series)
    if minimum is None:
        return _record(WARN, name,
                       "unknown pair: plugin " + str(plugin_version)
                       + " with loader " + str(loader_version)
                       + " is not in the known-good table")
    if _version_tuple(loader_version) >= _version_tuple(minimum):
        return _record(OK, name,
                       "plugin " + str(plugin_version) + " with loader "
                       + str(loader_version) + " meets the known-good minimum "
                       + minimum)
    return _record(FAIL, name,
                   "plugin " + str(plugin_version) + " needs loader " + minimum
                   + " or newer and this machine has " + str(loader_version))


# --------------------------------------------------------------------------
# 5. hooks
# --------------------------------------------------------------------------

def _hook_label(command: str) -> str:
    """The name a hook goes by: its trailing argument, else its script name."""
    tokens = [t for t in str(command).replace('"', " ").replace("'", " ").split() if t]
    if not tokens:
        return "unnamed"
    if len(tokens) >= 2:
        return tokens[-1]
    return PurePosixPath(tokens[0].replace("\\", "/")).name


def _hook_script(command: str, *, root: Path):
    """The on-disk path a hook command points at, or None if it names none."""
    match = _PLUGIN_ROOT_TOKEN.search(str(command))
    if match is None:
        return None
    rel = match.group(1).replace("\\", "/").lstrip("/")
    return (root / rel) if rel else None


def check_hooks(*, root=REPO_ROOT) -> Record:
    root = Path(root)
    name = "hooks"

    data, why = _read_json(root / HOOKS_REL)
    if why is not None:
        return _record(FAIL, name, HOOKS_REL + " " + why)
    if not isinstance(data, dict) or not isinstance(data.get("hooks"), dict):
        return _record(FAIL, name,
                       HOOKS_REL + " has no hooks object, so the plugin"
                       " registers nothing")

    labels = []
    missing = []
    for event, groups in sorted(data["hooks"].items()):
        if not isinstance(groups, list):
            return _record(FAIL, name,
                           HOOKS_REL + " event " + str(event)
                           + " is not a list of matcher groups")
        for group in groups:
            if not isinstance(group, dict):
                continue
            for hook in group.get("hooks") or []:
                if not isinstance(hook, dict):
                    continue
                command = str(hook.get("command") or "")
                labels.append(str(event) + ":" + _hook_label(command))
                script = _hook_script(command, root=root)
                if script is not None and not script.exists():
                    missing.append(script.relative_to(root).as_posix()
                                   if str(script).startswith(str(root))
                                   else str(script))

    if not labels:
        return _record(FAIL, name,
                       HOOKS_REL + " declares events but registers no hook"
                       " commands")
    listing = str(len(labels)) + " registered: " + ", ".join(labels)
    if missing:
        return _record(WARN, name,
                       listing + "; script missing on disk: "
                       + ", ".join(sorted(set(missing))))
    return _record(OK, name, listing)


# --------------------------------------------------------------------------
# 6. directories
# --------------------------------------------------------------------------

def report_dir(*, env=None, home=None) -> Path:
    """Where reports land: MEMSTACK_REPORT_DIR, else ~/.memstack/reports.

    The same rule scripts/verify.py applies, restated here against an injected
    environment so a test never has to mutate the real one.
    """
    env = os.environ if env is None else env
    home = Path.home() if home is None else Path(home)
    raw = (env.get(REPORT_DIR_ENV) or "").strip()
    if raw:
        return Path(raw).expanduser()
    return home / ".memstack" / "reports"


def _writable(path: Path):
    """True if a file can be created and removed here. Cleans up either way."""
    handle = None
    temp_name = None
    try:
        handle, temp_name = tempfile.mkstemp(prefix=".memstack-doctor-", dir=str(path))
        return True, None
    except OSError as exc:
        return False, exc.__class__.__name__
    finally:
        if handle is not None:
            try:
                os.close(handle)
            except OSError:
                pass
        if temp_name is not None:
            try:
                os.unlink(temp_name)
            except OSError:
                pass


def check_directory(*, path, name) -> Record:
    path = Path(path)
    if not path.exists():
        return _record(WARN, name, "does not exist yet: " + str(path))
    if not path.is_dir():
        return _record(FAIL, name, "exists but is not a directory: " + str(path))
    ok, why = _writable(path)
    if not ok:
        return _record(FAIL, name,
                       "exists but is not writable (" + str(why) + "): " + str(path))
    return _record(OK, name, "present and writable: " + str(path))


def check_directories(*, root=REPO_ROOT, env=None, home=None) -> list:
    """The two directories a working install writes to. One record each."""
    return [
        check_directory(path=report_dir(env=env, home=home), name="report dir"),
        check_directory(path=Path(root) / SESSIONS_REL, name="sessions dir"),
    ]


# --------------------------------------------------------------------------
# 7. environment
# --------------------------------------------------------------------------

def check_environment(*, env=None, names=ENV_NAMES) -> Record:
    """Names and set-or-unset. Nothing else ever leaves this function.

    No value, no prefix of a value, no length, no hash. Whether a variable is
    set is a fact about configuration; what it holds is a credential in at
    least two of these cases, and this output gets pasted into bug reports.
    """
    env = os.environ if env is None else env
    parts = []
    for var in names:
        raw = env.get(var)
        state = "set" if raw is not None and str(raw).strip() != "" else "unset"
        parts.append(var + " " + state)
    return _record(OK, "environment", ", ".join(parts))


# --------------------------------------------------------------------------
# run and report
# --------------------------------------------------------------------------

def run_checks(*, root=REPO_ROOT, env=None, home=None,
               candidates=None, probe=default_loader_probe,
               pairs=KNOWN_GOOD_PAIRS) -> list:
    """Every check, in reading order. The registry is read once and shared."""
    info = installed_plugin_info(env=env, home=home, candidates=candidates)
    present, loader_version, _ = probe()

    records = [
        check_plugin_install(info=info),
        check_skill_count(root=root),
        check_loader(probe=probe),
        check_version_pair(plugin_version=info["version"],
                           loader_version=loader_version if present else None,
                           pairs=pairs),
        check_hooks(root=root),
    ]
    records.extend(check_directories(root=root, env=env, home=home))
    records.append(check_environment(env=env))
    return records


def format_records(records) -> str:
    return "\n".join(r.status + " " + r.name + ": " + r.detail for r in records)


def exit_code(records) -> int:
    return EXIT_FAIL if any(r.status == FAIL for r in records) else EXIT_OK


class _Parser(argparse.ArgumentParser):
    """argparse exits 2 on a usage error. 2 is reserved by the verify gate."""

    def error(self, message: str) -> None:  # type: ignore[override]
        self.print_usage(sys.stderr)
        sys.stderr.write(self.prog + ": error: " + message + "\n")
        raise SystemExit(EXIT_USAGE)


def main(argv=None) -> int:
    parser = _Parser(
        prog="doctor",
        description="Report which MemStack pieces are installed and whether they agree.",
    )
    parser.add_argument("--json", dest="as_json", action="store_true",
                        help="emit the same records as JSON")
    args = parser.parse_args(argv)

    records = run_checks()

    if args.as_json:
        print(json.dumps([r._asdict() for r in records], indent=2))
    else:
        print(format_records(records))

    return exit_code(records)


if __name__ == "__main__":
    sys.exit(main())
