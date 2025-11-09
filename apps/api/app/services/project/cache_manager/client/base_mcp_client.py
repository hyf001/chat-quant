"""
Base MCP Client - 通用的MCP客户端基类
支持调用任意MCP工具的异步HTTP客户端
"""

import asyncio
import aiohttp
import json
import logging
from typing import Dict, Any, Optional, AsyncIterator, Callable
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class SSEEvent:
    """SSE事件数据结构"""
    event_type: str
    data: str
    id: Optional[str] = None


class BaseMCPClient:
    """通用MCP客户端基类"""

    def __init__(self, email: str, tenant_id: str = "2", base_url: Optional[str] = None):
        """
        初始化MCP客户端

        Args:
            email: 用户邮箱
            tenant_id: 租户ID
            base_url: API基础URL
        """
        self.email = email
        self.tenant_id = tenant_id
        self.base_url = base_url

        # 会话管理
        self._session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """获取或创建HTTP会话"""
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=300)  # 5分钟超时
            self._session = aiohttp.ClientSession(timeout=timeout)
        return self._session

    async def call_mcp_tool(self,
                           tool_name: str,
                           arguments: Dict[str, Any],
                           method: str = "tools/call") -> Dict[str, Any]:
        """
        调用MCP工具（普通模式）

        Args:
            tool_name: MCP工具名称
            arguments: 工具参数
            method: RPC方法名

        Returns:
            Dict[str, Any]: 工具返回结果
        """
        url = f"{self.base_url}/call"

        # 构造MCP JSON-RPC请求
        rpc_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }

        headers = {
            "Content-Type": "application/json"
        }

        session = await self._get_session()

        try:
            logger.info(f"调用MCP工具: {tool_name}")
            logger.debug(f"请求参数: {json.dumps(rpc_request, indent=2, ensure_ascii=False)}")

            async with session.post(url, json=rpc_request, headers=headers) as response:
                if response.status == 200:
                    result = await response.json()

                    if "error" in result:
                        error_msg = result["error"].get("message", "未知错误")
                        logger.error(f"MCP工具调用失败: {error_msg}")
                        raise Exception(f"MCP工具调用失败: {error_msg}")

                    return result.get("result", {})
                else:
                    error_msg = f"HTTP请求失败: {response.status}"
                    logger.error(error_msg)
                    raise Exception(error_msg)

        except Exception as e:
            logger.error(f"调用MCP工具失败: {str(e)}")
            raise

    async def stream_mcp_tool(self,
                             tool_name: str,
                             arguments: Dict[str, Any],
                             progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None,
                             method: str = "tools/call") -> AsyncIterator[Dict[str, Any]]:
        """
        流式调用MCP工具（自动适配SSE或JSON模式）

        Args:
            tool_name: MCP工具名称
            arguments: 工具参数
            progress_callback: 进度回调函数
            method: RPC方法名

        Yields:
            Dict[str, Any]: 流式返回的数据项
        """
        url = f"{self.base_url}/call"

        # 构造MCP JSON-RPC请求
        rpc_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        }

        session = await self._get_session()

        try:
            logger.info(f"流式调用MCP工具: {tool_name}")
            logger.debug(f"请求参数: {json.dumps(rpc_request, indent=2, ensure_ascii=False)}")

            async with session.post(url, json=rpc_request, headers=headers) as response:
                if response.status == 200:
                    content_type = response.headers.get('Content-Type', '')

                    # 根据Content-Type判断响应格式
                    if 'text/event-stream' in content_type:
                        # SSE流式响应
                        logger.debug("使用SSE流式处理模式")
                        async for event in self._parse_sse_stream(response):
                            if event.event_type == "data":
                                try:
                                    data_item = json.loads(event.data)

                                    # 调用进度回调
                                    if progress_callback:
                                        progress_callback(data_item)

                                    yield data_item

                                except json.JSONDecodeError as e:
                                    logger.warning(f"解析SSE数据失败: {e}, 数据: {event.data}")
                                    continue

                            elif event.event_type == "error":
                                error_msg = f"SSE流中的错误: {event.data}"
                                logger.error(error_msg)
                                raise Exception(error_msg)
                    else:
                        # 普通JSON响应，模拟流式处理
                        logger.debug("使用JSON批量处理模式（模拟流式）")
                        result = await response.json()

                        if "error" in result:
                            error_msg = result["error"].get("message", "未知错误")
                            logger.error(f"MCP工具调用失败: {error_msg}")
                            raise Exception(f"MCP工具调用失败: {error_msg}")

                        # 解析MCP响应并流式yield数据
                        async for data_item in self._parse_json_to_stream(result, progress_callback):
                            yield data_item

                else:
                    error_msg = f"HTTP请求失败: {response.status}"
                    logger.error(error_msg)
                    raise Exception(error_msg)

        except Exception as e:
            logger.error(f"流式调用MCP工具失败: {str(e)}")
            raise

    async def _parse_sse_stream(self, response: aiohttp.ClientResponse) -> AsyncIterator[SSEEvent]:
        """解析SSE数据流"""
        buffer = ""

        async for chunk in response.content.iter_chunked(8192):
            if not chunk:
                continue

            try:
                text_chunk = chunk.decode('utf-8')
                buffer += text_chunk

                # 处理完整的SSE消息
                while "\n\n" in buffer:
                    message, buffer = buffer.split("\n\n", 1)

                    event = self._parse_sse_message(message)
                    if event:
                        yield event

            except UnicodeDecodeError as e:
                logger.warning(f"解码SSE数据块失败: {e}")
                continue

    def _parse_sse_message(self, message: str) -> Optional[SSEEvent]:
        """解析单个SSE消息"""
        if not message.strip():
            return None

        event_type = "message"
        data = ""
        event_id = None

        for line in message.split('\n'):
            line = line.strip()
            if line.startswith('event:'):
                event_type = line[6:].strip()
            elif line.startswith('data:'):
                data_part = line[5:].strip()
                if data:
                    data += '\n' + data_part
                else:
                    data = data_part
            elif line.startswith('id:'):
                event_id = line[3:].strip()

        if data:
            return SSEEvent(event_type=event_type, data=data, id=event_id)
        return None

    async def _parse_json_to_stream(self,
                                   mcp_response: Dict[str, Any],
                                   progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None) -> AsyncIterator[Dict[str, Any]]:
        """
        解析MCP的JSON响应，模拟流式输出

        Args:
            mcp_response: MCP的JSON-RPC响应
            progress_callback: 进度回调函数

        Yields:
            Dict[str, Any]: 解析后的数据行
        """
        try:
            # 提取result.content[0].text
            result = mcp_response.get("result", {})
            content_list = result.get("content", [])

            if not content_list:
                logger.warning("MCP响应中没有content数据")
                return

            first_content = content_list[0]
            text = first_content.get("text", "")

            # 调试：输出响应文本的前500个字符
            logger.debug(f"MCP响应文本预览（前500字符）:\n{text[:500]}")

            # 从text中提取JSON（查找 "Original Response" 后的JSON）
            start_marker = '## Original Response'
            start_pos = text.find(start_marker)

            if start_pos < 0:
                logger.warning("未找到 'Original Response' 标记")
                logger.debug(f"完整响应文本:\n{text}")
                return

            # 查找JSON起始位置
            json_start = text.find('{"statusCode"', start_pos)
            if json_start < 0:
                json_start = text.find('{"', start_pos)

            if json_start < 0:
                logger.warning("未找到JSON数据")
                return

            # 提取并解析JSON
            json_text = text[json_start:].strip()
            api_response = json.loads(json_text)

            # 提取data.headers和data.rows
            data_obj = api_response.get("data", {})
            headers = data_obj.get("headers", [])
            rows = data_obj.get("rows", [])

            logger.info(f"解析到 {len(rows)} 行数据，字段: {headers}")

            # 将每行转换为字典并yield
            for idx, row in enumerate(rows):
                try:
                    # 组合headers和row成字典
                    data_item = dict(zip(headers, row))

                    # 调用进度回调
                    if progress_callback:
                        progress_callback(data_item)

                    yield data_item

                    # 添加微小延迟，模拟流式处理
                    if idx % 10 == 0:
                        await asyncio.sleep(0)  # 让出控制权

                except Exception as e:
                    logger.error(f"处理第 {idx} 行数据失败: {e}")
                    continue

        except json.JSONDecodeError as e:
            logger.error(f"解析JSON失败: {e}")
            raise
        except Exception as e:
            logger.error(f"解析MCP响应失败: {e}")
            raise

    async def close(self):
        """关闭客户端会话"""
        if self._session and not self._session.closed:
            await self._session.close()
            logger.debug("MCP客户端会话已关闭")