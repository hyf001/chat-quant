"""Unified CLI Manager implementation.

Moved from unified_manager.py to a dedicated module.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
import asyncio

from app.core.terminal_ui import ui
from app.core.websocket.manager import manager as ws_manager
from app.models.messages import Message
from app.common.types import AgentType
from app.services.cli.adapters import ClaudeAgentCLIAnalysis,ClaudeAgentFinAnalysis
from app.services.cli.base import BaseCLI

from sqlalchemy.orm import Session

@dataclass
class SessionContext:
    """Session context information for CLI execution"""
    session_id: str
    project_id: str
    cli: BaseCLI
    agent_type: AgentType
    instructions: list[str] = field(default_factory=list)
    model: Optional[str] = None
    images: Optional[List[Dict[str, Any]]] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_active_at: datetime = field(default_factory=datetime.utcnow)
    claude_session_id: Optional[str] = None


class UnifiedSessionManager:
    """Unified manager for all CLI implementations"""

    def __init__(self):
        self.session_context_map: dict[str, SessionContext] = {}
        self._cleanup_running: bool = False
        self._cleanup_task: Optional[asyncio.Task] = None
        self.session_timeout_minutes: int = 5  # 会话超时时间（分钟）
        self.cleanup_interval_minutes: int = 5  # 清理检查间隔（分钟）


    def get_session_context(self, session_id: str) -> Optional[SessionContext]:
        """Get session context by session_id"""
        return self.session_context_map.get(session_id)

    async def interrupt(self, cli_type: AgentType, session_id: str):
        """cancel the chat stream"""
        context = self.session_context_map.get(session_id)
        if context is None:
            return
        count = 100
        while count > 0:  
            if context and context.claude_session_id is not None:
                await context.cli.interrupt()
                break
            else:
                count -= 1
                await asyncio.sleep(1)
        if count <= 0:
            raise Exception("interrupt timeout: claude session id is none")

        
    async def _create_session(
        self,
        session_id: str,
        project_id: str,
        cli_type: AgentType,
        model: Optional[str] = None,
    ) -> SessionContext:
        """Create a new session context"""
        ui.info(f"Creating new session: {session_id}", "Session")

        # Create CLI adapter
        if cli_type == AgentType.ANALYIS:
            cli = ClaudeAgentCLIAnalysis()
        elif cli_type == AgentType.FIN_ANALYSIS:
            cli = ClaudeAgentFinAnalysis()
        else:
            raise ValueError(f"Unsupported agent type: {cli_type}")

        # Create session context
        context = SessionContext(
            session_id=session_id,
            project_id=project_id,
            cli=cli,
            agent_type=cli_type,
            model=model
        )

        # Store in map
        self.session_context_map[session_id] = context

        ui.success(f"Session created: {session_id}", "Session")
        return context

    async def execute_instruction(
        self,
        session_id: str,
        project_id: str,
        instruction: str,
        conversation_id: str,
        cli_type: AgentType,
        db : Session,
        fallback_enabled: bool = True,  # Kept for backward compatibility but not used
        images: List = [],
        model: Optional[str] = None,
        is_initial_prompt: bool = False,
        
    ) -> Dict[str, Any]:
        """Execute instruction with specified CLI with session state management"""

        # Check if session exists
        context = self.session_context_map.get(session_id)

        if context is None:
            # Session doesn't exist - create new session
            ui.info(f"Session not found, creating new session: {session_id}")
            context = await self._create_session(session_id, project_id, cli_type, model)

        # Add instruction to context history
        context.instructions.append(instruction)
        context.last_active_at = datetime.utcnow()

        # Update images if provided
        if images:
            context.images = images

        # Execute with the CLI
        return await self._execute_with_cli(
                cli=context.cli,
                project_id=project_id,
                session_id=session_id,
                conversation_id=conversation_id,
                db=db,
                instruction=instruction,
                images=images,
                model=model,
                is_initial_prompt=is_initial_prompt
            )

    async def _execute_with_cli(
        self,
        cli: BaseCLI,
        project_id: str,
        session_id: str,
        conversation_id: Optional[str],
        db: Any,
        instruction: str,
        images: Optional[List[Dict[str, Any]]],
        model: Optional[str] = None,
        is_initial_prompt: bool = False,
    ) -> Dict[str, Any]:
        """Execute instruction with a specific CLI"""

        ui.info(f"Starting {cli.cli_type.value} execution", "CLI")
        if model:
            ui.debug(f"Using model: {model}", "CLI")

        messages_collected: List[Message] = []
        has_changes = False
        has_error = False  # Track if any error occurred
        result_success: Optional[bool] = None  # Track result event success status

        # Log callback
        def log_callback(message: Dict) -> Any:
            self.session_context_map[session_id].claude_session_id = message.get("claude_session_id",None)
            

        async for message in cli.execute_with_streaming(
            instruction=instruction,
            project_id=project_id,
            session_id=session_id,
            claude_session_id=self.session_context_map[session_id].claude_session_id,
            log_callback=log_callback,
            images=images,
            model=model,
            is_initial_prompt=is_initial_prompt,
        ):
            # Check for error messages or result status
            if message.message_type == "error":
                has_error = True
                ui.error(f"CLI error detected: {message.content[:100]}", "CLI")

            # Check for result event (stored in metadata)
            if message.metadata_json:
                event_type = message.metadata_json.get("event_type")
                original_event = message.metadata_json.get("original_event", {})

                if event_type == "result" or original_event.get("type") == "result":
                    # Check result event for success/error status
                    is_error = original_event.get("is_error", False)
                    subtype = original_event.get("subtype", "")

                    # DEBUG: Log the complete result event structure
                    ui.info(f"🔍 Result event received:", "DEBUG")
                    ui.info(f"   Full event: {original_event}", "DEBUG")
                    ui.info(f"   is_error: {is_error}", "DEBUG")
                    ui.info(f"   subtype: '{subtype}'", "DEBUG")
                    ui.info(f"   has event.result: {'result' in original_event}", "DEBUG")
                    ui.info(f"   has event.status: {'status' in original_event}", "DEBUG")
                    ui.info(f"   has event.success: {'success' in original_event}", "DEBUG")

                    if is_error or subtype == "error":
                        has_error = True
                        result_success = False
                        ui.error(
                            f"Result: error (is_error={is_error}, subtype='{subtype}')",
                            "CLI",
                        )
                    elif subtype == "success":
                        result_success = True
                        ui.success(
                            f"Result: success (subtype='{subtype}')", "CLI"
                        )
                    else:
                        # Handle case where subtype is not "success" but execution was successful
                        ui.warning(
                            f"Result: no explicit success subtype (subtype='{subtype}', is_error={is_error})",
                            "CLI",
                        )
                        # If there's no error indication, assume success
                        if not is_error:
                            result_success = True
                            ui.success(
                                f"Result: assuming success (no error detected)", "CLI"
                            )

            # Save message to database
            message.project_id = project_id
            message.conversation_id = conversation_id
            db.add(message)
            db.commit()

            messages_collected.append(message)

            # Check if message should be hidden from UI
            should_hide = (
                message.metadata_json and message.metadata_json.get("hidden_from_ui", False)
            )

            # Send message via WebSocket only if not hidden
            if not should_hide:
                ws_message = {
                    "type": "message",
                    "data": {
                        "id": message.id,
                        "role": message.role,
                        "message_type": message.message_type,
                        "content": message.content,
                        "metadata_json": message.metadata_json,
                        "parent_message_id": getattr(message, "parent_message_id", None),
                        "session_id": message.session_id,
                        "conversation_id": conversation_id,
                        "created_at": message.created_at.isoformat(),
                    },
                    "timestamp": message.created_at.isoformat(),
                }
                try:
                    await ws_manager.send_message(project_id, ws_message)
                except Exception as e:
                    ui.error(f"WebSocket send failed: {e}", "Message")

            # Check if changes were made
            if message.metadata_json and "changes_made" in message.metadata_json:
                has_changes = True

        # Determine final success status
        # Check has_error to determine success
        ui.info(
            f"🔍 Final success determination: cli_type={cli.cli_type}, has_error={has_error}",
            "CLI",
        )

        success = not has_error
        ui.info(f"Using has_error logic: not {has_error} = {success}", "CLI")

        if success:
            ui.success(
                f"Streaming completed successfully. Total messages: {len(messages_collected)}",
                "CLI",
            )
        else:
            ui.error(
                f"Streaming completed with errors. Total messages: {len(messages_collected)}",
                "CLI",
            )

        return {
            "success": success,
            "cli_used": cli.cli_type.value,
            "has_changes": has_changes,
            "message": f"{'Successfully' if success else 'Failed to'} execute with {cli.cli_type.value}",
            "error": "Execution failed" if not success else None,
            "messages_count": len(messages_collected),
        }

        # End _execute_with_cli

    async def check_cli_status(
        self, cli_type: AgentType, selected_model: Optional[str] = None
    ) -> Dict[str, Any]:
        """Check status of a specific CLI"""
        return {
            "available": False,
            "configured": False,
            "error": f"CLI type not implemented",
        }

session_manager = UnifiedSessionManager()

__all__ = ["SessionContext", "session_manager"]
