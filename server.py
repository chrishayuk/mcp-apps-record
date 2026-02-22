"""
MCP Apps Record — three demo servers on one app, different paths.

Endpoints:
  /simple/mcp      — Shot 3: plain text, no MCP Apps
  /manual/mcp      — Shot 4: manual CallToolResult + structuredContent
  /decorator/mcp   — Shot 5: @chart_tool decorator

Run locally:  uv run server.py
Deploy:       fly deploy
"""

import os
from contextlib import asynccontextmanager

import uvicorn
from starlette.applications import Starlette
from starlette.routing import Mount

from simple_server import mcp as simple_mcp
from manual_server import mcp as manual_mcp
from decorator_server import mcp as decorator_mcp

# Get the sub-apps (this lazily creates session managers)
simple_app = simple_mcp.streamable_http_app()
manual_app = manual_mcp.streamable_http_app()
decorator_app = decorator_mcp.streamable_http_app()


@asynccontextmanager
async def lifespan(app):
    async with simple_mcp.session_manager.run():
        async with manual_mcp.session_manager.run():
            async with decorator_mcp.session_manager.run():
                yield


app = Starlette(
    routes=[
        Mount("/simple", app=simple_app),
        Mount("/manual", app=manual_app),
        Mount("/decorator", app=decorator_app),
    ],
    lifespan=lifespan,
)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
    )
