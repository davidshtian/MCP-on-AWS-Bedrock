import httpx
import argparse
from pydantic import Field
from mcp.server.fastmcp import FastMCP


def create_fetch_url_tool(mcp):
    @mcp.tool()
    async def fetch_url(
        url: str = Field(description="URL to fetch"),
    ) -> str:
        """Fetches a website and returns its content"""
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            return response.text

    return fetch_url


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run MCP server with optional transport and port"
    )
    parser.add_argument("--transport", type=str, help="Transport method to use")
    parser.add_argument(
        "--port", type=int, default=8000, help="Port to run server on (default: 8000)"
    )
    args = parser.parse_args()

    if args.transport == "streamable-http":
        mcp = FastMCP("Echo", port=args.port)
        # Register the tool
        create_fetch_url_tool(mcp)
        mcp.run(transport="streamable-http")
    else:
        mcp = FastMCP("Echo")
        # Register the tool
        create_fetch_url_tool(mcp)
        mcp.run()
