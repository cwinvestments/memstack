---
name: token-optimization
description: "Use when the user says 'token optimization', 'save tokens', 'context window', 'reduce tokens', 'RTK', 'Serena', 'token stack', or asks about extending context window capacity. Covers the 3-layer token optimization stack: Headroom (API compression), RTK (CLI output compression), and Serena (LSP-backed code navigation). Do NOT use for Headroom-only troubleshooting (Compress skill)."
version: 1.0.0
license: "Proprietary — MemStack Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# Token Optimization Guide — Full Stack Setup

*Three complementary tools that reduce token consumption by 50-80% across different layers of the Claude Code pipeline.*

## Activation

When this skill activates, output:

`Token Optimization Guide — Configuring the 3-layer token stack...`

Then execute the protocol below.

## Context Guard

| Context | Status |
|---------|--------|
| **User asks about token savings, context optimization** | ACTIVE — full guide |
| **User says "RTK", "Serena", "token stack"** | ACTIVE — relevant section |
| **User wants to install or configure any layer** | ACTIVE — install steps |
| **User asks about context window limits** | ACTIVE — explain stack |
| **Headroom-only troubleshooting (proxy crash, health check)** | DORMANT — use Compress skill |
| **User is actively coding (no optimization discussion)** | DORMANT — do not activate |

## How They Stack

```
                    Claude Code Context Window
                    ==========================

  Layer 3: Serena (MCP)         Prevents token waste at the SOURCE
  ─────────────────────         Instead of reading entire files,
                                 use LSP to fetch only the symbols
                                 and references you need.
                                 Savings: variable (avoids 1000s of
                                 tokens per file read)
                                        │
                                        ▼
  Layer 2: RTK (CLI proxy)      Compresses tool OUTPUT
  ────────────────────────      git diff, npm install, build logs —
                                 all compressed 60-90% before they
                                 enter the context window.
                                        │
                                        ▼
  Layer 1: Headroom (API proxy) Compresses API TRAFFIC
  ──────────────────────────    Compresses the full conversation
                                 payload between CC and the Anthropic
                                 API. ~34% reduction on wire traffic.
                                        │
                                        ▼
                              Anthropic API
```

**Key insight:** Each layer operates at a different point in the pipeline, so they multiply rather than overlap. A `git diff` that produces 5,000 tokens might become 1,000 after RTK, and the full conversation round-trip is further compressed by Headroom.

---

## Layer 1: Headroom (API Compression)

Headroom is a local proxy that compresses conversation payloads between Claude Code and the Anthropic API using LLMLingua-2.

### Prerequisites

- Python 3.10+ with pip
- ~500MB disk for model weights (downloaded on first run)

### Install

```bash
pip install headroom-ai[code]
```

The `[code]` extra includes tree-sitter AST compression for code-aware filtering.

### Run

**Terminal 1 — Start the proxy:**
```bash
headroom proxy --llmlingua-device cpu --port 8787
```

**Terminal 2 — Start Claude Code with proxy:**

Windows:
```bash
set ANTHROPIC_BASE_URL=http://127.0.0.1:8787
claude
```

macOS/Linux:
```bash
ANTHROPIC_BASE_URL=http://127.0.0.1:8787 claude
```

### Verify

```bash
# Health check
curl http://127.0.0.1:8787/health

# Token savings stats
curl http://127.0.0.1:8787/stats
```

Expected output from `/stats`: compression ratio, tokens saved, requests processed.

### Typical Savings

| Content Type | Compression |
|-------------|-------------|
| Code files | 30-46% |
| Conversation text | 25-35% |
| Tool output | 30-40% |
| **Average** | **~34%** |

### Troubleshooting

| Issue | Fix |
|-------|-----|
| Compression at 0% | Install with `[code]` extra: `pip install headroom-ai[code]` |
| Proxy not reachable | Check `curl http://127.0.0.1:8787/health` — restart if needed |
| API errors in CC | Headroom may have crashed — unset `ANTHROPIC_BASE_URL` to bypass |
| Slow first request | Model weights downloading (~500MB) — one-time cost |

---

## Layer 2: RTK (CLI Output Compression)

RTK (Rust Token Killer) is a Rust binary that sits between shell commands and Claude Code, compressing verbose CLI output before it enters the context window.

### Prerequisites

- No runtime dependencies (single static binary)

### Install

**Windows (pre-built binary):**
```bash
# Download from GitHub releases
gh release download --repo rtk-ai/rtk --pattern "rtk-x86_64-pc-windows-msvc.zip" --dir /tmp
unzip /tmp/rtk-x86_64-pc-windows-msvc.zip -d /tmp/rtk-extract
cp /tmp/rtk-extract/rtk.exe ~/.local/bin/rtk.exe
```

**macOS/Linux (pre-built binary):**
```bash
curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/main/install.sh | sh
```

**From source (any platform with Rust):**
```bash
cargo install --git https://github.com/rtk-ai/rtk
```

### Configure for Claude Code

```bash
# Global (all projects) — recommended
rtk init -g

# Per-project only
rtk init
```

**Platform behavior:**
- **macOS/Linux:** Installs as a Claude Code hook (automatic interception)
- **Windows:** Falls back to CLAUDE.md injection (injects instructions telling CC to prefix commands with `rtk`)

Both approaches produce identical token savings.

### Usage

Prefix any command with `rtk`:

```bash
rtk git status          # Compact status (62% savings)
rtk git diff            # Ultra-condensed diff
rtk git log             # Compact log
rtk npm install         # Filtered install output (70-90%)
rtk npm run build       # Compressed build output
rtk ls -la              # Token-optimized directory listing
rtk docker ps           # Compact container list
rtk kubectl get pods    # Compressed k8s output
```

