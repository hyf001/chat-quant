import requests
import json
import os
from typing import Optional, Dict, Any
import time
from datetime import datetime


class SqlQueryClient:
    """
    Presto查询客户端，用于调用Java服务接口执行SQL并生成本地文件
    """

    def __init__(self, base_url: str = "http://localhost:8080"):
        """
        初始化客户端

        Args:
            base_url: Java服务的基础URL
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            "CBAS_EMAIL": "zuolizheng@myhexin.com",
            'User-Agent': 'PrestoQueryClient-Python/1.0'
        })

    def preview_query(self, sql: str, catalog_name: str = "presto-hive") -> Dict[str, Any]:
        """
        预览查询结果（根据 presto查询.md 接口规范）

        Args:
            sql: SQL查询语句
            catalog_name: 目录名称，默认为 "presto-hive"

        Returns:
            包含columns、data、error字段的字典，格式兼容原有调用方式
        """
        url = f"{self.base_url}/v2/tool/data/fetch"
        payload = {
            "sql": sql,
            "catalog_name": catalog_name
        }

        try:
            response = self.session.post(url, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()

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

        except requests.exceptions.RequestException as e:
            return {"error": f"预览请求失败: {str(e)}"}

    def download_query_result(self, sql: str, file_path: str = None,
                            custom_filename: str = None) -> Dict[str, Any]:
        """
        执行SQL查询并下载结果到本地文件

        Args:
            sql: SQL查询语句
            file_path: 本地文件保存路径，如果为None则保存到当前目录
            custom_filename: 自定义文件名

        Returns:
            包含success、file_path、message等字段的字典
        """
        url = f"{self.base_url}/v2/tool/data/fetch_presto_download"
        payload = {"sql": sql}

        if custom_filename:
            payload["fileName"] = custom_filename

        try:
            print(f"开始执行查询...")
            response = self.session.post(url, json=payload, stream=True, timeout=300)
            response.raise_for_status()

            # 获取文件名
            filename = self._extract_filename(response, custom_filename)

            # 确定保存路径
            if file_path is None:
                file_path = os.getcwd()

            if os.path.isdir(file_path):
                full_path = os.path.join(file_path, filename)
            else:
                full_path = file_path

            # 确保目录存在
            os.makedirs(os.path.dirname(full_path) if os.path.dirname(full_path) else '.', exist_ok=True)

            # 流式写入文件
            file_size = 0
            with open(full_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        file_size += len(chunk)

            print(f"文件下载完成: {full_path}")
            print(f"文件大小: {self._format_size(file_size)}")

            return {
                "success": True,
                "file_path": full_path,
                "file_size": file_size,
                "message": f"查询结果已保存到: {full_path}"
            }

        except requests.exceptions.RequestException as e:
            error_msg = f"下载失败: {str(e)}"
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.text
                    error_msg += f" - {error_detail}"
                except:
                    pass
            return {"success": False, "error": error_msg}
        except Exception as e:
            return {"success": False, "error": f"保存文件失败: {str(e)}"}


    def _extract_filename(self, response: requests.Response, custom_filename: str = None) -> str:
        """从响应头中提取文件名"""
        if custom_filename:
            return custom_filename if custom_filename.endswith('.csv') else f"{custom_filename}.csv"

        content_disposition = response.headers.get('Content-Disposition', '')
        if 'filename=' in content_disposition:
            import re
            match = re.search(r'filename=([^;\s]+)', content_disposition)
            if match:
                return match.group(1)

        # 默认文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"query_result_{timestamp}.csv"

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

    
    def close(self):
        """关闭会话"""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()