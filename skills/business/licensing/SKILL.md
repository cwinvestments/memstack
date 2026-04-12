---
name: memstack-business-licensing
description: "Use this skill when the user says 'licensing', 'license audit', 'can I use this commercially', 'OSS license check', 'license compatibility', 'GPL', 'MIT', 'AGPL', 'copyleft'. Scans the repository for every dependency and asset license, then produces a per-package verdict table: ready for commercial use, citation/attribution required, more information needed, or commercial use not allowed. Do NOT use for vulnerability scanning (use dependency-audit) or contract drafting (use contract-template)."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# Licensing — Commercial-use license audit from the repo...
*Scans a repository for every license that touches the product (deps, vendored code, fonts, assets), then produces a per-package verdict table marking each as Ready, Citation Required, Needs Info, or Not Allowed for commercial use.*

## Activation

When this skill activates, output:

`Licensing — Commercial-use license audit from the repo...`

Then execute the protocol below.

## Context Guard

| Context | Status |
|---------|--------|
| User says "license audit", "licensing", "license check" | ACTIVE |
| User asks "can I use this commercially?" or "is this safe to ship?" | ACTIVE |
| User mentions GPL, AGPL, LGPL, MPL, MIT, BSD, Apache, copyleft | ACTIVE |
| User is preparing to ship, sell, or relicense a product | ACTIVE |
| User wants security vulnerability scanning | DORMANT — use dependency-audit |
| User wants a service contract or NDA | DORMANT — use contract-template |

## Common Mistakes

| Mistake | Why It's Wrong |
|---------|---------------|
| "MIT and GPL are both open source so they're compatible" | Combining MIT into GPL is fine; the reverse forces your code under GPL. Direction matters. |
| "We don't distribute, so AGPL doesn't apply" | AGPL §13 triggers on *network use*. SaaS counts. |
| "It's on GitHub so it's free to use" | Public ≠ licensed. No LICENSE file = all rights reserved. |
| "Transitive dependencies don't matter" | Your bundle ships every dep in the tree. Copyleft transitives can taint the whole product. |
| "License from package.json metadata is authoritative" | The actual `LICENSE` file in upstream source is authoritative. Metadata is often wrong, missing, or outdated. |
| "BSL / SSPL / Elastic / Commons Clause are open source" | They are not OSI-approved and usually restrict commercial hosting or competition. Read the actual terms. |

**Disclaimer:** Produces a license inventory and risk assessment, not legal advice. License interpretation — especially copyleft scope, "linking", and SaaS triggers — is contested. Engage IP counsel before shipping high-stakes products.

## Protocol

### Step 1: Confirm the distribution model

Just one question — the verdict logic depends on it:

> How is the product distributed?
> - **A. SaaS / hosted** (users access over the network, no binary handed out)
> - **B. Distributed binary** (desktop, mobile, on-prem install, downloadable executable)
> - **C. Open-source library** you publish for others to consume
> - **D. Internal only** (no users outside your organisation)

Default to A if the repo contains web framework code (Next.js, FastAPI, Rails, etc.) and no installer/build target.

### Step 2: Scan the repo for every license source

Walk every manifest, lockfile, vendored directory, and asset folder. Never trust a single source — cross-check.

