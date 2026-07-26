from __future__ import annotations

from dataclasses import dataclass

from app.schemas.contracts.agent_runtime import AgentExecutionCommand, RuntimeErrorCode


@dataclass(frozen=True)
class HookDecision:
    allowed: bool
    code: RuntimeErrorCode | None = None
    reason: str | None = None


class AgentRuntimeHooks:
    def pre_run(self, command: AgentExecutionCommand) -> HookDecision:
        if not command.working_dir.strip():
            return HookDecision(
                False,
                RuntimeErrorCode.TOOL_PERMISSION_DENIED,
                "working_dir is required",
            )
        if ".." in command.working_dir.split("/"):
            return HookDecision(
                False,
                RuntimeErrorCode.TOOL_PERMISSION_DENIED,
                "working_dir cannot contain parent traversal",
            )
        return HookDecision(True)
