---
name: python-unit-test
description: 专门用于 Python 单元测试工作的技能。仅当用户明确要求编写、生成、运行、改进或调试 Python 单元测试时使用此技能。适用于当前��库的 FastAPI 后端，优先面向 `backend/app/` 目录下的模块、接口、服务层与数据层测试。不用于一般功能开发、随手排查或非测试任务。
---

# Python 单元测试指南

面向 AIrchieve 后端结构工作：

- 被测代码在 `backend/app/`
- 测试文件放在 `tests/`（仓库根目录下）
- Python 命令通过 `uv run` 执行（由 `uv` 管理仓库根目录下的 `.venv`）
- `pyproject.toml` 中 `pythonpath = ["backend"]` 确保 `from app...` 导入正常工作
- `asyncio_mode = "auto"` — 异步测试无需手动加 `@pytest.mark.asyncio`
- 接口入口是 `app.main:app`（通过 `create_app()` 工厂函数创建）
- 依赖通过 `pyproject.toml` 的 `[project.optional-dependencies] dev` 管理

## 什么时候使用

仅在用户明确表达测试意图时触发，例如：

- "给这个模块写单元测试"
- "运行 pytest"
- "补测试覆盖率"
- "调试测试失败"

不要在普通功能开发或代码评审时自动切到这个技能。

## 工作流程

1. 先读被测代码，再决定测试范围。
2. 判断测试类型：
   - 纯函数或工具函数：优先写真正的单元测试
   - `service/`：优先 mock 外部依赖、数据库、HTTP 调用
   - `api/v1/`：优先写接口测试，使用 FastAPI 测试客户端覆盖状态码、响应体、鉴权和错误分支
3. 如需新建测试文件，先运行：

```bash
uv run python .codex/skills/python-unit-test/scripts/create_test_file.py backend/app/service/book/book_service.py
```

4. 再补充真实测试用例，不要保留空洞模板。
5. 运行最小必要范围的测试：

```bash
uv run pytest tests/service/book/test_book_service.py -v
```

6. 如果失败，先判断是测试设计问题还是源代码 bug。不要为了"让测试通过"去掩盖真实缺陷。

## AIrchieve 项目约定

### 项目结构

```
（仓库根目录）
├── pyproject.toml          # 依赖 + pytest 配置
├── .venv/                  # Python 虚拟环境
├── backend/
│   ├── app/
│   │   ├── main.py         # FastAPI 应用工厂
│   │   ├── core/           # 配置、工具函数
│   │   ├── db/             # 数据库引擎、会话
│   │   ├── model/          # SQLAlchemy 模型（按领域分子目录）
│   │   ├── schema/         # Pydantic schema（按领域分子目录）
│   │   ├── service/        # 业务逻辑（按领域分子目录）
│   │   └── api/v1/         # FastAPI 路由（扁平文件）
│   └── alembic/            # 数据库迁移
└── tests/                  # 测试目录（与 backend/app/ 镜像）
```

### 测试目录映射

测试目录结构与源码路径保持对应（去掉 `backend/` 前缀，`app/` 替换为 `tests/`）：

| 源文件 | 测试文件 |
|---|---|
| `backend/app/main.py` | `tests/test_main.py` |
| `backend/app/api/v1/book_api.py` | `tests/api/v1/test_book_api.py` |
| `backend/app/service/account/auth_service.py` | `tests/service/account/test_auth_service.py` |
| `backend/app/model/book/book.py` | `tests/model/book/test_book.py` |
| `backend/app/core/utils/sms.py` | `tests/core/utils/test_sms.py` |

### 推荐的导入方式

`pythonpath = ["backend"]` 确保 `from app...` 在测试中直接可用：

```python
from app.main import app
from app.service.book.book_service import BookService
from app.model.book import Book
from app.schema.account.account import UserCreate
```

### 包导入约定

不需要 `conftest.py` 手动注入 `sys.path`——`pyproject.toml` 的 `pythonpath` 配置已处理。
`tests/conftest.py` 仅用于定义共享 fixture（如数据库会话、测试客户端等）。

脚本首次创建测试文件时，应同时确保 `tests/conftest.py` 存在。

### pytest 配置要点

```toml
[tool.pytest.ini_options]
addopts = "-q"
asyncio_mode = "auto"
pythonpath = ["backend"]
testpaths = ["tests"]
```

- `asyncio_mode = "auto"` — 异步测试函数自动识别，无需 `@pytest.mark.asyncio`
- `pythonpath = ["backend"]` — 测试中 `from app...` 直接可用
- `testpaths = ["tests"]` — 测试发现范围

### 接口测试建议

- 优先覆盖 `/health` 这类稳定接口的模式，再迁移到业务接口
- 对 API 路由，重点验证：
  - 状态码
  - 响应 JSON 结构
  - 参数校验失败
  - 认证/权限分支
  - 服务层抛错后的返回

常见模式：

```python
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "service" in data
```

如果接口依赖异步服务、数据库或外部 HTTP，请优先 patch 服务层边界，而不是直接打真实依赖。

### 服务层测试建议

- 对数据库访问使用 mock / stub，避免碰真实库
- 对 `httpx.AsyncClient`、第三方 SDK、OSS、支付、LLM 调用全部 mock
- 优先验证：
  - 输入到输出的业务转换
  - 分支逻辑
  - 异常传播或错误包装

异步函数测试示例（`asyncio_mode = "auto"` 无需装饰器）：

```python
async def test_async_behavior():
    result = await some_async_function()
    assert result == "expected"
```

### 模型层测试建议

- 重点验证字段约束、默认值、枚举类型
- 可用 SQLAlchemy 内存 SQLite 进行轻量级模型验证
- 枚举类测试确认值覆盖完整

## 编写要求

- 每个测试只验证一个明确行为
- 命名直接表达意图，例如 `test_health_check_returns_ok_status`
- 优先小范围、低耦合、可重复执行的测试
- 测试行为，不测试实现细节
- 能 mock 的外部依赖尽量 mock

## 失败处理原则

- 如果测试合理而结果失败，优先报告源码问题
- 只有确认测试设计错误时才修改测试
- 不要通过降低断言强度、移除关键分支或迎合当前错误行为来"修绿"

## 执行命令

```bash
# 运行全部测试
uv run pytest

# 运行单个测试文件
uv run pytest tests/service/book/test_book_service.py -v

# 运行单个测试
uv run pytest tests/api/v1/test_book_api.py::test_health_check -v

# 查看更详细失败信息
uv run pytest tests/path/to/test_module.py -vv

# 运行并显示覆盖率
uv run pytest --cov=app tests/
```

如果 `.venv` 里还没有测试依赖，运行：

```bash
uv sync --extra dev
```

不要让脚本自动改动 `pyproject.toml`，也不要混用系统 Python 或手动 pip 安装。
