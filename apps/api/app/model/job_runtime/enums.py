from __future__ import annotations

from enum import StrEnum


class TriggerType(StrEnum):
    SCHEDULE = "schedule"
    MANUAL = "manual"
    SYSTEM = "system"


class InstanceStatus(StrEnum):
    WAITING = "waiting"
    DISPATCHING = "dispatching"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
