@echo off
REM ============================================================
REM  MemStack v3.2 - Session Launcher
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
echo  MemStack v3.2 - Starting session...
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

REM 4. Open VS Code
echo.
echo  [4/4] Opening VS Code...
code "%MEMSTACK_DIR%"

echo.
echo  =========================================
echo  MemStack v3.2 ready - 17 public skills
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
        echo.
        echo  SKIP: %TARGET%\.claude is already a junction.
        echo.
        goto :eof
    )
    echo.
    echo  WARNING: %TARGET%\.claude exists as a real folder.
    echo  Removing it and replacing with junction...
    rmdir /s /q "%TARGET%\.claude"
)

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
