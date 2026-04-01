---
name: forge
description: "Use when the user says 'forge this', 'new skill', 'create enchantment', or wants to create a MemStack skill."
version: 1.0.0
---


# 🔨 Forge — Creating New Enchantment...
*Create new MemStack skills or improve existing ones.*

## Activation

When this skill activates, output:

`🔨 Forge — Creating new enchantment...`

Then execute the protocol below.

## Protocol

### Creating a new skill:

1. **Ask the user:**
   - What should the skill do?
   - What trigger keywords should activate it?
   - What inputs does it need? What should it output?

2. **Generate the skill file** with v2.1 format:
   - YAML frontmatter with name and description ("MUST use when..." format)
   - Activation message (pick an appropriate emoji)
   - Context guard (if the skill could have false positives)
   - Protocol steps
   - Inputs/Outputs
   - Example usage
   - Level history starting at Lv.1

3. **Write the file** to `C:\Projects\memstack\skills\{name}.md`

4. **Update MEMSTACK.md** — add a new row to the Skill Index table

5. **Confirm creation** — show the skill summary

### Improving an existing skill:

1. **Read the current skill file**
2. **Apply improvements** based on user feedback
3. **Increment the level** in Level History
4. **Update the file**

## Inputs
- Skill concept description, trigger keywords, desired behavior

## Outputs
- New skill .md file in skills/
- Updated MEMSTACK.md index

## Example Usage

**User:** "forge a new skill called Beacon for health check pinging"

```
🔨 Forge — Creating new enchantment...

Creating: Beacon
Emoji: 🔔 | Type: Passive | Triggers: "health check", "ping", "uptime"

Writing: skills/beacon.md ✓
Updating: MEMSTACK.md — added row #N ✓

Beacon is ready. Triggers: "health check", "ping", "uptime"
```

## Level History

- **Lv.1** — Base: Skill file generation and index updates. (Origin: MemStack v1.0, Feb 2026)
- **Lv.2** — Enhanced: Added YAML frontmatter, v2.1 format generation, level tracking. (Origin: MemStack v2.0 MemoryCore merge, Feb 2026)
