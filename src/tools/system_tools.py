import asyncio
import os
from langchain_core.tools import tool
from typing import Dict, Any, Optional
from src.jupyter import JupyterExecutor
import subprocess

import os
from typing import Optional


from src.utils import logger

log = logger.get_logger("__name__")

executor_by_thread_id : Dict[str,JupyterExecutor] = {}


@tool
def execute_python_code(thread_id:str,code:str) -> Dict[str,Any]:
    """
    在jupyter环境执行python代码，python的版本是3.12。同一个会话执行多次代码，共享变量
    """
    executor = executor_by_thread_id.get(thread_id,JupyterExecutor())
    executor_by_thread_id[thread_id] = executor
    return asyncio.run(executor.execute_code(code))


@tool
def execute_linux_command(command: str, timeout: int = 30, cwd: Optional[str] = None) -> Dict[str, Any]:
    """执行Linux命令行工具

    Args:
        command: 要执行的Linux命令
        timeout: 命令执行超时时间（秒），默认30秒
        cwd: 命令执行的工作目录，默认为None（使用当前目录）

    Returns:
        包含命令执行结果的字典，包括状态、输出和错误信息
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=cwd
        )

        return {
            "status": "success" if result.returncode == 0 else "error",
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "command": command,
            "cwd": cwd or os.getcwd()
        }
    except subprocess.TimeoutExpired:
        return {
            "status": "timeout",
            "return_code": None,
            "stdout": "",
            "stderr": f"Command timed out after {timeout} seconds",
            "command": command,
            "cwd": cwd or os.getcwd()
        }
    except Exception as e:
        return {
            "status": "error",
            "return_code": None,
            "stdout": "",
            "stderr": str(e),
            "command": command,
            "cwd": cwd or os.getcwd()
        }