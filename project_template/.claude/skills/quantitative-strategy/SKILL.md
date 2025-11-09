---
name: quantitative-strategy
description: 金融量化交易策略创建及回测
allowed-tools: Read, Grep, Glob, Bash, Write, Edit, WebFetch, WebSearch, TodoWrite, Task
---

# Quantitative Stratogy Skill

## 概述

本Skill用于创建交易策略及其回测。数据获取使用akshare，回测框架使用backtrader，金融指标计算使用TA-Lib.

### 适用场景

当需要创建并测试新的量化交易策略时，使用本技能完成从策略设计到回测分析的全流程。

---

## 工作流程

1. **需求分析**
   - 明确策略类型（趋势跟踪、均值回归、套利等）
   - 确定交易标的（股票、期货、外汇等）
   - 定义时间周期和回测区间
   - 确认风险控制要求

2. **数据获取**
   - 使用 akshare 获取市场数据
   - 支持多种数据源：股票、期货、指数、基金等
   - 数据预处理和清洗
   - 数据格式转换以适配 backtrader

3. **策略设计**
   - 使用 TA-Lib 计算技术指标（MA、MACD、RSI、布林带等）
   - 定义交易信号生成逻辑
   - 设置仓位管理规则
   - 配置风险控制参数

4. **策略实现**
   - 继承 `BaseStrategy` 类（位于 `{project_path}/strategy/base_strategy.py`）
   - 实现 `__init__`、`next` 等核心方法
   - 使用 TA-Lib 或 backtrader 内置指标计算技术指标
   - 使用 `self.buy_signal()` 和 `self.sell_signal()` 发出交易信号
   - 策略文件保存到 `{project_path}/strategy/impls/` 目录
   - 策略文件中只保留策略类定义，不需要测试运行代码

5. **回测执行**
   - 使用 `{project_path}/strategy/run_backtest.py` 脚本执行回测
   - 命令格式：
     ```bash
     python {project_path}/strategy/run_backtest.py <策略文件名> --symbols <股票代码> --start-date <开始日期> --end-date <结束日期> [选项]
     ```
   - 必需参数：
     - 策略文件名（如 `ma_cross_strategy.py`，自动从 impls 目录加载）
     - `--symbols`: 股票代码（逗号分隔，如 "300031,000001"）
     - `--start-date`: 开始日期（格式：YYYYMMDD）
     - `--end-date`: 结束日期（格式：YYYYMMDD）
     - `--output`: 输出文件路径（必须在 {project_path}/data_file/final/ 目录下）
   - 可选参数：
     - `--cash`: 初始资金（默认：100000）
     - `--commission`: 手续费率（默认：0.001）
     - `--params`: 策略参数（JSON格式，如 '{"ma_short":10}'）
   - 使用示例：
     ```bash
     # 基本用法
     python /path/to/strategy/run_backtest.py ma_cross_strategy.py --symbols "300031" --start-date 20240101 --end-date 20241231 --output data_file/final/backtest_result.json

     # 多股票回测
     python /path/to/strategy/run_backtest.py ma_cross_strategy.py --symbols "300031,000001" --start-date 20240101 --end-date 20241231 --output data_file/final/multi_stock_result.json

     # 带策略参数
     python /path/to/strategy/run_backtest.py ma_cross_strategy.py --symbols "300031" --start-date 20240101 --end-date 20241231 --params '{"ma_short":5,"ma_long":20}' --output data_file/final/custom_params_result.json
     ```
   - 注意：确保日期范围足够长，至少要能覆盖策略中最长周期的指标计算（如60日均线需要至少3个月数据）


## 环境和限制

### Python 环境
- **Python 版本**: 3.12

### 已安装的包及其版本
```
akshare                   1.17.76  # 金融数据获取
numpy                     2.3.4    # 数值计算
pandas                    2.3.3    # 数据处理
TA-Lib                    0.6.8    # 技术指标计算
scikit-learn              1.6.1    # 机器学习（可选）
backtrader                1.9.78.123  # 回测框架
```

### 重要约束
1. **仅使用已安装的包**：不要尝试安装新的依赖包
2. **严禁伪造数据**：绝对禁止在没有真实数据的情况下伪造或模拟数据
3. **数据源限制**：仅使用 akshare 作为数据获取工具
4. **代码风格**：遵循 PEP 8 编码规范，保持代码清晰可读

### 技术栈说明

#### akshare 使用
- 支持 A 股、港股、美股等多市场数据
- 提供实时行情、历史数据、财务数据等
- 常用函数：`stock_zh_a_hist()`、`fund_etf_hist_em()` 等

#### backtrader 框架
- 核心组件：Cerebro（引擎）、Strategy（策略）、Data Feed（数据源）
- 支持多种订单类型：市价单、限价单、止损单等
- 内置分析器：SharpeRatio、DrawDown、Returns 等

#### TA-Lib 指标
- 趋势指标：SMA、EMA、MACD、ADX
- 震荡指标：RSI、Stochastic、CCI
- 波动率指标：ATR、Bollinger Bands
- 成交量指标：OBV、AD、ADOSC

---

## 示例代码

```python
import backtrader as bt
import talib
from base_strategy import BaseStrategy

class MACrossStrategy(BaseStrategy):
    """双均线交叉策略"""
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

        # 使用 TA-Lib 计算移动平均线
        if len(close) >= self.p.ma_long:
            close_array = close.get(size=self.p.ma_long)
            self.ma_short = talib.SMA(close_array, timeperiod=self.p.ma_short)[-1]
            self.ma_long = talib.SMA(close_array, timeperiod=self.p.ma_long)[-1]

        # 交易逻辑
        if self.ma_short and self.ma_long:
            if not self.position:
                if self.ma_short > self.ma_long:
                    self.buy_signal()
            else:
                if self.ma_short < self.ma_long:
                    self.sell_signal()
```

---

## 注意事项

1. **数据质量**：确保从 akshare 获取的数据完整无缺失
2. **代码测试**：充分测试策略逻辑的正确性

---


