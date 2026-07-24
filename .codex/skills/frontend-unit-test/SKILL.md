---
name: frontend-unit-test
description: 专门用于 AIrchieve 项目前端单元测试和组件测试工作的技能。仅当用户明确要求编写、生成、运行、改进或调试 frontend/ 下的 React/Vite/Vitest 测试时使用。不包括 miniprogram 小程序测试，也不用于普通功能开发或后端测试。
---

# Frontend 单元测试指南

面向当前项目时，默认只处理 `frontend/`：

- 前端技术栈是 React + Vite + TypeScript
- 测试框架是 Vitest
- 组件测试使用 React Testing Library
- 测试环境是 jsdom
- 不处理 `miniprogram/`

## 什么时候使用

仅在用户明确表达前端测试意图时触发，例如：

- “给这个 React 组件写测试”
- “补 frontend 的单元测试”
- “运行 Vitest”
- “调试前端测试失败”

不要在普通功能开发、代码评审、后端测试或小程序测试任务中自动使用。

## 工作流程

1. 先读被测代码，再决定测试范围。
2. 判断测试类型：
   - 纯函数或工具函数：优先写真正的单元测试
   - hooks：使用 React Testing Library 的组件包裹方式测试行为
   - 组件：优先测试用户可见行为和交互，不测试内部实现细节
   - services：mock `fetch`、第三方 SDK、浏览器 API 和后端接口
3. 测试文件优先与被测文件同目录放置，使用 `*.test.ts` 或 `*.test.tsx`。
4. 运行最小必要范围的测试。
5. 如果失败，先判断是测试设计问题还是源码 bug。不要为了“让测试通过”降低关键断言。

## AIrchieve 前端约定

### 路径与命令

所有命令默认在 `frontend/` 下执行：

```bash
npm run test:run
npm run test:coverage
npm run typecheck
```

运行单个测试文件：

```bash
npx vitest run src/path/to/file.test.tsx
```

运行 watch 模式：

```bash
npm test
```

### 测试文件位置

优先与源文件同目录：

- 源文件：`src/utils/editorUtils.ts`
- 测试文件：`src/utils/editorUtils.test.ts`
- 源文件：`src/components/LoginModal.tsx`
- 测试文件：`src/components/LoginModal.test.tsx`

跨组件集成测试可以放在更高层目录，但不要放到 `miniprogram/`。

### 推荐导入

项目配置了 `@` 指向 `frontend/src`，测试里可以直接使用：

```ts
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { cn } from '@/lib/utils';
```

`src/test/setup.ts` 已加载 `@testing-library/jest-dom/vitest`，断言中可以使用：

```ts
expect(screen.getByRole('button')).toBeInTheDocument();
```

## 编写要求

- 测试行为，不测试实现细节
- 优先使用 `getByRole`、`getByLabelText`、`getByText` 等用户视角查询
- 对交互使用 `userEvent.setup()`
- 外部依赖必须 mock，避免测试真实网络、真实支付、真实 AI SDK 或真实浏览器下载
- 每个测试只验证一个明确行为
- 命名直接表达意图，例如 `renders_submit_button_when_form_is_valid`
- 不为小程序代码创建测试

## 常见 mock 边界

优先在这些边界 mock：

- `fetch`
- `localStorage` / `sessionStorage`
- `URL.createObjectURL`
- `HTMLCanvasElement`
- `ResizeObserver` / `IntersectionObserver`
- `@google/genai`
- `@imgly/background-removal`
- `@mediapipe/tasks-vision`

如果组件依赖路由，使用 `MemoryRouter` 包裹。  
如果组件依赖认证上下文，优先 mock context 边界或使用最小测试 provider。

## 失败处理原则

- 如果测试合理而结果失败，优先报告源码问题
- 只有确认测试设计错误时才修改测试
- 不要通过删除断言、跳过测试或扩大 mock 来掩盖真实缺陷

## 执行顺序

完成测试变更后，优先运行：

```bash
npm run test:run
npm run typecheck
```

如果只改了一个测试文件，先运行单文件测试，再根据风险决定是否跑全量。
