"""
报表执行工具
基于 ReportQueryClient 调用接口执行报表查询、数据量查询和样例数据查询
"""
import os
from pathlib import Path
from typing import Any
from claude_agent_sdk import tool, create_sdk_mcp_server
from .report_query_client import ReportQueryClient
from .report_query_https_client import ReportQueryHttpsClient
from app.core.config import settings
from datetime import datetime


# 配置信息通过环境变量获取
ENVIRONMENT = settings.environment  # dev 或 prod
# 智能BI
JAVA_SERVICE_URL = settings.bi_container_host
REPORT_RESULTS_DIR = os.getenv("REPORT_RESULTS_DIR", "./report_results")

# HTTPS证书配置 (用于dev环境)
CERT_PATH = settings.ssl_cert_file
CERT_PASSWORD = settings.ssl_cert_password
HTTPS_BASE_URL = settings.bi_domain



@tool("download_report_data", "下载报表数据到本地文件", {

    "type":"object",
    "properties":{
        "id": {"type":"number"},
        "start_time": {"type":"string","description":"格式必须为yyyyMMdd"},
        "end_time": {"type":"string","description":"格式必须为yyyyMMdd"},
        "project_path":{"type":"string"}
    }
})
async def download_report_data_tool(args: dict[str, Any]) -> dict[str, Any]:
    """
    下载报表全量数据到本地文件

    Args:
        args: 包含以下键的字典:
            - id: 报表ID (必需)
            - start_time: 起始日期，格式：yyyyMMdd (必需)
            - end_time: 截止日期，格式：yyyyMMdd (必需)
            - project_path: 项目目录

    Returns:
        包含执行结果信息的字典
    """
    report_id = args["id"]
    start_time = args["start_time"]
    end_time = args["end_time"]
    project_path = args["project_path"]
    if not project_path :
        raise Exception("project_path 不能为空")
    
    file_path = os.path.join(project_path,"data_file","intermediate")
    if not os.path.exists(file_path):
        raise Exception("文件路径不存在，请检查project_path是否有误")
    try:
        # 根据环境选择客户端
        if ENVIRONMENT == "dev":
            # dev环境使用HTTPS双向认证
            client = ReportQueryHttpsClient(
                cert_path=CERT_PATH,
                cert_password=CERT_PASSWORD,
                base_url=HTTPS_BASE_URL
            )

            # 调用下载方法
            result = await client.download_report_data(
                id=report_id,
                start_time=str(start_time),
                end_time=str(end_time),
                file_path=file_path
            )

            # 关闭客户端
            await client.close()
        else:
            # prod环境使用普通HTTP
            client = ReportQueryClient(base_url=JAVA_SERVICE_URL)

            # 调用下载方法
            result = client.download_report_data(
                id=report_id,
                start_time=start_time,
                end_time=end_time,
                file_path=file_path
            )

            # 关闭客户端
            client.close()

        if result.get("success"):
            return {
                "content": [{
                    "type": "text",
                    "text": f"报表数据下载成功！\n报表ID: {report_id}\n日期范围: {start_time} 至 {end_time}\n文件保存路径: {result['file_path']}\n文件大小: {result.get('file_size', 0)} bytes"
                }]
            }
        else:
            service_url = HTTPS_BASE_URL if ENVIRONMENT == "dev" else JAVA_SERVICE_URL
            return {
                "content": [{
                    "type": "text",
                    "text": f"报表数据下载失败！\n报表ID: {report_id}\n日期范围: {start_time} 至 {end_time}\n错误信息: {result.get('error', 'Unknown error')}\n执行时间: {datetime.now().isoformat()}\n环境: {ENVIRONMENT}\n服务地址: {service_url}"
                }]
            }

    except Exception as e:
        service_url = HTTPS_BASE_URL if ENVIRONMENT == "dev" else JAVA_SERVICE_URL
        return {
            "content": [{
                "type": "text",
                "text": f"报表数据下载异常！\n报表ID: {report_id}\n日期范围: {start_time} 至 {end_time}\n错误信息: {str(e)}\n执行时间: {datetime.now().isoformat()}\n环境: {ENVIRONMENT}\n服务地址: {service_url}"
            }]
        }


