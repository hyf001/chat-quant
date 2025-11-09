"""
EasyFetch HTTPS客户端
用于直接调用EasyFetch HTTPS接口，替代MCP工具
"""
import logging
from typing import Dict, Any, Optional
from pathlib import Path
import os

from app.utils.https_mtls_client import HttpsMtlsClient

logger = logging.getLogger(__name__)


class EasyFetchHttpsClient:
    """EasyFetch HTTPS客户端"""

    def __init__(self,
                 email: Optional[str] = None,
                 tenant_id: Optional[str] = None,
                 base_url: Optional[str] = None,
                 cert_path: Optional[str] = None,
                 cert_password: Optional[str] = None):
        """
        初始化EasyFetch HTTPS客户端

        根据环境变量 THS_TIER 自动选择配置：
        - THS_TIER=dev (开发环境):
          - 使用 BI_DOMAIN (默认 https://phonestat.hexin.cn/sdmp/easyfetch)
          - 需要 SSL 双向认证 (SSL_CERT_FILE, SSL_CERT_PASSWORD)
        - THS_TIER=prod/beimeipri/dreamface (生产环境):
          - 使用 BI_CONTAINER_HOST (默认 http://easyfetch:9596)
          - 不需要 SSL 认证

        其他参数：
        - email: 从 EXPORT_DEFAULT_EMAIL 环境变量读取（向后兼容 MCP_DEFAULT_EMAIL）
        - tenant_id: 从 EXPORT_TENANT_ID 环境变量读取（向后兼容 MCP_TENANT_ID）

        Args:
            email: 用户邮箱（认证），默认从环境变量 EXPORT_DEFAULT_EMAIL 读取
            tenant_id: 租户ID，默认从环境变量 EXPORT_TENANT_ID 读取
            base_url: 基础URL，如果提供则忽略 THS_TIER 的自动选择
            cert_path: SSL证书路径（支持.p12或.pem格式），默认从环境变量 SSL_CERT_FILE 读取
            cert_password: 证书密码，默认从环境变量 SSL_CERT_PASSWORD 读取
        """
        # 从环境变量获取配置（如果未提供）
        # 优先使用新的EXPORT_前缀，向后兼容MCP_前缀
        self.email = email or os.getenv('EXPORT_DEFAULT_EMAIL') or os.getenv('MCP_DEFAULT_EMAIL')
        self.tenant_id = tenant_id or os.getenv('EXPORT_TENANT_ID') or os.getenv('MCP_TENANT_ID', '2')

        # 根据 THS_TIER 动态选择 base_url 和 SSL 配置
        ths_tier = os.getenv('THS_TIER', 'dev').lower()

        # 判断是否为生产环境
        is_production = ths_tier in ['prod', 'beimeipri', 'dreamface']

        # 处理 base_url
        if base_url is None:
            if is_production:
                # 生产环境 (prod/beimeipri/dreamface)：使用容器内部地址，不需要 SSL
                container_host = os.getenv('BI_CONTAINER_HOST', 'http://easyfetch:9596/easyfetch')
                base_url = f"{container_host.rstrip('/')}/v2"
                logger.info(f"生产环境模式 (THS_TIER={ths_tier}): 使用 BI_CONTAINER_HOST = {container_host}")
            else:
                # 开发环境 (dev)：使用外部域名，需要 SSL
                bi_domain = os.getenv('BI_DOMAIN', 'https://phonestat.hexin.cn/sdmp/easyfetch')
                base_url = f"{bi_domain.rstrip('/')}/v2"
                logger.info(f"开发环境模式 (THS_TIER={ths_tier}): 使用 BI_DOMAIN = {bi_domain}")
        self.base_url = base_url.rstrip('/')

        # 验证必需参数（仅在生产环境需要）
        # 开发环境使用SSL证书认证，不需要email和tenant_id
        if is_production:
            if not self.email:
                raise ValueError("生产环境需要 email 参数，请设置环境变量 EXPORT_DEFAULT_EMAIL 或 MCP_DEFAULT_EMAIL")
            if not self.tenant_id:
                raise ValueError("生产环境需要 tenant_id 参数，请设置环境变量 EXPORT_TENANT_ID 或 MCP_TENANT_ID")

        # 从环境变量获取证书配置（如果未提供）
        # 在生产环境下，默认不使用 SSL 双向认证
        if cert_path is None and not is_production:
            cert_path = os.getenv('SSL_CERT_FILE')
        if cert_password is None and not is_production:
            cert_password = os.getenv('SSL_CERT_PASSWORD')

        # 如果提供了证书，使用mTLS客户端，否则使用普通HTTPS
        self.use_mtls = cert_path is not None and cert_password is not None
        self.ths_tier = ths_tier  # 保存环境类型
        self.is_production = is_production  # 保存环境判断结果

        if self.use_mtls:
            # 使用双向认证的HTTPS客户端
            # 注意：内网环境通常使用自签名证书，需要禁用服务器证书验证
            self.client = HttpsMtlsClient(
                cert_path=cert_path,
                cert_password=cert_password,
                base_url=base_url,
                timeout=60,
                verify_ssl=False  # 禁用服务器证书验证（内网自签名证书）
            )
            logger.info(f"初始化EasyFetch HTTPS客户端(mTLS): {base_url}")
        else:
            # 使用普通HTTPS（不需要双向认证）
            self.client = None
            logger.info(f"初始化EasyFetch HTTPS客户端(普通): {base_url}")
            if not is_production:
                logger.warning("开发环境未配置SSL证书，可能无法访问外网API")

    def _build_headers(self) -> Dict[str, str]:
        """
        构建请求头

        注意：
        - 开发环境 (THS_TIER=dev): 使用SSL双向认证，不需要额外的认证header
        - 生产环境 (THS_TIER=prod/beimeipri/dreamface): 不使用SSL认证，需要通过header传递认证信息
        """
        headers = {
            "Content-Type": "application/json"
        }

        # 只在生产环境（非SSL认证）时添加认证header
        # 或者开发环境没有配置SSL证书时添加（但需要确保email和tenant_id存在）
        if self.is_production or not self.use_mtls:
            if self.email:  # 只有当email存在时才添加
                headers["CBAS_EMAIL"] = self.email
            if self.tenant_id:  # 只有当tenant_id存在时才添加
                headers["x-data-portal-tenant-id"] = str(self.tenant_id)

        return headers

    async def get_table_list(self, query: str = "", table_type: str = "PHYSICAL") -> Dict[str, Any]:
        """
        获取数据表列表

        POST https://phonestat.hexin.cn/sdmp/easyfetch/v2/table/dir/tree
        参数：{query: "", table_type: "PHYSICAL"}

        Args:
            query: 查询关键字
            table_type: 表类型 (PHYSICAL/REPORT)

        Returns:
            数据表列表响应
        """
        try:
            url = f"{self.base_url}/table/dir/tree"
            headers = self._build_headers()
            json_data = {
                "query": query,
                "table_type": table_type
            }

            if self.use_mtls:
                # 使用mTLS客户端
                response = await self.client.post(url, headers=headers, json=json_data)

                if response.get('ok', False):
                    return response.get('json', {})
                else:
                    logger.error(f"获取表列表失败: HTTP {response.get('status')}, {response.get('body')}")
                    return {}
            else:
                # 使用普通HTTP请求（需要aiohttp）
                import aiohttp
                async with aiohttp.ClientSession() as session:
                    async with session.post(url, headers=headers, json=json_data) as resp:
                        if resp.status == 200:
                            return await resp.json()
                        else:
                            body = await resp.text()
                            logger.error(f"获取表列表失败: HTTP {resp.status}, {body}")
                            return {}
        except Exception as e:
            logger.error(f"获取表列表异常: {str(e)}")
            raise

    async def get_report_list(self, query: str = "", table_type: str = "REPORT") -> Dict[str, Any]:
        """
        获取报表列表

        POST https://phonestat.hexin.cn/sdmp/easyfetch/v2/table/schema/tree
        参数：{query: "", table_type: "REPORT"}

        Args:
            query: 查询关键字
            table_type: 表类型 (固定为REPORT)

        Returns:
            报表列表响应
        """
        try:
            url = f"{self.base_url}/table/schema/tree"
            headers = self._build_headers()
            json_data = {
                "query": query,
                "table_type": table_type
            }

            if self.use_mtls:
                # 使用mTLS客户端
                response = await self.client.post(url, headers=headers, json=json_data)

                if response.get('ok', False):
                    return response.get('json', {})
                else:
                    logger.error(f"获取报表列表失败: HTTP {response.get('status')}, {response.get('body')}")
                    return {}
            else:
                # 使用普通HTTP请求
                import aiohttp
                async with aiohttp.ClientSession() as session:
                    async with session.post(url, headers=headers, json=json_data) as resp:
                        if resp.status == 200:
                            return await resp.json()
                        else:
                            body = await resp.text()
                            logger.error(f"获取报表列表失败: HTTP {resp.status}, {body}")
                            return {}
        except Exception as e:
            logger.error(f"获取报表列表异常: {str(e)}")
            raise

    async def get_table_detail(self, table_id: str) -> Dict[str, Any]:
        """
        获取数据表或报表详情

        GET https://phonestat.hexin.cn/sdmp/easyfetch/v2/table/schema/get?id=1017

        Args:
            table_id: 表ID

        Returns:
            表详情响应
        """
        try:
            url = f"{self.base_url}/table/schema/get"
            headers = self._build_headers()
            params = {"id": table_id}

            if self.use_mtls:
                # 使用mTLS客户端
                response = await self.client.get(url, headers=headers, params=params)

                if response.get('ok', False):
                    result = response.get('json', {})
                    # 处理字段字典信息
                    await self._enrich_column_dict(result)
                    return result
                else:
                    logger.error(f"获取表详情失败 (ID: {table_id}): HTTP {response.get('status')}, {response.get('body')}")
                    return {}
            else:
                # 使用普通HTTP请求
                import aiohttp
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers=headers, params=params) as resp:
                        if resp.status == 200:
                            result = await resp.json()
                            # 处理字段字典信息
                            await self._enrich_column_dict(result)
                            return result
                        else:
                            body = await resp.text()
                            logger.error(f"获取表详情失败 (ID: {table_id}): HTTP {resp.status}, {body}")
                            return {}
        except Exception as e:
            logger.error(f"获取表详情异常 (ID: {table_id}): {str(e)}")
            raise

    async def _enrich_column_dict(self, table_detail: Dict[str, Any]) -> None:
        """
        为表详情中的列字段补充字典信息

        如果列的 data_format.name == "dic"，则调用 /table/column/dict 接口获取字典列表

        Args:
            table_detail: 表详情数据（会直接修改）
        """
        if not table_detail or table_detail.get("status_code") != 0:
            return

        data = table_detail.get("data", {})

        # 只处理数据表（PHYSICAL），报表（REPORT）不存在 data_format.name == "dic" 的列
        table_type = data.get("table_type", "")
        if table_type != "PHYSICAL":
            return

        column_list = data.get("column_list", [])

        if not column_list:
            return

        # 收集需要获取字典的列
        columns_need_dict = []
        for col in column_list:
            data_format = col.get("data_format")
            if data_format and isinstance(data_format, dict):
                if data_format.get("name") == "dic":
                    column_id = col.get("id")
                    if column_id:
                        columns_need_dict.append((col, column_id))

        # 批量获取字典信息
        if columns_need_dict:
            import asyncio
            tasks = [
                self.get_column_dict(column_id)
                for _, column_id in columns_need_dict
            ]
            dict_results = await asyncio.gather(*tasks, return_exceptions=True)

            # 将字典信息添加到对应的列
            for (col, column_id), dict_result in zip(columns_need_dict, dict_results):
                col_name = col.get('en_name', 'unknown')
                if isinstance(dict_result, Exception):
                    logger.warning(f"获取列字典失败 {col_name} (column_id: {column_id}): {str(dict_result)}")
                elif dict_result.get("status_code") == 0:
                    dict_data = dict_result.get("data", {})

                    # 字典数据格式: {dict_code, dict_name, dict_items}
                    # 封装为 dict: {dict_name: "xxx", dict_items: {...}}
                    if isinstance(dict_data, dict) and "dict_items" in dict_data:
                        col["dict"] = {
                            "dict_name": dict_data.get("dict_name", ""),
                            "dict_items": dict_data.get("dict_items", {})
                        }
                    else:
                        # 如果格式不符，记录警告
                        logger.warning(f"列 {col_name} (column_id: {column_id}) 的字典数据格式不正确: {dict_data}")
                else:
                    logger.warning(f"获取列字典失败 {col_name} (column_id: {column_id}): {dict_result.get('status_msg', 'Unknown error')}")

    async def get_column_dict(self, column_id: str) -> Dict[str, Any]:
        """
        获取列的字典信息

        GET https://phonestat.hexin.cn/sdmp/easyfetch/v2/table/column/dict?column_id=56153

        Args:
            column_id: 列ID

        Returns:
            字典信息响应
        """
        try:
            url = f"{self.base_url}/table/column/dict"
            headers = self._build_headers()
            params = {"column_id": column_id}

            if self.use_mtls:
                # 使用mTLS客户端
                response = await self.client.get(url, headers=headers, params=params)

                if response.get('ok', False):
                    return response.get('json', {})
                else:
                    logger.error(f"获取列字典失败 (column_id: {column_id}): HTTP {response.get('status')}, {response.get('body')}")
                    return {"status_code": -1, "status_msg": "Request failed"}
            else:
                # 使用普通HTTP请求
                import aiohttp
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers=headers, params=params) as resp:
                        if resp.status == 200:
                            return await resp.json()
                        else:
                            body = await resp.text()
                            logger.error(f"获取列字典失败 (column_id: {column_id}): HTTP {resp.status}, {body}")
                            return {"status_code": -1, "status_msg": "Request failed"}
        except Exception as e:
            logger.error(f"获取列字典异常 (column_id: {column_id}): {str(e)}")
            return {"status_code": -1, "status_msg": str(e)}

    async def close(self):
        """关闭客户端"""
        if self.use_mtls and self.client:
            await self.client.close()
