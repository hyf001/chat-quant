from app.infrastructure.agent.sdk_skills import select_available_sdk_skills
from app.schemas.contracts.agent_runtime import AgentScenario


def test_select_available_sdk_skills_suppresses_missing_default_skills() -> None:
    selection = select_available_sdk_skills(AgentScenario.CHAT_ANALYSIS, [], ())

    assert selection.names == ()


def test_select_available_sdk_skills_enables_only_installed_allowlisted_skills() -> None:
    selection = select_available_sdk_skills(
        AgentScenario.CHAT_ANALYSIS,
        [],
        ("stock_query", "risk_disclaimer", "unknown_local_skill"),
    )

    assert selection.names == ("stock_query", "risk_disclaimer")
