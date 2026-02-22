"""
Shot 3: The "Before" — a plain MCP server with no MCP Apps.
Returns programming language popularity as plain text.

Run locally:  uv run simple_server.py
Deploy:       fly deploy -c fly-simple.toml
"""

import os

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "language-stats",
    host="0.0.0.0",
    port=int(os.getenv("PORT", "8000")),
)


@mcp.tool()
async def get_language_popularity() -> str:
    """Get programming language popularity from latest survey data."""
    data = {
        "Python": 31.0,
        "JavaScript": 25.2,
        "Rust": 18.1,
        "Go": 14.3,
        "TypeScript": 11.4,
    }
    lines = [f"  {lang}: {pct}%" for lang, pct in data.items()]
    return "Programming Language Popularity (2026):\n" + "\n".join(lines)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
