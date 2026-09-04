: << 'CMDBLOCK'
@echo off
REM Cross-platform polyglot wrapper for hook scripts.
REM On Windows: cmd.exe runs the batch portion, which finds and calls bash.
REM On Unix: the shell interprets this as a script (: is a no-op in bash).
REM
REM Hook scripts use extensionless filenames (e.g. "session-start" not
REM "session-start.sh") so Claude Code's Windows auto-detection -- which
REM prepends "bash" to any command containing .sh -- doesn't interfere.
REM
REM Usage: run-hook.cmd <script-name> [args...]

if "%~1"=="" (
    echo run-hook.cmd: missing script name >&2
    exit /b 1
)

if /i "%~1"=="verify-gate" goto verify_gate
if /i "%~1"=="report-marker" goto report_marker

set "HOOK_DIR=%~dp0"

REM Try Git for Windows bash in standard locations
if exist "C:\Program Files\Git\bin\bash.exe" (
    "C:\Program Files\Git\bin\bash.exe" "%HOOK_DIR%%~1" %2 %3 %4 %5 %6 %7 %8 %9
    exit /b %ERRORLEVEL%
)
if exist "C:\Program Files (x86)\Git\bin\bash.exe" (
    "C:\Program Files (x86)\Git\bin\bash.exe" "%HOOK_DIR%%~1" %2 %3 %4 %5 %6 %7 %8 %9
    exit /b %ERRORLEVEL%
)

REM Try bash on PATH (e.g. user-installed Git Bash, MSYS2, Cygwin)
where bash >nul 2>nul
if %ERRORLEVEL% equ 0 (
    bash "%HOOK_DIR%%~1" %2 %3 %4 %5 %6 %7 %8 %9
    exit /b %ERRORLEVEL%
)

REM No bash found - exit silently rather than error
REM (plugin still works, just without SessionStart context injection)
exit /b 0

REM The Stop gate. Runs the verify CLI's gate subcommand with stdin
REM inherited, so the hook payload reaches it untouched. Anything this
REM branch itself cannot do exits 0: an absent python, a python that is
REM the Windows Store stub, a broken python or a missing verify.py must
REM never look like a block, because 2 is the only code that means
REM blocked and it belongs to verify.py alone.
REM The probe runs the interpreter instead of asking where it is. The
REM Store stub satisfies a path lookup and then exits 9009 without
REM running any code, so only executing something proves anything.
REM Both invocations go through call, because a python that is a .cmd
REM or .bat shim would otherwise take control and never hand it back:
REM the shim's own exit code would become this hook's, and the lines
REM below would never run.
:verify_gate
call python -c "import sys" >nul 2>nul
if errorlevel 1 exit /b 0
if not exist "%CLAUDE_PLUGIN_ROOT%\scripts\verify.py" exit /b 0
call python "%CLAUDE_PLUGIN_ROOT%\scripts\verify.py" gate
exit /b %ERRORLEVEL%

REM The report marker. Same probe as the gate above, and the same rule
REM that anything this branch cannot do exits 0. The difference is the
REM last line: this one discards verify.py's exit code instead of
REM forwarding it. UserPromptSubmit treats exit 2 as a block that ERASES
REM the user's prompt, so a bookkeeping hook must not be able to return
REM one, whatever goes wrong inside it.
:report_marker
call python -c "import sys" >nul 2>nul
if errorlevel 1 exit /b 0
if not exist "%CLAUDE_PLUGIN_ROOT%\scripts\verify.py" exit /b 0
call python "%CLAUDE_PLUGIN_ROOT%\scripts\verify.py" report-marker
exit /b 0
CMDBLOCK
# Everything from here to the re-exec below must be a comment.
# This file is stored with CRLF endings because the batch half above
# needs them: cmd.exe's goto label parsing is unreliable in a file
# with bare LF endings. bash cannot read CRLF, so the next line makes
# bash re-execute a CR-stripped copy of this file, exactly once. The
# MEMSTACK_CR_STRIPPED environment guard is what stops that from
# recursing: on the stripped re-run the variable is already set and
# the line becomes a no-op. $0 survives because it is passed as the
# first argument after the bash -c command string. The trailing #
# keeps this line's own CR out of the parser. On the stripped re-run
# the heredoc above is a no-op and the Unix half runs with LF.
[ -n "$MEMSTACK_CR_STRIPPED" ] || MEMSTACK_CR_STRIPPED=1 exec bash -c "$(tr -d '\r' < "$0")" "$0" "$@" #

# Unix: run the named script directly
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SCRIPT_NAME="$1"
shift

# The Stop gate, same contract as the batch branch above: stdin is
# inherited, and anything this branch itself cannot do exits 0 rather
# than looking like a block.
if [ "$SCRIPT_NAME" = "verify-gate" ]; then
    PY=""
    command -v python >/dev/null 2>&1 && PY="python"
    if [ -z "$PY" ]; then
        command -v python3 >/dev/null 2>&1 && PY="python3"
    fi
    [ -n "$PY" ] || exit 0
    [ -f "${CLAUDE_PLUGIN_ROOT}/scripts/verify.py" ] || exit 0
    exec "$PY" "${CLAUDE_PLUGIN_ROOT}/scripts/verify.py" gate
fi

# The report marker, same contract, with one difference: it is not exec'd
# and its exit code is discarded, because exit 2 on UserPromptSubmit
# erases the user's prompt.
if [ "$SCRIPT_NAME" = "report-marker" ]; then
    PY=""
    command -v python >/dev/null 2>&1 && PY="python"
    if [ -z "$PY" ]; then
        command -v python3 >/dev/null 2>&1 && PY="python3"
    fi
    [ -n "$PY" ] || exit 0
    [ -f "${CLAUDE_PLUGIN_ROOT}/scripts/verify.py" ] || exit 0
    "$PY" "${CLAUDE_PLUGIN_ROOT}/scripts/verify.py" report-marker
    exit 0
fi

exec bash "${SCRIPT_DIR}/${SCRIPT_NAME}" "$@"
