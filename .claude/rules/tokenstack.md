# TokenStack - Context Compression Proxy

TokenStack is the built-in compression proxy at `127.0.0.1:8787`. It compresses Claude Code tool output before it reaches the Anthropic API, extending effective context and lowering token cost. It ships inside the `memstack-skill-loader` package, so there is no separate install.

## Starting it

Start the dashboard with the proxy enabled (this also sets `ANTHROPIC_BASE_URL` automatically):

```cmd
python -m memstack_skill_loader dashboard --with-proxy
```

To run only the proxy without the dashboard:

```cmd
python -m memstack_skill_loader proxy
```

## Troubleshooting

- Health check: `curl http://127.0.0.1:8787/health`
- The proxy has no `/stats` endpoint. Read savings in the dashboard (Overview header and Burn Report).
- If CC shows connection errors to the Anthropic API, the proxy may have stopped. Restart it with the dashboard command above.
- TokenStack is optional. If it is not running, Claude Code works normally without compression.

## Tiers

- Free tier: six lossless text transforms, always on.
- Pro tier: adds seven transforms including AST truncation; activated by a valid Pro license.
