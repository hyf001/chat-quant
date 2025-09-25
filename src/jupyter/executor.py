import asyncio
import re
from typing import Dict, Any, Optional, List
from jupyter_client.manager import KernelManager
from jupyter_client.client import KernelClient
from jupyter_client.kernelspec import KernelSpecManager
import time


def strip_ansi_codes(text: str) -> str:
    """移除字符串中的ANSI转义序列（颜色代码等）"""
    ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
    return ansi_escape.sub('', text)


def format_error_message(ename: str, evalue: str, traceback_lines: List[str]) -> str:
    """格式化错误信息为更清晰的格式"""
    clean_traceback = [strip_ansi_codes(line) for line in traceback_lines]

    # 过滤掉分隔线
    filtered_lines = []
    for line in clean_traceback:
        if line.strip() == '-' * 75:  # 跳过分隔线
            continue
        if line.strip():  # 只保留非空行
            filtered_lines.append(line.strip())

    # 构建清晰的错误信息
    formatted_lines = []
    for line in filtered_lines:
        if 'Traceback (most recent call last)' in line:
            formatted_lines.append('错误追踪:')
        elif line.startswith('Cell In[') and 'line' in line:
            # 提取行号信息
            if 'line' in line:
                parts = line.split('line')
                if len(parts) > 1:
                    line_info = parts[1].strip()
                    formatted_lines.append(f'  在第 {line_info} 行:')
        elif '-->' in line:
            # 代码行
            code_part = line.split('-->')[-1].strip()
            formatted_lines.append(f'    {code_part}')
        elif line.strip().isdigit():
            # 行号
            continue
        elif line.startswith(ename):
            # 错误详情
            formatted_lines.append(f'错误类型: {ename}')
            formatted_lines.append(f'错误信息: {evalue}')
        else:
            # 其他代码行
            if any(char.isalnum() for char in line):
                formatted_lines.append(f'    {line.strip()}')

    return '\n'.join(formatted_lines)


class JupyterExecutor:
    def __init__(self, kernel_name: str = 'python'):
        self.km: Optional[KernelManager] = None
        self.kc: Optional[KernelClient] = None
        self.is_running = False
        self.kernel_name = kernel_name

    async def start_kernel(self) -> None:
        """启动Jupyter内核"""
        if self.is_running:
            return
        self.km = KernelManager()
        self.km.start_kernel()
        self.kc = self.km.blocking_client()
        self.kc.wait_for_ready()
        self.is_running = True

    async def stop_kernel(self) -> None:
        """停止Jupyter内核"""
        if not self.is_running:
            return

        if self.kc:
            self.kc.stop_channels()
        if self.km:
            await asyncio.get_event_loop().run_in_executor(None, self.km.shutdown_kernel)

        self.is_running = False
        self.km = None
        self.kc = None

    async def execute_code(self, code: str, timeout: int = 30) -> Dict[str, Any]:
        """
        执行代码并返回结果

        Args:
            code: 要执行的Python代码
            timeout: 超时时间（秒）

        Returns:
            包含执行结果的字典，格式：
            {
                "success": bool,
                "output": str,
                "execute_result": str,
                "error": str,
                "execution_count": int
            }
        """
        if not self.is_running:
            await self.start_kernel()

        assert self.kc is not None, "Kernel client should be initialized"
        msg_id = self.kc.execute(code)

        result = {
            "success": True,
            "output": "",
            "execute_result": "",
            "error": "",
            "execution_count": 0
        }

        start_time = time.time()

        while True:
            if time.time() - start_time > timeout:
                result["success"] = False
                result["error"] = "Execution timeout"
                break

            try:
                msg = self.kc.iopub_channel.get_msg(timeout=0.1)
            except Exception:
                continue

            if msg['parent_header'].get('msg_id') != msg_id:
                continue

            msg_type = msg['msg_type']
            content = msg['content']

            if msg_type == 'execute_input':
                result["execution_count"] = content.get('execution_count', 0)

            elif msg_type == 'stream':
                if content['name'] == 'stdout':
                    result["output"] += strip_ansi_codes(content['text'])
                elif content['name'] == 'stderr':
                    result["error"] += strip_ansi_codes(content['text'])

            elif msg_type == 'execute_result':
                # 直接提供执行结果
                if 'text/plain' in content['data']:
                    result["execute_result"] += content['data']['text/plain']
                result["execution_count"] = content['execution_count']

            elif msg_type == 'display_data':
                # 处理显示数据
                if 'text/plain' in content['data']:
                    result["output"] += content['data']['text/plain']

            elif msg_type == 'error':
                result["success"] = False
                # 格式化错误信息并放入error字段
                formatted_error = format_error_message(
                    content['ename'],
                    content['evalue'],
                    content['traceback']
                )
                result["error"] += formatted_error

            elif msg_type == 'status' and content['execution_state'] == 'idle':
                break

        return result

    async def __aenter__(self):
        await self.start_kernel()
        return self

    async def __aexit__(self, _exc_type, _exc_val, _exc_tb):
        await self.stop_kernel()
        return False