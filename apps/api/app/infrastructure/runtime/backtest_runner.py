from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Chat-Quant backtest runner")
    parser.add_argument("--spec", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    _import_entrypoint(spec["entrypoint"])
    Path(args.output_dir).mkdir(parents=True, exist_ok=True)
    raise RuntimeError(
        "Real market data adapter is not configured; backtest execution did not run."
    )


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


if __name__ == "__main__":
    main()
