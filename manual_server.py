import os

import httpx
from mcp.server.fastmcp import FastMCP
from mcp.types import CallToolResult, TextContent

mcp = FastMCP(
    "language-stats",
    host="0.0.0.0",
    port=int(os.getenv("PORT", "8000")),
)

# ── CDN config ────────────────────────────────────────────────────────────
CDN_URL = "https://chuk-mcp-ui-views.fly.dev/chart/v1"
RESOURCE_URI = "ui://language-stats/chart"

# ── Step 1: Register a ui:// resource ─────────────────────────────────────
# The host fetches this HTML and renders it in a sandboxed iframe.

_html_cache: str | None = None


@mcp.resource(RESOURCE_URI, name="Chart View", mime_type="text/html;profile=mcp-app")
async def chart_resource() -> str:
    global _html_cache
    if _html_cache is None:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(CDN_URL, follow_redirects=True)
            resp.raise_for_status()
            _html_cache = resp.text
    return _html_cache


# ── Step 2: Tool with _meta.ui.resourceUri ────────────────────────────────
# The host sees resourceUri and knows to preload the UI resource.

@mcp.tool(
    meta={"ui": {"resourceUri": RESOURCE_URI}},
)
async def show_chart(chart_type: str = "bar") -> CallToolResult:
    """Show programming language popularity as an interactive chart.
    chart_type: bar, pie, line, doughnut, or area."""

    data = {
        "Python": 31.0,
        "JavaScript": 25.2,
        "Rust": 18.1,
        "Go": 14.3,
        "TypeScript": 11.4,
    }

    # Step 3: Return CallToolResult (NOT a plain dict!)
    # ❌ Returning a plain dict silently drops structuredContent.
    # ✅ Must use CallToolResult for the UI to receive data.
    return CallToolResult(
        # What the LLM sees — text summary for reasoning
        content=[
            TextContent(
                type="text",
                text=f"Programming language popularity ({chart_type} chart).",
            )
        ],
        # What the UI sees — full data, hydrates the chart component
        structuredContent={
            "type": "chart",
            "version": "1.0",
            "title": "Programming Language Popularity (2026)",
            "chartType": chart_type,
            "data": [
                {
                    "label": "Usage %",
                    "values": [
                        {"label": lang, "value": pct}
                        for lang, pct in data.items()
                    ],
                }
            ],
        },
    )


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
