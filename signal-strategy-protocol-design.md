# 信号策略协议最小设计

## 目标

基于现有 Backtrader 回测系统，最小化补齐 AI 生成复杂策略所缺的能力：

- 交易行情仍然由现有回测配置加载，例如 `symbols = [300059.SZ]`。
- 策略仍然是 Python 代码，仍然运行在 Backtrader 中。
- AI 可以自己读取、理解、计算任意外部数据，并把结果变成交易信号。
- 平台不规范化任意新增数据源，只提供信号接口和交易执行边界。

这个设计只新增两个协议接口：

1. `chatq_signal_init`
2. `chatq_signal_next`

## 最小协议

### chatq_signal_init

`chatq_signal_init` 在回测开始前调用一次。

它负责初始化信号数据，例如：

- 读取创业板指历史数据并计算月K MACD。
- 读取新闻、公告、财务数据并整理成信号表。
- 读取用户提供的 CSV 或其他文件并计算条件。
- 生成后续 `chatq_signal_next` 要使用的内部状态。

平台不要求它返回统一的数据源结构。只要求它返回一个 Python 对象，后续原样传给 `chatq_signal_next`。

### chatq_signal_next

`chatq_signal_next` 在 Backtrader 每个 `next()` 时点调用。

它负责根据当前回测状态返回交易动作。返回值可以是单个动作，也可以是动作列表：

```text
{
  "action": "buy" | "sell" | "close" | "cancel" | "hold",
  "params": {...}
}

[
  {"action": "sell", "params": {...}},
  {"action": "buy", "params": {...}}
]
```

其中：

- `action` 必填。
- `params` 可选。
- `buy`、`sell`、`close` 的 `params` 对齐 Backtrader 同名函数参数。
- `cancel` 的 `params` 使用平台包装参数：`{"ref": order_ref}`。
- `params` 不能包含 `data`。

`buy`、`sell`、`close` 暴露的参数集：

```text
buy(size=None, price=None, plimit=None, exectype=None, valid=None,
    tradeid=0, oco=None, trailamount=None, trailpercent=None, parent=None,
    transmit=True, **kwargs)

sell(size=None, price=None, plimit=None, exectype=None, valid=None,
     tradeid=0, oco=None, trailamount=None, trailpercent=None, parent=None,
     transmit=True, **kwargs)

close(size=None, **kwargs)
```

`cancel` 对应 Backtrader 的 `strategy.cancel(order)`。Backtrader 需要的是 order 对象，但信号协议不暴露 order 对象，因此信号只返回订单 `ref`：

```text
{"action": "cancel", "params": {"ref": 123}}
```

平台负责维护 `order_ref -> Backtrader order` 映射，并把 `data` 注入为当前默认交易 feed：

```text
strategy.buy(data=trade_data, **params)
strategy.sell(data=trade_data, **params)
strategy.close(data=trade_data, **params)
strategy.cancel(open_order_by_ref[ref])
```

## signal_next 输入

`chatq_signal_next` 需要接收一个只读上下文。第一版不直接暴露 Backtrader 对象本身，只暴露从 Backtrader 当前状态提取出的简单快照。

建议包含：

- 当前回测时间。
- 当前交易 bar：
  - `datetime`
  - `open`
  - `high`
  - `low`
  - `close`
  - `volume`
  - `openinterest`
- 当前现金。
- 当前持仓。
  - `size`
  - `price`
  - `market_value`
  - `position_percent`
  - `unrealized_pnl`
- 当前组合净值。
- 未完成订单。
  - `ref`
  - `status`
  - `size`
  - `price`
  - `exectype`
- 自上次调用以来的订单事件。
  - `ref`
  - `status`
  - `is_buy`
  - `created_price`
  - `executed_price`
  - `executed_size`
  - `executed_value`
  - `executed_comm`
- 上一次订单状态。
- 策略参数。
- `chatq_signal_init` 返回的信号状态。

这些数据可以参与信号逻辑。

例如：

> 总市值突破 100 亿，并且当前仓位不足 10%，返回 `buy`，并计算加仓 10% 对应的 `size`。

但上下文是只读的。信号函数不能修改现金、持仓、订单状态，也不能直接下单。

注意：Backtrader 的 `position` 是净持仓，不记录每一笔买入档位。因此“最后一个头寸”“最低买入价头寸”这类分笔持仓信息，不能直接从 `position` 读取。需要由信号逻辑在 `chatq_signal_init` 返回的信号状态中维护，例如根据订单事件更新 `holdings_by_price`，再在 `chatq_signal_next` 中读取 `min(holdings_by_price)`。

这些字段基本来自 Backtrader 的当前策略实例：

