# ChatQ 平台无关策略协议设计

## 背景

当前项目已经具备策略资产管理、Backtrader 回测、数据集查询和 Job Runtime 定时任务能力。现有回测策略通常是 `backtrader.Strategy` 子类，策略代码依赖 `self.data`、`self.broker`、`self.buy()`、`bt.ind.*` 等 Backtrader API。

如果策略要上线运行，不能把 Backtrader 策略原样放到实盘。实盘运行需要处理真实行情、账户资金、持仓、未成交订单、成交回报、风控、幂等、防重复下单、券商接口和断线恢复。这些职责不应该进入策略代码，也不适合由 Backtrader 作为主运行框架承载。

新的协议目标是：

- 策略代码不依赖 Backtrader。
- 同一份策略可以用于回测、信号观察、模拟盘和实盘。
- Backtrader 只作为回测适配器，负责历史 bar 推进和模拟撮合。
- 运行时由 ChatQ 自己的 runner 负责调度、风控、订单意图、券商适配和状态落库。
- `chatq.sql` 作为策略只读数据服务，在回测和运行时保持一致语义。

## 总体架构

```text
策略源码
  -> chatq_params / chatq_init / chatq_next

回测
  -> ChatQBacktraderAdapter
  -> Backtrader Cerebro/Broker
  -> 回测结果

信号观察
  -> ChatQLiveRunner
  -> 保存 strategy_signal

模拟盘
  -> ChatQLiveRunner
  -> RiskEngine
  -> PaperBroker
  -> 订单/成交/持仓快照

实盘
  -> ChatQLiveRunner
  -> RiskEngine
  -> LiveBrokerAdapter
  -> 真实券商订单/成交/持仓对账
```

核心边界：

> 策略只产生信号，平台负责校验、风控、幂等和执行。信号不是订单；订单是否提交、撤销、成交，由平台和执行适配器决定。

## 策略源码协议

策略源码是一段 Python 代码。新协议不要求定义 `backtrader.Strategy` 子类，而是要求暴露以下函数：

```python
from app.service.strategy.protocol import (
    ChatQBarContext,
    ChatQInitContext,
    ChatQNextResult,
    ChatQState,
)


def chatq_params() -> list[dict]:
    ...

def chatq_init(context: ChatQInitContext) -> ChatQState:
    ...

def chatq_next(context: ChatQBarContext, state: ChatQState) -> ChatQNextResult:
    ...
```

类型注解不是运行时必填项，但建议策略生成器和智能体始终带上。`ChatQInitContext`、`ChatQBarContext`、`ChatQState`、`ChatQNextResult` 是协议字段的机器可读契约，比裸 `dict[str, Any]` 更适合让智能体稳定生成代码。

### chatq_params

`chatq_params` 返回策略参数 schema，用于创建策略版本时沉淀到 `custom_params`。

示例：

```python
def chatq_params():
    return [
        {"name": "fast_period", "label": "短均线周期", "type": "integer", "default": 5},
        {"name": "slow_period", "label": "长均线周期", "type": "integer", "default": 20},
        {"name": "order_size", "label": "下单股数", "type": "integer", "default": 1000},
    ]
```

字段约定：

- `name` 或 `name_en`：参数英文名。
- `label` 或 `name_cn`：展示名。
- `type`：`integer`、`number`、`string`、`boolean`。
- `default`：默认值。
- `required`：可选，默认 `true`。

### chatq_init

`chatq_init` 在一次策略运行启动时调用一次。

在回测中，它在 Backtrader adapter 初始化时调用；在信号观察、模拟盘和实盘中，它在 deployment 首次启动或 state 缺失时调用。

职责：

- 初始化策略内部状态。
- 通过 `context["chatq"].sql(...)` 读取只读数据。
- 基于 `context["history"]` 预计算指标。
- 返回可序列化的 `state`。

约束：

- 返回值必须可以 JSON 序列化，或可以由平台序列化后存储。
- 不允许下单。
- 不允许修改账户、持仓、订单。
- 不允许持有 Backtrader 对象、数据库连接、券商连接等不可序列化运行时对象。

