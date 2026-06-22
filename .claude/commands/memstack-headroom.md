Check TokenStack proxy status.

First check if the TokenStack proxy is running:

```bash
curl -s -m 2 http://127.0.0.1:8787/health
```

If it responds, the proxy is up and routing Claude Code traffic.

The proxy does not expose a stats endpoint. Report token savings from the dashboard instead:

- Proxy indicator: PRO or FREE badge with session and 30-day percentages
- Overview header: session and lifetime tokens saved
- Burn Report: per-transform breakdown, estimated cost, and per-agent split

If the proxy is not running, respond with:

"TokenStack is offline. Start it with: python -m memstack_skill_loader dashboard --with-proxy"
