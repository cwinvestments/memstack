#!/usr/bin/env bash
# ============================================================
#  MemStack v3.2 - Session Launcher (Mac/Linux)
#
#  First time: chmod +x start-memstack.sh
#  Then run:   ./start-memstack.sh
# ============================================================

MEMSTACK_DIR="$(cd "$(dirname "$0")" && pwd)"

echo ""
echo "  MemStack v3.2 - Starting session..."
echo "  ========================================="
echo ""

# 1. Check if Headroom is already running
echo "  [1/4] Checking Headroom proxy on port 8787..."
if curl -s -o /dev/null -w "" http://127.0.0.1:8787/health 2>/dev/null; then
    echo ""
    echo "  Headroom: ALREADY RUNNING (skipping steps 2-3)"
else
    # 2. Start Headroom proxy in background
    echo "  [2/4] Starting Headroom proxy..."
    nohup headroom proxy --port 8787 --llmlingua-device cpu > /dev/null 2>&1 &

    # 3. Wait and health check
    echo "  [3/4] Waiting for Headroom to initialize..."
    sleep 2

    if curl -s -o /dev/null -w "" http://127.0.0.1:8787/health 2>/dev/null; then
        echo ""
        echo "  Headroom: RUNNING"
    else
        echo ""
        echo "  Headroom: FAILED - proxy may not be installed"
        echo "  Install with: pip install headroom-ai[code]"
    fi
fi

# 4. Open VS Code
echo ""
echo "  [4/4] Opening VS Code..."
code "$MEMSTACK_DIR"

echo ""
echo "  ========================================="
echo "  MemStack v3.2 ready - 16 public skills"
echo "  ========================================="
echo ""
