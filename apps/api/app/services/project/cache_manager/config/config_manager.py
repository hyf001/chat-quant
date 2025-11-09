"""
配置管理器 - 从 Settings 加载配置
"""
import os
import logging
from pathlib import Path
from typing import Any, Optional

from .constants import DEFAULT_CONFIG, get_mcp_tool_config

logger = logging.getLogger(__name__)


class ConfigManager:
    """配置管理器 - 从 Settings 读取配置"""

    def __init__(self):
        """
        初始化配置管理器

        注意：
        - 所有配置统一从 Settings 类获取
        - Settings 类会从环境变量加载配置
        """
        # 初始化配置
        self._config = DEFAULT_CONFIG.copy()
        self._load_settings_config()

    def _load_settings_config(self):
        """从 Settings 加载配置"""
        try:
            from app.core.config import settings

            # 从 Settings 加载所有配置
            config_mappings = {
                "default_email": settings.export_default_email,
                "tenant_id": settings.export_tenant_id,
                "max_workers": settings.export_max_workers,
                "timeout": settings.export_timeout,
                "log_level": settings.export_log_level,
                "cache_root": settings.export_cache_root,
                "mcp_data_transmission_url": settings.mcp_data_transmission_url,
                "environment": settings.environment,
                "ssl_cert_file": settings.ssl_cert_file,
                "ssl_cert_password": settings.ssl_cert_password,
                "bi_domain": settings.bi_domain,
                "bi_container_host": settings.bi_container_host,
            }

            # 更新配置
            for config_key, value in config_mappings.items():
                self._config[config_key] = value
                logger.debug(f"从 Settings 加载配置: {config_key} = {value}")

        except Exception as e:
            logger.warning(f"无法从 Settings 加载配置: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值

        Args:
            key: 配置键
            default: 默认值

        Returns:
            配置值
        """
        return self._config.get(key, default)

    def set(self, key: str, value: Any):
        """
        设置配置值

        Args:
            key: 配置键
            value: 配置值
        """
        self._config[key] = value

    def get_mcp_url(self, service_name: str) -> str:
        """
        获取MCP服务URL

        Args:
            service_name: 服务名称（如：data_transmission）

        Returns:
            MCP服务URL

        Raises:
            ValueError: 当未配置对应服务URL时
        """
        config_key = f"mcp_{service_name}_url"
        url = self._config.get(config_key)

        if not url:
            raise ValueError(
                f"未配置MCP服务URL: {service_name}, "
                f"请在.env中设置 MCP_{service_name.upper()}_URL"
            )

        return url

    def get_output_dir(self, agent_type: str) -> Path:
        """
        获取指定智能体类型的输出目录

        Args:
            agent_type: 智能体类型（如：data_analysis）

        Returns:
            输出目录路径
        """
        cache_root = Path(self.get("cache_root"))
        return cache_root / agent_type

    def validate_config(self) -> tuple[bool, str]:
        """
        验证配置有效性

        根据环境配置决定验证规则：
        - dev (开发环境): 不需要验证 email 和 tenant_id（使用SSL证书认证）
        - prod (生产环境): 必须验证 email 和 tenant_id（使用Header认证）

        Returns:
            (是否有效, 错误信息)
        """
        # 获取环境类型（从 Settings）
        environment = self.get("environment", "dev").lower()

        # 开发环境：使用SSL证书认证，不需要email和tenant_id
        if environment == 'dev':
            logger.info("开发环境模式：使用SSL证书认证，跳过email和tenant_id验证")
            return True, ""

        # 生产环境：使用Header认证，需要email和tenant_id
        required_keys = ["default_email", "tenant_id"]
        missing_keys = []

        for key in required_keys:
            if not self.get(key):
                missing_keys.append(key)

        if missing_keys:
            error_msg = (
                f"生产环境缺少必需配置: {', '.join(missing_keys)}\n"
                f"请在.env中配置: EXPORT_DEFAULT_EMAIL 和 EXPORT_TENANT_ID"
            )
            return False, error_msg

        # 验证邮箱格式
        email = self.get("default_email")
        if email and "@" not in email:
            error_msg = f"邮箱格式无效: {email}"
            return False, error_msg

        return True, ""
