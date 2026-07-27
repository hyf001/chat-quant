from app.core.project_dirs import project_dir, safe_project_dir_segment


def test_project_dir_uses_project_id_as_safe_root_segment() -> None:
    assert project_dir("/tmp/chatq/projects", "project_1") == "/tmp/chatq/projects/project_1"
    assert project_dir("/tmp/chatq/projects", "../escape/project") == (
        "/tmp/chatq/projects/.._escape_project"
    )
    assert safe_project_dir_segment("..") == "local_project"
