#!/usr/bin/env python
"""Strict YAML parse of every SKILL.md frontmatter block.

Called by scripts/check-manifest-skills.mjs, never by hand. Node's standard
library has no YAML parser, and the defect this guards against is precisely a
block that a strict parser rejects, so an approximate reader written in Node
would reproduce the bug rather than catch it.

Protocol, deliberately shell-free:

    stdin   one JSON object, {"root": "<abs repo root>", "files": [rel, ...]}
    stdout  one JSON object, {"checked": N, "errors": [ ... ]}
    exit    0 whenever the protocol was honoured, including when parse errors
            were found. The caller decides the verdict. A non-zero exit means
            this script itself could not run, which the caller must report as
            a failure rather than a skip.

Each error carries file, line, col, problem and context. Line numbers are FILE
line numbers, not offsets into the frontmatter block. The block starts on file
line 2, so a parser mark at block line 0 is reported as file line 2.

Stdlib plus PyYAML. No shell is involved on either side of this boundary: the
caller passes an argument array and the file list arrives on stdin, so nothing
in a path or a message can be read as a shell operator.
"""

import io
import json
import os
import sys

try:
    import yaml
except ImportError:
    sys.stderr.write("check-frontmatter-yaml: PyYAML is not installed\n")
    sys.exit(2)


def frontmatter_block(text):
    """Return (block_text, None) on success, or (None, reason) on failure."""
    lines = text.split("\n")
    i = 0
    while i < len(lines) and lines[i].strip() == "":
        i += 1
    if i >= len(lines) or lines[i].strip() != "---":
        return None, "no opening frontmatter delimiter"
    start = i + 1
    for j in range(start, len(lines)):
        if lines[j].strip() == "---":
            return "\n".join(lines[start:j]), None
    return None, "no closing frontmatter delimiter"


def main():
    payload = json.loads(sys.stdin.read())
    root = payload["root"]
    files = payload["files"]

    errors = []
    checked = 0

    for rel in files:
        path = os.path.join(root, rel.replace("/", os.sep))
        checked += 1

        try:
            text = io.open(path, encoding="utf-8").read()
        except (IOError, OSError, UnicodeDecodeError) as exc:
            errors.append({
                "file": rel,
                "line": 0,
                "col": 0,
                "problem": "cannot read file: %s" % exc,
                "context": "",
            })
            continue

        block, reason = frontmatter_block(text)
        if block is None:
            errors.append({
                "file": rel,
                "line": 1,
                "col": 0,
                "problem": reason,
                "context": "",
            })
            continue

        try:
            yaml.safe_load(block)
        except yaml.YAMLError as exc:
            mark = getattr(exc, "problem_mark", None)
            line = (mark.line + 2) if mark is not None else 0
            col = (mark.column + 1) if mark is not None else 0
            problem = getattr(exc, "problem", None) or str(exc)
            context = getattr(exc, "context", None) or ""
            errors.append({
                "file": rel,
                "line": line,
                "col": col,
                "problem": " ".join(str(problem).split()),
                "context": " ".join(str(context).split()),
            })

    sys.stdout.write(json.dumps({"checked": checked, "errors": errors}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
