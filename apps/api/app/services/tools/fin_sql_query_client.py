"""
金融查数接口客户端 (生产环境 HTTP)
用于调用金融数据查询接口,支持预览和下载CSV功能
"""
import requests
import csv
import os
from typing import Dict, Any
from datetime import datetime


class FinSqlQueryClient:
    """
    金融查数客户端,用于调用接口执行SQL并生成本地CSV文件
    """

    def __init__(self, base_url: str = "http://cbas-babel-frontend-prod:10399"):
        """
        初始化客户端

        Args:
            base_url: 服务的基础URL
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'FinSqlQueryClient-Python/1.0'
        })

    def preview_query(self, sql: str) -> Dict[str, Any]:
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
        url = f"{self.base_url}/bfe/internalSqlRun"

        # 使用 multipart/form-data 格式
        files = {
            'sql': (None, sql),
            'env': (None, 'prod')
        }

        try:
            response = self.session.post(url, files=files, timeout=30)
            response.raise_for_status()
            result = response.json()

            # 检查响应状态
            if result.get("status_code") != 0:
                return {"error": f"查询失败: {result.get('status_msg', 'Unknown error')}"}

            # 直接返回完整响应
            return result

        except requests.exceptions.RequestException as e:
            return {"error": f"预览请求失败: {str(e)}"}

    def download_query_result(self, sql: str, file_path: str = None) -> Dict[str, Any]:
        """
        执行SQL查询并下载结果为CSV文件

        Args:
            sql: SQL查询语句
            file_path: 本地文件保存目录,如果为None则保存到当前目录

        Returns:
            包含success、file_path、message等字段的字典
        """
        url = f"{self.base_url}/bfe/internalSqlRun"

        # 使用 multipart/form-data 格式
        files = {
            'sql': (None, sql),
            'env': (None, 'prod')
        }

        try:
            print(f"开始执行查询...")
            response = self.session.post(url, files=files, timeout=300)
            response.raise_for_status()
            result = response.json()

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
