# Shard — MemStack Skill

## Trigger Keywords
- shard this, files over 1K lines, refactor, split file

## Purpose
Refactor large files (1000+ lines) into smaller, focused modules while maintaining all imports and exports.

## Instructions

1. **Identify the target file** and count its lines:
   ```bash
   wc -l <file>
   ```

2. **Analyze the file structure:**
   - List all exports (functions, components, types, constants)
   - Identify logical groupings (related functions, component + helpers, types + validators)
   - Map internal dependencies (what calls what within the file)

3. **Plan the split** — propose a split to the user before executing:
   - Target: each new file should be 100-300 lines
   - Group related functionality together
   - Keep types/interfaces near their consumers
   - Shared utilities go in a separate utils file

4. **Execute the refactor:**
   - Create new files with proper names
   - Move code into the appropriate files
   - Add import/export statements to each new file
   - Create an index.ts barrel file if needed for backwards compatibility
   - Update all imports throughout the project that reference the old file

5. **Verify nothing broke:**
   ```bash
   npm run build 2>&1 | tail -20
   ```

6. **Present the result** — show the new file structure with line counts

## Inputs
- File path to refactor
- Optional: preferred split strategy or target file count

## Outputs
- Multiple smaller files replacing the original
- Updated imports throughout the project
- Build verification

## Example Usage

**User prompt:** "shard src/app/(dashboard)/infrastructure/page.tsx — it's over 1100 lines"

**Shard activates:**

```
Analyzing: infrastructure/page.tsx (1,110 lines)

Exports found: 1 default export (InfrastructurePage)
Internal components: RailwayTab, HetznerTab, HeadroomTab
Types: 8 interfaces
Constants: 3 status config objects

Proposed split:
  infrastructure/
    page.tsx              (~120 lines) — Main page, tab switcher
    RailwayTab.tsx        (~200 lines) — Railway monitoring
    HetznerTab.tsx        (~180 lines) — Hetzner monitoring
    HeadroomTab.tsx       (~250 lines) — Headroom proxy + setup guide
    types.ts              (~80 lines)  — Shared interfaces
    constants.ts          (~60 lines)  — Status configs

Proceed? [User confirms]

Splitting... ✓
Updating imports... ✓
Build check... ✓ passed

6 files created, 0 build errors.
```
