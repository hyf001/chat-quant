"""
Async MCP Client - 基于BaseMCPClient的实现，保持向后兼容
"""

import logging
from typing import Dict, Any, Optional, AsyncIterator, Callable

from .base_mcp_client import BaseMCPClient

logger = logging.getLogger(__name__)


class AsyncMCPClient(BaseMCPClient):
    """异步MCP客户端，保持向后兼容性"""

    def __init__(self, email: str, tenant_id: str = "2", base_url: Optional[str] = None):
        """
        初始化异步MCP客户端

        Args:
            email: 用户邮箱
            tenant_id: 租户ID，默认"2"
            base_url: API基础URL
        """
        super().__init__(email, tenant_id, base_url)

    # 为了向后兼容，保留一些常用方法的别名
    async def call_mcp_function(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """调用MCP工具的别名方法，保持向后兼容"""
        return await self.call_mcp_tool(tool_name, arguments)

    async def stream_mcp_function(self,
                                 tool_name: str,
                                 arguments: Dict[str, Any],
                                 progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None) -> AsyncIterator[Dict[str, Any]]:
        """流式调用MCP工具的别名方法，保持向后兼容"""
        async for item in self.stream_mcp_tool(tool_name, arguments, progress_callback):
            yield item