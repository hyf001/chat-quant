# Chat-Quant 量化交易平台

基于 AI 对话的量化交易策略开发与回测平台。

## 项目简介

Chat-Quant 是一个全栈量化交易平台，通过 AI 对话界面帮助用户创建、回测和分析量化交易策略。

### 核心功能

- 🤖 **AI 对话界面** - 通过自然语言与 Claude 交互，创建交易策略
- 📊 **策略回测** - 基于 backtrader 框架的完整回测系统
- 📈 **数据获取** - 集成 akshare，支持 A 股市场数据
- 🔧 **技术指标** - 内置 TA-Lib 技术指标库
- 💾 **项目管理** - 多项目管理，策略版本控制

### 技术栈

**前端**
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- WebSocket 实时通信

**后端**
- FastAPI
- SQLAlchemy (SQLite)
- Claude Agent SDK
- uvicorn

**量化交易**
- backtrader - 回测框架
- akshare - 金融数据
- TA-Lib - 技术指标
- pandas/numpy - 数据处理

## 快速开始

### 环境要求

- Node.js >= 18.0.0
- Python >= 3.10
- npm >= 9.0.0

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd chat-quant
```

2. **安装依赖**
```bash
npm run setup
```

3. **配置环境变量**
```bash
cp .env.example .env
# 编辑 .env 文件，填入必需的配置项
```

必需配置：
- `ANTHROPIC_API_KEY` - Claude API 密钥（从 https://console.anthropic.com/ 获取）

4. **启动开发服务器**
```bash
npm run dev
```

服务将在以下地址启动：
- 前端：http://localhost:3000
- 后端：http://localhost:8080
- API 文档：http://localhost:8080/docs

## 使用指南

### 创建交易策略

1. 在 `project_template/strategy/impls/` 目录下创建策略文件
2. 继承 `BaseStrategy` 类
3. 实现 `__init__()` 和 `next()` 方法

示例策略：
```python
from base_strategy import BaseStrategy
import talib

class MACrossStrategy(BaseStrategy):
    params = (
        ('ma_short', 10),
        ('ma_long', 30),
    )

    def __init__(self):
        super().__init__()
        self.ma_short = None
        self.ma_long = None

    def next(self):
        close = self.datas[0].close

        if len(close) >= self.p.ma_long:
            close_array = close.get(size=self.p.ma_long)
            self.ma_short = talib.SMA(close_array, timeperiod=self.p.ma_short)[-1]
            self.ma_long = talib.SMA(close_array, timeperiod=self.p.ma_long)[-1]

        if self.ma_short and self.ma_long:
            if not self.position:
                if self.ma_short > self.ma_long:
                    self.buy_signal()
            else:
                if self.ma_short < self.ma_long:
                    self.sell_signal()
```

### 运行回测

```bash
cd project_template/strategy
python run_backtest.py ma_cross_strategy.py \
  --symbols "300031" \
  --start-date 20240101 \
  --end-date 20241231 \
  --output data_file/final/result.json \
  --cash 100000 \
  --commission 0.001
```

参数说明：
- `--symbols` - 股票代码（多个用逗号分隔）
- `--start-date` - 回测开始日期（YYYYMMDD）
- `--end-date` - 回测结束日期（YYYYMMDD）
- `--output` - 结果输出路径
- `--cash` - 初始资金（可选，默认 100000）
- `--commission` - 手续费率（可选，默认 0.001）
- `--params` - 策略参数（可选，JSON 格式）

## 开发命令

```bash
# 开发
npm run dev              # 启动前后端
npm run dev:web          # 仅启动前端
npm run dev:api          # 仅启动后端

# 数据库
npm run db:reset         # 重置数据库
npm run db:backup        # 备份数据库

# 清理
npm run clean            # 清理构建产物
```

## Docker 部署

```bash
# 构建镜像
docker build -f docker/Dockerfile -t chat-quant:latest .

# 运行容器
docker run -d \
  --name chat-quant \
  -p 3000:3000 \
  -p 8000:8000 \
  -v /path/to/data:/app/data \
  chat-quant:latest
```

详细部署文档见 `docker/README.md`

## 项目结构

```
chat-quant/
├── apps/
│   ├── web/              # Next.js 前端
│   └── api/              # FastAPI 后端
├── project_template/     # 策略项目模板
│   └── strategy/         # 策略代码
│       ├── base_strategy.py      # 策略基类
│       ├── strategy_runner.py    # 回测执行器
│       ├── run_backtest.py       # 回测脚本
│       └── impls/                # 策略实现
├── components/           # React 组件
├── contexts/            # React 上下文
├── scripts/             # 开发脚本
├── docker/              # Docker 配置
└── data/                # 数据目录
    ├── cc.db            # SQLite 数据库
    └── projects/        # 项目文件
```

## 环境变量

| 变量名 | 必需 | 默认值 | 说明 |
|--------|------|--------|------|
| ANTHROPIC_API_KEY | ✅ | - | Claude API 密钥 |
| API_PORT | ❌ | 8080 | 后端服务端口 |
| DATABASE_URL | ❌ | sqlite:///data/cc.db | 数据库连接 |
| PROJECTS_ROOT | ❌ | ./data/projects | 项目存储目录 |
| CLAUDE_CODE_MODEL | ❌ | claude-sonnet-4-5-20250929 | Claude 模型 |

完整配置见 `.env.example`

## 许可证

[添加许可证信息]

## 贡献

欢迎提交 Issue 和 Pull Request！
