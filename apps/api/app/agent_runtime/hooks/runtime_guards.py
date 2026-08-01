from __future__ import annotations

from dataclasses import dataclass

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
        if ".." in command.project_dir.split("/"):
            return HookDecision(
                False,
                RuntimeErrorCode.TOOL_PERMISSION_DENIED,
                "project_dir cannot contain parent traversal",
            )
        return HookDecision(True)
