from __future__ import annotations

import platform
import tempfile
from importlib import metadata
from pathlib import Path

from fastapi import APIRouter

from app.core.config import get_settings
from app.schemas.runtime import RuntimeHealthResponse

router = APIRouter(prefix="/runtime", tags=["runtime"])

_PACKAGE_NAMES = ("fastapi", "pandas", "backtrader", "claude-agent-sdk")


@router.get("/health", response_model=RuntimeHealthResponse)
async def runtime_health() -> RuntimeHealthResponse:
    settings = get_settings()
    return RuntimeHealthResponse(
        status="ok",
        python_version=platform.python_version(),
        packages=_package_versions(_PACKAGE_NAMES),
        runtime_root_writable=_is_runtime_root_writable(Path(settings.agent_workdir_root)),
    )


def _package_versions(package_names: tuple[str, ...]) -> dict[str, str]:
    versions: dict[str, str] = {}
    for package_name in package_names:
        try:
            versions[package_name] = metadata.version(package_name)
        except metadata.PackageNotFoundError:
            continue
    return versions


def _is_runtime_root_writable(runtime_root: Path) -> bool:
    try:
        runtime_root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryFile(dir=runtime_root):
            return True
    except OSError:
        return False
