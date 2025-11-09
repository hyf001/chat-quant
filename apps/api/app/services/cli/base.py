"""
Base abstractions and shared utilities for CLI providers.

This module defines a precise, minimal adapter contract (BaseCLI) and common
helpers so that adding a new provider remains consistent and easy.
"""
from __future__ import annotations

import os
import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, AsyncGenerator, Callable, Dict, List, Optional

from claude_agent_sdk import ClaudeAgentOptions, ClaudeSDKClient

from app.models.messages import Message
from app.common.types import AgentType
import os
import uuid
from datetime import datetime
from typing import Any, AsyncGenerator, Callable, Dict, List, Optional

from app.core.terminal_ui import ui
from app.models.messages import Message
from claude_agent_sdk import ClaudeSDKClient

from app.common.types import AgentType
from app.core.config import settings
from claude_agent_sdk.types import (
                SystemMessage,
                AssistantMessage,
                UserMessage,
                ResultMessage,
            )
from claude_agent_sdk.types import (
                                        TextBlock,
                                        ToolUseBlock,
                                        ToolResultBlock,
                                    )
from .message_logger import MessageLogger

def get_project_root() -> str:
    """Return project root directory using relative path navigation.

    This function intentionally mirrors the logic previously embedded in
    unified_manager.py so imports remain stable after refactor.
    """
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    # base.py is in: app/services/cli/
    # Navigate: cli -> services -> app -> api -> apps -> project-root
    project_root = os.path.join(current_file_dir, "..", "..", "..", "..", "..")
    return os.path.abspath(project_root)


def get_display_path(file_path: str) -> str:
    """Convert absolute path to a shorter display path scoped to the project.

    - Strips the project root prefix when present
    - Compacts repo-specific prefixes (e.g., data/projects -> …/)
    """
    try:
        project_root = get_project_root()
        if file_path.startswith(project_root):
            display_path = file_path.replace(project_root + "/", "")
            return display_path.replace("data/projects/", "…/")
    except Exception:
        pass
    return file_path


# Model mapping from unified names to CLI-specific names
MODEL_MAPPING: Dict[str, str] = {
    "opus-4.1": "claude-opus-4-1-20250805",
    "sonnet-4": "claude-sonnet-4-20250514",
    "sonnet-4.5": "claude-sonnet-4-5-20250929",
    "opus-4": "claude-opus-4-20250514",
    "haiku-3.5": "claude-3-5-haiku-20241022",
    # Handle claude-prefixed model names
    "claude-sonnet-4": "claude-sonnet-4-20250514",
    "claude-sonnet-4-5": "claude-sonnet-4-5-20250929",
    "claude-opus-4.1": "claude-opus-4-1-20250805",
    "claude-opus-4": "claude-opus-4-20250514",
    "claude-haiku-3.5": "claude-3-5-haiku-20241022",
    # Support direct full model names
    "claude-opus-4-1-20250805": "claude-opus-4-1-20250805",
    "claude-sonnet-4-20250514": "claude-sonnet-4-20250514",
    "claude-sonnet-4-5-20250929": "claude-sonnet-4-5-20250929",
    "claude-opus-4-20250514": "claude-opus-4-20250514",
    "claude-3-5-haiku-20241022": "claude-3-5-haiku-20241022",
}

