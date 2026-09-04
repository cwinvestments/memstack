// Parser and assertions for the Claude Code plugin load trace.
//
// Split out of check-plugin-load.mjs so it can be imported and driven with
// fixture logs without spawning a Claude Code process. The gate imports it; the
// tests import it. There is exactly one implementation of these rules.
//
// It has no side effects: no file writes, no process spawning, no exit calls.
//
// LINE SHAPES, all copied from real traces rather than from documentation:
//
//   [DEBUG] Checking plugin memstack: skillsPath=exists, skillsPaths=9 paths
//   [DEBUG] Loaded 18 skills from plugin memstack default directory
//   [DEBUG] Loaded 6 skills from plugin memstack custom path: C:\...\skills\automation
//   [WARN] Failed to parse YAML frontmatter in C:\...\SKILL.md: YAML Parse error: Unexpected character
//
// CLI mode, used by the pytest suite so the parser is tested where the rest of
// this repo's tests run:
//
//   node scripts/_plugin-load-parse.mjs <logPath> <pluginName> <pluginRoot> \
//        <expectedSkillsPaths> <manifestEntries> <onDisk>
//
// prints a JSON object with a verdict and one entry per assertion, exit 0
// always. The caller decides what to do with the verdict.

import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { resolve } from "node:path";

const slash = (p) => String(p).split("\\").join("/");

export function parseTrace(text, pluginName, pluginRoot) {
  const lines = String(text).split(/\r?\n/);
  const esc = String(pluginName).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

  const checkedRe = new RegExp("Checking plugin " + esc + ":.*?skillsPaths=(\\d+) paths");
  const loadedRe = new RegExp("Loaded (\\d+) skills from plugin " + esc + "\\b");

  const checked = [];
  const loadedCounts = [];
  const warnFrontmatter = [];

  const rootNorm = pluginRoot ? slash(pluginRoot).toLowerCase() : null;
  const nameNorm = String(pluginName).toLowerCase();

  for (const line of lines) {
    const c = checkedRe.exec(line);
    if (c) checked.push(Number(c[1]));

    const l = loadedRe.exec(line);
    if (l) loadedCounts.push(Number(l[1]));

    // A WARN naming a SKILL.md is the ONLY evidence that a skill was counted by
    // the Loaded lines and then dropped before being offered. Measured against
    // a tree carrying the 3.9.7-era code-reviewer escape: Loaded summed to 86,
    // the loader printed "Total plugin skills loaded: 86", and the skill was
    // never offered. Without this the sum assertion passes that tree.
    if (/\[WARN\]/.test(line) && /SKILL\.md/i.test(line)) {
      const norm = slash(line).toLowerCase();
      // Attribute to this plugin by path, so a WARN about a different plugin's
      // skill cannot fail this tree. Fall back to the plugin name when no root
      // is supplied, which is how the fixtures are driven.
      if (!rootNorm ? norm.includes(nameNorm) : norm.includes(rootNorm)) {
        warnFrontmatter.push(line.trim());
      }
    }
  }

  return {
    lineCount: lines.length,
    checkedCount: checked.length,
    skillsPaths: checked.length ? checked[0] : null,
    loadedLines: loadedCounts.length,
    loadedSum: loadedCounts.reduce((a, b) => a + b, 0),
    warnFrontmatter,
  };
}

export function assertTrace(parsed, expected) {
  const out = [];
  const add = (name, ok, detail) => out.push({ name, status: ok ? "PASS" : "FAIL", detail });

  // 1. The plugin was checked, exactly once. Exactly once matters because this
  // repo's plugin is also installed from the marketplace and enabled in user
  // settings, so a run that loaded both would double every count below.
  if (parsed.checkedCount === 0) {
    add(
      "plugin was checked by the loader",
      false,
      'no "Checking plugin ' + expected.pluginName + '" line in the trace. The loader never ' +
        "saw this plugin, so every other number here is meaningless.",
    );
  } else if (parsed.checkedCount > 1) {
    add(
      "plugin was checked by the loader",
      false,
      parsed.checkedCount + ' "Checking plugin ' + expected.pluginName + '" lines, so two ' +
        "copies of the same plugin loaded and every count is doubled. The marketplace copy " +
        "is enabled in user settings; --setting-sources project is what excludes it.",
    );
  } else {
    add("plugin was checked by the loader", true, "exactly one Checking line");
  }

  // 2. skillsPaths equals the manifest's skills entries minus one, because the
  // first entry is consumed as the plugin's default skillsPath.
  add(
    "skillsPaths equals manifest entries minus one",
    parsed.skillsPaths === expected.skillsPaths,
    "reported " + parsed.skillsPaths + ", expected " + expected.skillsPaths + " from " +
      expected.manifestSkillsEntries + " manifest entries" +
      (expected.manifestSkillsEntries === 0
        ? ". No top-level skills array is declared, so the loader fell back to the default skills root."
        : ""),
  );

  // 3. The Loaded lines sum to what is on disk.
  add(
    "Loaded lines sum to SKILL.md on disk",
    parsed.loadedSum === expected.onDisk,
    parsed.loadedLines + " Loaded line(s) summing to " + parsed.loadedSum + ", against " +
      expected.onDisk + " SKILL.md on disk under skills/" +
      (parsed.loadedSum < expected.onDisk
        ? ". " + (expected.onDisk - parsed.loadedSum) +
          " skill(s) shipped to disk and were never registered."
        : ""),
  );

  // 4. No WARN names a SKILL.md belonging to this plugin.
  add(
    "no WARN names a SKILL.md in this plugin",
    parsed.warnFrontmatter.length === 0,
    parsed.warnFrontmatter.length === 0
      ? "none"
      : parsed.warnFrontmatter.length + " WARN line(s). A skill named here was counted by the " +
        "Loaded lines above and then dropped before it was offered, so the sum can be correct " +
        "while the skill is missing:\n      " + parsed.warnFrontmatter.join("\n      "),
  );

  return out;
}

export function verdictOf(results) {
  return results.some((r) => r.status === "FAIL") ? "FAIL" : "PASS";
}

// CLI mode for the pytest suite.
if (process.argv[1] && resolve(process.argv[1]) === resolve(fileURLToPath(import.meta.url))) {
  const [logPath, pluginName, pluginRoot, sp, entries, onDisk] = process.argv.slice(2);
  const text = readFileSync(logPath, "utf8");
  const parsed = parseTrace(text, pluginName, pluginRoot === "-" ? null : pluginRoot);
  const results = assertTrace(parsed, {
    pluginName,
    skillsPaths: Number(sp),
    manifestSkillsEntries: Number(entries),
    onDisk: Number(onDisk),
  });
  process.stdout.write(
    JSON.stringify({ parsed, results, verdict: verdictOf(results) }, null, 2) + "\n",
  );
}
