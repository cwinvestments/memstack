# Forge — MemStack Skill

## Trigger Keywords
- create enchantment, forge this, new skill, improve skill, add skill

## Purpose
Create new MemStack skills or improve existing ones. Walks through the creation process step by step.

## Instructions

### Creating a new skill:

1. **Ask the user:**
   - What should the skill do?
   - What trigger keywords should activate it?
   - What inputs does it need?
   - What should it output?

2. **Generate the skill file** following the standard format:
   ```markdown
   # [Name] — MemStack Skill

   ## Trigger Keywords
   ## Purpose
   ## Instructions
   ## Inputs
   ## Outputs
   ## Example Usage
   ```

3. **Write the file** to `C:\Projects\memstack\skills\{name}.md`

4. **Update MEMSTACK.md** — add a new row to the Skill Index table with:
   - Next number in sequence
   - Skill name
   - Brief function description
   - Trigger keywords

5. **Confirm creation** — show the user the new skill summary

### Improving an existing skill:

1. **Read the current skill file**
2. **Identify what to improve** based on user feedback
3. **Update the file** — keep the same format, enhance the instructions
4. **Confirm changes**

## Inputs
- Skill concept description
- Trigger keywords
- Desired behavior

## Outputs
- New skill .md file in skills/
- Updated MEMSTACK.md index
- Confirmation summary

## Example Usage

**User prompt:** "forge a new skill called Beacon that pings a health check endpoint every 5 minutes"

**Forge activates:**

```
Creating new MemStack skill: Beacon

Skill name: Beacon
Triggers: "health check", "ping", "uptime"
Purpose: Periodically ping health check endpoints and report status

Writing: skills/beacon.md ✓
Updating: MEMSTACK.md — added row #15 ✓

Beacon skill created. It will activate when you say:
  "health check", "ping", or "uptime"
```
