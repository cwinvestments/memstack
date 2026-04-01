---
name: memstack-security-dependency-audit
description: "Use this skill when the user says 'dependency audit', 'npm audit', 'pip audit', 'cargo audit', 'security vulnerabilities', 'outdated packages', 'supply chain', or needs to scan project dependencies for vulnerabilities, abandoned packages, and upgrade risks. Do NOT use for application-level security or secrets scanning."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# 🔒 Dependency Audit — Supply Chain Security Scanner
*Scan project dependencies for vulnerabilities, outdated packages, abandoned libraries, and supply chain risks with a prioritized upgrade plan.*

## Activation

When this skill activates, output:

`🔒 Dependency Audit — Scanning your dependency tree...`

| Context | Status |
|---------|--------|
| **User says "dependency audit", "npm audit", "scan dependencies"** | ACTIVE |
| **User wants to check for vulnerable or outdated packages** | ACTIVE |
| **User mentions CVEs, supply chain security, or abandoned packages** | ACTIVE |
| **User wants OWASP web app security (not just dependencies)** | DORMANT — see owasp-top10 |
| **User wants secrets scanning (not package vulnerabilities)** | DORMANT — see secrets-scanner |
| **User wants general code review** | DORMANT — see code-reviewer |

## Protocol

### Step 1: Detect Project Type

Identify the package ecosystem from project files:

| File Found | Ecosystem | Audit Command | Outdated Command |
|-----------|-----------|---------------|-----------------|
| `package.json` | npm/Node.js | `npm audit --json` | `npm outdated --json` |
| `package-lock.json` | npm (locked) | `npm audit --json` | `npm outdated --json` |
| `yarn.lock` | Yarn | `yarn audit --json` | `yarn outdated --json` |
| `pnpm-lock.yaml` | pnpm | `pnpm audit --json` | `pnpm outdated --json` |
| `requirements.txt` | pip/Python | `pip audit --format=json` | `pip list --outdated --format=json` |
| `Pipfile.lock` | Pipenv | `pipenv check --output json` | `pipenv update --dry-run` |
| `pyproject.toml` | Poetry/Python | `pip audit --format=json` | `poetry show --outdated` |
| `Cargo.toml` | Rust/Cargo | `cargo audit --json` | `cargo outdated --format json` |
| `go.mod` | Go | `govulncheck ./...` | `go list -u -m all` |
| `Gemfile.lock` | Ruby/Bundler | `bundle audit check --format json` | `bundle outdated` |

If multiple ecosystems detected, audit all of them. Report which ecosystem each finding belongs to.

### Step 2: Run Vulnerability Scan

Execute the appropriate audit command and parse results into a unified format:

```
── VULNERABILITY SCAN ─────────────────────

CVE-2024-XXXXX  🔴 CRITICAL
  Package: [name]@[version]
  Dependency: Direct / Transitive (via [parent])
  Fixed in: [version]
  Description: [brief description]
  CVSS Score: [score]
  Exploitability: [network/local] [complexity]

CVE-2024-YYYYY  🟡 HIGH
  Package: [name]@[version]
  Dependency: Transitive (via [parent] → [grandparent])
  Fixed in: [version]
  Description: [brief description]
  CVSS Score: [score]
  Exploitability: [network/local] [complexity]
```

**Severity classification:**

| Severity | CVSS Score | Icon | Action |
|----------|-----------|------|--------|
| Critical | 9.0 - 10.0 | 🔴 | Fix immediately — potential active exploitation |
| High | 7.0 - 8.9 | 🟡 | Fix within 1 week — significant risk |
| Medium | 4.0 - 6.9 | 🟠 | Fix within 1 month — moderate risk |
| Low | 0.1 - 3.9 | 🔵 | Fix when convenient — minimal risk |

**Direct vs transitive priority:**
- **Direct dependency**: You explicitly installed it — highest priority, easiest to fix
- **Transitive dependency**: Pulled in by another package — fix by updating the direct parent
- If the transitive parent hasn't released a fix, consider overriding with `overrides` (npm) or `resolutions` (Yarn)

### Step 3: Check for Outdated Packages

Run the outdated command and categorize results:

