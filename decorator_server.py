"""
Shot 5: The Decorator Version — the payoff.

Same language popularity data, but using @chart_tool from chuk-view-schemas.
No HTML. No JavaScript. No resource registration. No CallToolResult boilerplate.

Run locally:  uv run decorator_server.py
Deploy:       fly deploy -c fly-decorator.toml
"""

import os

from mcp.server.fastmcp import FastMCP
from chuk_view_schemas.fastmcp import chart_tool
from chuk_view_schemas.chart import ChartContent, ChartDataset

mcp = FastMCP(
    "language-stats",
    host="0.0.0.0",
    port=int(os.getenv("PORT", "8000")),
)


@chart_tool(mcp, "show_popularity")
async def show_popularity(chart_type: str = "bar") -> ChartContent:
    """Show programming language popularity as an interactive chart.
    chart_type: bar, pie, line, doughnut, or area."""
    return ChartContent(
        chartType=chart_type,
        title="Programming Language Popularity (2026)",
        data=[
            ChartDataset(
                label="Usage %",
                values=[
                    {"label": "Python", "value": 31.0},
                    {"label": "JavaScript", "value": 25.2},
                    {"label": "Rust", "value": 18.1},
                    {"label": "Go", "value": 14.3},
                    {"label": "TypeScript", "value": 11.4},
                ],
            )
        ],
    )


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
