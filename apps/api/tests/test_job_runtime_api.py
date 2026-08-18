from __future__ import annotations

from datetime import datetime

from app.core.config import get_settings
from app.db.schema import ensure_database_schema
from app.model.job_runtime import JobInstanceRow
from app.model.job_runtime.enums import InstanceStatus, TriggerType
from fastapi.testclient import TestClient
from sqlalchemy import create_engine


def test_job_runtime_instances_list_returns_paginated_full_fields(client: TestClient) -> None:
    _insert_instance(
        "inst_old",
        job_id="a_stock_daily_price",
        trigger_type=TriggerType.MANUAL,
        scheduled_for=datetime(2026, 8, 14, 10, 0),
        summary="old summary",
    )
    _insert_instance(
        "inst_new",
        job_id="a_stock_daily_price",
        trigger_type=TriggerType.SCHEDULE,
        scheduled_for=datetime(2026, 8, 15, 10, 0),
        summary="new summary",
        result_status="success",
    )

    response = client.get(
        "/api/job-runtime/instances",
        params={
            "job_type": "mindgo_dataset_sync",
            "job_id": "a_stock_daily_price",
            "page": 1,
            "page_size": 1,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] == 2
    assert payload["page"] == 1
    assert payload["page_size"] == 1
    assert payload["total_pages"] == 2
    assert {item["status"]: item["count"] for item in payload["status_counts"]} == {
        "waiting": 0,
        "dispatching": 0,
        "running": 0,
        "completed": 2,
        "failed": 0,
        "cancelled": 0,
    }
    assert payload["items"][0] == {
        "id": "inst_new",
        "job_type": "mindgo_dataset_sync",
        "job_id": "a_stock_daily_price",
        "trigger_type": "schedule",
        "trigger_key": "trigger_inst_new",
        "payload": {"source": "test"},
        "priority": 7,
        "scheduled_for": "2026-08-15T10:00:00",
        "started_at": None,
        "completed_at": None,
        "status": "completed",
        "result_status": "success",
        "summary": "new summary",
        "error_message": "",
        "created_at": "2026-08-14T09:00:00",
        "updated_at": "2026-08-14T09:00:00",
    }

    filtered_response = client.get(
        "/api/job-runtime/instances",
        params={
            "job_type": "mindgo_dataset_sync",
            "job_id": "a_stock_daily_price",
            "status": "waiting",
        },
    )

    assert filtered_response.status_code == 200
    filtered_payload = filtered_response.json()
    assert filtered_payload["total"] == 0
    assert filtered_payload["items"] == []
    assert {item["status"]: item["count"] for item in filtered_payload["status_counts"]}[
        "completed"
    ] == 2


def test_job_runtime_instances_rerun_and_delete(client: TestClient) -> None:
    _insert_instance(
        "inst_rerun",
        job_id="a_stock_daily_price",
        trigger_type=TriggerType.SCHEDULE,
        scheduled_for=datetime(2026, 8, 15, 10, 0),
        started_at=datetime(2026, 8, 15, 10, 1),
        completed_at=datetime(2026, 8, 15, 10, 2),
        status=InstanceStatus.FAILED,
        result_status=None,
        summary="failed",
        error_message="boom",
    )

    rerun_response = client.post("/api/job-runtime/instances/inst_rerun/rerun")

    assert rerun_response.status_code == 200
    rerun_payload = rerun_response.json()
    assert rerun_payload["id"] == "inst_rerun"
    assert rerun_payload["trigger_type"] == "rerun"
    assert rerun_payload["status"] == "waiting"
    assert rerun_payload["started_at"] is None
    assert rerun_payload["completed_at"] is None
    assert rerun_payload["result_status"] is None
    assert rerun_payload["summary"] == ""
    assert rerun_payload["error_message"] == ""

    delete_response = client.delete("/api/job-runtime/instances/inst_rerun")

    assert delete_response.status_code == 204
    list_response = client.get(
        "/api/job-runtime/instances",
        params={"job_id": "a_stock_daily_price"},
    )
    assert list_response.status_code == 200
    assert list_response.json()["items"] == []


def _insert_instance(
    instance_id: str,
    *,
    job_id: str,
    trigger_type: TriggerType,
    scheduled_for: datetime,
    started_at: datetime | None = None,
    completed_at: datetime | None = None,
    status: InstanceStatus = InstanceStatus.COMPLETED,
    result_status: str | None = None,
    summary: str = "",
    error_message: str = "",
) -> None:
    settings = get_settings()
    ensure_database_schema(settings)
    engine = create_engine(f"sqlite:///{settings.database_path}")
    now = datetime(2026, 8, 14, 9, 0)
    try:
        with engine.begin() as connection:
            connection.execute(
                JobInstanceRow.__table__.insert(),
                {
                    "id": instance_id,
                    "job_type": "mindgo_dataset_sync",
                    "job_id": job_id,
                    "trigger_type": trigger_type.value,
                    "trigger_key": f"trigger_{instance_id}",
                    "trigger_payload_json": {"source": "test"},
                    "status": status.value,
                    "priority": 7,
                    "scheduled_for": scheduled_for,
                    "started_at": started_at,
                    "completed_at": completed_at,
                    "result_status": result_status,
                    "summary": summary,
                    "error_message": error_message,
                    "created_at": now,
                    "updated_at": now,
                },
            )
    finally:
        engine.dispose()
