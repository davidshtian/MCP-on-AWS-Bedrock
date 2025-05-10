import asyncio
import json
import boto3
import logging
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def convert_tool_format(tools):
    """
    Converts tools into the format required for the Bedrock API.

    Args:
        tools (list): List of tool objects

    Returns:
        dict: Tools in the format required by Bedrock
    """
    converted_tools = []

    for tool in tools:
        converted_tool = {
            "toolSpec": {
                "name": tool.name,
                "description": tool.description,
                "inputSchema": {"json": tool.inputSchema},
            }
        }
        converted_tools.append(converted_tool)

    return {"tools": converted_tools}


async def main():
    # Initialize Bedrock client
    bedrock = boto3.client("bedrock-runtime")

    async with streamablehttp_client("http://localhost:8000/mcp") as (
        read_stream,
        write_stream,
        _,
    ):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            # List available tools and convert to serializable format
            tools_result = await session.list_tools()
            tools_list = [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "inputSchema": tool.inputSchema,
                }
                for tool in tools_result.tools
            ]
            logger.info("Available tools: %s", tools_list)

            # Prepare the request for Nova Pro model
            system = [
                {
                    "text": "You are a helpful AI assistant. You have access to the following tools: "
                    + json.dumps(tools_list)
                }
            ]

            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "text": "Hello, can you help me fetch the website 'https://www.example.com?'"
                        }
                    ],
                }
            ]

            while True:

                # Call Bedrock with Nova Pro model
                response = bedrock.converse(
                    modelId="us.amazon.nova-pro-v1:0",
                    messages=messages,
                    system=system,
                    inferenceConfig={"maxTokens": 300, "topP": 0.1, "temperature": 0.3},
                    toolConfig=convert_tool_format(tools_result.tools),
                )

                output_message = response["output"]["message"]
                messages.append(output_message)
                stop_reason = response["stopReason"]

                # Print the model's response
                for content in output_message["content"]:
                    if "text" in content:
                        print("Model:", content["text"])

                if stop_reason == "tool_use":
                    # Tool use requested. Call the tool and send the result to the model.
                    tool_requests = response["output"]["message"]["content"]
                    print(tool_requests)
                    for tool_request in tool_requests:
                        if "toolUse" in tool_request:
                            tool = tool_request["toolUse"]
                            logger.info(
                                "Requesting tool %s. Request: %s",
                                tool["name"],
                                tool["toolUseId"],
                            )

                            try:
                                # Call the tool through the MCP session
                                tool_response = await session.call_tool(
                                    tool["name"], tool["input"]
                                )

                                # Convert tool response to expected format
                                tool_result = {
                                    "toolUseId": tool["toolUseId"],
                                    "content": [{"text": str(tool_response)}],
                                }
                            except Exception as err:
                                logger.error("Tool call failed: %s", str(err))
                                tool_result = {
                                    "toolUseId": tool["toolUseId"],
                                    "content": [{"text": f"Error: {str(err)}"}],
                                    "status": "error",
                                }

                            # Add tool result to messages
                            messages.append(
                                {
                                    "role": "user",
                                    "content": [{"toolResult": tool_result}],
                                }
                            )
                else:
                    # No more tool use requests, we're done
                    break


if __name__ == "__main__":
    asyncio.run(main())
