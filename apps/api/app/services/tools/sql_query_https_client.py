"""
基于HTTPS双向认证的Presto查询客户端
基于 PrestoQueryClient 的逻辑，但使用 HttpsMtlsClient 进行HTTP调用
"""
import os
import asyncio
from typing import Optional, Dict, Any
from datetime import datetime
from app.utils.https_mtls_client import HttpsMtlsClient


class SqlQueryHttpsClient:
    """
    基于HTTPS双向认证的Presto查询客户端，用于调用Java服务接口执行SQL并生成本地文件
    使用HttpsMtlsClient进行双向SSL认证
    """

    def __init__(
        self,
        cert_path: str,
        cert_password: str,
        base_url: str = "https://phonestat.hexin.cn/sdmp",
        timeout: int = 30,
        max_retries: int = 3,
        verify_ssl: bool = False
    ):
        """
        初始化客户端

        Args:
            cert_path: 证书文件路径
            cert_password: 证书密码
            base_url: Java服务的基础URL
            timeout: 请求超时时间
            max_retries: 最大重试次数
            verify_ssl: 是否验证SSL证书
        """
        self.base_url = base_url.rstrip('/')
        self.https_client = HttpsMtlsClient(
            cert_path=cert_path,
            cert_password=cert_password,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            verify_ssl=verify_ssl
        )

    async def preview_query(self, sql: str, catalog_name: str = "presto-hive") -> Dict[str, Any]:
        """
        预览查询结果（根据 presto查询.md 接口规范）

        Args:
            sql: SQL查询语句
            catalog_name: 目录名称，默认为 "presto-hive"

        Returns:
            包含columns、data、error字段的字典，格式兼容原有调用方式
        """
        url = "/v2/tool/data/fetch"
        payload = {
            "sql": sql,
            "catalog_name": catalog_name
        }

        try:
            response = await self.https_client.post(url, json=payload)

            if not response['ok']:
                return {"error": f"HTTP请求失败: {response['status']} {response['status_text']}"}

            result = response['json']
            if not result:
                return {"error": "响应不是有效的JSON格式"}

            # 检查响应状态
            if result.get("status_code") != 0:
                return {"error": f"查询失败: {result.get('status_msg', 'Unknown error')}"}

            # 提取数据
            data_section = result.get("data", {})
            query_result = data_section.get("result", {})

            # 转换为原有格式，保持兼容性
            row_list = query_result.get("row_list", [])
            column_info_list = query_result.get("column_info_list", [])

            # 构造列名列表
            columns = [col["name"] for col in column_info_list]

            # 转换行数据为字典格式（保持与原格式兼容）
            data = []
            for row in row_list:
                if len(row) == len(columns):
                    row_dict = {columns[i]: row[i] for i in range(len(columns))}
                    data.append(row_dict)
                else:
                    # 如果列数不匹配，保持原始行数据
                    data.append(row)

            return {
                "columns": columns,
                "data": data,
                "sql": data_section.get("sql", sql),
                "total": result.get("total"),
                "raw_response": result  # 保留原始响应用于调试
            }

        except Exception as e:
            return {"error": f"预览请求失败: {str(e)}"}

    async def download_query_result(self, sql: str, file_path: str = None) -> Dict[str, Any]:
        """
        执行SQL查询并下载结果到本地文件

        Args:
            sql: SQL查询语句
            file_path: 本地文件保存路径，如果为None则保存到当前目录

        Returns:
            包含success、file_path、message等字段的字典
        """
        url = "/v2/tool/data/fetch_presto_download"
        payload = {"sql": sql}

        try:
            print(f"开始执行查询...")
            response = await self.https_client.post(url, json=payload)

            if not response['ok']:
                return {"success": False, "error": f"HTTP请求失败: {response['status']} {response['status_text']}"}

            # 获取文件名
            filename = self._extract_filename(response)

            # 确定保存路径
            if file_path is None:
                file_path = os.getcwd()

            if os.path.isdir(file_path):
                full_path = os.path.join(file_path, filename)
            else:
                full_path = file_path

            # 确保目录存在
            os.makedirs(os.path.dirname(full_path) if os.path.dirname(full_path) else '.', exist_ok=True)

            # 检查是否是文件下载响应
            content_type = response.get('headers', {}).get('content-type', '')
            if 'application/octet-stream' in content_type or 'text/csv' in content_type or response.get('body'):
                # 保存文件到本地
                file_size = 0

                if isinstance(response['body'], bytes):
                    # 如果body是bytes，直接写入
                    with open(full_path, 'wb') as f:
                        f.write(response['body'])
                        file_size = len(response['body'])
                else:
                    # 如果body是字符串，转换为bytes写入
                    content = response['body']
                    if isinstance(content, str):
                        content = content.encode('utf-8')
                    with open(full_path, 'wb') as f:
                        f.write(content)
                        file_size = len(content)

                print(f"文件下载完成: {full_path}")
                print(f"文件大小: {self._format_size(file_size)}")

                return {
                    "success": True,
                    "file_path": full_path,
                    "file_size": file_size,
                    "message": f"查询结果已保存到: {full_path}"
                }
            else:
                # 如果不是文件下载，解析JSON响应
                if response['json']:
                    result = response['json']
                    return {"success": False, "error": f"非文件响应: {result.get('status_msg')}"}
                else:
                    return {"success": False, "error": "Unexpected response format"}

        except Exception as e:
            return {"success": False, "error": f"下载请求失败: {str(e)}"}

    def _extract_filename(self, response: Dict[str, Any]) -> str:
        """从响应头中提取文件名"""
        content_disposition = response.get('headers', {}).get('Content-Disposition', '')
        if 'filename=' in content_disposition:
            import re
            # 尝试匹配带引号的文件名: filename="file.csv"
            match = re.search(r'filename="([^"]+)"', content_disposition)
            if match:
                filename = match.group(1)
            else:
                # 尝试匹配不带引号的文件名: filename=file.csv
                match = re.search(r'filename=([^;\s]+)', content_disposition)
                if match:
                    filename = match.group(1)
                else:
                    # 默认文件名
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"query_result_{timestamp}.csv"
        else:
            # 默认文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"query_result_{timestamp}.csv"

        # 如果没有扩展名，添加.csv
        if not filename.endswith('.csv'):
            filename = f"{filename}.csv"

        return filename

    def _format_size(self, size_bytes: int) -> str:
        """格式化文件大小"""
        if size_bytes == 0:
            return "0B"

        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1

        return f"{size_bytes:.2f}{size_names[i]}"

    async def test_connection(self) -> Dict[str, Any]:
        """
        测试与服务的连接状态

        Returns:
            包含连接测试结果的字典
        """
        try:
            # 使用简单的健康检查接口或者可访问的接口来测试连接
            response = await self.https_client.get("/")

            if response['ok']:
                return {
                    "success": True,
                    "message": f"连接成功 - 状态码: {response['status']}"
                }
            else:
                return {
                    "success": False,
                    "error": f"连接失败 - 状态码: {response['status']} {response['status_text']}"
                }

        except Exception as e:
            return {
                "success": False,
                "error": f"连接测试失败: {str(e)}"
            }

    async def close(self):
        """关闭客户端连接"""
        await self.https_client.close()

    async def __aenter__(self):
        """异步上下文管理器入口"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器退出"""
        await self.close()