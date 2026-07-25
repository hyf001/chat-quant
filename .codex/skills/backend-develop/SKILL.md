---
name: backend-develop
description: Chat-Quant 项目后端开发技能。当处理 apps/api 下的 Python 后端代码时使用此技能，包括 DDD 架构下的 FastAPI 路由、应用服务、领域模型、仓储接口、基础设施适配、Pydantic 契约、配置和后端规范审查。
---

# Backend Develop

本技能用于 Chat-Quant 后端开发。项目后端采用 DDD / Clean Architecture 风格组织代码，开发时优先维护领域边界、依赖方向和明确的数据契约，避免退化为 MVC 分层或跨层直连。

## 快速判断

当任务涉及以下内容时，使用本技能：

- 修改 `apps/api/app/` 或 `apps/api/tests/` 下的后端代码。
- 新增或修改 FastAPI 路由、应用服务、领域模型、领域服务、仓储接口或基础设施适配。
- 修改 Pydantic 请求/响应 schema 或跨层契约。
- 修改配置、依赖注入、运行时封装、持久化适配或外部系统适配。
- 设计或调整后端模块边界、依赖方向、事务边界和错误处理方式。

不适用范围：

- 前端开发使用 `frontend-develop`。
- 明确要求编写、运行或调试 Python 单元测试时，同时使用 `python-unit-test`。
- 仅做代码审查时，同时参考 `code-review`。

## 项目结构

当前后端包位于 `apps/api/app/`，使用仓库根目录 workspace 和 `apps/api/pyproject.toml` 管理后端包。

```text
apps/api/
  app/
    main.py                    # FastAPI app 创建入口
    api/                       # HTTP 接入层：router、route、API dependency
      routes/                  # 按能力拆分路由文件
      router.py                # 路由聚合
    application/               # 应用层：用例编排、事务边界、依赖装配
    domain/                    # 领域层：领域模型、值对象、领域服务、仓储接口
      {context}/               # 按 bounded context / 领域能力组织
    infrastructure/            # 基础设施层：DB、外部 SDK、文件、进程、运行时等适配
    schemas/                   # Pydantic API schema 与稳定契约
      contracts/               # 跨层或外部可复用契约
    core/                      # 配置和通用基础能力
    cli/                       # CLI 入口
  tests/                       # 后端包内测试
tests/                         # 仓库级后端测试
```

常见命令从仓库根目录执行：

```bash
uv sync --extra dev
uv run uvicorn app.main:app --reload --app-dir apps/api
uv run pytest
uv run ruff check apps/api tests
```

## DDD 依赖方向

依赖必须整体朝内：

```text
api -> application -> domain
infrastructure -> domain
application -> infrastructure  # 仅通过依赖注入、接口实现或装配点连接
schemas -> domain/application  # 仅承载边界契约，不承载业务流程
```

强制规则：

- `domain` 不依赖 `api`、`application`、`infrastructure`、FastAPI 或具体外部 SDK。
- `application` 负责用例编排，可以调用领域对象、领域服务和抽象仓储，不把业务规则散落到 route 中。
- `infrastructure` 实现持久化、外部服务、文件系统、进程、SDK 等技术细节，不拥有核心业务规则。
- `api` 只处理 HTTP 契约、依赖注入、认证上下文提取、状态码和错误映射。
- 跨 bounded context 交互优先通过应用服务、领域服务、明确 DTO 或仓储接口，不直接修改对方内部对象。

## 各层职责

### API 层：`apps/api/app/api/`

职责：

- 定义 route、HTTP 方法、路径、状态码和 response model。
- 接收和校验请求参数，注入依赖。
- 调用应用层用例并返回明确 schema。
- 将领域/应用错误映射为合适的 HTTP 错误。

规则：

- 不在 route 中写复杂业务流程、状态流转或持久化细节。
- 不从 route 直接操作基础设施实现，除非是非常薄的健康检查或调试入口。
- 新路由应注册到 `apps/api/app/api/router.py` 或既有聚合路由。
- API 不直接返回内部领域对象或基础设施对象；使用 schema 输出。