示例：

```python
def chatq_init(context):
    symbol = context["symbols"][0]
    fast = context["params"]["fast_period"]
    slow = context["params"]["slow_period"]
    history = context["history"][symbol]

    close = history["close"]
    ma_fast = close.rolling(fast).mean()
    ma_slow = close.rolling(slow).mean()

    return {
        "last_signal": "none",
        "indicator_cache": {
            "ma_fast": ma_fast.dropna().to_dict(),
            "ma_slow": ma_slow.dropna().to_dict(),
        },
    }
```

### chatq_next

`chatq_next` 在每个策略触发点调用。

在回测中，触发点通常是每根历史 bar 的 `next()`；在运行时，触发点可以是 Job Runtime 调度、行情 bar 到达、人工触发或补偿重跑。

职责：

- 读取 `context` 的当前行情、持仓、资金、未完成订单、订单事件和参数。
- 根据 `state` 维护策略内部状态。
- 返回动作列表和新的 `state`。

返回格式：

```python
{
    "actions": [
        {
            "action": "buy",
            "symbol": "300059.SZ",
            "order_type": "market",
            "size": 1000,
            "price": None,
            "reason": "ma_cross_up",
            "client_signal_id": "optional-idempotency-key"
        }
    ],
    "state": {},
    "logs": []
}
```

兼容简写：

```python
{"action": "hold"}
```

平台会规范化为：

```python
{"actions": [{"action": "hold"}], "state": old_state, "logs": []}
```

## 上下文协议

`context` 是只读上下文字典。策略可以读取上下文，但不能通过上下文修改平台状态。

### InitContext

```python
{
    "mode": "backtest" | "signal" | "paper" | "live",
    "symbols": ["300059.SZ"],
    "timeframe": "1d",
    "params": {},
    "history": {
        "300059.SZ": pandas.DataFrame
    },
    "chatq": ChatQReadOnlyServices
}
```

### BarContext

```python
{
    "mode": "backtest" | "signal" | "paper" | "live",
    "datetime": "2026-08-20T15:00:00",
    "symbols": ["300059.SZ"],
    "current_bars": {
        "300059.SZ": {
            "symbol": "300059.SZ",
            "datetime": "2026-08-20T15:00:00",
            "open": 10.0,
            "high": 10.5,
            "low": 9.8,
            "close": 10.2,
            "volume": 123456.0
        }
    },
    "bars": {
        "300059.SZ": pandas.DataFrame
    },
    "cash": 100000.0,
    "portfolio_value": 105000.0,
    "positions": {
        "300059.SZ": {
            "symbol": "300059.SZ",
            "size": 1000.0,
            "price": 9.8
        }
    },
    "open_orders": [
        {
            "ref": "broker-or-backtest-order-ref",
            "symbol": "300059.SZ",
            "side": "buy",
            "status": "submitted",
            "order_type": "limit",
            "size": 1000.0,
            "price": 10.0
        }
    ],
    "order_events": [
        {
            "ref": "broker-or-backtest-order-ref",
            "symbol": "300059.SZ",
            "side": "buy",
            "status": "filled",
            "price": 9.98,
            "size": 1000.0
        }
    ],
    "params": {},
    "chatq": ChatQReadOnlyServices
}
```

上下文字段保持最小可用：策略只接收生成信号所需的行情、资金、持仓、挂单、订单事件、参数和只读数据服务。平台内部 ID、策略版本 ID、部署 ID、账户快照明细、券商私有字段、订单审计时间、成交金额和费用等非核心属性不进入 `context`；这些信息由平台落库、风控和执行链路自行维护。

## chatq.sql

`context["chatq"].sql(sql)` 是策略可用的只读数据查询接口。它继承当前项目已有的 `self.chatq.sql(sql)` 能力，但从 Backtrader 策略对象迁移到平台无关上下文。

示例：

```python
def chatq_init(context):
    df = context["chatq"].sql("""
        SELECT symbol, trade_date, total_mv
        FROM stock_daily_factor
        WHERE symbol = '300059.SZ'
        ORDER BY trade_date
    """)
    return {"market_value_by_date": dict(zip(df["trade_date"], df["total_mv"]))}
```

