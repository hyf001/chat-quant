#!/usr/bin/env python3
"""
为 AIrchieve 项目生成 pytest 测试文件骨架。

约定：
- 被测代码位于 backend/app/
- 测试文件位于 tests/（仓库根目录下）
- 测试目录与 backend/app/ 保持镜像结构
- pyproject.toml 中 pythonpath = ["backend"] 保证 from app... 导入正常
- asyncio_mode = "auto"，异步测试无需 @pytest.mark.asyncio 装饰器

示例：
    uv run python .codex/skills/python-unit-test/scripts/create_test_file.py backend/app/main.py
    uv run python .codex/skills/python-unit-test/scripts/create_test_file.py backend/app/service/book/book_service.py
"""

from __future__ import annotations

import sys
from pathlib import Path


def find_repo_root(source_path: Path) -> Path:
    """向上查找包含 backend/app/ 的仓库根目录。"""
    current = source_path.resolve().parent
    for candidate in [current, *current.parents]:
        if (candidate / "backend" / "app").is_dir():
            return candidate
    raise ValueError(f"未找到仓库根目录（缺少 backend/app/ 目录）: {source_path}")


def build_test_path(source_path: Path, repo_root: Path) -> Path:
    """将 backend/app/foo/bar.py 映射为 tests/foo/test_bar.py。"""
    try:
        relative_path = source_path.resolve().relative_to(repo_root.resolve())
    except ValueError as exc:
        raise ValueError(f"源文件不在仓库根目录下: {source_path}") from exc

    parts = relative_path.parts
    if len(parts) < 3 or parts[0] != "backend" or parts[1] != "app":
        raise ValueError("当前脚本只支持为 backend/app/ 目录下的 Python 文件生成测试")

    # backend/app/foo/bar.py → tests/foo/test_bar.py
    test_dir = repo_root / "tests" / Path(*parts[2:-1])
    return test_dir / f"test_{source_path.stem}.py"


def module_import_path(source_path: Path, repo_root: Path) -> str:
    """将文件路径转换为 Python 导入路径（从 app 开始）。

    backend/app/service/book/book_service.py → app.service.book.book_service
    """
    try:
        relative_path = source_path.resolve().relative_to(repo_root.resolve())
    except ValueError as exc:
        raise ValueError(f"源文件不在仓库根目录下: {source_path}") from exc

    parts = relative_path.with_suffix("").parts
    # 去掉 backend/ 前缀，保留 app.foo.bar
    if parts[0] == "backend":
        parts = parts[1:]
    return ".".join(parts)


def class_name_from_stem(stem: str) -> str:
    """将 snake_case 文件名转换为驼峰风格类名片段。"""
    return "".join(part.capitalize() for part in stem.split("_") if part) or "Module"


def ensure_conftest(repo_root: Path) -> Path:
    """确保 tests/conftest.py 存在。pythonpath 配置已处理导入，这里只提供 fixture 基础设施。"""
    tests_dir = repo_root / "tests"
    tests_dir.mkdir(parents=True, exist_ok=True)

    conftest_path = tests_dir / "conftest.py"
    if not conftest_path.exists():
        conftest_path.write_text(
            """import os

import pytest
from fastapi.testclient import TestClient

from app.main import app

os.environ.setdefault("DEBUG", "false")


@pytest.fixture
def client():
    return TestClient(app)
""",
            encoding="utf-8",
        )

    return conftest_path


def build_template(source_path: Path, import_path: str) -> str:
    """根据模块位置生成更贴近项目的测试模板。"""
    stem = source_path.stem

    if source_path.name == "main.py":
        return f'''"""
{stem} 的测试
"""

from fastapi.testclient import TestClient

from {import_path} import app


client = TestClient(app)


def test_health_check_returns_ok_status():
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "service" in data
'''

    if "api" in source_path.parts:
        return f'''"""
{stem} 的接口测试
"""

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_{stem}_placeholder():
    """根据实际路由补充接口测试。"""
    # TODO: 调用对应接口并断言状态码、响应体和错误分支
    assert client is not None
'''

    if "service" in source_path.parts:
        return f'''"""
{stem} 的单元测试
"""

# TODO: 按需导入被测对象
# from {import_path} import YourService


class Test{class_name_from_stem(stem)}:
    async def test_placeholder(self):
        """根据真实业务补充异步测试（asyncio_mode=auto 无需装饰器）。"""
        # TODO: mock 外部依赖后补充断言
        assert True
'''

    return f'''"""
{stem} 的单元测试
"""

# TODO: 按需导入被测对象
# from {import_path} import your_function, YourClass


class Test{class_name_from_stem(stem)}:
    def test_placeholder(self):
        """根据真实业务补充测试。"""
        assert True
'''


def create_test_file(source_file: str) -> dict[str, str | bool]:
    """创建测试文件并返回结果。"""
    source_path = Path(source_file).resolve()

    if not source_path.exists():
        return {"success": False, "message": f"源文件不存在: {source_file}"}
    if source_path.suffix != ".py":
        return {"success": False, "message": f"源文件不是 Python 文件: {source_file}"}

    try:
        repo_root = find_repo_root(source_path)
        test_file_path = build_test_path(source_path, repo_root)
        import_path = module_import_path(source_path, repo_root)
    except ValueError as exc:
        return {"success": False, "message": str(exc)}

    if test_file_path.exists():
        return {
            "success": False,
            "message": f"测试文件已存在: {test_file_path}",
            "test_file_path": str(test_file_path),
        }

    conftest_path = ensure_conftest(repo_root)
    test_file_path.parent.mkdir(parents=True, exist_ok=True)
    test_file_path.write_text(build_template(source_path, import_path), encoding="utf-8")

    return {
        "success": True,
        "message": f"测试文件已创建: {test_file_path}",
        "test_file_path": str(test_file_path),
        "import_path": import_path,
        "conftest_path": str(conftest_path),
    }


def main() -> None:
    if len(sys.argv) != 2:
        print("用法: uv run python create_test_file.py <backend/app 下的源文件路径>")
        print("示例: uv run python create_test_file.py backend/app/service/book/book_service.py")
        sys.exit(1)

    result = create_test_file(sys.argv[1])

    if not result["success"]:
        print(f"✗ {result['message']}")
        sys.exit(1)

    print(f"✓ {result['message']}")
    print(f"  导入路径: {result['import_path']}")
    print(f"  测试配置: {result['conftest_path']}")
    print(f"  下一步: 编辑 {result['test_file_path']} 并运行 uv run pytest")


if __name__ == "__main__":
    main()
