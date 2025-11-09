"""
Base Exporter - 导出器基类
"""
import logging
from abc import ABC, abstractmethod
from typing import Optional, List
from pathlib import Path

from ..config.config_manager import ConfigManager

logger = logging.getLogger(__name__)


class BaseExporter(ABC):
    """导出器基类"""

    def __init__(self, config: ConfigManager, agent_type: str):
        """
        初始化导出器

        Args:
            config: 配置管理器
            agent_type: 智能体类型（如：data_analysis）
        """
        self.config = config
        self.agent_type = agent_type
        self.output_dir = config.get_output_dir(agent_type)

        # 确保输出目录存在
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    async def export(self,
                    business_lines: Optional[List[str]] = None,
                    dry_run: bool = False,
                    verbose: bool = False) -> bool:
        """
        执行导出

        Args:
            business_lines: 业务线过滤
            dry_run: 是否为预览模式
            verbose: 是否详细输出

        Returns:
            是否成功
        """
        pass

    def get_category_dir(self, business_line: str, category: str) -> Path:
        """
        获取分类目录路径

        Args:
            business_line: 业务线
            category: 数据类型

        Returns:
            目录路径
        """
        return self.output_dir / business_line / category
