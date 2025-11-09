"""
SQL 校验工具
使用 SQLGlot 验证 SQL 语法的正确性
"""
from typing import Any
from claude_agent_sdk import tool, create_sdk_mcp_server
import sqlglot
from sqlglot import ParseError


@tool("validate_sql", "验证SQL语句的语法正确性", {"sql": str, "engine": str})
async def validate_sql_tool(args: dict[str, Any]) -> dict[str, Any]:
    """
    验证SQL语句的语法正确性

    支持的数据库引擎:
    - presto: Facebook开源的分布式SQL查询引擎
    - hive: Apache Hive数据仓库
    - starrocks: 高性能分析型数据库

    Args:
        args: 包含以下键的字典:
            - sql: 要验证的SQL语句 (必需)
            - engine: 数据库引擎类型 (可选，默认为 hive)

    Returns:
        包含验证结果信息的字典
    """
    sql = args.get("sql", "").strip()
    engine = args.get("engine", "hive").lower()

    # 参数验证
    if not sql:
        return {
            "content": [{
                "type": "text",
                "text": "[FAIL] SQL验证失败！\n错误: SQL语句不能为空"
            }]
        }

    # 验证引擎类型
    supported_engines = ["presto", "hive", "starrocks"]
    if engine not in supported_engines:
        return {
            "content": [{
                "type": "text",
                "text": f"[FAIL] SQL验证失败！\n错误: 不支持的数据库引擎 '{engine}'\n支持的引擎: {', '.join(supported_engines)}"
            }]
        }

    try:
        # 使用 SQLGlot 解析 SQL
        parsed_statements = sqlglot.parse(
            sql,
            read=engine,
            error_level=sqlglot.ErrorLevel.RAISE
        )

        if not parsed_statements:
            return {
                "content": [{
                    "type": "text",
                    "text": f"[FAIL] SQL验证失败！\n错误: 无法解析SQL语句，可能包含语法错误\n引擎: {engine}"
                }]
            }

        # 统计成功解析的语句数量
        valid_count = sum(1 for stmt in parsed_statements if stmt is not None)

        # 生成验证结果消息
        sql_preview = sql[:200]
        ellipsis = "..." if len(sql) > 200 else ""
        result_text = f"""[OK] SQL语法验证通过！

[INFO] 验证信息:
  - 数据库引擎: {engine}
  - 解析语句数: {valid_count}
  - 验证状态: 成功

[TIP] SQL预览 (前200字符):
{sql_preview}{ellipsis}
"""

        return {
            "content": [{
                "type": "text",
                "text": result_text
            }]
        }

    except ParseError as e:
        # 提取解析错误的详细信息
        error_details = _extract_parse_error(e, sql)

        error_text = f"""[FAIL] SQL语法验证失败！

[DEBUG] 错误信息:
  - 错误描述: {error_details.get('message', str(e))}
  - 数据库引擎: {engine}
"""

        # 添加行号和列号信息（如果有）
        if error_details.get('line'):
            error_text += f"  - 错误行号: {error_details['line']}\n"
        if error_details.get('column'):
            error_text += f"  - 错误列号: {error_details['column']}\n"

        # 添加修复建议（如果有）
        suggestions = error_details.get('suggestions', [])
        if suggestions:
            error_text += f"\n[TIP] 修复建议:\n"
            for suggestion in suggestions:
                error_text += f"  - {suggestion}\n"

        return {
            "content": [{
                "type": "text",
                "text": error_text
            }]
        }

    except Exception as e:
        return {
            "content": [{
                "type": "text",
                "text": f"[FAIL] SQL验证异常！\n错误: {str(e)}\n引擎: {engine}"
            }]
        }


def _extract_parse_error(error: ParseError, sql: str) -> dict[str, Any]:
    """提取解析错误的详细信息"""
    error_msg = str(error)
    error_list = error.errors if hasattr(error, 'errors') else [error]

    # 提取第一个错误的详细信息
    first_error = error_list[0] if error_list else error

    result = {
        "message": str(first_error),
        "suggestions": []
    }

    # 尝试提取行号和列号
    if hasattr(first_error, 'line'):
        result["line"] = first_error.line
    if hasattr(first_error, 'col'):
        result["column"] = first_error.col
    if hasattr(first_error, 'context'):
        result["context"] = first_error.context

    # 生成修复建议
    error_str = error_msg.lower()
    if "expected" in error_str and "from" in error_str:
        result["suggestions"].append("检查是否缺少 FROM 子句")
    if "where" in error_str:
        result["suggestions"].append("检查 WHERE 子句是否完整")
    if "select" in error_str:
        result["suggestions"].append("检查 SELECT 语句的列名是否正确")
    if "table" in error_str:
        result["suggestions"].append("检查表名是否正确")
    if "column" in error_str:
        result["suggestions"].append("检查列名是否存在")

    return result


# 创建 SDK MCP 服务器
sql_validator_server = create_sdk_mcp_server(
    name="sql-validator-tool",
    version="1.0.0",
    tools=[validate_sql_tool]
)
