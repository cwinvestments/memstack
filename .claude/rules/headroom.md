# Headroom — Context Compression Proxy

Headroom proxy at localhost:8787 compresses CC tool outputs by ~34%, extending effective context window. Auto-started by the session-start hook if installed.

## Troubleshooting
- If you see connection errors to the Anthropic API, Headroom proxy may have crashed. Check: `curl http://127.0.0.1:8787/health`
- To check token savings: `curl http://127.0.0.1:8787/stats`
- To restart manually: `headroom proxy --port 8787 &`
- If Headroom is not installed, CC works normally — the proxy is optional
