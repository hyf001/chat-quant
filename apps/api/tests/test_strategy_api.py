import asyncio
import logging
from datetime import datetime

import pytest
from app.core.config import get_settings
from app.db.session import get_session_factory
from app.model.strategy import StrategySignalRow
from app.service.strategy.strategy_deployment_job import (
    StrategyDeploymentRuntimeContext,
    StrategyRuntimeTrigger,
    execute_strategy_deployment_tick,
)
from fastapi.testclient import TestClient
from sqlalchemy import create_engine

pytestmark = pytest.mark.usefixtures("project_test")


def test_create_strategy_returns_draft_first_version(client: TestClient, caplog) -> None:
    caplog.set_level(logging.INFO, logger="app.service.strategy.strategy_service")

    response = client.post(
        "/api/strategies",
        json=strategy_create_payload(),
    )

    assert response.status_code == 201
    data = response.json()
    assert data["strategy_id"].startswith("str_")
    assert set(data) == {"strategy_id"}

    assert any(
        record.levelname == "INFO"
        and record.name == "app.service.strategy.strategy_service"
        and record.message == "strategy created"
        and record.strategy_id == data["strategy_id"]
        for record in caplog.records
    )


def test_create_strategy_rejects_missing_project(client: TestClient) -> None:
    payload = strategy_create_payload()
    payload["project_id"] = "project_missing"

    response = client.post(
        "/api/strategies",
        json=payload,
    )

    assert response.status_code == 404
    assert response.json()["detail"]["error_code"] == "PROJECT_NOT_FOUND"


def test_create_strategy_rejects_chatq_param_default_type_mismatch(client: TestClient) -> None:
    payload = strategy_create_payload()
    payload["source_code"] = payload["source_code"].replace(
        '"default": 20',
        '"default": "20"',
        1,
    )

    response = client.post(
        "/api/strategies",
        json=payload,
    )

    assert response.status_code == 422


def test_create_strategy_rejects_request_custom_params(client: TestClient) -> None:
    payload = strategy_create_payload()
    payload["custom_params"] = [
        {
            "name_cn": "短期均线周期",
            "name_en": "fast_period",
            "type": "integer",
            "default": 20,
            "required": True,
        }
    ]

    response = client.post(
        "/api/strategies",
        json=payload,
    )

    assert response.status_code == 422


def test_create_strategy_rejects_external_data_access(client: TestClient) -> None:
    payload = strategy_create_payload()
    payload["source_code"] = f"import akshare as ak\n{payload['source_code']}"

    response = client.post(
        "/api/strategies",
        json=payload,
    )

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert detail["error_code"] == "STRATEGY_EXTERNAL_DATA_ACCESS"
    assert detail["issues"][0]["detail"]["module"] == "akshare"


def test_create_strategy_rejects_missing_protocol_function(client: TestClient) -> None:
    payload = strategy_create_payload()
    payload["source_code"] = "\n".join(
        [
            "def chatq_init(context):",
            "    return {}",
        ]
    )

    response = client.post(
        "/api/strategies",
        json=payload,
    )

    assert response.status_code == 422
    assert response.json()["detail"]["error_code"] == "STRATEGY_PROTOCOL_INVALID"


