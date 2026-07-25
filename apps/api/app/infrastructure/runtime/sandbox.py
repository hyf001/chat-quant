from __future__ import annotations

import json
import os
import re
import secrets
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from app.schemas.contracts.runtime_specs import (
    BacktestRunSpec,
    PythonExecutionSpec,
    RuntimeCodeFile,
)


class RuntimeSandboxError(ValueError):
    code = "PATH_OUT_OF_BOUNDS"


@dataclass(frozen=True)
class RuntimeWorkspace:
    run_id: str
    root_dir: Path
    input_dir: Path
    code_dir: Path
    work_dir: Path
    output_dir: Path
    tmp_dir: Path
    manifest_path: Path


class RuntimeSandbox:
    def __init__(self, runtime_root: Path) -> None:
        self.runtime_root = runtime_root.resolve()

    def create_workspace(
        self,
        spec: PythonExecutionSpec | BacktestRunSpec,
        *,
        purpose: str,
    ) -> RuntimeWorkspace:
        run_id = self._new_run_id()
        root_dir = self.runtime_root / "runs" / run_id
        workspace = RuntimeWorkspace(
            run_id=run_id,
            root_dir=root_dir,
            input_dir=root_dir / "input",
            code_dir=root_dir / "code",
            work_dir=root_dir / "work",
            output_dir=root_dir / "output",
            tmp_dir=root_dir / "tmp",
            manifest_path=root_dir / "manifest.json",
        )
        for directory in (
            workspace.input_dir,
            workspace.code_dir,
            workspace.work_dir,
            workspace.output_dir,
            workspace.tmp_dir,
        ):
            directory.mkdir(parents=True, exist_ok=False)

        self._materialize_code_files(workspace, spec.code_files)
        self._write_json(workspace.input_dir / "stdin.json", self._stdin_payload(spec))
        if isinstance(spec, BacktestRunSpec):
            self._write_json(
                workspace.input_dir / "backtest_spec.json",
                spec.model_dump(mode="json"),
            )

        manifest = {
            "run_id": run_id,
            "purpose": purpose,
            "entrypoint": spec.entrypoint,
            "code_artifact_id": spec.code_artifact_id,
            "created_at": datetime.now(tz=ZoneInfo("Asia/Shanghai")).isoformat(),
            "env_keys": sorted(self.build_environment(workspace, {}).keys()),
        }
        self._write_json(workspace.manifest_path, manifest)
        return workspace

    def prepare_command(
        self,
        workspace: RuntimeWorkspace,
        *,
        python_executable: str,
        entrypoint: str,
        args: list[str],
    ) -> list[str]:
        if ":" in entrypoint:
            file_path, function_name = entrypoint.split(":", maxsplit=1)
            source_path = self.resolve_code_path(workspace, file_path)
            if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", function_name):
                raise RuntimeSandboxError("Entrypoint function name is invalid")
            wrapper_path = workspace.work_dir / "__chatq_function_entrypoint.py"
            wrapper_path.write_text(
                "\n".join(
                    [
                        "import importlib.util",
                        "import json",
                        "import os",
                        "from pathlib import Path",
                        f"source_path = {str(source_path)!r}",
                        f"function_name = {function_name!r}",
                        "stdin_path = Path(os.environ['CHATQ_STDIN_JSON'])",
                        "output_path = Path(os.environ['CHATQ_RESULT_JSON'])",
                        "spec = importlib.util.spec_from_file_location(",
                        "    'chatq_user_module', source_path",
                        ")",
                        "module = importlib.util.module_from_spec(spec)",
                        "assert spec and spec.loader",
                        "spec.loader.exec_module(module)",
                        "payload = json.loads(stdin_path.read_text(encoding='utf-8'))",
                        "result = getattr(module, function_name)(payload)",
                        "if result is not None and not output_path.exists():",
                        "    output_path.write_text(",
                        "        json.dumps(result, ensure_ascii=False),",
                        "        encoding='utf-8',",
                        "    )",
                    ]
                ),
                encoding="utf-8",
            )
            return [python_executable, str(wrapper_path), *args]

        if entrypoint.endswith(".py"):
            source_path = self.resolve_code_path(workspace, entrypoint)
            return [python_executable, str(source_path), *args]

        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)*", entrypoint):
            raise RuntimeSandboxError("Entrypoint must be a Python file, module, or file:function")
        return [python_executable, "-m", entrypoint, *args]

    def build_environment(
        self,
        workspace: RuntimeWorkspace,
        requested_env: dict[str, str],
    ) -> dict[str, str]:
        inherited_keys = ("PATH", "HOME", "LANG", "LC_ALL", "VIRTUAL_ENV", "PYTHONPATH")
        env = {key: value for key in inherited_keys if (value := os.environ.get(key))}
        env.update(
            {
                "CHATQ_RUNTIME_RUN_ID": workspace.run_id,
                "CHATQ_INPUT_DIR": str(workspace.input_dir),
                "CHATQ_OUTPUT_DIR": str(workspace.output_dir),
                "CHATQ_RESULT_JSON": str(workspace.output_dir / "result.json"),
                "CHATQ_STDIN_JSON": str(workspace.input_dir / "stdin.json"),
                "CHATQ_BACKTEST_SPEC": str(workspace.input_dir / "backtest_spec.json"),
                "CHATQ_MARKET_DATA_MODE": "akshare",
                "CHATQ_NO_REAL_TRADING": "1",
                "PYTHONUNBUFFERED": "1",
                "MPLBACKEND": "Agg",
                "TZ": "Asia/Shanghai",
                "PYTHONPATH": self._python_path_with_code(workspace, env.get("PYTHONPATH")),
            }
        )
        blocked_keys = {
            "CHATQ_OUTPUT_DIR",
            "CHATQ_RESULT_JSON",
            "CHATQ_STDIN_JSON",
            "CHATQ_BACKTEST_SPEC",
            "PYTHONPATH",
        }
        for key, value in requested_env.items():
            if key in blocked_keys:
                continue
            forbidden_tokens = ("TOKEN", "SECRET", "PASSWORD", "BROKER", "TRADE")
            if any(token in key.upper() for token in forbidden_tokens):
                continue
            env[key] = value
        return env

    def resolve_code_path(self, workspace: RuntimeWorkspace, relative_path: str) -> Path:
        if Path(relative_path).is_absolute() or ".." in Path(relative_path).parts:
            raise RuntimeSandboxError("Entrypoint path must stay inside the code directory")
        path = (workspace.code_dir / relative_path).resolve()
        code_root = workspace.code_dir.resolve()
        if not path.is_file() or not path.is_relative_to(code_root):
            raise RuntimeSandboxError("Entrypoint file was not found in code directory")
        return path

    def remove_workspace(self, workspace: RuntimeWorkspace) -> None:
        shutil.rmtree(workspace.root_dir, ignore_errors=True)

    def _materialize_code_files(
        self,
        workspace: RuntimeWorkspace,
        code_files: list[RuntimeCodeFile],
    ) -> None:
        # TODO(m3-integration): Resolve CodeArtifact directories from M3 once that module lands.
        for code_file in code_files:
            if Path(code_file.path).is_absolute() or ".." in Path(code_file.path).parts:
                raise RuntimeSandboxError("Code file paths must be relative to the code directory")
            destination = workspace.code_dir / code_file.path
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(code_file.content, encoding="utf-8")

    def _stdin_payload(self, spec: PythonExecutionSpec | BacktestRunSpec) -> dict[str, object]:
        if isinstance(spec, PythonExecutionSpec):
            return spec.stdin_json or {}
        return spec.model_dump(mode="json")

    def _write_json(self, path: Path, payload: object) -> None:
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def _new_run_id(self) -> str:
        stamp = datetime.now(tz=ZoneInfo("Asia/Shanghai")).strftime("%Y%m%d%H%M%S")
        return f"rt_{stamp}_{secrets.token_hex(3)}"

    def _python_path_with_code(self, workspace: RuntimeWorkspace, existing: str | None) -> str:
        api_root = Path(__file__).resolve().parents[3]
        entries = [str(workspace.code_dir), str(api_root)]
        if existing:
            entries.append(existing)
        return os.pathsep.join(entries)
