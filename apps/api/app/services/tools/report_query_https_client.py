"""
基于HTTPS双向认证的报表查询客户端
使用 HttpsMtlsClient 进行HTTP调用
"""
import os
import json
from typing import Dict, Any
from datetime import datetime
from app.utils.https_mtls_client import HttpsMtlsClient


class ReportQueryHttpsClient:
    """
    基于HTTPS双向认证的报表查询客户端（开发环境）
    使用HttpsMtlsClient进行双向SSL认证
    """

    def __init__(
        self,
        cert_path: str,
        cert_password: str,
        base_url: str = "https://phonestat.hexin.cn/sdmp/easyfetch",
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

    async def download_report_data(self, id: int, start_time: str, end_time: str,
                                  file_path: str = None) -> Dict[str, Any]:
        """
        下载报表全量数据

        Args:
            id: 报表ID
            start_time: 起始日期（格式：yyyyMMdd）
            end_time: 截止日期（格式：yyyyMMdd）
            file_path: 本地文件保存路径，如果为None则保存到当前目录

        Returns:
            包含success、file_path、message等字段的字典
        """
        url = "/v2/tool/report_data/fetch"
        payload = {
            "id": id,
            "start_time": start_time,
            "end_time": end_time
        }

        try:
            print(f"开始下载报表数据: {id}")
            response = await self.https_client.post(url, json=payload)

            if not response['ok']:
                return {"success": False, "error": f"HTTP请求失败: {response['status']} {response['status_text']}"}

            # 获取响应数据
            result = response.get('json')

            # 确定保存路径
            if file_path is None:
                file_path = os.getcwd()

            # 生成 JSON 文件名
            filename = f"report_{id}_{start_time}_to_{end_time}.json"

            if os.path.isdir(file_path):
                full_path = os.path.join(file_path, filename)
            else:
                full_path = file_path

            # 确保目录存在
            os.makedirs(os.path.dirname(full_path) if os.path.dirname(full_path) else '.', exist_ok=True)

            # 保存为 JSON 格式
            if result is not None:
                # 如果响应是 JSON 数据，保存为格式化的 JSON
                with open(full_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                file_size = os.path.getsize(full_path)

                print(f"报表数据下载完成: {full_path}")
                print(f"文件大小: {self._format_size(file_size)}")

                return {
                    "success": True,
                    "file_path": full_path,
                    "file_size": file_size,
                    "message": f"报表数据已保存到: {full_path}"
                }
            elif response.get('body'):
                # 如果没有 JSON，但有 body 内容
                body = response['body']

                # 尝试解析 body 为 JSON
                if isinstance(body, bytes):
                    body_str = body.decode('utf-8', errors='ignore')
                else:
                    body_str = str(body)

                try:
                    # 尝试解析为 JSON
                    body_json = json.loads(body_str)
                    with open(full_path, 'w', encoding='utf-8') as f:
                        json.dump(body_json, f, ensure_ascii=False, indent=2)
                except json.JSONDecodeError:
                    # 如果不是 JSON，直接保存原始内容
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(body_str)

                file_size = os.path.getsize(full_path)

                print(f"报表数据下载完成: {full_path}")
                print(f"文件大小: {self._format_size(file_size)}")

                return {
                    "success": True,
                    "file_path": full_path,
                    "file_size": file_size,
                    "message": f"报表数据已保存到: {full_path}"
                }
            else:
                return {"success": False, "error": "响应中没有数据"}

        except Exception as e:
            return {"success": False, "error": f"下载请求失败: {str(e)}"}

    async def query_report_count(self, id: int, start_time: str, end_time: str) -> Dict[str, Any]:
        """
        查询报表数据量

        Args:
            id: 报表ID
            start_time: 起始日期（格式：yyyyMMdd）
            end_time: 截止日期（格式：yyyyMMdd）

        Returns:
            包含count、error字段的字典
        """
        url = "/v2/tool/report_data/count"
        payload = {
            "id": id,
            "start_time": start_time,
            "end_time": end_time
        }

        try:
            response = await self.https_client.post(url, json=payload)

            if not response['ok']:
                return {"error": f"HTTP请求失败: {response['status']} {response['status_text']}"}

            result = response['json']
            if result is None:
                return {"error": "响应不是有效的JSON格式"}

            # 如果响应直接是数字（count值）
            if isinstance(result, (int, float)):
                return {
                    "count": int(result),
                    "report_id": id,
                    "start_date": start_time,
                    "end_date": end_time,
                    "raw_response": result
                }

            # 如果响应是字典
            if isinstance(result, dict):
                # 检查响应状态
                if result.get("status_code") != 0:
                    return {"error": f"查询失败: {result.get('status_msg', 'Unknown error')}"}

                # 提取数据量
                data_section = result.get("data", {})
                if isinstance(data_section, dict):
                    count = data_section.get("count", 0)
                else:
                    count = data_section if isinstance(data_section, (int, float)) else 0

                return {
                    "count": count,
                    "report_id": id,
                    "start_date": start_time,
                    "end_date": end_time,
                    "raw_response": result
                }

            return {"error": f"不支持的响应格式: {type(result)}"}

        except Exception as e:
            return {"error": f"查询数据量失败: {str(e)}"}

    async def query_report_sample(self, id: int, start_time: str, end_time: str) -> Dict[str, Any]:
        """
        查询报表样例数据

        Args:
            id: 报表ID
            start_time: 起始日期（格式：yyyyMMdd）
            end_time: 截止日期（格式：yyyyMMdd）

        Returns:
            包含columns、data、error字段的字典
        """
        url = "/v2/tool/report_data/sample"
        payload = {
            "id": id,
            "start_time": start_time,
            "end_time": end_time
        }

        try:
            response = await self.https_client.post(url, json=payload)

            if not response['ok']:
                return {"error": f"HTTP请求失败: {response['status']} {response['status_text']}"}

            result = response['json']
            if result is None:
                return {"error": "响应不是有效的JSON格式"}

            # 如果响应不是字典，尝试直接当作列表处理
            if isinstance(result, list):
                # 直接返回列表数据
                return {
                    "columns": [],
                    "data": result,
                    "report_id": id,
                    "start_time": start_time,
                    "end_time": end_time,
                    "total": len(result),
                    "raw_response": result
                }

            # 如果响应是字典
            if isinstance(result, dict):
                # 检查响应状态
                status_code = result.get("status_code")
                if status_code is not None and status_code != 0:
                    return {"error": f"查询失败: {result.get('status_msg', 'Unknown error')}"}

                # 提取 data 字段
                data_section = result.get("data", {})
                if isinstance(data_section, dict):
                    # 提取 table_data
                    table_data = data_section.get("table_data", {})
                    if isinstance(table_data, dict):
                        row_list = table_data.get("row_list", [])
                        column_info_list = table_data.get("column_info_list", [])
                        row_count = table_data.get("row_count", len(row_list))

                        # 构造列名列表（从 cn_name 提取）
                        columns = [col.get("cn_name", col.get("en_name", "")) if isinstance(col, dict) else str(col) for col in column_info_list]

                        # 转换行数据为字典格式
                        data = []
                        for row in row_list:
                            if isinstance(row, list) and len(row) == len(columns):
                                row_dict = {columns[i]: row[i] for i in range(len(columns))}
                                data.append(row_dict)
                            else:
                                # 如果列数不匹配，保持原始行数据
                                data.append(row)

                        return {
                            "columns": columns,
                            "data": data,
                            "report_id": id,
                            "start_time": start_time,
                            "end_time": end_time,
                            "total": row_count,
                            "raw_response": table_data  # 只返回 table_data 部分
                        }

                # 如果 data 直接是列表
                if isinstance(data_section, list):
                    return {
                        "columns": [],
                        "data": data_section,
                        "report_id": id,
                        "start_time": start_time,
                        "end_time": end_time,
                        "total": len(data_section),
                        "raw_response": data_section
                    }

                # 其他格式，直接返回 data
                return {
                    "columns": [],
                    "data": [],
                    "report_id": id,
                    "start_time": start_time,
                    "end_time": end_time,
                    "total": 0,
                    "raw_response": data_section
                }

            return {"error": f"不支持的响应格式: {type(result)}"}

        except Exception as e:
            return {"error": f"查询样例数据失败: {str(e)}"}

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

    async def close(self):
        """关闭客户端连接"""
        await self.https_client.close()

    async def __aenter__(self):
        """异步上下文管理器入口"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器退出"""
        await self.close()
