---
name: backend-develop
description: AIrchieve 项目后端开发技能。当处理后端代码（backend/app/ 目录）时使用此技能，包括创建 API、服务、模型、数据库操作、Alembic 迁移、FastAPI 开发和后端规范审查。
---

# AIrchieve Backend Develop

本技能用于 AIrchieve 后端开发。目标是让不同开发者进入项目后能快速理解目录结构、运行方式、模块边界和强制规范，避免多人并行时出现重复实现、跨层直连和业务规则漂移。

## 快速判断

当任务涉及以下内容时，必须使用本技能：

- 修改 `backend/app/` 下任何 Python 后端代码。
- 新增或修改 FastAPI API、service、schema、model。
- 新增数据库表、字段、索引或 Alembic 迁移。
- 修改后端配置、数据库 session、鉴权、支付、权益、生成任务、存储、隐私授权等公共能力。
- 设计或审查后端模块边界、接口契约和数据流。

不适用范围：

- 前端 `frontend/` 开发使用 `frontend-develop`。
- 明确要求写 Python 单元测试时，同时使用 `python-unit-test`。
- 仅做代码审查时，同时参考 `code-review`。

## 项目结构

当前后端包位于 `backend/app/`，使用根目录 `pyproject.toml` 管理依赖。

```text
backend/
  app/
    main.py                 # FastAPI app 创建和路由注册入口
    api/v1/                 # API 路由层（按模块 {module}_api.py）
    core/                   # 配置、安全、日志、基础设施
    db/                     # 数据库 engine/session/base
    model/{module}/         # ORM 模型层（按模块子目录组织）
    schema/{module}/        # Pydantic 请求/响应/DTO（按模块子目录组织）
    service/{module}/       # 业务逻辑层（按模块子目录组织）
  alembic/
    env.py                  # Alembic 异步迁移配置
    versions/               # 数据库迁移文件
tests/
  api/                      # 后端 API 测试
```

当前技术栈：

- Python `>=3.12`
- FastAPI
- Pydantic v2 / `pydantic-settings`
- SQLAlchemy 2.x async
- Alembic
- 默认数据库：`sqlite+aiosqlite:///data/app.db`
- 测试：pytest / pytest-asyncio / httpx

## 开发环境

常用命令从仓库根目录执行。

安装依赖：

```bash
uv sync --extra dev
```

启动后端：

```bash
uv run uvicorn app.main:app --reload --app-dir backend
```


运行测试：

```bash
uv run pytest
```

运行 Alembic 迁移：

```bash
uv run alembic upgrade head
```

生成迁移：

```bash
uv run alembic revision --autogenerate -m "describe_change"
```

迁移文件组织：

- Alembic 迁移按表归档维护；同一张表只保留一个迁移文件，新增字段、索引、约束或 seed 数据都应合并到该表对应的迁移文件里。
- 不要为同一张表反复新增零散迁移文件，例如 `taxonomy_items` 的结构和 seed 更新都应维护在 taxonomy 对应迁移中。
- 只有当一次变更同时跨多张表且无法清晰归属时，才创建新的跨表迁移，并在文件名和最终说明中写明原因。

配置说明：

- 配置统一从 `backend/app/core/config.py` 的 `Settings` 读取。
- `.env` 默认从仓库根目录读取。
- 不要在业务代码里散落读取环境变量。
- 数据库连接统一使用 `backend/app/db/session.py` 里的 `get_db` / `async_session_maker`。

## 分层职责

### API 层：`backend/app/api/v1/`

职责：

- 定义路由、HTTP 方法、路径、状态码和 response model。
- 接收和校验请求参数。
- 注入数据库 session、当前用户等依赖。
- 调用 service 并返回 schema。

强制规则：

- API 层不得写复杂业务逻辑。
- API 层不得直接修改 ORM 对象状态。
- API 层不得直接调用外部 AI、OSS、支付渠道等基础设施。
- API 层不得堆大量 Pydantic model；稳定业务 schema 必须放到 `backend/app/schema/`。

### Service 层：`backend/app/service/`

职责：

- 承载业务规则、状态流转和跨模块编排。
- 统一处理事务、额度、权限、任务、存储、生成等流程。
- 对外暴露模块公开方法，作为模块边界。

