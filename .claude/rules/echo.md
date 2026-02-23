# Echo — Memory Recall Rule

When the user references past sessions, asks "what did we do", "do you remember", "last session", "recall", or "continue from" — search memory using semantic vector search first, then SQLite.

## Protocol
1. Run: `python C:/Projects/memstack/skills/echo/search.py "<keywords>" --top-k 5` for semantic vector search
2. Run: `python C:/Projects/memstack/db/memstack-db.py search "<keywords>"` (add `--project <name>` if project is known)
3. Run: `python C:/Projects/memstack/db/memstack-db.py get-sessions <project> --limit 5` for recent sessions
4. Run: `python C:/Projects/memstack/db/memstack-db.py get-insights <project>` for decisions and patterns
5. Present findings with similarity scores, dates, accomplishments, and pending items
6. If vector search fails (not installed, no DB), SQLite results are sufficient
7. If all sources return nothing, check `C:\Projects\memstack\memory\sessions\` as fallback

## Ownership
- "recall" / "remember" / "what did we do" = Echo (not Diary, not Project)
- "save" / "log" = Diary territory — do not activate Echo for saving
