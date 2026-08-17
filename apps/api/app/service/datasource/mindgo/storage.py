from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

DEFAULT_MINDGO_STORAGE_ROOT = Path("data") / "mindgo" / "parquet"
DEFAULT_MINDGO_PARTITION_FILENAME = "data.parquet"


@dataclass(frozen=True)
class MindgoSourceStorage:
    storage_root: Path

    def __init__(self, storage_root: Path | str = DEFAULT_MINDGO_STORAGE_ROOT) -> None:
        object.__setattr__(self, "storage_root", Path(storage_root).expanduser())

    def source_root(self, source_id: str) -> Path:
        return self.storage_root / _safe_path_segment(source_id)

    def partition_path(
        self,
        source_id: str,
        partition_values: Mapping[str, str],
        *,
        filename: str = DEFAULT_MINDGO_PARTITION_FILENAME,
    ) -> Path:
        path = self.source_root(source_id)
        for key, value in partition_values.items():
            path /= f"{_safe_path_segment(key)}={_safe_path_segment(value)}"
        return path / _safe_path_segment(filename)

    def partition_summary(
        self,
        source_id: str,
        partition_keys: list[str],
        *,
        filename: str = DEFAULT_MINDGO_PARTITION_FILENAME,
    ) -> MindgoSourcePartitionSummary:
        partitions = sorted(
            _source_partitions(
                self.source_root(source_id),
                partition_keys,
                filename=_safe_path_segment(filename),
            )
        )
        return MindgoSourcePartitionSummary(
            min_partition=partitions[0] if partitions else None,
            max_partition=partitions[-1] if partitions else None,
            partition_count=len(partitions),
        )


@dataclass(frozen=True)
class MindgoSourcePartitionSummary:
    min_partition: str | None
    max_partition: str | None
    partition_count: int


def mindgo_source_partition_path(
    storage_root: Path | str,
    source_id: str,
    partition_values: Mapping[str, str],
) -> Path:
    return MindgoSourceStorage(storage_root).partition_path(source_id, partition_values)


def _safe_path_segment(value: str) -> str:
    text = str(value)
    if not text or "/" in text or "\\" in text or text in {".", ".."}:
        raise ValueError(f"invalid MindGo storage path segment: {text!r}")
    return text


def _source_partitions(
    base_path: Path,
    partition_keys: list[str],
    *,
    filename: str,
) -> list[str]:
    if not partition_keys:
        return []
    partitions: list[str] = []
    _collect_source_partitions(
        base_path,
        partition_keys,
        filename=filename,
        values=[],
        partitions=partitions,
    )
    return partitions


def _collect_source_partitions(
    base_path: Path,
    partition_keys: list[str],
    *,
    filename: str,
    values: list[str],
    partitions: list[str],
) -> None:
    if len(values) == len(partition_keys):
        if (base_path / filename).exists():
            partitions.append("/".join(values))
        return
    if not base_path.exists():
        return
    partition_key = _safe_path_segment(partition_keys[len(values)])
    prefix = f"{partition_key}="
    for child in base_path.iterdir():
        if not child.is_dir() or not child.name.startswith(prefix):
            continue
        partition_value = child.name[len(prefix) :]
        if partition_value:
            _safe_path_segment(partition_value)
            _collect_source_partitions(
                child,
                partition_keys,
                filename=filename,
                values=[*values, partition_value],
                partitions=partitions,
            )