### 应用层：`apps/api/app/application/`

职责：

- 承载用户可见用例和跨领域编排。
- 管理事务边界、权限上下文、幂等、重试和副作用触发。
- 将 API 输入转换为领域调用，将领域结果转换为边界输出。

规则：

- 应用服务可以编排多个领域能力，但不应把领域不变量写成散落的过程代码。
- 一个用例的提交、回滚、补偿或失败语义必须清晰。
- 非阻塞副作用优先隔离到独立适配或事件/任务机制中。
- 对外部系统调用要有超时、错误归一、日志上下文和可测试替身。

### 领域层：`apps/api/app/domain/`

职责：

- 定义领域模型、值对象、领域服务、领域错误和仓储抽象。
- 表达核心规则、不变量、状态转换和可复用领域计算。
- 按 bounded context 组织代码，不按 MVC 技术层横切组织业务概念。

规则：

- 领域对象应保持与框架、HTTP、数据库和外部 SDK 解耦。
- 稳定状态、类型、动作、来源等有限取值使用 `Enum` / `StrEnum` 或明确类型。
- 领域错误使用明确异常或结果类型，避免用裸字符串、魔法返回值或通用 `Exception` 表达业务失败。
- 跨 context 暴露最小必要信息，优先使用 id、值对象、摘要 DTO 或公开服务方法。
- 不要让一个领域模块同时承担多个不相关职责；职责变宽时先拆边界。

### 基础设施层：`apps/api/app/infrastructure/`

职责：

- 实现仓储接口、外部 SDK 适配、文件/对象存储、进程运行、数据库访问、运行时隔离等技术细节。
- 把外部返回值转换为项目内部契约。
- 封装技术错误，避免外部异常类型泄漏到 API 层。

规则：

- 基础设施可以依赖领域接口和契约，但不要反向驱动领域设计。
- 外部路径、命令、环境变量、超时和开关应通过统一配置读取。
- 文件系统、网络、子进程和第三方 SDK 调用必须便于测试替换。
- 日志记录使用项目统一 logger；不要用 `print` 作为运行时日志。

### Schema / Contract 层：`apps/api/app/schemas/`

职责：

- 定义请求、响应、跨层 DTO 和稳定 JSON 契约。
- 使用 Pydantic v2 表达边界数据结构。
- 将 API 契约和领域内部对象解耦。

规则：

- 稳定契约禁止使用裸 `dict`、`dict[str, Any]`、`Any` 或万能 payload；使用明确 schema、DTO、TypedDict 或值对象。
- 请求、响应、内部 DTO 分开命名，不复用一个万能 schema。
- 输出 schema 如需从对象转换，使用 Pydantic v2 兼容方式，例如 `ConfigDict(from_attributes=True)`。
- 对外契约字段命名、可空性、默认值和枚举范围必须清晰。

## 配置与依赖

- 配置统一从 `apps/api/app/core/config.py` 的 settings 读取。
- 不要在业务代码里散落读取环境变量。
- 依赖装配集中在应用入口、dependency provider 或明确 composition root。
- 不要随意引入新的框架、ORM、配置系统、任务系统或全局状态管理方式。
- 新增依赖前先确认现有标准库、项目工具和已安装包是否足够。

## 数据与事务

- 持久化细节放在基础设施层，领域层只暴露仓储抽象或纯领域行为。
- 应用层定义用例级事务边界；不要让 route 或领域对象隐式提交事务。
- 需要幂等的命令型用例应设计幂等键、唯一约束或重复提交处理。
- 列表查询必须考虑分页、排序和过滤条件，不返回无上限全量数据。
- 数据结构变化必须配套迁移或兼容处理；如果项目当前没有迁移系统，最终说明要写明处理方式和残余风险。

## API 设计

- 新增 API 前先确认它属于哪个用例和 bounded context。
- response model 必须明确，错误场景使用合适 HTTP 状态码。
- 权限、资源归属、限流、幂等、校验等横切规则应通过统一依赖或应用服务断言实现。
- 不把内部异常、堆栈、文件路径、SDK 原始响应直接暴露给客户端。
- 后台、CLI、任务和 HTTP 入口复用同一应用层用例，避免重复业务规则。