- `self.data` / `self.data0`：默认交易 feed。
- `self.data.open[0]`、`high[0]`、`low[0]`、`close[0]`、`volume[0]`、`openinterest[0]`：当前 bar。
- `self.data.datetime.datetime(0)` 或 `date(0)`：当前时间。
- `self.broker.getcash()`：当前现金。
- `self.broker.getvalue()`：当前组合净值。
- `self.getposition(self.data)`：当前交易标的持仓。
- `self.broker.get_orders_open()`：未完成订单。
- `notify_order`：平台记录订单事件和上一次订单状态。

暂不建议把以下 Backtrader 对象直接传给信号函数：

- `broker` 对象。
- `data` feed 对象。
- `order` 对象。
- `position` 对象。

原因是这些对象可变且包含交易能力，直接暴露会模糊“信号只读、平台执行”的边界。

## 平台职责

平台只做最小适配：

1. 继续按现有配置加载默认交易行情。
2. 回测开始前调用 `chatq_signal_init`。
3. 每个 Backtrader `next()` 调用 `chatq_signal_next`。
4. 校验返回值是否合法。
5. 拒绝 `params.data`。
6. 把 `buy`、`sell`、`close`、`cancel` 转成 Backtrader 调用。
7. 让 Backtrader/Broker 决定订单是否成交。

第一版不要新增：

- 多交易 feed 声明。
- 数据源注册表。
- 通用字段规范化。
- 独立信号仓库。
- 复杂审计系统。
- 自定义执行策略 DSL。

## 策略与平台边界

策略控制：

- 信号什么时候发生。
- 返回 `buy`、`sell`、`close`、`cancel` 还是 `hold`。
- 返回哪些 Backtrader 参数，例如 `size`、`price`、`exectype`。
- 是否根据持仓、现金、组合净值、订单状态调整信号。

平台控制：

- 默认交易 feed。
- `data` 参数绑定。
- `cancel` 的 `ref` 到 Backtrader order 对象映射。
- 返回值校验。
- 执行时点规则。
- 平台强规则，例如是否允许做空、是否允许超过现金买入。
- Backtrader/Broker 撮合。
- 回测结果记录。

核心边界：

> 信号可以带订单参数，也可以请求撤单，但信号不是订单；订单是否提交、撤销和成交，由平台和 Backtrader 决定。

## 示例

### 创业板指月K MACD

回测配置仍然只指定交易标的：

```text
symbols = [300059.SZ]
```

`chatq_signal_init`：

- 读取创业板指 `399006.SZ` 数据。
- 聚合成月K。
- 计算 MACD。
- 保存每个月的翻红、翻绿状态。

`chatq_signal_next`：

- 当前时点遇到 MACD 翻红，返回：

```text
{"action": "buy"}
```

- 当前时点遇到 MACD 翻绿，返回：

```text
{"action": "close"}
```

- 其他时间返回：

```text
{"action": "hold"}
```

### 仓位敏感加仓

`chatq_signal_next` 读取只读上下文：

- 当前组合净值。
- 当前持仓。
- 当前价格。
- `chatq_signal_init` 中计算好的市值信号。

如果满足“市值突破 100 亿，并且当前仓位不足 10%”，返回：

```text
{
  "action": "buy",
  "params": {
    "size": 1200
  }
}
```

平台负责绑定 `data`，并交给 Backtrader 判断能否成交。

### 阶梯网格策略验证

这类策略包括：

- 挂限价买单。
- 买单成交后，按成交价挂对应止盈卖单。
- 持仓档位变化后，撤销旧买单并重新挂新的买单。
- 同时维护一个买单和多个卖单。

当前最小协议可以覆盖这类策略，原因是：

- `buy` 带 `price`、`exectype`、`size` 可以表达限价买单。
- `sell` 带 `price`、`exectype`、`size` 可以表达限价卖单。
- `signal_next` 读取持仓、现金、未完成订单，可以计算下一档价格和数量。
- `signal_next` 可以返回动作列表，一次返回止盈卖单和下一档买单。
- `cancel` 可以撤销过时买单。
- 订单事件输入提供成交价、成交数量、订单 ref、买卖方向，用于维护每个持仓档位。

这个策略里的“当前持仓中最低一档买入价”不能依赖 Backtrader 的净持仓 `position`。可行做法是：信号状态维护分笔持仓表，订单成交事件进入 `signal_next` 后，信号逻辑用成交价和成交数量更新分笔持仓，再用其中的最低买入价计算下一档买入价格。

这仍然不引入多交易 feed、数据源注册表或复杂执行 DSL，只是把 Backtrader 已有订单生命周期以只读快照形式暴露给信号逻辑。

## 最小落地步骤

1. 在策略协议中允许策略类定义 `chatq_signal_init` 和 `chatq_signal_next`。
2. 在策略校验中校验这两个函数的返回格式。
3. 在 Backtrader 执行器里增加一个薄包装：调用信号接口，再调用 `buy/sell/close/cancel`。
4. 先只支持单交易标的，也就是现有 `single_symbol`。
5. 用“创业板指月K MACD 翻红买东方财富，翻绿清仓”验收。
