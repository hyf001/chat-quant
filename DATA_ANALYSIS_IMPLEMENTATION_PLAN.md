# 扩展 Claudable 支持数据分析应用 - 完整技术实施方案

## 项目背景
Claudable 是一个基于 Next.js 的 Web 应用构建器，当前仅支持生成 Next.js 应用。本方案旨在扩展平台功能，新增数据分析应用类型，让用户可以通过 AI 助手进行数据分析、SQL 查询和可视化报告生成。

## 核心目标
1. 在主页面增加应用类型选择，支持"Next.js应用"和"数据分析应用"
2. 根据不同应用类型初始化不同的项目结构
3. 为数据分析应用提供专用的系统提示词和工具集
4. 实现完整的数据分析工作流程

## 数据流设计

### 1. 创建项目流程（数据分析项目）

#### (1) 用户输入项目信息
- 选择项目类型：`data_analysis`
- 项目名称（initial_prompt）
- 项目描述/需求（可选）
- 选择 CLI：`agent`
- 选择模型：`sonnet-4.5/opus-4.1` 等

#### (2) 前端发起创建请求
```json
POST /api/projects/
{
  "project_id": "project-xxx",
  "name": "销售数据分析",
  "project_type": "data_analysis",
  "initial_prompt": "分析2024年销售数据趋势",
  "preferred_cli": "agent",
  "selected_model": "claude-sonnet-4-5"
}
```

#### (3) 后端创建项目记录
- 保存 `template_type` = "data_analysis"
- 设置状态为 "initializing"

#### (4) 项目初始化
创建数据分析项目文件结构：
```
/data/projects/{project_id}/
├── repo/                    # 业务线元数据
│   ├── dream/              # Dream 业务线
│   │   ├── reports/        # 报表
│   │   ├── tables/         # 数据表
│   │   ├── kyc_labels/     # KYC用户标签
│   │   ├── events/         # 用户行为事件
│   │   └── tpc_metrics/    # TPC指标
│   ├── ainvest/           # AI投资业务线
│   └── aime/              # AI医疗业务线
├── assets/                 # 上传的图片、文件等
├── data/
│   └── metadata/          # 项目名称、描述等
├── dashboard/             # 生成的分析报告
├── data_file/            # 生成的数据文件
│   ├── intermediate/     # 中间结果
│   └── final/           # 最终结果
└── scripts/             # 生成的数据处理脚本
```

### 2. 用户发送指令流程
1. 聊天页面自动发送 initial_prompt
2. 用户上传图片或发送后续指令
3. 前端上传图片到 `{project_id}/assets/`
4. 将图片路径传给 AI，AI 使用 Read 工具读取

### 3. 后端处理和 AI 执行
1. API 接收请求，保存消息到数据库
2. 创建会话记录，维护 Claude 会话上下文
3. UnifiedCLIManager 调度执行
4. ClaudeAgentCLI 加载数据分析系统提示词
5. 配置数据分析工具集
6. 执行分析任务并生成结果

## 前端改动详细说明

### 1. 类型定义扩展
**文件：`apps/web/types/cli.ts`**

```typescript
// 新增项目类型枚举
export enum ProjectType {
  NEXTJS = 'nextjs',
  DATA_ANALYSIS = 'data_analysis'
}

// 扩展项目接口
export interface Project {
  id: string;
  name: string;
  project_type: ProjectType;
  // ... 其他字段
}

// 项目类型配置
export const PROJECT_TYPE_OPTIONS = [
  {
    value: ProjectType.NEXTJS,
    label: 'Next.js 应用',
    description: '构建现代化的全栈 Web 应用',
    icon: '⚛️'
  },
  {
    value: ProjectType.DATA_ANALYSIS,
    label: '数据分析应用',
    description: '数据分析、SQL查询和可视化报告',
    icon: '📊'
  }
];
```

### 2. 主页面改造
**文件：`apps/web/app/page.tsx`**

主要修改点：
- 添加项目类型选择器（Select 组件）
- 修改 `handleSubmit` 函数，包含 `project_type` 参数
- 根据选择的类型显示不同的占位符文本和提示

### 3. 项目创建模态框
**文件：`apps/web/components/CreateProjectModal.tsx`**

主要修改点：
- 在表单中添加项目类型选择器
- 修改提交数据结构，包含 `project_type` 字段
- 更新初始化进度消息，区分不同类型

