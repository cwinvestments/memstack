#!/usr/bin/env node
// Verify that plugin.json's components.skills registers every SKILL.md on disk.
//
// WHY THIS EXISTS
//
// Claude Code scans each declared skills directory exactly ONE level deep. It
// looks for SKILL.md in the directory itself (depth 0) and in each immediate
// subdirectory (depth 1). It does not recurse below that. The plugins
// reference documents the field as "Custom skill directories containing
// <name>/SKILL.md", and there is no file-path form and no glob form.
//
// So a manifest declaring only the skills root registers skills/<name>/SKILL.md
// and silently skips skills/<category>/<name>/SKILL.md. Through 3.9.6 that is
// exactly what happened: all 86 free skills were delivered to the customer's
// disk, 18 registered, and the other 68 were inert bytes. Nothing reported it.
// Delivery and registration are different things, and only delivery was ever
// being checked.
//
// This script closes that gap by deriving the required directory set from the
// filesystem and comparing it against the hand-written manifest.
//
// ASSERTIONS (all fail-loud, all report every offender rather than the first)
//
//   1. EXACT SET    The declared directory set equals the set derived from
//                   disk: the skills root, plus the parent of every SKILL.md
//                   found two levels below it. Stronger than coverage alone,
//                   because it catches both directions at once.
//   2. COVERAGE     Every SKILL.md under skills/ is reachable from some
//                   declared directory at depth 0 or depth 1. Reported
//                   separately so a failure names the unregistered files.
//   3. NO DEAD      Every declared directory exists and yields at least one
//      ENTRIES      SKILL.md. A typo or a directory emptied by a later change
//                   would otherwise sit in the manifest unnoticed.
//   4. UNIQUE       Every frontmatter name is distinct. Registered skills all
//      NAMES        flatten into one memstack:<name> namespace regardless of
//                   which directory they came from, so two skills sharing a
//                   name collide once both are registered. Before this release
//                   only 18 were registered, which meant a latent collision
//                   among the other 68 could not have surfaced.
//
// It also checks the "./" prefix the plugins reference requires on every
// declared path, and that each SKILL.md actually carries a frontmatter name.
//
// Usage: node scripts/check-manifest-skills.mjs
// Exit 0 on pass, 1 on any failure. Stdlib only, no deps, deterministic.

