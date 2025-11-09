"""Claude Agent provider implementation.

Moved from unified_manager.py to a dedicated adapter module.
"""
from __future__ import annotations

import asyncio
import os
import uuid
from datetime import datetime
from typing import Any, AsyncGenerator, Callable, Dict, List, Optional

from app.core.terminal_ui import ui
from app.models.messages import Message
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions

from ..base import BaseCLI, CLIType


class ClaudeAgentCLI(BaseCLI):
    """Claude Agent Python SDK implementation"""

    def __init__(self):
        super().__init__(CLIType.AGENT)
        self.session_mapping: Dict[str, str] = {}

    async def check_availability(self) -> Dict[str, Any]:
        """Check if Claude Agent SDK is available"""
        try:
            import claude_agent_sdk
            return {
                "available": True,
                "configured": True,
                "mode": "SDK",
                "models": self.get_supported_models(),
                "default_models": [
                    "claude-sonnet-4-5-20250929",
                    "claude-opus-4-1-20250805",
                ],
            }
        except ImportError:
            # Return as configured for development environment
            # Even if SDK is not installed, we treat it as configured
            return {
                "available": True,
                "configured": True,  # Changed to True for dev environment
                "mode": "SDK (Development Mode)",
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

    async def execute_with_streaming(
        self,
        instruction: str,
        project_path: str,
        session_id: Optional[str] = None,
        log_callback: Optional[Callable[[str], Any]] = None,
        images: Optional[List[Dict[str, Any]]] = None,
        model: Optional[str] = None,
        is_initial_prompt: bool = False,
    ) -> AsyncGenerator[Message, None]:
        """Execute instruction using Claude Agent Python SDK"""

        ui.info("Starting Claude Agent SDK execution", "Claude Agent SDK")
        ui.debug(f"Instruction: {instruction[:100]}...", "Claude Agent SDK")
        ui.debug(f"Project path: {project_path}", "Claude Agent SDK")
        ui.debug(f"Session ID: {session_id}", "Claude Agent SDK")

        if log_callback:
            await log_callback("Starting execution...")

        # Load system prompt
        try:
            from app.services.claude_act import get_system_prompt

            system_prompt = get_system_prompt()
            ui.debug(f"System prompt loaded: {len(system_prompt)} chars", "Claude Agent SDK")
        except Exception as e:
            ui.error(f"Failed to load system prompt: {e}", "Claude Agent SDK")
            system_prompt = (
                "You are Claude Agent, an AI coding assistant specialized in building modern web applications."
            )

        # Get CLI-specific model name
        cli_model = self._get_cli_model_name(model) or "claude-sonnet-4-5-20250929"

        # Add project directory structure for initial prompts
        if is_initial_prompt:
            project_structure_info = """
<initial_context>
## Project Directory Structure (node_modules are already installed)
.eslintrc.json
.gitignore
next.config.mjs
next-env.d.ts
package.json
postcss.config.mjs
README.md
tailwind.config.ts
tsconfig.json
.env
src/app/favicon.ico
src/app/globals.css
src/app/layout.tsx
src/app/page.tsx
public/
node_modules/
</initial_context>"""
            instruction = instruction + project_structure_info
            ui.info(
                f"Added project structure info to initial prompt", "Claude Agent SDK"
            )

        # Configure tools based on initial prompt status
        if is_initial_prompt:
            # For initial prompts: use disallowed_tools to explicitly block TodoWrite
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
            ]
            disallowed_tools = ["TodoWrite"]

            ui.info(
                f"TodoWrite tool EXCLUDED via disallowed_tools (is_initial_prompt: {is_initial_prompt})",
                "Claude Agent SDK",
            )
            ui.debug(f"Allowed tools: {allowed_tools}", "Claude Agent SDK")
            ui.debug(f"Disallowed tools: {disallowed_tools}", "Claude Agent SDK")

            # Configure Claude Agent options with disallowed_tools
            options = ClaudeAgentOptions(
                system_prompt=system_prompt,
                allowed_tools=allowed_tools,
                disallowed_tools=disallowed_tools,
                permission_mode="bypassPermissions",
                model=cli_model,
                continue_conversation=True,
                setting_sources=["user", "project", "local"]
            )
        else:
            # For non-initial prompts: include TodoWrite in allowed tools
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
            ]

            ui.info(
                f"TodoWrite tool INCLUDED (is_initial_prompt: {is_initial_prompt})",
                "Claude Agent SDK",
            )
            ui.debug(f"Allowed tools: {allowed_tools}", "Claude Agent SDK")

            # Configure Claude Agent options without disallowed_tools
            options = ClaudeAgentOptions(
                system_prompt=system_prompt,
                allowed_tools=allowed_tools,
                permission_mode="bypassPermissions",
                model=cli_model,
                continue_conversation=True,
                setting_sources=["user", "project", "local"]
            )

        ui.info(f"Using model: {cli_model}", "Claude Agent SDK")
        ui.debug(f"Project path: {project_path}", "Claude Agent SDK")
        ui.debug(f"Instruction: {instruction[:100]}...", "Claude Agent SDK")
        ui.debug(f"Images provided: {len(images) if images else 0}", "Claude Agent SDK")

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
                processed_instruction = f"{instruction}\n\nUploaded images:\n{chr(10).join(image_refs)}\n\nPlease use the Read tool to view these image files and analyze their content."
                ui.success(f"Enhanced instruction with {len(image_refs)} image references", "Claude Agent SDK")
                ui.debug(f"Final instruction: {processed_instruction[:200]}...", "Claude Agent SDK")
            else:
                ui.warning("Images provided but no valid paths/names found", "Claude Agent SDK")
        else:
            ui.debug("No images provided to Claude Agent", "Claude Agent SDK")

        try:
            # Change to project directory
            original_cwd = os.getcwd()
            os.chdir(project_path)

            # Get project ID for session management
            project_id = (
                project_path.split("/")[-1] if "/" in project_path else project_path
            )
            existing_session_id = await self.get_session_id(project_id)

            # Update options with resume session if available
            if existing_session_id:
                options.resumeSessionId = existing_session_id
                ui.info(f"Resuming session: {existing_session_id}", "Claude Agent SDK")

            try:
                async with ClaudeSDKClient(options=options) as client:
                    # Send initial query with processed instruction (including image references)
                    await client.query(processed_instruction)

                    # Stream responses and extract session_id
                    claude_session_id = None

                    async for message_obj in client.receive_messages():
                        # Import SDK types for isinstance checks
                        try:
                            from anthropic.claude_agent.types import (
                                SystemMessage,
                                AssistantMessage,
                                UserMessage,
                                ResultMessage,
                            )
                        except ImportError:
                            try:
                                from claude_agent_sdk.types import (
                                    SystemMessage,
                                    AssistantMessage,
                                    UserMessage,
                                    ResultMessage,
                                )
                            except ImportError:
                                # Fallback - check type name strings
                                SystemMessage = type(None)
                                AssistantMessage = type(None)
                                UserMessage = type(None)
                                ResultMessage = type(None)

                        # Handle SystemMessage for session_id extraction
                        if (
                            isinstance(message_obj, SystemMessage)
                            or "SystemMessage" in str(type(message_obj))
                        ):
                            # Extract session_id if available
                            if (
                                hasattr(message_obj, "session_id")
                                and message_obj.session_id
                            ):
                                claude_session_id = message_obj.session_id
                                await self.set_session_id(
                                    project_id, claude_session_id
                                )

                            # Send init message (hidden from UI)
                            init_message = Message(
                                id=str(uuid.uuid4()),
                                project_id=project_path,
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
                            content = ""

                            # Process content - AssistantMessage has content: list[ContentBlock]
                            if hasattr(message_obj, "content") and isinstance(
                                message_obj.content, list
                            ):
                                for block in message_obj.content:
                                    # Import block types for comparison
                                    from claude_agent_sdk.types import (
                                        TextBlock,
                                        ToolUseBlock,
                                        ToolResultBlock,
                                    )

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
                            ui.success(
                                f"Session completed in {getattr(message_obj, 'duration_ms', 0)}ms",
                                "Claude Agent SDK",
                            )

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

            finally:
                # Restore original working directory
                os.chdir(original_cwd)

        except Exception as e:
            ui.error(f"Exception occurred: {str(e)}", "Claude Agent SDK")
            if log_callback:
                await log_callback(f"Claude Agent SDK Exception: {str(e)}")
            raise

    async def get_session_id(self, project_id: str) -> Optional[str]:
        """Get current session ID for project from database"""
        try:
            # Try to get from database if available (we'll need to pass db session)
            return self.session_mapping.get(project_id)
        except Exception as e:
            ui.warning(f"Failed to get session ID from DB: {e}", "Claude Agent SDK")
            return self.session_mapping.get(project_id)

    async def set_session_id(self, project_id: str, session_id: str) -> None:
        """Set session ID for project in database and memory"""
        try:
            # Store in memory as fallback
            self.session_mapping[project_id] = session_id
            ui.debug(
                f"Session ID stored for project {project_id}", "Claude Agent SDK"
            )
        except Exception as e:
            ui.warning(f"Failed to save session ID: {e}", "Claude Agent SDK")
            # Fallback to memory storage
            self.session_mapping[project_id] = session_id