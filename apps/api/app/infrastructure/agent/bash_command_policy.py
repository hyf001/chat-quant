from __future__ import annotations

import shlex
from dataclasses import dataclass

from app.schemas.contracts.agent_runtime import AgentScenario, RuntimeErrorCode


@dataclass(frozen=True)
class BashCommand:
    name: str
    enabled: bool
    modules: tuple[str, ...]
    description: str


@dataclass(frozen=True)
class BashCommandPolicy:
    policy_id: str
    version: int
    commands: tuple[BashCommand, ...]

    def enabled_commands(self) -> tuple[BashCommand, ...]:
        return tuple(command for command in self.commands if command.enabled)

    def command_names(self) -> tuple[str, ...]:
        return tuple(command.name for command in self.enabled_commands())


@dataclass(frozen=True)
class CommandContext:
    chat_session_id: str
    sdk_session_id: str | None
    project_id: str


@dataclass(frozen=True)
class CommandPolicyDecision:
    allowed: bool
    code: RuntimeErrorCode | None = None
    reason: str | None = None
    matched_command: str | None = None


SCENARIO_COMMANDS: dict[AgentScenario, tuple[str, ...]] = {
    AgentScenario.CHAT_ANALYSIS: (
        "chatq artifact save-code",
        "chatq runtime execute",
        "chatq chart kline",
        "chatq conversation link-asset",
    ),
    AgentScenario.SCREENING: (
        "chatq artifact save-code",
        "chatq runtime execute",
        "chatq conversation link-asset",
    ),
    AgentScenario.STRATEGY_BUILD: (
        "chatq artifact save-code",
        "chatq strategy create",
        "chatq strategy validate",
        "chatq conversation link-asset",
    ),
    AgentScenario.BACKTEST: (
        "chatq strategy get",
        "chatq backtest create",
        "chatq backtest run",
        "chatq backtest get",
        "chatq conversation link-asset",
    ),
    AgentScenario.FOLLOW_UP: (
        "chatq artifact save-code",
        "chatq runtime execute",
        "chatq chart kline",
        "chatq strategy get",
        "chatq strategy create",
        "chatq strategy validate",
        "chatq backtest create",
        "chatq backtest run",
        "chatq backtest get",
        "chatq conversation link-asset",
    ),
}


BLOCKED_SUBSTRINGS = (
    ";",
    "&&",
    "||",
    "|",
    ">",
    "<",
    "`",
    "$(",
    "\n",
    "\r",
    " /etc",
    " /Users",
    " ~/.",
    " rm ",
    " chmod ",
    " chown ",
    " curl ",
    " wget ",
    " pip install",
    " npm install",
    " trade ",
    " order ",
)


def load_default_policy() -> BashCommandPolicy:
    commands = (
        BashCommand(
            name="chatq artifact save-code",
            enabled=True,
            modules=("M3",),
            description="保存 Agent 生成的 Python 代码产物",
        ),
        BashCommand(
            name="chatq runtime execute",
            enabled=True,
            modules=("M4",),
            description="执行已保存代码产物",
        ),
        BashCommand(
            name="chatq chart kline",
            enabled=True,
            modules=("M3", "M4"),
            description="生成 K 线图表产物",
        ),
        BashCommand(
            name="chatq strategy create",
            enabled=True,
            modules=("M5",),
            description="根据 StrategyPackage 创建策略和版本",
        ),
        BashCommand(
            name="chatq strategy get",
            enabled=True,
            modules=("M5",),
            description="查询策略版本、入口和参数 schema",
        ),
        BashCommand(
            name="chatq strategy validate",
            enabled=True,
            modules=("M5", "M4"),
            description="校验策略版本",
        ),
        BashCommand(
            name="chatq backtest create",
            enabled=True,
            modules=("M6",),
            description="创建 BacktestRun",
        ),
        BashCommand(
            name="chatq backtest run",
            enabled=True,
            modules=("M6", "M4"),
            description="执行 BacktestRun",
        ),
        BashCommand(
            name="chatq backtest get",
            enabled=True,
            modules=("M6",),
            description="查询回测结果",
        ),
        BashCommand(
            name="chatq conversation link-asset",
            enabled=True,
            modules=("M1",),
            description="将产物、策略或回测关联到会话",
        ),
    )
    names = [command.name for command in commands]
    if len(names) != len(set(names)):
        raise ValueError("duplicate bash command policy entries")
    return BashCommandPolicy(policy_id="default", version=1, commands=commands)


def resolve_allowed_commands(
    policy: BashCommandPolicy,
    scenario: AgentScenario,
) -> tuple[BashCommand, ...]:
    scenario_prefixes = set(SCENARIO_COMMANDS[scenario])
    return tuple(
        command for command in policy.enabled_commands() if command.name in scenario_prefixes
    )


def describe_commands(commands: tuple[BashCommand, ...]) -> str:
    lines = [
        f"- `{command.name}`: {command.description}；模块：{', '.join(command.modules)}"
        for command in commands
    ]
    return "\n".join(lines)


def validate_bash_command(
    command: str,
    allowed_commands: tuple[BashCommand, ...],
    context: CommandContext,
) -> CommandPolicyDecision:
    normalized = " ".join(command.strip().split())
    if not normalized:
        return CommandPolicyDecision(False, RuntimeErrorCode.COMMAND_NOT_ALLOWED, "empty command")

    padded = f" {normalized} "
    for blocked in BLOCKED_SUBSTRINGS:
        if blocked in padded:
            return CommandPolicyDecision(
                False,
                RuntimeErrorCode.TOOL_PERMISSION_DENIED,
                f"blocked shell pattern: {blocked.strip()}",
            )

    matched = next(
        (entry.name for entry in allowed_commands if normalized.startswith(entry.name)),
        None,
    )
    if matched is None:
        return CommandPolicyDecision(
            False,
            RuntimeErrorCode.COMMAND_NOT_ALLOWED,
            "command prefix is not in bash policy",
        )

    try:
        parts = shlex.split(command)
    except ValueError as exc:
        return CommandPolicyDecision(
            False,
            RuntimeErrorCode.COMMAND_NOT_ALLOWED,
            f"invalid shell quoting: {exc}",
        )

    flag_values = _extract_flag_values(parts)
    expected = {
        "--chat-session-id": context.chat_session_id,
        "--conversation-id": context.chat_session_id,
        "--project-id": context.project_id,
    }
    if context.sdk_session_id is not None:
        expected["--sdk-session-id"] = context.sdk_session_id

    for flag, expected_value in expected.items():
        actual_value = flag_values.get(flag)
        if actual_value is not None and actual_value != expected_value:
            return CommandPolicyDecision(
                False,
                RuntimeErrorCode.TOOL_PERMISSION_DENIED,
                f"{flag} does not match current context",
            )

    return CommandPolicyDecision(True, matched_command=matched)


def _extract_flag_values(parts: list[str]) -> dict[str, str]:
    values: dict[str, str] = {}
    for index, item in enumerate(parts):
        if not item.startswith("--"):
            continue
        if "=" in item:
            key, value = item.split("=", 1)
            values[key] = value
        elif index + 1 < len(parts) and not parts[index + 1].startswith("--"):
            values[item] = parts[index + 1]
    return values
