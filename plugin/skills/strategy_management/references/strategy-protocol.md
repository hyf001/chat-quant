# 策略源码协议与框架

## 使用框架

Chat-Quant 策略源码使用平台无关策略协议。策略文件不继承、不导入 `backtrader`，而是定义模块级 `chatq_params()`、`chatq_init(context)`、`chatq_next(context, state)`。Backtrader 只作为后端回测适配器，策略源码本身不感知 Backtrader。

策略源码只负责读取只读上下文并返回信号动作。行情、broker、手续费、滑点、资金、参数注入和结果收集由 Chat-Quant 回测系统提供。

## 源码基本要求

- 源码必须定义 `chatq_init(context)` 和 `chatq_next(context, state)`。
- `chatq_params()` 可选，用于声明参数 schema。
- `chatq_init(context)` 返回可序列化状态字典，不允许下单。
- `chatq_next(context, state)` 返回 `{"actions": [...], "state": state}`。
- 参数通过源码协议注册，策略内部通过 `context["params"]` 使用。
- 不要在源码中维护外部 API key、数据库连接或行情下载逻辑。
- 不要导入 `backtrader`，不要定义 `bt.Strategy` 子类，也不要调用 `order_target_percent` 这类 Backtrader API。

## Context 字段

`chatq_init(context)` 可读取：

- `context["mode"]`：运行模式，回测时为 `backtest`。
- `context["symbols"]`：本次策略运行的交易标的列表。
- `context["timeframe"]`：周期，目前回测只支持 `1d`。
- `context["params"]`：参数值，包含 `chatq_params()` 注册参数的默认值和回测覆盖值。
- `context["history"]`：完整历史行情，按 symbol 映射为 pandas DataFrame。
- `context["chatq"]`：只读平台服务，目前主要用于 `context["chatq"].sql(sql)`。

`chatq_next(context, state)` 每根 bar 调用一次，可读取：

- `context["datetime"]`：当前 bar 时间，ISO 字符串。
- `context["current_bars"][symbol]`：当前 bar，包含 `open/high/low/close/volume`。
- `context["bars"][symbol]`：截至当前 bar 的历史窗口 DataFrame。
- `context["cash"]`：当前可用现金。
- `context["portfolio_value"]`：当前组合总权益。
- `context["positions"]`：当前持仓，按 symbol 映射，字段含 `size`、`price`。
- `context["open_orders"]`：未完成订单列表。
- `context["order_events"]`：上一根 bar 以来的订单事件。
- `context["params"]`：参数值。
- `context["chatq"]`：只读平台服务。

## 动作返回协议

`chatq_next` 返回的 `actions` 支持：

- `{"action": "hold"}`：无动作。
- `{"action": "buy", "symbol": "...", "size": 100}`：买入指定数量。
- `{"action": "sell", "symbol": "...", "size": 100}`：卖出指定数量。
- `{"action": "close", "symbol": "..."}`：清仓该标的；也可带 `size` 部分平仓。
- `{"action": "cancel", "ref": "..."}`：撤销未完成订单。

买卖默认是市价单。限价单写：

```python
{"action": "buy", "symbol": symbol, "size": size, "order_type": "limit", "price": limit_price}
```

协议没有 `target_percent` 动作；需要目标仓位时，策略应根据 `portfolio_value`、当前价格和当前持仓换算出本次 `buy`/`sell` 的 `size`。

## 读取平台数据集

交易标的行情仍由回测配置加载，策略通过 `context["current_bars"]` 读取当前 bar，通过 `context["bars"]` 读取历史窗口。若策略需要读取指数、财务、公告、新闻等已暴露给智能体的补充信号数据集，可在策略中调用 `context["chatq"].sql(sql)`，返回 pandas DataFrame。

- `context["chatq"].sql` 只用于查询平台已暴露的补充信号数据集，不能连接外部 API、数据库或文件。
- 一般不要用 `context["chatq"].sql` 加载股票交易行情；交易标的行情由回测引擎提供。
- 写 SQL 前先按 [dataset-api.md](dataset-api.md) 查询真实数据集、字段和口径，不要猜视图名或字段名。
- SQL 必须是只读 SELECT。
- 查询结果可以在 `chatq_init` 中二次计算后保存为策略状态，在 `chatq_next` 中按当前 bar 决策。

示例：读取指数信号数据生成日期信号，交易标的行情仍走回测配置。

```python
from app.service.strategy.protocol import ChatQBarContext, ChatQInitContext, ChatQNextResult, ChatQState


def chatq_init(context: ChatQInitContext) -> ChatQState:
    frame = context["chatq"].sql(
        "SELECT signal_date, is_bullish FROM index_event_signal "
        "WHERE index_symbol = '399006.SZ' ORDER BY signal_date"
    )
    buy_dates = {
        value.date().isoformat() if hasattr(value, "date") else str(value)
        for value in frame.loc[frame["is_bullish"], "signal_date"]
    }
    return {"buy_dates": sorted(buy_dates)}


def chatq_next(context: ChatQBarContext, state: ChatQState) -> ChatQNextResult:
    symbol = context["symbols"][0]
    today = context["datetime"][:10]
    position = context["positions"].get(symbol, {"size": 0})
    if position["size"] == 0 and today in state["buy_dates"]:
        close = context["current_bars"][symbol]["close"]
        cash = context["cash"] * 0.95
        size = int(cash // close)
        if size > 0:
            return {"actions": [{"action": "buy", "symbol": symbol, "size": size}], "state": state}
    if position["size"] > 0 and today not in state["buy_dates"]:
        return {"actions": [{"action": "close", "symbol": symbol}], "state": state}
    return {"actions": [{"action": "hold"}], "state": state}
```

## 参数注册协议

推荐定义模块级 `chatq_params()`：

```python
def chatq_params():
    return [
        {"name": "fast_period", "type": "integer", "default": 20, "label": "短期均线周期"},
        {"name": "slow_period", "type": "integer", "default": 60, "label": "长期均线周期"},
        {"name": "enabled", "type": "boolean", "default": True, "label": "启用过滤"},
    ]
```

每个参数支持：

- `name` 或 `name_en`：英文参数名，必须能作为 Python 标识符使用。
- `type`：`integer`、`number`、`string`、`boolean`。
- `default`：默认值，类型必须与 `type` 匹配。
- `label` 或 `name_cn`：中文展示名。

后端会从源码中解析参数，并保存为策略版本的参数快照。创建策略或编辑策略时不要手动传参数 schema。

## 策略模式

策略创建时需要指定策略模式，例如 `single_symbol`、`multi_symbol`、`portfolio`、`universe_selection`。编辑已有策略源码时，`update_strategy` 未传 `strategy_mode` 会沿用当前版本的策略模式。回测时 `run_backtest` 会从当前版本或指定版本推断策略模式，不要在回测命令里传策略模式。

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
