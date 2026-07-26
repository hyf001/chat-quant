from app.agent_runtime.sdk_skill_plugin import SDKSkillPlugin


def test_skill_plugin_exposes_local_plugin_config_and_namespaces_skills(tmp_path) -> None:
    plugin_dir = tmp_path / "plugin"
    skill_dir = plugin_dir / "skills" / "financial_data_query"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("# Financial Data Query\n\nUse akshare.", encoding="utf-8")

    plugin = SDKSkillPlugin(str(plugin_dir), "chat-quant")

    assert plugin.list_skill_names() == ("financial_data_query",)
    assert plugin.qualify_skill_names(("financial_data_query",)) == (
        "chat-quant:financial_data_query",
    )
    assert plugin.sdk_plugin_configs() == (
        {"type": "local", "path": str(plugin_dir.resolve())},
    )
