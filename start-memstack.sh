#!/usr/bin/env bash
# ============================================================
#  MemStack v3.2 - Session Launcher (Mac/Linux)
#
#  First time: chmod +x start-memstack.sh
#  Then run:   ./start-memstack.sh
# ============================================================

echo ""
echo "  MemStack v3.2 - Starting session..."
echo "  ========================================="
echo ""

# 1. Check if Headroom is already running
echo "  [1/4] Checking Headroom proxy on port 8787..."
if curl -s -o /dev/null -w "" http://127.0.0.1:8787/health 2>/dev/null; then
    echo ""
    echo "  Headroom: ALREADY RUNNING"
else
    # 2. Start Headroom proxy in background
    echo "         Starting Headroom proxy..."
    nohup headroom proxy --port 8787 > /dev/null 2>&1 &

    # 3. Wait for initialization
    echo "  [2/4] Waiting for Headroom to initialize..."
    sleep 2

    # 4. Health check
    echo "  [3/4] Checking Headroom health..."
    if curl -s -o /dev/null -w "" http://127.0.0.1:8787/health 2>/dev/null; then
        echo ""
        echo "  Headroom: RUNNING"
    else
        echo ""
        echo "  Headroom: FAILED - proxy may not be installed"
        echo "  Install with: pip install headroom-ai"
    fi
fi

# 4. Open VS Code
echo ""
echo "  [4/4] Opening VS Code..."
code "$HOME/Projects"

echo ""
echo "  ========================================="
echo "  MemStack v3.2 ready - 16 public skills"
echo "  ========================================="
echo ""
