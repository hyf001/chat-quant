# Claudable 项目代码生成完整实现逻辑分析

## 📊 系统架构概览

Claudable 采用**前后端分离 + 实时 WebSocket 通信 + 多 CLI 适配器**的架构：

```
┌─────────────────────────────────────────────────────────────┐
│                      前端 (Next.js)                          │
│  ┌────────────┐  ┌──────────────┐  ┌───────────────┐       │
│  │ ChatInput  │→ │ ChatLog      │→ │ useWebSocket  │       │
│  └────────────┘  └──────────────┘  └───────────────┘       │
└─────────────────────────────┬───────────────────────────────┘
                              │ HTTP/WebSocket
┌─────────────────────────────┴───────────────────────────────┐
│                      后端 (FastAPI)                          │
│  ┌────────────┐  ┌──────────────┐  ┌───────────────┐       │
│  │ act.py API │→ │ UnifiedCLI   │→ │ ClaudeCodeCLI │       │
│  │            │  │ Manager      │  │ (SDK)         │       │
│  └────────────┘  └──────────────┘  └───────────────┘       │
│         ↓                                    ↓               │
│  ┌──────────────────┐           ┌────────────────────┐     │
│  │ WebSocket        │           │ Project Files      │     │
│  │ Manager          │           │ (data/projects/)   │     │
│  └──────────────────┘           └────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

---

## 完整流程：从用户输入到代码生成

### 阶段 1: 项目创建

#### 1.1 用户输入项目信息
**文件**: `apps/web/components/CreateProjectModal.tsx`

用户填写：
- 项目名称
- 项目描述/需求 (initial_prompt)
- 选择 CLI (claude/agent)
- 选择模型 (sonnet-4.5/opus-4.1 等)

#### 1.2 前端发起创建请求

```typescript
// CreateProjectModal.tsx:408
POST ${API_BASE}/api/projects/
{
  project_id: uuid,
  name: "项目名称",
  initial_prompt: "用户的项目描述",
  preferred_cli: "agent",
  selected_model: "claude-sonnet-4-5"
}
```

#### 1.3 后端创建项目记录

**文件**: `apps/api/app/api/projects/crud.py:316-370`

```python
@router.post("/", response_model=Project)
async def create_project(body: ProjectCreate, db: Session):
    # 1. 创建数据库记录，状态为 "initializing"
    project = ProjectModel(
        id=body.project_id,
        name=body.name,
        initial_prompt=body.initial_prompt,
        status="initializing",
        preferred_cli=body.preferred_cli,
        selected_model=body.selected_model
    )
    db.add(project)
    db.commit()

    # 2. 通过 WebSocket 发送初始化状态
    await websocket_manager.broadcast_to_project(project.id, {
        "type": "project_status",
        "data": {"status": "initializing", "message": "Setting up workspace..."}
    })

    # 3. 异步执行项目初始化
    asyncio.create_task(initialize_project_background(...))
```

#### 1.4 项目初始化

**文件**: `apps/api/app/api/projects/crud.py:68-151`

```python
async def initialize_project_background(project_id, project_name, body):
    # 1. 初始化 Next.js 项目文件结构
    project_path = await initialize_project(project_id, project_name)
    # 创建: data/projects/{project_id}/
    # 包含: package.json, tsconfig.json, next.config.mjs,
    #      src/app/page.tsx, src/app/layout.tsx, etc.

    # 2. 更新项目路径
    project.repo_path = project_path
    project.status = "active"
    db.commit()

    # 3. 发送完成状态
    await websocket_manager.broadcast_to_project(project_id, {
        "type": "project_status",
        "data": {"status": "active", "message": "Project ready!"}
    })
