#!/usr/bin/env node
/**
 * generate-pro-stubs.js — Create upsell stub SKILL.md files for Pro-only skills
 *
 * Reads frontmatter from each Pro skill, generates a stub in the free repo.
 * Does NOT copy any skill logic — stubs only.
 */

const fs = require("fs");
const path = require("path");

const PRO_DIR = "C:/Projects/memstack-pro/skills";
const FREE_DIR = "C:/Projects/memstack/skills";

// Pro-only skills (not in free repo)
const PRO_ONLY = [
  "business/proposal-writer",
  "business/scope-of-work",
  "business/sop-builder",
  "content/blog-post",
  "content/email-sequence",
  "content/landing-page-copy",
  "content/youtube-script",
  "deployment/ci-cd-pipeline",
  "deployment/docker-setup",
  "deployment/domain-ssl",
  "deployment/hetzner-setup",
  "deployment/netlify-deploy",
  "deployment/railway-deploy",
  "development/api-designer",
  "development/code-reviewer",
  "development/database-architect",
  "development/performance-audit",
  "security/api-audit",
  "security/csp-headers",
  "security/dependency-audit",
  "security/owasp-top10",
  "security/rls-checker",
  "security/rls-guardian",
  "security/secrets-scanner",
  "seo-geo/ai-search-visibility",
  "seo-geo/keyword-research",
  "seo-geo/local-seo",
  "seo-geo/meta-tag-optimizer",
  "seo-geo/schema-markup",
  "seo-geo/site-audit",
];

function parseFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return {};
  const fm = {};
  for (const line of match[1].split("\n")) {
    const m = line.match(/^(\w+):\s*"?(.*?)"?\s*$/);
    if (m) fm[m[1]] = m[2];
  }
  return fm;
}

function extractFirstHeading(content) {
  const match = content.match(/^#\s+.*?—\s*(.*?)\.{3}.*$/m);
  if (match) return match[1].trim();
  const h1 = content.match(/^#\s+(.+)$/m);
  if (h1) return h1[1].replace(/[🔒🚂📊🛡️🔍📝📧🎬🎯📦🐳🌐🖥️💻🧪⚡🔄📋🏗️🔐🕵️📡🔑🏷️🗺️📈🔎]/g, "").trim();
  return "";
}

function extractOneLiner(content) {
  // Get the italic subtitle line after the heading
  const match = content.match(/^\*(.+?)\*$/m);
  if (match) return match[1].trim();
  return "";
}

function prettyName(skillPath) {
  return skillPath
    .split("/")[1]
    .split("-")
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(" ");
}

let created = 0;

for (const skill of PRO_ONLY) {
  const proPath = path.join(PRO_DIR, skill, "SKILL.md");
  const freePath = path.join(FREE_DIR, skill, "SKILL.md");

  if (!fs.existsSync(proPath)) {
    console.error(`  SKIP: Pro skill not found: ${proPath}`);
    continue;
  }

  const content = fs.readFileSync(proPath, "utf8");
  const fm = parseFrontmatter(content);
  const oneLiner = extractOneLiner(content);
  const displayName = prettyName(skill);

  const stub = `---
name: ${fm.name || "memstack-" + skill.replace(/\//g, "-")}
description: "${(fm.description || "").replace(/"/g, '\\"')}"
license: "Free preview — full skill available in MemStack™ Pro"
---

# 🔒 ${displayName} — MemStack™ Pro

This skill is available in **MemStack™ Pro**.

**What it does:**
${oneLiner || displayName + " automation and guidance."}

**Upgrade to Pro** to unlock this skill plus 59 others:
👉 https://memstack.cwaffiliateinvestments.com
`;

  fs.mkdirSync(path.dirname(freePath), { recursive: true });
  fs.writeFileSync(freePath, stub);
  console.log(`  Created: ${skill}`);
  created++;
}

console.log(`\n  Done: ${created} stubs created.`);
