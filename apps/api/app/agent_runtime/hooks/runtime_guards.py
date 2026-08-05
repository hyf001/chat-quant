from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from app.schema.agent_runtime import AgentExecutionCommand, RuntimeErrorCode


@dataclass(frozen=True)
class HookDecision:
    allowed: bool
    code: RuntimeErrorCode | None = None
    reason: str | None = None


class AgentRuntimeHooks:
    def pre_run(self, command: AgentExecutionCommand) -> HookDecision:
        if not command.project_dir.strip():
            return HookDecision(
                False,
                RuntimeErrorCode.TOOL_PERMISSION_DENIED,
                "project_dir is required",
            )
        project_dir = Path(command.project_dir)
        if not project_dir.is_absolute():
            return HookDecision(
                False,
                RuntimeErrorCode.TOOL_PERMISSION_DENIED,
                "project_dir must be an absolute path",
            )
        if not project_dir.exists() or not project_dir.is_dir():
            return HookDecision(
                False,
                RuntimeErrorCode.TOOL_PERMISSION_DENIED,
                "project_dir must be an existing directory",
            )
        return HookDecision(True)
