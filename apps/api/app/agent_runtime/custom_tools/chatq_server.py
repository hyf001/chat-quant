from __future__ import annotations

from typing import Any

from claude_agent_sdk import McpSdkServerConfig
from mcp.server import Server
from mcp.types import CallToolResult, TextContent, Tool

from app.agent_runtime.custom_tools.chatq_python import (
    CHATQ_PYTHON_MCP_TOOL_NAME,
    build_chatq_python_tool_schema,
    handle_chatq_python_tool,
)
from app.agent_runtime.custom_tools.chatq_strategy import (
    CHATQ_STRATEGY_MCP_TOOL_NAME,
    build_chatq_strategy_tool_schema,
    handle_chatq_strategy_tool,
)
from app.agent_runtime.custom_tools.chatq_visualization import (
    CHATQ_VISUALIZATION_MCP_TOOL_NAME,
    build_chatq_visualization_tool_schema,
    handle_chatq_visualization_tool,
)
from app.schema.agent_runtime import AgentExecutionCommand

CHATQ_SERVER_NAME = "chatq"


def build_chatq_mcp_server(command: AgentExecutionCommand) -> object:
    server = Server(CHATQ_SERVER_NAME, version="1.0.0")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool.model_validate(
                {
                    "name": CHATQ_STRATEGY_MCP_TOOL_NAME,
                    "description": (
                        "Operate Chat-Quant strategies and backtests using a CLI-style "
                        "command string. Supports --help and normal --flag arguments. "
                        "The current project is supplied by Chat-Quant; do not pass "
                        "project_id, user_id, or project_path."
                    ),
                    "inputSchema": build_chatq_strategy_tool_schema(),
                }
            ),
            Tool.model_validate(
                {
                    "name": CHATQ_PYTHON_MCP_TOOL_NAME,
                    "description": (
                        "Run Python code through Chat-Quant's internal Python execution "
                        "service using a chatq-python command string. For --code-file, "
                        "pass an absolute path under the current agent project directory."
                    ),
                    "inputSchema": build_chatq_python_tool_schema(),
                }
            ),
            Tool.model_validate(
                {
                    "name": CHATQ_VISUALIZATION_MCP_TOOL_NAME,
                    "description": (
                        "Validate and render strict Chat-Quant visualization specs using "
                        "a chatq-visualization command string. Supports chart/table/card/"
                        "report render, validate, and schema commands. The spec file and "
                        "output file must stay under the current project directory."
                    ),
                    "inputSchema": build_chatq_visualization_tool_schema(),
                }
            ),
        ]

    @server.call_tool(validate_input=False)
    async def call_tool(name: str, arguments: dict[str, Any]) -> CallToolResult:
        if name == CHATQ_STRATEGY_MCP_TOOL_NAME:
            result = await handle_chatq_strategy_tool(command, arguments)
        elif name == CHATQ_PYTHON_MCP_TOOL_NAME:
            result = await handle_chatq_python_tool(command, arguments)
        elif name == CHATQ_VISUALIZATION_MCP_TOOL_NAME:
            result = await handle_chatq_visualization_tool(command, arguments)
        else:
            raise ValueError(f"Tool not found: {name}")
        return CallToolResult(
            content=[TextContent(type="text", text=result.text)],
            isError=result.is_error,
        )

    return McpSdkServerConfig(
        type="sdk",
        name=CHATQ_SERVER_NAME,
        instance=server,
    )


build_chatq_strategy_mcp_server = build_chatq_mcp_server