RTK is a transparent proxy — if it has a dedicated filter for the command, it compresses. If not, it passes through unchanged. `rtk <anything>` is always safe.

### Verify

```bash
rtk --version    # Should show version number
rtk gain         # Show cumulative token savings
```

### Typical Savings

| Command Category | Compression |
|-----------------|-------------|
| Git (status, log, diff) | 59-80% |
| GitHub CLI (pr, run, issue) | 26-87% |
| Package managers (npm, pnpm) | 70-90% |
| File operations (ls, read) | 60-75% |
| Infrastructure (docker, k8s) | 85% |
| Network (curl, wget) | 65-70% |
| **Average** | **60-90%** |

---

## Layer 3: Serena (LSP Code Navigation)

Serena is an MCP server that provides IDE-like code navigation tools backed by Language Server Protocol. Instead of reading entire files to find a function definition, Serena uses LSP to return only the symbol you need.

### Prerequisites

- uv (Python package manager): `pip install uv`

### Install & Configure

```bash
# Add to Claude Code as a global MCP server
claude mcp add --scope user serena -- \
  uvx --from git+https://github.com/oraios/serena \
  serena start-mcp-server \
  --context=claude-code \
  --project-from-cwd
```

**Flags explained:**
- `--context=claude-code` disables tools that duplicate CC's built-in capabilities
- `--project-from-cwd` auto-detects the project from CC's working directory

### Verify

```bash
claude mcp list 2>&1 | grep serena
# Should show: serena: ... ✓ Connected
```

### Key Tools (28 total in claude-code context)

**Symbol navigation (the core value):**

| Tool | Purpose |
|------|---------|
| `find_symbol` | Global symbol search via LSP (functions, classes, variables) |
| `find_referencing_symbols` | Find all references to a symbol across the codebase |
| `get_symbols_overview` | List top-level symbols in a file (like an IDE outline) |
| `rename_symbol` | Refactor-safe rename across the entire codebase |
| `replace_symbol_body` | Replace a function/class definition by name |
| `insert_before_symbol` | Insert code before a symbol definition |
| `insert_after_symbol` | Insert code after a symbol definition |

**File and search:**

| Tool | Purpose |
|------|---------|
| `find_file` | Find files by name/pattern |
| `read_file` | Read file contents |
| `search_for_pattern` | Regex search across project |
| `list_dir` | Directory listing |

**Memory (cross-session project knowledge):**

| Tool | Purpose |
|------|---------|
| `write_memory` | Store project facts for future sessions |
| `read_memory` | Retrieve stored project knowledge |
| `list_memories` | List all stored memory files |

**Workflow:**

| Tool | Purpose |
|------|---------|
| `onboarding` | Auto-discover project structure |
| `activate_project` | Switch active project |
| `get_current_config` | Show current Serena configuration |

### Why LSP Matters for Tokens

Traditional approach (brute force):
```
Read entire 500-line file → find the one function → 3,000 tokens consumed
```

Serena approach (surgical):
```
find_symbol("handleAuth") → returns only that function → 200 tokens consumed
```

For large codebases, this difference compounds across every file interaction.

### Language Support

Serena supports 40+ languages via LSP, including: TypeScript, JavaScript, Python, Rust, Go, Java, C#, C/C++, Ruby, PHP, Swift, Kotlin, and more.

---

## Quick Start Checklist

For a fresh machine, install all three layers in order:

```bash
# 1. Headroom (API compression)
pip install headroom-ai[code]

# 2. RTK (CLI compression)
gh release download --repo rtk-ai/rtk --pattern "rtk-x86_64-pc-windows-msvc.zip" --dir /tmp
unzip /tmp/rtk-x86_64-pc-windows-msvc.zip -d /tmp/rtk-extract
cp /tmp/rtk-extract/rtk.exe ~/.local/bin/rtk.exe
rtk init -g

# 3. Serena (LSP navigation)
pip install uv
claude mcp add --scope user serena -- \
  uvx --from git+https://github.com/oraios/serena \
  serena start-mcp-server \
  --context=claude-code \
  --project-from-cwd
```

**Start a session with all layers active:**
```bash
# Terminal 1
headroom proxy --llmlingua-device cpu --port 8787

# Terminal 2
set ANTHROPIC_BASE_URL=http://127.0.0.1:8787   # Windows
claude
```

RTK and Serena activate automatically (CLAUDE.md injection and MCP server).

## Verify All Layers

```bash
# Headroom
curl http://127.0.0.1:8787/health

# RTK
rtk --version
rtk gain

# Serena
claude mcp list 2>&1 | grep serena
```

## Windows-Specific Notes

| Component | Windows Behavior |
|-----------|-----------------|
| **Headroom** | Use `set ANTHROPIC_BASE_URL=...` (not `export`) |
| **RTK** | Uses CLAUDE.md injection instead of CC hooks. Download `.zip` from releases, not the install script. Binary goes in `~/.local/bin/rtk.exe` |
| **Serena** | Works identically — `uv`/`uvx` handle Windows natively |
| **PATH** | Ensure `~/.local/bin` is in your PATH for RTK |

## Relationship to Other Skills

| Skill | Scope | When to Use |
|-------|-------|-------------|
| **Token Optimization** (this) | Full 3-layer stack setup and reference | Installing, configuring, or understanding the optimization stack |
| **Compress** | Headroom-only troubleshooting | Proxy crashes, health checks, stats monitoring |
| **Context DB** | SQLite fact store | Reducing token waste from repeatedly reading project context |

## Level History

- **Lv.1** — Base: Comprehensive 3-layer token optimization guide covering Headroom (API compression), RTK (CLI output compression), and Serena (LSP code navigation). Install steps, verification commands, typical savings, and Windows-specific notes. (Origin: MemStack Pro v3.3.2, Mar 2026)