语义：

- 回测和运行时都通过同名接口访问数据。
- 返回 `pandas.DataFrame`。
- 只允许读查询。
- 只允许访问平台暴露给策略的数据集。
- SQL 不提供下单、撤单、账户修改能力。
- 策略不能通过 SQL 绕过风控。

建议限制：

- 只允许 `SELECT` 或等价只读查询。
- 禁止 `INSERT`、`UPDATE`、`DELETE`、`DROP`、`ALTER`、`CREATE`、`COPY`、`ATTACH` 等写入或文件访问语句。
- 限制最大返回行数、最大执行时间和最大内存。
- 运行时建议避免在 `chatq_next` 里查询大表；重计算数据应放在 `chatq_init` 或盘前任务中。

回测语义：

- `chatq.sql` 查询的是回测环境暴露的数据集。
- 如果数据包含未来日期，策略必须自行按 `context["datetime"]` 过滤，或由平台提供防未来函数包装。
- 推荐平台在后续版本支持 `context["chatq"].sql_asof(sql, asof=context["datetime"])`，用于统一防止未来函数。

运行时语义：

- `chatq.sql` 查询的是运行环境当前可见的数据集。
- 数据新鲜度由数据同步任务保证。
- 运行时不保证每次查询都是最新交易所实时行情；实时行情应来自 `context["current_bars"]` 或行情服务。

## 动作协议

动作统一放在 `actions` 列表中。

### hold

```python
{"action": "hold", "reason": "no_signal"}
```

### buy

```python
{
    "action": "buy",
    "symbol": "300059.SZ",
    "order_type": "market",
    "size": 1000,
    "price": None,
    "reason": "breakout"
}
```

### sell

```python
{
    "action": "sell",
    "symbol": "300059.SZ",
    "order_type": "limit",
    "size": 1000,
    "price": 12.34,
    "reason": "take_profit"
}
```

### close

```python
{
    "action": "close",
    "symbol": "300059.SZ",
    "size": None,
    "reason": "stop_loss"
}
```

`size` 为空时，平台解释为关闭该 symbol 的全部可用持仓。

### cancel

```python
{
    "action": "cancel",
    "ref": "order-ref",
    "symbol": "300059.SZ",
    "reason": "replace_grid_order"
}
```

### 字段说明

- `action`：必填，`buy`、`sell`、`close`、`cancel`、`hold`。
- `symbol`：除 `hold` 外建议必填；`cancel` 可以只传 `ref`，平台再反查订单。
- `order_type`：`market`、`limit`，第一版只要求这两个。
- `size`：下单数量。A 股实盘适配器应按 100 股整手校验。
- `price`：限价单价格。
- `reason`：策略解释文本，用于审计。
- `client_signal_id`：可选幂等键。未提供时平台根据 deployment、datetime、action、symbol、reason 生成。

平台必须拒绝：

- 未知 action。
- 非法 symbol。
- `size <= 0` 的买卖动作。
- `limit` 单缺少 `price`。
- 策略试图指定 broker account、绕过风控或携带底层券商私有对象。

## 回测接口调用伪代码

Backtrader 回测执行器新增一个薄适配器。策略源码不继承 `bt.Strategy`，由 adapter 继承。