强制规则：

- 跨模块写操作必须调用目标模块 service，不得直接 import 对方 model 后修改。
- 一个 service 只拥有本模块的数据写逻辑。
- 业务模块不得自行判断 VIP、额度、次数上限，必须调用 `entitlement_service`。
- 非阻塞副作用优先发布领域事件，不要在核心写流程里同步堆统计、审计、通知等逻辑。

### Schema 层：`backend/app/schema/`

职责：

- 定义请求、响应、跨模块 DTO 和稳定内容结构。
- 使用 Pydantic v2。
- 输出 schema 使用 `ConfigDict(from_attributes=True)` 支持 ORM 转换。

强制规则：

- 稳定业务结构禁止使用裸 `dict`、`dict[str, Any]`、`Any` 或万能 payload；必须定义明确的 Pydantic schema、DTO、TypedDict 或专用值对象。
- 请求、响应、内部 DTO 要分开命名，不要复用一个万能 schema。
- 跨模块调用尽量传递 id、`SummaryDTO` 或 `InternalDTO`，不得暴露 SQLAlchemy model。
- 适合枚举的状态值、类型字段、来源字段、动作字段等必须定义 `Enum` / `StrEnum` 或项目既有枚举类型，禁止散落字符串常量。

### Model 层：`backend/app/model/`

职责：

- 定义 SQLAlchemy ORM 模型、表名、字段、索引、关系。
- 所有 model 必须继承 `Base`，需要时间戳时复用 `TimestampMixin`。

强制规则：

- 新增 model 后必须在 `backend/app/model/__init__.py` 导出，保证 Alembic metadata 能发现。
- 任何数据库结构变化必须配套 Alembic migration。
- 所有 ORM model 的主键 `id` 以及指向内部 model 的外键 id 必须使用 `int` / SQLAlchemy `Integer` 自增主键，禁止使用 UUID 或 `String(36)` 作为内部模型 id；外部平台单号、业务编码、素材引用等非内部模型 id 可继续使用字符串字段。
- 不要在 model 里写业务流程。
- 删除类能力优先使用软删除或状态字段；涉及用户内容、支付、审计、导出、分享记录时不要物理删除历史事实。

### Core / DB 层

职责：

- `core/` 放配置、安全、日志和基础设施封装。
- `db/` 放 engine、session、Base 和迁移基座。

强制规则：

- 不要在业务代码里自行创建 engine/session。
- 不要在业务代码里散落读取环境变量。
- 日志应使用项目统一 logger，不要直接 `print`。

## 推荐模块边界

业务模块以 `docs/wiki/raw/articles/module-design.md` 为准。开发前必须先确认自己负责的模块边界。

当前推荐模块包括：

- `account`：用户、角色、登录态、儿童档案。
- `membership / entitlement`：会员计划、订阅状态、权益校验和额度。
- `payment`：订单、支付回调、退款、订阅账单。
- `taxonomy`：年龄段、主题、教育目标、语言、阅读水平、叙事风格等配置。
- `story`：纯文本故事资产。
- `book`：绘本内容资产、页面、媒体、共读提示、学习卡片、播放器内容组装。
- `reading`：收藏、阅读进度、继续阅读、阅读历史。
- `template`：基于现有绘本的角色标注和复用。
- `asset / storage`：形象、画风、声音、文件存储。
- `creation`：基于故事生成绘本的创作流程。
- `generation_task`：AI/导出等异步任务状态、进度、失败、重试。
- `share`：分享链接和分享访问。
- `export`：PDF 导出任务、导出文件、导出状态。
- `recommendation`：推荐位、专题、运营配置。
- `analytics`：事件记录、统计聚合、运营数据。
- `privacy`：上传授权、个人素材隐私、分享/导出隐私确认。
- `domain_event`：领域事件发布、投递、消费、失败重试。
- `admin`：后台入口和运营动作编排。
- `moderation / audit`：审核、举报、后台写操作审计。

核心边界：