```
── OUTDATED PACKAGES ──────────────────────

Package          Current    Latest     Type      Risk
─────────────────────────────────────────────────────
[package-a]      1.2.3      1.2.8      Patch     ✅ Safe — bug fixes only
[package-b]      2.1.0      2.4.0      Minor     ✅ Safe — new features, backward compatible
[package-c]      3.0.0      4.2.1      Major     ⚠️ Breaking — review changelog
[package-d]      1.0.0      1.0.0      Current   ✅ Up to date
```

**Version gap classification:**

| Gap Type | Risk | Approach |
|----------|------|----------|
| **Patch** (1.2.3 → 1.2.8) | Very Low | Update immediately — bug/security fixes |
| **Minor** (2.1.0 → 2.4.0) | Low | Update in batch — new features, backward compatible |
| **Major** (3.0.0 → 4.2.1) | Medium-High | Review migration guide, test thoroughly |
| **Multiple majors** (1.x → 4.x) | High | Dedicate time, may require code changes |

### Step 4: Identify Abandoned Packages

Check each dependency for maintenance status:

```
── ABANDONED PACKAGE CHECK ────────────────

Package          Last Publish    Downloads/wk    Status
──────────────────────────────────────────────────────
[package-x]      3 years ago     12,000          ⚠️ ABANDONED — find alternative
[package-y]      2.5 years ago   800             🔴 DEAD — replace immediately
[package-z]      6 months ago    250,000         ✅ Active
```

**Abandonment indicators:**
- No npm/PyPI publish in 2+ years
- No GitHub commits in 1+ year
- Open issues/PRs with no maintainer response for 6+ months
- Maintainer has publicly archived the repository
- Deprecation notice in README or package metadata

**For each abandoned package, suggest:**
- Alternative package (actively maintained fork or replacement)
- Migration effort estimate (drop-in replacement vs API changes)
- Risk of staying: known unpatched vulnerabilities, compatibility drift

### Step 5: Supply Chain Risk Assessment

Check for packages with known supply chain risk factors:

| Risk Factor | Detection Method | Severity |
|-------------|-----------------|----------|
| **Typosquatting** | Package name similar to popular package | High |
| **Install scripts** | `preinstall`/`postinstall` scripts in package.json | Medium |
| **Excessive permissions** | Package requests network/fs access unexpectedly | Medium |
| **Single maintainer** | One person controls publishing | Low-Medium |
| **Recent ownership transfer** | npm ownership changed recently | High |
| **Minified source only** | No readable source code in package | Medium |
| **Unpinned dependencies** | Using `*` or `>=` in dependency ranges | Medium |

```
── SUPPLY CHAIN RISKS ─────────────────────

[package-a]  ⚠️ Has postinstall script
  Script: "postinstall": "node setup.js"
  Review: [does it fetch remote code? write to fs? safe build step?]

[package-b]  ⚠️ Single maintainer, low download count
  Maintainer: [username]
  Weekly downloads: [count]
  Alternative: [more established package]
```

### Step 6: Generate Upgrade Plan

Create a prioritized upgrade plan in three tiers:

```
━━━ TIER 1: IMMEDIATE (This Sprint) ━━━━━━
Critical/High vulnerabilities in direct dependencies.
Patch updates with no breaking changes.

1. [package]@[current] → [target]
   Reason: 🔴 CVE-2024-XXXXX (CRITICAL)
   Risk: None — patch update
   Command: npm install [package]@[target]

2. [package]@[current] → [target]
   Reason: 🟡 CVE-2024-YYYYY (HIGH)
   Risk: None — minor update
   Command: npm install [package]@[target]

━━━ TIER 2: PLANNED (Next 2 Weeks) ━━━━━━━
Medium vulnerabilities, minor version updates,
replacing abandoned packages.

3. [package]@[current] → [target]
   Reason: 🟠 CVE-2024-ZZZZZ (MEDIUM) + 8 minor versions behind
   Risk: Low — review changelog for deprecations
   Command: npm install [package]@[target]
   Test: [specific areas to regression test]

4. [package] → [replacement-package]
   Reason: ⚠️ Abandoned (last publish: 2 years ago)
   Risk: Medium — API differences, migration needed
   Migration: [brief migration steps]

━━━ TIER 3: SCHEDULED (Next Quarter) ━━━━━━
Major version upgrades requiring migration effort.

5. [package]@[current] → [target]
   Reason: 3 major versions behind, accumulating tech debt
   Risk: High — breaking changes in v3 and v4
   Migration guide: [URL]
   Estimated effort: [hours/days]
   Test: [comprehensive regression testing required]
```

