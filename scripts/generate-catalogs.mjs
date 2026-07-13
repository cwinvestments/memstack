#!/usr/bin/env node
// Generate memstack catalogs from vendored loader data (Phase 2).
//
// Sources : scripts/_generated/{skills.public.json, skill_descriptions.json}
// Targets : README.md   -> two delimited regions (catalog + Pro list)
//           SKILL-REFERENCE.md -> full file
//
// Grouping: authoritative `category` from skills.public.json (which flows from
//           categories.py upstream). The generator NEVER reassigns a category —
//           it only orders the 10 sections (presentation, unavoidable).
// Identity: slug (Decision 2 = Option A). No display names, no triggers, no
//           overlay — those have no authoritative public source and are exactly
//           the unsourced data that drifts. Columns are 100% loader-sourced:
//           README   = slug + what
//           SKILL-REF = slug + what + not_for (authoritative anti-triggers).
//
// Modes   : (default) preview to _generated/*.preview.md — touches NO doc
//           --write   splice README regions + write SKILL-REFERENCE.md
//           --check   regenerate, diff committed docs, exit 1 on drift
// No deps; node: builtins only; offline-deterministic; fail-loud validation.

import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = resolve(__dirname, "..");
const GEN = join(__dirname, "_generated");
const README = join(REPO_ROOT, "README.md");
const SKILLREF = join(REPO_ROOT, "SKILL-REFERENCE.md");

// --- presentation constants (SECTION ORDER ONLY — never reassigns a skill) ----
const CATEGORY_ORDER = [
  "Core", "Security", "Deployment", "Development", "Business",
  "Content", "SEO & GEO", "Marketing", "Product", "Automation",
];
const SKILLREF_VERSION = "3.5.4"; // doc chrome only; version bumps are out of scope

// --- region markers -----------------------------------------------------------
const CAT_BEGIN = "<!-- BEGIN GENERATED SKILLS CATALOG -->";
const CAT_END = "<!-- END GENERATED SKILLS CATALOG -->";
const PRO_BEGIN = "<!-- BEGIN GENERATED PRO LIST -->";
const PRO_END = "<!-- END GENERATED PRO LIST -->";

function die(msg) {
  console.error(`\n[generate-catalogs] FAIL: ${msg}\n`);
  process.exit(1);
}

// ============================================================================
// Load + fail-loud validation
// ============================================================================
const skills = JSON.parse(readFileSync(join(GEN, "skills.public.json"), "utf8"));
const descs = JSON.parse(readFileSync(join(GEN, "skill_descriptions.json"), "utf8"));

if (!Array.isArray(skills)) die("skills.public.json is not an array");

// Defensive: the gitignored local-only skill must NEVER reach a public catalog.
if (skills.some((s) => s.slug === "kdp-format"))
  die("kdp-format present in vendored data — must never appear in a public catalog");

const free = skills.filter((s) => !s.isPro);
const pro = skills.filter((s) => s.isPro);
if (skills.length !== 130) die(`expected 130 skills, got ${skills.length}`);
if (free.length !== 86) die(`expected 86 free skills, got ${free.length}`);
if (pro.length !== 44) die(`expected 44 Pro skills, got ${pro.length}`);

for (const s of skills) {
  if (!CATEGORY_ORDER.includes(s.category))
    die(`skill "${s.slug}" has category "${s.category}" not in CATEGORY_ORDER — add it deliberately`);
  const d = descs[s.slug];
  if (!d || !d.what || !String(d.what).trim())
    die(`skill "${s.slug}" has no "what" in skill_descriptions.json`);
}

// Group + deterministic in-category sort: free-first, then alphabetical by slug.
const byCat = new Map(CATEGORY_ORDER.map((c) => [c, []]));
for (const s of skills) byCat.get(s.category).push(s);
for (const arr of byCat.values())
  arr.sort((a, b) => a.isPro - b.isPro || a.slug.localeCompare(b.slug));

let sum = 0;
for (const arr of byCat.values()) sum += arr.length;
if (sum !== 130) die(`per-category counts sum to ${sum}, expected 130`);

// ============================================================================
// Render helpers
// ============================================================================
const proTag = (s) => (s.isPro ? " **[PRO]**" : "");
const esc = (t) => String(t).replace(/\|/g, "\\|").trim(); // pipe-safe table cells
const whatOf = (s) => esc(descs[s.slug].what);
const notForOf = (s) => {
  const v = descs[s.slug].not_for;
  return v && String(v).trim() ? esc(v) : "—";
};
const catHeaderCount = (arr) => {
  const f = arr.filter((s) => !s.isPro).length;
  const p = arr.length - f;
  return p > 0 ? `${arr.length} — ${f} free + ${p} Pro` : `${arr.length} skills`;
};

// ============================================================================
// Renderers
// ============================================================================
function readmeCatalog() {
  const out = [];
  for (const cat of CATEGORY_ORDER) {
    const arr = byCat.get(cat);
    out.push(`### ${cat} (${catHeaderCount(arr)})`, "");
    out.push("| Skill | Description |", "|-------|-------------|");
    for (const s of arr) out.push(`| \`${s.slug}\`${proTag(s)} | ${whatOf(s)} |`);
    out.push("");
  }
  return out.join("\n").trimEnd();
}

