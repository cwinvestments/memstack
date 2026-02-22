# Echo — Memory Recall Rule

When the user references past sessions, asks "what did we do", "do you remember", "last session", "recall", or "continue from" — search SQLite memory first.

## Protocol
1. Run: `python C:/Projects/memstack/db/memstack-db.py search "<keywords>"` (add `--project <name>` if project is known)
2. Run: `python C:/Projects/memstack/db/memstack-db.py get-sessions <project> --limit 5` for recent sessions
3. Run: `python C:/Projects/memstack/db/memstack-db.py get-insights <project>` for decisions and patterns
4. Present findings with dates, accomplishments, and pending items
5. If SQLite returns nothing, check `C:\Projects\memstack\memory\sessions\` as fallback

## Ownership
- "recall" / "remember" / "what did we do" = Echo (not Diary, not Project)
- "save" / "log" = Diary territory — do not activate Echo for saving