- `story` 是纯文本资产，不包含页面、图片、音频、播放结构。
- `book` 是可播放内容资产，不负责收藏/进度；收藏和进度归 `reading`。
- `book_player_service` 是 `book` 内部文件，不是独立业务模块。
- `template` 只标注和复用现有绘本，不重新创作绘本结构。
- `asset` 管业务素材，`storage` 只管文件存取。
- `generation_task` 只管任务生命周期和结果引用，不决定结果归属。
- `admin` 只编排后台操作，不拥有核心业务规则。

## 强制开发规则

以下规则必须遵守，除非用户明确要求破例，并且在最终说明中解释原因。

1. 新增 API 必须走 `api -> service -> model` 分层，不允许 API 直写数据库业务状态。
2. 新增业务能力必须先判断归属模块；不能确定时先看 `docs/wiki/raw/articles/module-design.md`。
3. 跨模块写操作只能调用目标模块 service，禁止直接 import 对方 ORM model 修改。
4. 权限、会员、额度、VIP 判断必须集中在 `entitlement_service`，业务模块不得自行散写判断。
5. 配置读取只能走 `core/config.py`，禁止业务代码直接读环境变量。
6. 数据库 session 只能走 `get_db` 或 `async_session_maker`，禁止自行创建 engine。
7. 数据库结构变化必须新增 Alembic migration，并确保 model 在 `model/__init__.py` 导出。
8. 稳定请求/响应/DTO 必须放 `schema/`，禁止使用 `Any`、裸 `dict`、`dict[str, Any]` 或万能 payload；必须用明确对象规范表达数据契约。
9. 跨模块引用使用 `target_type + target_id`、id 或明确 DTO，禁止保存对方内部模型。
10. 非阻塞副作用优先走 `domain_event_service`，例如统计、运营分析、审计辅助事件。
11. 强一致行为必须同步调用 service，例如权限校验、额度预占、隐私确认、支付回调、发布/下架。
12. 用户上传、个人声音、个人形象、分享、导出相关流程必须考虑 `privacy_service`。
13. 支付订单、审计日志、导出记录、分享记录、审核记录等历史事实不得随意物理删除。
14. 后台接口可以单独写 API，但底层必须调用业务模块公开 service，并记录 audit。
15. 不要引入新的框架、ORM、配置系统、任务系统，除非先确认现有能力无法满足。
16. 不要把同一业务规则同时写在前台 API 和后台 API；规则必须沉到同一个 service。
17. 函数返回值、schema 字段、状态枚举必须类型收窄；适合枚举的字段必须定义枚举，不要用万能类型掩盖契约。
18. 代码改动后，至少运行与改动相关的测试；无法运行时必须在最终说明中说明原因。
19. 对已知优化项、临时方案、后续增强或未完成但不阻塞当前交付的事项，必须在最相关的代码位置留下清晰 `TODO(scope): ...` 注释，说明触发条件和后续动作；不要用 TODO 掩盖当前必须修复的 bug、安全问题或数据一致性问题。

## 规范整理模式

当任务是“代码规范检查、清理、收敛命名或优化结构”时，按保守整理处理：

- 不引入新包、不改变 API 语义、不改变数据库结构、不改变业务状态流转。
- 优先收敛重复常量、散落字符串、裸 `dict`/`Any`、模糊命名和跨层耦合。
- 有限取值字段优先定义或复用 `StrEnum`；数据库字段不能随意从 `String` 改成 SQL `Enum`，除非同步迁移并确认兼容。
- 稳定 JSON 契约优先定义 Pydantic schema、DTO 或专用值对象；只有外部供应商透传、临时日志快照、非稳定扩展字段可以保留窄类型 `dict[str, object]`。
- 清理历史包袱只移除无引用、无语义或已被新规则替代的内容；不能顺手重写仍在承载业务兼容的代码。

## 资产上传与存储规则

- 用户图片、声音、示例图等业务资产优先走后端上传接口；前端不得为业务资产直接拿 OSS 签名 URL 直传，除非该模块已有明确例外。
- 后端上传接口接收 base64/data URL 或后端可控文件流，统一调用 `storage_service.save_base64_asset`、`save_generated_data_url` 等 storage service。
- 业务资产必须使用业务语义化存储路径模板，例如 `asset/character/reference/user/{user_id}/...`、`asset/character/generated/user/{user_id}/...`，不要混用泛化 `asset/image/...` 路径。
- 上传前需要版权、授权、隐私确认的资产，必须先走 `privacy_service` 记录确认，再把确认结果关联到业务流程。
- 生成任务只产出结果并回写自己的 owner 业务对象；存储文件落地仍通过 storage service，不能在任务里手写 OSS key 或直连基础设施。

