# 策略源码协议与框架

## 使用框架

Chat-Quant 策略源码使用 `backtrader` 框架。策略文件应定义一个 `backtrader.Strategy` 子类，由后端加载并交给 Backtrader 回测引擎执行。

策略源码只负责交易逻辑，不负责拉取行情、不负责实盘下单。行情、broker、手续费、滑点、资金、参数注入和结果收集由 Chat-Quant 回测系统提供。

## 源码基本要求

- 源码必须定义且只定义一个可执行的 `backtrader.Strategy` 子类。
- 策略逻辑优先写在 Backtrader 生命周期方法中，例如 `__init__`、`next`、`notify_order`、`notify_trade`。
- 参数通过源码协议注册，策略内部通过 `self.p.<param_name>` 使用。
- 不要在源码中维护外部 API key、数据库连接、行情下载逻辑或实盘交易逻辑。

## 读取平台数据集

交易标的行情仍由回测配置加载，策略中通常只用 `self.datas[0]` 访问当前交易标的的前复权行情。若策略需要读取指数、财务、公告、新闻等已暴露给智能体的补充信号数据集，可在策略中调用 `self.chatq.sql(sql)`，返回 pandas DataFrame。

- `self.chatq.sql` 只用于查询平台已暴露的补充信号数据集，不能连接外部 API、数据库或文件。
- 一般不要用 `self.chatq.sql` 加载股票交易行情；交易标的行情由回测引擎提供。
- 写 SQL 前先按 [dataset-api.md](dataset-api.md) 查询真实数据集、字段和口径，不要猜视图名或字段名。
- SQL 必须是只读 SELECT。
- 查询结果可以在 `__init__` 中二次计算后保存为策略状态，在 `next` 中按当前 bar 决策。

示例：读取指数信号数据生成日期信号，交易标的行情仍只走 `self.datas[0]`。

```python
import backtrader as bt


class GeneratedStrategy(bt.Strategy):
    def __init__(self):
        frame = self.chatq.sql(
            "SELECT signal_date, is_bullish FROM index_event_signal "
            "WHERE index_symbol = '399006.SZ' ORDER BY signal_date"
        )
        self.buy_dates = {
            value.date().isoformat() if hasattr(value, "date") else str(value)
            for value in frame.loc[frame["is_bullish"], "signal_date"]
        }

    def next(self):
        today = self.datas[0].datetime.date(0).isoformat()
        if not self.position and today in self.buy_dates:
            self.buy()
        elif self.position and today not in self.buy_dates:
            self.close()
```

## 参数注册协议

推荐在策略类上定义 `chatq_params()`：

```python
import backtrader as bt


class GeneratedStrategy(bt.Strategy):
    @classmethod
    def chatq_params(cls):
        return [
            {"name": "fast_period", "type": "integer", "default": 20, "label": "短期均线周期"},
            {"name": "slow_period", "type": "integer", "default": 60, "label": "长期均线周期"},
            {"name": "enabled", "type": "boolean", "default": True, "label": "启用过滤"},
        ]

    def __init__(self):
        close = self.datas[0].close
        self.fast_ma = bt.ind.SMA(close, period=self.p.fast_period)
        self.slow_ma = bt.ind.SMA(close, period=self.p.slow_period)
```

每个参数支持：

- `name` 或 `name_en`：英文参数名，必须能作为 Python 标识符使用。
- `type`：`integer`、`number`、`string`、`boolean`。
- `default`：默认值，类型必须与 `type` 匹配。
- `label` 或 `name_cn`：中文展示名。

后端会从源码中解析参数，并保存为策略版本的参数快照。创建策略或编辑策略时不要手动传参数 schema。

## 策略模式

策略创建时需要指定策略模式，例如 `single_symbol`、`multi_symbol`、`portfolio`、`universe_selection`。编辑已有策略源码时，`update_strategy` 未传 `strategy_mode` 会沿用当前版本的策略模式。回测时 `run_backtest` 会从当前版本或指定版本推断策略模式。

单只股票策略使用 `single_symbol`，回测 `config.symbols` 中应只有一个标的。

## 回测参数覆盖

运行回测时可以覆盖源码协议注册过的参数：

```json
{
  "params": {
    "fast_period": 20,
    "slow_period": 60
  }
}
```

只能覆盖已注册参数。未在源码协议中声明的参数会被后端拒绝。
