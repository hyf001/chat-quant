"""
常量和MCP工具配置
"""
from pathlib import Path
from typing import Dict, Any


def _find_project_root() -> Path:
    """
    动态查找项目根目录（Claudable目录）

    从当前文件向上查找，直到找到包含apps/api目录结构的根目录
    """
    current = Path(__file__).resolve().parent
    while current.parent != current:  # 防止到达文件系统根目录
        # 检查是否是项目根目录的标志：
        # 1. 包含apps目录
        # 2. apps下包含api目录
        # 3. apps/api下包含app目录
        if (current / "apps").exists() and \
           (current / "apps" / "api").exists() and \
           (current / "apps" / "api" / "app").exists():
            return current
        current = current.parent

    # 如果没找到，抛出错误
    raise RuntimeError(
        "无法找到项目根目录。请确保此文件位于正确的项目结构中。"
    )


# 项目根目录
PROJECT_ROOT = _find_project_root()

# 默认输出根目录
DEFAULT_CACHE_ROOT = PROJECT_ROOT / "data" / "projects" / "cache"

# 默认配置
DEFAULT_CONFIG = {
    "cache_root": str(DEFAULT_CACHE_ROOT),
    "tenant_id": "2",
    "file_permissions": "640",
    "dir_permissions": "750",
    "max_workers": 10,
    "timeout": 300,
    "retry_times": 3,
    "log_level": "INFO"
}

# 智能体类型到数据类型的映射配置
AGENT_TYPE_CONFIG = {
    "data_develop": {
        "description": "数据开发智能体",
        "data_types": ["data_source", "transmission_task"],
        "mcp_tools": ["datasource_list", "transmission_task_list"]
    },
    "data_analysis": {
        "description": "数据分析智能体",
        "data_types": ["data_table", "bi_report"],
        "mcp_tools": []  # 不使用MCP工具，直接通过HTTPS API获取
    },
    "fin_data_analysis": {
        "description": "金融数据分析智能体",
        "data_types": ["view_table"],
        "mcp_tools": []  # 不使用MCP工具，直接通过HTTPS API获取
    },
    # 未来可以添加其他智能体类型
    # "web_app": {
    #     "description": "Web应用智能体",
    #     "data_types": ["api_endpoints", "database_schema"],
    #     "mcp_tools": ["api_list", "schema_list"]
    # }
}

# MCP工具配置
# 注：data_analysis 和 fin_data_analysis 已改用 HTTPS API，不再使用 MCP 工具
MCP_TOOLS = {
    "datasource_list": {
        "function": "datasource_list",
        "category": "data_source",
        "required_params": ["CBAS_EMAIL", "x-data-portal-tenant-id"],
        "business_line_field": "business_segment",
        "service_name": "data_transmission",
        "description": "数据传输MCP服务 - 数据源列表"
    },
    "transmission_task_list": {
        "function": "transmission_task_list",
        "category": "transmission_task",
        "required_params": ["CBAS_EMAIL", "x-data-portal-tenant-id"],
        "business_line_field": "business_segment",
        "service_name": "data_transmission",
        "description": "数据传输MCP服务 - 传输任务列表"
    }
}


def get_agent_type_config(agent_type: str) -> Dict[str, Any]:
    """
    获取智能体类型配置

    Args:
        agent_type: 智能体类型

    Returns:
        智能体类型配置字典

    Raises:
        ValueError: 当智能体类型不存在时
    """
    if agent_type not in AGENT_TYPE_CONFIG:
        raise ValueError(f"未知智能体类型: {agent_type}")
    return AGENT_TYPE_CONFIG[agent_type]


def get_mcp_tool_config(tool_name: str) -> Dict[str, Any]:
    """
    获取MCP工具配置

    Args:
        tool_name: MCP工具名称

    Returns:
        工具配置字典

    Raises:
        ValueError: 当工具名称不存在时
    """
    if tool_name not in MCP_TOOLS:
        raise ValueError(f"未找到MCP工具配置: {tool_name}")
    return MCP_TOOLS[tool_name]
