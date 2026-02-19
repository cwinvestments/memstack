# Scan — MemStack Skill

## Trigger Keywords
- scan project, analyze project, how much should I charge, how much to charge, estimate

## Purpose
Analyze a project's scope, complexity, and technology stack to generate a pricing recommendation.

## Instructions

1. **Scan the codebase:**
   ```bash
   find . -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" -o -name "*.py" -o -name "*.css" \) | wc -l
   find . -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" \) -exec cat {} + | wc -l
   ```

2. **Count key components:**
   - Pages / routes
   - API endpoints
   - Database tables
   - External integrations (Stripe, Supabase, email, etc.)
   - Authentication system complexity
   - File upload / media handling

3. **Assess complexity tier:**
   - **Simple** (< 20 files, < 3K LOC, 1-3 pages): $500–$2,000
   - **Medium** (20-60 files, 3K-15K LOC, 4-10 pages): $2,000–$8,000
   - **Complex** (60-150 files, 15K-50K LOC, 10-25 pages): $8,000–$25,000
   - **Enterprise** (150+ files, 50K+ LOC, 25+ pages): $25,000+

4. **Factor in:**
   - Auth complexity (basic vs 2FA vs SSO)
   - Payment integration (adds $1,000–$3,000)
   - Real-time features (adds $1,000–$2,000)
   - Admin dashboard (adds $2,000–$5,000)
   - Mobile responsiveness (adds 20-30%)
   - API integrations per service ($500–$1,500 each)

5. **Generate pricing report** with three tiers: Budget, Standard, Premium

## Inputs
- Project directory path
- Whether this is a new build or maintenance estimate

## Outputs
- Project analysis report: file counts, LOC, endpoints, tables
- Complexity tier assessment
- Three-tier pricing recommendation with justification

## Example Usage

**User prompt:** "scan AdminStack and tell me what I should charge for something like this"

**Scan activates:**

```
AdminStack Project Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━
Files: 127 source files
Lines of Code: ~28,000
Pages: 22 dashboard pages + 5 auth pages
API Routes: 34 endpoints
Database Tables: 19
Integrations: Supabase, Stripe, Square, SendGrid, Railway, Hetzner

Complexity: Complex tier

Pricing Recommendation:
  Budget:   $15,000 — Core features, basic styling, no admin panel
  Standard: $22,000 — Full feature set, admin panel, responsive
  Premium:  $30,000 — Full features + custom integrations + 3mo support
```