### 4. 聊天界面适配
**文件：`apps/web/app/[project_id]/chat/page.tsx`**

主要修改点：
- 获取项目类型信息
- 数据分析项目显示特定的帮助提示
- 支持数据文件和报告的显示

### 5. 项目设置
**文件：`apps/web/components/ProjectSettings.tsx`**

主要修改点：
- 显示项目类型（只读字段）
- 根据项目类型显示相关配置选项

## 后端改动详细说明

### 6. 数据模型扩展
**文件：`apps/api/app/models/projects.py`**

```python
class Project(Base):
    __tablename__ = "projects"

    # 使用现有字段
    template_type: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
        comment="Project type: nextjs or data_analysis"
    )

    # 添加验证
    @validates('template_type')
    def validate_template_type(self, key, value):
        if value and value not in ['nextjs', 'data_analysis']:
            raise ValueError(f"Invalid project type: {value}")
        return value
```

### 7. 项目创建 API 扩展
**文件：`apps/api/app/api/projects/crud.py`**

```python
class ProjectCreate(BaseModel):
    project_id: str
    name: str
    project_type: str = "nextjs"  # 新增字段，默认为 nextjs
    initial_prompt: str | None = None
    # ... 其他字段

@router.post("/", response_model=Project)
async def create_project(body: ProjectCreate, db: Session = Depends(get_db)):
    # 创建项目时保存 project_type
    project = ProjectModel(
        id=body.project_id,
        name=body.name,
        template_type=body.project_type,  # 保存项目类型
        # ... 其他字段
    )

    # 后台初始化时传递项目类型
    asyncio.create_task(
        initialize_project_background(
            project.id,
            project.name,
            body,
            project_type=body.project_type  # 传递类型
        )
    )
```

### 8. 项目初始化服务
**文件：`apps/api/app/services/project/initializer.py`**

```python
async def initialize_project(
    project_id: str,
    name: str,
    project_type: str = "nextjs"
) -> str:
    """根据项目类型初始化不同的项目结构"""

    if project_type == "data_analysis":
        return await initialize_data_analysis_project(project_id, name)
    else:
        return await initialize_nextjs_project(project_id, name)

async def initialize_data_analysis_project(project_id: str, name: str) -> str:
    """初始化数据分析项目"""

    # 创建项目根目录
    project_root = os.path.join(settings.projects_root, project_id)

    # 创建数据分析项目结构
    dirs = [
        f"{project_root}/repo/dream/reports",
        f"{project_root}/repo/dream/tables",
        f"{project_root}/repo/dream/kyc_labels",
        f"{project_root}/repo/dream/events",
        f"{project_root}/repo/dream/tpc_metrics",
        f"{project_root}/repo/ainvest",
        f"{project_root}/repo/aime",
        f"{project_root}/assets",
        f"{project_root}/data/metadata",
        f"{project_root}/dashboard",
        f"{project_root}/data_file/intermediate",
        f"{project_root}/data_file/final",
        f"{project_root}/scripts",
    ]

    for dir_path in dirs:
        ensure_dir(dir_path)

    # 创建项目元数据
    create_project_metadata(project_id, name)

    # 初始化示例元数据
    await init_sample_metadata(project_id)

    return f"{project_root}/repo"
```

### 9. 系统提示词管理
**文件：`apps/api/app/services/claude_act.py`**

```python
def get_system_prompt(project_type: str = "nextjs") -> str:
    """根据项目类型返回不同的系统提示词"""

    if project_type == "data_analysis":
        # 加载数据分析系统提示词
        prompt_path = os.path.join(
            os.path.dirname(__file__),
            "../prompt/data-analysis-system-prompt.md"
        )
    else:
        # 加载 Next.js 系统提示词
        prompt_path = os.path.join(
            os.path.dirname(__file__),
            "../prompt/system-prompt.md"
        )

    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()
```

### 10. Claude Agent 适配器扩展
**文件：`apps/api/app/services/cli/adapters/claude_agent.py`**