```python
class ChatQBacktraderAdapter(bt.Strategy):
    params = (
        ("strategy_module", None),
        ("chatq_params", None),
        ("symbols", None),
        ("timeframe", None),
        ("history", None),
        ("services", None),
    )

    def __init__(self):
        self.strategy_module = self.p.strategy_module
        self.strategy_state = None
        self.open_order_by_ref = {}
        self.pending_order_events = []
        self.data_by_symbol = {
            data._name: data
            for data in self.datas
        }

        init_ctx = {
            "mode": "backtest",
            "symbols": self.p.symbols,
            "timeframe": self.p.timeframe,
            "params": self.p.chatq_params,
            "history": self.p.history,
            "chatq": self.p.services,
        }

        self.strategy_state = self.strategy_module.chatq_init(init_ctx)

    def next(self):
        current_dt = self.datas[0].datetime.datetime(0)

        context = {
            "mode": "backtest",
            "datetime": current_dt.isoformat(),
            "symbols": self.p.symbols,
            "current_bars": extract_current_bars(self.datas),
            "bars": extract_history_until_current_bar(self.datas),
            "cash": self.broker.getcash(),
            "portfolio_value": self.broker.getvalue(),
            "positions": normalize_positions(extract_positions(self)),
            "open_orders": normalize_open_orders(self.broker.get_orders_open()),
            "order_events": normalize_order_events(self.pending_order_events),
            "params": self.p.chatq_params,
            "chatq": self.p.services,
        }
        self.pending_order_events = []

        raw_result = self.strategy_module.chatq_next(context, self.strategy_state)
        result = normalize_chatq_result(raw_result, old_state=self.strategy_state)
        self.strategy_state = result["state"]

        for action in result["actions"]:
            checked = validate_action(action, mode="backtest")
            if checked["action"] == "hold":
                continue

            if checked["action"] == "buy":
                data = self.data_by_symbol[checked["symbol"]]
                order = self.buy(
                    data=data,
                    size=checked["size"],
                    price=checked.get("price"),
                    exectype=to_backtrader_exectype(checked.get("order_type")),
                )
                self.open_order_by_ref[str(order.ref)] = order

            elif checked["action"] == "sell":
                data = self.data_by_symbol[checked["symbol"]]
                order = self.sell(
                    data=data,
                    size=checked["size"],
                    price=checked.get("price"),
                    exectype=to_backtrader_exectype(checked.get("order_type")),
                )
                self.open_order_by_ref[str(order.ref)] = order

            elif checked["action"] == "close":
                data = self.data_by_symbol[checked["symbol"]]
                order = self.close(
                    data=data,
                    size=checked.get("size"),
                )
                self.open_order_by_ref[str(order.ref)] = order

            elif checked["action"] == "cancel":
                order = self.open_order_by_ref.get(str(checked["ref"]))
                if order is not None:
                    self.cancel(order)

    def notify_order(self, order):
        event = convert_backtrader_order_event(order)
        self.pending_order_events.append(event)

        if is_terminal_backtrader_order(order):
            self.open_order_by_ref.pop(str(order.ref), None)
```

回测引擎外层伪代码：

```python
def execute_backtest(backtest, strategy_version):
    strategy_module = load_chatq_strategy_module(strategy_version.source_code)
    params = merge_param_defaults(strategy_version.custom_params, backtest.config.params)
    history = load_history_frames(backtest.config.symbols, backtest.config)

    cerebro = bt.Cerebro(stdstats=False)
    cerebro.broker.setcash(backtest.config.initial_cash)
    cerebro.broker.setcommission(commission=backtest.config.commission)
    cerebro.broker.set_slippage_perc(backtest.config.slippage)

    for symbol in backtest.config.symbols:
        data = pandas_frame_to_backtrader_feed(history[symbol])
        cerebro.adddata(data, name=symbol)

    services = BacktestChatQServices(
        database_path=settings.database_path,
        asof_guard=True,
        current_datetime_provider=lambda: adapter_current_datetime,
    )

    cerebro.addstrategy(
        ChatQBacktraderAdapter,
        strategy_module=strategy_module,
        chatq_params=params,
        symbols=backtest.config.symbols,
        timeframe=backtest.config.timeframe,
        history=history,
        services=services,
    )

    cerebro.addanalyzer(EquityCurveAnalyzer, _name="equity_curve")
    cerebro.addanalyzer(OrderExecutionAnalyzer, _name="orders")
    executed = cerebro.run()

    return build_strategy_backtest_result(executed[0])
```

## 运行时接口调用伪代码

运行时由 Job Runtime 或行情事件触发。第一版建议先做日线或分钟级定时触发，不做高频事件引擎。

