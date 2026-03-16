---
name: sight
description: "Use when the user says 'draw', 'diagram', 'visualize', 'architecture', or needs a visual overview of code structure."
---


# 👁️ Sight — The Hidden Becomes Clear
*Generate Mermaid diagrams showing project architecture, schema, and data flow.*

## Activation

When this skill activates, output:

`👁️ Sight — The hidden becomes clear.`

Then execute the protocol below.

## Context Guard

| Context | Status |
|---------|--------|
| **User asks for a diagram or visualization** | ACTIVE — generate diagram |
| **User says "draw", "diagram", "architecture"** | ACTIVE — generate diagram |
| **User asks to "show" or "map" the structure** | ACTIVE — generate diagram |
| **Discussing diagrams conceptually** | DORMANT — do not activate |
| **User is looking at existing diagrams** | DORMANT — do not activate |

## Protocol

1. **Determine diagram type** from context:
   - "database" / "schema" → `erDiagram`
   - "api" / "endpoints" → `flowchart TD`
   - "components" / "pages" → `graph TD`
   - "architecture" / "structure" → `flowchart TD` (system overview)
   - "flow" / "process" → `sequenceDiagram`

2. **Scan the relevant code:**
   - For DB: read migration files in `database/`
   - For API: list files in `src/app/api/`
   - For pages: list files in `src/app/`
   - For architecture: read package.json, directory structure, configs

3. **Generate Mermaid diagram** as a code block

4. **Optionally save** to `docs/diagrams/{name}.mermaid`

## Inputs
- What to visualize (database, API, components, architecture)
- Project directory

## Outputs
- Mermaid diagram code block ready to render
- Optional saved .mermaid file

## Example Usage

**User:** "draw the AdminStack database schema"

```
👁️ Sight — The hidden becomes clear.

​```mermaid
erDiagram
    accounts ||--o{ organizations : "has"
    accounts ||--o{ cc_sessions : "tracks"
    organizations ||--o{ projects : "contains"
    organizations ||--o{ contacts : "stores"
    organizations ||--o{ orders : "processes"

    accounts {
        uuid id PK
        text email
        boolean is_platform_admin
    }
    cc_sessions {
        uuid id PK
        text name
        text status
    }
​```
```

## Level History

- **Lv.1** — Base: Mermaid diagram generation from codebase analysis. (Origin: MemStack v1.0, Feb 2026)
- **Lv.2** — Enhanced: Added YAML frontmatter, context guard, activation message, diagram type detection. (Origin: MemStack v2.0 MemoryCore merge, Feb 2026)

> 💎 Pro: PostToolUse hook auto-logs this work to your observation history.
