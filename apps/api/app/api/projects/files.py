"""
Project Files API
Handles file listing and search for @ mention autocomplete
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
import os
from pathlib import Path

from app.api.deps import get_db
from app.models.projects import Project
from app.core.config import settings
from app.core.terminal_ui import ui


router = APIRouter()


class FileItem(BaseModel):
    path: str  # 相对路径
    type: str  # 'file' or 'dir'
    size: Optional[int] = None
    name: str  # 文件名


class FileSearchResponse(BaseModel):
    files: List[FileItem]
    total: int


@router.get("/{project_id}/files/search", response_model=FileSearchResponse)
async def search_project_files(
    project_id: str,
    q: str = Query("", description="搜索查询词"),
    limit: int = Query(50, ge=1, le=100, description="返回结果数量限制"),
    db: Session = Depends(get_db)
):
    """
    搜索项目文件和目录（用于 @ 自动补全）

    参数:
        project_id: 项目 ID
        q: 搜索查询词（模糊匹配）
        limit: 返回结果数量限制

    返回:
        FileSearchResponse: 包含匹配文件列表
    """
    # 验证项目存在
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # 获取项目路径
    project_path = os.path.join(settings.projects_root, project_id)

    # 搜索文件
    try:
        files = search_files(project_path, q, limit)
        return FileSearchResponse(
            files=files,
            total=len(files)
        )
    except Exception as e:
        ui.error(f"File search error: {e}", "File Search")
        raise HTTPException(status_code=500, detail=str(e))


def search_files(project_path: str, query: str, limit: int) -> List[FileItem]:
    """
    在项目目录中搜索文件

    参数:
        project_path: 项目根目录
        query: 搜索查询词
        limit: 返回结果数量限制

    返回:
        List[FileItem]: 匹配的文件列表
    """
    # 忽略的目录
    IGNORED_DIRS = {
        '.git', '.next', 'node_modules', '__pycache__',
        '.venv', 'venv', 'dist', 'build', '.cache',
        '.DS_Store', '.vscode', '.idea', 'coverage',
        '.pytest_cache', '.mypy_cache', 'out', 'target'
    }

    # 忽略的文件扩展名
    IGNORED_EXTENSIONS = {
        '.pyc', '.pyo', '.swp', '.swo', '.log',
        '.lock', '.tmp', '.temp', '.bak', '.map'
    }

    results = []
    query_lower = query.lower()

    # 遍历项目目录
    for root, dirs, files in os.walk(project_path):
        # 过滤忽略的目录（就地修改 dirs 列表）
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS and not d.startswith('.')]

        # 计算相对路径
        rel_root = os.path.relpath(root, project_path)
        if rel_root == '.':
            rel_root = ''

        # 搜索目录
        for dir_name in dirs:
            rel_dir_path = os.path.join(rel_root, dir_name) if rel_root else dir_name

            # 模糊匹配
            if not query or query_lower in rel_dir_path.lower() or query_lower in dir_name.lower():
                results.append(FileItem(
                    path=rel_dir_path,
                    type='dir',
                    name=dir_name
                ))

        # 搜索文件
        for file_name in files:
            # 跳过忽略的扩展名
            if any(file_name.endswith(ext) for ext in IGNORED_EXTENSIONS):
                continue

            rel_file_path = os.path.join(rel_root, file_name) if rel_root else file_name

            # 模糊匹配（匹配完整路径或文件名）
            if not query or query_lower in rel_file_path.lower() or query_lower in file_name.lower():
                file_full_path = os.path.join(root, file_name)
                try:
                    file_size = os.path.getsize(file_full_path)
                except:
                    file_size = None

                results.append(FileItem(
                    path=rel_file_path,
                    type='file',
                    size=file_size,
                    name=file_name
                ))

        # 如果结果已经足够，提前退出
        if len(results) >= limit * 2:  # 收集更多结果以便后续排序
            break

    # 排序：目录优先，然后按路径长度（更短的更相关）
    results.sort(key=lambda x: (
        0 if x.type == 'dir' else 1,  # 目录优先
        len(x.path),  # 路径长度
        x.path.lower()  # 字母顺序
    ))

    # 限制返回数量
    return results[:limit]
