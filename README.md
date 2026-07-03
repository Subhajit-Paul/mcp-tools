# mcp-tools

A collection of [MCP](https://modelcontextprotocol.io/) (Model Context Protocol) servers built with [FastMCP](https://github.com/jlowin/fastmcp), exposing tools that LLM agents can call. Most of the tools here wrap `subprocess.run` calls to shell out to command-line utilities (`git grep`, `tree`, `jg`), so `example.py` is included as a beginner-friendly reference for that pattern.

## Setup

Requires Python >= 3.13. Dependencies are managed with [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

## Servers

Each file is a standalone FastMCP server. Run one with:

```bash
fastmcp run <file>:mcp --transport sse --host 127.0.0.1 --port 6969
```

- **`jgmcp.py`** - Drives Cadence JasperGold formal verification: write an assertion into a SystemVerilog file, run `jg` on a Tcl script, and read back the report.
- **`codebase-search.py`** - Searches Verilog/SystemVerilog repositories using `git grep`: find patterns (with optional context), list signal declarations, find signal usages, and list module definitions (including ports/parameters).
- **`eq.py`** - Solves a univariate equation for its numerical roots using SymPy.
- **`test.py`** - Minimal example server (`mul(a, b)`) used to sanity-check the FastMCP setup.

## example.py

A standalone, dependency-free script demonstrating common `subprocess.run` usage patterns (capturing output, checking exit codes, error handling, timeouts, `cwd`, `env`, stdin). Not an MCP tool - just run it directly:

```bash
python3 example.py
```
