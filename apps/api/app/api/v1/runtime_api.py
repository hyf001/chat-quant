from __future__ import annotations

import platform
import tempfile
from importlib import metadata
from pathlib import Path

from fastapi import APIRouter

from app.core.config import get_settings
from app.schema.runtime import RuntimeHealthResponse

router = APIRouter()

_PACKAGE_NAMES = ("fastapi", "pandas", "backtrader", "claude-agent-sdk")


@router.get("/health", response_model=RuntimeHealthResponse)
async def runtime_health() -> RuntimeHealthResponse:
    settings = get_settings()
    return RuntimeHealthResponse(
        status="ok",
        python_version=platform.python_version(),
        packages=_package_versions(_PACKAGE_NAMES),
        project_home_writable=_is_project_home_writable(Path(settings.project_home)),
    )


def _package_versions(package_names: tuple[str, ...]) -> dict[str, str]:
    versions: dict[str, str] = {}
    for package_name in package_names:
        try:
            versions[package_name] = metadata.version(package_name)
        except metadata.PackageNotFoundError:
            continue
    return versions


def _is_project_home_writable(project_home: Path) -> bool:
    try:
        project_home.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryFile(dir=project_home):
            return True
    except OSError:
        return False
