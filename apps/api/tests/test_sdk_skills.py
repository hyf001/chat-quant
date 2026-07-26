from app.agent_runtime.sdk_skills import select_available_sdk_skills
from app.schemas.contracts.agent_runtime import AgentScenario


def test_select_available_sdk_skills_suppresses_missing_default_skills() -> None:
    selection = select_available_sdk_skills(AgentScenario.CHAT_ANALYSIS, [], ())

    assert selection.names == ()


def test_select_available_sdk_skills_enables_only_installed_allowlisted_skills() -> None:
    selection = select_available_sdk_skills(
        AgentScenario.CHAT_ANALYSIS,
        [],
        ("financial_data_query", "risk_disclaimer", "unknown_local_skill"),
    )

    assert selection.names == ("financial_data_query", "risk_disclaimer")


def test_select_available_sdk_skills_accepts_plugin_qualified_requests() -> None:
    selection = select_available_sdk_skills(
        AgentScenario.CHAT_ANALYSIS,
        ["chat-quant:financial_data_query"],
        ("financial_data_query", "risk_disclaimer"),
    )

    assert selection.names == ("financial_data_query",)