def test_update_metadata_does_not_create_new_version(client: TestClient) -> None:
    created = client.post(
        "/api/strategies",
        json=strategy_create_payload(),
    ).json()

    response = client.patch(
        f"/api/strategies/{created['strategy_id']}",
        json={
            "name": "稳健均线策略",
            "description": "保留同一策略逻辑，只更新展示元数据",
            "tags": ["沪深300", "稳健版", "沪深300"],
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "稳健均线策略"
    assert data["tags"] == ["沪深300", "稳健版"]
    detail = client.get(f"/api/strategies/{created['strategy_id']}").json()
    assert detail["strategy"]["name"] == "稳健均线策略"


def test_create_strategy_version_switches_current_version(client: TestClient) -> None:
    created = client.post(
        "/api/strategies",
        json=strategy_create_payload(),
    ).json()

    response = client.post(
        f"/api/strategies/{created['strategy_id']}/versions",
        json=strategy_version_payload(fast_period=30, slow_period=90, strategy_mode="multi_symbol"),
    )

    assert response.status_code == 201
    version = response.json()
    assert version["strategy_id"] == created["strategy_id"]
    assert version["version"] == 2
    assert version["strategy_mode"] == "multi_symbol"
    assert version["custom_params"][0]["default"] == 30
    assert version["custom_params"][1]["default"] == 90

    detail = client.get(f"/api/strategies/{created['strategy_id']}").json()
    assert detail["strategy"]["current_version_id"] == version["id"]

    strategies = client.get("/api/strategies?project_id=project_test").json()
    assert strategies[0]["strategy_version_id"] == version["id"]
    assert strategies[0]["version"] == 2
    assert strategies[0]["strategy_mode"] == "multi_symbol"
    assert "strategy_config" not in strategies[0]
    assert strategies[0]["custom_params"][0]["default"] == 30


def test_create_strategy_version_rejects_request_custom_params(client: TestClient) -> None:
    created = client.post(
        "/api/strategies",
        json=strategy_create_payload(),
    ).json()
    payload = strategy_version_payload(fast_period=30, slow_period=90)
    payload["custom_params"] = [
        {
            "name_cn": "短期均线周期",
            "name_en": "fast_period",
            "type": "integer",
            "default": 30,
            "required": True,
        }
    ]

    response = client.post(
        f"/api/strategies/{created['strategy_id']}/versions",
        json=payload,
    )

    assert response.status_code == 422


def test_create_strategy_version_protocol_failure_is_blocked_without_switching(
    client: TestClient,
) -> None:
    created = client.post(
        "/api/strategies",
        json=strategy_create_payload(),
    ).json()
    first_version = client.get(f"/api/strategies/{created['strategy_id']}/versions").json()[0]
    payload = strategy_version_payload()
    payload["source_code"] = "\n".join(
        [
            "def chatq_init(context):",
            "    return {}",
        ]
    )

    response = client.post(
        f"/api/strategies/{created['strategy_id']}/versions",
        json=payload,
    )

    assert response.status_code == 422
    assert response.json()["detail"]["error_code"] == "STRATEGY_PROTOCOL_INVALID"
    versions = client.get(f"/api/strategies/{created['strategy_id']}/versions").json()
    assert [version["id"] for version in versions] == [first_version["id"]]
    detail = client.get(f"/api/strategies/{created['strategy_id']}").json()
    assert detail["strategy"]["current_version_id"] == first_version["id"]


def test_switch_current_version_can_select_existing_version(client: TestClient) -> None:
    created = client.post(
        "/api/strategies",
        json=strategy_create_payload(),
    ).json()
    first_version = client.get(f"/api/strategies/{created['strategy_id']}/versions").json()[0]
    second_version = client.post(
        f"/api/strategies/{created['strategy_id']}/versions",
        json=strategy_version_payload(fast_period=30, slow_period=90, strategy_mode="multi_symbol"),
    ).json()

    response = client.patch(
        f"/api/strategies/{created['strategy_id']}/current-version",
        json={"strategy_version_id": first_version["id"]},
    )

    assert response.status_code == 200
    summary = response.json()
    assert summary["strategy_version_id"] == first_version["id"]
    assert summary["version"] == 1
    assert summary["strategy_mode"] == "single_symbol"

    detail = client.get(f"/api/strategies/{created['strategy_id']}").json()
    assert detail["strategy"]["current_version_id"] == first_version["id"]

    strategies = client.get("/api/strategies?project_id=project_test").json()
    assert strategies[0]["strategy_version_id"] == first_version["id"]
    assert strategies[0]["version"] == 1
    assert strategies[0]["strategy_version_id"] != second_version["id"]


def test_list_strategy_versions_returns_all_versions(client: TestClient) -> None:
    created = client.post(
        "/api/strategies",
        json=strategy_create_payload(),
    ).json()
    client.post(
        f"/api/strategies/{created['strategy_id']}/versions",
        json=strategy_version_payload(fast_period=30, slow_period=90),
    )

    response = client.get(f"/api/strategies/{created['strategy_id']}/versions")

    assert response.status_code == 200
    versions = response.json()
    assert [version["version"] for version in versions] == [1, 2]
    assert [version["strategy_mode"] for version in versions] == ["single_symbol", "single_symbol"]
    assert versions[0]["source_code"]
    assert "strategy_config" not in versions[0]


def test_get_strategy_version_by_id(client: TestClient) -> None:
    created = client.post(
        "/api/strategies",
        json=strategy_create_payload(),
    ).json()
    version = client.get(f"/api/strategies/{created['strategy_id']}/versions").json()[0]

    response = client.get(f"/api/strategy-versions/{version['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == version["id"]
    assert response.json()["strategy_id"] == created["strategy_id"]


def test_create_strategy_version_rejects_deleted_strategy(client: TestClient) -> None:
    created = client.post(
        "/api/strategies",
        json=strategy_create_payload(),
    ).json()
    client.delete(f"/api/strategies/{created['strategy_id']}")

    response = client.post(
        f"/api/strategies/{created['strategy_id']}/versions",
        json=strategy_version_payload(fast_period=30, slow_period=90),
    )

    assert response.status_code == 409
    assert response.json()["detail"]["error_code"] == "STRATEGY_DELETED"


def test_deleted_strategy_is_hidden_from_list(client: TestClient) -> None:
    created = client.post(
        "/api/strategies",
        json=strategy_create_payload(),
    ).json()

    response = client.delete(f"/api/strategies/{created['strategy_id']}")

    assert response.status_code == 200
    assert client.get("/api/strategies?project_id=project_test").json() == []


def test_strategy_deployment_stores_complete_param_snapshot(client: TestClient) -> None:
    created = client.post(
        "/api/strategies",
        json=strategy_create_payload(),
    ).json()
    strategy = client.get("/api/strategies?project_id=project_test").json()[0]

    response = client.post(
        "/api/strategy-deployments",
        json={
            "project_id": "project_test",
            "strategy_id": created["strategy_id"],
            "strategy_version_id": strategy["strategy_version_id"],
            "name": "MA signal deployment",
            "mode": "signal",
            "symbols": ["000001.SZ"],
            "params": {"fast_period": 12},
        },
    )

    assert response.status_code == 201
    deployment = response.json()
    assert deployment["params"] == {
        "fast_period": 12,
        "slow_period": 60,
        "volatility_filter": "medium",
    }

    update_response = client.patch(
        f"/api/strategy-deployments/{deployment['id']}",
        json={"params": {"slow_period": 80}},
    )

    assert update_response.status_code == 200
    assert update_response.json()["params"] == {
        "fast_period": 20,
        "slow_period": 80,
        "volatility_filter": "medium",
    }


def test_delete_strategy_deployment_cleans_schedule_and_instances(client: TestClient) -> None:
    created = client.post(
        "/api/strategies",
        json=strategy_create_payload(),
    ).json()
    strategy = client.get("/api/strategies?project_id=project_test").json()[0]
    deployment = client.post(
        "/api/strategy-deployments",
        json={
            "project_id": "project_test",
            "strategy_id": created["strategy_id"],
            "strategy_version_id": strategy["strategy_version_id"],
            "name": "Cleanup deployment",
            "mode": "signal",
            "symbols": ["000001.SZ"],
        },
    ).json()
    schedule_response = client.put(
        f"/api/strategy-deployments/{deployment['id']}/schedule",
        json={"cron": "0 15 * * 1-5"},
    )
    trigger_response = client.post(
        f"/api/strategy-deployments/{deployment['id']}/trigger",
        json={},
    )

    assert schedule_response.status_code == 200
    assert schedule_response.json()["scheduled"] is True
    assert trigger_response.status_code == 201
    instances_before = client.get(
        "/api/job-runtime/instances",
        params={"job_type": "strategy_deployment_tick", "job_id": deployment["id"]},
    ).json()
    assert instances_before["total"] == 1

    delete_response = client.delete(f"/api/strategy-deployments/{deployment['id']}")

    assert delete_response.status_code == 200
    assert delete_response.json()["id"] == deployment["id"]
    assert client.get(f"/api/strategy-deployments/{deployment['id']}").status_code == 404
    instances_after = client.get(
        "/api/job-runtime/instances",
        params={"job_type": "strategy_deployment_tick", "job_id": deployment["id"]},
    ).json()
    assert instances_after["total"] == 0


def test_list_strategy_signals_returns_backend_action_counts(client: TestClient) -> None:
    created = client.post(
        "/api/strategies",
        json=strategy_create_payload(),
    ).json()
    strategy = client.get("/api/strategies?project_id=project_test").json()[0]
    deployment = client.post(
        "/api/strategy-deployments",
        json={
            "project_id": "project_test",
            "strategy_id": created["strategy_id"],
            "strategy_version_id": strategy["strategy_version_id"],
            "name": "Signal counts deployment",
            "mode": "signal",
            "symbols": ["000001.SZ"],
        },
    ).json()
    now = datetime.now()
    settings = get_settings()
    engine = create_engine(f"sqlite:///{settings.database_path}")
    try:
        with engine.begin() as connection:
            connection.execute(
                StrategySignalRow.__table__.insert(),
                [
                    {
                        "id": "ssig_buy_1",
                        "deployment_id": deployment["id"],
                        "job_instance_id": None,
                        "strategy_version_id": strategy["strategy_version_id"],
                        "signal_datetime": now,
                        "action_json": {"action": "buy", "symbol": "000001.SZ", "size": 10},
                        "status": "generated",
                        "reason": None,
                        "created_at": now,
                    },
                    {
                        "id": "ssig_buy_2",
                        "deployment_id": deployment["id"],
                        "job_instance_id": None,
                        "strategy_version_id": strategy["strategy_version_id"],
                        "signal_datetime": now,
                        "action_json": {"action": "buy", "symbol": "000002.SZ", "size": 20},
                        "status": "generated",
                        "reason": None,
                        "created_at": now,
                    },
                    {
                        "id": "ssig_close_1",
                        "deployment_id": deployment["id"],
                        "job_instance_id": None,
                        "strategy_version_id": strategy["strategy_version_id"],
                        "signal_datetime": now,
                        "action_json": {"action": "close", "symbol": "000001.SZ"},
                        "status": "generated",
                        "reason": None,
                        "created_at": now,
                    },
                ],
            )
    finally:
        engine.dispose()

    response = client.get(f"/api/strategy-deployments/{deployment['id']}/signals")
    filtered_response = client.get(
        f"/api/strategy-deployments/{deployment['id']}/signals",
        params={"action": "buy"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] == 3
    assert {item["action"]: item["count"] for item in payload["action_counts"]} == {
        "buy": 2,
        "sell": 0,
        "close": 1,
        "cancel": 0,
    }
    assert filtered_response.status_code == 200
    filtered_payload = filtered_response.json()
    assert filtered_payload["total"] == 2
    assert {item["action"]["action"] for item in filtered_payload["items"]} == {"buy"}
    assert {item["action"]: item["count"] for item in filtered_payload["action_counts"]}[
        "close"
    ] == 1


def test_strategy_deployment_persists_rejected_non_hold_actions(client: TestClient) -> None:
    payload = strategy_create_payload()
    payload["source_code"] = "\n".join(
        [
            "def chatq_init(context):",
            "    return {}",
            "",
            "def chatq_next(context, state):",
            "    symbol = context['symbols'][0]",
            "    return {",
            "        'actions': [",
            "            {'action': 'hold', 'reason': 'no_signal'},",
            "            {'action': 'buy', 'size': 10, 'reason': 'missing_symbol'},",
            "            {'action': 'dance', 'foo': 'bar'},",
            "            {'action': 'sell', 'symbol': symbol, 'size': 5, 'reason': 'valid_sell'},",
            "        ],",
            "        'state': state,",
            "    }",
        ]
    )
    created = client.post("/api/strategies", json=payload).json()
    strategy = client.get("/api/strategies?project_id=project_test").json()[0]
    deployment = client.post(
        "/api/strategy-deployments",
        json={
            "project_id": "project_test",
            "strategy_id": created["strategy_id"],
            "strategy_version_id": strategy["strategy_version_id"],
            "name": "Rejected action deployment",
            "mode": "signal",
            "symbols": ["000001.SZ"],
        },
    ).json()

    result = asyncio.run(_execute_static_strategy_deployment(deployment["id"]))
    response = client.get(f"/api/strategy-deployments/{deployment['id']}/signals")

    assert result.payload["signal_count"] == 3
    assert result.payload["generated_count"] == 1
    assert result.payload["rejected_count"] == 2
    payload = response.json()
    assert payload["total"] == 3
    signals = sorted(payload["items"], key=lambda item: item["action"]["action"])
    assert [signal["status"] for signal in signals] == ["rejected", "rejected", "generated"]
    assert [signal["action"]["action"] for signal in signals] == ["buy", "dance", "sell"]
    assert all(signal["action"]["action"] != "hold" for signal in signals)


async def _execute_static_strategy_deployment(deployment_id: str):
    async with get_session_factory()() as db:
        return await execute_strategy_deployment_tick(
            db,
            deployment_id=deployment_id,
            trigger=StrategyRuntimeTrigger(
                instance_id="inst_test_rejected_actions",
                scheduled_for=datetime.now(),
                payload={},
            ),
            context_provider=_StaticDeploymentContextProvider(),
        )


class _StaticDeploymentContextProvider:
    async def load_context(self, db, *, deployment, trigger):
        del db, deployment, trigger
        return StrategyDeploymentRuntimeContext(
            history={},
            current_bars={},
            bars={},
            cash=100000,
            portfolio_value=100000,
        )


def strategy_create_payload(
    *,
    fast_period: int = 20,
    slow_period: int = 60,
    volatility_filter: str = "medium",
    strategy_mode: str = "single_symbol",
) -> dict[str, object]:
    return {
        "project_id": "project_test",
        "name": "均线突破策略",
        "description": "短期均线上穿长期均线买入，下穿卖出",
        "source_code": "\n".join(
            [
                "from app.service.strategy.protocol import ChatQBarContext, ChatQInitContext, ChatQNextResult, ChatQState",
                "",
                "def chatq_params():",
                "    return [",
                chatq_param_source("fast_period", "integer", fast_period, "短期均线周期"),
                chatq_param_source("slow_period", "integer", slow_period, "长期均线周期"),
                chatq_param_source(
                    "volatility_filter",
                    "string",
                    volatility_filter,
                    "波动过滤",
                ),
                "    ]",
                "",
                "def chatq_init(context: ChatQInitContext) -> ChatQState:",
                "    return {}",
                "",
                "def chatq_next(context: ChatQBarContext, state: ChatQState) -> ChatQNextResult:",
                "    symbol = context['symbols'][0]",
                "    params = context['params']",
                "    bars = context['bars'][symbol]",
                "    if len(bars) < params['slow_period']:",
                "        return {'actions': [], 'state': state}",
                "    fast_ma = bars['close'].tail(params['fast_period']).mean()",
                "    slow_ma = bars['close'].tail(params['slow_period']).mean()",
                "    position = context['positions'].get(symbol, {'size': 0})",
                "    if position['size'] == 0 and fast_ma > slow_ma:",
                "        return {'actions': [{'action': 'buy', 'symbol': symbol, 'size': 10, 'reason': 'ma_cross_up'}], 'state': state}",
                "    if position['size'] > 0 and fast_ma < slow_ma:",
                "        return {'actions': [{'action': 'close', 'symbol': symbol, 'reason': 'ma_cross_down'}], 'state': state}",
                "    return {'actions': [], 'state': state}",
            ]
        ),
        "strategy_mode": strategy_mode,
        "risk_notes": ["历史回测不代表未来收益，不构成投资建议"],
    }


def strategy_version_payload(
    *,
    fast_period: int = 20,
    slow_period: int = 60,
    volatility_filter: str = "medium",
    strategy_mode: str = "single_symbol",
) -> dict[str, object]:
    payload = strategy_create_payload(
        fast_period=fast_period,
        slow_period=slow_period,
        volatility_filter=volatility_filter,
        strategy_mode=strategy_mode,
    )
    payload.pop("name")
    payload.pop("description")
    payload.pop("project_id")
    return payload


def chatq_param_source(
    name: str,
    param_type: str,
    default: object,
    label: str,
) -> str:
    return (
        "        "
        f'{{"name": {name!r}, "type": {param_type!r}, '
        f'"default": {default!r}, "label": {label!r}}},'
    )