```python
async def execute_with_streaming(
    self,
    instruction: str,
    project_path: str,
    session_id: Optional[str] = None,
    project_type: str = "nextjs",  # 新增参数
    # ... 其他参数
) -> AsyncGenerator[Message, None]:

    # 根据项目类型加载不同的系统提示词
    from app.services.claude_act import get_system_prompt
    system_prompt = get_system_prompt(project_type)

    # 根据项目类型配置不同的工具集
    if project_type == "data_analysis":
        # 数据分析项目的工具集
        allowed_tools = [
            "Read", "Write", "Edit", "Bash",
            "Glob", "Grep", "WebFetch", "WebSearch",
            # 自定义数据分析工具
            "DownloadDataFile",
            "QueryReportFull", "CountReportData", "QueryReportSample",
            "ValidateSQL", "ExecuteSQLQuery", "CountSQLResult",
            "QuerySQLSample", "CreateTableAsSelect"
        ]

        # 注册自定义工具
        from app.services.tools import register_data_analysis_tools
        custom_tools = register_data_analysis_tools()

        options = ClaudeAgentOptions(
            system_prompt=system_prompt,
            allowed_tools=allowed_tools,
            custom_tools=custom_tools,  # 传入自定义工具
            permission_mode="bypassPermissions",
            model=cli_model
        )
    else:
        # Next.js 项目的默认工具集
        # ... 保持现有逻辑
```

### 11. 自定义工具实现
**新建文件：`apps/api/app/services/tools/data_analysis_tools.py`**

```python
from typing import Dict, Any, Optional
import json
import aiohttp
from pathlib import Path

class DataAnalysisTool:
    """数据分析工具基类"""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError

class DownloadDataFile(DataAnalysisTool):
    """下载数据文件工具"""

    def __init__(self):
        super().__init__(
            "DownloadDataFile",
            "下载远程数据文件到本地"
        )

    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        file_url = params.get("file_url")
        project_id = params.get("project_id")

        # 下载文件
        async with aiohttp.ClientSession() as session:
            async with session.get(file_url) as response:
                data = await response.json()

        # 保存到本地
        output_dir = Path(f"/data/projects/{project_id}/data_file")
        output_dir.mkdir(parents=True, exist_ok=True)

        filename = f"downloaded_{datetime.now():%Y%m%d_%H%M%S}.json"
        output_path = output_dir / filename

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return {
            "success": True,
            "local_file": str(output_path),
            "records_count": len(data) if isinstance(data, list) else 1
        }

class QueryReportFull(DataAnalysisTool):
    """查询报表全量数据"""

    def __init__(self):
        super().__init__(
            "QueryReportFull",
            "查询报表全量数据并返回文件地址"
        )

    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        report_id = params.get("report_id")

        # 模拟查询报表数据
        # 实际实现需要连接到真实的数据源
        mock_data_url = f"https://data.example.com/reports/{report_id}/full"

        return {
            "success": True,
            "file_url": mock_data_url,
            "report_id": report_id
        }

class ValidateSQL(DataAnalysisTool):
    """验证SQL语句语法"""

    def __init__(self):
        super().__init__(
            "ValidateSQL",
            "验证SQL语句的语法正确性"
        )

    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        sql = params.get("sql")
        engine = params.get("engine", "hive")

        # 这里需要实现实际的SQL验证逻辑
        # 可以使用 sqlparse 或连接到对应的数据库引擎

        try:
            import sqlparse
            parsed = sqlparse.parse(sql)
            if not parsed:
                return {
                    "is_valid": False,
                    "error_message": "无法解析SQL语句"
                }

            return {
                "is_valid": True,
                "engine": engine
            }
        except Exception as e:
            return {
                "is_valid": False,
                "error_message": str(e)
            }

class ExecuteSQLQuery(DataAnalysisTool):
    """执行SQL查询语句"""

    def __init__(self):
        super().__init__(
            "ExecuteSQLQuery",
            "执行SQL查询并返回结果文件地址"
        )

    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        sql = params.get("sql")
        engine = params.get("engine", "hive")
        project_id = params.get("project_id")

        # 这里需要实现实际的SQL执行逻辑
        # 连接到对应的数据库引擎执行查询

        # 模拟执行结果
        mock_result = [
            {"id": 1, "name": "Product A", "sales": 1000},
            {"id": 2, "name": "Product B", "sales": 1500},
        ]

        # 保存结果到文件
        output_dir = Path(f"/data/projects/{project_id}/data_file/intermediate")
        output_dir.mkdir(parents=True, exist_ok=True)

        filename = f"sql_result_{datetime.now():%Y%m%d_%H%M%S}.json"
        output_path = output_dir / filename

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(mock_result, f, ensure_ascii=False, indent=2)

        return {
            "success": True,
            "file_url": str(output_path),
            "records_count": len(mock_result),
            "engine": engine
        }

# 注册所有数据分析工具
def register_data_analysis_tools() -> list:
    """注册并返回所有数据分析工具实例"""

    tools = [
        DownloadDataFile(),
        QueryReportFull(),
        CountReportData(),
        QueryReportSample(),
        ValidateSQL(),
        ExecuteSQLQuery(),
        CountSQLResult(),
        QuerySQLSample(),
        CreateTableAsSelect(),
    ]

    # 转换为 Claude Agent SDK 格式
    sdk_tools = []
    for tool in tools:
        sdk_tools.append({
            "name": tool.name,
            "description": tool.description,
            "execute": tool.execute
        })

    return sdk_tools
```

