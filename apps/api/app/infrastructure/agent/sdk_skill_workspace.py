from __future__ import annotations

import shutil
from pathlib import Path


class SDKSkillWorkspace:
    def __init__(self, source_skill_dir: str) -> None:
        self.source_skill_dir = Path(source_skill_dir)

    def prepare(self, working_dir: str) -> Path:
        working_path = Path(working_dir)
        project_skill_dir = working_path / ".claude" / "skills"
        project_skill_dir.mkdir(parents=True, exist_ok=True)

        if not self.source_skill_dir.exists():
            return project_skill_dir

        for source in self.source_skill_dir.iterdir():
            target = project_skill_dir / source.name
            if source.is_dir():
                shutil.copytree(
                    source,
                    target,
                    dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
                )
            elif source.is_file() and source.name != ".gitkeep":
                shutil.copy2(source, target)

        return project_skill_dir

    def list_skill_names(self, project_skill_dir: Path) -> tuple[str, ...]:
        if not project_skill_dir.exists():
            return ()
        return tuple(
            sorted(
                entry.name
                for entry in project_skill_dir.iterdir()
                if entry.is_dir() and (entry / "SKILL.md").is_file()
            )
        )
