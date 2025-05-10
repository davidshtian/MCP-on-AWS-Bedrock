# MCP on AWS Bedrock
A simple and clear example for implementation and understanding Anthropic MCP (on AWS Bedrock).

<a href="https://glama.ai/mcp/servers/cuhom1oc17">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/cuhom1oc17/badge" />
</a>

> For multiple MCP servers management, [this tiny project Q-2001](https://github.com/davidshtian/Q-2001) could be referred~

## Overview
This project demonstrates how to implement and use Anthropic's Model Context Protocol (MCP) with AWS Bedrock. It provides a client implementation that can interact with MCP-enabled tools through AWS Bedrock's runtime service.

## Updates 2025-05-10: Streamable HTTP

- Add support for [Streamable HTTP](https://github.com/modelcontextprotocol/python-sdk/releases/tag/v1.8.0)
- Rewrite the URL fetching MCP server `fetch_url_mcp_server.py` that demonstrates different transport types

### Usage Instructions

Run the server with default stdio settings (no transport parameter):
```bash
uv run fetch_url_mcp_server.py

# client
uv run client_stdio.py
```

Run with streamable-http transport on default port (8000):
```bash
python fetch_url_mcp_server.py --transport streamable-http

# client
uv run client_streamablehttp.py
```

Run with streamable-http transport on custom port:
```bash
python fetch_url_mcp_server.py --transport streamable-http --port 8080
```

## Prerequisites
- Python 3.10 or higher
- AWS account with Bedrock access
- Configured AWS credentials
- UV package manager

## Features
- Seamless integration with AWS Bedrock runtime using Converse API
- Tool format conversion for Bedrock compatibility
- Asynchronous communication handling
- Structured logging for debugging

## Contributing
Feel free to submit issues and pull requests to improve the implementation.

## License
MIT License

## References
- [Anthropic MCP](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [AWS Bedrock](https://aws.amazon.com/bedrock/)