```

#### 1.5 前端接收状态并导航

**文件**: `apps/web/components/CreateProjectModal.tsx:206-224`

```typescript
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.type === 'project_status' && data.data.status === 'active') {
    // 项目就绪，导航到聊天页面，携带 initial_prompt
    router.push(`/${projectId}/chat?initial_prompt=${encodeURIComponent(prompt)}`);
  }
}
```

---

### 阶段 2: 用户发送指令

#### 2.1 聊天页面自动发送 initial_prompt

**文件**: `apps/web/app/[project_id]/chat/page.tsx`

```typescript
useEffect(() => {
  const params = new URLSearchParams(window.location.search);
  const initialPrompt = params.get('initial_prompt');
  if (initialPrompt && !hasSentInitialPrompt) {
    // 自动发送初始指令
    handleSendMessage(initialPrompt, [], true); // is_initial_prompt=true
  }
}, []);
```

#### 2.2 用户在 ChatInput 中输入后续指令

**文件**: `apps/web/components/chat/ChatInput.tsx:47-60`

```typescript
const handleSubmit = (e: React.FormEvent) => {
  if (message.trim() || uploadedImages.length > 0) {
    onSendMessage(message, uploadedImages); // 发送消息和图片
    setMessage('');
    setUploadedImages([]);
  }
};
```

#### 2.3 前端发送 Act/Chat 请求

```typescript
// 根据模式 (act/chat) 发送到不同端点
const endpoint = mode === 'act'
  ? `${API_BASE}/api/chat/${projectId}/act`
  : `${API_BASE}/api/chat/${projectId}/chat`;

POST endpoint
{
  instruction: "用户的指令",
  conversation_id: "会话ID",
  images: [{ path: "图片路径", name: "文件名" }],
  is_initial_prompt: true/false
}
```

---

### 阶段 3: 后端处理请求

#### 3.1 API 接收请求

**文件**: `apps/api/app/api/chat/act.py:501-688`

```python
@router.post("/{project_id}/act", response_model=ActResponse)
async def run_act(project_id: str, body: ActRequest, background_tasks, db):
    # 1. 保存用户消息到数据库
    user_message = Message(
        id=str(uuid.uuid4()),
        project_id=project_id,
        role="user",
        content=body.instruction,
        metadata_json={
            "has_images": len(body.images) > 0,
            "attachments": [...] # 图片附件信息
        }
    )
    db.add(user_message)

    # 2. 创建会话记录
    session = ChatSession(
        id=str(uuid.uuid4()),
        project_id=project_id,
        status="active",
        cli_type=preferred_cli
    )
    db.add(session)

    # 3. 通过 WebSocket 发送用户消息
    await manager.send_message(project_id, {
        "type": "message",
        "data": user_message
    })

    # 4. 在后台任务中执行指令
    background_tasks.add_task(
        execute_act_task,
        project_info,
        session,
        body.instruction,
        conversation_id,
        body.images,
        db,
        cli_preference,
        body.is_initial_prompt
    )
```

#### 3.2 后台任务执行

**文件**: `apps/api/app/api/chat/act.py:261-498`

```python
async def execute_act_task(project_info, session, instruction, ...):
    # 1. 发送开始事件
    await manager.broadcast_to_project(project_id, {
        "type": "act_start",
        "data": {"session_id": session.id, "instruction": instruction}
    })

    # 2. 初始化 UnifiedCLIManager
    cli_manager = UnifiedCLIManager(
        project_id=project_id,
        project_path=project_repo_path,
        session_id=session.id,
        conversation_id=conversation_id,
        db=db
    )

    # 3. 执行指令
    result = await cli_manager.execute_instruction(
        instruction=instruction,
        cli_type=cli_preference,  # claude/agent
        images=images,
        model=project_selected_model,
        is_initial_prompt=is_initial_prompt
    )

    # 4. 提交更改 (如果有)
    if result.get("has_changes"):
        commit_result = commit_all(project_repo_path, commit_message)

    # 5. 发送完成事件
    await manager.broadcast_to_project(project_id, {
        "type": "act_complete",
        "data": {"status": "completed", "session_id": session.id}
    })
```

---

### 阶段 4: CLI 适配器执行

#### 4.1 UnifiedCLIManager 调度

**文件**: `apps/api/app/services/cli/manager.py:41-81`

```python
class UnifiedCLIManager:
    async def execute_instruction(self, instruction, cli_type, ...):
        # 1. 获取对应的 CLI 适配器
        cli = self.cli_adapters[cli_type]  # ClaudeCodeCLI 或 ClaudeAgentCLI

        # 2. 检查可用性
        status = await cli.check_availability()
        if status.get("available"):
            # 3. 执行指令
            return await self._execute_with_cli(cli, instruction, images, model)
