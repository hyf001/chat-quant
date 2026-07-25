from __future__ import annotations

import ast
import importlib.util
import sys
import traceback
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from app.core.config import Settings
from app.infrastructure.runtime.artifact_collector import ArtifactCollector
from app.infrastructure.runtime.process_runner import ProcessRunner, ProcessRunOutput
from app.infrastructure.runtime.sandbox import RuntimeSandbox, RuntimeSandboxError, RuntimeWorkspace
from app.infrastructure.runtime.schema_validator import RuntimeSchemaValidator
from app.schemas.contracts.execution_result import ExecutionResult, RuntimeErrorInfo
from app.schemas.contracts.runtime_health import RuntimeHealthResponse
from app.schemas.contracts.runtime_specs import BacktestRunSpec, PythonExecutionSpec


class PythonRuntimeService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.sandbox = RuntimeSandbox(settings.runtime_root)
        self.runner = ProcessRunner(
            stdout_limit_bytes=settings.runtime_stdout_limit_bytes,
            grace_seconds=settings.runtime_timeout_grace_seconds,
        )
        self.collector = ArtifactCollector(
            max_files=settings.runtime_max_output_files,
            max_file_bytes=settings.runtime_max_artifact_bytes,
        )
        self.validator = RuntimeSchemaValidator()
        self._results: dict[str, ExecutionResult] = {}

    async def execute_python_artifact(self, spec: PythonExecutionSpec) -> ExecutionResult:
        workspace: RuntimeWorkspace | None = None
        started_at = datetime.now(tz=ZoneInfo("Asia/Shanghai"))
        try:
            workspace = self.sandbox.create_workspace(spec, purpose=spec.purpose)
            self._preflight_python_files(workspace)
            command = self.sandbox.prepare_command(
                workspace,
                python_executable=sys.executable,
                entrypoint=spec.entrypoint,
                args=spec.args,
            )
            env = self.sandbox.build_environment(workspace, spec.env)
            process_output = await self.runner.run(
                run_id=workspace.run_id,
                command=command,
                cwd=workspace.work_dir,
                env=env,
                timeout_seconds=spec.timeout_seconds,
            )
            schema_validation = self._merge_validations(
                self.validator.validate_optional_json_result(workspace.output_dir),
                self.validator.validate_expected_outputs(
                    workspace.output_dir,
                    spec.expected_outputs,
                ),
            )
            result = self._build_result(
                workspace=workspace,
                command=command,
                process_output=process_output,
                schema_validation=schema_validation,
                metadata={
                    "chat_session_id": spec.chat_session_id,
                    "source_sdk_session_id": spec.source_sdk_session_id,
                    "source_sdk_message_uuid": spec.source_sdk_message_uuid,
                    "source_sdk_tool_use_id": spec.source_sdk_tool_use_id,
                    "code_artifact_id": spec.code_artifact_id,
                    "purpose": spec.purpose,
                    "uses_inline_code_files": bool(spec.code_files),
                },
            )
        except Exception as exc:
            result = self._build_prepare_failure(
                run_id=workspace.run_id if workspace else "rt_prepare_failed",
                started_at=started_at,
                workspace=workspace,
                exc=exc,
            )
        self._results[result.run_id] = result
        return result

    async def execute_backtest_spec(self, spec: BacktestRunSpec) -> ExecutionResult:
        workspace: RuntimeWorkspace | None = None
        started_at = datetime.now(tz=ZoneInfo("Asia/Shanghai"))
        try:
            workspace = self.sandbox.create_workspace(spec, purpose="backtest")
            self._preflight_python_files(workspace)
            command = [
                sys.executable,
                "-m",
                "app.infrastructure.runtime.backtest_runner",
                "--spec",
                str(workspace.input_dir / "backtest_spec.json"),
                "--output-dir",
                str(workspace.output_dir),
            ]
            env = self.sandbox.build_environment(workspace, {})
            process_output = await self.runner.run(
                run_id=workspace.run_id,
                command=command,
                cwd=workspace.code_dir,
                env=env,
                timeout_seconds=120,
            )
            schema_validation = self.validator.validate_backtest_result(workspace.output_dir)
            result = self._build_result(
                workspace=workspace,
                command=command,
                process_output=process_output,
                schema_validation=schema_validation,
                metadata={
                    "backtest_run_id": spec.backtest_run_id,
                    "strategy_version_id": spec.strategy_version_id,
                    "code_artifact_id": spec.code_artifact_id,
                    "purpose": "backtest",
                    "uses_inline_code_files": bool(spec.code_files),
                },
            )
        except Exception as exc:
            result = self._build_prepare_failure(
                run_id=workspace.run_id if workspace else "rt_prepare_failed",
                started_at=started_at,
                workspace=workspace,
                exc=exc,
            )
        self._results[result.run_id] = result
        return result

    async def cancel_runtime_run(self, run_id: str) -> dict[str, str]:
        canceled = await self.runner.cancel(run_id)
        return {"run_id": run_id, "status": "canceled" if canceled else "not_running"}

    def get_runtime_health(self) -> RuntimeHealthResponse:
        self.settings.runtime_root.mkdir(parents=True, exist_ok=True)
        packages = {
            package_name: self._package_status(package_name)
            for package_name in ("akshare", "pandas", "backtrader")
        }
        return RuntimeHealthResponse(
            status="ok",
            python_version=sys.version.split()[0],
            packages=packages,
            runtime_root_writable=self._is_writable(self.settings.runtime_root),
        )

    def get_result(self, run_id: str) -> ExecutionResult | None:
        return self._results.get(run_id)

    def _build_result(
        self,
        *,
        workspace: RuntimeWorkspace,
        command: list[str],
        process_output: ProcessRunOutput,
        schema_validation: dict[str, object],
        metadata: dict[str, object],
    ) -> ExecutionResult:
        artifact_result = self.collector.collect(workspace.output_dir)
        validation_passed = bool(schema_validation.get("passed", False))
        status = "succeeded"
        error = None
        if process_output.timed_out:
            status = "timeout"
            error = RuntimeErrorInfo(
                code="PROCESS_TIMEOUT",
                message="Python process exceeded timeout and was terminated",
                phase="timeout",
            )
        elif process_output.canceled:
            status = "canceled"
            error = RuntimeErrorInfo(
                code="PROCESS_CANCELED",
                message="Python process was canceled",
                phase="timeout",
            )
        elif process_output.exit_code != 0:
            status = "failed"
            error = RuntimeErrorInfo(
                code="PROCESS_EXIT_NONZERO",
                message="Python process exited with a non-zero status",
                detail=process_output.stderr[-4000:] or None,
                traceback=self._extract_traceback(process_output.stderr),
                phase="execute",
            )
        elif not validation_passed:
            status = "failed"
            error = RuntimeErrorInfo(
                code="RESULT_SCHEMA_INVALID",
                message="Runtime result schema validation failed",
                detail=str(schema_validation.get("errors", [])),
                phase="schema_validation",
            )

        warnings = list(artifact_result.warnings)
        metadata_with_warnings = dict(metadata)
        if warnings:
            metadata_with_warnings["warnings"] = warnings

        return ExecutionResult(
            run_id=workspace.run_id,
            status=status,
            exit_code=process_output.exit_code,
            stdout=process_output.stdout,
            stderr=process_output.stderr,
            artifacts=artifact_result.artifacts,
            error=error,
            duration_ms=process_output.duration_ms,
            started_at=process_output.started_at,
            completed_at=process_output.completed_at,
            python_version=sys.version.split()[0],
            command=command,
            cwd=str(workspace.work_dir),
            output_dir=str(workspace.output_dir),
            schema_validation=schema_validation,
            metadata=metadata_with_warnings,
        )

    def _build_prepare_failure(
        self,
        *,
        run_id: str,
        started_at: datetime,
        workspace: RuntimeWorkspace | None,
        exc: Exception,
    ) -> ExecutionResult:
        completed_at = datetime.now(tz=ZoneInfo("Asia/Shanghai"))
        code = "PATH_OUT_OF_BOUNDS" if isinstance(exc, RuntimeSandboxError) else "PREPARE_FAILED"
        return ExecutionResult(
            run_id=run_id,
            status="failed",
            exit_code=None,
            stdout="",
            stderr="",
            artifacts=[],
            error=RuntimeErrorInfo(
                code=code,
                message=str(exc),
                traceback=traceback.format_exc(),
                phase="prepare",
            ),
            duration_ms=int((completed_at - started_at).total_seconds() * 1000),
            started_at=started_at,
            completed_at=completed_at,
            python_version=sys.version.split()[0],
            command=[],
            cwd=str(workspace.work_dir if workspace else self.settings.runtime_root),
            output_dir=str(workspace.output_dir if workspace else self.settings.runtime_root),
            schema_validation={"schema": "ExecutionPrepare", "passed": False, "errors": [str(exc)]},
            metadata={},
        )

    def _merge_validations(self, *validations: dict[str, object]) -> dict[str, object]:
        errors = []
        for validation in validations:
            errors.extend(validation.get("errors", []))
        schema_names = [
            str(validation.get("schema", "unknown"))
            for validation in validations
        ]
        return {
            "schema": "+".join(schema_names),
            "passed": not errors,
            "errors": errors,
        }

    def _preflight_python_files(self, workspace: RuntimeWorkspace) -> None:
        for source_path in workspace.code_dir.rglob("*.py"):
            tree = ast.parse(source_path.read_text(encoding="utf-8"), filename=str(source_path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import | ast.ImportFrom):
                    names = [alias.name for alias in node.names]
                    if any(name.split(".")[0] in {"subprocess", "socket"} for name in names):
                        raise ValueError("Python code imports blocked process or socket modules")
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                    if isinstance(node.func.value, ast.Name):
                        call_name = f"{node.func.value.id}.{node.func.attr}"
                        if call_name in {"os.system", "os.popen", "requests.post"}:
                            raise ValueError(f"Python code uses blocked call: {call_name}")

    def _extract_traceback(self, stderr: str) -> str | None:
        marker = "Traceback (most recent call last):"
        index = stderr.rfind(marker)
        if index == -1:
            return None
        return stderr[index:]

    def _package_status(self, package_name: str) -> str:
        return "installed" if importlib.util.find_spec(package_name) else "missing"

    def _is_writable(self, path: Path) -> bool:
        probe = path / ".write_probe"
        try:
            probe.write_text("ok", encoding="utf-8")
            probe.unlink(missing_ok=True)
            return True
        except OSError:
            return False
