---
name: code-review
description: AIrchieve 项目代码审查技能。当用户要求 review、代码审查、检查 PR/变更、找 bug/风险/回归时使用。覆盖后端 FastAPI/SQLAlchemy/Alembic、前端 React/TypeScript/Vite，以及项目模块边界、测试验证和交付质量审查。
---

# AIrchieve Code Review

本技能用于 AIrchieve 项目的代码审查。审查目标是优先发现真实缺陷、行为回归、模块边界破坏、测试缺口和可维护性风险，而不是泛泛给风格建议。

## 使用范围

当用户提出以下请求时使用本技能：

- “review / code review / 代码审查 / 检查这次改动 / 看看有没有问题”。
- 审查 PR、diff、commit、工作区变更或指定文件。
- 查找 bug、回归风险、安全风险、数据一致性风险、测试遗漏。
- 审查后端、前端、前后端契约或项目模块边界。

配合使用：

- 审查 `backend/app/` 后端代码时，同时参考 `backend-develop`。
- 审查 `frontend/` 前端代码时，同时参考 `frontend-develop`。
- 用户明确要求补测试、改测试或调试测试时，再使用对应测试技能。

不适用：

- 用户明确要求实现功能时，优先使用开发技能；只有完成后需要自检时再按本技能做审查。
- 纯文案、纯需求讨论且不涉及代码质量判断时不需要使用。

## 审查原则

必须遵守：

- 以缺陷优先。先找会导致错误行为、数据损坏、安全问题、权限绕过、构建失败、测试失败、用户可见回归的问题。
- 只报告能被代码、diff、文档或运行结果支撑的问题。不要用“可能不够优雅”当作主要发现。
- 不把个人偏好、无关重构、命名小意见包装成阻塞问题。
- 对每个发现给出文件和行号，并说明触发条件与影响。
- 如果没有发现问题，明确说没有发现阻塞性问题，并说明仍有哪些验证未覆盖。
- 不要擅自修改代码，除非用户明确要求“顺手修掉”或后续要求实现修复。

规范审查补充：

- 规范类问题必须能落到高内聚低耦合、模块边界、类型契约、命名歧义、重复历史包袱或测试可验证性，不报告空泛“更优雅”。
- 检查有限取值是否使用枚举或枚举式常量，稳定结构是否使用 schema/DTO/interface，而不是散落字符串、裸 `dict`、`Any`、`any` 或万能 payload。
- 只建议不改变现有逻辑的整理；如果修复会影响 API、数据库结构、业务状态流转或依赖包，必须单独标出并等待确认。
- 对重复发现按根因聚合，优先给出代表性文件和可复用修复方向，避免啰嗦罗列同类低价值项。

严重度分级：

- `Critical`：会造成数据丢失、权限绕过、支付/隐私/安全事故、生产不可用。
- `High`：主要功能错误、接口契约破坏、数据库迁移不可用、构建或核心测试失败。
- `Medium`：边界场景错误、状态不一致、可见体验回归、重要测试缺失。
- `Low`：局部可维护性、可访问性、类型收窄、非阻塞一致性问题。

## 推荐流程

1. 明确审查范围：工作区 diff、指定文件、指定 commit/PR，或用户粘贴的代码。
2. 查看变更概览：优先使用 `git status --short`、`git diff --stat`、`git diff`、`git diff --cached`。
3. 按改动路径加载对应技能与上下文：
   - 后端：读相关 `api/v1`、`service`、`schema`、`model`、迁移文件。
   - 前端：读相关页面、组件、类型、API 调用、共享 UI。
   - 跨模块：读 `docs/wiki/raw/articles/module-design.md` 中相关边界。
4. 顺着数据流审查，而不是只看单个文件：
   - 前端交互 -> API 契约 -> 后端 schema -> service 规则 -> model/迁移。
   - 后端 API -> service -> model -> migration -> 测试。
5. 需要时运行最小验证命令；无法运行时在结果中说明。
6. 输出 findings first：问题列表在前，摘要在后。

## 输出格式

审查回复默认使用以下结构：

```markdown
**Findings**
- [High] `path/to/file.ts:42` 问题标题
  说明触发条件、实际影响，以及为什么当前实现会出错。

**Open Questions**
- 需要用户确认的业务边界或假设。

**Notes**
- 未发现问题时说明“未发现阻塞性问题”。
- 简短说明看过的范围和未运行/已运行的验证。
```

要求：

- Findings 按严重度从高到低排序。
- 每条 finding 必须包含可定位位置，例如 `frontend/src/pages/X.tsx:88`。
- 说明要具体到“什么输入/状态会触发什么错误结果”。
- 如果只是测试缺口，必须说明该缺口对应的实际风险。
- 摘要保持简短，不要盖过 findings。

## 后端审查清单

审查 `backend/app/` 时重点检查：

