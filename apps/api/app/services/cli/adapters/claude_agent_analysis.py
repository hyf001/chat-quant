"""Claude Agent provider implementation.

Moved from unified_manager.py to a dedicated adapter module.
"""
from __future__ import annotations

import os
from datetime import datetime
from typing import Any, Dict, Optional, override

from app.core.terminal_ui import ui
from claude_agent_sdk import ClaudeAgentOptions

from app.common.types import AgentType
from app.prompt import prompt_util
from app.core.config import settings

from ..base import MODEL_MAPPING, BaseCLI
from app.services.tools import sql_tools_server,report_tools_server,fin_sql_tools_server


class ClaudeAgentCLIAnalysis(BaseCLI):
    """Claude Agent Python SDK implementation"""

    def __init__(self):
        super().__init__(AgentType.ANALYIS)
        self.cli = None
        self.session_mapping: Dict[str, str] = {}

    async def check_availability(self) -> Dict[str, Any]:
        """Check if Claude Agent SDK is available"""
        
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
        

    @override
    def init_claude_option(self,
                       project_id: str,
                       claude_session_id: Optional[str],
                       model: Optional[str] = None) -> ClaudeAgentOptions:
        """connect and return Claude Agent SDK client"""
        # Load system prompt···
        try:
            project_path = os.path.join(settings.projects_root,project_id)
            system_prompt = prompt_util.getPrompt(AgentType.ANALYIS,
                                                  project_path = project_path,
                                                  current_date = datetime.now().strftime("%Y-%m-%d"),
                                                  python_home= settings.python_home)
            ui.debug(f"System prompt loaded: {len(system_prompt)} chars", "Claude Agent SDK")
        except Exception as e:
            ui.error(f"Failed to load system prompt: {e}", "Claude Agent SDK")
            system_prompt = (
                "You are Claude Agent, an AI coding assistant specialized in building modern web applications."
            )
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
            "Skill"
            ]
        # Get CLI-specific model name
        cli_model = "claude-sonnet-4-5-20250929" if model is None else MODEL_MAPPING.get(model,"claude-sonnet-4-5-20250929")
        options = ClaudeAgentOptions(
            system_prompt=system_prompt,
            allowed_tools=allowed_tools,
            mcp_servers={"sql":sql_tools_server,"fin-sql":fin_sql_tools_server,"report":report_tools_server},
            permission_mode="bypassPermissions",
            model=cli_model,
            continue_conversation=True,
            setting_sources=["user", "project", "local"],
            cwd=os.path.join(settings.projects_root,project_id),
            env={
                    "NODE_TLS_REJECT_UNAUTHORIZED": "0"
                }
        )
        if claude_session_id:
            options.resume = claude_session_id
            ui.info(f"Resuming session: {claude_session_id}", "Claude Agent SDK")
        return options


