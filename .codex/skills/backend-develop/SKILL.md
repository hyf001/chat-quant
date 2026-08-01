---
name: backend-develop
description: Chat-Quant 项目后端开发技能。当处理 apps/api 下的 Python 后端代码时使用此技能，包括 FastAPI API、MVC 风格目录、SQLAlchemy 数据库 model、Pydantic schema、service 业务逻辑、数据库会话依赖、配置、测试和后端规范整理。
---

# Backend Develop

本技能用于 Chat-Quant 后端开发。后端采用轻量 MVC 风格组织代码，避免 DDD/Clean Architecture 目录和 repository 抽象过度拆分。开发时优先参考当前 `apps/api/app` 的实际结构，以及用户指定的 AIrchieve 后端案例目录：`/Users/huyufei/Documents/hyf/code/github/AIrchieve/backend/app`。

## 核心结构

后端包位于 `apps/api/app/`：

```text
apps/api/
  app/
    main.py                    # FastAPI app 创建入口
    api/
      v1/                      # API route，按能力拆分为 *_api.py
        router.py              # v1 路由聚合
        dependencies.py        # 仅放请求上下文/header/db 等轻量依赖
    model/                     # SQLAlchemy ORM 数据库 model
      {module}/
        {module}.py
    schema/                    # Pydantic 请求/响应/契约 schema
      {module}/
        {module}.py
    service/                   # 业务逻辑和数据库查询/写入
      {module}/
        service.py
    db/                        # 数据库 session、schema 初始化、通用 DB payload
    core/                      # 配置、日志、通用工具
    agent_runtime/             # Agent/SDK runtime 适配
    cli/                       # CLI 入口
  tests/
```

## 硬约束

- 不新增或恢复 `domain/`、`infrastructure/`、`application/`、`views/`、`controllers/`。
- 不使用重复目录名：不要有 `model/models`、`model/modes`、`service/services`、`schema/schemas`。
- 不新增 `repository` 或 `repositories` 模块；旧 repository 逻辑要合并进对应 `service`。
- `model` 只放真正的数据库 ORM model，也就是 SQLAlchemy row/table 类。不要把领域 dataclass、DTO 或 Pydantic schema 放进 `model`。
- `schema` 只放 Pydantic 请求、响应和稳定 JSON 契约。
- `service` 承载业务逻辑，也可以直接写 SQLAlchemy 查询、持久化和事务提交。
- API route 只能依赖请求上下文和数据库会话，例如 `db: AsyncSession = Depends(get_db)`；不要 `Depends` service provider。
- route 内可以用 `service.some_function(db, ...)` 或 `SomeService(db)` 调用业务逻辑，但不要把复杂业务流程写在 route 中。
- 不从 service 再依赖 FastAPI 的 `Depends`；service 接收普通参数和 `AsyncSession`。

## API 层

- 路由文件放在 `app/api/v1/*_api.py`，统一注册到 `app/api/v1/router.py`。
- 路由变量命名为 `router`。
- route 负责 HTTP 方法、路径、状态码、response model、请求参数、header 上下文和错误映射。
- route 通过 `get_db` 注入数据库会话，并把 `db` 传给 service。
- route 不直接操作 ORM row，不直接写复杂查询，不直接提交事务。
- 资源归属、权限校验、状态流转等业务判断优先放在 service。

示例模式：

```python
@router.post("/projects", response_model=ProjectRead)
async def create_project(
    request: ProjectCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    user_id: UserId,
) -> ProjectRead:
    try:
        created = await project.create_project(db, user_id=user_id, name=request.name)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from None
    return ProjectRead.model_validate(created)
```

## Service 层

- 每个业务模块优先提供 `service.py`，必要时提供同目录下的 `types.py` 或专项实现文件。
- service 函数或 service 类接收 `AsyncSession`，内部完成查询、校验、状态更新和提交。
- 查询和写入可以直接使用 SQLAlchemy `select`、`delete`、`db.get`、`db.add`、`db.commit`。
- 对外部 SDK、文件系统、运行时等调用放在 service 或明确的 runtime 适配模块中，调用路径和配置来自 `core/config.py`。
- 业务错误使用明确异常类，例如 `ProjectNotFoundError`、`ChatSessionAccessError`，由 API 映射成 HTTP 错误。
- 列表查询必须支持分页、排序和过滤，不返回无上限全量数据。

## Model 层

- ORM model 放在 `app/model/{module}/{module}.py`。
- `app/db/schema.py` 必须显式 import 这些 ORM model，确保 metadata 建表能发现表定义。
- ORM 类命名优先使用 `XxxRow`，避免和 Pydantic schema 或 service 内部类型混淆。
- 数据库字段默认值、nullable、索引、唯一约束要与 API 契约和业务规则一致。

## Schema 层

- Pydantic schema 放在 `app/schema/{module}/{module}.py`。
- 请求 schema 使用 `XxxRequest`、`XxxCreate`、`XxxUpdate`。
- 响应 schema 使用 `XxxResponse`、`XxxRead`、`XxxSummary`、`XxxDetail`。
- 输出 schema 如需从对象转换，使用 Pydantic v2 的 `ConfigDict(from_attributes=True)` 或显式转换。
- 稳定契约避免裸 `Any`、万能 `dict`；确实需要 JSON payload 时使用项目已有 JSON 类型或明确 schema。

## 数据库与依赖

- 数据库 session 统一来自 `app/db/session.py` 的 `get_db`。
- 需要手动创建 session 时使用 `get_session_factory()()` 或 `make_session_factory(make_engine(settings))`。
- API 依赖只保留轻量上下文：数据库会话、用户 ID、项目 ID、header/query/path 参数。
- 不创建 service dependency provider，例如 `get_xxx_service`、`ServicesDep`、`M1Services`。
- 配置统一来自 `app/core/config.py` 的 `get_settings()` 或注入的 `Settings`，不要散落读取环境变量。

## 命名与整理

- 目录用单数：`model`、`schema`、`service`。
- API 文件使用 `*_api.py`，service 主文件使用 `service.py`。
- 不引入新框架、ORM、配置系统或任务系统，除非用户明确要求。
- 清理历史架构时，删除无引用旧目录和旧 import，不保留兼容空壳。
- 改动已迁移文件时，不恢复旧 DDD 分层、repository 抽象或 service dependency provider。

## 测试与验证

常用命令从仓库根目录执行：

```bash
uv sync --extra dev
uv run uvicorn app.main:app --reload --app-dir apps/api
uv run pytest apps/api/tests
uv run ruff check apps/api
```

针对后端改动，优先验证：

- API 成功路径和错误映射。
- 权限、用户/项目归属、资源不存在。
- service 内数据库读写、事务提交、分页过滤。
- Pydantic schema 请求/响应兼容性。
- 外部 SDK、文件系统或 runtime 替身在测试中可控。

## 交付说明

完成后端开发后，最终回复说明：

- 改动了哪些 API、model、schema、service、db 模块。
- 是否新增或修改 API 契约、数据库结构、配置或外部适配。
- 是否移除了旧 DDD/repository/service dependency 残留。
- 运行了哪些测试和 lint，或为什么无法运行。
- 是否存在迁移、兼容或数据风险。