```

#### 4.2 执行并收集消息

**文件**: `apps/api/app/services/cli/manager.py:83-233`

```python
async def _execute_with_cli(self, cli, instruction, images, model):
    messages_collected = []
    has_changes = False

    # 流式处理 CLI 输出
    async for message in cli.execute_with_streaming(
        instruction=instruction,
        project_path=self.project_path,
        images=images,
        model=model,
        is_initial_prompt=is_initial_prompt
    ):
        # 1. 保存消息到数据库
        message.project_id = self.project_id
        self.db.add(message)
        self.db.commit()

        # 2. 通过 WebSocket 实时发送给前端
        await ws_manager.send_message(self.project_id, {
            "type": "message",
            "data": {
                "id": message.id,
                "role": message.role,
                "content": message.content,
                "metadata": message.metadata_json
            }
        })

        messages_collected.append(message)

    return {"success": True, "has_changes": has_changes}
```

#### 4.3 ClaudeCodeCLI 执行 (核心)

**文件**: `apps/api/app/services/cli/adapters/claude_code.py:83-484`

```python
class ClaudeCodeCLI(BaseCLI):
    async def execute_with_streaming(
        self, instruction, project_path, images, model, is_initial_prompt
    ):
        # 1. 加载系统提示词
        system_prompt = get_system_prompt()

        # 2. 处理图片 (如果有)
        if images:
            # 添加图片引用到指令中
            image_refs = [f"Image #{i+1}: {img['path']}" for i, img in enumerate(images)]
            instruction = f"{instruction}\n\nUploaded images:\n{image_refs}\n..."

        # 3. 配置工具 (根据 is_initial_prompt 决定是否包含 TodoWrite)
        if is_initial_prompt:
            allowed_tools = ["Read", "Write", "Edit", "Bash", "Glob", "Grep", ...]
            disallowed_tools = ["TodoWrite"]  # 初始提示不允许使用 TodoWrite
        else:
            allowed_tools = [..., "TodoWrite"]  # 后续提示允许使用

        # 4. 配置 Claude Code 选项
        options = ClaudeCodeOptions(
            system_prompt=system_prompt,
            allowed_tools=allowed_tools,
            disallowed_tools=disallowed_tools,
            model=cli_model,  # claude-sonnet-4-5-20250929
            continue_conversation=True  # 继续之前的会话
        )

        # 5. 切换到项目目录并执行
        os.chdir(project_path)  # cd data/projects/{project_id}/

        async with ClaudeSDKClient(options=options) as client:
            # 6. 发送查询
            await client.query(instruction)

            # 7. 流式接收响应
            async for message_obj in client.receive_messages():
                if isinstance(message_obj, AssistantMessage):
                    # 处理 AI 响应
                    for block in message_obj.content:
                        if isinstance(block, TextBlock):
                            # 文本内容
                            yield Message(content=block.text, ...)
                        elif isinstance(block, ToolUseBlock):
                            # 工具使用 (Read, Write, Edit, Bash 等)
                            tool_name = block.name
                            tool_input = block.input
                            summary = self._create_tool_summary(tool_name, tool_input)
                            yield Message(
                                content=summary,
                                message_type="tool_use",
                                ...
                            )

                elif isinstance(message_obj, ResultMessage):
                    # 执行完成
                    yield Message(
                        content=f"Session completed in {message_obj.duration_ms}ms",
                        message_type="result",
                        metadata_json={"hidden_from_ui": True}
                    )
                    break
```

#### 4.4 Claude Code SDK 工作原理

Claude Code SDK (`ClaudeSDKClient`) 会：

- **在项目目录下执行**: `cd data/projects/{project_id}/`
- **根据配置使用工具**:
  - `Read`: 读取文件内容
  - `Write`: 创建新文件
  - `Edit`: 编辑现有文件
  - `Bash`: 执行命令 (如 `npm install`, `npm run dev`)
  - `Glob/Grep`: 搜索文件
- **AI 自主决策**:
  - 需要创建哪些文件
  - 文件的具体内容
  - 需要安装哪些依赖
  - 需要执行哪些命令
- **直接操作文件系统**: 所有文件操作直接在项目目录下进行

---

### 阶段 5: 实时通信

#### 5.1 WebSocket 连接管理

**文件**: `apps/api/app/core/websocket/manager.py`

```python
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def send_message(self, project_id: str, message_data: dict):
        # 向项目的所有 WebSocket 连接发送消息
        for connection in self.active_connections[project_id]:
            await connection.send_text(json.dumps(message_data))
