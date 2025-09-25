# 金融数据策略开发工作流

基于LangGraph框架实现的金融策略开发工作流引擎，集成金融数据查询、策略开发和策略回测功能。

## 🚀 功能特性

- **📊 金融数据查询**: 支持股票、加密货币、外汇等多种金融数据获取
- **🤖 智能策略生成**: 基于自然语言描述生成量化交易策略
- **📈 策略回测分析**: 全面的策略性能评估和风险分析
- **💬 自然语言处理**: 智能理解用户需求，无需编程知识
- **🔄 智能工作流**: 基于LangGraph的状态管理和流程控制
- **🎯 API接口**: 提供简洁的工作流执行接口

## 📁 项目结构

```
chat-quant/
├── src/
│   ├── agents/              # AI Agent实现
│   │   ├── data_query_agent.py    # 数据查询Agent
│   │   ├── strategy_agent.py      # 策略生成Agent
│   │   └── backtest_agent.py      # 回测分析Agent
│   ├── graph/               # LangGraph核心组件
│   │   ├── state.py              # 状态定义
│   │   ├── nodes.py              # 节点实现
│   │   └── tools.py              # 工具函数
│   ├── workflow/            # 工作流实现
│   │   └── financial_workflow.py # 金融工作流
│   ├── utils/               # 工具模块
│   │   └── error_handler.py      # 错误处理
│   ├── config/              # 配置管理
│   └── cli.py               # 命令行界面
├── main.py                  # 主入口文件
├── requirements.txt         # 依赖包列表
└── README.md               # 项目说明
```

## 🛠️ 安装与配置

### 1. 环境要求

- Python 3.8+
- 支持LangChain和LangGraph的环境

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 环境配置

项目默认使用豆包模型，你也可以配置其他LLM服务：

```python
# 在 src/cli.py 中修改API配置
os.environ['OPENAI_API_KEY'] = "your-api-key"
os.environ['OPENAI_BASE_URL'] = "your-api-base-url"
```

## 🚀 使用方法

### 基本用法

```python
from src.cli import create_workflow

# 创建工作流实例
workflow = create_workflow()

# 执行查询
result = workflow.execute_workflow("查询苹果公司2023年的股价数据")

# 处理中断（如需要用户确认）
if result.get("needs_human_input"):
    result = workflow.continue_workflow("用户反馈")

# 获取工作流状态
state = workflow.get_workflow_state()

# 重置会话
workflow.reset_session()
```

### 使用示例

#### 数据查询
```python
result = workflow.execute_workflow("查询苹果公司2023年的股价数据")
```

#### 策略开发
```python
result = workflow.execute_workflow("基于移动平均线开发一个交易策略")
```

#### 综合任务
```python
result = workflow.execute_workflow("我想开发一个基于MACD的股票交易策略，请帮我完成数据获取、策略编写和回测分析")
```

### 运行示例

```bash
python example_usage.py
```

## 🏗️ 架构设计

### 工作流图

系统基于以下流程图实现：

```
start → 协调节点 → plan → human调整plan → Agent查数 → Agent生成策略 → human回测参数 → Agent回测 → end
```

### 核心组件

1. **协调节点**: 判断用户需求，决定下一步操作
2. **计划节点**: 生成执行计划，供用户确认
3. **数据查询Agent**: 处理金融数据获取请求
4. **策略生成Agent**: 基于数据和需求生成交易策略
5. **回测分析Agent**: 执行策略回测和性能分析

### 状态管理

使用LangGraph的状态管理机制，维护以下关键状态：

- `financial_data`: 金融数据
- `strategy`: 交易策略
- `backtest_result`: 回测结果
- `workflow_step`: 当前工作流步骤
- `needs_human_input`: 是否需要人工输入

## 🔧 扩展开发

### 添加新的数据源

在 `src/graph/tools.py` 中扩展 `get_financial_api_details` 函数：

```python
api_details = {
    "new_data_source": {
        "description": "新数据源描述",
        "parameters": {...},
        "example": "...",
        "returns": "..."
    }
}
```

### 添加新的Agent

1. 在 `src/agents/` 目录下创建新的Agent文件
2. 继承基础Agent类并实现核心逻辑
3. 在工作流中添加对应的节点和路由

### 自定义策略模板

在策略生成Agent中添加预定义的策略模板，提高生成质量。

## 🐛 错误处理

系统包含完善的错误处理机制：

- **节点级错误处理**: 捕获节点执行异常
- **Agent级错误处理**: 处理AI Agent执行失败
- **工具级错误处理**: 处理工具调用异常
- **工作流恢复**: 自动错误恢复和状态修复

## 📊 性能优化

- **异步处理**: 支持异步工具调用
- **状态缓存**: 避免重复计算
- **错误重试**: 自动重试机制
- **内存管理**: 对话历史管理

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交代码变更
4. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证。

## 🆘 技术支持

如有问题或建议，请提交 Issue 或联系开发团队。

---

**注意**: 这是一个演示项目，生产环境使用需要连接真实的金融数据API和回测引擎。