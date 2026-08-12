from __future__ import annotations

from pathlib import Path

from supermind_mcp.download import _download_node
from supermind_mcp.models import DownloadResult


class FakeDownloadAPI:
    def __init__(self, nodes: dict[str, dict]):
        self.nodes = nodes

    async def get_contents(self, path: str, content: bool = True) -> dict:
        return self.nodes[path]


async def test_download_node_recurses_and_writes_files(tmp_path: Path) -> None:
    api = FakeDownloadAPI(
        {
            "project/data.txt": {
                "type": "file",
                "path": "project/data.txt",
                "format": "text",
                "content": "hello",
            },
        }
    )
    root = {
        "type": "directory",
        "path": "project",
        "content": [{"type": "file", "path": "project/data.txt"}],
    }
    result = DownloadResult(success=True)

    await _download_node(api, root, base=tmp_path, result=result)

    assert result.downloaded == 1
    assert (tmp_path / "project" / "data.txt").read_text(encoding="utf-8") == "hello"


async def test_download_node_writes_notebook(tmp_path: Path) -> None:
    node = {
        "type": "notebook",
        "path": "project/work.ipynb",
        "content": {
            "cells": [],
            "metadata": {},
            "nbformat": 4,
            "nbformat_minor": 5,
        },
    }
    result = DownloadResult(success=True)

    await _download_node(FakeDownloadAPI({}), node, base=tmp_path, result=result)

    assert result.downloaded == 1
    assert '"nbformat": 4' in (tmp_path / "project" / "work.ipynb").read_text(
        encoding="utf-8"
    )
