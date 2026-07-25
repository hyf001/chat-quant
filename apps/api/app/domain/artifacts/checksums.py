from __future__ import annotations

import hashlib
import json

from app.domain.artifacts.models import ArtifactType, JsonObject


def normalize_text_content(content: str) -> bytes:
    return content.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def canonical_json_bytes(payload: JsonObject) -> bytes:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode(
        "utf-8"
    )


def sha256_digest(content: bytes) -> str:
    return f"sha256:{hashlib.sha256(content).hexdigest()}"


def package_checksum(
    artifact_type: ArtifactType,
    entrypoint: str | None,
    file_checksums: list[tuple[str, str]],
) -> str:
    rows = [f"{relative_path}:{checksum}" for relative_path, checksum in sorted(file_checksums)]
    payload = f"{artifact_type.value}\n{entrypoint or ''}\n" + "\n".join(rows)
    return sha256_digest(payload.encode("utf-8"))
