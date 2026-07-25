from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from app.core.logging import get_logger

logger = get_logger(__name__)


@dataclass(frozen=True)
class ProcessRunOutput:
    exit_code: int | None
    stdout: str
    stderr: str
    duration_ms: int
    started_at: datetime
    completed_at: datetime
    timed_out: bool = False
    canceled: bool = False


class ProcessRunner:
    def __init__(self, *, stdout_limit_bytes: int, grace_seconds: float) -> None:
        self.stdout_limit_bytes = stdout_limit_bytes
        self.grace_seconds = grace_seconds
        self._active: dict[str, asyncio.subprocess.Process] = {}

    async def run(
        self,
        *,
        run_id: str,
        command: list[str],
        cwd: Path,
        env: dict[str, str],
        timeout_seconds: int,
    ) -> ProcessRunOutput:
        started_at = datetime.now(tz=ZoneInfo("Asia/Shanghai"))
        process = await asyncio.create_subprocess_exec(
            *command,
            cwd=str(cwd),
            env=env,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        self._active[run_id] = process
        timed_out = False
        canceled = False
        try:
            try:
                stdout_bytes, stderr_bytes = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout_seconds,
                )
            except TimeoutError:
                timed_out = True
                logger.warning("process run timed out", extra={"run_id": run_id})
                stdout_bytes, stderr_bytes = await self._terminate(process)
        except asyncio.CancelledError:
            canceled = True
            logger.info("process run cancelled", extra={"run_id": run_id})
            stdout_bytes, stderr_bytes = await self._terminate(process)
        finally:
            self._active.pop(run_id, None)

        completed_at = datetime.now(tz=ZoneInfo("Asia/Shanghai"))
        return ProcessRunOutput(
            exit_code=process.returncode,
            stdout=self._decode_and_truncate(stdout_bytes),
            stderr=self._decode_and_truncate(stderr_bytes),
            duration_ms=int((completed_at - started_at).total_seconds() * 1000),
            started_at=started_at,
            completed_at=completed_at,
            timed_out=timed_out,
            canceled=canceled,
        )

    async def cancel(self, run_id: str) -> bool:
        process = self._active.get(run_id)
        if process is None or process.returncode is not None:
            return False
        await self._terminate(process)
        logger.info("process cancel sent", extra={"run_id": run_id, "found": True})
        return True

    async def _terminate(self, process: asyncio.subprocess.Process) -> tuple[bytes, bytes]:
        if process.returncode is None:
            process.terminate()
            try:
                return await asyncio.wait_for(process.communicate(), timeout=self.grace_seconds)
            except TimeoutError:
                logger.warning("process terminate grace elapsed; killing process")
                process.kill()
        return await process.communicate()

    def _decode_and_truncate(self, content: bytes) -> str:
        if len(content) > self.stdout_limit_bytes:
            content = content[-self.stdout_limit_bytes :]
        return content.decode("utf-8", errors="replace")
