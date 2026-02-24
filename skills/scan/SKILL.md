---
name: scan
description: "Use when the user says 'scan project', 'estimate', 'how much to charge', or needs codebase complexity analysis."
---


# 🔍 Scan — Analyzing Project Scope...
*Analyze a project's complexity and generate pricing recommendations.*

## Activation

When this skill activates, output:

`🔍 Scan — Analyzing project scope...`

Then execute the protocol below.

## Context Guard

| Context | Status |
|---------|--------|
| **User asks to scan or analyze a project** | ACTIVE — full scan |
| **User asks about pricing or estimates** | ACTIVE — full scan + pricing |
| **User mentions project metrics (LOC, file count)** | ACTIVE — quick metrics |
| **Discussing project analysis concepts generally** | DORMANT — do not activate |
| **User is building/coding, not analyzing** | DORMANT — do not activate |

## Protocol

1. **Scan the codebase:**
   ```bash
   find . -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.py" -o -name "*.css" \) | wc -l
   find . -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" \) -exec cat {} + | wc -l
   ```

2. **Count key components:** pages/routes, API endpoints, database tables, external integrations, auth complexity

3. **Assess complexity tier:**
   - **Simple** (< 20 files, < 3K LOC): $500–$2,000
   - **Medium** (20-60 files, 3K-15K LOC): $2,000–$8,000
   - **Complex** (60-150 files, 15K-50K LOC): $8,000–$25,000
   - **Enterprise** (150+ files, 50K+ LOC): $25,000+

4. **Factor in:** Auth (+2FA/SSO), payments (+$1-3K), real-time (+$1-2K), admin panel (+$2-5K), mobile responsive (+20-30%), per API integration (+$500-1.5K)

5. **Generate three-tier pricing:** Budget, Standard, Premium

## Inputs
- Project directory path
- New build vs maintenance estimate

## Outputs
- Project analysis: file counts, LOC, endpoints, tables
- Complexity tier assessment
- Three-tier pricing recommendation

## Example Usage

**User:** "scan AdminStack and estimate pricing"

```
🔍 Scan — Analyzing project scope...

Files: 127 | LOC: ~28,000 | Pages: 27 | API Routes: 34 | Tables: 20
Integrations: Supabase, Stripe, Square, SendGrid, Railway, Hetzner
Complexity: Complex tier

Budget:   $15,000 — Core features, basic styling
Standard: $22,000 — Full features, admin panel, responsive
Premium:  $30,000 — Full + custom integrations + 3mo support
```

## Level History

- **Lv.1** — Base: File/LOC counting with complexity assessment. (Origin: MemStack v1.0, Feb 2026)
- **Lv.2** — Enhanced: Added YAML frontmatter, context guard, activation message, integration pricing. (Origin: MemStack v2.0 MemoryCore merge, Feb 2026)