```python
async def execute_strategy_deployment_tick(db, deployment_id, trigger):
    deployment = await load_strategy_deployment(db, deployment_id)
    if not deployment.enabled:
        return ExecutionResult(result_status="skipped", summary="deployment disabled")

    strategy_version = await load_strategy_version(db, deployment.strategy_version_id)
    strategy_module = load_chatq_strategy_module(strategy_version.source_code)
    params = merge_param_defaults(strategy_version.custom_params, deployment.params)

    broker = broker_registry.get(deployment.broker_id)
    market_data = market_data_registry.get(deployment.market_data_source_id)
    services = LiveChatQServices(
        database_path=settings.database_path,
        deployment_id=deployment.id,
    )

    runtime_state = await load_strategy_state(db, deployment.id)
    if runtime_state is None:
        history = await market_data.load_history(
            symbols=deployment.symbols,
            timeframe=deployment.timeframe,
            lookback=deployment.history_lookback,
        )
        init_ctx = {
            "mode": deployment.mode,
            "symbols": deployment.symbols,
            "timeframe": deployment.timeframe,
            "params": params,
            "history": history,
            "chatq": services,
        }
        state = strategy_module.chatq_init(init_ctx)
    else:
        state = runtime_state.state

    account = await broker.get_account_snapshot()
    positions = await broker.get_positions()
    open_orders = await broker.get_open_orders()
    order_events = await load_unconsumed_order_events(db, deployment.id)
    current_bars = await market_data.get_latest_bars(deployment.symbols, deployment.timeframe)
    recent_bars = await market_data.get_recent_bars(
        deployment.symbols,
        deployment.timeframe,
        lookback=deployment.next_lookback,
    )

    context = {
        "mode": deployment.mode,
        "datetime": trigger.scheduled_for.isoformat(),
        "symbols": deployment.symbols,
        "current_bars": current_bars,
        "bars": recent_bars,
        "cash": account["cash"],
        "portfolio_value": account["total_value"],
        "positions": normalize_positions(positions),
        "open_orders": normalize_open_orders(open_orders),
        "order_events": normalize_order_events(order_events),
        "params": params,
        "chatq": services,
    }

    raw_result = strategy_module.chatq_next(context, state)
    result = normalize_chatq_result(raw_result, old_state=state)

    saved_signals = []
    for action in result["actions"]:
        checked = validate_action(action, mode=deployment.mode)
        signal = await save_strategy_signal(
            db,
            deployment_id=deployment.id,
            trigger_id=trigger.instance_id,
            action=checked,
        )
        saved_signals.append(signal)

        if checked["action"] == "hold":
            continue

        risk_result = await risk_engine.check(
            db,
            deployment=deployment,
            action=checked,
            account=account,
            positions=positions,
            open_orders=open_orders,
        )
        if not risk_result.allowed:
            await save_risk_event(db, signal.id, risk_result)
            continue

        intent = await create_order_intent(
            db,
            signal_id=signal.id,
            deployment=deployment,
            normalized_order=risk_result.normalized_order,
            idempotency_key=build_order_intent_key(deployment, trigger, checked),
        )

        if deployment.mode == "signal":
            continue

        if deployment.requires_manual_confirm:
            await mark_order_intent_waiting_confirm(db, intent.id)
            continue

        if deployment.mode == "paper":
            broker_order = await paper_broker.submit_order(intent)
        elif deployment.mode == "live":
            broker_order = await broker.submit_order(intent)
        else:
            raise ValueError(f"unsupported deployment mode: {deployment.mode}")

        await save_broker_order(db, intent.id, broker_order)

    await mark_order_events_consumed(db, deployment.id, order_events)
    await save_strategy_state(db, deployment.id, result["state"])

    return ExecutionResult(
        result_status="completed",
        summary=f"generated {len(saved_signals)} signals",
        payload={"signal_count": len(saved_signals)},
    )
```

## Job Runtime 接入

建议新增 job type：

```text
strategy_deployment_tick
```

调度由 Job Runtime 自有表承载，不在策略部署表重复保存 cron：

