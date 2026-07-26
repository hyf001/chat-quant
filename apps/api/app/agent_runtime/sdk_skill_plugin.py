from __future__ import annotations

from pathlib import Path


class SDKSkillPlugin:
    def __init__(self, plugin_dir: str, plugin_name: str) -> None:
        self.plugin_dir = Path(plugin_dir).expanduser().resolve()
        self.plugin_name = plugin_name

    @property
    def skills_dir(self) -> Path:
        return self.plugin_dir / "skills"

    def list_skill_names(self) -> tuple[str, ...]:
        if not self.skills_dir.exists():
            return ()
        return tuple(
            sorted(
                entry.name
                for entry in self.skills_dir.iterdir()
                if entry.is_dir() and (entry / "SKILL.md").is_file()
            )
        )

    def qualify_skill_names(self, skill_names: tuple[str, ...]) -> tuple[str, ...]:
        return tuple(
            skill_name
            if ":" in skill_name
            else f"{self.plugin_name}:{skill_name}"
            for skill_name in skill_names
        )

    def sdk_plugin_configs(self) -> tuple[dict[str, str], ...]:
        if not self.plugin_dir.exists():
            return ()
        return ({"type": "local", "path": str(self.plugin_dir)},)
