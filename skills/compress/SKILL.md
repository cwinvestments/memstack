---
name: compress
description: "Use when the user says 'tokenstack', 'compression', 'token savings', 'proxy status', or asks about context window usage."
version: 2.0.0
---


# Compress - TokenStack Proxy Manager
*Monitor and troubleshoot the built-in TokenStack compression proxy for CC sessions.*

## Activation

When this skill activates, output:

`Compress - Checking TokenStack status...`

Then execute the protocol below.

- **Keywords:** tokenstack, compression stats, token savings, proxy status, check proxy
- **Contextual:** When user asks about token usage, context window limits, or session cost
- **Level:** 2 (explicit trigger only)

## Context Guard

| Context | Status |
|---------|--------|
| **User says "tokenstack", "compression stats", "check proxy"** | ACTIVE - run status check |
| **User asks about token savings or context window** | ACTIVE - point to dashboard report |
| **Proxy errors or API connection failures appear** | ACTIVE - run health diagnostics |
| **General discussion about CC features** | DORMANT - do not activate |
| **User is actively coding (no proxy issues)** | DORMANT - do not activate |

## What It Does

TokenStack is a transparent proxy between Claude Code and the Anthropic API. It compresses tool output before it reaches the API, extending effective context and lowering token cost.

This skill checks that the proxy is running and routing, and troubleshoots connection issues. For the full feature overview, enable steps, and transform tables, use the Token Optimization skill.

## Prerequisites

TokenStack ships inside the `memstack-skill-loader` package. There is no separate install.

- **Start with the dashboard (recommended):** `python -m memstack_skill_loader dashboard --with-proxy`
  - Starts the proxy on `127.0.0.1:8787` and sets `ANTHROPIC_BASE_URL` automatically.
- **Run only the proxy:** `python -m memstack_skill_loader proxy`

## Workflow

### 1. Health Check

```cmd
curl http://127.0.0.1:8787/health
```

A healthy proxy responds on `/health`. If there is no response, the proxy is not running.

Note: the proxy has no `/stats` endpoint. Live savings are reported in the dashboard, not over curl. See "Reading Savings" below.

### 2. Confirm Routing

Open the dashboard and look at the proxy indicator. A live **PRO** or **FREE** badge means Claude Code traffic is routing through TokenStack. If the badge reads "not detected," the dashboard was started without `--with-proxy`; restart it with the flag.

### 3. Diagnose "not running"

Check the port:

```cmd
netstat -ano | findstr 8787
```

If nothing is listening, start it:

```cmd
python -m memstack_skill_loader dashboard --with-proxy
```

### 4. Reading Savings

Savings live in the dashboard (default `http://localhost:3333`):

- **Proxy indicator:** PRO or FREE badge with session and 30-day percentages
- **Overview header:** session and lifetime tokens saved
- **Burn Report:** per-transform breakdown, estimated cost, time filters (all-time, daily, weekly, monthly), and a per-agent split for the Manager, Builder, and Reviewer

## Tier Behavior

| Tier | Transforms |
|------|-----------|
| Free | Six lossless text reductions, always applied |
| Pro | Adds seven transforms including AST truncation (license-gated) |

A valid Pro license switches the proxy to Pro tier automatically. The dashboard badge shows the active tier.

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| **No response on `/health`** | Proxy not running. Start with `python -m memstack_skill_loader dashboard --with-proxy`. |
| **Proxy indicator shows "not detected"** | Dashboard was started without `--with-proxy`. Restart with the flag. |
| **Badge shows FREE but you hold Pro** | License cache may be stale. The proxy revalidates the license on next start. |
| **Cost figures differ from Anthropic Console** | Estimates use list token prices and do not model server-side prompt caching. For billed cost, check console.anthropic.com. |

## Output Format

```
TokenStack Status
  Proxy: Running on :8787
  Tier: PRO
  Savings: read in the dashboard (Overview header and Burn Report)
```

## Integration

- **Dashboard:** proxy indicator, Overview header, and Burn Report
- **CC sessions:** auto-routed when the dashboard is started with `--with-proxy`
- **Standalone proxy:** `python -m memstack_skill_loader proxy`

## Relationship to Other Skills

| Skill | Scope | When to Use |
|-------|-------|-------------|
| **Token Optimization** | Full TokenStack overview, enable steps, transform tables | Understanding or turning on compression |
| **Compress** (this) | Health, routing, troubleshooting | Proxy not running or not routing |

## Level History

- **Lv.1** - Base: health check and stats reporting for the legacy Headroom proxy. (Origin: MemStack, Feb 2026)
- **Lv.2** - Rewrite: retargeted to the built-in TokenStack proxy. Removed the external Headroom install and the `/stats` curl; savings are now read from the dashboard. (Jun 2026)