class BaseCLI(ABC):
    """Abstract adapter contract for CLI providers.

    Subclasses must implement availability checks, streaming execution, and
    session persistence. Common utilities (model mapping, content parsing,
    tool summaries) are provided here for reuse.
    """


    def __init__(self, cli_type: AgentType):
        self.cli_type = cli_type
        self.message_logger = MessageLogger(output_dir="logs/claude_messages")

    

    # ---- Mandatory adapter interface ------------------------------------
    @abstractmethod
    async def check_availability(self) -> Dict[str, Any]:
        """Return provider availability/configuration status.

        Expected keys in the returned dict used by the manager:
        - available: bool
        - configured: bool
        - models/default_models (optional): List[str]
        - error (optional): str
        """
    @abstractmethod
    def init_claude_option(self,
                       project_id: str,
                       claude_session_id: Optional[str],
                       model: Optional[str] = None)  -> ClaudeAgentOptions:
        """init claude options"""
        
    
    async def execute_with_streaming(
        self,
        instruction: str,
        project_id: str,
        log_callback: Callable[[dict], Any],
        session_id: Optional[str] = None,
        claude_session_id:Optional[str] = None,
        images: Optional[List[Dict[str, Any]]] = None,
        model: Optional[str] = None,
        is_initial_prompt: bool = False
    ) -> AsyncGenerator[Message, None]:
        """Execute instruction using Claude Agent Python SDK"""

        ui.info("Starting Claude Agent SDK execution", "Claude Agent SDK")
        ui.debug(f"Instruction: {instruction[:100]}...", "Claude Agent SDK")
        ui.debug(f"Project ID: {project_id}", "Claude Agent SDK")
        ui.debug(f"Session ID: {session_id}", "Claude Agent SDK")

         # 记录用户指令
        self.message_logger.log_user_instruction(instruction, images)


        # Process images if provided
        processed_instruction = instruction
        if images and len(images) > 0:
            ui.info(f"Processing {len(images)} images for Claude Agent", "Claude Agent SDK")
            ui.debug(f"Raw images data: {images}", "Claude Agent SDK")
            image_refs = []
            for i, img in enumerate(images):
                ui.debug(f"Processing image {i+1}: {img}", "Claude Agent SDK")
                # Handle both dict and object formats
                if hasattr(img, 'path'):
                    # ImageAttachment object with attributes
                    path = img.path
                    name = img.name
                elif isinstance(img, dict):
                    # Dictionary format
                    path = img.get('path')
                    name = img.get('name')
                else:
                    path = None
                    name = None

                ui.debug(f"Image {i+1} - path: {path}, name: {name}", "Claude Agent SDK")
                if path:
                    image_refs.append(f"Image #{i+1}: {path}")
                    ui.info(f"Added image reference: {path}", "Claude Agent SDK")
                elif name:
                    image_refs.append(f"Image #{i+1}: {name}")
                    ui.info(f"Added image reference by name: {name}", "Claude Agent SDK")

            if image_refs:
                processed_instruction = f"{instruction}\n\nUploaded files:\n{chr(10).join(image_refs)}"
                ui.success(f"Enhanced instruction with {len(image_refs)} image references", "Claude Agent SDK")
                ui.debug(f"Final instruction: {processed_instruction[:200]}...", "Claude Agent SDK")
            else:
                ui.warning("Images provided but no valid paths/names found", "Claude Agent SDK")
        else:
            ui.debug("No images provided to Claude Agent", "Claude Agent SDK")
        cli_model = "claude-sonnet-4-5-20250929" if model is None else MODEL_MAPPING.get(model,"claude-sonnet-4-5-20250929")
        project_path = os.path.join(settings.projects_root,project_id)
        options = self.init_claude_option(project_id=project_id,
                                            model=model,
                                            claude_session_id=claude_session_id)
        async with ClaudeSDKClient(options=options) as client:
            self.cli = client
            
            await self.cli.query(processed_instruction)
            
            async for message_obj in self.cli.receive_messages():
                # Handle SystemMessage for session_id extraction
                if (isinstance(message_obj, SystemMessage)or "SystemMessage" in str(type(message_obj))):
                    # Log message
                    self.message_logger.log_message(message_obj, "SystemMessage")

                    # Extract session_id if available
                    if (hasattr(message_obj, "subtype") and message_obj.subtype == 'init'):
                        claude_session_id = message_obj.data.get('session_id')
                        log_callback({"claude_session_id":claude_session_id})
                        # 设置 message_logger 的 session_id
                        self.message_logger.set_session_id(claude_session_id)
                    # Send init message (hidden from UI)
                    init_message = Message(
                        id=str(uuid.uuid4()),
                        project_id=project_id,
                        role="system",
                        message_type="system",
                        content=f"Claude Agent SDK initialized (Model: {cli_model})",
                        metadata_json={
                            "cli_type": self.cli_type.value,
                            "mode": "SDK",
                            "model": cli_model,
                            "session_id": getattr(
                                message_obj, "session_id", None
                            ),
                            "hidden_from_ui": True,
                        },
                        session_id=session_id,
                        created_at=datetime.utcnow(),
                    )
                    yield init_message

                # Handle AssistantMessage (complete messages)
                elif (
                    isinstance(message_obj, AssistantMessage)
                    or "AssistantMessage" in str(type(message_obj))
                ):
                    # Log message
                    self.message_logger.log_message(message_obj, "AssistantMessage")

                    content = ""
                    # Process content - AssistantMessage has content: list[ContentBlock]
                    if hasattr(message_obj, "content") and isinstance(
                        message_obj.content, list
                    ):
                        for block in message_obj.content:
                            if isinstance(block, TextBlock):
                                # TextBlock has 'text' attribute
                                content += block.text
                            elif isinstance(block, ToolUseBlock):
                                # ToolUseBlock has 'id', 'name', 'input' attributes
                                tool_name = block.name
                                tool_input = block.input
                                tool_id = block.id
                                summary = self._create_tool_summary(
                                    tool_name, tool_input
                                )

                                # Yield tool use message immediately
                                tool_message = Message(
                                    id=str(uuid.uuid4()),
                                    project_id=project_path,
                                    role="assistant",
                                    message_type="tool_use",
                                    content=summary,
                                    metadata_json={
                                        "cli_type": self.cli_type.value,
                                        "mode": "SDK",
                                        "tool_name": tool_name,
                                        "tool_input": tool_input,
                                        "tool_id": tool_id,
                                    },
                                    session_id=session_id,
                                    created_at=datetime.utcnow(),
                                )
                                # Display clean tool usage like Claude Agent
                                tool_display = self._get_clean_tool_display(
                                    tool_name, tool_input
                                )
                                ui.info(tool_display, "")
                                yield tool_message
                            elif isinstance(block, ToolResultBlock):
                                # Handle tool result blocks if needed
                                pass

                    # Yield complete assistant text message if there's text content
                    if content and content.strip():
                        text_message = Message(
                            id=str(uuid.uuid4()),
                            project_id=project_path,
                            role="assistant",
                            message_type="chat",
                            content=content.strip(),
                            metadata_json={
                                "cli_type": self.cli_type.value,
                                "mode": "SDK",
                            },
                            session_id=session_id,
                            created_at=datetime.utcnow(),
                        )
                        yield text_message

                # Handle UserMessage (tool results, etc.)
                elif (
                    isinstance(message_obj, UserMessage)
                    or "UserMessage" in str(type(message_obj))
                ):
                    # Log message
                    self.message_logger.log_message(message_obj, "UserMessage")

                    # UserMessage has content: str according to types.py
                    # UserMessages are typically tool results - we don't need to show them
                    pass

                # Handle ResultMessage (final session completion)
                elif (
                    isinstance(message_obj, ResultMessage)
                    or "ResultMessage" in str(type(message_obj))
                    or (
                        hasattr(message_obj, "type")
                        and getattr(message_obj, "type", None) == "result"
                    )
                ):
                    # Log message
                    self.message_logger.log_message(message_obj, "ResultMessage")

                    ui.success(
                        f"Session completed in {getattr(message_obj, 'duration_ms', 0)}ms",
                        "Claude Agent SDK",
                    )

                    # Export to JSON
                    try:
                        summary = self.message_logger.get_summary()
                        ui.info(f"Preparing to export {summary['total']} messages", "Message Logger")

                        if summary['total'] > 0:
                            # 导出 JSON
                            json_path = self.message_logger.export_to_json()
                            ui.success(f"JSON exported to: {json_path}", "Message Logger")
                            ui.info(f"Total messages: {summary['total']}", "Message Logger")
                            ui.info(f"By type: {summary['by_type']}", "Message Logger")
                        else:
                            ui.warning("No messages to export", "Message Logger")
                    except Exception as e:
                        import traceback
                        ui.error(f"Failed to export messages: {e}", "Message Logger")
                        ui.debug(f"Traceback: {traceback.format_exc()}", "Message Logger")


                    # Create internal result message (hidden from UI)
                    result_message = Message(
                        id=str(uuid.uuid4()),
                        project_id=project_path,
                        role="system",
                        message_type="result",
                        content=(
                            f"Session completed in {getattr(message_obj, 'duration_ms', 0)}ms"
                        ),
                        metadata_json={
                            "cli_type": self.cli_type.value,
                            "mode": "SDK",
                            "duration_ms": getattr(
                                message_obj, "duration_ms", 0
                            ),
                            "duration_api_ms": getattr(
                                message_obj, "duration_api_ms", 0
                            ),
                            "total_cost_usd": getattr(
                                message_obj, "total_cost_usd", 0
                            ),
                            "usage": str(getattr(message_obj, "usage", None)),
                            "num_turns": getattr(message_obj, "num_turns", 0),
                            "is_error": getattr(message_obj, "is_error", False),
                            "subtype": getattr(message_obj, "subtype", None),
                            "session_id": getattr(
                                message_obj, "session_id", None
                            ),
                            "hidden_from_ui": True,  # Don't show to user
                        },
                        session_id=session_id,
                        created_at=datetime.utcnow(),
                    )
                    yield result_message
                    break

                # Handle unknown message types
                else:
                    ui.debug(
                        f"Unknown message type: {type(message_obj)}",
                        "Claude Agent SDK",
                    )

    
    async def interrupt(self):
        """interrupt chat"""   
        if self.cli is not None:
            await self.cli.interrupt()


    def get_supported_models(self) -> List[str]:
        cli_models = MODEL_MAPPING.get("agent", {})
        return list(cli_models.keys()) + list(cli_models.values())

    def is_model_supported(self, model: str) -> bool:
        return (
            model in self.get_supported_models()
            or model in MODEL_MAPPING.get("agent", {}).values()
        )

    def parse_message_data(self, data: Dict[str, Any], project_id: str, session_id: str) -> Message:
        """Normalize provider-specific message payload to our `Message`."""
        return Message(
            id=str(uuid.uuid4()),
            project_id=project_id,
            role=self._normalize_role(data.get("role", "assistant")),
            message_type="chat",
            content=self._extract_content(data),
            metadata_json={
                **data,
                "cli_type": self.cli_type.value,
                "original_format": data,
            },
            session_id=session_id,
            created_at=datetime.utcnow(),
        )

    def _normalize_role(self, role: str) -> str:
        role_mapping = {
            "model": "assistant",
            "ai": "assistant",
            "human": "user",
            "bot": "assistant",
        }
        return role_mapping.get(role.lower(), role.lower())

    def _extract_content(self, data: Dict[str, Any]) -> str:
        """Extract best-effort text content from various provider formats."""
        # Claude content array
        if "content" in data and isinstance(data["content"], list):
            content = ""
            for item in data["content"]:
                if item.get("type") == "text":
                    content += item.get("text", "")
                elif item.get("type") == "tool_use":
                    tool_name = item.get("name", "Unknown")
                    tool_input = item.get("input", {})
                    summary = self._create_tool_summary(tool_name, tool_input)
                    content += f"{summary}\n"
            return content

        # Simple text
        elif "content" in data:
            return str(data["content"])

        # Gemini parts
        elif "parts" in data:
            content = ""
            for part in data["parts"]:
                if "text" in part:
                    content += part.get("text", "")
                elif "functionCall" in part:
                    func_call = part["functionCall"]
                    tool_name = func_call.get("name", "Unknown")
                    tool_input = func_call.get("args", {})
                    summary = self._create_tool_summary(tool_name, tool_input)
                    content += f"{summary}\n"
            return content

        # OpenAI/Codex choices
        elif "choices" in data and data["choices"]:
            choice = data["choices"][0]
            if "message" in choice:
                return choice["message"].get("content", "")
            elif "text" in choice:
                return choice.get("text", "")

        # Direct text fields
        elif "text" in data:
            return str(data["text"])
        elif "message" in data:
            if isinstance(data["message"], dict):
                return self._extract_content(data["message"])
            return str(data["message"])

        # Generic response field
        elif "response" in data:
            return str(data["response"])

        # Delta streaming
        elif "delta" in data and "content" in data["delta"]:
            return str(data["delta"]["content"])

        # Fallback
        else:
            return str(data)

    def _normalize_tool_name(self, tool_name: str) -> str:
        """Normalize tool names across providers to a unified label."""
        key = (tool_name or "").strip()
        key_lower = key.replace(" ", "").lower()
        tool_mapping = {
            # File operations
            "read_file": "Read",
            "read": "Read",
            "write_file": "Write",
            "write": "Write",
            "edit_file": "Edit",
            "replace": "Edit",
            "edit": "Edit",
            "delete": "Delete",
            # Qwen/Gemini variants (CamelCase / spaced)
            "readfile": "Read",
            "readfolder": "LS",
            "readmanyfiles": "Read",
            "writefile": "Write",
            "findfiles": "Glob",
            "savememory": "SaveMemory",
            "save memory": "SaveMemory",
            "searchtext": "Grep",
            # Terminal operations
            "shell": "Bash",
            "run_terminal_command": "Bash",
            # Search operations
            "search_file_content": "Grep",
            "codebase_search": "Grep",
            "grep": "Grep",
            "find_files": "Glob",
            "glob": "Glob",
            "list_directory": "LS",
            "list_dir": "LS",
            "ls": "LS",
            "semSearch": "SemSearch",
            # Web operations
            "google_web_search": "WebSearch",
            "web_search": "WebSearch",
            "googlesearch": "WebSearch",
            "web_fetch": "WebFetch",
            "fetch": "WebFetch",
            # Task/Memory operations
            "save_memory": "SaveMemory",
            # Codex operations
            "exec_command": "Bash",
            "apply_patch": "Edit",
            "mcp_tool_call": "MCPTool",
            # Generic simple names
            "search": "Grep",
            # sql execute tool
            "mcp__sql__download_sql_result": "SqlDownload", 
            "mcp__sql__preview_sql_result": "SqlPreview",
            "mcp__sql__create_table_tool": "SqlCreate",
            "mcp__fin-sql__download_sql_result": "SqlDownload",
            "mcp__fin-sql__preview_sql_result": "SqlPreview",
            # report tool
            "mcp__report__download_report_data": "ReportDownload",
            "mcp__report__preview_report_data": "ReportPreview",
        }
        return tool_mapping.get(tool_name, tool_mapping.get(key_lower, key))

    def _get_clean_tool_display(self, tool_name: str, tool_input: Dict[str, Any]) -> str:
        """Return a concise, Claude-like tool usage display line."""
        normalized_name = self._normalize_tool_name(tool_name)

        if normalized_name == "Read":
            file_path = (
                tool_input.get("file_path")
                or tool_input.get("path")
                or tool_input.get("file", "")
            )
            if file_path:
                filename = file_path.split("/")[-1]
                return f"Reading {filename}"
            return "Reading file"
        elif normalized_name == "Write":
            file_path = (
                tool_input.get("file_path")
                or tool_input.get("path")
                or tool_input.get("file", "")
            )
            if file_path:
                filename = file_path.split("/")[-1]
                return f"Writing {filename}"
            return "Writing file"
        elif normalized_name == "Edit":
            file_path = (
                tool_input.get("file_path")
                or tool_input.get("path")
                or tool_input.get("file", "")
            )
            if file_path:
                filename = file_path.split("/")[-1]
                return f"Editing {filename}"
            return "Editing file"
        elif normalized_name == "Bash":
            command = (
                tool_input.get("command")
                or tool_input.get("cmd")
                or tool_input.get("script", "")
            )
            if command:
                cmd_display = command.split()[0] if command.split() else command
                return f"Running {cmd_display}"
            return "Running command"
        elif normalized_name == "LS":
            return "Listing directory"
        elif normalized_name == "TodoWrite":
            return "Planning next steps"
        elif normalized_name == "WebSearch":
            query = tool_input.get("query", "")
            if query:
                return f"Searching: {query[:50]}..."
            return "Web search"
        elif normalized_name == "WebFetch":
            url = tool_input.get("url", "")
            if url:
                domain = (
                    url.split("//")[-1].split("/")[0]
                    if "//" in url
                    else url.split("/")[0]
                )
                return f"Fetching from {domain}"
            return "Fetching web content"
        elif normalized_name.startswith("Sql"):
            return f"Executing SQL {tool_input.get("sql","")}"
        else:
            return f"Using {tool_name}"

    def _create_tool_summary(self, tool_name: str, tool_input: Dict[str, Any]) -> str:
        """Create a visual markdown summary for tool usage.

        NOTE: Special-cases Codex `apply_patch` to render one-line summaries per
        file similar to Claude Code.
        """
        # Handle apply_patch BEFORE normalization to avoid confusion with Edit
        if tool_name == "apply_patch":
            changes = tool_input.get("changes", {})
            if isinstance(changes, dict) and changes:
                if len(changes) == 1:
                    path, change = next(iter(changes.items()))
                    filename = str(path).split("/")[-1]
                    if isinstance(change, dict):
                        if "add" in change:
                            return f"**Write** `{filename}`"
                        elif "delete" in change:
                            return f"**Delete** `{filename}`"
                        elif "update" in change:
                            upd = change.get("update") or {}
                            move_path = upd.get("move_path")
                            if move_path:
                                new_filename = move_path.split("/")[-1]
                                return f"**Rename** `{filename}` → `{new_filename}`"
                            else:
                                return f"**Edit** `{filename}`"
                        else:
                            return f"**Edit** `{filename}`"
                    else:
                        return f"**Edit** `{filename}`"
                else:
                    file_summaries: List[str] = []
                    for raw_path, change in list(changes.items())[:3]:  # max 3 files
                        path = str(raw_path)
                        filename = path.split("/")[-1]
                        if isinstance(change, dict):
                            if "add" in change:
                                file_summaries.append(f"• **Write** `{filename}`")
                            elif "delete" in change:
                                file_summaries.append(f"• **Delete** `{filename}`")
                            elif "update" in change:
                                upd = change.get("update") or {}
                                move_path = upd.get("move_path")
                                if move_path:
                                    new_filename = move_path.split("/")[-1]
                                    file_summaries.append(
                                        f"• **Rename** `{filename}` → `{new_filename}`"
                                    )
                                else:
                                    file_summaries.append(f"• **Edit** `{filename}`")
                            else:
                                file_summaries.append(f"• **Edit** `{filename}`")
                        else:
                            file_summaries.append(f"• **Edit** `{filename}`")

                    result = "\n".join(file_summaries)
                    if len(changes) > 3:
                        result += f"\n• ... +{len(changes) - 3} more files"
                    return result
            return "**ApplyPatch** `files`"

        # Normalize name after handling apply_patch
        normalized_name = self._normalize_tool_name(tool_name)

        if normalized_name == "Edit":
            file_path = (
                tool_input.get("file_path")
                or tool_input.get("path")
                or tool_input.get("file", "")
            )
            if file_path:
                display_path = get_display_path(file_path)
                if len(display_path) > 40:
                    display_path = "…/" + "/".join(display_path.split("/")[-2:])
                return f"📝 **Edit** `{display_path}`"
            return "📝 **Edit** `file`"
        elif normalized_name == "Read":
            file_path = (
                tool_input.get("file_path")
                or tool_input.get("path")
                or tool_input.get("file", "")
            )
            if file_path:
                display_path = get_display_path(file_path)
                if len(display_path) > 40:
                    display_path = "…/" + "/".join(display_path.split("/")[-2:])
                return f"📖 **Read** `{display_path}`"
            return "📖 **Read** `file`"
        elif normalized_name == "Bash":
            command = (
                tool_input.get("command")
                or tool_input.get("cmd")
                or tool_input.get("script", "")
            )
            if command:
                display_cmd = command[:40] + "..." if len(command) > 40 else command
                return f"**Bash** `{display_cmd}`"
            return "**Bash** `command`"
        elif normalized_name == "TodoWrite":
            return "`Planning for next moves...`"
        elif normalized_name == "SaveMemory":
            fact = tool_input.get("fact", "")
            if fact:
                return f"**SaveMemory** `{fact[:40]}{'...' if len(fact) > 40 else ''}`"
            return "**SaveMemory** `storing information`"
        elif normalized_name == "Grep":
            pattern = (
                tool_input.get("pattern")
                or tool_input.get("query")
                or tool_input.get("search", "")
            )
            path = (
                tool_input.get("path")
                or tool_input.get("file")
                or tool_input.get("directory", "")
            )
            if pattern:
                if path:
                    display_path = get_display_path(path)
                    return f"🔍 **Search** `{pattern}` in `{display_path}`"
                return f"🔍 **Search** `{pattern}`"
            return "🔍 **Search** `pattern`"
        elif normalized_name == "Glob":
            if tool_name == "find_files":
                name = tool_input.get("name", "")
                if name:
                    return f"📓 **Glob** `{name}`"
                return "📓 **Glob** `finding files`"
            pattern = tool_input.get("pattern", "") or tool_input.get(
                "globPattern", ""
            )
            if pattern:
                return f"🔎 **Glob** `{pattern}`"
            return "🔎 **Glob** `pattern`"
        elif normalized_name == "Write":
            file_path = (
                tool_input.get("file_path")
                or tool_input.get("path")
                or tool_input.get("file", "")
            )
            if file_path:
                display_path = get_display_path(file_path)
                if len(display_path) > 40:
                    display_path = "…/" + "/".join(display_path.split("/")[-2:])
                return f"✏️ **Write** `{display_path}`"
            return "✏️ **Write** `file`"
        elif normalized_name == "MultiEdit":
            file_path = (
                tool_input.get("file_path")
                or tool_input.get("path")
                or tool_input.get("file", "")
            )
            if file_path:
                display_path = get_display_path(file_path)
                if len(display_path) > 40:
                    display_path = "…/" + "/".join(display_path.split("/")[-2:])
                return f"🔧 **MultiEdit** `{display_path}`"
            return "🔧 **MultiEdit** `file`"
        elif normalized_name == "LS":
            path = (
                tool_input.get("path")
                or tool_input.get("directory")
                or tool_input.get("dir", "")
            )
            if path:
                display_path = get_display_path(path)
                if len(display_path) > 40:
                    display_path = "…/" + display_path[-37:]
                return f"📁 **LS** `{display_path}`"
            return "📁 **LS** `directory`"
        elif normalized_name == "WebFetch":
            url = tool_input.get("url", "")
            if url:
                domain = (
                    url.split("//")[-1].split("/")[0]
                    if "//" in url
                    else url.split("/")[0]
                )
                return f"🌐 **WebFetch** [{domain}]({url})"
            return "🌐 **WebFetch** `url`"
        elif normalized_name == "WebSearch":
            query = tool_input.get("query") or tool_input.get("search_query", "")
            query = tool_input.get("query", "")
            if query:
                short_query = query[:40] + "..." if len(query) > 40 else query
                return f"🌐 **WebSearch** `{short_query}`"
            return "🌐 **WebSearch** `query`"
        elif normalized_name == "Task":
            description = tool_input.get("description", "")
            subagent_type = tool_input.get("subagent_type", "")
            if description and subagent_type:
                return (
                    f"🤖 **Task** `{subagent_type}`\n> "
                    f"{description[:50]}{'...' if len(description) > 50 else ''}"
                )
            elif description:
                return f"🤖 **Task** `{description[:40]}{'...' if len(description) > 40 else ''}`"
            return "🤖 **Task** `subtask`"
        elif normalized_name == "ExitPlanMode":
            return "✅ **ExitPlanMode** `planning complete`"
        elif normalized_name == "NotebookEdit":
            notebook_path = tool_input.get("notebook_path", "")
            if notebook_path:
                filename = notebook_path.split("/")[-1]
                return f"📓 **NotebookEdit** `{filename}`"
            return "📓 **NotebookEdit** `notebook`"
        elif normalized_name == "MCPTool" or tool_name == "mcp_tool_call":
            server = tool_input.get("server", "")
            tool_name_inner = tool_input.get("tool", "")
            if server and tool_name_inner:
                return f"🔧 **MCP** `{server}.{tool_name_inner}`"
            return "🔧 **MCP** `tool call`"
        elif tool_name == "exec_command":
            command = tool_input.get("command", "")
            if command:
                display_cmd = command[:40] + "..." if len(command) > 40 else command
                return f"⚡ **Exec** `{display_cmd}`"
            return "⚡ **Exec** `command`"
        elif normalized_name.startswith("Sql"):
            sql = tool_input.get("sql","")
            return f"👓 **{normalized_name}** `{sql[:40] + "..." if len(sql) > 40 else sql}`"
        elif normalized_name.startswith("Report"):
            report_id = tool_input.get("id","")
            return f"📈 **{normalized_name}** id={report_id}"
        else:
            return f"**{tool_name}** `executing...`"
