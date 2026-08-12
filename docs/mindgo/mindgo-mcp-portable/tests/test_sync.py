from __future__ import annotations

from pathlib import Path

import pytest

from supermind_mcp.errors import JupyterHTTPError
from supermind_mcp.sync import ensure_remote_parent_dirs, iter_sync_files


def test_iter_sync_files_honors_default_excludes_and_gitignore(tmp_path: Path) -> None:
    (tmp_path / ".gitignore").write_text("ignored.txt\nbuild/\n", encoding="utf-8")
    (tmp_path / "keep.txt").write_text("ok", encoding="utf-8")
    (tmp_path / "ignored.txt").write_text("ignored", encoding="utf-8")
    (tmp_path / "build").mkdir()
    (tmp_path / "build" / "asset.bin").write_bytes(b"ignored")
    (tmp_path / ".git").mkdir()
    (tmp_path / ".git" / "config").write_text("ignored", encoding="utf-8")
    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "module.py").write_text("print('ok')", encoding="utf-8")

    files = iter_sync_files(tmp_path)

    assert [item.relative_path for item in files] == [".gitignore", "keep.txt", "pkg/module.py"]


class FakeAPI:
    def __init__(self, existing: set[str] | None = None):
        self.existing = existing or set()
        self.created: list[str] = []

    async def get_contents(self, path: str, content: bool = False) -> dict[str, str]:
        if path not in self.existing:
            raise JupyterHTTPError(404, "not found")
        return {"type": "directory"}

    async def create_directory(self, path: str) -> dict[str, str]:
        self.created.append(path)
        self.existing.add(path)
        return {"type": "directory"}


@pytest.mark.asyncio
async def test_ensure_remote_parent_dirs_creates_missing_parents() -> None:
    api = FakeAPI(existing={"project"})
    created = await ensure_remote_parent_dirs(
        api,
        "project/data/results/out.csv",
        created_dirs=set(),
    )

    assert created == 2
    assert api.created == ["project/data", "project/data/results"]
