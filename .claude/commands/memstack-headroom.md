Check Headroom proxy status and token savings.

First check if Headroom is running:

```bash
curl -s -m 2 http://127.0.0.1:8787/health
```

If running, show detailed stats:

```bash
curl -s http://127.0.0.1:8787/stats | python -m json.tool
```

Present the results showing:
- Token savings (input/output)
- Compression ratio
- Estimated cost savings
- Uptime

If Headroom is not running, respond with:
"Headroom is offline. To install and start: `pip install headroom-ai && headroom proxy`"
