"""MCP server entry point."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from . import tools


def create_server() -> FastMCP:
    """Create the FastMCP application."""

    mcp = FastMCP("supermind-mcp")

    mcp.tool()(tools.list_kernels)
    mcp.tool()(tools.create_kernel)
    mcp.tool()(tools.execute_code)
    mcp.tool()(tools.interrupt_kernel)
    mcp.tool()(tools.delete_kernel)
    mcp.tool()(tools.sync_files)
    mcp.tool()(tools.download_files)
    mcp.tool()(tools.stock_intraday_realtime)
    mcp.tool()(tools.stock_intraday_realtime_batch)

    return mcp


def main() -> None:
    """Run the MCP server over stdio."""

    create_server().run()


if __name__ == "__main__":
    main()
