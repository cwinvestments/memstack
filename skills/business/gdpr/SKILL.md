---
name: memstack-business-gdpr
description: "Use this skill when the user says 'GDPR', 'data protection', 'privacy compliance', 'DPA', 'DSAR', 'data subject request', 'cookie consent', 'privacy audit', 'CCPA', or asks 'do I need GDPR for this repo'. Scans the repository to detect what personal data is collected, classifies sensitivity, determines whether GDPR applies and how critical it is, then reports required roles, obligations, and remediation. Do NOT use for general security audits (use owasp-top10) or contract drafting (use contract-template)."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# GDPR — Personal-data assessment from the repo...
*Scans a repository for evidence of personal data collection, classifies sensitivity under GDPR, decides whether GDPR applies and how critical the obligations are, and reports the required roles, articles to satisfy, and remediation plan.*

## Activation

When this skill activates, output:

`GDPR — Personal-data assessment from the repo...`

Then execute the protocol below.

## Context Guard

| Context | Status |
|---------|--------|
| User says "GDPR", "data protection", "privacy compliance" | ACTIVE |
| User asks "do I need GDPR", "does GDPR apply to this project" | ACTIVE |
| User says "DSAR", "right to be forgotten", "cookie consent", "DPA" | ACTIVE |
| User asks about CCPA, LGPD, PIPEDA, UK GDPR | ACTIVE |
| User wants a generic security audit | DORMANT — use owasp-top10 |
| User wants a service agreement or NDA | DORMANT — use contract-template |
| User wants RLS / database access policies | DORMANT — use rls-checker |

## Common Mistakes

| Mistake | Why It's Wrong |
|---------|---------------|
| "We're a US company so GDPR doesn't apply" | GDPR follows the data subject, not the company. Any EU/UK resident's data triggers it. |
| "Hashed emails aren't personal data" | Hashes are still personal data if reversible or linkable. True anonymisation is irreversible. |
| "Cookie banner with only Accept" | Reject must be equally prominent. Pre-ticked = invalid consent. |
| "Legitimate interest covers everything" | Requires a documented balancing test. Cannot be used for special category data or marketing to children. |
| "We'll get the DPA later" | Article 28 requires a written DPA *before* processing begins. |
| "72-hour clock starts after we finish investigating" | The clock starts on *awareness* of a likely breach. |

**Disclaimer:** Produces a compliance assessment, not legal advice. Engage a qualified DPO or data-protection lawyer before relying on outputs for regulated processing.

## Protocol

### Step 1: Scan the repo for personal-data signals

Don't ask the user what they collect — find out from the code. Run discovery against every relevant surface:

**Database schemas / migrations**
```bash
find . \( -name "*.sql" -o -name "schema.prisma" -o -name "models.py" -o -name "*.dbml" \) -not -path "*/node_modules/*"
grep -rEin "email|phone|address|first_?name|last_?name|date_?of_?birth|dob|ssn|passport|tax_?id|national_?id|ip_?address|geo|lat|lng|location|gender|race|religion|health|medical|biometric|fingerprint|face|child|minor" --include="*.sql" --include="*.prisma" --include="*.py" --include="*.ts"
```

**Form / UI input fields**
```bash
grep -rEin "<input[^>]*name=|formField|FormControl|registerField" --include="*.tsx" --include="*.jsx" --include="*.vue" --include="*.svelte"
grep -rEin "type=[\"']email[\"']|type=[\"']tel[\"']|autoComplete=[\"'](name|email|tel|address|cc-|bday)" .
```

**API request schemas / DTOs**
```bash
grep -rEin "z\.object|class.*BaseModel|interface.*Request|Schema\(" --include="*.ts" --include="*.py"
```

**Auth configuration**
```bash
find . -iname "auth*" -o -iname "*supabase*" -o -iname "*clerk*" -o -iname "*next-auth*" -o -iname "*firebase*"
grep -rEin "providers:|GoogleProvider|GitHubProvider|EmailProvider|magicLink|phoneSignIn"
```

**Analytics / tracking SDKs**
```bash
grep -rEin "posthog|mixpanel|amplitude|segment|google-?analytics|gtag|fbq|hotjar|fullstory|datadog.*RUM|sentry" .
```

**Cookies / sessions**
```bash
grep -rEin "Set-Cookie|cookies\.set|res\.cookie|getServerSession|session\(" .
```

**Logging that may capture PII**
```bash
grep -rEin "console\.log.*req\.|logger\.(info|debug).*body|print\(.*request" .
```

**Third-party data recipients**
```bash
cat package.json requirements.txt pyproject.toml composer.json Gemfile 2>/dev/null | grep -Ei "stripe|paypal|sendgrid|mailgun|twilio|openai|anthropic|hubspot|intercom|zendesk|algolia"
```

**Existing privacy artifacts (gap check)**
```bash
find . \( -iname "privacy*" -o -iname "*dpa*" -o -iname "ropa*" -o -iname "cookie-policy*" -o -iname "data-processing*" \)
```