### Step 7: Override Guidance

When a transitive dependency can't be fixed by updating the direct parent:

**npm (overrides in package.json):**
```json
{
  "overrides": {
    "vulnerable-package": ">=2.0.1"
  }
}
```

**Yarn (resolutions in package.json):**
```json
{
  "resolutions": {
    "vulnerable-package": ">=2.0.1"
  }
}
```

**pnpm (overrides in package.json):**
```json
{
  "pnpm": {
    "overrides": {
      "vulnerable-package": ">=2.0.1"
    }
  }
}
```

**Pip (constraint file):**
```
# constraints.txt
vulnerable-package>=2.0.1
```
```bash
pip install -c constraints.txt -r requirements.txt
```

**Caution:** Overrides can break compatibility. Always test after applying.

### Step 8: CI Integration Recommendation

Recommend automated dependency scanning in CI:

```yaml
# GitHub Actions example
name: Dependency Audit
on:
  schedule:
    - cron: '0 9 * * 1'  # Weekly Monday 9 AM
  pull_request:
    paths:
      - 'package.json'
      - 'package-lock.json'

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm audit --audit-level=high
      - run: npm outdated || true  # Don't fail on outdated
```

**Recommended tools for ongoing monitoring:**
- **Dependabot** (GitHub): Auto-creates PRs for updates
- **Renovate** (any platform): More configurable than Dependabot
- **Snyk**: Deep vulnerability scanning + fix PRs
- **Socket.dev**: Supply chain risk detection

### Step 9: Output

Present the complete dependency health report:

```
━━━ DEPENDENCY HEALTH REPORT ━━━━━━━━━━━━━
Project: [name]
Ecosystem: [npm/pip/cargo/etc.]
Scan date: [date]
Total dependencies: [direct] direct, [transitive] transitive

── VULNERABILITY SUMMARY ──────────────────
🔴 Critical: [count]
🟡 High:     [count]
🟠 Medium:   [count]
🔵 Low:      [count]

── VULNERABILITIES ────────────────────────
[detailed CVE list with fix versions]

── OUTDATED PACKAGES ──────────────────────
Patch updates available: [count]
Minor updates available: [count]
Major updates available: [count]

── ABANDONED PACKAGES ─────────────────────
[list with alternatives]

── SUPPLY CHAIN RISKS ─────────────────────
[risk factors found]

── UPGRADE PLAN ───────────────────────────
Tier 1 (Immediate): [count] packages
Tier 2 (Planned):   [count] packages
Tier 3 (Scheduled): [count] packages

── COMMANDS ───────────────────────────────
[copy-paste upgrade commands]

── CI RECOMMENDATION ──────────────────────
[automated scanning setup]

── HEALTH SCORE ───────────────────────────
Score: [X/100]
  Vulnerabilities: [-points per severity]
  Currency: [-points per outdated major]
  Maintenance: [-points per abandoned dep]
  Supply chain: [-points per risk factor]
```

**Health score calculation:**
- Start at 100
- Critical CVE: -20 each
- High CVE: -10 each
- Medium CVE: -5 each
- Major version behind: -3 each
- Abandoned dependency: -8 each
- Supply chain risk: -5 each
- Minimum score: 0

## Inputs
- Project path (or current directory)
- Package ecosystem (auto-detected from lockfiles)
- Severity threshold (default: all)
- Include dev dependencies? (default: yes)

## Outputs
- Unified vulnerability list with CVE IDs, severity, affected package, and fix version
- Direct vs transitive dependency classification
- Outdated packages categorized by version gap type
- Abandoned package list with alternatives
- Supply chain risk assessment
- Three-tier prioritized upgrade plan with commands
- Override guidance for transitive dependency fixes
- CI integration config for ongoing monitoring
- Dependency health score (0-100)

## Level History

- **Lv.1** — Base: Multi-ecosystem audit (npm, pip, cargo, go, bundler), unified vulnerability format with CVSS severity, direct vs transitive classification, outdated package analysis, abandoned package detection with alternatives, supply chain risk assessment, three-tier upgrade plan, override guidance, CI integration config, health score. (Origin: MemStack v3.2, Mar 2026)