function readmeProList() {
  const slugs = pro.map((s) => s.slug).sort();
  const list = slugs.map((x) => `\`${x}\``).join(", ");
  return `**Pro-exclusive skills (${slugs.length}):** ${list} — these require an active Pro license.`;
}

function skillReference() {
  const out = [];
  const nCat = CATEGORY_ORDER.length;
  out.push("# MemStack™ — Skill Quick Reference", "");
  out.push(
    `> **${skills.length} skills across ${nCat} categories** (${free.length} free + ${pro.length} Pro-exclusive). Describe your task and the matching skill activates.`,
    ">",
    "> Pro-exclusive skills are marked with **[PRO]**. Requires a Pro license key — activate via Dashboard Settings or `activate_license()` in Claude Code.",
    "",
    "---",
    "",
  );
  for (const cat of CATEGORY_ORDER) {
    const arr = byCat.get(cat);
    out.push(`## ${cat} (${arr.length})`, "");
    out.push("| Skill | What It Does | Not For |", "|-------|-------------|---------|");
    for (const s of arr) out.push(`| \`${s.slug}\`${proTag(s)} | ${whatOf(s)} | ${notForOf(s)} |`);
    out.push("", "---", "");
  }
  out.push(
    `*MemStack™ v${SKILLREF_VERSION} — ${skills.length} skills across ${nCat} categories (${free.length} free + ${pro.length} Pro-exclusive), one prompt away.*`,
    "",
  );
  return out.join("\n");
}

// ============================================================================
// Region splice (--write) / extract (--check)
// ============================================================================
function spliceRegion(text, begin, end, body, label) {
  const i = text.indexOf(begin);
  const j = text.indexOf(end);
  if (i === -1 || j === -1 || j < i)
    die(`README markers for ${label} not found (${begin} / ${end}). Insert them once before the first --write.`);
  return text.slice(0, i + begin.length) + "\n" + body + "\n" + text.slice(j);
}
function extractRegion(text, begin, end, label) {
  const i = text.indexOf(begin);
  const j = text.indexOf(end);
  if (i === -1 || j === -1 || j < i) die(`README markers for ${label} not found — has --write run yet?`);
  return text.slice(i + begin.length, j).trim();
}

// ============================================================================
// Validation report (printed in every mode)
// ============================================================================
function report() {
  console.log("[generate-catalogs] validation:");
  console.log(`  total=130 ✓   free=86 ✓   pro=44 ✓   per-category sum=${sum} ✓`);
  console.log("  every skill resolves a `what` ✓   no kdp-format ✓");
  for (const cat of CATEGORY_ORDER) {
    const arr = byCat.get(cat);
    const f = arr.filter((s) => !s.isPro).length;
    console.log(`    ${cat.padEnd(12)} ${String(arr.length).padStart(3)}  (${f} free + ${arr.length - f} Pro)`);
  }
}

// ============================================================================
// Main
// ============================================================================
const mode = process.argv[2] || "--preview";
const catalog = readmeCatalog();
const prolist = readmeProList();
const skillref = skillReference();
report();

if (mode === "--write") {
  let rd = readFileSync(README, "utf8");
  rd = spliceRegion(rd, CAT_BEGIN, CAT_END, catalog, "catalog");
  rd = spliceRegion(rd, PRO_BEGIN, PRO_END, prolist, "Pro list");
  writeFileSync(README, rd);
  writeFileSync(SKILLREF, skillref);
  console.log("\n[write] README.md regions + SKILL-REFERENCE.md updated.");
} else if (mode === "--check") {
  // Normalize line endings on BOTH sides before comparing. The repo's working
  // tree is CRLF but the generator emits LF; without this, a fresh checkout (or
  // CI) reads CRLF regions and exact-compares them against LF output -> false
  // drift. EOL is not content, so the guard must not cry wolf over it.
  const eol = (s) => s.replace(/\r\n/g, "\n");
  const rd = readFileSync(README, "utf8");
  const problems = [];
  if (eol(extractRegion(rd, CAT_BEGIN, CAT_END, "catalog")) !== eol(catalog.trim()))
    problems.push("README catalog region out of date");
  if (eol(extractRegion(rd, PRO_BEGIN, PRO_END, "Pro list")) !== eol(prolist.trim()))
    problems.push("README Pro-list region out of date");
  if (eol(readFileSync(SKILLREF, "utf8").trim()) !== eol(skillref.trim()))
    problems.push("SKILL-REFERENCE.md out of date");
  if (problems.length) {
    console.error("\n[check] DRIFT:\n  - " + problems.join("\n  - ") + "\n  Run: npm run gen:catalogs\n");
    process.exit(1);
  }
  console.log("\n[check] catalogs match vendored sources ✓");
} else {
  writeFileSync(join(GEN, "README-catalog.preview.md"), catalog + "\n");
  writeFileSync(join(GEN, "README-prolist.preview.md"), prolist + "\n");
  writeFileSync(join(GEN, "SKILL-REFERENCE.preview.md"), skillref);
  console.log(
    "\n[preview] wrote _generated/{README-catalog,README-prolist,SKILL-REFERENCE}.preview.md — no docs touched.",
  );
}
