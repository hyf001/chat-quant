"""
金融查数接口客户端 (开发环境 HTTPS)
基于HTTPS双向认证,使用 HttpsMtlsClient 进行HTTP调用
"""
import os
import csv
from typing import Dict, Any
from datetime import datetime
import aiohttp
from app.utils.https_mtls_client import HttpsMtlsClient


class FinSqlQueryHttpsClient:
    """
    基于HTTPS双向认证的金融查数客户端,用于调用接口执行SQL并生成本地CSV文件
    使用HttpsMtlsClient进行双向SSL认证
    """

    def __init__(
        self,
        cert_path: str,
        cert_password: str,
        base_url: str = "https://indexmap.myhexin.com",
        timeout: int = 30,
        max_retries: int = 3,
        verify_ssl: bool = False
    ):
        """
        初始化客户端

        Args:
            cert_path: 证书文件路径
            cert_password: 证书密码
            base_url: 服务的基础URL
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

    async def preview_query(self, sql: str) -> Dict[str, Any]:
        """
        预览查询结果

        Args:
            sql: SQL查询语句

        Returns:
            包含原始响应数据的字典,格式:
            {
                "status_code": 0,
                "status_msg": "ok",
                "data": {
                    "total": 104,
                    "title": [{"type": "varchar", "name": "股票代码"}, ...],
                    "body": [["000417.SZ", "合百集团", ...], ...]
                }
            }
            或错误信息:
            {"error": "错误描述"}
        """
        url = "/bfe/internalSqlRun"

        try:
            # 使用 aiohttp.FormData 构建 multipart/form-data 请求
            form_data = aiohttp.FormData()
            form_data.add_field('sql', sql)
            form_data.add_field('env', 'prod')

            # 发送请求
            response = await self.https_client.post(url, data=form_data)

            if not response['ok']:
                return {"error": f"HTTP请求失败: {response['status']} {response['status_text']}"}

            result = response['json']
            if not result:
                return {"error": "响应不是有效的JSON格式"}

            # 检查响应状态
            if result.get("status_code") != 0:
                return {"error": f"查询失败: {result.get('status_msg', 'Unknown error')}"}

            # 直接返回完整响应
            return result

        except Exception as e:
            return {"error": f"预览请求失败: {str(e)}"}

    async def download_query_result(self, sql: str, file_path: str = None) -> Dict[str, Any]:
        """
        执行SQL查询并下载结果为CSV文件

        Args:
            sql: SQL查询语句
            file_path: 本地文件保存目录,如果为None则保存到当前目录

        Returns:
            包含success、file_path、message等字段的字典
        """
        url = "/bfe/internalSqlRun"

        try:
            print(f"开始执行查询...")
            # 使用 aiohttp.FormData 构建 multipart/form-data 请求
            form_data = aiohttp.FormData()
            form_data.add_field('sql', sql)
            form_data.add_field('env', 'prod')

            # 发送请求
            response = await self.https_client.post(url, data=form_data)

            if not response['ok']:
                return {"success": False, "error": f"HTTP请求失败: {response['status']} {response['status_text']}"}

            result = response['json']
            if not result:
                return {"success": False, "error": "响应不是有效的JSON格式"}

            # 检查响应状态
            if result.get("status_code") != 0:
                return {
                    "success": False,
                    "error": f"查询失败: {result.get('status_msg', 'Unknown error')}"
                }

            # 提取数据
            data_section = result.get("data", {})
            title_list = data_section.get("title", [])
            body_list = data_section.get("body", [])
            total = data_section.get("total", 0)

            if not title_list:
                return {"success": False, "error": "响应数据中没有列定义(title)"}

            # 确定保存路径
            if file_path is None:
                file_path = os.getcwd()

            # 生成文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"fin_query_result_{timestamp}.csv"

            if os.path.isdir(file_path):
                full_path = os.path.join(file_path, filename)
            else:
                full_path = file_path

            # 确保目录存在
            os.makedirs(os.path.dirname(full_path) if os.path.dirname(full_path) else '.', exist_ok=True)

            # 提取列名
            column_names = [col.get("name", f"column_{i}") for i, col in enumerate(title_list)]

            # 写入CSV文件
            file_size = 0
            with open(full_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
                writer = csv.writer(csvfile)

                # 写入表头
                writer.writerow(column_names)

                # 写入数据行
                for row in body_list:
                    writer.writerow(row)

                file_size = csvfile.tell()

            print(f"文件下载完成: {full_path}")
            print(f"文件大小: {self._format_size(file_size)}")
            print(f"总行数: {total}")

            return {
                "success": True,
                "file_path": full_path,
                "file_size": file_size,
                "total_rows": total,
                "message": f"查询结果已保存到: {full_path}"
            }

        except Exception as e:
            return {"success": False, "error": f"下载请求失败: {str(e)}"}

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
