from pydantic import BaseModel
import os
from pathlib import Path
from dotenv import load_dotenv

def find_project_root() -> Path:
    """
    Find the project root directory by looking for specific marker files.
    This ensures consistent behavior regardless of where the API is executed from.
    """
    current_path = Path(__file__).resolve()
    
    # Start from current file and go up
    for parent in [current_path] + list(current_path.parents):
        # Check if this directory has both apps/ and Makefile (project root indicators)
        if (parent / 'apps').is_dir() and (parent / 'Makefile').exists():
            return parent
    
    # Fallback: navigate up from apps/api to project root
    # Current path is likely: /project-root/apps/api/app/core/config.py
    # So we need to go up 4 levels: config.py -> core -> app -> api -> apps -> project-root
    api_dir = current_path.parent.parent.parent  # /project-root/apps/api
    if api_dir.name == 'api' and api_dir.parent.name == 'apps':
        return api_dir.parent.parent  # /project-root
    
    # Last resort: current working directory
    return Path.cwd()


# Get project root once at module load
PROJECT_ROOT = find_project_root()
load_dotenv(os.path.join(PROJECT_ROOT,".env"))


class Settings(BaseModel):
    api_port: int = int(os.getenv("API_PORT", "8080"))

    # SQLite database URL
    database_url: str = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{PROJECT_ROOT / 'data' / 'cc.db'}",
    )

    # Use project root relative paths
    projects_root: str = os.getenv("PROJECTS_ROOT", str(PROJECT_ROOT / "data" / "projects"))
    projects_root_host: str = os.getenv("PROJECTS_ROOT_HOST", os.getenv("PROJECTS_ROOT", str(PROJECT_ROOT / "data" / "projects")))

    # Export cache root for analysis project initialization data (derived from projects_root)
    # Data is exported from various sources (MCP services, HTTPS APIs, etc.)
    @property
    def export_cache_root(self) -> str:
        """导出缓存根目录，固定为 projects_root/cache"""
        return str(Path(self.projects_root) / "cache")

    preview_port_start: int = int(os.getenv("PREVIEW_PORT_START", "3100"))
    preview_port_end: int = int(os.getenv("PREVIEW_PORT_END", "3999"))
    getway_url: str = os.getenv("GETWAY_URL","http://localhost:8080")
	
	# 环境配置 (prod: 生产环境, dev/空: 开发环境)
    environment: str = os.getenv("THS_TIER", "dev")

    ssl_cert_file: str = os.getenv("SSL_CERT_FILE", "")
    ssl_cert_password: str = os.getenv("SSL_CERT_PASSWORD", "")

    # 智能BI域名配置 (开发环境使用HTTPS双向认证)
    bi_domain: str = os.getenv("BI_DOMAIN", "https://phonestat.hexin.cn/sdmp/easyfetch")

    # 智能BI容器服务配置 (生产环境使用HTTP)
    bi_container_host: str = os.getenv("BI_CONTAINER_HOST", "http://easyfetch:9596/easyfetch")

    # 金融查数接口配置
    fin_sql_domain: str = os.getenv("FIN_SQL_DOMAIN", "https://indexmap.myhexin.com")
    fin_sql_container_host: str = os.getenv("FIN_SQL_CONTAINER_HOST", "http://cbas-babel-frontend-prod:10399")

    # 数据导出配置
    export_default_email: str = os.getenv("EXPORT_DEFAULT_EMAIL", "")
    export_tenant_id: str = os.getenv("EXPORT_TENANT_ID", "2")
    export_max_workers: int = int(os.getenv("EXPORT_MAX_WORKERS", "10"))
    export_timeout: int = int(os.getenv("EXPORT_TIMEOUT", "300"))
    export_log_level: str = os.getenv("EXPORT_LOG_LEVEL", "INFO")

    # MCP服务URL（仅用于数据传输服务）
    mcp_data_transmission_url: str = os.getenv("MCP_DATA_TRANSMISSION_URL", "")

    claudable_project_root: str = str(PROJECT_ROOT)



settings = Settings()