```

#### 5.2 前端 WebSocket 钩子

**文件**: `apps/web/hooks/useWebSocket.ts:17-154`

```typescript
export function useWebSocket({ projectId, onMessage, onStatus }) {
  useEffect(() => {
    const ws = new WebSocket(`${WS_BASE}/api/chat/${projectId}`);

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);

      // 处理不同类型的消息
      if (data.type === 'message') {
        onMessage(data.data); // 显示 AI 消息
      } else if (data.type === 'act_start') {
        onStatus('act_start', data.data); // 显示加载状态
      } else if (data.type === 'act_complete') {
        onStatus('act_complete', data.data); // 清除加载状态
      }
    };
  }, [projectId]);
}
```

#### 5.3 ChatLog 显示消息

**文件**: `apps/web/components/ChatLog.tsx:152-224`

```typescript
const { isConnected } = useWebSocket({
  projectId,
  onMessage: (message) => {
    // 接收到新消息，添加到聊天记录
    setMessages(prev => [...prev, message]);
  },
  onStatus: (status, data) => {
    if (status === 'act_complete') {
      setIsWaitingForResponse(false); // 清除"思考中"状态
    }
  }
});
```

---

## 关键技术点

### 1. 多 CLI 适配器架构

**文件**: `apps/api/app/services/cli/`

```python
# 基础适配器接口
class BaseCLI(ABC):
    @abstractmethod
    async def check_availability(self) -> Dict[str, Any]:
        """检查 CLI 是否可用"""

    @abstractmethod
    async def execute_with_streaming(
        self, instruction, project_path, session_id, images, model
    ) -> AsyncGenerator[Message, None]:
        """执行指令并流式返回消息"""

# Claude Code 实现
class ClaudeCodeCLI(BaseCLI):
    async def execute_with_streaming(...):
        async with ClaudeSDKClient(...) as client:
            await client.query(instruction)
            async for message in client.receive_messages():
                yield parse_message(message)

# Claude Agent 实现 (类似)
class ClaudeAgentCLI(BaseCLI):
    ...
```

### 2. 会话持久化

每个项目维护独立的 Claude 会话 ID，后续对话会继续之前的上下文。

**文件**: `apps/api/app/services/cli/adapters/claude_code.py:486-506`

```python
async def get_session_id(self, project_id: str) -> Optional[str]:
    return self.session_mapping.get(project_id)

async def set_session_id(self, project_id: str, session_id: str):
    self.session_mapping[project_id] = session_id
```

### 3. 图片支持

前端上传图片 → 保存到 `data/assets/{project_id}/` → 将路径传给 AI → AI 使用 Read 工具读取图片

**文件**: `apps/api/app/api/chat/act.py:533-574`

```python
for img in body.images:
    path = img.path  # /data/assets/{project_id}/image.jpg
    attachments.append({
        "name": img.name,
        "url": f"/api/assets/{project_id}/{filename}"
    })
```

### 4. 工具使用可视化

AI 使用工具时，前端显示友好的摘要。

**文件**: `apps/api/app/services/cli/base.py:398-617`

```python
def _create_tool_summary(self, tool_name, tool_input):
    if tool_name == "Edit":
        file_path = tool_input.get("file_path")
        return f"**Edit** `{file_path}`"
    elif tool_name == "Write":
        return f"**Write** `{file_path}`"
    elif tool_name == "Bash":
        command = tool_input.get("command")
        return f"**Bash** `{command}`"
```

前端显示：
```
**Edit** `src/app/page.tsx`
**Write** `components/Button.tsx`
**Bash** `npm install react-icons`
```

---

## 完整数据流示例

**用户请求**: "创建一个带有登录表单的首页"

```
1. 前端 CreateProjectModal
   → POST /api/projects/
   → 创建项目 (project_id: abc-123)

2. 后端初始化项目
   → initialize_project("abc-123", "My App")
   → 创建: data/projects/abc-123/
   → 包含基础 Next.js 文件

3. 前端导航到聊天页面
   → /${project_id}/chat?initial_prompt=创建一个带有登录表单的首页

4. 聊天页面自动发送指令
   → POST /api/chat/abc-123/act
   → { instruction: "创建一个带有登录表单的首页", is_initial_prompt: true }

5. 后端处理
   → execute_act_task()
   → UnifiedCLIManager.execute_instruction()
   → ClaudeCodeCLI.execute_with_streaming()

