#!/usr/bin/env bash
# verify-free-repo.sh — Checks that no Pro skill content has leaked into the free repo.
# Reads FREE-SKILLS.txt for the allowlist, flags any SKILL.md with >20 lines not on it.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MANIFEST="$REPO_ROOT/FREE-SKILLS.txt"

if [ ! -f "$MANIFEST" ]; then
  echo "FAIL: FREE-SKILLS.txt not found at $MANIFEST"
  exit 1
fi

# Load allowlist (strip comments and blank lines)
allowed=()
while IFS= read -r line; do
  line="${line%%#*}"                    # strip inline comments
  line="$(echo "$line" | xargs)"       # trim leading/trailing whitespace
  [ -z "$line" ] && continue
  allowed+=("$line")
done < "$MANIFEST"

leaks=0
checked=0
passed=0

while IFS= read -r skill_file; do
  rel_path="${skill_file#$REPO_ROOT/}"
  lines=$(wc -l < "$skill_file")
  checked=$((checked + 1))

  if [ "$lines" -gt 20 ]; then
    # Check if this file is in the allowlist
    found=false
    for a in "${allowed[@]}"; do
      if [ "$a" = "$rel_path" ]; then
        found=true
        break
      fi
    done

    if [ "$found" = false ]; then
      echo "LEAK: $rel_path ($lines lines — not in FREE-SKILLS.txt)"
      leaks=$((leaks + 1))
    else
      passed=$((passed + 1))
    fi
  else
    passed=$((passed + 1))
  fi
done < <(find "$REPO_ROOT/skills" -name "SKILL.md" -type f | sort)

echo ""
echo "=== Skill Guard Report ==="
echo "Checked: $checked"
echo "Passed:  $passed"
echo "Leaks:   $leaks"

if [ "$leaks" -gt 0 ]; then
  echo ""
  echo "FAILED — Pro skill content detected in free repo."
  echo "Either add the skill to FREE-SKILLS.txt or replace it with an upsell stub."
  exit 1
else
  echo "PASSED — no Pro skill leaks detected."
  exit 0
fi