## 开发流程

新增一个后端业务接口时，按这个顺序执行：

1. 确认模块归属和边界。
2. 在 `schema/` 定义请求、响应和必要 DTO。
3. 在 `model/` 定义或复用 ORM 模型。
4. 在 `service/` 实现业务逻辑和事务。
5. 在 `api/v1/` 添加路由，只做参数接收、依赖注入和 service 调用。
6. 在 `api/v1/router.py` 注册路由。
7. 如果有数据库变化，新增 Alembic migration。
8. 添加或更新测试。
9. 运行相关测试和迁移检查。

修改已有模块时，先阅读：

- 对应 `api/v1/*_api.py`
- 对应 `service/{module}/`
- 对应 `schema/{module}/`
- 对应 `model/{module}/`
- `docs/wiki/raw/articles/module-design.md` 中的模块边界

## 命名约定

- API 文件：`{module}_api.py`
- Service 目录：`service/{module}/`
- Model 目录：`model/{module}/`
- Schema 目录：`schema/{module}/`
- 路由变量统一命名为 `router`
- 数据库 session 参数统一命名为 `db`
- 创建 schema：`XxxCreate`
- 更新 schema：`XxxUpdate`
- 读取 schema：`XxxRead`
- 列表摘要：`XxxSummary`
- 内部 DTO：`XxxInternalDTO`

## 数据库与事务规则

- service 层负责提交事务。
- 单个业务动作应尽量在一个 service 方法内完成事务边界。
- 需要跨模块编排时，由编排模块 service 控制流程，但目标对象写入仍调用目标模块 service。
- 异步生成、导出、支付回调等必须设计幂等键或幂等处理。
- 额度消耗类流程应采用“预占 -> 确认 -> 释放”，避免任务失败或重复点击导致重复扣减。
- 列表查询必须考虑分页、排序和过滤条件，不要返回无上限全量数据。

## API 设计规则

- 所有 v1 API 放在 `backend/app/api/v1/`。
- 新路由必须注册到 `backend/app/api/v1/router.py`。
- response model 必须明确。
- 错误场景使用合适 HTTP 状态码。
- 需要登录、管理员、资源归属校验时，必须通过统一依赖或 service 断言实现。
- API 不返回 ORM model 的内部结构；必须通过 schema 输出。

## 测试与验证

优先运行：

```bash
uv run pytest
```

针对 API 改动，至少覆盖：

- 成功路径。
- 权限/归属失败。
- 参数非法。
- 关键业务边界，例如额度不足、资源不存在、状态不允许。

针对数据库改动，至少检查：

- Alembic migration 可以执行。
- model 被导入到 `model/__init__.py`。
- 新字段默认值、nullable、索引、唯一约束符合业务含义。

## 常见反模式

避免以下写法：

- 在 API 文件里写几十行业务流程。
- API 直接 `db.get()` 后修改别的模块对象。
- service 里直接读取环境变量。
- 为了省事把稳定结构写成 `dict`、`dict[str, Any]`、`Any` 或万能 payload，而不是定义明确对象。
- 把状态、类型、来源、动作等有限取值字段写成散落字符串，而不是定义枚举。
- 一个模块同时拥有内容、进度、统计、推荐、审核等多种不相关职责。
- 后台接口绕过前台 service 直接改表。
- 生成任务模块决定生成结果写入哪个业务表。
- 推荐位复制完整绘本或故事内容，而不是保存目标引用和摘要。
- analytics 反向修改业务对象。
- privacy 替代 moderation 做审核结论。

## 交付说明要求

完成后端开发后，最终回复必须说明：

- 改动了哪些模块。
- 是否新增/修改数据库结构和迁移。
- 是否新增/修改 API。
- 运行了哪些测试或为什么无法运行。
- 是否存在需要后续确认的业务边界。