```text
job_schedulers.job_type = "strategy_deployment_tick"
job_schedulers.job_id   = strategy_deployments.id
job_schedulers.cron     = 用户配置的运行周期
job_schedulers.payload_json = {}
```

`strategy_deployments` 仍然建议保留。它表示“一个策略运行实体”，承载策略版本、标的、参数、broker、风控、运行状态等配置；`job_schedulers` 只表示“什么时候触发这个实体”。这样手动触发、行情事件触发、暂停恢复和实盘状态管理都不用塞进调度表。

调度实例不需要在 payload 里重复保存 `deployment_id`、`mode` 或 `scheduled_for`。`deployment_id` 来自 `instance.job_id`，`scheduled_for` 来自 `job_instances.scheduled_for`，`mode` 来自部署配置。

手动触发或补偿重跑也使用同一个 job ref：

```json
{
  "reason": "manual_retry"
}
```

注册伪代码：

```python
def register_strategy_deployment_job_runtime_handlers(registry):
    registry.register_instance_factory(
        job_type="strategy_deployment_tick",
        factory=StrategyDeploymentTickInstanceFactory(),
    )
    registry.register_job_executor(
        job_type="strategy_deployment_tick",
        executor=StrategyDeploymentTickExecutor(),
    )
```

执行器伪代码：

```python
class StrategyDeploymentTickExecutor:
    async def execute_job_instance(self, db, *, instance, instance_service):
        payload = instance.trigger_payload_json or {}
        return await execute_strategy_deployment_tick(
            db,
            deployment_id=instance.job_id,
            trigger=StrategyRuntimeTrigger(
                instance_id=instance.id,
                scheduled_for=instance.scheduled_for,
                payload=payload,
            ),
        )
```

## 推荐落库模型

### strategy_deployments

策略部署配置。

```text
id
project_id
strategy_id
strategy_version_id
name
mode: signal | paper | live
enabled
symbols_json
timeframe
params_json
broker_id
market_data_source_id
requires_manual_confirm
risk_config_json
state_json
created_at
updated_at
```

`enabled` 是策略运行层的安全开关；定时调度的创建、更新和删除仍由 `job_schedulers` 管理。

### strategy_signals

每次策略输出的动作。

```text
id
deployment_id
job_instance_id
strategy_version_id
signal_datetime
action_json
status: generated | rejected | converted | ignored
reason
created_at
```

### order_intents

平台准备提交的订单意图。它是风控后的结果。

```text
id
deployment_id
signal_id
idempotency_key
symbol
side
order_type
size
price
status: pending | waiting_confirm | submitted | cancelled | rejected
risk_result_json
created_at
updated_at
```

### broker_orders

券商或模拟盘订单。

```text
id
order_intent_id
broker_id
broker_order_id
symbol
side
order_type
size
price
filled_size
avg_filled_price
status
raw_json
created_at
updated_at
```

### broker_order_events

订单状态和成交事件。

```text
id
deployment_id
broker_order_id
event_type
event_at
payload_json
consumed_at
created_at
```

### account_snapshots / position_snapshots

运行时对账数据。

```text
id
deployment_id
snapshot_at
payload_json
created_at
```

## Backtrader 策略迁移规则

旧策略：

```python
class MyStrategy(bt.Strategy):
    params = (("fast", 5), ("slow", 20), ("size", 1000))

    def __init__(self):
        self.ma_fast = bt.ind.SMA(self.data.close, period=self.p.fast)
        self.ma_slow = bt.ind.SMA(self.data.close, period=self.p.slow)

    def next(self):
        if self.ma_fast[0] > self.ma_slow[0] and not self.position:
            self.buy(size=self.p.size)
        elif self.ma_fast[0] < self.ma_slow[0] and self.position:
            self.close()
```

迁移后：

