from app.agent_runtime.sdk_skill_workspace import SDKSkillWorkspace


def test_skill_workspace_copies_project_skills_into_session_cwd(tmp_path) -> None:
    source_skill_dir = tmp_path / "project" / ".claude" / "skills"
    skill_dir = source_skill_dir / "stock_query"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("# Stock Query\n\nUse akshare.", encoding="utf-8")

    working_dir = tmp_path / "session"
    prepared_dir = SDKSkillWorkspace(str(source_skill_dir)).prepare(str(working_dir))

    assert prepared_dir == working_dir / ".claude" / "skills"
    assert (prepared_dir / "stock_query" / "SKILL.md").read_text(encoding="utf-8").startswith(
        "# Stock Query"
    )
    assert SDKSkillWorkspace(str(source_skill_dir)).list_skill_names(prepared_dir) == (
        "stock_query",
    )
