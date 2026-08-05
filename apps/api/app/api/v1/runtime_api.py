from __future__ import annotations

import platform
from importlib import metadata

from fastapi import APIRouter

from app.schema.runtime import RuntimeHealthResponse

router = APIRouter()

_PACKAGE_NAMES = ("fastapi", "pandas", "backtrader", "claude-agent-sdk")


@router.get("/health", response_model=RuntimeHealthResponse)
async def runtime_health() -> RuntimeHealthResponse:
    return RuntimeHealthResponse(
        status="ok",
        python_version=platform.python_version(),
        packages=_package_versions(_PACKAGE_NAMES),
    )


def _package_versions(package_names: tuple[str, ...]) -> dict[str, str]:
    versions: dict[str, str] = {}
    for package_name in package_names:
        try:
            versions[package_name] = metadata.version(package_name)
        except metadata.PackageNotFoundError:
            continue
    return versions