## 命名约定

- API 路由文件按能力命名，放在 `api/routes/`。
- 路由变量命名为 `router`。
- 请求 schema：`XxxRequest`、`XxxCreate`、`XxxUpdate`。
- 响应 schema：`XxxResponse`、`XxxRead`、`XxxSummary`。
- 内部 DTO：`XxxDTO`、`XxxInternalDTO`。
- 领域错误：`XxxError` 或更具体的异常名。
- 仓储接口：`XxxRepository`；基础设施实现用技术后缀区分，例如 `FileXxxRepository`、`SqlXxxRepository`。

## 规范整理模式

当任务是“代码规范检查、清理、收敛命名或优化结构”时，按保守整理处理：

- 不引入新包、不改变 API 语义、不改变持久化结构、不改变核心状态流转。
- 优先收敛重复常量、散落字符串、裸 `dict`/`Any`、模糊命名和跨层耦合。
- 有限取值字段优先定义或复用枚举。
- 稳定 JSON 契约优先定义 Pydantic schema、DTO 或专用值对象。
- 清理历史包袱只移除无引用、无语义或已被新规则替代的内容。

## 常见反模式

避免以下写法：

- 把 DDD 目录当作 MVC，按 controller/service/model 机械搬运代码。
- 在 route 中写几十行业务流程或直接调用外部 SDK。
- 领域层 import FastAPI、Pydantic API schema、数据库 session 或基础设施实现。
- 应用服务绕过领域模型，直接堆过程式状态修改。
- 基础设施层泄漏外部 SDK 原始对象到 API 输出。
- 为了省事把稳定结构写成 `Any`、裸 `dict` 或万能 payload。
- 把有限状态写成散落字符串，而不是定义明确枚举或类型。
- 多个入口重复实现同一条业务规则。
- 在业务代码里直接读取环境变量或创建临时全局客户端。
- 用 TODO 掩盖当前必须修复的数据一致性、安全或契约问题。

## 开发流程

新增后端能力时，按这个顺序执行：

1. 确认 bounded context、入口类型和用例边界。
2. 定义或复用领域模型、值对象、领域服务和仓储抽象。
3. 在应用层实现用例编排、事务边界、错误归一和副作用策略。
4. 在基础设施层实现必要适配。
5. 在 `schemas/` 定义请求、响应和稳定契约。
6. 在 `api/routes/` 添加路由，并注册到路由聚合入口。
7. 添加或更新测试。
8. 运行相关测试和 lint。

修改已有能力时，优先阅读：

- 对应 `api/routes/` 路由。
- 对应 `application/` 应用服务。
- 对应 `domain/{context}/` 领域模型、服务、错误和仓储接口。
- 对应 `infrastructure/` 适配实现。
- 对应 `schemas/` 契约。
- 相关测试。

## 测试与验证

优先运行：

```bash
uv run pytest
uv run ruff check apps/api tests
```

针对 API 改动，至少覆盖：

- 成功路径。
- 参数非法。
- 权限、上下文或资源归属失败。
- 资源不存在或状态不允许。

针对应用/领域改动，至少覆盖：

- 领域不变量和状态转换。
- 跨 context 编排的失败语义。
- 幂等、重复提交或重试边界。
- 外部适配失败时的错误归一。

针对持久化或基础设施改动，至少检查：

- 替身或测试夹具能覆盖关键 I/O。
- 默认值、唯一约束、索引、nullable 和兼容路径符合契约。
- 外部命令、路径、网络、SDK 调用有可控配置和错误处理。

## 交付说明要求

完成后端开发后，最终回复必须说明：

- 改动了哪些层或模块。
- 是否新增/修改 API、契约、持久化结构或外部适配。
- 运行了哪些测试和 lint，或为什么无法运行。
- 是否存在需要后续确认的架构边界、迁移策略或兼容风险。
