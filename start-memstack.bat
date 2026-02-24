@echo off
REM ============================================================
REM  MemStack v3.2 - Session Launcher
REM
REM  Shortcut: Right-click this file, Send to, Desktop
REM            (create shortcut). Then double-click to launch.
REM ============================================================

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
start /min "Headroom Proxy" cmd /c "headroom proxy --port 8787"

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
    echo  Install with: pip install headroom-ai
)

:headroom_done

REM 4. Open VS Code
echo.
echo  [4/4] Opening VS Code...
code C:\Projects

echo.
echo  =========================================
echo  MemStack v3.2 ready - 16 public skills
echo  =========================================
echo.

pause