```python
def chatq_params():
    return [
        {"name": "fast", "label": "短均线", "type": "integer", "default": 5},
        {"name": "slow", "label": "长均线", "type": "integer", "default": 20},
        {"name": "size", "label": "下单数量", "type": "integer", "default": 1000},
    ]


def chatq_init(context):
    return {"last_signal": "none"}


def chatq_next(context, state):
    symbol = context["symbols"][0]
    params = context["params"]
    bars = context["bars"][symbol]
    position = context["positions"].get(symbol, {"size": 0})

    ma_fast = bars["close"].rolling(params["fast"]).mean().iloc[-1]
    ma_slow = bars["close"].rolling(params["slow"]).mean().iloc[-1]

    if ma_fast > ma_slow and position["size"] == 0:
        state["last_signal"] = "buy"
        return {
            "actions": [
                {
                    "action": "buy",
                    "symbol": symbol,
                    "order_type": "market",
                    "size": params["size"],
                    "reason": "ma_fast_above_slow",
                }
            ],
            "state": state,
        }

    if ma_fast < ma_slow and position["size"] > 0:
        state["last_signal"] = "close"
        return {
            "actions": [
                {
                    "action": "close",
                    "symbol": symbol,
                    "reason": "ma_fast_below_slow",
                }
            ],
            "state": state,
        }

    return {"actions": [{"action": "hold", "reason": "no_cross"}], "state": state}
```

迁移映射：

```text
bt.Strategy.params      -> chatq_params()
__init__ 指标声明       -> chatq_init 或 chatq_next 中的 pandas 计算
self.data.close[0]      -> context["current_bars"][symbol]["close"]
self.position.size      -> context["positions"][symbol]["size"]
self.broker.getcash()   -> context["cash"]
self.broker.getvalue()  -> context["portfolio_value"]
self.buy(...)           -> return {"action": "buy", ...}
self.sell(...)          -> return {"action": "sell", ...}
self.close(...)         -> return {"action": "close", ...}
self.cancel(order)      -> return {"action": "cancel", "ref": ...}
self.chatq.sql(sql)     -> context["chatq"].sql(sql)
```

## 分阶段落地

### 第一阶段：协议解析和回测适配

1. 策略协议支持 `chatq_params`、`chatq_init`、`chatq_next`。
2. 策略版本创建时解析 `chatq_params`。
3. 新增 `ChatQBacktraderAdapter`。
4. 回测引擎支持运行平台无关策略。
5. 保留旧 Backtrader 策略协议作为兼容模式。

验收：

- 同一份平台无关策略可以完成 Backtrader 回测。
- 回测结果继续产出收益曲线、订单、持仓快照和指标。
- `context["chatq"].sql(...)` 在回测中可用。

### 第二阶段：信号观察

1. 新增 `strategy_deployments`。
2. 接入 Job Runtime，定时触发 deployment tick。
3. 只保存策略信号，不下单。
4. UI 展示信号历史和运行日志。

验收：

- 策略每天或每分钟定时运行。
- 信号可审计。
- 禁用 deployment 后不再产生新信号。

### 第三阶段：模拟盘

1. 新增 `PaperBroker`。
2. 新增 `order_intents`、`broker_orders`、`broker_order_events`。
3. 新增基础风控。
4. 运行时根据最新行情模拟成交。

验收：

- 信号能转为模拟订单。
- 模拟订单能产生成交事件。
- `order_events` 会在下一次 `chatq_next` 进入上下文。

### 第四阶段：实盘适配

1. 新增真实券商 `LiveBrokerAdapter`。
2. 支持人工确认模式。
3. 支持账户、持仓、委托、成交对账。
4. 增加一键暂停、最大仓位、单票上限、单日亏损熔断。

验收：

- 实盘前可跑 `signal` 和 `paper` 双轨验证。
- 实盘订单有完整审计链路：signal -> risk -> intent -> broker_order -> event -> position。
- 重复触发不会重复下单。

## 设计取舍

第一版不做：

- 高频撮合引擎。
- 复杂事件流 DSL。
- 策略直接访问券商 SDK。
- 策略直接修改数据库。
- 策略返回任意券商私有订单参数。
- 多账户组合净额下单。

第一版优先保证：

- 回测和运行时共用同一份策略。
- 策略与执行解耦。
- `chatq.sql` 只读且语义稳定。
- 信号、风控、订单、成交链路可审计。
- 实盘前有 signal-only 和 paper 过渡层。
