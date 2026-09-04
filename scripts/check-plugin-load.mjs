#!/usr/bin/env node
// Prove what a customer's Claude Code actually LOADS from this tree, by machine.
//
// WHY THIS EXISTS
//
// check-manifest-skills.mjs reasons about the manifest. It reads plugin.json,
// walks skills/, and decides what SHOULD register. That is a model of the
// loader, written by hand, and a model can be wrong in the same direction as
// the thing it models. 3.9.7 is the proof: the manifest was edited, a check was
// written for it, the check passed, and the release shipped registering 18 of
// 86 skills. Nothing in the repo ran the real loader even once.
//
// This gate runs the real loader. It starts a genuine Claude Code process
// against this tree, reads the load trace that process writes about itself, and
// asserts on what the trace says. It is the only check here whose evidence
// comes from the program the customer will run rather than from our reading of
// its documentation.
//
// THE INSTRUMENT
//
// claude accepts --plugin-dir <path> to load a local plugin tree for one
// session only, and --debug-file <path> to write the startup debug trace to a
// file. The trace carries, per plugin:
//
//   [DEBUG] Checking plugin <name>: skillsPath=exists, skillsPaths=N paths
//   [DEBUG] Loaded <n> skills from plugin <name> default directory
//   [DEBUG] Loaded <n> skills from plugin <name> custom path: <abs dir>
//   [WARN]  Failed to parse YAML frontmatter in <abs>/SKILL.md: YAML Parse error: ...
//
// The "minus one" in assertion 2 is not arbitrary. The first entry of the
// manifest skills array is consumed as the plugin's default skillsPath and the
// remainder become skillsPaths, so a manifest with 10 entries reports
// "skillsPaths=9 paths" and emits one "default directory" line plus 9 "custom
// path" lines. Measured, not assumed: 10 entries produced skillsPaths=9 on this
// tree, and the 3.9.7 tree, whose skills array was nested under components and
// therefore invisible, produced skillsPaths=0 and a single Loaded line of 18.
//
// WHY ASSERTION 4 IS SEPARATE FROM ASSERTION 3
//
// A skill whose frontmatter does not parse is still COUNTED by the Loaded
// lines and then dropped before it is offered. Measured against a scratch copy
// of this tree carrying the 3.9.7-era code-reviewer escape: the Loaded lines
// summed to 86, the loader printed "Total plugin skills loaded: 86", and the
// skill was never offered. The only evidence of the loss anywhere in the trace
// was one WARN line. So the sum can be right while a skill is missing, and a
// gate checking only the sum would pass the exact tree that carried 3.9.8's
// second defect. Assertion 4 exists because assertion 3 provably cannot see it.
//
// ASSERTIONS (in scripts/_plugin-load-parse.mjs, so tests drive the same code)
//
//   1. CHECKED   The plugin was checked exactly once.
//   2. PATHS     skillsPaths equals the manifest's skills entries minus one.
//   3. SUM       The Loaded lines sum to the SKILL.md count on disk under skills/.
//   4. NO WARN   No WARN line names a SKILL.md belonging to this plugin.
//
// ISOLATION
//
// The run must observe this tree and nothing else about this machine:
//
//   --setting-sources project   Drops user settings. Without it the
//                               marketplace copy of this same plugin loads from
//                               enabledPlugins and collides by name, doubling
//                               every count. Assertion 1 proves it worked.
//   cwd outside the repo        "project" settings then resolve to a scratch
//                               directory with no .claude, so this repo's
//                               hooks, CLAUDE.md and MCP servers never load.
//   --strict-mcp-config         No --mcp-config is passed, so this means zero
//                               MCP servers.
//   --no-session-persistence    No session file is written.
//   --permission-mode plan      The run cannot edit anything.
//   --max-turns 1               One turn.
//
// The plugin's OWN hooks do fire, because they are part of the plugin under
// test. That is deliberate. The scratch cwd is named for this gate so that any
// row a plugin hook writes keyed on the directory basename is identifiable.
//
// TWO ENVIRONMENT VARIABLES ARE SCRUBBED
//
// ANTHROPIC_BASE_URL and ANTHROPIC_API_KEY are removed from the child's
// environment. The gate must test the real loader, not a compression proxy in
// front of it, and must not fail because a key rotated. On the machine this was
// written on, leaving a stale key in place turned a 4 second run into a 3
// minute authentication retry loop. No value is read, logged or printed; the
// names are deleted from a copy of the environment.
//
// THE GATE DOES NOT DEPEND ON THE MODEL ANSWERING
//
// Everything asserted here is written during startup, before the first API
// call. Measured: a run that failed authentication with a 401 still produced a
// complete and correct trace. So the log is parsed regardless of how the child
// exited, and the child's exit code is recorded on the receipt as information
// rather than treated as a verdict. Requiring a successful API round trip would
// add cost, latency and a network dependency for no extra evidence.
//
// claude MISSING IS A FAILURE, NOT A SKIP
//
// A release cannot be cut from a machine that cannot run this gate. A skip here
// would reproduce the exact shape of the defect the gate exists to catch: a
// check reporting something other than failure while proving nothing.
//
// THE LOG IS NOT PRINTED
//
// The trace contains hook output, which on this repo includes injected session
// context. Only structurally matched lines are ever echoed, and the log is
// written under .memstack/, which is gitignored.
//
// RECEIPT
//
// Written to .memstack/receipts/plugin-load-<timestamp>.json in the shape
// verify.py uses: task_id, started, finished, cwd, kind, head, dirty,
// untracked_count, checks[], verdict, plus the counts and the log path. It
// deliberately carries NO tree_fingerprint. That algorithm lives in verify.py,
// a second implementation here would be free to drift from it, and drift
// between two copies of one computation is a defect this repo has already paid
// for. The consequence is that verify.py's Stop gate will not accept a
// plugin-load receipt as proof a tree was verified, which is correct: this is
// different evidence about a different question.
//
// Usage: node scripts/check-plugin-load.mjs
// Exit 0 on PASS, 1 on FAIL. Deterministic.

