# MCP on AWS Bedrock
A simple and clear example for implementation and understanding Anthropic MCP (on AWS Bedrock, with Nova).

## Overview
This project demonstrates how to implement and use Anthropic's Model Context Protocol (MCP) with AWS Bedrock. It provides a client implementation that can interact with MCP-enabled tools through AWS Bedrock's runtime service.

## Prerequisites
- Python 3.10 or higher
- AWS account with Bedrock access
- Configured AWS credentials
- UV package manager

## Project Structure
- `client_stdio.py`: Main client implementation for interacting with Bedrock and MCP tools using stdio mode
- `client_sse.py`: Main client implementation for interacting with Bedrock and MCP tools using sse mode
- `mcp_simple_tool/`: Directory containing the MCP tool implementation
  - `server.py`: MCP tool server implementation
  - `__main__.py`: Entry point for the tool
- `pyproject.toml`: Project dependencies and configuration

## Usage
Run the stdio client with:
```bash
uv pip install boto3
uv run client_stdio.py
```

The client will:
1. Initialize a connection to AWS Bedrock
2. Start the MCP tool server
3. List available tools and convert them to the format required by Bedrock
4. Handle communication between Bedrock and the MCP tools

Run the sse client with:
```bash
uv run mcp-simple-tool --transport sse --port 8000

uv pip install boto3
uv run client_sse.py
```

## Features
- Seamless integration with AWS Bedrock runtime
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
