import requests
import json
import os
from typing import Optional, Dict, Any
from datetime import datetime


class ReportQueryClient:
    """
    报表查询客户端，用于调用报表服务接口（生产环境）
    """

    def __init__(self, base_url: str = "http://localhost:8080"):
        """
        初始化客户端

        Args:
            base_url: 报表服务的基础URL
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            "CBAS_EMAIL": "zuolizheng@myhexin.com",
            'User-Agent': 'ReportQueryClient-Python/1.0'
        })

    def download_report_data(self, id: str, start_time: str, end_time: str,
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
        url = f"{self.base_url}/v2/tool/report_data/fetch"
        payload = {
            "id": id,
            "start_time": start_time,
            "end_time": end_time
        }

        try:
            print(f"开始下载报表数据: {id}")
            response = self.session.post(url, json=payload, stream=True, timeout=300)
            response.raise_for_status()

            # 获取文件名
            filename = self._extract_filename(response, id, start_time, end_time)

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

            print(f"报表数据下载完成: {full_path}")
            print(f"文件大小: {self._format_size(file_size)}")

            return {
                "success": True,
                "file_path": full_path,
                "file_size": file_size,
                "message": f"报表数据已保存到: {full_path}"
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

    def query_report_count(self, id: str, start_time: str, end_time: str) -> Dict[str, Any]:
        """
        查询报表数据量

        Args:
            id: 报表ID
            start_time: 起始日期（格式：yyyyMMdd）
            end_time: 截止日期（格式：yyyyMMdd）

        Returns:
            包含count、error字段的字典
        """
        url = f"{self.base_url}/v2/tool/report_data/count"
        payload = {
            "id": id,
            "start_time": start_time,
            "end_time": end_time
        }

        try:
            response = self.session.post(url, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()

            # 检查响应状态
            if result.get("status_code") != 0:
                return {"error": f"查询失败: {result.get('status_msg', 'Unknown error')}"}

            # 提取数据量
            data_section = result.get("data", {})
            count = data_section.get("count", 0)

            return {
                "count": count,
                "id": id,
                "start_time": start_time,
                "end_time": end_time,
                "raw_response": result
            }

        except requests.exceptions.RequestException as e:
            return {"error": f"查询数据量失败: {str(e)}"}

    def query_report_sample(self, id: str, start_time: str, end_time: str) -> Dict[str, Any]:
        """
        查询报表样例数据

        Args:
            id: 报表ID
            start_time: 起始日期（格式：yyyyMMdd）
            end_time: 截止日期（格式：yyyyMMdd）

        Returns:
            包含columns、data、error字段的字典
        """
        url = f"{self.base_url}/v2/tool/report_data/sample"
        payload = {
            "id": id,
            "start_time": start_time,
            "end_time": end_time
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
            sample_result = data_section.get("result", {})

            # 转换为原有格式，保持兼容性
            row_list = sample_result.get("row_list", [])
            column_info_list = sample_result.get("column_info_list", [])

            # 构造列名列表
            columns = [col["name"] for col in column_info_list]

            # 转换行数据为字典格式
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
                "id": id,
                "start_time": start_time,
                "end_time": end_time,
                "total": len(data),
                "raw_response": result
            }

        except requests.exceptions.RequestException as e:
            return {"error": f"查询样例数据失败: {str(e)}"}

    def _extract_filename(self, response: requests.Response, id: str,
                         start_time: str, end_time: str) -> str:
        """从响应头中提取文件名"""
        content_disposition = response.headers.get('Content-Disposition', '')
        if 'filename=' in content_disposition:
            import re
            match = re.search(r'filename=([^;\s]+)', content_disposition)
            if match:
                return match.group(1)

        # 默认文件名：report_{id}_{start_time}_to_{end_time}.csv
        return f"report_{id}_{start_time}_to_{end_time}.csv"

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
