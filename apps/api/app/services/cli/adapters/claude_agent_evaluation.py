"""Claude Agent Evaluation provider implementation.

This adapter evaluates the quality of data analysis agent execution sessions.
"""
from __future__ import annotations

import asyncio
import json
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, AsyncGenerator, Callable, Dict, List, Optional, override

from app.core.terminal_ui import ui
from app.models.messages import Message
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions

from app.common.types import AgentType
from app.core.config import settings, PROJECT_ROOT

from ..base import MODEL_MAPPING, BaseCLI
from claude_agent_sdk.types import (
    SystemMessage,
    AssistantMessage,
    UserMessage,
    ResultMessage,
    TextBlock,
    ToolUseBlock,
    ToolResultBlock,
)
from app.services.tools import sql_tools_server,report_tools_server


class ClaudeAgentEvaluation():
    """Claude Agent Evaluation implementation for assessing agent execution quality"""

    def __init__(self, project_id: str, model: str):
        self.project_id = project_id
        self.model = model

        # Load evaluation prompt to use in instructions (Windows compatibility)
        self.evaluation_prompt = self._load_evaluation_prompt()

    def _load_evaluation_prompt(self) -> str:
        """Load evaluation prompt from file"""
        try:
            # Use PROJECT_ROOT from config
            prompt_dir = PROJECT_ROOT / "apps" / "api" / "app" / "prompt"
            ui.debug(f"Prompt directory: {prompt_dir}", "Evaluation")

            # Load the evaluation prompt
            prompt_path = prompt_dir / "system-prompt-analysis-evaluation.md"

            if not prompt_path.exists():
                raise FileNotFoundError(f"Evaluation prompt not found: {prompt_path}")

            ui.success(f"Using evaluation prompt: {prompt_path.name}", "Evaluation")

            with open(prompt_path, 'r', encoding='utf-8') as f:
                system_prompt = f.read()

            ui.success(f"Loaded evaluation prompt: {len(system_prompt)} chars", "Evaluation")
            return system_prompt
        except Exception as e:
            ui.error(f"Failed to load evaluation prompt: {e}", "Evaluation")
            return (
                "You are an Agent Evaluation Expert specialized in assessing data analysis agent execution quality. "
                "Evaluate the agent trace and provide a comprehensive evaluation report."
            )

    def _get_clean_tool_display(self, tool_name: str, tool_input: Dict[str, Any]) -> str:
        """Generate clean display string for tool usage"""
        try:
            # Format tool input nicely
            if isinstance(tool_input, dict):
                # Show key parameters only
                key_params = []
                for key, value in tool_input.items():
                    if isinstance(value, str) and len(value) > 50:
                        key_params.append(f"{key}=<{len(value)} chars>")
                    else:
                        key_params.append(f"{key}={value}")
                params = ", ".join(key_params[:3])  # Show max 3 params
                if len(tool_input) > 3:
                    params += ", ..."
                return f"Tool: {tool_name}({params})"
            else:
                return f"Tool: {tool_name}"
        except Exception as e:
            return f"Tool: {tool_name} (display error: {e})"

    def get_supported_models(self) -> List[str]:
        """Get list of supported Claude models for evaluation"""
        # Return all available Claude models from MODEL_MAPPING
        return list(set(MODEL_MAPPING.values()))

    async def check_availability(self) -> Dict[str, Any]:
        """Check if Claude Agent SDK is available"""
        try:
            import claude_agent_sdk
            return {
                "available": True,
                "configured": True,
                "mode": "Evaluation",
                "models": self.get_supported_models(),
                "default_models": [
                    "claude-sonnet-4-5-20250929",
                    "claude-opus-4-1-20250805",
                ],
            }
        except ImportError:
            return {
                "available": True,
                "configured": True,
                "mode": "Evaluation (Development Mode)",
                "models": self.get_supported_models(),
                "default_models": [
                    "claude-sonnet-4-5-20250929",
                    "claude-opus-4-1-20250805",
                ],
                "warning": (
                    "Claude Agent SDK not installed. Running in development mode.\n"
                    "To install: pip install claude-agent-sdk>=0.1.2"
                ),
            }

    def init_claude_option(self,
                       project_id: str,
                       claude_session_id: Optional[str],
                       model: Optional[str] = None) -> ClaudeAgentOptions:
        """connect and return Claude Agent SDK client"""

        allowed_tools = [
            "Read",
            "Write",
            "Edit",
            "MultiEdit",
            "Bash",
            "Glob",
            "Grep",
            "LS",
            "WebFetch",
            "WebSearch",
            "TodoWrite",
            "mcp__sql__download_sql_result",
            "mcp__sql__preview_sql_result",
            "mcp__report__preview_report_data",
            "mcp__report__download_report_data",
            ]
        # Get CLI-specific model name
        cli_model = "claude-sonnet-4-5-20250929" if model is None else MODEL_MAPPING.get(model,"claude-sonnet-4-5-20250929")

        # Determine working directory - ensure it exists
        project_path = os.path.join(settings.projects_root, project_id)
        if not os.path.exists(project_path):
            # If project directory doesn't exist, create it
            try:
                os.makedirs(project_path, exist_ok=True)
                ui.info(f"Created project directory: {project_path}", "Evaluation")
            except Exception as e:
                # If we can't create it, use projects_root as fallback
                ui.warning(f"Failed to create project directory: {e}, using projects_root", "Evaluation")
                project_path = settings.projects_root

        options = ClaudeAgentOptions(
            system_prompt=None,
            allowed_tools=allowed_tools,
            mcp_servers={"sql":sql_tools_server,"report":report_tools_server},
            permission_mode="bypassPermissions",
            model=cli_model,
            setting_sources=["user", "project", "local"],
            cwd=project_path,
            env={
                    "NODE_TLS_REJECT_UNAUTHORIZED": "0"
                }
        )
        return options

    async def evaluate_trace_with_streaming(
        self,
        trace_file_path: str,
        project_id: str,
        session_id: Optional[str] = None,
        log_callback: Optional[Callable[[str], Any]] = None,
        model: Optional[str] = None,
        reference_answer: Optional[str] = None,
    ) -> AsyncGenerator[Message, None]:
        """
        Evaluate a trace file using Claude Agent SDK with streaming responses.

        Args:
            trace_file_path: Path to the trace JSON file
            project_id: Project ID for storing evaluation results
            session_id: Optional session ID for tracking (unused, kept for compatibility)
            log_callback: Callback for logging
            model: Model to use for evaluation
            reference_answer: Optional human-labeled reference answer for comparison

        Yields:
            Message objects with evaluation progress and results
        """
        ui.info("Starting trace evaluation", "Evaluation")
        ui.debug(f"Trace file: {trace_file_path}", "Evaluation")
        ui.debug(f"Project ID: {project_id}", "Evaluation")
        if reference_answer:
            ui.info(f"Reference answer provided ({len(reference_answer)} chars)", "Evaluation")

        # Verify trace file exists
        trace_path = Path(trace_file_path)
        if not trace_path.exists():
            error_msg = f"Trace file not found: {trace_file_path}"
            ui.error(error_msg, "Evaluation")
            yield Message(
                id=str(uuid.uuid4()),
                project_id=project_id,
                role="system",
                message_type="error",
                content=error_msg,
                metadata_json={"error": "file_not_found"},
                session_id=session_id,
                created_at=datetime.utcnow(),
            )
            return

        # Load trace data
        try:
            with open(trace_path, 'r', encoding='utf-8') as f:
                trace_data = json.load(f)
            ui.success(f"Loaded trace data: {trace_data.get('statistics', {}).get('total_messages', 0)} messages", "Evaluation")
        except Exception as e:
            error_msg = f"Failed to parse trace file: {e}"
            ui.error(error_msg, "Evaluation")
            yield Message(
                id=str(uuid.uuid4()),
                project_id=project_id,
                role="system",
                message_type="error",
                content=error_msg,
                metadata_json={"error": "parse_failed"},
                session_id=session_id,
                created_at=datetime.utcnow(),
            )
            return

        if log_callback:
            await log_callback("Starting evaluation...")

        # Get project path (root directory containing data/, repo/, scripts/, dashboard/)
        project_path_str = os.path.join(settings.projects_root, project_id)

        # Get current date
        current_date = datetime.now().strftime("%Y-%m-%d")

        # Construct evaluation instruction using template variable replacement
        instruction = self.evaluation_prompt

        # Replace template variables
        instruction = instruction.replace("{{project_path}}", project_path_str)
        instruction = instruction.replace("{{current_date}}", current_date)
        instruction = instruction.replace("{{trace_file_path}}", trace_file_path)
        instruction = instruction.replace("{{reference_answer}}", reference_answer or "")

        ui.debug(f"Instruction prepared: {len(instruction)} chars", "Evaluation")
        ui.debug(f"Variables: project_path={project_path_str}, date={current_date}", "Evaluation")

        # Change to project root directory to access trace files
        cli_model = MODEL_MAPPING.get(model, "") or "claude-sonnet-4-5-20250929"

        try:

            ui.success("Query sent", "Evaluation")
            async with ClaudeSDKClient(self.init_claude_option(project_id, session_id, model)) as cli:
                await cli.query(instruction)
            # Stream responses - only yield final report content
                async for message_obj in cli.receive_messages():
                    # Handle SystemMessage
                    if isinstance(message_obj, SystemMessage) or "SystemMessage" in str(type(message_obj)):
                        # Just log, don't yield to frontend
                        ui.success(f"Evaluation Agent initialized (Model: {cli_model})", "Evaluation")

                    # Handle AssistantMessage
                    elif isinstance(message_obj, AssistantMessage) or "AssistantMessage" in str(type(message_obj)):
                        content = ""

                        if hasattr(message_obj, "content") and isinstance(message_obj.content, list):
                            for block in message_obj.content:
                                if isinstance(block, TextBlock):
                                    content += block.text
                                elif isinstance(block, ToolUseBlock):
                                    tool_name = block.name
                                    tool_input = block.input

                                    # Log tool use but don't yield to frontend
                                    tool_display = self._get_clean_tool_display(tool_name, tool_input)
                                    ui.info(tool_display, "Evaluation")

                        # Only yield text message (evaluation report content)
                        if content and content.strip():
                            text_message = Message(
                                id=str(uuid.uuid4()),
                                project_id=project_id,
                                role="assistant",
                                message_type="chat",
                                content=content.strip(),
                                metadata_json={
                                    "cli_type": "eval",
                                    "mode": "Evaluation",
                                },
                                session_id=session_id,
                                created_at=datetime.utcnow(),
                            )
                            yield text_message

                    # Handle UserMessage (tool results)
                    elif isinstance(message_obj, UserMessage) or "UserMessage" in str(type(message_obj)):
                        # Tool results - no need to show
                        pass

                    # Handle ResultMessage
                    elif (
                        isinstance(message_obj, ResultMessage)
                        or "ResultMessage" in str(type(message_obj))
                        or (hasattr(message_obj, "type") and getattr(message_obj, "type", None) == "result")
                    ):
                        ui.success(
                            f"Evaluation completed in {getattr(message_obj, 'duration_ms', 0)}ms",
                            "Evaluation",
                        )
                        # Don't yield result message to frontend, it's already complete
                        break

                    else:
                        ui.debug(f"Unknown message type: {type(message_obj)}", "Evaluation")

        except Exception as e:
            # Handle any errors during evaluation
            error_msg = f"Evaluation failed: {str(e)}"
            ui.error(error_msg, "Evaluation")

            # Yield error message
            error_message = Message(
                id=str(uuid.uuid4()),
                project_id=project_id,
                role="system",
                message_type="error",
                content=error_msg,
                metadata_json={
                    "cli_type": "eval",
                    "mode": "Evaluation",
                    "error": str(e),
                },
                session_id=session_id,
                created_at=datetime.utcnow(),
            )
            yield error_message