"""
Data processing utilities for MCP responses
"""

import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Tuple, Optional
from .business_line import extract_business_line
from ..config.field_metadata import get_all_field_comments

logger = logging.getLogger(__name__)


def parse_json_data(json_str: str) -> Dict[str, Any]:
    """
    解析JSON配置数据，处理嵌套JSON

    Args:
        json_str: JSON字符串

    Returns:
        Dict[str, Any]: 解析后的数据
    """
    try:
        data = json.loads(json_str)

        # 处理嵌套的JSON字符串
        for key, value in data.items():
            if isinstance(value, str) and value.strip().startswith('{'):
                try:
                    data[key] = json.loads(value)
                except json.JSONDecodeError:
                    # 解析失败保持原值
                    logger.debug(f"嵌套JSON解析失败: {key}")
                    pass

        return data

    except json.JSONDecodeError as e:
        logger.warning(f"JSON解析失败: {json_str[:100]}...")
        return {
            "raw_config": json_str,
            "parse_error": str(e)
        }


def sanitize_filename(filename: str) -> str:
    """
    清理文件名，移除不安全字符

    Args:
        filename: 原始文件名

    Returns:
        str: 安全的文件名
    """
    import re

    # 移除或替换不安全的文件名字符
    safe_name = re.sub(r'[<>:"/\\|?*]', '_', filename)
    safe_name = safe_name.strip()

    # 确保文件名不为空
    if not safe_name:
        safe_name = "unnamed_datasource"

    # 限制文件名长度
    if len(safe_name) > 100:
        safe_name = safe_name[:100]

    return safe_name


def build_datasource_yaml_data(datasource: Dict[str, Any],
                              connection_config: Dict[str, Any],
                              business_line: str,
                              export_time: str,
                              mcp_tool: str) -> Dict[str, Any]:
    """
    构建数据源YAML数据结构 - 只保留MCP返回的原始字段，并按指定顺序排列

    Args:
        datasource: 原始数据源信息
        connection_config: 解析后的连接配置（不使用）
        business_line: 业务线标识
        export_time: 导出时间
        mcp_tool: MCP工具名称

    Returns:
        Dict[str, Any]: YAML数据结构（只包含原始字段，按指定顺序）
    """
    # 定义字段顺序
    field_order = [
        "id",
        "name",
        "business_segment",
        "principal",
        "description",
        "data_source_type",
        "data_source_version",
        "json_data"
    ]

    # 按指定顺序构建YAML数据
    yaml_data = {}
    for field in field_order:
        if field in datasource:
            value = datasource[field]
            # 特殊处理json_data字段：格式化为多行JSON字符串
            if field == "json_data" and isinstance(value, str):
                try:
                    # 解析后重新格式化为缩进的JSON字符串
                    parsed = json.loads(value)
                    yaml_data[field] = json.dumps(parsed, indent=2, ensure_ascii=False)
                except json.JSONDecodeError:
                    # 解析失败则保持原值
                    yaml_data[field] = value
            else:
                yaml_data[field] = value

    # 添加其他未在顺序列表中的字段（如果有）
    for key, value in datasource.items():
        if key not in yaml_data:
            # 对其他可能的JSON字段也做同样处理
            if isinstance(value, str) and value.strip().startswith('{'):
                try:
                    parsed = json.loads(value)
                    yaml_data[key] = json.dumps(parsed, indent=2, ensure_ascii=False)
                except json.JSONDecodeError:
                    yaml_data[key] = value
            else:
                yaml_data[key] = value

    # 添加字段注释（内部使用，不会写入YAML文件）
    yaml_data["_field_comments"] = get_all_field_comments(yaml_data)

    return yaml_data


def build_transmission_task_yaml_data(task: Dict[str, Any],
                                     business_line: str,
                                     export_time: str,
                                     mcp_tool: str) -> Dict[str, Any]:
    """
    构建传输任务YAML数据结构 - 只保留MCP返回的原始字段，并按指定顺序排列

    Args:
        task: 原始传输任务信息
        business_line: 业务线标识
        export_time: 导出时间
        mcp_tool: MCP工具名称

    Returns:
        Dict[str, Any]: YAML数据结构（只包含原始字段，按指定顺序）
    """
    # 定义字段顺序
    field_order = [
        "id",
        "name",
        "business_segment",
        "principles",
        "description",
        "compute_type",
        "create_model",
        "running_model",
        "source_type",
        "target_type",
        "task_text"
    ]

    # 按指定顺序构建YAML数据
    yaml_data = {}
    for field in field_order:
        if field in task:
            value = task[field]
            # 特殊处理task_text字段：格式化为多行JSON字符串
            if field == "task_text" and isinstance(value, str):
                try:
                    # 解析后重新格式化为缩进的JSON字符串
                    parsed = json.loads(value)
                    yaml_data[field] = json.dumps(parsed, indent=2, ensure_ascii=False)
                except json.JSONDecodeError:
                    # 解析失败则保持原值
                    yaml_data[field] = value
            # 特殊处理principles字段：如果是JSON数组字符串，解析为真正的数组
            elif field == "principles" and isinstance(value, str):
                # 如果是字符串 "null"、"None" 等，转换为空数组
                if value.strip().lower() in ['null', 'none', '']:
                    yaml_data[field] = []
                else:
                    try:
                        parsed = json.loads(value)
                        # 如果解析后是list，使用解析后的list；否则保持原值
                        if isinstance(parsed, list):
                            yaml_data[field] = parsed
                        else:
                            yaml_data[field] = value
                    except json.JSONDecodeError:
                        # 解析失败则保持原值
                        yaml_data[field] = value
            else:
                yaml_data[field] = value

    # 添加其他未在顺序列表中的字段（如果有）
    for key, value in task.items():
        if key not in yaml_data:
            # 尝试解析JSON字符串（对象或数组）
            if isinstance(value, str) and value.strip():
                stripped_value = value.strip()
                # 如果是JSON对象字符串，格式化为多行
                if stripped_value.startswith('{'):
                    try:
                        parsed = json.loads(value)
                        yaml_data[key] = json.dumps(parsed, indent=2, ensure_ascii=False)
                    except json.JSONDecodeError:
                        yaml_data[key] = value
                # 如果是JSON数组字符串，解析为真正的数组
                elif stripped_value.startswith('['):
                    try:
                        parsed = json.loads(value)
                        if isinstance(parsed, list):
                            yaml_data[key] = parsed
                        else:
                            yaml_data[key] = value
                    except json.JSONDecodeError:
                        yaml_data[key] = value
                else:
                    yaml_data[key] = value
            else:
                yaml_data[key] = value

    # 添加字段注释（内部使用，不会写入YAML文件）
    yaml_data["_field_comments"] = get_all_field_comments(yaml_data, field_type="transmission_task")

    return yaml_data


