"""
SQL 执行工具
基于 PrestoQueryClient 调用接口执行 SQL 并下载结果文件
包含 SQL 执行、预览、计数和建表功能
"""
import os
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Any
from claude_agent_sdk import tool, create_sdk_mcp_server
import aiohttp
from .sql_query_client import SqlQueryClient
from .sql_query_https_client import SqlQueryHttpsClient
from app.core.config import settings
from app.utils.https_mtls_client import HttpsMtlsClient



# 配置信息通过环境变量获取
ENVIRONMENT = settings.environment #os.getenv("THS_TIER", "dev")  # dev 或 prod
#智能BI
JAVA_SERVICE_URL = settings.bi_container_host
#os.getenv("JAVA_SERVICE_URL", "http://localhost:8080")
# SQL_RESULTS_DIR = os.getenv("SQL_RESULTS_DIR", "./sql_results")

# HTTPS证书配置 (用于dev环境)
CERT_PATH = settings.ssl_cert_file#os.getenv("CERT_PATH", "/Users/itoch/Desktop/cert/zuolizheng@myhexin.com.p12")
CERT_PASSWORD = settings.ssl_cert_password#os.getenv("CERT_PASSWORD", "659029")
HTTPS_BASE_URL = settings.bi_domain#os.getenv("HTTPS_BASE_URL", "https://phonestat.hexin.cn/sdmp/easyfetch")

# 固定的请求邮箱 (用于建表工具)
CBAS_EMAIL = "huangnengxin@myhexin.com"

# 创建输出目录
# OUTPUT_DIR = Path(SQL_RESULTS_DIR)
# OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


@tool("download_sql_result", "执行SQL查询并下载结果文件", {"sql": str,"project_path":str})
async def download_sql_result_tool(args: dict[str, Any]) -> dict[str, Any]:
    """
    执行SQL查询并下载结果文件到本地

    Args:
        args: 包含以下键的字典:
            - sql: 要执行的 SQL 语句 (必需)

    Returns:
        包含执行结果信息的字典
    """
    sql = args["sql"]
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
            client = SqlQueryHttpsClient(
                cert_path=CERT_PATH,
                cert_password=CERT_PASSWORD,
                base_url=HTTPS_BASE_URL
            )
            # 调用下载方法
            result = await client.download_query_result(sql,file_path)

            # 关闭客户端
            await client.close()
        else:
            # prod环境使用普通HTTP
            client = SqlQueryClient(base_url=JAVA_SERVICE_URL)

            # 调用下载方法
            result = client.download_query_result(sql,file_path)

            # 关闭客户端
            client.close()

        if result.get("success"):
            return {
                "content": [{
                    "type": "text",
                    "text": f"SQL查询执行成功！\n文件保存路径: {result['file_path']}"
                }]
            }
        else:
            service_url = HTTPS_BASE_URL if ENVIRONMENT == "dev" else JAVA_SERVICE_URL
            return {
                "content": [{
                    "type": "text",
                    "text": f"SQL查询执行失败！\n错误信息: {result.get('error', 'Unknown error')}\n执行时间: {datetime.now().isoformat()}\n环境: {ENVIRONMENT}\n服务地址: {service_url}"
                }]
            }

    except Exception as e:
        service_url = HTTPS_BASE_URL if ENVIRONMENT == "dev" else JAVA_SERVICE_URL
        return {
            "content": [{
                "type": "text",
                "text": f"SQL查询执行异常！\n错误信息: {str(e)}\n执行时间: {datetime.now().isoformat()}\n环境: {ENVIRONMENT}\n服务地址: {service_url}"
            }]
        }


