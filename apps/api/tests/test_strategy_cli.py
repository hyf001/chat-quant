import json
from pathlib import Path

import pytest
from app.cli.main import main
from app.domain.strategies.repository import strategy_repository
from tests.test_strategy_api import strategy_package


def test_strategy_cli_create_get_validate_and_copy(
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
) -> None:
    package_file = tmp_path / "strategy_package.json"
    package_file.write_text(json.dumps(strategy_package(), ensure_ascii=False), encoding="utf-8")

    create_exit_code = main(
        [
            "strategy",
            "create",
            "--conversation-id",
            "conv_cli",
            "--package-file",
            str(package_file),
        ]
    )
    created = json.loads(capsys.readouterr().out)

    assert create_exit_code == 0
    assert created["version"] == 1
    assert created["status"] == "draft"

    get_exit_code = main(
        ["strategy", "get", "--strategy-version-id", created["strategy_version_id"]]
    )
    version = json.loads(capsys.readouterr().out)

    assert get_exit_code == 0
    assert version["entrypoint"] == "strategy.py:GeneratedStrategy"

    validate_exit_code = main(
        ["strategy", "validate", "--strategy-version-id", created["strategy_version_id"]]
    )
    validation = json.loads(capsys.readouterr().out)

    assert validate_exit_code == 0
    assert validation["status"] == "validated"

    copy_exit_code = main(
        [
            "strategy",
            "copy",
            "--strategy-version-id",
            created["strategy_version_id"],
            "--mode",
            "summary",
        ]
    )
    copied = json.loads(capsys.readouterr().out)

    assert copy_exit_code == 0
    assert copied["mode"] == "summary"
    assert "不构成投资建议" in copied["summary"]


def test_strategy_cli_returns_json_error_for_invalid_package(
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
) -> None:
    package_file = tmp_path / "strategy_package.json"
    package = strategy_package()
    package["entrypoint"] = "../bad.py:GeneratedStrategy"
    package_file.write_text(json.dumps(package, ensure_ascii=False), encoding="utf-8")

    exit_code = main(
        [
            "strategy",
            "create",
            "--conversation-id",
            "conv_cli",
            "--package-file",
            str(package_file),
        ]
    )
    output = json.loads(capsys.readouterr().out)

    assert exit_code == 1
    assert output["error_code"] == "STRATEGY_PACKAGE_INVALID"
    assert strategy_repository.list_strategies("demo-user", "default-project") == []