- API 层是否只负责路由、参数、依赖注入和 response model；是否把业务流程写进 API。
- 写操作是否进入对应模块 service；跨模块写操作是否绕过目标模块 service 直接改 ORM。
- 权限、归属、管理员、会员、额度、隐私确认是否通过统一依赖或 service 执行。
- 业务结构是否使用明确 schema/DTO/枚举；是否出现稳定契约里的 `Any`、裸 `dict`、万能 payload。
- SQLAlchemy async 用法是否正确；是否遗漏 `await`、错误复用 session、在业务代码自行创建 engine/session。
- 事务边界是否合理；支付、导出、生成、额度消耗是否具备幂等或重复提交保护。
- 列表查询是否分页、排序、过滤明确；是否返回无上限全量数据。
- 数据库结构变化是否有 Alembic migration，model 是否在 `backend/app/model/__init__.py` 导出。
- 内部 ORM 主键和外键 id 是否使用 `int` / `Integer`，没有误用 UUID 或字符串作为内部模型 id。
- 历史事实类数据（支付、审计、导出、分享、审核）是否被危险物理删除。
- 错误码和异常是否符合 HTTP 语义，是否泄露内部实现或敏感信息。
- 测试是否覆盖成功路径、权限/归属失败、非法参数和关键业务边界。

后端高风险模块：

- `membership / entitlement`、`payment`、`privacy`、`generation_task`、`storage`、`share`、`export`、`admin`、`audit`。
- 涉及这些模块时，提高对幂等、权限、隐私、审计和历史记录的审查优先级。

## 前端审查清单

审查 `frontend/` 时重点检查：

- 页面是否只做编排，复杂业务流程是否沉到对应 `features` / 业务模块。
- 是否破坏 `docs/wiki/raw/articles/module-design.md` 的模块边界，例如播放器实现上传、会员外部自行计算权益、创建流程复制素材库逻辑。
- React 状态是否存在重复来源、派生状态错误、render 中副作用、异步竞态或卸载后更新。
- 异步请求是否处理 loading、error、empty、权限不足、登录失效和会员限制。
- TypeScript 类型是否收窄；是否使用 `any` 掩盖公共契约。
- 内部后端 id 是否用 `number`，外部平台标识或配置项 id 才使用 `string`。
- 列表 key 是否稳定，避免用可变数组下标造成状态错位。
- 表单是否阻止默认提交、处理校验和错误反馈，禁用态是否防重复提交。
- 交互控件是否有可访问名称、键盘可用性、focus/disabled 状态。
- UI 是否在移动端 375px 宽度下不重叠、不溢出、不出现按钮文字挤出。
- 是否复用现有 `components/ui`、`cn`、`lucide-react`，避免复制基础组件或引入新 UI 库。
- 是否残留 `console.log`、无用 import、未使用状态、注释掉的大段代码。
- 验证是否至少覆盖 `npm run typecheck`；页面/样式/路由/构建配置改动优先跑 `npm run build`。

儿童产品体验风险：

- 儿童阅读和播放主流程不应出现商业购买入口。
- 分享播放页应只读展示，不应开放编辑。
- 上传个人图片、声音、故事前应有授权或隐私提示。
- 删除形象或声音不应破坏历史绘本展示。

## 前后端契约审查

当前后端都改动时，必须检查：

- API 路径、HTTP 方法、请求字段、响应字段、错误结构是否一致。
- `id` 类型是否一致：内部模型 id 前后端应为数字。
- 枚举值、状态流转、分页字段、排序字段是否一致。
- 前端是否依赖后端没有承诺的 ORM 内部字段。
- 后端 response model 是否能满足前端 loading/empty/error 展示。
- 权限、会员、隐私限制是否由后端强制，前端只做展示和交互引导。

## 模块边界审查

`docs/wiki/raw/articles/module-design.md` 是主依据。重点防止：

- `story` 混入绘本页面、图片、音频、播放器结构。
- `book` 承担收藏、阅读进度；这些应归 `reading`。
- `template` 重新创作绘本结构或开放画风/正文/背景修改。
- `asset` 与 `storage` 混淆：素材业务归 asset，文件存取归 storage。
- `generation_task` 决定生成结果归属；它只管理任务生命周期和结果引用。
- `analytics` 反向修改业务对象。
- `admin` 绕过业务 service 直接改核心表。
- `privacy` 替代 `moderation / audit` 做审核结论。

## 验证命令选择

按变更范围选择最小有效验证：

后端：

```bash
uv run pytest
uv run alembic upgrade head
```

前端：

```bash
cd frontend
npm run typecheck
npm run build
```

审查时不必为了完整性运行所有命令；优先运行能验证当前风险的命令。命令失败时区分：

- 发现了真实问题：作为 finding 报告。
- 环境或依赖缺失：在 Notes 中说明无法验证的原因。

## 常见有效 Findings 示例

有效：

- “`backend/app/api/v1/orders_api.py:73` 未校验订单归属，登录用户可以传入其他用户的 `order_id` 查看支付状态。”
- “`frontend/src/pages/book/ReaderPage.tsx:118` 使用数组下标作为页面 key，删除页面后音频播放状态会错位。”
- “`backend/alembic/versions/xxx.py:34` 新增非空字段没有 server default，已有数据库执行迁移会失败。”

无效或应降级：

- “这里可以更优雅。”
- “建议重构一下。”
- “变量名不够好。”
- “最好加测试。”但没有说明缺少测试会漏掉什么风险。
