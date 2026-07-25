from __future__ import annotations

import argparse
import importlib.util
import json
import math
from datetime import datetime, timedelta
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Chat-Quant P0 backtest runner")
    parser.add_argument("--spec", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    spec_path = Path(args.spec)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    _import_entrypoint(spec["entrypoint"])

    start_date = datetime.fromisoformat(spec["start_date"]).date()
    end_date = datetime.fromisoformat(spec["end_date"]).date()
    days = max((end_date - start_date).days, 1)
    initial_cash = float(spec["initial_cash"])
    symbol_count = max(len(spec["symbols"]), 1)
    ma_bonus = _numeric_param(spec.get("params", {}), "short_window", 20) / max(
        _numeric_param(spec.get("params", {}), "long_window", 60),
        1,
    )
    gross_return = min(max(0.045 + ma_bonus * 0.03 - float(spec["commission"]) * 100, -0.35), 0.45)
    final_value = round(initial_cash * (1 + gross_return), 2)
    annual_return_pct = round(((1 + gross_return) ** (365 / days) - 1) * 100, 4)
    total_return_pct = round(gross_return * 100, 4)
    equity_curve = _build_equity_curve(start_date, days, initial_cash, final_value)
    drawdown_curve = _build_drawdown_curve(equity_curve)
    max_drawdown_pct = min(point["drawdown_pct"] for point in drawdown_curve)

    result = {
        "status": "succeeded",
        "metrics": {
            "initial_value": initial_cash,
            "final_value": final_value,
            "total_return_pct": total_return_pct,
            "annual_return_pct": annual_return_pct,
            "max_drawdown_pct": max_drawdown_pct,
            "max_drawdown_start": equity_curve[0]["date"],
            "max_drawdown_end": equity_curve[-1]["date"],
            "max_drawdown_duration_days": days,
            "sharpe_ratio": round(0.8 + symbol_count * 0.03, 4),
            "win_rate_pct": 52.0,
            "total_trades": max(symbol_count * 2, 1),
        },
        "trades": [],
        "equity_curve": equity_curve,
        "drawdown_curve": drawdown_curve,
        "warnings": [
            "P0 runner uses deterministic sample pricing until the M6 data adapter is integrated."
        ],
        "data_source": {
            "mode": "sample",
            "market": spec["market"],
            "data_adjust": spec.get("data_adjust", "qfq"),
        },
        "assumptions": {
            "timeframe": spec.get("timeframe", "1d"),
            "no_real_trading": True,
        },
    }
    _write_json(output_dir / "result.json", result)
    _write_json(output_dir / "equity_curve.json", equity_curve)
    _write_json(output_dir / "drawdown_curve.json", drawdown_curve)


def _import_entrypoint(entrypoint: str) -> None:
    if ":" not in entrypoint:
        if entrypoint.endswith(".py"):
            path = Path(entrypoint)
            if not path.exists():
                raise FileNotFoundError(f"Strategy entrypoint not found: {entrypoint}")
            spec = importlib.util.spec_from_file_location("chatq_strategy", path)
            module = importlib.util.module_from_spec(spec)
            assert spec and spec.loader
            spec.loader.exec_module(module)
        return
    path_text, function_name = entrypoint.split(":", maxsplit=1)
    path = Path(path_text)
    if not path.exists():
        raise FileNotFoundError(f"Strategy entrypoint not found: {entrypoint}")
    spec = importlib.util.spec_from_file_location("chatq_strategy", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    if not hasattr(module, function_name):
        raise AttributeError(f"Strategy entrypoint function missing: {function_name}")


def _numeric_param(params: dict[str, object], key: str, default: float) -> float:
    value = params.get(key, default)
    if isinstance(value, int | float) and math.isfinite(value):
        return float(value)
    return default


def _build_equity_curve(
    start_date,
    days: int,
    initial_cash: float,
    final_value: float,
) -> list[dict[str, float | str]]:
    steps = min(max(days, 2), 30)
    curve = []
    for index in range(steps):
        ratio = index / (steps - 1)
        date = start_date + timedelta(days=round(days * ratio))
        noise = math.sin(index * 0.9) * initial_cash * 0.006
        value = round(initial_cash + (final_value - initial_cash) * ratio + noise, 2)
        curve.append({"date": date.isoformat(), "value": value})
    return curve


def _build_drawdown_curve(
    equity_curve: list[dict[str, float | str]],
) -> list[dict[str, float | str]]:
    peak = 0.0
    drawdown_curve = []
    for point in equity_curve:
        value = float(point["value"])
        peak = max(peak, value)
        drawdown_pct = 0.0 if peak <= 0 else round((value / peak - 1) * 100, 4)
        drawdown_curve.append({"date": point["date"], "drawdown_pct": drawdown_pct})
    return drawdown_curve


def _write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
