---
name: token-optimization
description: "Use when the user says 'token optimization', 'save tokens', 'context window', 'reduce tokens', 'token stack', or 'TokenStack', or asks about extending context window capacity. Covers TokenStack, the built-in compression proxy that shrinks Claude Code tool output before it reaches the Anthropic API. Do NOT use for proxy troubleshooting or live status (Compress skill)."
version: 2.0.0
license: "Proprietary - MemStack Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# Token Optimization Guide - TokenStack

*One built-in compression proxy that shrinks Claude Code tool output before it reaches the Anthropic API.*

## Activation

When this skill activates, output:

`TokenStack - enabling compression & reading your savings...`

Then execute the protocol below.

## Context Guard

| Context | Status |
|---------|--------|
| **User asks about token savings or context optimization** | ACTIVE - full guide |
| **User says "TokenStack", "token stack", "reduce tokens"** | ACTIVE - relevant section |
| **User wants to enable or confirm the proxy** | ACTIVE - enable steps |
| **User asks how to read their savings** | ACTIVE - dashboard section |
| **Proxy crash, health check, or live status** | DORMANT - use Compress skill |
| **User is actively coding (no optimization discussion)** | DORMANT - do not activate |

## What TokenStack Is

TokenStack is a single transparent proxy that sits between Claude Code and the Anthropic API. It intercepts each request, compresses the bulky tool output inside it, and forwards the smaller payload upstream. Less text per turn means more usable context and lower token cost.

It is built into the `memstack-skill-loader` package. There is nothing extra to install: if you have MemStack, you have TokenStack.

> Earlier versions documented a 3-layer manual setup (Serena MCP, RTK CLI, and the Headroom API proxy). That stack is retired. TokenStack supersedes all three. There is no pip install, no Rust binary, no MCP server, and no command prefixing.

## Enabling It

Start the dashboard with the proxy flag:

```bash
python -m memstack_skill_loader dashboard --with-proxy
```

This starts the TokenStack proxy on `127.0.0.1:8787` and sets `ANTHROPIC_BASE_URL` for you, so Claude Code traffic routes through it automatically. No manual environment configuration is needed.

Options:

- `--proxy-port N` changes the proxy port (default 8787).
- To run only the proxy without the dashboard: `python -m memstack_skill_loader proxy`.

## Free vs Pro Transforms

Free-tier transforms run on every request and are lossless (they remove only redundant formatting):

| Transform | What it removes |
|-----------|-----------------|
| Strip ANSI codes | terminal color and escape sequences |
| Strip trailing whitespace | end-of-line padding |
| Collapse blank lines | runs of empty lines |
| Dedup consecutive identical lines | repeated identical lines |
| Strip preambles | "Here is the contents of file..." lead-ins |
| Collapse inline whitespace (Python) | redundant intra-line spacing |

Pro tier (active with a valid Pro license) adds seven more transforms on top:

| Transform | Effect |
|-----------|--------|
| AST truncation | Shortens Python function bodies while keeping signatures and type annotations. Largest single saving (around 78% on line-numbered Python). Lossy by design: Python code blocks are not preserved byte-for-byte. |
| JSON compression | Minifies verbose JSON output |
| Log deduplication | Folds repeated log lines |
| Path compression | Shortens long repeated file paths |
| Markdown stripping | Removes decorative markdown |
| System-prompt compression | Compresses system-prompt boilerplate |
| Conversation-history dedup | Drops duplicated earlier message blocks |

Only AST truncation is lossy. Every other transform reduces tokens without changing meaning.

## Confirming It Routes

The dashboard shows a proxy indicator with a live **PRO** or **FREE** tier badge plus your session and 30-day savings percentages. If the badge is present, traffic is routing through TokenStack.

A quick health check from a terminal:

```bash
curl http://127.0.0.1:8787/health
```

## Reading Your Savings

The dashboard reports savings in three places:

- **Overview header**: tokens saved for the current session and lifetime.
- **Burn Report**: a per-transform breakdown with estimated cost, filterable by all-time, daily, weekly, and monthly.
- **Per-Agent Token Cost**: the Burn Report also splits cost across the Manager, Builder, and Reviewer agents.

## What You Actually Do

1. Enable the proxy: `python -m memstack_skill_loader dashboard --with-proxy`.
2. Optionally activate a Pro license to unlock the seven Pro transforms.
3. Read your savings on the dashboard (Overview header and Burn Report).

No installs, no MCP servers, no command prefixing.

## Relationship to Other Skills

| Skill | Scope | When to Use |
|-------|-------|-------------|
| **Token Optimization** (this) | What TokenStack is, how to enable it, free vs Pro, reading savings | Understanding or turning on compression |
| **Compress** | Proxy health and live status troubleshooting | Proxy not routing, health checks |
| **Context DB** | SQLite fact store | Reducing repeated reads of project context |

## Level History

- **Lv.1** - Base: legacy 3-layer manual guide (Serena MCP, RTK CLI, Headroom API proxy). Retired. (Origin: MemStack Pro, Mar 2026)
- **Lv.2** - Rewrite: replaced the retired 3-layer manual stack with the built-in TokenStack proxy. Documents the verified enable command, free vs Pro transforms, proxy confirmation, and dashboard savings. (Jun 2026)