Record findings in a working table:

```markdown
| Source | Field / Signal | Personal Data? | Sensitivity Class |
|--------|---------------|----------------|-------------------|
| db/schema.sql L42 | users.email | Yes | Identifier |
| db/schema.sql L43 | users.phone | Yes | Identifier |
| src/forms/Profile.tsx L18 | dob input | Yes | Identifier (age) |
| src/forms/Health.tsx L7 | medical_conditions | Yes | **Special category (Art 9)** |
| package.json | posthog-js | Yes — behavioral | Behavioral |
| src/api/users.ts L88 | logger.info(req.body) | Possible PII leak | Risk |
```

If no personal-data signals are found, jump to Step 3 with verdict NO and stop.

### Step 2: Classify sensitivity

Bucket every confirmed finding into one or more of:

| Class | Examples | GDPR Treatment |
|-------|----------|----------------|
| **Identifier** | name, email, phone, address, account ID, IP | Standard personal data — Art 6 lawful basis required |
| **Financial** | card number, bank account, billing address | Standard personal data + PCI scope considerations |
| **Location** | precise GPS, geo, IP-derived city | Standard personal data; precise location may require explicit consent |
| **Behavioral** | clickstream, page views, session recording, fingerprint | Standard personal data; consent for non-essential cookies/tracking |
| **Government ID** | passport, SSN, national ID, driver's licence | Standard personal data but elevated risk; often national-law restricted |
| **Special category — Art 9** | health, biometric, genetic, race, ethnicity, religion, political, sexual orientation, trade-union | **Prohibited unless** an Art 9(2) condition applies — almost always **explicit consent** |
| **Children's data — Art 8** | any data from users under 16 (age varies 13–16 by member state) | Requires parental consent for information-society services |
| **Criminal data — Art 10** | offences, convictions | Only under official authority or specific national law |

### Step 3: Verdict — does GDPR apply, and how critical?

```markdown
| Question | Answer |
|----------|--------|
| Is any personal data collected? | [Yes / No] |
| Are EU/UK data subjects in scope? | [Yes / Probably (global product) / No (closed user base)] |
| Any special category data (Art 9)? | [Yes / No] |
| Any children's data (Art 8)? | [Yes / No] |
| Large-scale or systematic monitoring? | [Yes / No] |
| Third parties / processors involved? | [Yes / No] |
| Cross-border transfers outside EU/UK? | [Yes / No / Unknown] |
```

**Verdict matrix:**

| Scenario | Verdict | Criticality |
|----------|---------|-------------|
| No personal data at all | GDPR does **not apply** | None |
| Personal data + EU/UK subjects unlikely (e.g. closed internal tool, non-EU user base) | GDPR applies if even one EU/UK subject; treat as best practice | 🟩 LOW |
| Standard identifiers + EU/UK subjects | GDPR **applies** | 🟨 MEDIUM |
| Identifiers + financial / location / behavioral tracking | GDPR **applies**, multiple obligations | 🟧 HIGH |
| Any Art 9 special category data | GDPR **applies**, **strict** | 🟥 CRITICAL |
| Any children's data | GDPR **applies**, **strict** + Art 8 parental consent | 🟥 CRITICAL |
| Large-scale systematic monitoring or profiling | GDPR **applies**, DPIA required | 🟥 CRITICAL |

### Step 4: Map required roles

Based on the verdict, list which roles the project must staff:

| Role | Triggered When | Status |
|------|---------------|--------|
| **Controller** (Art 4(7)) | Project decides purposes and means of processing — almost always you | Required |
| **Joint controllers** (Art 26) | Shared decisions with another org | Check |
| **Processor** (Art 4(8)) | You process data on behalf of another controller | Check |
| **DPO** (Art 37) | Public authority, OR core activities = large-scale systematic monitoring, OR core activities = large-scale special category | Required if any trigger |
| **Art 27 EU representative** | Controller/processor not established in EU but processes EU data, AND processing is not occasional | Required if any trigger |
| **Internal owner** | Every project — accountable for GDPR posture day-to-day | Required |

### Step 5: Map required articles to fulfill

Only list the articles that actually trigger for this project, with a one-line "what to do" for each:

