"""
FinView HTTPS客户端
用于调用金融指标视图表API
"""
import logging
from typing import Dict, Any, Optional
import os

logger = logging.getLogger(__name__)


class FinViewHttpsClient:
    """金融指标视图表HTTPS客户端"""

    def __init__(self, base_url: Optional[str] = None):
        """
        初始化FinView HTTPS客户端

        Args:
            base_url: API基础URL，默认从环境变量 FIN_VIEW_BASE_URL 读取

        Note:
            如果未配置 FIN_VIEW_BASE_URL（如 THS_TIER=dreamface 环境），
            客户端将处于禁用状态，所有API调用将返回空结果
        """
        # 从环境变量或参数获取base_url
        self.base_url = base_url or os.getenv('FIN_VIEW_BASE_URL')

        if not self.base_url:
            # dreamface等环境不配置此环境变量，客户端禁用
            self.api_url = None
            logger.info("FIN_VIEW_BASE_URL 未配置，FinView客户端已禁用（适用于dreamface等环境）")
        else:
            # 构建完整API地址（统一后缀）
            self.api_url = f"{self.base_url.rstrip('/')}/api/view_table_struct"
            logger.info(f"初始化FinView HTTP客户端: {self.api_url}")

    async def get_view_table_list(self, page: int, pageSize: int) -> Dict[str, Any]:
        """
        获取金融指标视图表列表

        API文档:
        - 开发环境: https://indexmap.myhexin.com/bfe/api/view_table_struct?page=1&pageSize=1
        - 生产环境: http://cbas-babel-frontend-prod:10399/babel/api/view_table_struct
        - 北美环境: http://cbas-babel-frondend-beimeipri:10399/babel/api/view_table_struct

        Args:
            page: 页码（从1开始）
            pageSize: 每页大小

        Returns:
            API响应数据（如果客户端禁用，返回空结果）

        Raises:
            Exception: API调用失败
        """
        # 如果客户端禁用（未配置FIN_VIEW_BASE_URL），直接返回空结果
        if not self.api_url:
            logger.debug(f"FinView客户端已禁用，跳过API调用: page={page}, pageSize={pageSize}")
            return {
                "status_code": 0,
                "status_msg": "success (client disabled)",
                "data": {"items": [], "total": 0}
            }

        try:
            import aiohttp
            import ssl

            params = {
                "page": page,
                "pageSize": pageSize
            }

            logger.debug(f"请求视图表列表: page={page}, pageSize={pageSize}")

            # 创建SSL上下文，禁用证书验证
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

            connector = aiohttp.TCPConnector(ssl=ssl_context)
            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.get(self.api_url, params=params, timeout=aiohttp.ClientTimeout(total=60)) as resp:
                    if resp.status == 200:
                        result = await resp.json()

                        # 调试输出：检查返回数据类型
                        logger.debug(f"API返回数据类型: {type(result)}")

                        # 处理API返回的数据格式：可能是list或dict
                        if isinstance(result, list):
                            logger.debug(f"获取视图表列表成功(list格式): page={page}, 返回数据量={len(result)}")
                            # 将list格式转换为标准dict格式
                            # 注意: list格式的API不返回total，设置为-1表示未知总数，需要持续分页直到返回空数组
                            return {
                                "status_code": 0,
                                "status_msg": "success",
                                "data": result,  # 直接使用list作为data
                                "total": -1  # -1表示未知总数，需要继续分页
                            }
                        elif isinstance(result, dict):
                            # dict格式可能有两种情况：
                            # 1. 标准格式: {"data": {"items": [...], "total": 100}}
                            # 2. 简化格式: {"data": [...], "total": 100}
                            data_field = result.get('data', {})
                            if isinstance(data_field, list):
                                items_count = len(data_field)
                            elif isinstance(data_field, dict):
                                items_count = len(data_field.get('items', []))
                            else:
                                items_count = 0
                            logger.debug(f"获取视图表列表成功(dict格式): page={page}, 返回数据量={items_count}")
                            return result
                        else:
                            logger.error(f"未知的API返回格式: {type(result)}")
                            return {
                                "status_code": -1,
                                "status_msg": f"未知的API返回格式: {type(result)}",
                                "data": {"items": [], "total": 0}
                            }
                    else:
                        body = await resp.text()
                        logger.error(f"获取视图表列表失败: HTTP {resp.status}, {body}")
                        return {
                            "status_code": -1,
                            "status_msg": f"HTTP {resp.status}: {body}",
                            "data": {"items": [], "total": 0}
                        }
        except Exception as e:
            logger.error(f"获取视图表列表异常: {str(e)}")
            raise

    async def close(self):
        """关闭客户端（预留接口，aiohttp使用上下文管理器自动关闭）"""
        pass
