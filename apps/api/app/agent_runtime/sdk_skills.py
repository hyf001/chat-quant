from __future__ import annotations

from dataclasses import dataclass

from app.schemas.contracts.agent_runtime import AgentScenario

ALLOWED_SKILLS = {
    "financial_data_query",
    "charting",
    "strategy_authoring",
    "backtest",
    "risk_disclaimer",
}

SCENARIO_SKILLS: dict[AgentScenario, tuple[str, ...]] = {
    AgentScenario.CHAT_ANALYSIS: ("financial_data_query", "charting", "risk_disclaimer"),
    AgentScenario.SCREENING: ("financial_data_query", "charting", "risk_disclaimer"),
    AgentScenario.STRATEGY_BUILD: ("strategy_authoring", "backtest", "risk_disclaimer"),
    AgentScenario.BACKTEST: ("backtest", "charting", "risk_disclaimer"),
    AgentScenario.FOLLOW_UP: (
        "financial_data_query",
        "charting",
        "strategy_authoring",
        "backtest",
        "risk_disclaimer",
    ),
}


@dataclass(frozen=True)
class SkillSelection:
    names: tuple[str, ...]
    warnings: tuple[str, ...] = ()


def select_sdk_skills(scenario: AgentScenario, requested: list[str]) -> SkillSelection:
    return select_available_sdk_skills(scenario, requested, tuple(ALLOWED_SKILLS))


def select_available_sdk_skills(
    scenario: AgentScenario,
    requested: list[str],
    available: tuple[str, ...],
) -> SkillSelection:
    defaults = SCENARIO_SKILLS[scenario]
    candidates = tuple(_skill_short_name(skill) for skill in requested) if requested else defaults
    available_set = set(available)
    accepted = tuple(
        skill for skill in candidates if skill in ALLOWED_SKILLS and skill in available_set
    )
    rejected = tuple(skill for skill in candidates if skill not in ALLOWED_SKILLS)
    warnings = tuple(f"SDK skill is not allowed and was ignored: {skill}" for skill in rejected)
    return SkillSelection(names=accepted, warnings=warnings)


def _skill_short_name(skill_name: str) -> str:
    return skill_name.rsplit(":", maxsplit=1)[-1]