| Article | Obligation | Triggered? | Concrete action |
|---------|------------|------------|----------------|
| Art 5 — Principles | Lawfulness, fairness, transparency, purpose limitation, minimisation, accuracy, storage limitation, integrity, accountability | Always | Document each principle is met |
| Art 6 — Lawful basis | Pick one of 6 bases per processing activity | Always | Add lawful basis column to ROPA |
| Art 7 — Conditions for consent | If any basis is consent | If consent | Implement explicit, granular, withdrawable consent UI |
| Art 8 — Children | If under-16 users | If children | Parental consent flow |
| Art 9 — Special category | If health/biometric/etc. | If Art 9 data | Explicit consent + extra safeguards |
| Art 13/14 — Transparency | Privacy notice at collection | Always | Publish privacy policy that mirrors actual processing |
| Art 15–22 — Subject rights | Access, rectification, erasure, restriction, portability, objection, ADM | Always | Implement DSAR endpoint + 30-day SLA |
| Art 25 — Privacy by design | Default settings minimise data | Always | Code review checklist |
| Art 28 — Processors | Written DPA before processing | If any processor | Sign DPAs with every vendor |
| Art 30 — ROPA | Record of Processing Activities | If 250+ employees OR not occasional OR Art 9 | Maintain ROPA |
| Art 32 — Security | TIA-equivalent technical/organisational measures | Always | Document encryption, access control, backups |
| Art 33 — Breach to authority | 72h notification | Always | Breach runbook |
| Art 34 — Breach to subjects | Without undue delay if high risk | Always | Subject notification template |
| Art 35 — DPIA | High-risk processing | If profiling/large scale/Art 9 | Run DPIA before launch |
| Art 37–39 — DPO | If triggered (see Step 4) | If triggered | Appoint and publish |
| Chapter V — Transfers | International transfers | If any | SCCs / adequacy / BCRs + TIA |

### Step 6: Gap analysis from the repo

For each triggered article in Step 5, check whether the repo already has evidence of the obligation:

```markdown
| Obligation | Evidence in repo? | Gap |
|------------|-------------------|-----|
| Privacy policy (Art 13) | ❌ Not found | Draft from ROPA |
| Cookie banner (ePrivacy + Art 6) | ✅ src/components/CookieBanner.tsx | Verify reject is equally prominent |
| DSAR endpoint (Art 15–22) | ❌ Not found | Implement /api/account/export and /api/account/delete |
| DPA with Stripe (Art 28) | ❓ Unknown | Confirm signed, store reference |
| Breach runbook (Art 33) | ❌ Not found | Create docs/security/breach-runbook.md |
| ROPA (Art 30) | ❌ Not found | Draft from Step 1 inventory |
| DPIA (Art 35) | ❌ Required (Art 9 data present) | Run before any launch |
```

### Step 7: Produce the assessment report

```markdown
## GDPR Assessment — [Project Name]

**Date:** [YYYY-MM-DD]
**Verdict:** GDPR **[APPLIES / DOES NOT APPLY / APPLIES AS BEST PRACTICE]**
**Criticality:** [🟥 CRITICAL / 🟧 HIGH / 🟨 MEDIUM / 🟩 LOW / None]

### Why this verdict
[2–4 sentences referencing the specific data found in Step 1: e.g. "The repo collects user emails, phone numbers, dates of birth, and self-reported medical conditions through src/forms/Health.tsx. The medical_conditions field is special category data under Article 9, which elevates the project to CRITICAL regardless of user geography."]

### Personal data inventory
[Table from Step 1, filtered to confirmed personal data]

### Sensitivity classification
[Counts per class from Step 2]

### Required roles
[Table from Step 4]

### Required articles to satisfy
[Filtered table from Step 5 showing only triggered rows]

### Gaps found in the repo
[Table from Step 6]

### Remediation plan (priority order)
1. **🟥 [Critical fix]** — [what + which file/system + estimated effort]
2. **🟧 [High fix]** — ...
3. **🟨 [Medium fix]** — ...
4. **🟩 [Low / hardening]** — ...

### What to do if you ignore this
[1–3 sentences naming the concrete legal exposure: maximum fines under Art 83 are €20M or 4% of global annual turnover, whichever is higher; supervisory authority enforcement; reputational damage; civil claims under Art 82.]

### Recommended next steps
1. [Owner] — [Action] — [Due]
2. ...
```

## Output Format

Deliver the Step 7 report as markdown. Save under `docs/compliance/gdpr-assessment.md` if a project layout is available. Include the exact discovery commands you ran in an appendix so the user can reproduce the scan.

## Completion

```
GDPR — Assessment complete!

Verdict: [APPLIES / DOES NOT APPLY / BEST PRACTICE]
Criticality: [tier]
Personal data fields found: [N]
Special category fields: [N]
Triggered articles: [N]
Gaps to remediate: [N]

Next steps:
1. Address all 🟥 CRITICAL gaps before any further processing
2. Draft missing artifacts (privacy policy, ROPA, DPA, breach runbook)
3. Implement DSAR endpoints in the codebase
4. Run a DPIA if special-category or large-scale profiling is in scope
5. Have a qualified DPO or data-protection lawyer review before going live
```

## Level History

- **Lv.1** — Base: repo-driven scan across schemas/forms/DTOs/auth/analytics/cookies/logging/third parties, sensitivity classification (identifier/financial/location/behavioral/Art 9/Art 8/Art 10), verdict matrix with 7 scenarios, role mapping (Controller/Processor/DPO/Art 27 rep), 16-article obligation map, repo gap analysis, full assessment report with criticality tier, why-this-verdict section, remediation priority list, and exposure summary. (Origin: MemStack Pro v3.6, Apr 2026)
