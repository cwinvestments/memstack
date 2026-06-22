#!/usr/bin/env bash
# ============================================================
#  MemStack - Session Launcher (Mac/Linux)
#
#  First time: chmod +x start-memstack.sh
#  Then run:   ./start-memstack.sh
# ============================================================

MEMSTACK_DIR="$(cd "$(dirname "$0")" && pwd)"

echo ""
echo "  MemStack - Starting session..."
echo "  ========================================="
echo ""

# 1. Check if the TokenStack proxy is already running
echo "  [1/3] Checking TokenStack proxy on port 8787..."
if curl -s -o /dev/null -w "" http://127.0.0.1:8787/health 2>/dev/null; then
    echo ""
    echo "  TokenStack: ALREADY RUNNING (skipping start)"
else
    # 2. Start the dashboard with the TokenStack proxy in the background
    echo "  [2/3] Starting TokenStack (dashboard --with-proxy)..."
    nohup python -m memstack_skill_loader dashboard --with-proxy > /dev/null 2>&1 &

    sleep 2
    if curl -s -o /dev/null -w "" http://127.0.0.1:8787/health 2>/dev/null; then
        echo ""
        echo "  TokenStack: RUNNING"
    else
        echo ""
        echo "  TokenStack: not detected yet (it may still be starting)"
    fi
fi

# 3. Open VS Code
echo ""
echo "  [3/3] Opening VS Code..."
code "$MEMSTACK_DIR"

echo ""
echo "  ========================================="
echo "  MemStack ready"
echo "  ========================================="
echo ""