def process_datasource_data(mcp_response: Dict[str, Any],
                           mcp_tool: str = "mcp__data_transmission__datasource_list") -> Tuple[List[Dict[str, Any]], Dict[str, int]]:
    """
    处理数据源MCP响应数据

    Args:
        mcp_response: MCP响应数据
        mcp_tool: MCP工具名称

    Returns:
        Tuple[List[Dict[str, Any]], Dict[str, int]]: (处理后的数据源列表, 业务线统计)
    """
    headers = mcp_response["data"]["headers"]
    rows = mcp_response["data"]["rows"]

    processed_datasources = []
    business_line_stats = {}
    export_time = datetime.now().isoformat()

    logger.info(f"开始处理 {len(rows)} 个数据源")

    for i, row in enumerate(rows):
        try:
            # 构建数据源字典
            datasource = dict(zip(headers, row))

            # 解析JSON配置
            json_data = datasource.get("json_data", "{}")
            connection_config = parse_json_data(json_data)

            # 识别业务线
            business_line = extract_business_line(datasource.get("principal", ""))

            # 构建YAML数据
            yaml_data = build_datasource_yaml_data(
                datasource=datasource,
                connection_config=connection_config,
                business_line=business_line,
                export_time=export_time,
                mcp_tool=mcp_tool
            )

            # 添加文件路径信息
            # 使用数据源的实际name字段，如果没有name字段则使用ID或索引
            name_field = datasource.get("name")
            if name_field:
                filename = sanitize_filename(name_field)
            elif datasource.get("id"):
                filename = f"datasource_id_{datasource['id']}"
            else:
                filename = f"datasource_{i}"

            yaml_data["_file_info"] = {
                "filename": f"{filename}.yaml",
                "business_line": business_line,
                "category": "data_source"
            }

            processed_datasources.append(yaml_data)

            # 更新业务线统计
            business_line_stats[business_line] = business_line_stats.get(business_line, 0) + 1

            logger.debug(f"处理数据源: {datasource.get('name')} -> {business_line}")

        except Exception as e:
            logger.error(f"处理数据源失败 (第{i+1}行): {str(e)}")
            logger.debug(f"失败的数据行: {row}")
            continue

    logger.info(f"数据源处理完成: 成功 {len(processed_datasources)}, 失败 {len(rows) - len(processed_datasources)}")
    logger.info(f"业务线分布: {business_line_stats}")

    return processed_datasources, business_line_stats


def generate_export_report(exported_files: List[str],
                          business_line_stats: Dict[str, int],
                          command: str,
                          mcp_tool: str,
                          start_time: datetime,
                          end_time: datetime) -> Dict[str, Any]:
    """
    生成导出报告

    Args:
        exported_files: 导出文件列表
        business_line_stats: 业务线统计
        command: 执行的命令
        mcp_tool: MCP工具名称
        start_time: 开始时间
        end_time: 结束时间

    Returns:
        Dict[str, Any]: 导出报告数据
    """
    duration = (end_time - start_time).total_seconds()

    # 计算文件统计（只统计文件数量，不包含 size）
    file_stats_by_business_line = {}
    for file_path in exported_files:
        # 从文件路径提取业务线
        parts = file_path.replace("\\", "/").split("/")
        business_line = "unknown"
        for part in parts:
            if part in business_line_stats:
                business_line = part
                break

        if business_line not in file_stats_by_business_line:
            file_stats_by_business_line[business_line] = {
                "files": 0
            }
        file_stats_by_business_line[business_line]["files"] += 1

    report = {
        "export_summary": {
            "export_id": f"exp_{end_time.strftime('%Y%m%d_%H%M%S')}",
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "duration_seconds": round(duration, 2),
            "command": command,
            "mcp_tool": mcp_tool,
            "total_exported": len(exported_files),
            "business_line_distribution": business_line_stats,
            "status": "success"
        },
        "file_summary": {
            "total_files": len(exported_files),
            "by_business_line": file_stats_by_business_line
        }
    }

    return report


def validate_mcp_response(response: Dict[str, Any]) -> bool:
    """
    验证MCP响应格式

    Args:
        response: MCP响应

    Returns:
        bool: 是否有效
    """
    try:
        # 检查基本结构
        if not isinstance(response, dict):
            return False

        # 检查状态码
        if response.get("statusCode") != 0:
            return False

        # 检查数据结构
        data = response.get("data")
        if not data or not isinstance(data, dict):
            return False

        # 检查headers和rows
        headers = data.get("headers")
        rows = data.get("rows")

        if not isinstance(headers, list) or not isinstance(rows, list):
            return False

        # 检查数据一致性
        if rows and len(rows[0]) != len(headers):
            return False

        return True

    except Exception:
        return False