from __future__ import annotations

import ast
import re
from pathlib import PurePosixPath

from app.domain.artifacts.errors import (
    ArtifactFileTooLargeError,
    ArtifactInvalidEntrypointError,
    ArtifactPathEscapeError,
    ArtifactUnsupportedExtensionError,
)
from app.domain.artifacts.models import (
    SCRIPT_ARTIFACT_TYPES,
    ArtifactFileRole,
    ArtifactStatus,
    ArtifactType,
)

MAX_SIZE_BY_SUFFIX = {
    ".py": 1 * 1024 * 1024,
    ".json": 20 * 1024 * 1024,
    ".csv": 50 * 1024 * 1024,
    ".png": 10 * 1024 * 1024,
    ".jpg": 10 * 1024 * 1024,
    ".jpeg": 10 * 1024 * 1024,
    ".webp": 10 * 1024 * 1024,
    ".svg": 10 * 1024 * 1024,
    ".html": 5 * 1024 * 1024,
    ".log": 10 * 1024 * 1024,
    ".txt": 10 * 1024 * 1024,
}

MIME_BY_SUFFIX = {
    ".py": "text/x-python",
    ".json": "application/json",
    ".csv": "text/csv",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".svg": "image/svg+xml",
    ".html": "text/html",
    ".log": "text/plain",
    ".txt": "text/plain",
}

ROLE_SUFFIXES = {
    ArtifactFileRole.QUERY_SCRIPT: {".py"},
    ArtifactFileRole.ANALYSIS_SCRIPT: {".py"},
    ArtifactFileRole.STRATEGY_SCRIPT: {".py"},
    ArtifactFileRole.BACKTEST_SCRIPT: {".py"},
    ArtifactFileRole.JSON_RESULT: {".json"},
    ArtifactFileRole.CHART_FILE: {".png", ".jpg", ".jpeg", ".webp", ".svg", ".html", ".json"},
    ArtifactFileRole.LOG_FILE: {".log", ".txt"},
    ArtifactFileRole.DATA_FILE: {".csv", ".json"},
}

SCRIPT_ROLE_BY_TYPE = {
    ArtifactType.QUERY_SCRIPT: ArtifactFileRole.QUERY_SCRIPT,
    ArtifactType.ANALYSIS_SCRIPT: ArtifactFileRole.ANALYSIS_SCRIPT,
    ArtifactType.STRATEGY_SCRIPT: ArtifactFileRole.STRATEGY_SCRIPT,
    ArtifactType.BACKTEST_SCRIPT: ArtifactFileRole.BACKTEST_SCRIPT,
}

ENTRYPOINT_SYMBOL_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
RISKY_CODE_MARKERS = (
    "os.system",
    "subprocess.",
    "eval(",
    "exec(",
    "requests.get",
    "urllib.request",
    "pip install",
    "akshare.trade",
    "place_order",
    "send_order",
)


def normalize_relative_path(relative_path: str) -> str:
    if not relative_path or relative_path.strip() != relative_path:
        raise ArtifactPathEscapeError("relative_path must be non-empty and trimmed")
    if "\x00" in relative_path or any(ord(char) < 32 for char in relative_path):
        raise ArtifactPathEscapeError("relative_path contains control characters")

    path = PurePosixPath(relative_path)
    parts = path.parts
    if path.is_absolute() or ".." in parts:
        raise ArtifactPathEscapeError("relative_path must stay inside the artifact directory")
    if any(part.startswith(".") for part in parts):
        raise ArtifactPathEscapeError("hidden path segments are not allowed")
    if len(parts) == 0:
        raise ArtifactPathEscapeError("relative_path must point to a file")
    return path.as_posix()


def mime_type_for_path(relative_path: str) -> str:
    suffix = PurePosixPath(relative_path).suffix.lower()
    if suffix not in MIME_BY_SUFFIX:
        raise ArtifactUnsupportedExtensionError(f"unsupported file extension: {suffix or '<none>'}")
    return MIME_BY_SUFFIX[suffix]


def validate_role_extension(relative_path: str, file_role: ArtifactFileRole) -> None:
    suffix = PurePosixPath(relative_path).suffix.lower()
    if suffix not in ROLE_SUFFIXES[file_role]:
        raise ArtifactUnsupportedExtensionError(
            f"{file_role.value} does not support extension {suffix or '<none>'}"
        )


def validate_file_size(relative_path: str, size_bytes: int) -> None:
    suffix = PurePosixPath(relative_path).suffix.lower()
    limit = MAX_SIZE_BY_SUFFIX.get(suffix)
    if limit is None:
        raise ArtifactUnsupportedExtensionError(f"unsupported file extension: {suffix or '<none>'}")
    if size_bytes > limit:
        raise ArtifactFileTooLargeError(f"{relative_path} exceeds the {limit} byte limit")


def parse_entrypoint(entrypoint: str | None) -> tuple[str | None, str | None]:
    if not entrypoint:
        return None, None
    if any(char.isspace() for char in entrypoint) or "\x00" in entrypoint:
        raise ArtifactInvalidEntrypointError("entrypoint cannot contain whitespace or controls")

    path_part, separator, symbol = entrypoint.partition(":")
    path = normalize_relative_path(path_part)
    if not path.startswith("src/"):
        raise ArtifactInvalidEntrypointError("entrypoint path must be under src/")
    if separator and not ENTRYPOINT_SYMBOL_RE.fullmatch(symbol):
        raise ArtifactInvalidEntrypointError("entrypoint symbol must be a valid Python identifier")
    return path, symbol if separator else None


def validate_entrypoint(artifact_type: ArtifactType, entrypoint: str | None) -> None:
    path, symbol = parse_entrypoint(entrypoint)
    if artifact_type in SCRIPT_ARTIFACT_TYPES and path is None:
        raise ArtifactInvalidEntrypointError(f"{artifact_type.value} requires an entrypoint")
    if artifact_type not in SCRIPT_ARTIFACT_TYPES and entrypoint is not None:
        raise ArtifactInvalidEntrypointError(f"{artifact_type.value} cannot have an entrypoint")
    if artifact_type == ArtifactType.STRATEGY_SCRIPT and symbol is None:
        raise ArtifactInvalidEntrypointError("strategy_script requires a class entrypoint")


def validate_artifact_file_role(artifact_type: ArtifactType, file_role: ArtifactFileRole) -> None:
    expected = SCRIPT_ROLE_BY_TYPE.get(artifact_type)
    if expected is not None and file_role != expected:
        raise ArtifactUnsupportedExtensionError(
            f"{artifact_type.value} files must use {expected.value} role"
        )


def inspect_python_status(artifact_type: ArtifactType, content: str) -> ArtifactStatus:
    if artifact_type not in SCRIPT_ARTIFACT_TYPES:
        return ArtifactStatus.CREATED
    try:
        ast.parse(content)
    except SyntaxError:
        if artifact_type in {ArtifactType.STRATEGY_SCRIPT, ArtifactType.BACKTEST_SCRIPT}:
            raise ArtifactInvalidEntrypointError(
                "strategy and backtest code must be valid Python"
            ) from None
        return ArtifactStatus.INVALID

    if any(marker in content for marker in RISKY_CODE_MARKERS):
        return ArtifactStatus.INVALID
    return ArtifactStatus.VALIDATED
