"""
Business line utilities - 直接使用MCP工具返回的business_segment字段值
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


def extract_business_line(business_segment: str) -> str:
    """
    直接使用MCP工具返回的business_segment字段值作为业务线

    Args:
        business_segment: MCP工具返回的business_segment字段值

    Returns:
        str: 业务线标识
    """
    if not business_segment:
        return "unknown"

    # 清理并标准化
    cleaned = business_segment.strip().lower()

    # 将无效值统一映射为 "unknown"
    if cleaned in ['none', 'null', 'unknown', '', 'n/a', 'na']:
        return "unknown"

    # 返回原始值（保持大小写）
    return business_segment.strip()


def validate_business_line(business_line: str) -> bool:
    """
    验证业务线名称是否有效

    Args:
        business_line: 业务线标识

    Returns:
        bool: 是否有效
    """
    return bool(business_line and business_line.strip() and business_line != "unknown")


def extract_business_line_from_path(file_path: str) -> Optional[str]:
    """
    从文件路径中提取业务线信息

    Args:
        file_path: 文件路径

    Returns:
        Optional[str]: 业务线标识，如果无法识别则返回None
    """
    try:
        parts = file_path.replace("\\", "/").split("/")

        # 查找可能的业务线目录
        for part in parts:
            if validate_business_line(part) and len(part) > 1:
                return part

        return None
    except Exception as e:
        logger.warning(f"从路径提取业务线失败 {file_path}: {str(e)}")
        return None