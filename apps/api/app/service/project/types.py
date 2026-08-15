from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


def local_now() -> datetime:
    return datetime.now()


@dataclass(slots=True)
class Project:
    id: str
    local_path: str
    name: str
    description: str | None = None
    created_at: datetime = field(default_factory=local_now)
    updated_at: datetime = field(default_factory=local_now)
    deleted_at: datetime | None = None