@tool("query_report_count", "查询报表数据量", {
    "type":"object",
    "properties":{
        "id": {"type":"number"},
        "start_time": {"type":"string","description":"格式必须为yyyyMMdd"},
        "end_time": {"type":"string","description":"格式必须为yyyyMMdd"}
    }
})
async def query_report_count_tool(args: dict[str, Any]) -> dict[str, Any]:
    """
    查询报表数据量

    Args:
        args: 包含以下键的字典:
            - id: 报表ID (必需)
            - start_time: 起始日期，格式：yyyyMMdd (必需)
            - end_time: 截止日期，格式：yyyyMMdd (必需)

    Returns:
        包含执行结果信息的字典
    """
    report_id = args["id"]
    start_time = args["start_time"]
    end_time = args["end_time"]

    try:
        # 根据环境选择客户端
        if ENVIRONMENT == "dev":
            # dev环境使用HTTPS双向认证
            client = ReportQueryHttpsClient(
                cert_path=CERT_PATH,
                cert_password=CERT_PASSWORD,
                base_url=HTTPS_BASE_URL
            )

            # 调用查询方法
            result = await client.query_report_count(
                id=report_id,
                start_time=start_time,
                end_time=end_time
            )

            # 关闭客户端
            await client.close()
        else:
            # prod环境使用普通HTTP
            client = ReportQueryClient(base_url=JAVA_SERVICE_URL)

            # 调用查询方法
            result = client.query_report_count(
                id=report_id,
                start_time=str(start_time),
                end_time=str(end_time)
            )

            # 关闭客户端
            client.close()

        if result.get("error"):
            return {
                "content": [{
                    "type": "text",
                    "text": f"报表数据量查询失败！\n报表ID: {report_id}\n日期范围: {start_time} 至 {end_time}\n错误信息: {result['error']}\n执行时间: {datetime.now().isoformat()}\n环境: {ENVIRONMENT}\n服务地址: {HTTPS_BASE_URL if ENVIRONMENT == 'dev' else JAVA_SERVICE_URL}"
                }]
            }
        else:
            count = result.get("count", 0)
            return {
                "content": [{
                    "type": "text",
                    "text": f"报表数据量查询成功！\n报表ID: {report_id}\n日期范围: {start_time} 至 {end_time}\n数据量: {count} 条\n执行时间: {datetime.now().isoformat()}\n环境: {ENVIRONMENT}\n服务地址: {HTTPS_BASE_URL if ENVIRONMENT == 'dev' else JAVA_SERVICE_URL}"
                }]
            }

    except Exception as e:
        return {
            "content": [{
                "type": "text",
                "text": f"报表数据量查询异常！\n报表ID: {report_id}\n日期范围: {start_time} 至 {end_time}\n错误信息: {str(e)}\n执行时间: {datetime.now().isoformat()}\n环境: {ENVIRONMENT}\n服务地址: {HTTPS_BASE_URL if ENVIRONMENT == 'dev' else JAVA_SERVICE_URL}"
            }]
        }


@tool("preview_report_data", "预览报表样例数据，最多返回10条", 
    {
    "type":"object",
    "properties":{
        "id": {"type":"number"},
        "start_time": {"type":"string","description":"格式必须为yyyyMMdd"},
        "end_time": {"type":"string","description":"格式必须为yyyyMMdd"}
    }
    
})
async def preview_report_data_tool(args: dict[str, Any]) -> dict[str, Any]:
    """
    查询报表样例数据

    Args:
        args: 包含以下键的字典:
            - id: 报表ID (必需)
            - start_time: 起始日期，格式：yyyyMMdd (必需)
            - end_time: 截止日期，格式：yyyyMMdd (必需)

    Returns:
        包含执行结果信息的字典
    """
    report_id = args["id"]
    start_time = args["start_time"]
    end_time = args["end_time"]

    try:
        # 根据环境选择客户端
        if ENVIRONMENT == "dev":
            # dev环境使用HTTPS双向认证
            client = ReportQueryHttpsClient(
                cert_path=CERT_PATH,
                cert_password=CERT_PASSWORD,
                base_url=HTTPS_BASE_URL
            )

            # 调用查询方法
            result = await client.query_report_sample(
                id=report_id,
                start_time=start_time,
                end_time=end_time
            )

            # 关闭客户端
            await client.close()
        else:
            # prod环境使用普通HTTP
            client = ReportQueryClient(base_url=JAVA_SERVICE_URL)

            # 调用查询方法
            result = client.query_report_sample(
                id=report_id,
                start_time=str(start_time),
                end_time=str(end_time)
            )

            # 关闭客户端
            client.close()

        if result.get("error"):
            return {
                "content": [{
                    "type": "text",
                    "text": f"报表样例数据查询失败！\n报表ID: {report_id}\n日期范围: {start_time} 至 {end_time}\n错误信息: {result['error']}\n执行时间: {datetime.now().isoformat()}\n环境: {ENVIRONMENT}\n服务地址: {HTTPS_BASE_URL if ENVIRONMENT == 'dev' else JAVA_SERVICE_URL}"
                }]
            }
        else:
            # 返回raw_response数据
            data = result.get("data", [])
            columns = result.get("columns", [])
            total = result.get("total", 0)

            # 格式化输出
            output_text = f"报表样例数据查询成功！\n报表ID: {report_id}\n日期范围: {start_time} 至 {end_time}\n样例数量: {total} 条\n列信息: {', '.join(columns)}\n\n样例数据:\n{str(result.get('raw_response', result))}"

            return {
                "content": [{
                    "type": "text",
                    "text": output_text
                }]
            }

    except Exception as e:
        return {
            "content": [{
                "type": "text",
                "text": f"报表样例数据查询异常！\n报表ID: {report_id}\n日期范围: {start_time} 至 {end_time}\n错误信息: {str(e)}\n执行时间: {datetime.now().isoformat()}\n环境: {ENVIRONMENT}\n服务地址: {HTTPS_BASE_URL if ENVIRONMENT == 'dev' else JAVA_SERVICE_URL}"
            }]
        }


# 创建 SDK MCP 服务器
report_tools_server = create_sdk_mcp_server(
    name="report",
    version="1.0.0",
    tools=[download_report_data_tool, preview_report_data_tool]
)