| Stack | Manifest | Discovery command |
|-------|----------|-------------------|
| Node.js | `package.json`, `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock` | `npm ls --all --json` then `npx license-checker --json --production` |
| Python | `requirements*.txt`, `pyproject.toml`, `Pipfile.lock`, `poetry.lock` | `pip-licenses --format=json --with-license-file --with-urls` |
| Rust | `Cargo.toml`, `Cargo.lock` | `cargo license --json` |
| Go | `go.mod`, `go.sum` | `go-licenses report ./... --template '{{.Name}},{{.LicenseName}},{{.LicenseURL}}'` |
| Java | `pom.xml`, `build.gradle` | `mvn license:add-third-party` or `gradle-license-report` |
| Ruby | `Gemfile`, `Gemfile.lock` | `bundle exec license_finder report --format json` |
| PHP | `composer.json`, `composer.lock` | `composer licenses --format=json` |
| .NET | `*.csproj`, `packages.lock.json` | `dotnet list package --include-transitive` + `nuget-license` |
| Container base images | `Dockerfile` | `syft <image> -o spdx-json` then read package licenses |
| Vendored / submodules | `vendor/`, `third_party/`, `.gitmodules` | walk directories — look for `LICENSE`, `LICENSE.md`, `COPYING`, `NOTICE` |
| Fonts / icons / media | `assets/`, `public/`, `static/` | check each asset's source license — **commonly missed** |
| Snippets and copy-pasted code | comments, headers | `grep -rEin "Copyright|SPDX-License-Identifier"` |

For everything found, capture:

```markdown
| Package | Version | Declared license (manifest) | License file present | Direct/transitive | Source URL |
|---------|---------|----------------------------|---------------------|-------------------|------------|
| react | 18.3.1 | MIT | Yes | direct | github.com/facebook/react |
| ... | ... | ... | ... | ... | ... |
```

### Step 3: Resolve the actual license (don't trust metadata)

For every entry that is HIGH-impact (copyleft candidate, missing license, or version where licenses are known to change), open the upstream `LICENSE` file and confirm the SPDX identifier.

Watch for **license changes between versions**:

| Project | Version cut | Old → New |
|---------|-------------|-----------|
| Elasticsearch | 7.10 → 7.11 | Apache-2.0 → SSPL/Elastic |
| Redis | 7.2 → 7.4 | BSD → SSPL/RSAL |
| Terraform | 1.5 → 1.6 | MPL-2.0 → BSL |
| MongoDB | 4.0 | AGPL → SSPL |
| HashiCorp tools | 2023 | MPL-2.0 → BSL |
| Sentry | 8.x | BSD → FSL |

Pin to the last compliant version or migrate.

Also check for:
- **Dual licensing** ("MIT OR Apache-2.0") — pick the option you'll comply with and record the choice
- **Commons Clause** layered on top of an OSI license — restricts "selling"
- **Custom / vendor licenses** — read the actual terms verbatim

### Step 4: Classify each license

| Class | Examples | Commercial use allowed? | Reach |
|-------|----------|------------------------|-------|
| **Public domain** | CC0, Unlicense, WTFPL, 0BSD | Yes — no obligations | None |
| **Permissive** | MIT, BSD-2/3, ISC, Apache-2.0, Zlib | Yes — preserve notice | None |
| **Weak copyleft** | LGPL-2.1, LGPL-3.0, MPL-2.0, EPL-2.0 | Yes with obligations | File-level (MPL) or dynamic-linking carve-out (LGPL) |
| **Strong copyleft** | GPL-2.0, GPL-3.0 | Yes — but derivative works become GPL on distribution | Whole derivative work |
| **Network copyleft** | AGPL-3.0 | Yes — but SaaS triggers source disclosure | Whole derivative work + network use |
| **Source-available (non-OSI)** | BSL, SSPL, Elastic v2, Commons Clause, RSAL, FSL | **Restricted** — usually no competing hosted service | Per terms |
| **Creative Commons** | CC-BY, CC-BY-SA, CC-BY-NC, CC-BY-ND | NC = no commercial; SA = share-alike; ND = no derivatives | Per variant |
| **Proprietary / commercial EULA** | Vendor SDKs, paid libraries | Per contract | Per contract |
| **Unknown / no license** | No LICENSE file | **No — all rights reserved by default** | N/A |

### Step 5: Apply the verdict per package

For every dependency, run it through the **distribution model from Step 1** and assign exactly one verdict:

| Verdict | Symbol | Meaning |
|---------|--------|---------|
| **Ready for commercial use** | ✅ | No obligations beyond preserving the existing notice file. Safe to ship. |
| **Citation / attribution required** | 📝 | Commercial use is allowed but the license **requires** the copyright notice and license text to be reproduced (typically in `THIRD_PARTY_LICENSES.md`, an About page, or alongside the binary). MIT, BSD, Apache-2.0, ISC, Zlib all fall here when shipped to users. |
| **More information needed** | ❓ | License is unknown, ambiguous, dual-licensed, or version-changed. Cannot ship until resolved. |
| **Not allowed for commercial use** | ❌ | License blocks the chosen distribution model. Must replace, remove, relicense, or buy a commercial exception. |

**Verdict rules per distribution model:**

| License class | A. SaaS | B. Binary | C. OSS library | D. Internal |
|---------------|---------|-----------|----------------|-------------|
| Public domain | ✅ | ✅ | ✅ | ✅ |
| Permissive (MIT, BSD, Apache, ISC, Zlib) | 📝 | 📝 | 📝 | ✅ |
| LGPL | 📝 | 📝 (must allow relinking) | 📝 | ✅ |
| MPL-2.0 / EPL-2.0 | 📝 | 📝 (file-level disclosure) | 📝 | ✅ |
| GPL-2.0 / GPL-3.0 | 📝 (no distribution = no source disclosure) | ❌ (forces whole product GPL) | ❌ unless your lib is also GPL | ✅ |
| AGPL-3.0 | ❌ (network use triggers source disclosure) | ❌ | ❌ unless your lib is AGPL | ✅ |
| BSL | ❓ → usually ❌ for SaaS (read additional use grant) | ❓ | ❌ | ✅ |
| SSPL | ❌ for SaaS | ❌ | ❌ | ✅ |
| Elastic v2 / Commons Clause / RSAL / FSL | ❌ | ❌ | ❌ | ✅ |
| CC-BY | 📝 | 📝 | 📝 | ✅ |
| CC-BY-SA | 📝 (share-alike on derivatives) | 📝 | ❌ unless your work is also SA | ✅ |
| CC-BY-NC | ❌ | ❌ | ❌ | ✅ |
| CC-BY-ND | ❌ if modified | ❌ if modified | ❌ if modified | ✅ |
| Proprietary EULA | per contract | per contract | per contract | per contract |
| Unknown / no license | ❓ → ❌ until resolved | ❓ → ❌ | ❓ → ❌ | ❓ → ❌ |

### Step 6: Build the verdict table

This is the primary deliverable. One row per dependency, sorted by verdict severity (❌ → ❓ → 📝 → ✅).

```markdown
| Package | Version | License | Direct/Trans | Verdict | Required action |
|---------|---------|---------|--------------|---------|----------------|
| ❌ mongodb | 6.0.5 | SSPL-1.0 | direct | ❌ Not allowed for SaaS | Replace with PostgreSQL or buy commercial license |
| ❌ some-lib | 2.1.0 | AGPL-3.0 | direct | ❌ Not allowed for SaaS | Replace with permissive alternative |
| ❓ obscure-pkg | 0.4.2 | (no LICENSE file) | transitive | ❓ Unknown | Open upstream issue; pin or remove until resolved |
| ❓ dual-pkg | 1.2.0 | "MIT OR GPL-3.0" | direct | ❓ Choose | Document MIT election in NOTICE |
| 📝 react | 18.3.1 | MIT | direct | 📝 Citation required | Add to THIRD_PARTY_LICENSES.md |
| 📝 fastify | 4.26.0 | MIT | direct | 📝 Citation required | Add to THIRD_PARTY_LICENSES.md |
| 📝 lodash | 4.17.21 | MIT | transitive | 📝 Citation required | Add to THIRD_PARTY_LICENSES.md |
| 📝 protobufjs | 7.2.5 | BSD-3-Clause | transitive | 📝 Citation required | Add to THIRD_PARTY_LICENSES.md |
| 📝 fonts/inter | — | OFL-1.1 | asset | 📝 Citation required | Include OFL.txt in assets/fonts/ |
| ✅ classnames | 2.5.1 | MIT | transitive | ✅ Ready | (already in attribution bundle) |
| ✅ public-domain-pkg | 1.0.0 | CC0-1.0 | direct | ✅ Ready | None |
```

