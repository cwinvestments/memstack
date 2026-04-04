@echo off
REM ============================================================
REM  MemStack v3.3.4 - Session Launcher
REM
REM  Usage: start-memstack.bat              (launch session)
REM         start-memstack.bat link <path>  (link project)
REM
REM  Shortcut: Right-click this file, Send to, Desktop
REM            (create shortcut). Then double-click to launch.
REM ============================================================

REM --- Dynamic path detection ---
set "MEMSTACK_DIR=%~dp0"
if "%MEMSTACK_DIR:~-1%"=="\" set "MEMSTACK_DIR=%MEMSTACK_DIR:~0,-1%"

REM --- Subcommand routing ---
if /i "%~1"=="link" goto link_project

title MemStack Launcher

echo.
echo  MemStack v3.2.1 - Starting session...
echo  =========================================
echo.

REM 1. Check if Headroom is already running
echo  [1/4] Checking Headroom proxy on port 8787...
curl -s -o nul -w "" http://127.0.0.1:8787/health >nul 2>&1
if %errorlevel% equ 0 (
    echo.
    echo  Headroom: ALREADY RUNNING
    goto headroom_done
)

REM 2. Start Headroom proxy in a minimized window
echo         Starting Headroom proxy...
start /min "Headroom Proxy" cmd /c "headroom proxy --port 8787 --llmlingua-device cpu"

REM 3. Wait for initialization
echo  [2/4] Waiting for Headroom to initialize...
timeout /t 2 /nobreak >nul

REM 4. Health check
echo  [3/4] Checking Headroom health...
curl -s -o nul -w "" http://127.0.0.1:8787/health >nul 2>&1
if %errorlevel% equ 0 (
    echo.
    echo  Headroom: RUNNING
) else (
    echo.
    echo  Headroom: FAILED - proxy may not be installed
    echo  Install with: pip install headroom-ai[code]
)

:headroom_done

REM 4. Count skills
set /a SKILL_COUNT=0
for /r "%MEMSTACK_DIR%\skills" %%f in (SKILL.md) do set /a SKILL_COUNT+=1

REM 5. Open VS Code (if available)
echo.
where code >nul 2>nul
if %errorlevel% neq 0 (
    echo  [5/5] VS Code not found, skipping...
) else (
    echo  [5/5] Opening VS Code...
    code "%MEMSTACK_DIR%"
)

echo.
echo  =========================================
echo  MemStack v3.3.4 ready - %SKILL_COUNT% skills
echo  =========================================
echo.

pause
goto :eof

REM ============================================================
REM  link <project-path> — Create .claude junction to MemStack
REM ============================================================
:link_project
set "TARGET=%~2"

if "%TARGET%"=="" (
    echo.
    echo  ERROR: No project path provided.
    echo  Usage: start-memstack.bat link C:\Projects\MyProject
    echo.
    goto :eof
)

if not exist "%TARGET%" (
    echo.
    echo  ERROR: Directory not found: %TARGET%
    echo.
    goto :eof
)

REM Check if .claude already exists
if exist "%TARGET%\.claude" (
    REM Check if it's already a junction (reparse point)
    dir "%TARGET%" /AL 2>nul | findstr /C:".claude" >nul 2>&1
    if %errorlevel% equ 0 (
        REM It's a junction — remove it so we can recreate with current path
        echo.
        echo  Updating existing junction...
        rmdir "%TARGET%\.claude"
        goto :create_junction
    )
    REM It's a real directory — merge MemStack rules into it without destroying user files
    echo.
    echo  MERGE: %TARGET%\.claude exists as a real folder.
    echo  Copying MemStack rules into existing .claude directory...
    if not exist "%TARGET%\.claude\rules" mkdir "%TARGET%\.claude\rules"
    if not exist "%TARGET%\.claude\hooks" mkdir "%TARGET%\.claude\hooks"
    xcopy "%MEMSTACK_DIR%\.claude\rules\*" "%TARGET%\.claude\rules\" /Y /Q >nul 2>&1
    xcopy "%MEMSTACK_DIR%\.claude\hooks\*" "%TARGET%\.claude\hooks\" /Y /Q >nul 2>&1
    echo.
    echo  SUCCESS: MemStack rules merged into %TARGET%\.claude
    echo  Note: Your existing settings, commands, and other files were preserved.
    echo.
    goto :eof
)

:create_junction
mklink /J "%TARGET%\.claude" "%MEMSTACK_DIR%\.claude"
if %errorlevel% equ 0 (
    echo.
    echo  SUCCESS: Linked %TARGET%\.claude
    echo       -^> %MEMSTACK_DIR%\.claude
    echo.
) else (
    echo.
    echo  ERROR: Failed to create junction.
    echo.
)
goto :eof
