# MemStack™ Skill Loader

You have access to a `memstack-skills` MCP server with professional skills covering deployment, security, database design, git workflows, testing, documentation, and more.

## ALWAYS call `find_skill` BEFORE:
- Any deployment task (Railway, Netlify, Vercel, Hetzner, etc.)
- Any database work (migrations, RLS, schema design)
- Any git operation beyond simple commits
- Any infrastructure or DevOps task
- Any task where the user asks "how should I..." or "what's the best way to..."
- Any task you're unsure about — check if a skill exists first

## ALWAYS call `list_skills` when:
- The user asks "what skills are available" or similar
- You want to browse what's available for a broad topic

## DO NOT call find_skill for:
- Reading or explaining existing code
- Simple file edits the user has explicitly described
- Answering questions about the current codebase
- Chat/conversation that doesn't involve a task

## Tool names:
- `find_skill` — semantic search by task description
- `list_skills` — browse full catalog
- `get_skill` — fetch specific skill by name
- `reindex_skills` — rebuild index after skill changes