import { readFileSync, readdirSync, existsSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = resolve(__dirname, "..");
const MANIFEST = join(REPO_ROOT, ".claude-plugin", "plugin.json");
const SKILLS_REL = "skills";
const SKILLS_ROOT = join(REPO_ROOT, SKILLS_REL);

const problems = [];
const fail = (msg) => problems.push(msg);

// Forward slashes everywhere so Windows and CI compare identically.
const slash = (p) => p.split("\\").join("/");

// "./skills/" and "skills" both normalise to "skills". "." and "./" both
// denote the plugin root and normalise to the empty string.
function normalise(p) {
  let s = slash(String(p)).trim();
  if (s.startsWith("./")) s = s.slice(2);
  while (s.endsWith("/")) s = s.slice(0, -1);
  return s === "." ? "" : s;
}

// ---------------------------------------------------------------------------
// Read the manifest
// ---------------------------------------------------------------------------
if (!existsSync(MANIFEST)) {
  console.error("[check-manifest-skills] FAIL: .claude-plugin/plugin.json not found");
  process.exit(1);
}

let manifest;
try {
  manifest = JSON.parse(readFileSync(MANIFEST, "utf8"));
} catch (err) {
  console.error(`[check-manifest-skills] FAIL: plugin.json is not valid JSON: ${err.message}`);
  process.exit(1);
}

const declaredRaw = manifest?.components?.skills;
if (!Array.isArray(declaredRaw)) {
  console.error("[check-manifest-skills] FAIL: components.skills is missing or not an array");
  process.exit(1);
}

// The "./" prefix is required by the plugins reference for every path except
// the bare plugin root, which the skills field also accepts as ".".
for (const raw of declaredRaw) {
  if (typeof raw !== "string") {
    fail(`declared entry is not a string: ${JSON.stringify(raw)}`);
    continue;
  }
  if (raw !== "." && !raw.startsWith("./")) {
    fail(`declared path must start with "./": ${JSON.stringify(raw)}`);
  }
}

const declared = declaredRaw.filter((p) => typeof p === "string").map(normalise);
const declaredSet = new Set(declared);
if (declaredSet.size !== declared.length) {
  const seen = new Set();
  const dupes = declared.filter((d) => (seen.has(d) ? true : (seen.add(d), false)));
  fail(`duplicate declared directories: ${[...new Set(dupes)].join(", ")}`);
}

// ---------------------------------------------------------------------------
// Walk the tree: every SKILL.md that exists, at any depth
// ---------------------------------------------------------------------------
function walk(absDir, out) {
  for (const entry of readdirSync(absDir, { withFileTypes: true })) {
    const abs = join(absDir, entry.name);
    if (entry.isDirectory()) walk(abs, out);
    else if (entry.isFile() && entry.name === "SKILL.md") {
      out.push(slash(abs.slice(REPO_ROOT.length + 1)));
    }
  }
  return out;
}

if (!existsSync(SKILLS_ROOT)) {
  console.error("[check-manifest-skills] FAIL: skills/ directory not found");
  process.exit(1);
}

const onDisk = walk(SKILLS_ROOT, []).sort();
if (onDisk.length === 0) {
  console.error("[check-manifest-skills] FAIL: no SKILL.md found under skills/");
  process.exit(1);
}

// ---------------------------------------------------------------------------
// 1. EXACT SET: derive the required directories from disk
// ---------------------------------------------------------------------------
// A SKILL.md at skills/<a>/SKILL.md needs "skills" declared.
// A SKILL.md at skills/<a>/<b>/SKILL.md needs "skills/<a>" declared.
// Anything deeper cannot be registered at all, and is reported as such.
const required = new Set();
const unreachable = [];

for (const rel of onDisk) {
  const parts = rel.split("/"); // e.g. skills, security, rls-checker, SKILL.md
  const depth = parts.length - 2; // directories below the skills root
  if (depth === 0) required.add(SKILLS_REL); // skills/SKILL.md
  else if (depth === 1) required.add(SKILLS_REL); // skills/<a>/SKILL.md
  else if (depth === 2) required.add(parts.slice(0, 2).join("/")); // skills/<a>
  else unreachable.push(rel);
}

for (const rel of unreachable) {
  fail(`SKILL.md sits more than two levels below the repo root and cannot be registered by any directory declaration: ${rel}`);
}

const missingFromManifest = [...required].filter((d) => !declaredSet.has(d)).sort();
const extraInManifest = [...declaredSet].filter((d) => !required.has(d)).sort();

for (const d of missingFromManifest) {
  fail(`directory holds SKILL.md files but is not declared in components.skills: ./${d}/`);
}
for (const d of extraInManifest) {
  const abs = d === "" ? REPO_ROOT : join(REPO_ROOT, d);
  const why = !existsSync(abs)
    ? "the directory does not exist"
    : !statSync(abs).isDirectory()
      ? "the path is not a directory"
      : "no SKILL.md is reachable from it at depth 0 or depth 1";
  fail(`declared directory registers nothing (${why}): ./${d}/`);
}

// ---------------------------------------------------------------------------
// 2 and 3. COVERAGE and DEAD ENTRIES, reported per file and per entry
// ---------------------------------------------------------------------------
function registeredBy(relDir) {
  const abs = relDir === "" ? REPO_ROOT : join(REPO_ROOT, relDir);
  if (!existsSync(abs) || !statSync(abs).isDirectory()) return [];
  const hits = [];
  const prefix = relDir === "" ? "" : relDir + "/";
  if (existsSync(join(abs, "SKILL.md"))) hits.push(prefix + "SKILL.md");
  for (const entry of readdirSync(abs, { withFileTypes: true })) {
    if (!entry.isDirectory()) continue;
    if (existsSync(join(abs, entry.name, "SKILL.md"))) {
      hits.push(prefix + entry.name + "/SKILL.md");
    }
  }
  return hits;
}

const registered = new Set();
const perEntry = new Map();
for (const d of declaredSet) {
  const hits = registeredBy(d);
  perEntry.set(d, hits.length);
  for (const h of hits) registered.add(h);
}

const unregistered = onDisk.filter((f) => !registered.has(f));
for (const f of unregistered) {
  fail(`SKILL.md is on disk but no declared directory registers it: ${f}`);
}

// ---------------------------------------------------------------------------
// 4. UNIQUE NAMES: every skill flattens into one memstack:<name> namespace
// ---------------------------------------------------------------------------
function frontmatterName(relFile) {
  const text = readFileSync(join(REPO_ROOT, relFile), "utf8");
  const lines = text.split(/\r?\n/);
  let i = 0;
  while (i < lines.length && lines[i].trim() === "") i++;
  if (i >= lines.length || lines[i].trim() !== "---") return null;
  i++;
  for (; i < lines.length; i++) {
    const line = lines[i];
    if (line.trim() === "---") break;
    const m = /^name:\s*(.*)$/.exec(line);
    if (!m) continue;
    let v = m[1].trim();
    // Strip one matched pair of surrounding quotes, and any trailing comment.
    if ((v.startsWith('"') && v.endsWith('"')) || (v.startsWith("'") && v.endsWith("'"))) {
      v = v.slice(1, -1);
    }
    return v.trim();
  }
  return null;
}

const byName = new Map();
for (const rel of onDisk) {
  const name = frontmatterName(rel);
  if (!name) {
    fail(`SKILL.md has no frontmatter name field, so its invocation name would fall back to the directory basename: ${rel}`);
    continue;
  }
  if (!byName.has(name)) byName.set(name, []);
  byName.get(name).push(rel);
}

let collisions = 0;
for (const [name, files] of [...byName.entries()].sort()) {
  if (files.length > 1) {
    collisions++;
    fail(`namespace collision: ${files.length} skills share the frontmatter name "${name}", which flattens to memstack:${name}\n      ${files.join("\n      ")}`);
  }
}

// ---------------------------------------------------------------------------
// Report
// ---------------------------------------------------------------------------
console.log("[check-manifest-skills] manifest coverage:");
console.log(`  SKILL.md on disk under skills/ : ${onDisk.length}`);
console.log(`  registered by the manifest      : ${registered.size}`);
console.log(`  declared directories            : ${declaredSet.size}`);
console.log(`  distinct frontmatter names      : ${byName.size}`);
console.log(`  namespace collisions            : ${collisions}`);
console.log("  per declared directory:");
for (const d of [...declaredSet].sort()) {
  console.log(`    ${("./" + d + "/").padEnd(28)} ${String(perEntry.get(d) ?? 0).padStart(3)} skill(s)`);
}

if (problems.length) {
  console.error("\n[check-manifest-skills] FAIL:");
  for (const p of problems) console.error(`  - ${p}`);
  console.error(
    "\n  Claude Code scans each declared skills directory one level deep only.\n" +
      "  Declare every directory that directly contains <name>/SKILL.md.\n",
  );
  process.exit(1);
}

console.log("\n[check-manifest-skills] every SKILL.md on disk is registered, every declared directory is used, all names unique.");
