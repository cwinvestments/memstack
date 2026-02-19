# Quill — MemStack Skill

## Trigger Keywords
- create quotation, generate quote, write proposal, client quote, proposal

## Purpose
Generate professional client quotations and proposals using project analysis and templates.

## Instructions

1. **Gather requirements** — ask the user for:
   - Client name and company
   - Project description (or say "use Scan results" if just scanned)
   - Timeline expectations
   - Any specific requirements or constraints

2. **If project was already scanned** — use the Scan results for scope and pricing
3. **If not scanned** — run a quick Scan first to get baseline metrics

4. **Generate the quotation** using `templates/client-quote.md`:
   - Professional header with your company info
   - Project scope breakdown with line items
   - Three pricing tiers (if applicable)
   - Timeline with milestones
   - Terms and conditions
   - Valid-until date (30 days from now)

5. **Save the quotation** to `memory/projects/{client}-quote-{date}.md`
6. **Present it** formatted for copy-paste into email or PDF export

## Inputs
- Client name and company
- Project requirements
- Scan results (optional — will auto-scan if needed)

## Outputs
- Professional quotation document
- Saved copy in memory/projects/

## Example Usage

**User prompt:** "generate a quote for John at GreenTech Corp for a project similar to AdminStack"

**Quill activates:**

```
CW AFFILIATE INVESTMENTS
Project Quotation — GreenTech Corp
Date: 2026-02-18
Valid Until: 2026-03-20

Prepared for: John, GreenTech Corp

PROJECT SCOPE
━━━━━━━━━━━━
Full-stack admin dashboard with:
- User authentication with 2FA
- Multi-tenant organization system
- Contact management with email broadcasts
- Order management with payment integration
- Infrastructure monitoring dashboard
- Role-based access control

PRICING
━━━━━━━
Standard Package: $22,000
  - All features listed above
  - Mobile responsive design
  - 30-day bug fix warranty

TIMELINE
━━━━━━━━
Week 1-2: Database schema, auth, core layouts
Week 3-4: CRUD pages, API routes
Week 5-6: Integrations, admin panel, polish
Week 7: Testing, deployment, handoff

Quotation saved: memory/projects/greentech-quote-2026-02-18.md
```
