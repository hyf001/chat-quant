import asyncio
from typing import Dict, Any
from fastapi import APIRouter
from pydantic import BaseModel
from app.common.types import AgentType

router = APIRouter(prefix="/api/settings", tags=["settings"])

class CLIStatusResponse(BaseModel):
    cli_id: str
    installed: bool
    version: str | None = None
    error: str | None = None


async def check_cli_installation(cli_id: str, command: list) -> CLIStatusResponse:
    """단일 CLI의 설치 상태를 확인합니다."""
    try:
        # subprocess를 비동기로 실행
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode == 0:
            # 성공적으로 실행된 경우
            version_output = stdout.decode().strip()
            # 버전 정보에서 실제 버전 번호 추출 (첫 번째 라인만 사용)
            version = version_output.split('\n')[0] if version_output else "installed"
            
            return CLIStatusResponse(
                cli_id=cli_id,
                installed=True,
                version=version
            )
        else:
            # 명령어 실행은 되었지만 에러 리턴 코드
            error_msg = stderr.decode().strip() if stderr else f"Command failed with code {process.returncode}"
            return CLIStatusResponse(
                cli_id=cli_id,
                installed=False,
                error=error_msg
            )
            
    except FileNotFoundError:
        # 명령어를 찾을 수 없는 경우 (설치되지 않음)
        return CLIStatusResponse(
            cli_id=cli_id,
            installed=False,
            error="Command not found"
        )
    except Exception as e:
        # 기타 예외
        return CLIStatusResponse(
            cli_id=cli_id,
            installed=False,
            error=str(e)
        )


@router.get("/cli-status")
async def get_cli_status() -> Dict[str, Any]:
    """ 校验客户端是否可用 """
    results = {}

    cli_types = [AgentType.NEXT_JS,AgentType.ANALYIS,AgentType.FIN_ANALYSIS]
    AgentType.__class__.__iter__

    # CLI 확인
    for cli_type in cli_types:
        results[cli_type.value] = {
            "installed": True,
            "version": None,
            "error": None,
            "checking": False
        }

    return results


# 默认使用数据分析智能体
GLOBAL_SETTINGS = {
    "default_cli": AgentType.ANALYIS.value,
    "cli_settings": {
        "agent": {"model": "claude-sonnet-4-5"}
    }
}

class GlobalSettingsModel(BaseModel):
    default_cli: str
    cli_settings: Dict[str, Any]


@router.get("/global")
async def get_global_settings() -> Dict[str, Any]:
    """글로벌 설정을 반환합니다."""
    return GLOBAL_SETTINGS


@router.put("/global")
async def update_global_settings(settings: GlobalSettingsModel) -> Dict[str, Any]:
    """글로벌 설정을 업데이트합니다."""
    global GLOBAL_SETTINGS
    
    GLOBAL_SETTINGS.update({
        "default_cli": settings.default_cli,
        "cli_settings": settings.cli_settings
    })
    
    return {"success": True, "settings": GLOBAL_SETTINGS}