@tool("preview_sql_result", "预览SQL查询结果", {"sql": str})
async def preview_sql_result_tool(args: dict[str, Any]) -> dict[str, Any]:
    """
    预览SQL查询结果 (前100行)

    Args:
        args: 包含以下键的字典:
            - sql: 要执行的 SQL 语句

    Returns:
        包含预览结果信息的字典
    """
    sql = args["sql"]

    try:
        # 根据环境选择客户端
        if ENVIRONMENT == "dev":
            # dev环境使用HTTPS双向认证
            client = SqlQueryHttpsClient(
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
            client = SqlQueryClient(base_url=JAVA_SERVICE_URL)

            # 调用预览方法
            result = client.preview_query(sql=sql)

            # 关闭客户端
            client.close()

        if result.get("error"):
            return {
                "content": [{
                    "type": "text",
                    "text": f"SQL预览执行失败！\n错误信息: {result['error']}\n执行时间: {datetime.now().isoformat()}\n环境: {ENVIRONMENT}\n服务地址: {HTTPS_BASE_URL if ENVIRONMENT == 'dev' else JAVA_SERVICE_URL}"
                }]
            }
        else:
            # 返回raw_response数据
            return {
                "content": [{
                    "type": "text",
                    "text": str(result.get("raw_response", result))
                }]
            }

    except Exception as e:
        return {
            "content": [{
                "type": "text",
                "text": f"SQL预览执行异常！\n错误信息: {str(e)}\n执行时间: {datetime.now().isoformat()}\n环境: {ENVIRONMENT}\n服务地址: {HTTPS_BASE_URL if ENVIRONMENT == 'dev' else JAVA_SERVICE_URL}"
            }]
        }


# @tool("count_sql_result", "统计SQL查询结果数量", {"sql": str})
async def count_sql_result_tool(args: dict[str, Any]) -> dict[str, Any]:
    """
    统计SQL查询结果的行数

    Args:
        args: 包含以下键的字典:
            - sql: 要执行的 SQL 语句

    Returns:
        包含计数结果信息的字典
    """
    original_sql = args["sql"]

    try:
        # 构造计数SQL：SELECT COUNT(*) as cnt FROM (原SQL) as subquery
        count_sql = f"SELECT COUNT(*) as cnt FROM ({original_sql}) as subquery"

        # 根据环境选择客户端
        if ENVIRONMENT == "dev":
            # dev环境使用HTTPS双向认证
            client = SqlQueryHttpsClient(
                cert_path=CERT_PATH,
                cert_password=CERT_PASSWORD,
                base_url=HTTPS_BASE_URL
            )

            # 调用预览方法执行计数查询
            result = await client.preview_query(sql=count_sql)

            # 关闭客户端
            await client.close()
        else:
            # prod环境使用普通HTTP
            client = SqlQueryClient(base_url=JAVA_SERVICE_URL)

            # 调用预览方法执行计数查询
            result = client.preview_query(sql=count_sql)

            # 关闭客户端
            client.close()

        if result.get("error"):
            return {
                "content": [{
                    "type": "text",
                    "text": f"SQL计数执行失败！\n错误信息: {result['error']}\n原始SQL: {original_sql}\n计数SQL: {count_sql}\n执行时间: {datetime.now().isoformat()}\n环境: {ENVIRONMENT}\n服务地址: {HTTPS_BASE_URL if ENVIRONMENT == 'dev' else JAVA_SERVICE_URL}"
                }]
            }
        else:
            data = result.get("data", [])
            if data and len(data) > 0:
                # 获取计数结果
                count_value = data[0].get("cnt", 0) if isinstance(data[0], dict) else data[0][0] if isinstance(data[0], (list, tuple)) else 0

                return {
                    "content": [{
                        "type": "text",
                        "text": f"SQL计数执行成功！\n查询结果数量: {count_value}\n原始SQL: {original_sql}\n执行时间: {datetime.now().isoformat()}\n环境: {ENVIRONMENT}\n服务地址: {HTTPS_BASE_URL if ENVIRONMENT == 'dev' else JAVA_SERVICE_URL}"
                    }]
                }
            else:
                return {
                    "content": [{
                        "type": "text",
                        "text": f"SQL计数执行异常！\n无法获取计数结果\n原始SQL: {original_sql}\n计数SQL: {count_sql}\n执行时间: {datetime.now().isoformat()}\n环境: {ENVIRONMENT}\n服务地址: {HTTPS_BASE_URL if ENVIRONMENT == 'dev' else JAVA_SERVICE_URL}"
                    }]
                }

    except Exception as e:
        return {
            "content": [{
                "type": "text",
                "text": f"SQL计数执行异常！\n错误信息: {str(e)}\n原始SQL: {original_sql}\n执行时间: {datetime.now().isoformat()}\n环境: {ENVIRONMENT}\n服务地址: {HTTPS_BASE_URL if ENVIRONMENT == 'dev' else JAVA_SERVICE_URL}"
            }]
        }


@tool("create_table", "创建Hive或StarRocks表", {"catalog_type": str, "sql": str})
async def create_table_tool(args: dict[str, Any]) -> dict[str, Any]:
    """
    通过第三方接口创建 Hive 或 StarRocks 表

    支持 CREATE TABLE 和 CREATE TABLE AS SELECT 语法
    注意: 根据接口限制，只能在 db_test 库中创建表

    根据环境变量 THS_TIER 自动切换接口:
    - 开发环境 (dev/空): 使用 HTTPS 双向认证接口
    - 生产环境 (prod): 使用 HTTP 容器内部接口

    Args:
        args: 包含以下键的字典:
            - catalog_type: 数据源类型，可选值: hive, starrocks (必需)
            - sql: 建表SQL语句 (必需)

    Returns:
        包含建表结果信息的字典
    """
    catalog_type = args.get("catalog_type", "").lower()
    sql = args.get("sql", "").strip()

    # 参数验证
    if not catalog_type:
        return {
            "content": [{
                "type": "text",
                "text": "[FAIL] 建表失败！\n错误: catalog_type 不能为空\n说明: 必须指定数据源类型 (hive 或 starrocks)"
            }]
        }

    if catalog_type not in ["hive", "starrocks"]:
        return {
            "content": [{
                "type": "text",
                "text": f"[FAIL] 建表失败！\n错误: 不支持的数据源类型 '{catalog_type}'\n说明: catalog_type 必须是 'hive' 或 'starrocks'"
            }]
        }

    if not sql:
        return {
            "content": [{
                "type": "text",
                "text": "[FAIL] 建表失败！\n错误: sql 不能为空\n说明: 必须提供建表SQL语句"
            }]
        }

    # 验证SQL是否为CREATE语句
    sql_upper = sql.upper().strip()
    if not sql_upper.startswith("CREATE"):
        return {
            "content": [{
                "type": "text",
                "text": "[FAIL] 建表失败！\n错误: SQL必须是 CREATE TABLE 语句\n说明: 只支持 CREATE TABLE 或 CREATE TABLE AS SELECT 语句"
            }]
        }

    try:
        # 准备请求数据
        request_data = {
            "catalog_type": catalog_type,
            "sql": sql
        }

        # 准备请求头
        headers = {
            "Content-Type": "application/json",
            "CBAS_EMAIL": CBAS_EMAIL
        }

        # 根据环境选择不同的请求方式
        is_prod = ENVIRONMENT == "prod"

        if not is_prod:
            # 开发环境: 使用HTTPS双向认证
            api_url = f"{HTTPS_BASE_URL}/v2/tool/sql/create_table"

            # 初始化 HTTPS mTLS 客户端
            mtls_client = HttpsMtlsClient(
                cert_path=CERT_PATH,
                cert_password=CERT_PASSWORD,
                base_url=HTTPS_BASE_URL,
                timeout=3600,  # 1小时超时
                max_retries=2,
                verify_ssl=True
            )

            try:
                response = await mtls_client.post(
                    "/v2/tool/sql/create_table",
                    json=request_data,
                    headers=headers
                )

                # 关闭客户端
                await mtls_client.close()

                # 检查HTTP状态码
                if response['status'] != 200:
                    return {
                        "content": [{
                            "type": "text",
                            "text": f"[FAIL] 建表失败！\n错误: 服务器返回错误状态码 {response['status']}\n状态: {response.get('status_text', '')}\n环境: 开发环境 (HTTPS)\nAPI: {api_url}"
                        }]
                    }

                # 提取JSON响应
                response_data = response.get('json')
                if not response_data:
                    return {
                        "content": [{
                            "type": "text",
                            "text": f"[FAIL] 建表失败！\n错误: 服务器返回非JSON格式数据\n响应: {response.get('body', '')[:200]}\n环境: 开发环境 (HTTPS)\nAPI: {api_url}"
                        }]
                    }

            except Exception as e:
                await mtls_client.close()
                raise e

        else:
            # 生产环境: 使用HTTP
            api_url = f"{JAVA_SERVICE_URL}/v2/tool/sql/create_table"

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    api_url,
                    json=request_data,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=3600)  # 1小时超时
                ) as response:

                    # 读取响应
                    try:
                        response_data = await response.json()
                    except Exception:
                        response_text = await response.text()
                        return {
                            "content": [{
                                "type": "text",
                                "text": f"[FAIL] 建表失败！\n错误: 服务器返回非JSON格式数据\n响应: {response_text[:200]}\n环境: 生产环境 (HTTP)\nAPI: {api_url}"
                            }]
                        }

                    # 检查HTTP状态码
                    if response.status != 200:
                        return {
                            "content": [{
                                "type": "text",
                                "text": f"[FAIL] 建表失败！\n错误: 服务器返回错误状态码 {response.status}\n环境: 生产环境 (HTTP)\nAPI: {api_url}"
                            }]
                        }

        # 解析响应结果
        status_code = response_data.get("status_code", -1)
        status_msg = response_data.get("status_msg", "Unknown error")
        data = response_data.get("data")

        # 成功情况
        if status_code == 0:
            env_name = "开发环境 (HTTPS)" if not is_prod else "生产环境 (HTTP)"

            result_text = f"""[OK] 建表成功！

[INFO] 建表信息:
  - 数据源: {catalog_type}
  - 状态码: {status_code}
  - 状态消息: {status_msg}
  - 环境: {env_name}
  - API: {api_url}
"""

            if data:
                result_text += f"  - 返回数据: {data}\n"

            # 添加 SQL 预览 (修复 Python 3.10 f-string 嵌套引号问题)
            sql_preview = sql[:200]
            ellipsis = "..." if len(sql) > 200 else ""
            result_text += f"\n[TIP] SQL预览 (前200字符):\n{sql_preview}{ellipsis}"

            return {
                "content": [{
                    "type": "text",
                    "text": result_text
                }]
            }

        # 失败情况
        else:
            env_name = "开发环境 (HTTPS)" if not is_prod else "生产环境 (HTTP)"

            return {
                "content": [{
                    "type": "text",
                    "text": f"[FAIL] 建表失败！\n错误: {status_msg}\n状态码: {status_code}\n数据源: {catalog_type}\n环境: {env_name}\nAPI: {api_url}"
                }]
            }

    except aiohttp.ClientConnectorError as e:
        return {
            "content": [{
                "type": "text",
                "text": f"[FAIL] 建表失败！\n错误: 无法连接到API服务器\n详情: {str(e)}\n环境: {ENVIRONMENT}\n数据源: {catalog_type}"
            }]
        }

    except asyncio.TimeoutError:
        return {
            "content": [{
                "type": "text",
                "text": f"[FAIL] 建表失败！\n错误: API请求超时 (1小时)\n说明: 建表操作可能需要更长时间\n环境: {ENVIRONMENT}\n数据源: {catalog_type}"
            }]
        }

    except aiohttp.ClientError as e:
        return {
            "content": [{
                "type": "text",
                "text": f"[FAIL] 建表失败！\n错误: 网络请求错误\n详情: {str(e)}\n环境: {ENVIRONMENT}\n数据源: {catalog_type}"
            }]
        }

    except Exception as e:
        return {
            "content": [{
                "type": "text",
                "text": f"[FAIL] 建表失败！\n错误: 未知错误\n详情: {str(e)}\n环境: {ENVIRONMENT}\n数据源: {catalog_type}"
            }]
        }


# 创建 SDK MCP 服务器 - 包含所有 SQL 相关工具
sql_tools_server = create_sdk_mcp_server(
    name="sql",
    version="1.0.0",
    tools=[
        download_sql_result_tool,
        preview_sql_result_tool,
        create_table_tool  # 新增建表工具
    ]
)