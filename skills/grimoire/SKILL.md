---
name: grimoire
description: "Use when the user says 'update context', 'update claude', 'save library', or after significant project changes."
version: 1.0.0
---


# 📖 Grimoire — Updating the Knowledge Library
*Manage and update CLAUDE.md files across all projects.*

## Activation

When this skill activates, output:

`📖 Grimoire — Updating the knowledge library.`

Then execute the protocol below.

## Protocol

1. **Identify the target project** — use config.json to find the CLAUDE.md path
2. **Read the current CLAUDE.md** if it exists
3. **Determine what to update** based on the session's work:
   - New API endpoints built
   - New database tables/migrations
   - New pages or components added
   - Architecture decisions made
   - Environment variables added
   - Dependencies installed
4. **Update the CLAUDE.md:**
   - Keep existing content intact
   - Add new entries under the right headings
   - Don't duplicate existing entries
   - Use consistent formatting
5. **If no CLAUDE.md exists** — create one with standard sections:
   - Project Overview, Tech Stack, Directory Structure, Key Files
   - API Endpoints, Database Schema, Environment Variables, Dev Commands

## Inputs
- Project name (maps to config.json entry)
- What was built/changed this session

## Outputs
- Updated CLAUDE.md file
- Summary of what was added

## Example Usage

**User:** "update claude.md with the CC Monitor stuff"

```
📖 Grimoire — Updating the knowledge library.

Reading: C:\Projects\AdminStack\CLAUDE.md

Adding to API Endpoints:
  - POST/GET/PATCH/DELETE /api/cc-sessions
  - POST /api/cc-sessions/report

Adding to Database Schema:
  - cc_sessions (020_cc_sessions.sql)

Adding to Environment Variables:
  - CC_MONITOR_API_KEY

CLAUDE.md updated ✓
```

## Level History

- **Lv.1** — Base: CLAUDE.md read/write with section management. (Origin: MemStack v1.0, Feb 2026)
- **Lv.2** — Enhanced: Added YAML frontmatter, activation message, auto-detect what changed. (Origin: MemStack v2.0 MemoryCore merge, Feb 2026)
