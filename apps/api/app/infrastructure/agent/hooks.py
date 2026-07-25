from __future__ import annotations

from dataclasses import dataclass

from app.infrastructure.agent.bash_command_policy import (
    BashCommand,
    CommandContext,
    validate_bash_command,
)
from app.schemas.contracts.agent_runtime import AgentTurnCommand, RuntimeErrorCode


@dataclass(frozen=True)
class HookDecision:
    allowed: bool
    code: RuntimeErrorCode | None = None
    reason: str | None = None


class AgentRuntimeHooks:
    def pre_run(self, command: AgentTurnCommand) -> HookDecision:
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

    def pre_tool_use(
        self,
        event: dict[str, object],
        allowed_commands: tuple[BashCommand, ...],
        context: CommandContext,
    ) -> HookDecision:
        tool_name = str(event.get("name") or "")
        if tool_name != "Bash":
            return HookDecision(
                False,
                RuntimeErrorCode.TOOL_PERMISSION_DENIED,
                "only Bash is enabled",
            )

        bash_command = str(event.get("command") or "")
        decision = validate_bash_command(bash_command, allowed_commands, context)
        if decision.allowed:
            return HookDecision(True)
        return HookDecision(False, decision.code, decision.reason)
