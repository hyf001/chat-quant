"""
静态资源服务模块

提供静态文件服务功能，支持浏览器访问静态页面和资源
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
import mimetypes
import os

from app.core.config import settings

router = APIRouter()


def get_content_type(file_path: Path) -> str:
    """
    根据文件扩展名获取 Content-Type

    Args:
        file_path: 文件路径

    Returns:
        MIME 类型字符串
    """
    content_type, _ = mimetypes.guess_type(str(file_path))
    return content_type or "application/octet-stream"


@router.get("/{file_path:path}")
async def serve_static_file(file_path: str):
    """
    提供静态文件服务

    Args:
        file_path: 相对于静态资源目录的文件路径

    Returns:
        文件响应

    Raises:
        HTTPException: 文件不存在或访问错误时抛出
    """
    # 构建完整文件路径
    full_path = Path(os.path.join(settings.projects_root,file_path))
    

    # 检查文件是否存在
    if not full_path.exists():
        raise HTTPException(status_code=404, detail=f"文件不存在: {file_path}")

    # 检查是否为文件（不允许访问目录）
    if not full_path.is_file():
        raise HTTPException(status_code=400, detail="请求的路径不是文件")

    # 返回文件
    content_type = get_content_type(full_path)
    return FileResponse(
        path=full_path,
        media_type=content_type,
        filename=full_path.name,
        content_disposition_type="inline"
    )