### Step 7: Generate the attribution bundle

For every 📝 row, the user needs a `THIRD_PARTY_LICENSES.md` (or `NOTICES.txt`) shipped alongside the product. Offer to generate it:

```markdown
# Third-Party Licenses

This product includes the following third-party software:

## react v18.3.1
**License:** MIT
**Source:** https://github.com/facebook/react
**Copyright:** Copyright (c) Meta Platforms, Inc. and affiliates.

[Full MIT license text verbatim]

---

## next-package vA.B.C
...
```

For Apache-2.0 deps, also preserve any upstream `NOTICE` file content.

### Step 8: Produce the report

```markdown
## License Audit — [Project Name]

**Date:** [YYYY-MM-DD]
**Distribution model:** [A. SaaS / B. Binary / C. Library / D. Internal]
**Project's own license:** [SPDX or "proprietary"]
**Total dependencies analysed:** [N direct + M transitive + K assets]

### Verdict summary
| Verdict | Count |
|---------|-------|
| ❌ Not allowed for commercial use | [N] |
| ❓ More information needed | [N] |
| 📝 Citation / attribution required | [N] |
| ✅ Ready for commercial use | [N] |

### Commercial-use verdict
**[CLEAR TO SHIP / CLEAR WITH CITATION OBLIGATIONS / BLOCKED]**

[2–3 sentences explaining the verdict and naming the specific blockers if any.]

### Full verdict table
[Table from Step 6]

### Required attribution bundle
[Either inline THIRD_PARTY_LICENSES.md content, or a list of packages that must appear in it]

### Remediation plan (priority order)
1. **❌ [Blocker]** — [package] — [replace with X / remove feature Y / buy license / quarantine]
2. **❓ [Unknown]** — [package] — [investigation step]
3. **📝 [Attribution gap]** — [add to THIRD_PARTY_LICENSES.md]

### Recommended next steps
1. Resolve every ❌ before shipping
2. Resolve every ❓ before shipping
3. Generate / update `THIRD_PARTY_LICENSES.md` and ship with the product
4. Add an automated license check to CI to catch new dependencies
5. Re-run this audit before each release
6. Have IP counsel review if any BSL/SSPL/AGPL/unknown findings remain
```

## Output Format

Deliver the Step 8 report as markdown. Save under `docs/compliance/license-audit.md` if a project layout is available. Save the generated attribution bundle as `THIRD_PARTY_LICENSES.md` at the repo root. Include the exact discovery commands you ran in an appendix so the user can reproduce.

## Completion

```
Licensing — Audit complete!

Distribution model: [A / B / C / D]
Dependencies analysed: [N direct + M transitive + K assets]
❌ Blocked: [N]
❓ Unknown: [N]
📝 Citation required: [N]
✅ Ready: [N]
Verdict: [CLEAR / CLEAR WITH OBLIGATIONS / BLOCKED]

Next steps:
1. Resolve every ❌ before shipping
2. Resolve every ❓ before shipping
3. Ship THIRD_PARTY_LICENSES.md alongside the product
4. Add license check to CI
5. Have IP counsel review high-risk findings
```

## Level History

- **Lv.1** — Base: distribution-model question, multi-language repo scan (Node/Python/Rust/Go/Java/Ruby/PHP/.NET/containers/vendored/assets), upstream LICENSE verification, version-change traps (Elastic/Mongo/Redis/Terraform/Sentry/HashiCorp), 9-class taxonomy, 4-verdict system (✅ Ready / 📝 Citation / ❓ Needs info / ❌ Not allowed), distribution-model verdict matrix, primary verdict table, attribution bundle generator, full report with summary counts and remediation plan. (Origin: MemStack Pro v3.6, Apr 2026)
