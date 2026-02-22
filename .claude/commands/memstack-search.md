Search MemStack memory for past sessions, insights, and project context.

Run the following search and present results in a readable format:

```bash
python C:/Projects/memstack/db/memstack-db.py search "$ARGUMENTS"
```

If the query mentions a specific project name, also run:

```bash
python C:/Projects/memstack/db/memstack-db.py get-sessions <project> --limit 3
python C:/Projects/memstack/db/memstack-db.py get-insights <project>
```

Present results grouped by type:
- **Sessions**: Date, project, what was accomplished
- **Insights**: Decisions and patterns discovered
- **Context**: Current project state

If no results found, say: "No matches for '$ARGUMENTS'. Try broader keywords or check `python C:/Projects/memstack/db/memstack-db.py stats` for available data."
