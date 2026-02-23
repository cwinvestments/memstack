---
name: shard
description: "Large file refactoring. Splits files over 1000 lines into clean modules. Triggers on shard this, split file, or files over 1K lines."
---


# 💎 Shard — Refactoring Large File...
*Split monolithic files into focused, maintainable modules.*

## Activation

When this skill activates, output:

`💎 Shard — Refactoring large file...`

Then execute the protocol below.

## Context Guard

| Context | Status |
|---------|--------|
| **User says "shard", "split file", or "refactor"** | ACTIVE — full protocol |
| **Editing a file over 1000 lines** | ACTIVE — suggest refactor |
| **User says "refactor" for logic changes (not splitting)** | DORMANT — not a shard task |
| **Discussing code organization concepts** | DORMANT — do not activate |
| **File is under 500 lines** | DORMANT — not worth splitting |

## Protocol

1. **Identify the target file** and count lines:
   ```bash
   wc -l <file>
   ```

2. **Analyze structure:**
   - List all exports (functions, components, types, constants)
   - Identify logical groupings
   - Map internal dependencies (what calls what)

3. **Propose the split** — present to user BEFORE executing:
   - Target: 100-300 lines per new file
   - Group related functionality
   - Keep types near consumers
   - Shared utilities in separate file

4. **Execute the refactor:**
   - Create new files with proper names
   - Move code to appropriate files
   - Add import/export statements
   - Create index.ts barrel if needed for backwards compatibility
   - Update all imports throughout the project

5. **Verify build:**
   ```bash
   npm run build 2>&1 | tail -20
   ```

6. **Present result** — new file structure with line counts

## Inputs
- File path to refactor
- Optional: preferred split strategy or target file count

## Outputs
- Multiple smaller files replacing the original
- Updated imports throughout project
- Build verification

## Example Usage

**User:** "shard infrastructure/page.tsx — it's 1100 lines"

```
💎 Shard — Refactoring large file...

infrastructure/page.tsx (1,110 lines) → 6 files:
  page.tsx         (~120 lines) — Main page, tab switcher
  RailwayTab.tsx   (~200 lines) — Railway monitoring
  HetznerTab.tsx   (~180 lines) — Hetzner monitoring
  HeadroomTab.tsx  (~250 lines) — Headroom + setup guide
  types.ts         (~80 lines)  — Shared interfaces
  constants.ts     (~60 lines)  — Status configs

Build check: ✓ passed
```

## Level History

- **Lv.1** — Base: File analysis and splitting with import updates. (Origin: MemStack v1.0, Feb 2026)
- **Lv.2** — Enhanced: Added YAML frontmatter, context guard, propose-before-execute, activation message. (Origin: MemStack v2.0 MemoryCore merge, Feb 2026)