### 12. 工具注册机制
**新建文件：`apps/api/app/services/tools/tool_registry.py`**

```python
from typing import Dict, Callable, Any
import asyncio

class ToolRegistry:
    """工具注册中心"""

    def __init__(self):
        self._tools: Dict[str, Callable] = {}

    def register(self, name: str, tool_func: Callable):
        """注册工具"""
        self._tools[name] = tool_func

    async def execute(self, name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """执行工具"""
        if name not in self._tools:
            raise ValueError(f"Tool {name} not registered")

        tool = self._tools[name]

        # 执行工具
        if asyncio.iscoroutinefunction(tool):
            result = await tool(params)
        else:
            result = tool(params)

        return result

    def get_tool_schema(self, name: str) -> Dict[str, Any]:
        """获取工具的参数 schema"""
        # 返回工具的输入参数定义
        # 这个需要根据实际的工具定义来实现
        pass

# 全局工具注册表
tool_registry = ToolRegistry()
```

### 13. Act API 扩展
**文件：`apps/api/app/api/chat/act.py`**

```python
async def execute_act_task(
    project_info: Dict[str, Any],
    session: ChatSession,
    instruction: str,
    # ... 其他参数
):
    # 获取项目类型
    project = db.get(Project, project_info["id"])
    project_type = project.template_type or "nextjs"

    # 传递项目类型到 CLI Manager
    result = await cli_manager.execute_instruction(
        instruction=instruction,
        cli_type=cli_preference,
        project_type=project_type,  # 传递项目类型
        # ... 其他参数
    )
```

### 14. CLI Manager 扩展
**文件：`apps/api/app/services/cli/unified_manager.py`**

```python
async def execute_instruction(
    self,
    instruction: str,
    cli_type: CLIType,
    project_type: str = "nextjs",  # 新增参数
    # ... 其他参数
):
    # 获取 CLI 适配器
    cli = self.cli_adapters[cli_type]

    # 执行指令，传递项目类型
    async for message in cli.execute_with_streaming(
        instruction=instruction,
        project_path=self.project_path,
        session_id=self.session_id,
        project_type=project_type,  # 传递项目类型
        # ... 其他参数
    ):
        # 处理消息
        yield message
```

## 示例元数据初始化
**新建文件：`apps/api/scripts/init_sample_metadata.py`**

