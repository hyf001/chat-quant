"""
字段元数据定义 - 用于YAML导出时添加字段注释
"""

from typing import Dict, Any, Optional


# 数据源类型枚举
DATA_SOURCE_TYPES = {
    1: "MYSQL",
    2: "STARROCKS",
    3: "ORACLE",
    4: "HIVE",
    5: "FTP",
    6: "HDFS",
    7: "KAFKA",
    8: "MONGODB",
    9: "REDIS",
    10: "HTTP",
    11: "POSTGRESQL",
    12: "ELASTICSEARCH"
}

# 数据源版本枚举
DATA_SOURCE_VERSIONS = {
    1: "MYSQL5",
    2: "ORACLE",
    3: "HIVE1.x",
    4: "HIVE2.x",
    5: "FTP",
    6: "HDFS2.x",
    7: "HDFS3.x",
    8: "MONGODB",
    10: "HTTP",
    11: "POSTGRESQL",
    14: "STARROCKS",
    15: "ELASTICSEARCH7.x",
    16: "ELASTICSEARCH8.x",
    17: "KAFKA2.x"
}

# 数据源字段描述映射
DATASOURCE_FIELD_COMMENTS = {
    "id": "数据源ID",
    "name": "数据源名称",
    "business_segment": "业务线标识",
    "principal": "负责人（多个以逗号分隔）",
    "description": "数据源描述",
    "data_source_type": f"数据源类型：{', '.join(f'{k}: {v}' for k, v in DATA_SOURCE_TYPES.items())}",
    "data_source_version": f"数据源版本：{', '.join(f'{k}: {v}' for k, v in DATA_SOURCE_VERSIONS.items())}",
    "json_data": "连接配置JSON（包含jdbcUrl、database、username、password等）",
    "cluster_sign": "集群标识",
    "internal_source": "是否内部数据源：0: 否, 1: 是"
}

# 传输任务字段描述映射
TRANSMISSION_TASK_FIELD_COMMENTS = {
    "id": "传输任务ID",
    "name": "传输任务名称",
    "business_segment": "业务线标识",
    "principles": "负责人列表",
    "description": "传输任务描述",
    "compute_type": "计算类型：0=实时, 1=离线",
    "create_model": "创建任务模式：0=向导模式, 1=脚本模式",
    "running_model": "运行模式：0=本地模式, 1=集群模式",
    "source_type": f"来源数据源类型：{', '.join(f'{k}={v}' for k, v in DATA_SOURCE_TYPES.items())}",
    "target_type": f"目标数据源类型：{', '.join(f'{k}={v}' for k, v in DATA_SOURCE_TYPES.items())}",
    "task_text": "ChunJun任务配置JSON"
}


def get_field_comment(field_name: str, field_value: Any = None, field_type: str = "datasource") -> Optional[str]:
    """
    获取字段注释

    Args:
        field_name: 字段名
        field_value: 字段值（可选，用于动态生成更具体的注释）
        field_type: 字段类型，"datasource" 或 "transmission_task"

    Returns:
        Optional[str]: 字段注释，如果没有则返回None
    """
    # 根据字段类型选择对应的注释映射
    if field_type == "transmission_task":
        comment_map = TRANSMISSION_TASK_FIELD_COMMENTS
    else:
        comment_map = DATASOURCE_FIELD_COMMENTS

    comment = comment_map.get(field_name)

    # 对某些字段，可以根据值生成更具体的注释
    if field_name == "data_source_type" and field_value is not None:
        type_name = DATA_SOURCE_TYPES.get(field_value, "UNKNOWN")
        return f"数据源类型：{field_value} = {type_name}"

    if field_name == "data_source_version" and field_value is not None:
        version_name = DATA_SOURCE_VERSIONS.get(field_value, "UNKNOWN")
        return f"数据源版本：{field_value} = {version_name}"

    # 传输任务的特殊字段处理
    if field_type == "transmission_task":
        if field_name == "compute_type" and field_value is not None:
            compute_type_name = "实时" if field_value == 0 else "离线"
            return f"计算类型：{field_value}={compute_type_name}"

        if field_name == "create_model" and field_value is not None:
            create_model_name = "向导模式" if field_value == 0 else "脚本模式"
            return f"创建任务模式：{field_value}={create_model_name}"

        if field_name == "running_model" and field_value is not None:
            running_model_name = "本地模式" if field_value == 0 else "集群模式"
            return f"运行模式：{field_value}={running_model_name}"

        if field_name in ["source_type", "target_type"] and field_value is not None:
            type_name = DATA_SOURCE_TYPES.get(field_value, "UNKNOWN")
            field_desc = "来源数据源类型" if field_name == "source_type" else "目标数据源类型"
            return f"{field_desc}：{field_value}={type_name}"

    return comment


def get_all_field_comments(data: Dict[str, Any], field_type: str = "datasource") -> Dict[str, str]:
    """
    获取数据中所有字段的注释

    Args:
        data: 数据字典
        field_type: 字段类型，"datasource" 或 "transmission_task"

    Returns:
        Dict[str, str]: 字段名到注释的映射
    """
    comments = {}
    for field_name, field_value in data.items():
        comment = get_field_comment(field_name, field_value, field_type)
        if comment:
            comments[field_name] = comment

    return comments