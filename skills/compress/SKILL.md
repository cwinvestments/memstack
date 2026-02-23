---
name: compress
description: "Headroom proxy manager. Checks status, stats, and troubleshoots token compression. Triggers on headroom, compression, token savings, proxy status."
---


# ⚙️ Compress — Headroom Proxy Manager
*Monitor and manage Headroom context compression for CC sessions.*

## Activation

When this skill activates, output:

`⚙️ Compress — Checking Headroom status...`

Then execute the protocol below.

- **Keywords:** headroom, compression stats, token savings, proxy status, check headroom
- **Contextual:** When user asks about token usage, context window limits, or session cost optimization
- **Level:** 2 (explicit trigger only)

## Context Guard

| Context | Status |
|---------|--------|
| **User says "headroom", "compression stats", "check proxy"** | ACTIVE — run status check |
| **User asks about token savings or context window** | ACTIVE — run session report |
| **Proxy errors or API connection failures appear** | ACTIVE — run health diagnostics |
| **General discussion about CC features** | DORMANT — do not activate |
| **User is actively coding (no proxy issues)** | DORMANT — do not activate |

## What It Does

Headroom is a transparent proxy between Claude Code and the Anthropic API that compresses tool outputs by removing redundant boilerplate. It extends effective context window by 30–40%.

This skill checks proxy health, reports compression stats, and troubleshoots connection issues.

## Prerequisites

- **Headroom installed:** `pip install headroom-ai`
- **Proxy running:** `headroom proxy` (defaults to `localhost:8787`)
- **CC configured:** `ANTHROPIC_BASE_URL=http://127.0.0.1:8787`

## Workflow

### 1. Status Check

Run:
```bash
curl -s http://127.0.0.1:8787/stats | python -m json.tool
```

Report: proxy up/down, requests processed, compression ratio, tokens saved, estimated cost savings.

### 2. Health Diagnostics

If proxy is unreachable:

1. Check if process is running:
   ```bash
   # Windows
   tasklist | findstr headroom
   # Linux/macOS
   ps aux | grep headroom
   ```
2. Check port binding:
   ```bash
   netstat -ano | findstr 8787
   ```
3. Verify `ANTHROPIC_BASE_URL` is set:
   ```bash
   echo $ANTHROPIC_BASE_URL
   ```
4. Restart: `headroom proxy` in a separate terminal

### 3. Session Report

When triggered at session end or on request, report:

- Requests this session
- Tokens before/after compression
- Compression ratio (target: 30–40%)
- Estimated dollar savings (at $15/MTok input, $75/MTok output for Opus)

### 4. Configuration Reference

| Setting | Value | Notes |
|---------|-------|-------|
| Proxy URL | `http://127.0.0.1:8787` | Default port |
| Dashboard | AdminStack Infrastructure tab | Headroom monitoring panel |
| Repo | `github.com/chopratejas/headroom` | Apache 2.0 |
| Python | 3.10–3.12 required | Dependency constraint |

## Output Format

```
⚙️ Headroom Status
├── Proxy: ✅ Running on :8787
├── Requests: 47 processed
├── Compression: 34.2% reduction
├── Tokens saved: ~12,400 tokens
└── Cost savings: ~$0.19 this session
```

## Integration

- **AdminStack:** Infrastructure page has Headroom tab with live dashboard
- **CC Sessions:** Auto-routed when `ANTHROPIC_BASE_URL` is set
- **Monitoring:** Stats endpoint polled every 30s with visibility-aware polling

## Level History

- **Lv.1** — Base: Health check and stats reporting for Headroom proxy. (Origin: MemStack v3.0, Feb 2026)