```python
import json
from pathlib import Path

async def init_sample_metadata(project_id: str):
    """初始化示例元数据"""

    base_path = Path(f"/data/projects/{project_id}/repo/dream")

    # 创建示例报表元数据
    reports_path = base_path / "reports"
    reports_path.mkdir(parents=True, exist_ok=True)

    sample_report = {
        "id": "sales_monthly_2024",
        "name": "2024年月度销售报表",
        "description": "包含2024年每月的销售数据汇总",
        "fields": [
            {"name": "month", "type": "string", "description": "月份"},
            {"name": "total_sales", "type": "number", "description": "总销售额"},
            {"name": "order_count", "type": "number", "description": "订单数量"},
            {"name": "avg_order_value", "type": "number", "description": "平均订单金额"}
        ],
        "update_frequency": "monthly",
        "last_updated": "2024-12-01"
    }

    with open(reports_path / "sales_monthly_2024.json", 'w', encoding='utf-8') as f:
        json.dump(sample_report, f, ensure_ascii=False, indent=2)

    # 创建示例数据表元数据
    tables_path = base_path / "tables"
    tables_path.mkdir(parents=True, exist_ok=True)

    sample_table = {
        "name": "dw.fact_sales",
        "description": "销售事实表",
        "database": "dw",
        "engine": "hive",
        "columns": [
            {"name": "sale_id", "type": "bigint", "comment": "销售ID"},
            {"name": "product_id", "type": "string", "comment": "产品ID"},
            {"name": "customer_id", "type": "string", "comment": "客户ID"},
            {"name": "sale_date", "type": "date", "comment": "销售日期"},
            {"name": "amount", "type": "decimal(10,2)", "comment": "销售金额"},
            {"name": "quantity", "type": "int", "comment": "数量"}
        ],
        "partitions": ["dt"],
        "sample_sql": "SELECT * FROM dw.fact_sales WHERE dt='2024-12-01' LIMIT 100"
    }

    with open(tables_path / "fact_sales.json", 'w', encoding='utf-8') as f:
        json.dump(sample_table, f, ensure_ascii=False, indent=2)
```

## 测试计划

### 端到端测试流程
1. **创建数据分析项目**
   - 在主页选择"数据分析应用"类型
   - 输入项目名称和初始分析需求
   - 验证项目初始化成功

2. **执行数据分析**
   - 上传数据文件或图表截图
   - 发送分析指令
   - 验证工具调用正确

3. **生成分析报告**
   - 检查数据处理脚本生成
   - 验证可视化报告生成
   - 确认报告可以正常显示

### 关键测试点
- 项目类型选择和传递
- 系统提示词切换
- 自定义工具调用
- 数据文件管理
- 报告生成和展示

## 实施步骤和时间线

### 第一阶段：基础架构（2天）
- [ ] 前端类型定义和 UI 组件
- [ ] 后端项目模型扩展
- [ ] 项目初始化分支逻辑

### 第二阶段：系统集成（2天）
- [ ] 数据分析系统提示词集成
- [ ] Claude Agent 适配器扩展
- [ ] 项目类型参数传递

### 第三阶段：工具实现（3天）
- [ ] 实现基础数据分析工具
- [ ] 创建工具注册机制
- [ ] 集成工具到 Claude Agent

### 第四阶段：测试优化（2天）
- [ ] 创建测试数据和用例
- [ ] 端到端功能测试
- [ ] 性能优化和错误处理

### 第五阶段：文档和部署（1天）
- [ ] 编写用户使用文档
- [ ] 更新 API 文档
- [ ] 部署到生产环境

## 风险和缓解措施

### 技术风险
1. **工具集成复杂度**
   - 风险：自定义工具与 Claude Agent SDK 集成困难
   - 缓解：先实现核心工具，逐步增加功能

2. **数据源连接**
   - 风险：真实数据源连接可能有权限和安全问题
   - 缓解：初期使用模拟数据，后期逐步接入真实数据源

3. **性能问题**
   - 风险：大数据量查询可能导致超时
   - 缓解：实现查询优化、采样和分页机制

### 业务风险
1. **用户体验**
   - 风险：两种项目类型可能造成用户困惑
   - 缓解：清晰的 UI 设计和引导提示

2. **功能范围**
   - 风险：数据分析需求可能超出初期设计
   - 缓解：采用迭代开发，根据反馈逐步完善

## 成功标准
1. 用户可以成功创建数据分析项目
2. AI 能够理解并执行数据分析任务
3. 生成的报告专业且美观
4. 系统稳定，错误处理完善
5. 代码质量高，易于维护和扩展

## 附录

### A. 相关文件清单
- 前端文件（5个）
- 后端文件（9个）
- 新建文件（4个）
- 配置文件（2个）

### B. API 变更
- POST /api/projects/ - 新增 project_type 参数
- 各 Chat API 内部传递 project_type

### C. 数据库变更
- 使用现有 template_type 字段，无需数据库迁移

### D. 依赖项
- Python: sqlparse（SQL 验证）
- Python: aiohttp（异步 HTTP 请求）
- 前端：无新增依赖

---

本方案提供了完整的技术实施路线图，涵盖了从用户界面到后端服务的所有改动点，确保数据分析应用能够无缝集成到 Claudable 平台中。