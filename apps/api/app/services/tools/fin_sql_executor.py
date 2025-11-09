"""
金融查数工具
基于金融查数接口执行 SQL 查询,支持预览和下载CSV功能
"""
import os
from datetime import datetime
from typing import Any
from claude_agent_sdk import tool, create_sdk_mcp_server
from .fin_sql_query_client import FinSqlQueryClient
from .fin_sql_query_https_client import FinSqlQueryHttpsClient
from app.core.config import settings


# 配置信息通过环境变量获取
ENVIRONMENT = settings.environment  # dev 或 prod

# 开发环境 HTTPS 配置
CERT_PATH = settings.ssl_cert_file
CERT_PASSWORD = settings.ssl_cert_password
HTTPS_BASE_URL = settings.fin_sql_domain

# 生产环境 HTTP 配置
HTTP_BASE_URL = settings.fin_sql_container_host


@tool("preview_fin_sql_result", "预览金融数据查询结果", {"sql": str})
async def preview_fin_sql_result_tool(args: dict[str, Any]) -> dict[str, Any]:
    """
    预览金融数据SQL查询结果

    Args:
        args: 包含以下键的字典:
            - sql: 要执行的 SQL 语句 (必需)

    Returns:
        包含预览结果信息的字典
    """
    sql = args["sql"]

    try:
        # 根据环境选择客户端
        if ENVIRONMENT == "dev":
            # dev环境使用HTTPS双向认证
            client = FinSqlQueryHttpsClient(
                cert_path=CERT_PATH,
                cert_password=CERT_PASSWORD,
                base_url=HTTPS_BASE_URL
            )

            # 调用预览方法
            result = await client.preview_query(sql=sql)

            # 关闭客户端
            await client.close()
        else:
            # prod环境使用普通HTTP
            client = FinSqlQueryClient(base_url=HTTP_BASE_URL)

            # 调用预览方法
            result = client.preview_query(sql=sql)

            # 关闭客户端
            client.close()

        if result.get("error"):
            return {
                "content": [{
                    "type": "text",
                    "text": f"金融数据预览执行失败！\n错误信息: {result['error']}\n执行时间: {datetime.now().isoformat()}\n环境: {ENVIRONMENT}\n服务地址: {HTTPS_BASE_URL if ENVIRONMENT == 'dev' else HTTP_BASE_URL}"
                }]
            }
        else:
            # 返回完整的JSON响应数据
            return {
                "content": [{
                    "type": "text",
                    "text": str(result)
                }]
            }

    except Exception as e:
        return {
            "content": [{
                "type": "text",
                "text": f"金融数据预览执行异常！\n错误信息: {str(e)}\n执行时间: {datetime.now().isoformat()}\n环境: {ENVIRONMENT}\n服务地址: {HTTPS_BASE_URL if ENVIRONMENT == 'dev' else HTTP_BASE_URL}"
            }]
        }


@tool("download_fin_sql_result", "下载金融数据查询结果为CSV文件", {"sql": str, "project_path": str})
async def download_fin_sql_result_tool(args: dict[str, Any]) -> dict[str, Any]:
    """
    执行金融数据SQL查询并下载结果为CSV文件到本地

    Args:
        args: 包含以下键的字典:
            - sql: 要执行的 SQL 语句 (必需)
            - project_path: 项目路径 (必需)

    Returns:
        包含执行结果信息的字典
    """
    sql = args["sql"]
    project_path = args["project_path"]

    if not project_path:
        raise Exception("project_path 不能为空")

    file_path = os.path.join(project_path, "data_file", "intermediate")
    if not os.path.exists(file_path):
        raise Exception("文件路径不存在,请检查project_path是否有误")

    try:
        # 根据环境选择客户端
        if ENVIRONMENT == "dev":
            # dev环境使用HTTPS双向认证
            client = FinSqlQueryHttpsClient(
                cert_path=CERT_PATH,
                cert_password=CERT_PASSWORD,
                base_url=HTTPS_BASE_URL
            )
            # 调用下载方法
            result = await client.download_query_result(sql, file_path)

            # 关闭客户端
            await client.close()
        else:
            # prod环境使用普通HTTP
            client = FinSqlQueryClient(base_url=HTTP_BASE_URL)

            # 调用下载方法
            result = client.download_query_result(sql, file_path)

            # 关闭客户端
            client.close()

        if result.get("success"):
            return {
                "content": [{
                    "type": "text",
                    "text": f"金融数据查询执行成功！\n文件保存路径: {result['file_path']}\n总行数: {result.get('total_rows', 'N/A')}\n文件大小: {result.get('file_size', 'N/A')} bytes"
                }]
            }
        else:
            service_url = HTTPS_BASE_URL if ENVIRONMENT == "dev" else HTTP_BASE_URL
            return {
                "content": [{
                    "type": "text",
                    "text": f"金融数据查询执行失败！\n错误信息: {result.get('error', 'Unknown error')}\n执行时间: {datetime.now().isoformat()}\n环境: {ENVIRONMENT}\n服务地址: {service_url}"
                }]
            }

    except Exception as e:
        service_url = HTTPS_BASE_URL if ENVIRONMENT == "dev" else HTTP_BASE_URL
        return {
            "content": [{
                "type": "text",
                "text": f"金融数据查询执行异常！\n错误信息: {str(e)}\n执行时间: {datetime.now().isoformat()}\n环境: {ENVIRONMENT}\n服务地址: {service_url}"
            }]
        }


# 创建 SDK MCP 服务器 - 包含金融查数相关工具
fin_sql_tools_server = create_sdk_mcp_server(
    name="fin_sql",
    version="1.0.0",
    tools=[
        preview_fin_sql_result_tool,
        download_fin_sql_result_tool
    ]
)
