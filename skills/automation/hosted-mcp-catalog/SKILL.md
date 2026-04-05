---
name: memstack-automation-hosted-mcp-catalog
description: "Use when the user says 'what MCP servers', 'find an MCP for', 'hosted MCP', 'list MCP servers', 'MCP catalog', 'available MCP tools', or needs to discover zero-setup hosted MCP servers they can use immediately. Do NOT use for building MCP servers or configuring local MCP."
version: 1.0.0
---

# Hosted MCP Catalog — Finding hosted MCP servers...
*Reference guide for zero-setup hosted MCP servers that require no API keys, no local install — just point any MCP client at the URL.*

## Activation

| Trigger | Status |
|---------|--------|
| User says "what MCP servers" or "find an MCP for" | ACTIVE |
| User says "hosted MCP" or "MCP catalog" | ACTIVE |
| User says "available MCP tools" or "list MCP servers" | ACTIVE |
| User wants to BUILD an MCP server | NOT this skill — use mcp-builder |
| User wants to configure local MCP | NOT this skill — check .mcp.json docs |

## Context Guard

- Do NOT use for building MCP servers (that's mcp-builder Pro skill)
- Do NOT use for local MCP server configuration
- Do NOT use for debugging MCP connection issues
- This skill ONLY helps discover and connect to hosted MCP endpoints

## How Hosted MCP Works

Hosted MCP servers run remotely — no local install needed. Add the URL to your MCP client config and the tools are available immediately.

**In Claude Code** — add to `.mcp.json`:
```json
{
  "mcpServers": {
    "server-name": {
      "type": "url",
      "url": "https://example.com/mcp"
    }
  }
}
```

**In Claude Desktop** — add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "server-name": {
      "url": "https://example.com/mcp"
    }
  }
}
```

## Catalog: Official Platform MCP Servers

These are maintained by major platforms and generally stable:

| Server | URL | Tools | Use Case |
|--------|-----|-------|----------|
| Vercel | `https://mcp.vercel.com` | Deploy, logs, env vars, projects | Vercel deployment management |
| Supabase | `https://mcp.supabase.com/mcp` | DB queries, migrations, RLS | Database management |
| Sentry | `https://mcp.sentry.dev/mcp` | Issues, errors, performance | Error tracking |
| Stripe | `https://mcp.stripe.com` | Payments, customers, invoices | Payment processing |
| Linear | `https://mcp.linear.app/mcp` | Issues, projects, cycles | Project management |
| Slack | `https://mcp.slack.com/mcp` | Messages, channels, search | Team communication |
| Greptile | `https://api.greptile.com/mcp` | Codebase search, understanding | Code intelligence |

**Note:** Most official servers require OAuth authentication on first use. Claude Code handles this automatically — you'll get a browser prompt to authorize.

## How to Choose

When the user needs an MCP server, help them find the right one:

### Step 1: Identify the need

| User wants to... | Recommended MCP |
|-------------------|-----------------|
| Query a database | Supabase |
| Track errors/bugs | Sentry |
| Deploy code | Vercel |
| Process payments | Stripe |
| Manage issues/tickets | Linear |
| Send team messages | Slack |
| Search codebases | Greptile |

### Step 2: Add to config

Generate the `.mcp.json` entry for the chosen server:

```json
{
  "mcpServers": {
    "<server-name>": {
      "type": "url",
      "url": "<server-url>"
    }
  }
}
```

### Step 3: Test the connection

After adding, restart Claude Code and verify:
1. The server appears in the MCP tools list
2. Authentication completes (if required)
3. A simple tool call succeeds

## Discovery Resources

When the catalog above doesn't cover the user's need:

| Resource | URL | Description |
|----------|-----|-------------|
| Anthropic MCP Registry | https://github.com/modelcontextprotocol/servers | Official MCP server list |
| Smithery | https://smithery.ai | MCP server marketplace |
| MCP.so | https://mcp.so | Community MCP directory |
| Glama | https://glama.ai/mcp/servers | Curated MCP catalog |

## Output Template

```
MCP Server: [name]
URL: [endpoint]
Auth: [OAuth / API key / None]
Tools available: [list of key tools]
Config to add to .mcp.json:

{
  "mcpServers": {
    "[name]": {
      "type": "url",
      "url": "[endpoint]"
    }
  }
}

Restart Claude Code after adding.
```

## Disambiguation

- "what MCP servers" / "find an MCP for" / "hosted MCP" = Hosted MCP Catalog
- "build an MCP server" / "create MCP tools" = mcp-builder (not this skill)
- "MCP not connecting" / "MCP error" = Debug directly (not this skill)
- "what tools do I have" = Check current MCP config (not this skill)

## Level History

- **Lv.1** — Base: Hosted MCP server catalog with official platform endpoints, connection setup, discovery resources. (Origin: MemStack v3.5, Apr 2026)
