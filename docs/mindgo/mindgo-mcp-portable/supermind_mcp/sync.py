"""Local-to-Jupyter file synchronization."""

from __future__ import annotations

import base64
import os
from dataclasses import dataclass
from pathlib import Path

from pathspec import PathSpec

from .errors import JupyterHTTPError
from .jupyter_api import jupyter_api
from .models import FileTransferItem, SyncResult
from .paths import join_remote_path, normalize_remote_path


DEFAULT_EXCLUDED_DIRS = {
    ".git",
    "__pycache__",
    ".venv",
    "node_modules",
    ".mypy_cache",
    ".pytest_cache",
    ".sisyphus",
}


@dataclass(frozen=True)
class LocalFile:
    path: Path
    relative_path: str
    size: int


async def sync_files(
    *,
    remote_path: str = "",
    local_path: str = ".",
    dry_run: bool = False,
    url: str | None = None,
    token: str | None = None,
) -> SyncResult:
    """Sync files from a local directory into Jupyter Contents API."""

    root = Path(local_path).expanduser().resolve()
    if not root.exists():
        raise FileNotFoundError(f"Local path does not exist: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"Local path is not a directory: {root}")

    remote_root = normalize_remote_path(remote_path)
    planned = list(iter_sync_files(root))
    result = SyncResult(
        success=True,
        total=len(planned),
        dry_run=dry_run,
        files=[
            FileTransferItem(
                path=item.relative_path,
                size=item.size,
                type=_sniff_file(item.path)[0],
                action="upload",
            )
            for item in planned
        ],
    )
    if dry_run:
        return result

    created_dirs: set[str] = set()
    result.files = []

    async with jupyter_api(url=url, token=token) as api:
        for item in planned:
            remote_file = join_remote_path(remote_root, item.relative_path)
            try:
                created = await ensure_remote_parent_dirs(
                    api, remote_file, created_dirs=created_dirs
                )
                result.directories_created += created
                fmt, content = _sniff_file(item.path)
                await api.save_contents(remote_file, content=content, fmt=fmt)
                result.synced += 1
                result.files.append(
                    FileTransferItem(
                        path=item.relative_path,
                        size=item.size,
                        type=fmt,
                        action="upload",
                    )
                )
            except Exception as exc:  # noqa: BLE001 - continue syncing other files
                result.failed += 1
                result.errors.append(f"{item.relative_path}: {exc}")
                result.files.append(
                    FileTransferItem(
                        path=item.relative_path,
                        size=item.size,
                        action="upload",
                        error=str(exc),
                    )
                )

    result.success = result.failed == 0
    return result


def iter_sync_files(root: Path) -> list[LocalFile]:
    """Return all files under root that should be uploaded."""

    spec = load_gitignore(root)
    files: list[LocalFile] = []
    for current_root, dirnames, filenames in os.walk(root):
        current = Path(current_root)
        dirnames[:] = [
            name
            for name in dirnames
            if not should_skip(current / name, root=root, spec=spec, is_dir=True)
        ]
        for filename in filenames:
            path = current / filename
            if should_skip(path, root=root, spec=spec, is_dir=False):
                continue
            relative = path.relative_to(root).as_posix()
            files.append(LocalFile(path=path, relative_path=relative, size=path.stat().st_size))
    return sorted(files, key=lambda item: item.relative_path)


def load_gitignore(root: Path) -> PathSpec:
    gitignore = root / ".gitignore"
    if not gitignore.exists():
        return PathSpec.from_lines("gitignore", [])
    return PathSpec.from_lines(
        "gitignore",
        gitignore.read_text(encoding="utf-8", errors="ignore").splitlines(),
    )


def should_skip(path: Path, *, root: Path, spec: PathSpec, is_dir: bool) -> bool:
    relative = path.relative_to(root).as_posix()
    if any(part in DEFAULT_EXCLUDED_DIRS for part in path.relative_to(root).parts):
        return True
    match_target = f"{relative}/" if is_dir else relative
    return spec.match_file(match_target)


async def ensure_remote_parent_dirs(
    api: object,
    remote_file_path: str,
    *,
    created_dirs: set[str],
) -> int:
    """Ensure all parent directories exist for a remote file path."""

    remote_file = normalize_remote_path(remote_file_path)
    parts = remote_file.split("/")[:-1]
    created = 0
    current = ""
    for part in parts:
        current = join_remote_path(current, part)
        if current in created_dirs:
            continue
        created += await ensure_remote_dir(api, current)
        created_dirs.add(current)
    return created


async def ensure_remote_dir(api: object, remote_dir: str) -> int:
    """Create a remote directory if missing. Returns 1 only when created."""

    try:
        contents = await api.get_contents(remote_dir, content=False)  # type: ignore[attr-defined]
    except JupyterHTTPError as exc:
        if exc.status_code == 404:
            await api.create_directory(remote_dir)  # type: ignore[attr-defined]
            return 1
        raise

    if isinstance(contents, dict) and contents.get("type") == "directory":
        return 0
    raise NotADirectoryError(f"Remote path is not a directory: {remote_dir}")


def _sniff_file(path: Path) -> tuple[str, str]:
    data = path.read_bytes()
    try:
        return "text", data.decode("utf-8")
    except UnicodeDecodeError:
        return "base64", base64.b64encode(data).decode("ascii")
