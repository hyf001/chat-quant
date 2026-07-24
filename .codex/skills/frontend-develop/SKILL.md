---
name: frontend-develop
description: Chat-Quant 项目前端开发技能。当处理 apps/web 下的 React/TypeScript/Vite/Tailwind 代码时使用，包括搭建前端框架、创建页面、组件、交互壳、UI 改进和 API 接入。
---

# Chat-Quant 前端开发指南

当处理 `apps/web/` 下的前端代码时使用本技能。前端模块边界以 `docs/stock-agent-prototype.html` 原型的信息架构为准；实现可分阶段推进，不要求像素级复刻原型，也不要求提前实现完整页面细节。`docs/概要设计说明书.md` 主要作为后端系统能力、API 方向和术语参考，不直接决定前端目录模块边界。

## 1. 使用范围

使用本技能的场景：

- 新增或修改 Chat-Quant 前端页面、组件、布局、交互壳。
- 搭建或调整 `apps/web` 的 Vite/React/Tailwind 工程结构。
- 根据 `docs/stock-agent-prototype.html` 拆分工作台 UI 模块。
- 接入前端 API client、路由、状态、流式消息渲染、图表展示壳。

不使用本技能的场景：

- 后端 FastAPI、uv、数据库、Agent Runtime、Python 运行时开发。
- 专门编写或调试前端测试时，优先使用 `frontend-unit-test`。
- 仅修改文档且不涉及前端代码约束时。

## 2. 开发前必须阅读的上下文

按需阅读：

- `docs/stock-agent-prototype.html`：前端页面结构、模块边界和交互区域的主依据，不作为必须完整复刻的页面实现。
- `docs/概要设计说明书.md`：理解平台术语、后端模块、Agent-facing CLI 和资产类型。
- `docs/prd.md`：理解产品目标和用户任务。
- 当前前端目录：`apps/web/src/`。

## 3. 技术栈

当前前端使用：

- React
- TypeScript
- Vite
- Tailwind CSS
- lucide-react

优先沿用当前技术栈。没有明确收益时，不引入新框架、新状态库、新 UI 库或新 CSS 方案。

## 4. 前端模块边界

前端以原型工作台区域拆分模块，而不是以后端 M1-M6 领域模块拆分。

推荐目录：

```text
apps/web/src/
  app/
    App.tsx
    providers/
  pages/
    WorkbenchPage.tsx
  modules/
    history/
    workspace/
    conversation/
    result/
    insight/
    composer/
  shared/
    api/
    components/
    constants/
    lib/
    types/
    styles/
```

模块职责：

- `history`：左侧历史会话列表、会话入口、新建会话按钮、移动端抽屉。
- `workspace`：工作台三栏布局、顶部标题栏、连接状态、页面级编排。
- `conversation`：对话线程、消息气泡、澄清卡、工具调用进度。
- `result`：指标卡、图表容器、图表 tab、结果操作按钮。
- `insight`：右侧对象详情、图表对象详情、结果对象详情、参数快照、版本列表。
- `composer`：底部输入 dock、快捷 prompt、发送按钮、输入状态。
- `shared`：基础 UI、图标按钮、通用样式 token、API 基础能力、公共类型。

约束：

- 页面层只做编排，不沉淀复杂业务逻辑。
- 原型区域内的 UI 逻辑放到对应 `modules/*`。
- 与后端资产概念相关的类型可以命名为 artifact、strategy、backtest，但组件仍按原型展示区域归属。
- 不为了方便跨模块 import 而把业务展示组件放进 `shared`。

## 5. React 代码规则

- 使用函数组件。
- 使用 TypeScript 明确 props。
- 组件名使用 PascalCase。
- 列表渲染使用稳定 key，不用数组下标作为可变业务列表 key。
- 交互元素必须有清晰的可访问名称。
- 局部 UI 状态放组件内部；跨模块状态集中到页面或后续专门状态层。
- 异步请求必须处理 loading、error、empty 状态。
- 事件处理函数命名使用 `handleXxx`，传给子组件的回调命名使用 `onXxx`。
- 不使用 `any`，除非第三方边界确实无法表达，并添加简短说明。

## 6. 样式与 UI 规则

- 以原型的工作台区域为目标：左历史、中对话、右详情，先搭结构，再逐步补齐细节。
- 使用 Tailwind 和 `apps/web/src/shared/styles/tokens.ts` 中沉淀的设计 token。
- 图标优先使用 `lucide-react`。
- 卡片圆角保持 8px 或以下。
- 交互控件要有 hover、focus、disabled 状态。
- 移动端按原型收起右侧详情，左侧历史变成 drawer。
- 文本不能溢出按钮、卡片、标签和指标容器。
- 不使用营销页、hero 区、大面积装饰渐变或与工作台无关的视觉元素。
- 不把原型里的大量内联样式原样搬进 React；应拆成组件和样式 token。

## 7. API 与数据规则

- 通用 HTTP 能力放 `shared/api`。
- 原型阶段可以使用 mock 数据，但必须与真实 API client 分离。
- 不在组件 JSX 中直接拼接复杂请求逻辑。
- API 错误必须转换成用户可理解的状态。
- 前端不要复制后端 M1-M6 的业务流程；前端只表达展示区域、用户动作和 API 边界。

## 8. 文件与导出规则

- 页面放 `pages`。
- 原型区域模块放 `modules/<area>`。
- 基础组件放 `shared/components`。
- 通用类型放 `shared/types` 或模块内离使用处最近的位置。
- 通用 API 放 `shared/api`。
- 模块公共入口使用 `index.ts` 汇总。
- 页面只依赖模块公开入口，不深层引用其他模块内部文件。
- 避免循环依赖。

## 9. 代码质量约束

- 删除无用 import、变量、状态。
- 不留下 `console.log`。
- 不提交注释掉的大段代码。
- 不引入未使用依赖。
- 不做与需求无关的大重构。
- 不修改与任务无关的用户改动。
- 对不阻塞当前交付的后续增强，可在最相关代码位置留下 `TODO(scope): ...`。

## 10. 验证规则

完成前优先运行：

```bash
npm --prefix apps/web run lint
npm --prefix apps/web run build
```

根据改动类型选择：

- 只改类型或组件 props：至少运行 `npm --prefix apps/web run lint`。
- 改页面、样式、Vite/Tailwind 配置：运行 `npm --prefix apps/web run build`。
- 改交互复杂页面：建议启动 `npm --prefix apps/web run dev` 并进行浏览器检查。

如果命令因为环境、依赖或沙箱限制无法运行，需要在最终回复中说明。

## 11. 开发流程

1. 确认需求对应原型中的哪个工作台区域。
2. 阅读原型相关结构和样式。
3. 检查现有模块与共享组件，优先复用。
4. 按 `history/workspace/conversation/result/insight/composer` 放置代码。
5. 实现代码。
6. 检查模块边界和依赖方向。
7. 运行类型检查或构建。
8. 总结改动和验证结果。
