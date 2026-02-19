# Grimoire — MemStack Skill

## Trigger Keywords
- save library, load library, update context, update claude.md, update claude

## Purpose
Manage and update CLAUDE.md files across all projects. Keep project context current as features are built.

## Instructions

1. **Identify the target project** — use config.json to find the CLAUDE.md path
2. **Read the current CLAUDE.md** if it exists
3. **Determine what to update** based on the session's work:
   - New API endpoints built
   - New database tables/migrations
   - New pages or components added
   - Architecture decisions made
   - Environment variables added
   - Dependencies installed
4. **Update the CLAUDE.md** — add new information in the correct section:
   - Keep existing content intact
   - Add new entries under the right headings
   - Don't duplicate existing entries
   - Use consistent formatting with the rest of the file
5. **If no CLAUDE.md exists** — create one with standard sections:
   - Project Overview
   - Tech Stack
   - Directory Structure
   - Key Files
   - API Endpoints
   - Database Schema
   - Environment Variables
   - Development Commands

## Inputs
- Project name (maps to config.json entry)
- What was built/changed this session

## Outputs
- Updated CLAUDE.md file
- Summary of what was added

## Example Usage

**User prompt:** "update claude.md with the CC Monitor stuff we just built"

**Grimoire activates:**

```
Reading: C:\Projects\AdminStack\CLAUDE.md

Adding to API Endpoints section:
  - POST/GET/PATCH/DELETE /api/cc-sessions — CC session CRUD (admin)
  - POST /api/cc-sessions/report — Public reporter endpoint (API key auth)

Adding to Database Schema section:
  - cc_sessions — Claude Code session tracking (020_cc_sessions.sql)

Adding to Pages section:
  - /cc-monitor — Claude Code session monitoring dashboard

Adding to Environment Variables section:
  - CC_MONITOR_API_KEY — API key for cc-reporter script

CLAUDE.md updated successfully.
```
