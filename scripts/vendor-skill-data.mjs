#!/usr/bin/env node
// Vendor loader skill-data into memstack for catalog generation (Phase 2).
//
// Mirrors the site's scripts/vendor-skill-data.mjs: copies the loader's
// public-safe sources BYTE-FOR-BYTE into scripts/_generated/ and stamps
// SOURCE.md with the loader path + git short-SHA for provenance.
//
// Run MANUALLY when loader skill data changes (not part of any build).
// Loader is expected at ../memstack-skill-loader (override: MEMSTACK_LOADER_DIR).
// No dependencies — node: builtins only, offline-deterministic.

import { writeFileSync, mkdirSync, copyFileSync, existsSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = resolve(__dirname, "..");
const OUT_DIR = join(__dirname, "_generated");

const LOADER_DIR = resolve(
  process.env.MEMSTACK_LOADER_DIR || join(REPO_ROOT, "..", "memstack-skill-loader"),
);

// Public-safe sources only. skills.public.json = structural truth (slug/category/
// isPro/version); skill_descriptions.json = what/not_for capability text. NO Pro
// skill bodies cross this boundary — only names/tiers/categories/capability text.
const SOURCES = [
  { name: "skills.public.json", rel: "skills.public.json" },
  {
    name: "skill_descriptions.json",
    rel: join("src", "memstack_skill_loader", "skill_descriptions.json"),
  },
];

function die(msg) {
  console.error(`\n[vendor-skill-data] FAIL: ${msg}\n`);
  process.exit(1);
}

if (!existsSync(LOADER_DIR)) die(`loader dir not found: ${LOADER_DIR}`);
mkdirSync(OUT_DIR, { recursive: true });

let shortSha = "unknown";
try {
  shortSha = execFileSync("git", ["-C", LOADER_DIR, "rev-parse", "--short", "HEAD"], {
    encoding: "utf8",
  }).trim();
} catch {
  /* leave "unknown" — provenance still records the path */
}

for (const s of SOURCES) {
  const src = join(LOADER_DIR, s.rel);
  if (!existsSync(src)) die(`source missing: ${src}`);
  copyFileSync(src, join(OUT_DIR, s.name));
  console.log(`vendored ${s.name}  <-  ${src}`);
}

const stamp = `# Vendored skill-data provenance

Do not edit by hand. Regenerate with: \`npm run vendor:skills\`

| Field | Value |
|---|---|
| Loader repo | \`${LOADER_DIR}\` |
| Loader commit | \`${shortSha}\` |
| Vendored at | ${new Date().toISOString()} |
| Files | ${SOURCES.map((s) => "`" + s.name + "`").join(", ")} |

The source of truth lives in the loader; these are byte-for-byte copies consumed
by \`scripts/generate-catalogs.mjs\`. Same pattern as the site's
\`memstack-pro-site/src/data/_generated/SOURCE.md\`.
`;
writeFileSync(join(OUT_DIR, "SOURCE.md"), stamp);
console.log(`wrote SOURCE.md (loader @ ${shortSha})`);