import { spawnSync } from "node:child_process";
import { readFileSync, readdirSync, existsSync, mkdirSync, writeFileSync, rmSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { tmpdir } from "node:os";
import { parseTrace, assertTrace } from "./_plugin-load-parse.mjs";

const __dirname = dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = resolve(__dirname, "..");
const MANIFEST = join(REPO_ROOT, ".claude-plugin", "plugin.json");
const SKILLS_ROOT = join(REPO_ROOT, "skills");
const MEMSTACK_DIR = join(REPO_ROOT, ".memstack");
const LOG_PATH = join(MEMSTACK_DIR, "plugin-load.log");
const RECEIPTS_DIR = join(MEMSTACK_DIR, "receipts");
const RUN_CWD = join(tmpdir(), "memstack-plugin-load-gate");
const PROMPT = "Reply with the single word ok.";
const TIMEOUT_MS = Number(process.env.MEMSTACK_PLUGIN_LOAD_TIMEOUT_MS || 120000);

const slash = (p) => String(p).split("\\").join("/");
const nowIso = () => new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
const started = nowIso();
const stamp = started.replace(/[-:]/g, "");

const checks = [];
function record(name, status, detail, extra) {
  checks.push({
    name,
    cmd: (extra && extra.cmd) || null,
    exit: extra && "exit" in extra ? extra.exit : null,
    duration_s: (extra && extra.duration_s) || 0.0,
    status,
    skip_reason: null,
    output_tail: detail || "",
  });
}

function gitFacts(root) {
  const run = (args) => {
    const r = spawnSync("git", ["-C", root].concat(args), { encoding: "utf8" });
    return r.status === 0 ? String(r.stdout).trim() : null;
  };
  const head = run(["rev-parse", "HEAD"]);
  const porcelain = run(["status", "--porcelain"]);
  const lines = porcelain === null ? [] : porcelain.split(/\r?\n/).filter((l) => l.length);
  return {
    head,
    dirty: lines.length > 0,
    untracked_count: lines.filter((l) => l.startsWith("??")).length,
  };
}

function finish(counts) {
  const verdict = checks.some((c) => c.status === "FAIL") ? "FAIL" : "PASS";
  const facts = gitFacts(REPO_ROOT);
  const receipt = {
    task_id: "plugin-load-" + stamp,
    started,
    finished: nowIso(),
    cwd: REPO_ROOT,
    kind: "plugin-load",
    head: facts.head,
    dirty: facts.dirty,
    untracked_count: facts.untracked_count,
    plugin_name: counts.plugin_name,
    counts: {
      skill_md_on_disk: counts.skill_md_on_disk,
      loaded_sum: counts.loaded_sum,
      loaded_lines: counts.loaded_lines,
      skills_paths_reported: counts.skills_paths_reported,
      skills_paths_expected: counts.skills_paths_expected,
      manifest_skills_entries: counts.manifest_skills_entries,
      frontmatter_warns: counts.frontmatter_warns,
      plugin_checked_lines: counts.plugin_checked_lines,
    },
    log_path: slash(LOG_PATH),
    claude_version: counts.claude_version,
    child_exit: counts.child_exit,
    checks,
    verdict,
  };
  mkdirSync(RECEIPTS_DIR, { recursive: true });
  const receiptPath = join(RECEIPTS_DIR, "plugin-load-" + stamp + ".json");
  writeFileSync(receiptPath, JSON.stringify(receipt, null, 2) + "\n", { encoding: "utf8" });

  console.log("[check-plugin-load] what the real loader reported:");
  console.log("  plugin name                    : " + counts.plugin_name);
  console.log("  manifest skills entries        : " + counts.manifest_skills_entries);
  console.log("  skillsPaths expected / reported: " + counts.skills_paths_expected + " / " + counts.skills_paths_reported);
  console.log("  SKILL.md on disk under skills/ : " + counts.skill_md_on_disk);
  console.log("  Loaded lines / sum             : " + counts.loaded_lines + " / " + counts.loaded_sum);
  console.log("  frontmatter WARN lines         : " + counts.frontmatter_warns);
  console.log("  claude version                 : " + counts.claude_version);
  console.log("  child exit (informational)     : " + counts.child_exit);
  console.log("  trace                          : " + slash(LOG_PATH));
  console.log("  receipt                        : " + slash(receiptPath));
  console.log("");
  for (const c of checks) {
    console.log("  [" + c.status + "] " + c.name + (c.output_tail ? " : " + c.output_tail : ""));
  }

  if (verdict === "FAIL") {
    console.error("\n[check-plugin-load] FAIL. The loader's own trace disagrees with this tree.");
    console.error("  This is the real loader, not a model of it. Fix the tree, not the check.\n");
    process.exit(1);
  }
  console.log("\n[check-plugin-load] PASS. The real loader registered every SKILL.md on disk,");
  console.log("with no skill dropped for unparseable frontmatter.");
  console.log("Cite the receipt path above in the release record.");
  process.exit(0);
}

// ---------------------------------------------------------------------------
// Manifest and disk
// ---------------------------------------------------------------------------
if (!existsSync(MANIFEST)) {
  console.error("[check-plugin-load] FAIL: .claude-plugin/plugin.json not found");
  process.exit(1);
}

let manifest;
try {
  manifest = JSON.parse(readFileSync(MANIFEST, "utf8"));
} catch (err) {
  console.error("[check-plugin-load] FAIL: plugin.json is not valid JSON: " + err.message);
  process.exit(1);
}

const PLUGIN_NAME = typeof manifest.name === "string" ? manifest.name : null;
if (!PLUGIN_NAME) {
  console.error('[check-plugin-load] FAIL: plugin.json has no top-level "name"');
  process.exit(1);
}

// Only a TOP-LEVEL skills array is read by the loader. Anything else, including
// an array nested under components, declares nothing, and the expected
// skillsPaths for such a manifest is 0.
const declared = Array.isArray(manifest.skills) ? manifest.skills : [];
const manifestSkillsEntries = declared.length;
const expectedSkillsPaths = Math.max(0, manifestSkillsEntries - 1);

function walk(absDir, out) {
  for (const entry of readdirSync(absDir, { withFileTypes: true })) {
    const abs = join(absDir, entry.name);
    if (entry.isDirectory()) walk(abs, out);
    else if (entry.isFile() && entry.name === "SKILL.md") out.push(abs);
  }
  return out;
}

if (!existsSync(SKILLS_ROOT)) {
  console.error("[check-plugin-load] FAIL: skills/ directory not found");
  process.exit(1);
}
const onDiskCount = walk(SKILLS_ROOT, []).length;

const baseCounts = {
  plugin_name: PLUGIN_NAME,
  manifest_skills_entries: manifestSkillsEntries,
  skills_paths_expected: expectedSkillsPaths,
  skills_paths_reported: null,
  skill_md_on_disk: onDiskCount,
  loaded_sum: null,
  loaded_lines: 0,
  frontmatter_warns: null,
  plugin_checked_lines: 0,
  claude_version: null,
  child_exit: null,
};

// ---------------------------------------------------------------------------
// claude must be runnable. Missing is a FAIL.
// ---------------------------------------------------------------------------
const NO_CLAUDE =
  "claude is not on PATH, so this gate cannot run. A release cannot be cut from a machine " +
  "that cannot run the gate: the real loader is the only witness that counts here, and " +
  "skipping it would reproduce the defect this gate exists to catch. Install Claude Code " +
  "and run this again.";

const version = spawnSync("claude", ["--version"], { encoding: "utf8", timeout: 60000 });
if (version.error || version.status !== 0) {
  record("claude available on PATH", "FAIL", NO_CLAUDE, { cmd: "claude --version" });
  finish(baseCounts);
}
const claudeVersion = String(version.stdout).trim();
baseCounts.claude_version = claudeVersion;
record("claude available on PATH", "PASS", claudeVersion, { cmd: "claude --version", exit: 0 });

// ---------------------------------------------------------------------------
// Run the real loader
// ---------------------------------------------------------------------------
mkdirSync(MEMSTACK_DIR, { recursive: true });
mkdirSync(RUN_CWD, { recursive: true });

// --debug-file APPENDS. It does not truncate. Leaving a previous run's log in
// place makes every count cumulative: the second run of this gate against an
// unchanged, correct tree reported 5 "Checking plugin" lines, 50 Loaded lines
// and a sum of 430 against 86 on disk. Assertion 1 caught that, which is the
// reason it asserts "exactly once" rather than "at least once", but the log has
// to start empty or the gate measures its own history instead of this tree.
rmSync(LOG_PATH, { force: true });

const args = [
  "-p", PROMPT,
  "--plugin-dir", REPO_ROOT,
  "--debug-file", LOG_PATH,
  "--strict-mcp-config",
  "--setting-sources", "project",
  "--no-session-persistence",
  "--permission-mode", "plan",
  "--max-turns", "1",
  "--model", "haiku",
];

const childEnv = Object.assign({}, process.env);
delete childEnv.ANTHROPIC_BASE_URL;
delete childEnv.ANTHROPIC_API_KEY;

const t0 = Date.now();
const run = spawnSync("claude", args, {
  cwd: RUN_CWD,
  env: childEnv,
  encoding: "utf8",
  timeout: TIMEOUT_MS,
  stdio: ["ignore", "pipe", "pipe"],
});
const elapsed = (Date.now() - t0) / 1000;
const childExit = run.error ? "error:" + run.error.code : String(run.status);
baseCounts.child_exit = childExit;

record(
  "claude -p ran against --plugin-dir",
  "PASS",
  "exit " + childExit + " in " + elapsed.toFixed(1) + "s. Informational only: the trace is " +
    "written at startup before any API call, so the verdict does not depend on this.",
  {
    cmd: "claude -p ... --plugin-dir . --debug-file .memstack/plugin-load.log",
    exit: run.status,
    duration_s: elapsed,
  },
);

if (!existsSync(LOG_PATH)) {
  record(
    "load trace written",
    "FAIL",
    "no debug file at " + slash(LOG_PATH) + ". claude ran but wrote no trace, so nothing " +
      "about this tree was observed and nothing can be asserted.",
  );
  finish(baseCounts);
}

const parsed = parseTrace(readFileSync(LOG_PATH, "utf8"), PLUGIN_NAME, REPO_ROOT);
record("load trace written", "PASS", parsed.lineCount + " trace lines");

const results = assertTrace(parsed, {
  pluginName: PLUGIN_NAME,
  skillsPaths: expectedSkillsPaths,
  manifestSkillsEntries,
  onDisk: onDiskCount,
});
for (const r of results) record(r.name, r.status, r.detail);

finish(
  Object.assign({}, baseCounts, {
    skills_paths_reported: parsed.skillsPaths,
    loaded_sum: parsed.loadedSum,
    loaded_lines: parsed.loadedLines,
    frontmatter_warns: parsed.warnFrontmatter.length,
    plugin_checked_lines: parsed.checkedCount,
  }),
);
