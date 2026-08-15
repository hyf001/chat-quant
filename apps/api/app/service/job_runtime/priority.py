"""Priority helpers for job runtime execution."""
from __future__ import annotations

from datetime import datetime

from .types import PrioritySpec


def resolve_priority(priority: PrioritySpec | None, *, now: datetime | None = None) -> int:
    if priority is None:
        return 0
    now = now or datetime.now()
    overdue_weight = 0
    if priority.due_at is not None and priority.due_at < now:
        overdue_weight = 50
    waiting_age_weight = 0
    if priority.created_at is not None and priority.created_at < now:
        waiting_age_weight = min(int((now - priority.created_at).total_seconds() // 3600), 48)
    return (
        priority.business_priority
        + priority.trigger_priority
        + overdue_weight
        + waiting_age_weight
        + priority.custom_score
    )
