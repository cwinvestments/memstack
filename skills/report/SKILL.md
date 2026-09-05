---
name: report
description: 'Writes the session final report to a file when a prompt asks for it, then prints only the path and a one-line summary. Fires when the prompt contains "Report per memstack:report". Dormant otherwise.'
version: 1.0.0
---

# Report: Writing the Session Report
*The session states what it did, in a file, once, at the end.*

## Activation

Output `Report: writing the session report...`, then follow the rules below.

## Context Guard

| Context | Status | Priority |
|---------|--------|----------|
| **The prompt contains "Report per memstack:report"** | ACTIVE, write the file before finishing | P1 |
| **The prompt asks for a summary, a recap or a status line** | DORMANT, answer in the terminal, no file | n/a |
| **A long session ends and nobody asked for a report** | DORMANT, an unrequested file is litter | n/a |
| **The prompt asks for a diary or a handoff** | DORMANT, that is Diary and Project, not this | n/a |

The phrase is the whole trigger, and it is a phrase rather than a keyword
because "report" appears in ordinary prose constantly.

## Rules

### 1. Where it goes

`MEMSTACK_REPORT_DIR` when that variable is set and not empty, otherwise
`~/.memstack/reports`. Create the directory if it is absent.

A report is a session artifact, not a project file. Writing it into the working
tree puts it in front of `git status`, and then in front of `git add`, and a
report is not something anyone meant to commit.

### 2. What it is called

`<project>-<YYYY-MM-DD>-<HHMMSS>.txt`

- `<project>` is the leaf folder name of the working directory. Not the repo
  name, not the remote name: the folder, so two checkouts of one repo do not
  overwrite each other.
- `<YYYY-MM-DD>` is today, local time.
- `<HHMMSS>` is the local wall clock time at the moment of writing: six
  digits, 24 hour, zero padded. Read the clock when the file is about to be
  written, not when the work started.

The suffix is a clock reading rather than a sequence number because a sequence
has to be derived from what is already filed, and that derivation is what kept
failing. Reports move into a subfolder once they are reviewed, the directory
the count was taken from empties out, and the next report restarts at `01` on
top of a name that is still in use one folder down. A clock has no state to
lose.

### 3. How it is written

The **Write tool only**. Never a heredoc, never `echo`, never a shell
redirection into a path.

On Windows the redirection operator is recognised before quote pairing is
resolved, so one mis-paired quote anywhere in the command turns a redirect into
a zero-byte file named after the fragment that followed it. This repository has
collected four such files across three sessions, one of them from an arrow
inside ordinary prose in a command that ran no code at all. The Write tool
never touches a shell, so the hazard is not managed, it is absent.

### 4. What it may contain

- Plain ASCII. No em dashes, no smart quotes, no box drawing.
- No secret values. Not a key, not a token, not a password, not a signed URL,
  not the first six characters of any of them. A fingerprint (`sha256`, first
  8 characters) or a length answers "is it set" and "are these the same"
  without emitting the value.

The no-secrets rule applies to the file exactly as it applies to the terminal,
and the file is the more dangerous of the two: the terminal scrolls away, while
the file sits on disk and gets read later, or pasted into a ticket.

### 5. How it ends

The last line states the session approximate context usage as shown on the
status line, for example:

`Context: approximately 62 percent of the window used at the time of writing.`

A reader deciding whether to continue in this session or start a fresh one
cannot see the status line the report was written from. One line tells them how
much room is left.

### 6. What reaches the terminal

The file path, and one line saying what the report covers. Nothing else.

The body has already been written down. Printing it a second time doubles the
cost of the session final turn and buries the path the reader actually needs.

## Enforcement

A UserPromptSubmit hook records the request in `.memstack/report-required.json`
at the repository root, holding the session id, the request time, and the
expected file name prefix. The Stop gate in `scripts/verify.py` reads that
marker and blocks with exit 2 until a file carrying the prefix exists with an
mtime after the request. The gate deletes the marker once it finds the report,
and does nothing at all without one, so a session that was never asked for a
report is never gated for one.

## Known Gotchas

| Gotcha | Why it matters |
|--------|----------------|
| The suffix is a time, not a sequence number | Two sessions in one project on one day cannot collide on a second, and nothing has to be counted. The sequence was the actual failure: reviewed reports are filed into a subfolder, the live directory empties, and the count restarts at `01` over a name that already exists one level down. |
| A report is the session own claim about itself | It is testimony, not evidence. It never substitutes for a verify receipt: the receipt records what the check chain reported, the report records what the session says it did, and only one of those was produced by something other than the author. |
| The marker is keyed on the session id | A marker left by another session does not block this one, and a resumed session that receives a replayed hook still matches its own id. |
| A report that only lists what passed is half a report | State what was skipped, what is pending, and what could not be verified. The reader is deciding what to do next, and a report that reads clean when it is not costs them the next session. |

## Inputs and Outputs

- **In:** the prompt carrying the phrase, the working directory (for the
  project name), and `MEMSTACK_REPORT_DIR` when it is set.
- **Out:** one file at `<report dir>/<project>-<YYYY-MM-DD>-<HHMMSS>.txt`, plus one
  path and one summary line in the terminal.

## Level History

- **Lv.1** Base: File-backed session reports with a UserPromptSubmit marker and a Stop gate that blocks until the file exists. (Origin: MemStack, Sep 2026)
