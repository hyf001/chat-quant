from fastapi.testclient import TestClient


def test_create_strategy_returns_draft_first_version(client: TestClient) -> None:
    response = client.post(
        "/api/strategies",
        json={
            "chat_session_id": "conv_demo",
            "package": strategy_package(),
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["strategy_id"].startswith("str_")
    assert data["strategy_version_id"].startswith("stv_")
    assert data["version"] == 1
    assert data["status"] == "draft"
    assert data["entrypoint"] == "strategy.py:GeneratedStrategy"


def test_create_strategy_rejects_default_param_outside_schema(client: TestClient) -> None:
    package = strategy_package()
    package["default_params"]["fast_period"] = 1

    response = client.post(
        "/api/strategies",
        json={"chat_session_id": "conv_demo", "package": package},
    )

    assert response.status_code == 422


def test_create_strategy_version_increments_and_preserves_parent(client: TestClient) -> None:
    created = client.post(
        "/api/strategies",
        json={"chat_session_id": "conv_demo", "package": strategy_package()},
    ).json()
    next_package = strategy_package(
        logic_summary="MA 25/80 突破并使用较强波动过滤",
        fast_period=25,
        slow_period=80,
        volatility_filter="strong",
    )

    response = client.post(
        f"/api/strategies/{created['strategy_id']}/versions",
        json={
            "parent_version_id": created["strategy_version_id"],
            "change_summary": "加入更强波动过滤",
            "package": next_package,
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["version"] == 2
    detail = client.get(f"/api/strategies/{created['strategy_id']}").json()
    assert detail["strategy"]["current_version_id"] == data["strategy_version_id"]
    assert detail["versions"][1]["parent_version_id"] == created["strategy_version_id"]
    assert detail["versions"][1]["change_summary"] == "加入更强波动过滤"


def test_validate_strategy_version_marks_version_validated(client: TestClient) -> None:
    created = client.post(
        "/api/strategies",
        json={"chat_session_id": "conv_demo", "package": strategy_package()},
    ).json()

    response = client.post(f"/api/strategy-versions/{created['strategy_version_id']}/validate")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "validated"
    assert [check["name"] for check in data["checks"]] == [
        "entrypoint",
        "params_schema",
        "code_reference",
        "smoke_test",
    ]
    version = client.get(f"/api/strategy-versions/{created['strategy_version_id']}").json()
    assert version["status"] == "validated"
    assert version["validated_at"] is not None


def test_copy_summary_records_without_new_strategy(client: TestClient) -> None:
    created = client.post(
        "/api/strategies",
        json={"chat_session_id": "conv_demo", "package": strategy_package()},
    ).json()

    response = client.post(
        f"/api/strategy-versions/{created['strategy_version_id']}/copy",
        json={"mode": "summary"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["mode"] == "summary"
    assert data["target_strategy_id"] is None
    assert "不构成投资建议" in data["summary"]
    assert client.get("/api/strategies").json()[0]["strategy_id"] == created["strategy_id"]


def test_copy_new_strategy_creates_independent_asset(client: TestClient) -> None:
    created = client.post(
        "/api/strategies",
        json={"chat_session_id": "conv_demo", "package": strategy_package()},
    ).json()

    response = client.post(
        f"/api/strategy-versions/{created['strategy_version_id']}/copy",
        json={"mode": "new_strategy", "target_chat_session_id": "conv_copy"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["target_strategy_id"].startswith("str_")
    strategies = client.get("/api/strategies").json()
    assert {strategy["strategy_id"] for strategy in strategies} == {
        created["strategy_id"],
        data["target_strategy_id"],
    }


def test_update_metadata_does_not_create_new_version(client: TestClient) -> None:
    created = client.post(
        "/api/strategies",
        json={"chat_session_id": "conv_demo", "package": strategy_package()},
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
    assert len(detail["versions"]) == 1
    assert detail["strategy"]["current_version_id"] == created["strategy_version_id"]


def test_archived_strategy_rejects_new_version(client: TestClient) -> None:
    created = client.post(
        "/api/strategies",
        json={"chat_session_id": "conv_demo", "package": strategy_package()},
    ).json()
    client.patch(
        f"/api/strategies/{created['strategy_id']}",
        json={"status": "archived"},
    )

    response = client.post(
        f"/api/strategies/{created['strategy_id']}/versions",
        json={"package": strategy_package(fast_period=30, slow_period=90)},
    )

    assert response.status_code == 409
    assert response.json()["detail"]["error_code"] == "STRATEGY_ARCHIVED"


def test_deleted_strategy_is_hidden_from_list(client: TestClient) -> None:
    created = client.post(
        "/api/strategies",
        json={"chat_session_id": "conv_demo", "package": strategy_package()},
    ).json()

    response = client.patch(
        f"/api/strategies/{created['strategy_id']}",
        json={"status": "deleted"},
    )

    assert response.status_code == 200
    assert client.get("/api/strategies").json() == []


def strategy_package(
    *,
    logic_summary: str = "MA 20/60 突破并使用中等波动过滤",
    fast_period: int = 20,
    slow_period: int = 60,
    volatility_filter: str = "medium",
) -> dict[str, object]:
    return {
        "name": "均线突破策略",
        "description": "短期均线上穿长期均线买入，下穿卖出",
        "strategy_type": "ma_cross",
        "entrypoint": "strategy.py:GeneratedStrategy",
        "code_artifact_id": "code_demo",
        "params_schema": {
            "fast_period": {
                "type": "integer",
                "title": "短期均线周期",
                "default": fast_period,
                "minimum": 2,
                "maximum": 250,
                "ui": {"control": "number", "unit": "日"},
            },
            "slow_period": {
                "type": "integer",
                "title": "长期均线周期",
                "default": slow_period,
                "minimum": 5,
                "maximum": 500,
                "ui": {"control": "number", "unit": "日"},
            },
            "volatility_filter": {
                "type": "string",
                "title": "波动过滤",
                "enum": ["off", "medium", "strong"],
                "default": volatility_filter,
                "ui": {"control": "select"},
            },
        },
        "default_params": {
            "fast_period": fast_period,
            "slow_period": slow_period,
            "volatility_filter": volatility_filter,
        },
        "logic_summary": logic_summary,
        "risk_notes": ["历史回测不代表未来收益，不构成投资建议"],
    }
