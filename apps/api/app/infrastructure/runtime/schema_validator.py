from __future__ import annotations

import json
from math import isfinite
from pathlib import Path

from pydantic import ValidationError

from app.schemas.contracts.backtest_result import BacktestResultPayload
from app.schemas.contracts.json_types import JsonObject, JsonValue


class RuntimeSchemaValidator:
    def validate_optional_json_result(self, output_dir: Path) -> JsonObject:
        result_path = output_dir / "result.json"
        if not result_path.exists():
            return {"schema": "OptionalJson", "passed": True, "errors": []}
        try:
            payload = self._load_json(result_path)
            self._reject_non_finite(payload)
        except ValueError as exc:
            return {"schema": "OptionalJson", "passed": False, "errors": [str(exc)]}
        return {"schema": "OptionalJson", "passed": True, "errors": []}

    def validate_expected_outputs(
        self,
        output_dir: Path,
        expected_outputs: list[str],
    ) -> JsonObject:
        missing = []
        for expected_output in expected_outputs:
            path = Path(expected_output)
            if path.is_absolute() or ".." in path.parts or not (output_dir / path).is_file():
                missing.append(expected_output)
        return {
            "schema": "ExpectedOutputs",
            "passed": len(missing) == 0,
            "errors": [f"Missing expected output: {path}" for path in missing],
        }

    def validate_backtest_result(self, output_dir: Path) -> JsonObject:
        result_path = output_dir / "result.json"
        if not result_path.exists():
            return {
                "schema": "BacktestResultPayload",
                "passed": False,
                "errors": ["result.json is required for backtest execution"],
            }
        try:
            payload = self._load_json(result_path)
            self._reject_non_finite(payload)
            BacktestResultPayload.model_validate(payload)
        except (ValueError, ValidationError) as exc:
            return {
                "schema": "BacktestResultPayload",
                "passed": False,
                "errors": [str(exc)],
            }
        return {"schema": "BacktestResultPayload", "passed": True, "errors": []}

    def _load_json(self, path: Path) -> JsonValue:
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path.name} is not valid JSON: {exc.msg}") from exc

    def _reject_non_finite(self, value: JsonValue) -> None:
        if isinstance(value, float) and not isfinite(value):
            raise ValueError("JSON output must not contain NaN or Infinity")
        if isinstance(value, list):
            for item in value:
                self._reject_non_finite(item)
        if isinstance(value, dict):
            for item in value.values():
                self._reject_non_finite(item)