6. Claude Code SDK 执行
   → cd data/projects/abc-123/
   → client.query("创建一个带有登录表单的首页")

   AI 决策流程:
   a. 分析需求 → 需要创建登录表单组件
   b. 使用 Write 工具 → 创建 src/components/LoginForm.tsx
      ```typescript
      export default function LoginForm() {
        return (
          <form className="...">
            <input type="email" placeholder="Email" />
            <input type="password" placeholder="Password" />
            <button type="submit">Login</button>
          </form>
        );
      }
      ```
   c. 使用 Edit 工具 → 修改 src/app/page.tsx
      ```typescript
      import LoginForm from '@/components/LoginForm';
      export default function Home() {
        return <div><LoginForm /></div>;
      }
      ```
   d. 使用 Bash 工具 → 安装依赖 (如果需要)
      npm install react-hook-form

7. 实时流式响应
   → WebSocket 发送每个工具使用消息
   → 前端 ChatLog 实时显示:
      - "**Write** `components/LoginForm.tsx`"
      - "**Edit** `src/app/page.tsx`"
      - "Created a login form component with email and password fields..."

8. 完成
   → 提交代码 (如果有更改)
   → 发送 act_complete 事件
   → 前端清除加载状态

9. 用户可以预览
   → 访问 http://localhost:3000 (项目的 dev server)
   → 看到新创建的登录表单
```

---

## 核心文件索引

### 前端 (Next.js)

| 文件路径 | 功能 |
|---------|------|
| `apps/web/components/CreateProjectModal.tsx` | 项目创建模态框 |
| `apps/web/components/chat/ChatInput.tsx` | 聊天输入组件 |
| `apps/web/components/ChatLog.tsx` | 聊天日志显示 |
| `apps/web/hooks/useWebSocket.ts` | WebSocket 连接钩子 |
| `apps/web/app/[project_id]/chat/page.tsx` | 聊天页面 |

### 后端 (FastAPI)

| 文件路径 | 功能 |
|---------|------|
| `apps/api/app/api/chat/act.py` | Act/Chat API 端点 |
| `apps/api/app/api/projects/crud.py` | 项目 CRUD 操作 |
| `apps/api/app/services/cli/manager.py` | CLI 管理器 |
| `apps/api/app/services/cli/base.py` | CLI 基类和工具 |
| `apps/api/app/services/cli/adapters/claude_code.py` | Claude Code 适配器 |
| `apps/api/app/core/websocket/manager.py` | WebSocket 管理器 |

---

## 核心优势

1. **实时反馈**: WebSocket 实时流式传输，用户看到 AI 的每一步操作
2. **多模型支持**: 统一接口支持 Claude Sonnet/Opus、GPT 等多个模型
3. **会话持续**: 对话上下文保持，AI 了解项目的完整历史
4. **图片识别**: 支持上传设计图，AI 根据图片生成代码
5. **工具透明化**: 用户清楚地看到 AI 使用了哪些工具，修改了哪些文件
6. **自动提交**: 代码更改自动提交到 git，便于版本管理

---

## 技术栈

### 前端
- **框架**: Next.js 14, React 18
- **语言**: TypeScript
- **样式**: Tailwind CSS
- **状态管理**: React Hooks
- **实时通信**: WebSocket API
- **动画**: Framer Motion

### 后端
- **框架**: FastAPI
- **语言**: Python 3.10+
- **数据库**: SQLAlchemy (SQLite/PostgreSQL)
- **实时通信**: WebSocket (FastAPI)
- **AI SDK**: Claude Code SDK, Claude Agent SDK

### 基础设施
- **Monorepo**: npm workspaces
- **Git**: 自动提交
- **文件存储**: 本地文件系统 (`data/projects/`, `data/assets/`)

---

## 总结

Claudable 实现了一个优雅的"对话式代码生成"系统，核心特点是：

1. **自主决策**: AI 根据用户需求自主决定创建/修改哪些文件
2. **实时反馈**: 通过 WebSocket 流式传输，用户实时看到每一步操作
3. **工具透明**: 清晰展示 AI 使用的工具 (Read/Write/Edit/Bash)
4. **可扩展性**: 多 CLI 适配器架构，易于添加新的 AI 模型
5. **用户友好**: 从项目创建到代码生成，全程自动化

这个架构真正实现了"描述需求 → 自动生成代码"的愿景，用户只需要用自然语言描述想要什么，AI 就能完成从文件创建到依赖安装的全过程！
