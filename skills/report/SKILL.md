---
name: report
description: 'Writes the session final report to a file, then prints only the path and a one-line summary. Fires when the prompt contains "Report per memstack:report", and also when the prompt begins with a standing trigger configured through MEMSTACK_REPORT_ON_TASK_PROMPTS or MEMSTACK_REPORT_TRIGGERS. Dormant otherwise.'
version: 1.1.0
---

# Report: Writing the Session Report
*The session states what it did, in a file, once, at the end.*

## Activation

Output `Report: writing the session report...`, then follow the rules below.

## Context Guard

| Context | Status | Priority |
|---------|--------|----------|
| **The prompt contains "Report per memstack:report"** | ACTIVE, write the file before finishing | P1 |
| **The prompt's first non-blank line starts with a configured trigger** | ACTIVE, same requirement | P1 |
| **The prompt matched a prefix trigger, but is under 40 characters** | DORMANT, see the floor below | n/a |
| **The prompt asks for a summary, a recap or a status line** | DORMANT, answer in the terminal, no file | n/a |
| **A long session ends and nobody asked for a report** | DORMANT, an unrequested file is litter | n/a |
| **The prompt asks for a diary or a handoff** | DORMANT, that is Diary and Project, not this | n/a |

## Triggers

The phrase always arms, on every install, with nothing configured. It is a
phrase rather than a keyword because "report" appears in ordinary prose
constantly.

Two environment variables add standing triggers on top of it. Both are unset by
default, so a shipped install arms on the phrase and on nothing else.

| Variable | Effect |
|----------|--------|
| `MEMSTACK_REPORT_ON_TASK_PROMPTS` | Set to `1`, arms any prompt whose first non-blank line starts with `Working directory:`. Any other value, including `0`, changes nothing. |
| `MEMSTACK_REPORT_TRIGGERS` | Extra prefixes, semicolon separated, each matched against the first non-blank line. Surrounding spaces are trimmed, so `Task briefing:; Ticket:` configures two. |

`Working directory:` is separated out rather than left to the general list
because it is the opening line of a dispatched task prompt, which is the shape
this was built for, and because arming on it by default would file a report for
a large share of every prompt anyone writes.

When either variable is configured, the SessionStart hook injects one sentence
saying so. That sentence is the only announcement: a prompt carrying the phrase
announces the requirement itself, so a default install is told nothing and pays
nothing.

### The 40 character floor

**A prompt under 40 characters does not arm a prefix trigger.** A standing
prefix fires on "yes" and "commit" as readily as on a task, and a report about
"commit" is noise filed under a real project name.

**The floor applies to prefix triggers only. The phrase is exempt and arms at
any length.** A prompt consisting of nothing but `Report per memstack:report` is
26 characters and arms, because somebody typed the phrase on purpose and a short
request is still a request. No one-word answer can contain the phrase, so the
case the floor exists to stop is not a case the phrase can reach.

### Re-arming

A later prompt that matches overwrites the marker, so each task prompt in a
session owes its own report. The new marker carries a later request time than
the file the previous prompt produced, so an earlier report cannot satisfy a
later request.

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
  overwrite each other. When the prompt's first non-blank line names a working
  directory, that path's leaf is the project, not the directory the session was
  launched from. The gate reads the same line and keys the marker the same way,
  so a session opened in one repo and pointed at another agrees with itself.
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
at the repository root, holding the session id, the request time, the expected
file name prefix, which trigger matched, and the prompt's first 80 characters
with whitespace collapsed. The last of those is what lets the block message name
the prompt that is waiting, which matters once a session can hold more than one
request. The Stop gate in `scripts/verify.py` reads that
marker and blocks with exit 2 until a file carrying the prefix exists with an
mtime after the request, in that directory or one level below it. The gate
records that file's path in the marker once it finds one, so a later Stop is
answered from the record rather than from another scan, and it does nothing at
all without a marker, so a session that was never asked for a report is never
gated for one.

## Known Gotchas

| Gotcha | Why it matters |
|--------|----------------|
| The suffix is a time, not a sequence number | Two sessions in one project on one day cannot collide on a second, and nothing has to be counted. What the filing convention breaks is no longer the name but the gate: a report is moved into a reviewed subfolder while the session is still open, the gate found an empty top level, blocked, and the session wrote a second copy of a report that had never gone missing. The gate now records the accepted file's path in the marker and scans one level of subfolders when that recorded path is gone, and its block message says which of the two happened. |
| A report is the session own claim about itself | It is testimony, not evidence. It never substitutes for a verify receipt: the receipt records what the check chain reported, the report records what the session says it did, and only one of those was produced by something other than the author. |
| The marker is keyed on the session id | A marker left by another session does not block this one, and a resumed session that receives a replayed hook still matches its own id. |
| The prefix follows the prompt, not the launch directory | This is a fixed defect, not a design note. The marker used to key on the directory the session was launched from while the file was named for the directory the prompt pointed at, so a correctly named report was rejected and a second file appeared under the other name. One request, two files. |
| A standing trigger is a per-machine decision | Nothing ships armed beyond the phrase. A prefix arms every prompt that will ever start that way, including the ones written months after whoever set the variable stopped thinking about it, which is why it is opt in and why the floor exists. |
| A report that only lists what passed is half a report | State what was skipped, what is pending, and what could not be verified. The reader is deciding what to do next, and a report that reads clean when it is not costs them the next session. |

## Inputs and Outputs

- **In:** the prompt carrying the phrase or a configured trigger, the working
  directory the prompt names or the session was launched from (for the project
  name), `MEMSTACK_REPORT_DIR` when it is set, and
  `MEMSTACK_REPORT_ON_TASK_PROMPTS` and `MEMSTACK_REPORT_TRIGGERS` when the
  standing triggers are wanted.
- **Out:** one file at `<report dir>/<project>-<YYYY-MM-DD>-<HHMMSS>.txt`, plus one
  path and one summary line in the terminal.

## Level History

- **Lv.1** Base: File-backed session reports with a UserPromptSubmit marker and a Stop gate that blocks until the file exists. (Origin: MemStack, Sep 2026)
- **Lv.2** Standing triggers: opt-in prefix triggers behind two environment variables, a 40 character floor on those prefixes only, re-arming per prompt, a named prompt in the block message, and the project name keyed on the working directory the prompt names. (MemStack, Sep 2026)
