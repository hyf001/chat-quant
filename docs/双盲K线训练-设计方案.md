# 双盲 K 线训练（Phase 1）设计方案

> 范围：Chat-Quant 现有架构（FastAPI + DuckDB 数据集 + React 工作台 + Electron 桌面端）之上的新增模块。
> 本期只做**日线单标的训练闭环**。指标与移动平均线、A 股撮合规则层、题库均不在本期（见 §2.3）。
> 本文只做设计与落地规划，不改动现有代码语义。

---

## 1. 目标与语义

### 1.1 什么是"双盲"

参考产品（爆竹 K 线训练助手）的玩法是"随机标的 + 逐根揭示 + 即时买卖 + 结算收益"。它有效的前提是把两类先验知识屏蔽掉：

| 盲项 | 屏蔽内容 | 解决的问题 |
| --- | --- | --- |
| 标的盲 | 不显示股票代码 / 名称 / 所属板块 | 避免"这是茅台 / 这是妖股，它后面涨了"的身份记忆 |
| 时间盲 | 不显示真实日期 / 年份 | 避免"我记得 2024 年 9 月那波怎么走"的行情记忆 |

剩下考验的才是"看图 + 决策 + 纪律"。**双盲必须在服务端强制，而不是前端隐藏。**

### 1.2 与现有能力的关系

| 现有能力 | 与训练的关系 |
| --- | --- |
| 策略回测（Backtrader + chatq protocol） | 验证**规则**，跑完才看结果；训练验证**人**，逐根给反馈 |
| 行情预览（`StockKlineDialog`） | 只读浏览，已知标的与日期；训练是未知 + 可交互下单 |
| 模拟盘 | 用实时行情，标的不盲、时间不盲、无法重复 |

训练与策略模块之间只有一条产品级通路：训练沉淀的规则 → 生成策略草稿 → 回测验证（后者属后续阶段）。

---

## 2. 本期范围

### 2.1 三条范围决定

| 决定 | 本期口径 | 影响 |
| --- | --- | --- |
| **不考虑指标与移动平均线** | 主图只有 K 线 + 成交量（成交量是 K 线附属信息，非指标计算）；不做 MA / BOLL / MACD / KDJ / RSI，服务端不做任何指标计算 | 前端只有主图 + B/S 标记 + 价格线；`/reveal` 响应不含 `ind` 字段 |
| **撮合结算全交给 backtrader** | 不写训练账本、不写 A 股规则层；成交、费用、持仓、权益全部由 `BackBroker` 与 analyzers 产生 | 结算口径是 backtrader 的"通用多资产"口径，接受 §2.4 的已知偏差 |
| **不做题库** | 开局即时随机切片，不建题库表、不做难度分档 / 去重 / 每日一局 | 出题完全随机；题面重复由后续阶段处理 |

### 2.2 本期交付

- 共享引擎宿主抽取（`chatq_engine/backtrader_host.py`）+ 回测 golden 基线（见 §4.3、§9）。
- 训练适配器 `train_adapter.py`：`next()` 阻塞等人工信号 → 翻译成 `ChatQAction` → 交给 backtrader 撮合 → 输出账户与成交。**K 线不由引擎产出**：service 按 `cursor` 从切片里取当前这根，脱敏后返回前端（见 §4.2、§5.2）。
- 切片与脱敏：贴着数据末端切出连续两段（warmup 展示段固定 180 根 + 训练段 N 随机 60~180 根）；`symbol` / 日期照常入库，训练期响应不带这些字段、X 轴用序号（见 §5.1、§5.2）。
- 会话与引擎管理：进程内注册表、空闲回收、信号历史 replay 重建。
- 日线单标的闭环：开局 → 逐根揭示 → 买入 / 卖出 / 观望 → `finish` 揭晓与单局报告。
- 局列表（增量）：`GET /api/training/sessions?project_id=` 返回项目下的会话摘要（状态 / 进度 / 初始资金 / 用时），列表页「新建训练」弹窗收口开局表单；进度的游标由 `training_events` 行数得出，不重建引擎（见 §5.6）。
- 当日分时（增量）：双击任意一根**已揭示**的日线，弹出那一根当天的分钟走势（分时线 + 均价线 + 昨收基准 + 分钟成交量），见 §5.7。
- 前端 `modules/training/*`：K 线主图（B/S 标记 + 最新价格线）、下单面板、统计栏、报告弹窗。

### 2.3 不在本期范围

指标与指标面板、分时（1 分钟）模式与周 / 月 / 5 分周期切换、T+1 与涨跌停与整手与印花税等 A 股规则层、题库与难度分层与每日一局、训练档案 / 段位（列表只做到"局"这一层，不做档案聚合）、心得、AI 复盘、策略沉淀、多标的候选模式、限时模式。

其中"分时"的边界：**以分钟为推进单位的训练模式**（含周 / 月 / 5 分周期切换）仍然不在本期；本期加的只是"回看已揭示那一根的日内走势"这一层只读浏览（§5.7），推进单位始终是日线。

### 2.4 本期的已知偏差（有意接受，不是遗漏）

1. 撮合是 backtrader 的通用多资产口径：**无 T+1、无涨跌停、无一字板否决、无整手（broker 不强制 100 股，训练侧比例换算后向下取整成整数股）、无印花税 / 过户费 / 最低佣金**。
2. 决策依据只有 K 线形态与成交量，信息量少于参考产品（它带 5 个指标面板）。
3. 出题完全随机：难度不可控，同一标的 / 窗口可能重复出现。本期只保留一个最低限度过滤（除权窗口）；停牌 / 缺 bar 不做过滤，照缺失训练。切片终点又固定为数据末端，训练段总是"最近行情"，题面重复与记忆泄露的风险比随机终点更高（见 §5.1、§10）。
4. 结算统计默认不落库：`finish` 一次性返回；进程重启后靠 `training_events` 的信号历史 replay 复算。

---

## 3. 现状与约束

### 3.1 数据（已实测）

| 视图 / 数据集 | 覆盖 | 训练用途 |
| --- | --- | --- |
| `a_stock_daily_price_unadjusted` | 5,571 只，2021-08-13 ~ 2026-09-11，6,842,735 行 | **本期唯一价格来源**（见 §3.4 的复权约束） |
| `a_stock_daily_adjust_factor` | 复权因子 | 排除窗口内除权的切片 |
| `a_stock_snapshot_info` | symbol + name | 标的名称（仅服务端，用于揭晓） |
| `a_stock_minute_price` / `a_index_daily_price` | 1 分钟（2026-08-03 ~ 2026-09-14）；指数日线 | 本期不用（分时属后续；基准暂不做） |

### 3.2 可复用的后端骨架

- 服务层约定：`XxxService` + `XxxError(error_code, message, status_code, detail)`，样板见 `service/market/stock_preview.py`。
- DuckDB 查询：`DuckDBViewStore` + `duckdb_dataset_path(get_settings().database_path)`。
- 回测引擎：`service/backtest/backtrader.py`，公共符号只有 `BacktraderStrategyBacktestEngine`（`service/backtest/__init__.py:1`、`service/backtest/service.py:26`），其余（`_ChatQBacktraderAdapter`、`_load_market_data_feed`、4 个 analyzer）都是模块内私有且**外部零引用**——这是可以安全抽取共享宿主的前提。
- 策略协议：`service/strategy/protocol.py` 的 `ChatQAction` / `ChatQBarContext`，人工信号与策略信号共用同一形状。
- 异步与线程先例：`service/python_execution.py:139`（`loop.run_in_executor` + `asyncio.wait_for` + `ThreadPoolExecutor`）。
- SSE 先例：`api/v1/chat_api.py:39`（`StreamingResponse` + `text/event-stream`）与前端 `shared/api/client.ts:1060`。

### 3.3 可复用的前端骨架

- 无路由库：`shared/routes.ts` 的 `PrimaryRoute` + `WorkbenchPage` 的 `routePaths` + 分支渲染；页面模块放 `modules/<module>/`。
- 图表：`shared/components/charts/LightweightKlineChart.tsx`（lightweight-charts v5）已支持 K 线 + 成交量 + `markers`（B/S）+ `priceLines`（最新价格线）。

### 3.4 三条会影响设计的约束

1. **前复权视图含未来函数**：`a_stock_daily_price_pre_adjusted` 的定义是 `price * factor / latest_factor`，`latest_factor` 取全表最新因子，天然泄露未来且除权日会重写历史价 → 训练禁用该视图。
2. **服务端是 2 个 worker 进程**：`deploy/2_deploy.sh:92-95` 为 `gunicorn --workers 2 --worker-class uvicorn.workers.UvicornWorker`。内存中的训练引擎只属于启动它的进程，跨 worker 请求会丢失会话 → 本期把部署改为 `--workers 1`（见 §4.3、§9.1）。
3. **回测引擎缺少数字级测试基线**：`apps/api/tests/test_backtests_api.py:144` 端到端跑真引擎，但只断言结构（`final_value > 0`、`annual_return_pct is not None`），重构抓不住数字漂移 → 抽取宿主前必须先补 golden 用例。

---

## 4. 架构：一个 backtrader 引擎 + 两个适配器

### 4.1 分层

```
前端  modules/training/*  (K 线主图 + 下单面板 + 统计栏 + 报告)
                │ /api/training/*
API   api/v1/training_api.py           薄层，错误映射
服务  service/training/
        service.py          会话生命周期编排 + 揭示 bar（按 cursor 读切片）+ 写 training_events + 组装响应
        slice_loader.py     末端切片（180 根展示段 + 随机 N）+ 过滤 + point-in-time 归一化
        masking.py          出口脱敏：字段白名单 + 序号轴
        train_adapter.py    训练适配器：阻塞取信号 + 提交 + 在结算点吐出账户快照（不发布 K 线、不落库）
        transport.py        信号传输抽象：动作下发 + 结算点状态回报（本期内存实现）
        engine_manager.py   进程内会话注册表 + 空闲回收 + replay 重建
        recycler.py         定时回收：把已经自退的引擎句柄从注册表摘掉
共享  service/chatq_engine/
        backtrader_host.py  cerebro 装配 + 策略基类 + analyzers
        metrics.py          收益 / 回撤 / Sharpe / 胜率口径
回测  service/backtest/    BacktestAdapter + BacktraderStrategyBacktestEngine（公共入口不变）
存储  SQLite（训练会话 + 信号历史） · DuckDB + Parquet（只读行情）
```

依赖方向：`backtest → chatq_engine`、`training → chatq_engine`；**`training` 不 import `backtest`**。
这样可以避免"训练直接 import 回测模块的私有符号、回测一重构训练就碎"。

### 4.2 共享宿主的 3 个接缝

```python
class ChatQBacktraderStrategyBase(bt.Strategy):
    def next(self):
        ctx = self.build_context()                   # 共享：current_bars / history / positions / open_orders
        actions = self.next_actions(ctx)             # 接缝① 回测→把 chatq_next 的 actions 原样返回；训练→阻塞等人工动作（0 或 1 条）
        for action in actions:
            self.submit_action(action)               # 接缝② 回测/训练→统一走 broker（本期不自研账本）
        self.on_bar_settled(ctx, actions)            # 接缝③ 回测→no-op；训练→在结算点把 broker 快照（现金 / 权益 / 持仓 / 本根成交）交给 transport
```

**训练侧的接缝①②在 `next_open` 里**（回测保持上面的 `next` 不变）：训练开 `cheat_on_open`，
适配器把"阻塞取点击 + 提交"挪到 `next_open`（`prenext_open` / `nextstart_open` / `next_open`
三件套都指向它，保证每根恰好一次），`next` 只留接缝③的发布。于是点击在本根**开盘前**进入
broker、在本根 close 成交、`notify_order` 也在本根交付——结算点快照给出去时这一笔已经落地。

- **引擎里没有"把 K 线发给用户"这件事。** 揭示是 service 的读操作：按 `cursor` 从开局那份切片里取"下一根"，走 `masking` 后返回前端（§5.1、§5.2）。接缝③交出去的是**账户快照与成交回报**，不是 frame / candle。引擎不碰 K 线序列、不碰脱敏、不落库、不认识 `training_events` 这张表。
- **落库与审计也在 service**：请求进来先校验 `seq` → 写一条 `training_events`（这就是"人工信号历史"）→ 把动作交给引擎等结算点 → 组装响应（bar 来自切片 + 账户来自引擎）。空闲回收后的 replay 同样由 service 驱动：按 `seq` 顺序把事件喂回引擎的动作通道重跑（§5.4、§10）。
- **两侧靠同一个下标对齐**：service 认为"当前决策根 = `warmup_bars + cursor - 1`"（都已揭示），本次要揭示的是第 `warmup_bars + cursor` 根；引擎在同一根的 `next_open` 里收到动作、当场提交，broker 按**这一根的 close** 成交（`coc`），`notify_order` 也落在这一根，接缝③随之把成交后的账户交出去。对不上就靠 `seq` 校验挡掉（409，§5.4）。所以成交口径是确定的：**你看着第 t 根按的买入，成交价 = 第 t+1 根的 close**（滑点为 0 时；滑点打开时按比例向不利方向偏移，§5.3、§9.2 有断言）。成交与结算点在同一个响应里，不存在"等下一根开盘"的挂单，账户字段全部是 backtrader 的值。
- 接缝①让**人工信号与策略信号共用同一条 `ChatQAction` 通道**：回测侧就是把 `chatq_next` 的 actions 原样返回（等价于现状 `backtrader.py:84-113` 自己取 actions 再下单），`None` 与空列表都归一成 `[]`——这是"回测行为零漂移"的前提。
- 接缝②本期两侧都走 backtrader 的 `broker.buy/sell/close`（§2.1 决定），差异只在仓位换算（训练侧传比例，见 §5.3）。
- 接缝③是训练唯一的"出口"，且只载 broker 状态；回测侧零感知。

### 4.3 文件改动清单

新增：

- `apps/api/app/service/chatq_engine/{__init__.py,backtrader_host.py,metrics.py}`
- `apps/api/app/service/training/{__init__.py,service.py,slice_loader.py,masking.py,train_adapter.py,transport.py,engine_manager.py}`
- `apps/api/app/service/market_data/minute_price.py`（1 分钟行情读取层，训练分时与行情预览共用，见 §5.7）
- `apps/api/app/schema/training/{__init__.py,training.py}`
- `apps/api/app/model/training/{__init__.py,training.py}`
- `apps/api/app/api/v1/training_api.py`
- `apps/api/alembic/versions/20260915_0006_create_training_tables.py`
- `apps/api/tests/{test_backtrader_golden.py,test_training_masking.py,test_training_api.py,test_training_intraday_api.py,test_market_stock_intraday_api.py}`
- `apps/web/src/modules/training/*`、`apps/web/src/shared/api/training.ts`

修改（均为一处一改）：

- `apps/api/app/api/v1/router.py`（挂载新 router）
- `apps/api/app/db/schema.py`（import 新 model）
- `apps/api/app/service/backtest/backtrader.py`（改为从共享宿主取基类 / 数据馈送 / analyzers，公共入口与行为不变）
- `deploy/2_deploy.sh`（`--workers 2` → `1`）
- `apps/web/src/shared/routes.ts`、`apps/web/src/pages/WorkbenchPage.tsx`、`apps/web/src/modules/history/HistoryPanel.tsx`、`apps/web/src/shared/api/index.ts`
- `apps/api/app/service/market/{stock_preview.py}`、`apps/api/app/api/v1/market_api.py`、`apps/api/app/schema/market/{stock_preview.py,__init__.py}`、`apps/web/src/shared/api/market.ts`（行情预览的"查看分时"，见 §5.7）
- `apps/web/src/shared/components/charts/LightweightKlineChart.tsx`（标注菜单改为"水平线 / 垂直线 / 矩形 / 文字 / 查看分时 / 取消"，前四项**点完即画**、不再弹二次表单；新增垂直线 / 文字两种标注类型。已画出的标注：短按＝选中 + 弹编辑框，长按 240ms＝光标变手形后可拖动；四种标注都能设颜色，线 / 框设线宽、文字设字重。水平线 / 垂直线 / 矩形都能设**标题**，图上只显示标题不显示价格。矩形带左右日期边界，上/下沿 + 左/右边界 + 整体平移四个方向都能拖）

不动：`stock_preview` 的既有响应字段、数据集同步链路、`job_runtime`、**策略与回测的全部对外契约（见 §4.4）**。

### 4.4 对外契约冻结（本次不改）

训练是**新增**模块，不许改动任何现有的对外契约。下列内容一行都不改：

| 契约 | 位置 | 不变的部分 |
| --- | --- | --- |
| 策略协议 | `apps/api/app/service/strategy/protocol.py` | `chatq_init` / `chatq_next` 的入参出参、`ChatQAction` 的字段与语义（`action / symbol / order_type / size / price / ref / reason / client_signal_id`）、`ChatQState`、`normalize_chatq_result`、`validate_chatq_action`、`load_strategy_module`、`parse_strategy_source` |
| 协议文档 | `plugin/skills/strategy_management/references/strategy-protocol.md`、根目录 `signal-strategy-protocol-design.md` | 协议说明与示例 |
| 智能体技能 | `plugin/skills/strategy_management/*`（`SKILL.md` 及 references） | 智能体创建 / 管理策略的行为与产物；技能加载方式（`agent_runtime/sdk_skill_plugin.py`）也不变 |
| 策略与回测 API | `/api/strategies*`、`/api/backtests*` | 请求 / 响应 schema、错误码；`StrategyBacktestConfig` 不加字段 |
| 现有策略资产 | 数据库与 `strategy_versions.source_code` | 已有策略无需重写或迁移，`load_strategy_module` 的兼容性保持 |

训练与协议的关系是**只读复用**：

- 训练把人工点击表达成现有 `ChatQAction` 形状，并用现成的 `validate_chatq_action` 校验，不新增字段、不改语义。
- 如果将来要做"把某一局的操作序列导出成策略"，产物必须**符合现有协议**（一个普通的 `chatq_init` / `chatq_next` 模块），由现有技能与工具链路创建——不给训练开协议后门。
- 因此训练的接缝（§4.2）只能加在**训练自己的适配器**里；共享宿主是"抽取"而不是"改协议"，回测侧必须行为零漂移（§9）。

---

## 5. 关键机制

### 5.1 切片：切哪一段、谁看得到

从 `a_stock_daily_price_unadjusted` 取**连续两段、不重叠**的切片：**终点固定贴到数据末端（最新交易日）**，往前数 180 + N 根。

```
时间 ───────────────────────────────────────────────►

  ┌────────────────┐┌──────────────────┐
  │ warmup 180 根  ││  训练段 60~180 根 │
  └────────────────┘└──────────────────┘
   只给前端看           逐根揭示 + 喂 backtrader

  slice_start = 切片第一天（末端往前 180 + N 根）
  slice_end   = 数据末端（最新交易日，固定）
```

- **warmup（展示段）固定 180 根**：开局一次性全发给前端，让用户先看到历史形态；**不喂给 backtrader**。
- **训练段 N 根（随机 60~180，可配）**：逐根 reveal；**只有这一段喂给 backtrader** 作为 data feed，所以 broker 从一开始就只在训练段内撮合，权益曲线也只覆盖训练段。`N = 切片总根数 - warmup_bars`（`warmup_bars` 恒为 180），装载时一条 `COUNT` 就能得到，不需要单独存。
- 取数就是一条按区间读的 SQL（`slice_start` / `slice_end` 是切片两端，`warmup_bars` 标出展示段与训练段的分界）：

```sql
SELECT trade_date, open, high, low, close, volume
FROM a_stock_daily_price_unadjusted
WHERE symbol = ?
  AND trade_date BETWEEN <slice_start> AND <slice_end>
ORDER BY trade_date;
```

**三条采样口径**：

1. **可见段固定 180 根**：开局给用户的历史形态长度每局一致，不随题目漂移。
2. **训练段长度随机 60~180 根**：下限 60 保证一局有足够的决策空间，上限 180 控制单局时长；随机是为了让"这一局有多长"开局不可预判，同时"剩余 N 根"的进度感与结算口径仍然稳定。范围可配。
3. **终点固定为数据末端**：采样最简单，不需要计算随机偏移，切片永远是"最近 180 + N 根"。代价是时间盲被削弱——最后一根恒等于最新交易日，训练段也总是最近的行情（近期行情恰恰是记忆最鲜活的），且相邻日期开局会切出高度重叠、几乎同一道题。**本期有意接受**（见 §2.4、§10）：如果之后在意，只需把终点改成"数据末端往前随机 0~30 个交易日"，其余不变。

只剩一个最低限度的可用性过滤（不是算法，只是别切出没法看的题）：

- 排除窗口内含**除权除息**的切片（`a_stock_daily_adjust_factor` 在窗口内变化）——这也是本期能用不复权真实价的前提。
- **去除 ST**（`exclude_st`，默认开）：出题前先在候选里剔掉当前名称带 `ST` / `*ST` 的标的（名称取 `a_stock_snapshot_info`）；这个开关只改"候选池"，不改窗口。快照数据集不可用时退化为不过滤，不阻塞出题。

**不做缺失过滤**：停牌 / 缺 bar 就按实际存在的序列训练，窗口内只要真能数出 180 + N 根 bar 就成题。X 轴是序号，缺一段只是图上少几根，不会以日期形式暴露；代价是每局 warmup 覆盖的真实时间跨度不一样（停牌多的标的，180 根可能跨一年半）。

### 5.2 脱敏：只在接口出口做

数据库该存什么就存什么：`symbol`、`name`、`slice_start`、`slice_end` 都是普通列，正常写入、正常查询，不加密、不拆表。

**唯一的一条规则：脱敏发生在 API 出口**。训练期的响应由统一的白名单序列化产出，字段固定：

| 层 | symbol / name | 日期 | 其他 |
| --- | --- | --- | --- |
| 数据库 / 服务内部 | 原样保留 | 原样保留 | 正常读写、正常查询 |
| 训练期响应（`POST /sessions`、`GET /sessions/{id}`、`POST /reveal`） | 不返回，替换为 `instrument_alias`（"标的A"） | 不返回，替换为序号 `i` | `{i, o, h, l, c, v}` |
| `finish` 响应 | 返回真实 symbol / name | 返回真实窗口 | 用于复盘揭晓 |

也就是两个动作，没有算法：

1. **不发字段**：训练期响应里删掉 `symbol` / `name` / 日期，图表 X 轴显示连续序号 `i`（warmup 从 0 开始，训练段接着数），tooltip 也只显示序号。
2. **出口收口**：所有训练响应走同一个 `masking.scrub_*`，别让别的接口（比如直接查库的调试接口）把字段带出去。

两条配套约束：

- **入口补 symbol**：客户端提交的 action 里没有 `symbol`（有就泄露了），服务端在 `validate_chatq_action` 之前把会话的 `symbol` 填进 `ChatQAction`——协议对 `buy / sell / close` 强制要求该字段（`apps/api/app/service/strategy/protocol.py:241-249`）。
- **禁止 `SELECT *`**：行情视图本身带 `name` 列（`a_stock_daily_price_unadjusted` 有 `symbol / trade_date / name / open / high / low / close / volume / ...`），取数一律写死列名（§5.1 的 SQL 即是），别让 `name` 跟着 bar 流出去。

**可选的加固**：reveal 速率限流（防"按住下一根猛拖"偷看未来走势）、hash commitment（开局发 `sha256(symbol, window, bars, salt)`，结束给 `salt` 供复算）。单人自用无作弊动机，都可以不做，只有做多人盲测 / 挑战榜时才需要。

### 5.3 成交与统计口径

| 项 | 本期口径（backtrader 默认） |
| --- | --- |
| 成交时点 | 市价单按**本根 close**（当天尾盘价）成交：`cheat_on_open=True` 让适配器在本根开盘前拿到点击并提交，`set_coc(True)` 让 broker 用本根 close 撮合，`notify_order` 也在本根交付。锚点：用户看到第 t 根收盘 → 点击 → 揭示第 t+1 根，成交价 = 第 t+1 根 close（§4.2 的下标对齐保证这一点）。选它的原因：成交、结算点、响应三者在同一根闭合，**不存在挂单**，账户里的现金与持仓直接是 broker 的值，不用在服务端再算一套"可用"口径 |
| 费用 | `cerebro.broker.setcommission(commission=config.commission)`；百分比佣金，默认 `0.0005`（与回测配置一致），无最低 5 元 / 无印花税 / 无过户费 |
| 滑点 | `cerebro.broker.set_slippage_perc(perc=config.slippage, slip_open=True, slip_match=True)`：买入 ×(1+滑点)、卖出 ×(1-滑点)，且越不过当根 `high` / `low`；默认 `0.001`。`slip_open` 必须打开——训练全是"按本根 close 成交"的市价单，不打开就一点不滑。滑点只作用于训练这一局，回测口径不动（§4.4） |
| 委托类型 | 本期**只有市价单**，不做限价单（协议里的 `order_type=limit` 在训练侧不开口子） |
| 下单量 | 训练侧只传**仓位比例**（`size` 为 0~1 的小数：全仓、1/2、1/3、1/4、1/5），服务端换算成股数（向下取整）后交给 broker；broker 层面不强制 100 股整手。买入与卖出**各有一个档位**：买入按可用资金取比例，卖出按当前持仓取比例 |
| 比例换算 | 买入：`可用资金 × 比例 ÷ 成交价`；卖出：`当前持仓 × 比例`。两者都直接读 broker 的快照（`cash` / `position_size`），成交当场结算、没有挂单要扣。成交价就是正在揭示这一根的 close（+滑点），所以"全仓买入"不会被跳空挤成拒单、也不会剩一堆零钱。取整前先把份数四舍五入到 6 位小数（`_floor_shares`）——1/3、1/5 换算是无限小数，否则 300 股的 1/3 会算成 99 股 |
| 拒单 | 现金不足（`margin`）由 broker 拒单、卖出超过持仓（`oversell`）由适配器拒单，原因都透传前端（`TRAINING_BROKER_REJECTED` / `rejections[].reason`）；比例下单已预留缓冲，`margin` 是极端情况的兜底（`_floor_shares` 后仍买不起一股、或历史事件里的老股数） |
| 持仓方向 | **纯多头（long-only）**：训练只做多，卖单超过持仓时**整单拒掉**（不是缩量成交），永远不出现负持仓。服务端按快照换算股数，适配器在 `submit_action` 里再按 `getposition` 的实时持仓夹一次，`training_events` replay 也卖不出空头 |
| 价格序列 | 见 §3.4 约束 1：用不复权真实价，且切片内不含除权日 |

统计全部来自 analyzers，不落库：`_EquityCurveAnalyzer`（权益）、`_ClosedTradeAnalyzer`（平仓交易）、`_OrderExecutionAnalyzer`（逐笔成交）、`_DailyPortfolioAnalyzer`（每日持仓）。

两个推论，顺便写死：

- **没有挂单**：点击在本根开盘前提交、在本根 close 成交，结算点快照给出来时这一笔已经落地。所以账户里没有"挂单"这种中间态，事件词表里保留 `cancel` 只是为了与协议对齐，训练侧不产生它（提交与成交在同一根，来不及取消）。
- **不存在"未成交委托"**：每次点击都在"引擎正处理的那根"里提交并成交；走到最后一根（`cursor = N`）后只接受 `finish`（§7），不再接受 reveal，也就不可能留下没有结算点的委托。
- **训练段第一根就能成交**：warmup 不喂给 broker，但训练段第一根（第 180 根）本身就是可成交的——"开局看完 warmup 立刻买入"的第一笔按第 180 根的 close 成交，B 标记也钉在那一根。

### 5.4 推进与节奏

- 只有手动推进：`下一根`（键盘 `空格`）；买入 / 卖出 / 观望与推进合并为一次点击（一次点击 = 一条 `training_events` 事件 = 一根推进 = 一次响应：bar 由 service 从切片取、账户与成交由引擎在结算点给出；事件类型取 `buy / sell / close / cancel / hold`）。没有自动播放、没有倍速、没有暂停。
- 断线 / 刷新恢复：进度不在会话表里存，直接用 `training_events` 的信号历史 replay 重建（事件是唯一真相）；Web 与桌面端同 `session_id` 可续。这不是"暂停功能"，只是刷新后不丢局。空闲 30 分钟无请求只会回收**引擎线程**（§10），会话仍是 `active`，下次请求按事件重建——没有 `abandoned` 这种"偷偷作废"的状态。
- 安全推进：请求带客户端期望的 `seq`，与服务端 `cursor` 不一致返回 409 + 当前状态。
- **最后一根自动收局**：揭示到 `cursor = N` 的这一次 `reveal` 就会把会话置为 `finished`（`finished_at` 同时落下），响应里的 `session.status` 直接是 `finished`，复盘报告随后即可读。所以**没有"最后一根之后还要再点一次收局"这一步**；面板上的按钮只剩"提前结束"（见 §8.2）。引擎侧正好把训练段跑完（没有下一根），分析器结果已经就绪。

### 5.5 记分与复盘

| 字段 | 口径 |
| --- | --- |
| 初始资金 | `initial_cash`（默认 100,000） |
| 仓位 | `持仓市值 / 总权益` |
| 本局收益 | `(期末权益 - 初始) / 初始`；期末权益 = 最后一根揭示的 close 市值（未平仓持仓按市值计入） |
| 开仓收益 | 当前持仓浮动盈亏率（无持仓为 0.00%） |
| 附带 | 最大回撤、胜率、交易次数（复用 `chatq_engine/metrics.py`，与回测同口径可比） |

**收局不强制平仓**：`finish` 不会替用户卖出持仓，持仓按最后一根的 close 计入期末权益，浮动盈亏与已实现盈亏在报告里分开列（浮盈与 `open_return` 一致）。因此胜率 / 交易次数只统计**已平仓**交易；一局里从没平过仓（一路持有或一直观望）时，交易次数为 0、胜率显示"—"（无样本，不写成 0%，避免被读成"必输"）。

复盘：`finish` 揭晓真实标的 / 日期 + B/S 标记 + 逐笔成交 + 收益与回撤曲线（形状复用 `StrategyCurve`）。

### 5.6 局列表：只读摘要，不重建引擎

列表页要"一眼看完所有局"，但账户与收益是引擎产物、默认不落库（§2.4）。所以列表的取舍是：

| 项 | 来源 | 说明 |
| --- | --- | --- |
| 状态 / 初始资金 / 开始与结束时间 / 用时 | `training_sessions` 行本身 | 一次查询拿走，不带 `symbol` / 真实窗口日期（脱敏口径同 §5.2） |
| 进度 `cursor_index` | `training_events` 按 `session_id` 的计数 | "一次点击 = 一条事件 = 一根推进"（§6），所以行数就是游标，不用 replay |
| 训练段总长 `training_bars` | 开局时写入 `config_json` 的切片长度 | 早期会话没有这个键时返回 `null`，前端退化成"已推进 N 根" |
| 收益 / 回撤 | 不进列表 | 要算就得逐局 replay 引擎，代价与列表收益不匹配；点进去看复盘报告（走 `GET /sessions/{id}/report`） |

列表按 `created_at` 倒序分页（`limit` / `offset`，默认 20 条），并且只返回该 `project_id` 下的会话；`status`（`active` / `finished`）与 `keyword`（会话 ID 片段）是可选筛选，`total` 跟着筛选走，所以"第 N 页 / 共 M 条"始终自洽。前端只有一处入口：列表页的「新建训练」弹窗（初始资金 + 手续费 + 滑点 + 去除 ST；**仓位档位不在弹窗里**，它属于下单动作、训练中随时可换），开局成功后直接进入该局；进行中的局可以从列表「继续训练」续做，已收局的局直接进复盘。

列表用 shadcn `Table` + `Pagination` 呈现：上方是卡片标题（共 N 局）与筛选器（会话 ID 搜索 + 状态），表格里第一列是会话 ID（`trn_xxx`，脱敏口径下可安全展示），下方是上一页 / 下一页与页码。

### 5.7 当日分时：双击一根已揭示的日线

**为什么它能和双盲共存**：分时是**已经揭示过的那一天**的日内展开——这一根的开高低收早在图上，分钟数据不带来任何未来信息，所以它既不泄露标的身份，也不泄露后续走势。真正的红线只有两条，都在服务端收口：

1. **只有已揭示的根可看**：`seq < warmup_bars + cursor`，否则 `409 TRAINING_INTRADAY_NOT_REVEALED`。展示段（前 180 根）开局就给，所以在整段展示段上都能用。
2. **日期不出出口**：出口沿用 §5.2 的白名单，分钟点只有 `{t: "09:31", p, v}`——X 轴是 `HH:MM`，交易日只用来查数据。K 线侧的 `seq` 与分时的"第 N 根"是同一套序号，页面上没有任何能反推日历的字段。

**实现取舍**：

| 决定 | 口径 |
| --- | --- |
| 不 acquire 引擎 | 分时是只读旁路。序号 → 交易日的映射优先借用引擎手里那份切片（`training_engine_manager.get`），引擎已被空闲回收时用 `load_slice_window` 按窗口重装，**不 replay、不新建引擎** |
| 数据来源 | `a_stock_minute_price`（按 `trade_date` 前缀过滤，DuckDB 靠分区统计裁剪），**不做任何复权换算**：日线用的是 `a_stock_daily_price_unadjusted`，两者同口径 |
| 读取层复用 | 分钟序列由 `service/market_data/minute_price.py` 统一提供：训练分时与行情预览的"查看分时"（`GET /api/market/stocks/{symbol}/intraday?date=`）走同一份只读、容错实现；训练侧只多做"序号 → 交易日"这一步映射 |
| 涨跌幅基准 | 切片里前一根的 close（`prev_close`）；第 0 根没有前一根，返回 `null`，前端退化成"以本根开盘为基准" |
| 缺失不报错 | 分钟行情只同步了最近若干个交易日（§3.1），更早的日线拿不到分时：`available: false` + 空 `points`，前端提示"这一天没有分时数据"。数据集整体没接入时同样按不可用返回（服务端只记一条 warning），不阻塞训练 |
| 输出形态 | 复用 lightweight-charts：`BaselineSeries`（以昨收为基线，高于红、低于绿）+ 均价 `LineSeries`（按分钟成交量加权近似，分钟数据没有成交额字段）+ 分钟成交量 `HistogramSeries`；X 轴与 K 线同口径用**序号**，刻度 / crosshair 标签由 formatter 映射成 `HH:MM` |

**已知边界**：只有最近十来根训练段（以及展示段末尾）真的有分钟数据——切片贴着数据末端，而分钟数据只同步了最近 30 来个交易日，所以越靠近"最新"的根越可能看得到分时。分时**不影响撮合**：成交价仍是这一根的 close（§5.3），看了分时也不会改变任何结算口径。

---

## 6. 数据模型（SQLite，本期 2 张表）

```sql
-- 训练会话（symbol / 日期按普通列存，脱敏在 API 出口做，见 §5.2）
CREATE TABLE training_sessions (
  id             VARCHAR(64) PRIMARY KEY,
  project_id     VARCHAR(128) NOT NULL,
  mode           VARCHAR(16)  NOT NULL,   -- 本期恒为 daily（留位给后续分时）
  period         VARCHAR(8)   NOT NULL,   -- 本期恒为 1d
  symbol         VARCHAR(64)  NOT NULL,   -- 标的代码
  name           VARCHAR(128),            -- 标的名称
  slice_start    DATE         NOT NULL,   -- 切片起始日（warmup 第一天）
  slice_end      DATE         NOT NULL,   -- 切片结束日（训练段最后一天）
  warmup_bars    INTEGER      NOT NULL,   -- 前多少根是展示段，本期恒为 180
  status         VARCHAR(16)  NOT NULL,   -- active | finished
  initial_cash   DECIMAL(18,2) NOT NULL,
  config_json    JSON         NOT NULL,   -- 会话级参数：佣金 / 滑点 / 去除 ST / 切片长度（§5.6）
  started_at     DATETIME     NOT NULL,
  finished_at    DATETIME,
  created_at     DATETIME     NOT NULL,
  updated_at     DATETIME     NOT NULL
);
CREATE INDEX idx_training_sessions_project ON training_sessions(project_id, created_at);
CREATE INDEX idx_training_sessions_status  ON training_sessions(status);

-- 人工信号历史：每行 = 一次点击 = 一根推进（顺序看 seq，不看时间），崩溃后 replay 重建的唯一依据
CREATE TABLE training_events (
  id           VARCHAR(64) PRIMARY KEY,
  session_id   VARCHAR(64) NOT NULL,
  seq          INTEGER     NOT NULL,   -- 训练段第几根（0-based），一次点击 +1
  event_type   VARCHAR(32) NOT NULL,   -- 与 ChatQAction.action 同词表：buy | sell | close | cancel | hold
  payload_json JSON,                   -- 完整 ChatQAction（symbol 由服务端补）；hold 可只留 reason
  created_at   DATETIME    NOT NULL    -- 服务端落库时间
);
CREATE UNIQUE INDEX uq_training_events_session_seq ON training_events(session_id, seq);
```

派生量都不进表：`source_dataset` 本期恒为 `a_stock_daily_price_unadjusted`（写死在代码里，多数据源时再补列）；训练段根数 `N = COUNT(切片) - warmup_bars`（切开时随机抽 60~180，`warmup_bars` 恒为 180）；进度 `cursor = 该会话的事件条数`（每行一根推进，从 `training_events` 数出来，不单独存）。`mode` / `period` 本期也是常量，保留只是为了后续分时不用改表——如果想彻底精简，这两个也可以一起去掉。

说明：`event_type` 不引入新词表——`buy / sell / close / cancel` 就是回测那条 `ChatQAction.action` 通道上的取值，`hold` 表示"只推进、不下单"（观望 / 下一根；与协议里 `hold` 归一化成"无 action"的语义一致）。于是 replay 就是"按 `seq` 顺序重放每条事件的 `ChatQAction`，`hold` 只推进"；会话的创建与结束不进这张表，由 `training_sessions.status / finished_at` 表达。空闲回收（30 分钟，§10）只回收引擎线程，不动这张表和 `status`：会话永远只有 `active → finished` 两个状态。

`training_events.created_at` 由服务端写入，用于排障与复盘（相邻两条事件的差值就是这一根的思考时长）；总用时仍由 `training_sessions.started_at / finished_at` 算出。**不需要订单 / 成交表**（由 backtrader 局内产生，`finish` 一次性返回）。单局成绩默认不落库；若后续要翻历史成绩，再加一列 `report_json`。若要启用 §5.2 的可选加固，再加 `commitment / salt` 两列。

Alembic：`20260915_0006_create_training_tables.py`（`down_revision = "20260903_0005"`）；`apps/api/app/db/schema.py` 增加一行 model import。

---

## 7. API 契约（`/api/training`）

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/sessions?project_id=&status=&keyword=&limit=&offset=` | 项目下的局列表（倒序分页 + 可选筛选）：状态 / 进度 / 初始资金 / 用时；进度按 `training_events` 行数算，不重建引擎（见 §5.6） |
| POST | `/sessions` | 开局：`{project_id, mode:"daily", config?}` → 会话 + warmup bars + 掩码元数据。`config` 可选项：`warmup_bars` / `training_bars_min` / `training_bars_max` / `initial_cash` / `commission`（默认 0.0005）/ `slippage`（默认 0.001）/ `exclude_st`（默认 true）/ `idle_ttl_seconds` |
| GET | `/sessions/{id}` | 当前状态：掩码元数据、已揭示 bars、账户、持仓（全是 broker 的实时值，见 §5.3） |
| POST | `/sessions/{id}/reveal` | `{seq, action?, size?}` → 推进一根，返回新增 bar + 成交回报 + 账户；`action` 取值同 `ChatQAction.action`（`buy / sell / close / cancel / hold`），缺省即 `hold`；`size` 是**仓位比例**（0~1，见 §5.3），不传股数；**推完最后一根的这一次就把会话收局**（响应 `session.status = finished`，之后不再接受 reveal） |
| POST | `/sessions/{id}/finish` | 提前结束（走到最后一根会自动收局，这里是"没走完就想收"和幂等兜底；**不强制平仓**，持仓按最后一根 close 计市值）→ 揭晓 `symbol / name / 真实窗口`（启用 §5.2 加固时才有 `salt`）+ 单局报告 |
| GET | `/sessions/{id}/intraday?seq=` | 第 `seq` 根日线当天的分时（双击已揭示的日线）→ `{session_id, seq, available, bar, prev_close, points:[{t, p, v}]}`；`seq` 超出已揭示范围返回 `409 TRAINING_INTRADAY_NOT_REVEALED`，这一天没有分钟数据返回 `available: false`（见 §5.7） |
| GET | `/sessions/{id}/report` | 复盘报告（逐笔成交 + B/S 标记 + 收益 / 回撤曲线） |

训练期响应的字段（无任何 symbol / date，本期也没有 `ind` 字段；这里只列字段与派生关系，不写示例值，免得和上面的派生关系打架）：

- `session`：`id`、`status`、`instrument_alias`、`started_at`、`elapsed_seconds`、`warmup_bars`（恒 180）、`training_bars`（= `N`，60~180）、`cursor_index`（= 已揭示训练根数）、`remaining`（= `N - cursor_index`）、`account`。
- `account`（backtrader 的实时快照，前端靠它显示"可用资金 + 持仓"并决定买卖按钮是否可用）：`initial_cash`、`cash`（可用资金）、`position_size`（持仓股数）、`position_price`（持仓均价，空仓为 0）、`position_value`（按最新一根 close 计的市值）、`position_pct`、`total_return`、`open_return`。字段全部取自 broker，服务端不做二次加工；派生关系见 §5.5：空仓且没交易过时 `total_return` 与 `open_return` 都是 0。
- `bars`：已揭示的 bar，字段固定 `{i, o, h, l, c, v}`。
- `markers`：B/S 标记 `{i, side, text}`。

错误码（沿用 `{error_code, message, detail}`）：

| 错误码 | 场景 |
| --- | --- |
| `TRAINING_SESSION_NOT_FOUND` / `TRAINING_SESSION_FINISHED` | 会话不存在 / 已结束（训练段走完会自动收局，之后只能看报告） |
| `TRAINING_REVEAL_SEQ_CONFLICT` | `seq` 与服务端 `cursor` 不一致（重复 / 回退） |
| `TRAINING_SLICE_UNAVAILABLE` | 切不出可用切片（窗口含除权除息，或凑不满 180 + N 根 bar），重新出题 |
| `TRAINING_BROKER_REJECTED` | broker 拒单（本期唯一来源是资金不足等），透传原因 |
| `TRAINING_INTRADAY_NOT_REVEALED` | 请求的 `seq` 还没揭示（分时只覆盖已揭示的根，见 §5.7） |

---

## 8. 前端设计

### 8.1 目录与路由

```
apps/web/src/modules/training/
  TrainingPage.tsx          局列表 + 训练主体（列表为空 / 有一局进行中时都有落点）
  TrainingCreateDialog.tsx  「新建训练」弹窗：初始资金 + 手续费 + 滑点 + 去除 ST
  TrainingChart.tsx         训练专用图表（lightweight-charts；增量追加 + 遮罩轴 + B/S + 价格线）
  TrainingOrderPanel.tsx    买入 / 卖出 / 观望 / 下一根
  TrainingStatsBar.tsx      初始资金 / 仓位 / 本局收益 / 开仓收益
  TrainingReportDialog.tsx  揭晓（真实标的 / 日期）+ 逐笔复盘
  useTrainingSession.ts     会话状态机 + reveal 调用 + 列表进入（续做 / 看复盘）
  types.ts
apps/web/src/shared/api/training.ts
```

路由：`shared/routes.ts` 增加 `"kline-training"`，`WorkbenchPage` 的 `routePaths` 增加 `/training` 与分支渲染，`HistoryPanel` 增加导航项。

**图表的逻辑和现有行情图一样**：都是"给一个 candles 数组 → 渲染 K 线"。差别只有两点：

| | 现有 `LightweightKlineChart` | 训练 `TrainingChart` |
| --- | --- | --- |
| X 轴 | 真实日期 | **遮住**：只显示序号 `i`（warmup 从 0 起，训练段接着数） |
| 数据 | 一次性全量 `setData` | 开局送 warmup，之后**每 reveal 多一根** |
| 其余能力 | MA、成交量、B/S、价格线、标注 | 只保留 K 线 + 成交量 + B/S + 最新价格线 |

所以可以新做一个 `TrainingChart.tsx`（组件接口沿用现有形状：父组件维护 `candles` 数组），但**必须沿用 `lightweight-charts`**（仓库已依赖 `^5.2.1`，`apps/web/package.json`），不引入第二个图表库。

实现要点（lightweight-charts v5）：

- **轴遮罩**：服务端不下发日期，`time` 直接用序号 `i`；再用 `localization.timeFormatter` / `tickMarkFormatter` 把刻度显示成序号。**不要生成伪日期**（比如"2000-01-03 + i 个交易日"），那是给用户制造假信息。
- **增量追加**：用 `candleSeries.update(bar)` 追加，不要每根都 `setData` 全量——`update` 正是为这种场景提供的（time 递增时性能最好；成交量 series 同理）。
- **B/S 标记**：`createSeriesMarkers` 的实例 `.setMarkers(...)` 增量更新（现有组件已在用 `createSeriesMarkers`）。
- **最新价格线**：`createPriceLine` 之后用 `applyOptions({ price })` 滚动更新，不需要重建。

`LightweightKlineChart` 保持不动（现有行情图零回归）；主题与 series 配置可抽公共常量复用。

### 8.2 图表与交互

| 功能 | 实现落点 |
| --- | --- |
| 现价 / 涨跌幅、开 / 收 / 高 / 低 / 量 | 当前 bar 的头部信息条；涨跌幅基准 = 上一根 close（首根为 0） |
| 日 K 主图 + 成交量 | 本期只做日 K；成交量作为 K 线附属保留（可关闭），不做任何指标 |
| B/S 标记 | `markers`（已有能力），买入红 B、卖出蓝 S，钉在成交 bar |
| "最新价格"虚线 | `priceLines`（已有能力） |
| 买入 / 卖出 / 观望 | `TrainingOrderPanel`：按钮后面各跟一个仓位档位（全仓、1/2、1/3、1/4、1/5），买入按可用资金、卖出按当前持仓，提交的是比例、服务端换算股数（见 §5.3）；买入映射 `buy`、卖出映射 `sell`（long-only），观望/下一根映射 `hold` |
| 账户快照 | 面板顶部常显 broker 的实时快照：可用资金、持仓股数 / 市值 / 均价 / 占权益比（成交在本根结算点已落地，所以点完按钮这些数字当场就变）。**卖出按钮的禁用条件 = 没有持仓，买入按钮的禁用条件 = 没有剩余可用资金**（外加训练段走完 / 请求进行中两条通用禁用） |
| 提前结束 | `finish`：训练段没走完就收局（走完最后一根会自动收局，不需要点它） |
| 下一根 | `reveal` |
| 当日分时 | 双击 K 线上任意一根**已揭示**的日线 → `TrainingIntradayDialog`（分时线 / 均价线 / 昨收虚线 / 分钟成交量 + 开高低收与成交量，涨跌颜色以昨收为基准）；图表下方常显一行"双击任意一根已揭示的日线看当日分时"的提示（见 §5.7） |
| 用时 / 剩余根数 | `elapsed_seconds`（由 `started_at` 现算）/ `remaining` |
| 底部 4 项统计 | `TrainingStatsBar` |

`remaining = 0`（已揭示到最后一根）时，服务端已经把这一局收掉、页面直接进复盘，不再有"只能结束揭晓"的中间态（见 §5.4）。

交互细节：键盘 `空格` 下一根、`B` 买入、`S` 卖出、`Enter` 确认、`Esc` 取消（Web 与桌面端一致）；训练中页面标题 / tab 标题 / tooltip / 水印一律不含 symbol 与日期（tooltip 只显示序号与价格）；`finish` 后过渡揭晓真实标的与日期；刷新后按 `session_id` 恢复，不重播已揭示数据（一次性 `setData` 出当前进度，之后继续 `update` 追加）。

---

## 9. 落地顺序与测试

### 9.1 顺序

1. **补回测 golden 基线**：固定夹具数据集（沿用 `ds_backtest_market`）+ 固定源策略 → 冻结 `metrics` / `trades` / `curves` / `candles` 快照。
2. **抽共享宿主** `chatq_engine/backtrader_host.py`，回测改用它，跑 golden 确认零漂移。
3. **训练侧**：`slice_loader`（末端切片：180 根展示段 + 随机 60~180 根训练段 + 除权过滤）→ `masking`（出口脱敏：字段白名单 + 序号轴）→ `train_adapter`（只喂训练段 + 阻塞取动作 + 结算点吐账户）；揭示与事件落库留在 service。
4. **会话与引擎管理**：`training_sessions` / `training_events` 落库、`transport`（内存）、`engine_manager`（注册表 + 空闲回收 + replay）、`recycler`（定时把自退的句柄从注册表摘掉）。
5. **API** 与 `router` 挂载。
6. **前端** 页面、图表、下单面板、报告；`deploy/2_deploy.sh` 改 `--workers 1`。

### 9.2 测试

单元：

1. **出口脱敏**：`/sessions`、`/reveal` 的响应递归断言不含 `symbol / name / trade_date`；`finish` 响应才出现这些字段。
2. **游标与事件词表**：`seq` 冲突返回 409；游标（= 事件条数）不超过训练段根数 `N`；`event_type` 只出现 `buy / sell / close / cancel / hold`（不新增词表），且每条事件都恰好推进一根；**揭示到最后一根的响应里 `session.status` 已是 `finished`**、紧随其后的 `GET /report` 直接可用、再 reveal 返回 `TRAINING_SESSION_FINISHED`；提前 `finish` 落在同一个状态，且重复 `finish` 幂等。
3. **切片正确性**：`warmup_bars` 恒为 180 且 `N` 落在 60~180；切片终点 = 数据末端最新交易日；warmup 与训练段连续不重叠；含除权窗口的切片被排除；缺失 bar 不过滤（窗口内实际凑满 180 + N 根即算可用）；只把训练段喂给 backtrader（断言 data feed 长度 = N）。
4. **回测零回归**：golden 快照逐字段一致。
5. **对外契约未变**：现有策略 / 回测 API 测试（`test_strategy_api.py`、`test_backtests_api.py`、`test_strategy_persistence.py`）全绿，且 `service/strategy/` 与 `plugin/skills/strategy_management/` 零 diff。
6. **比例下单**：买入按 1/4、1/2、1 换算出的股数与可用资金自洽（按成交价换算、向下取整 + 佣金与滑点缓冲，`_floor_shares` 消浮点噪声，如 300 股的 1/3 = 100 股；全仓买入后剩下的钱不够再买一股）；比例卖出按持仓比例减仓、全仓卖出清零；资金不足时返回 `TRAINING_BROKER_REJECTED` 而不是静默成交。
7. **空闲回收**：无请求超过 `idle_ttl`（30 分钟）后引擎线程退出，同一 `session_id` 再请求时按 `training_events` replay 恢复到相同 `cursor` 与相同账户状态（数字级一致）。**收局不等超时**：自动收局时引擎把训练段跑完自退，`finish` 时由 `stop_and_collect` 发停止信号让线程当场退出；两条路径都在读完快照后立刻 `discard` 掉注册表条目，另有 `recycler` 每 60s 兜底清扫自退但没人再访问的句柄。
8. **推进时点**：用户在第 t 根上点击发出的市价单，成交价 == 第 t+1 根的 close（滑点关掉时；打开滑点则 == close ×(1+滑点)，卖出反向，且受当根 high / low 约束），且这一笔在**同一个响应的快照**里就能看到（没有挂单）——防止引擎与 service 的下标错位一格。
9. **纯多头与账户取值**：`account` 的 `cash` / `position_size` 与 broker 逐字段一致（服务端不二次加工）；"卖 1/2 紧接着卖全仓"两笔合计正好等于持仓、卖出后持仓为 0，空仓再卖返回 `TRAINING_BROKER_REJECTED`；引擎侧再夹一次——`submit_action` 收到超过实时持仓的卖单时整单拒掉（`oversell`），replay 同一串事件也不会出现负持仓。
10. **分层边界**：`train_adapter` 能脱离 HTTP 与数据库单独驱动（喂一串动作 → 得到正确的账户/成交序列），且引擎侧代码不写 `training_events`、不返回 K 线字段；揭示与事件落库只在 service。
11. **当日分时**（`test_training_intraday_api.py`）：只有已揭示的根能取（未揭示返回 409 `TRAINING_INTRADAY_NOT_REVEALED`，展示段与已揭示的训练根都能取）；响应递归断言无 `symbol / name / date`，且响应体里不出现那一天的日期字符串；`prev_close` == 切片里前一根的 close；分钟数据集缺失 / 当天没有分钟数据都返回 `available: false` 而不报错；引擎被回收（或提前收局后）仍按窗口重装切片给出同一份分时。

集成：对照 `test_market_stock_preview_api.py` 的写法，跑通"开局 → reveal → 下单（本根成交）→ finish → report"；并断言 `finish` 不替用户平仓（持仓保持不变，期末权益 = 现金 + 持仓 × 最后一根 close）。

前端：`npm --prefix apps/web run lint`（tsc）+ `build`；手工验收（掩码无泄露、刷新续做、Electron 下计时正确、双击日线弹出分时且只对已揭示的根生效）。

---

## 10. 风险与缓解

| 风险 | 影响 | 缓解 |
| --- | --- | --- |
| 训练期响应 / 日志 / tooltip 泄露标的或日期 | 双盲失效 | 出口统一白名单序列化 + 单测递归断言 + `finish` 才揭晓 |
| 前复权视图的 look-ahead | 切片隐含未来 | 禁用该视图；用不复权价 + 排除除权窗口 |
| 服务端 2 个 worker | 跨 worker 请求丢会话 | 本期 `--workers 1`（与桌面端形态一致） |
| 引擎线程生命周期（超时 / 进程重启） | 线程残留、丢局 | `queue.get(timeout=idle_ttl)` 自退 + `engine_manager` 空闲回收 + 信号历史 replay。`idle_ttl` 默认 **30 分钟**（可配），每次 reveal / GET 刷新；超时只回收引擎线程，会话保持 `active`，下次请求按事件重建。收局不用等超时：自动收局 / `finish` 当场让线程退出，随后 `discard` 句柄，`recycler` 每 60s 兜底清扫 |
| 撮合口径偏离 A 股现实 | 训练手感与实盘有差距 | 有意接受（§2.4），报告中标注口径；规则层属后续阶段 |
| 无指标导致信息量偏少 | 训练价值打折 | 明确本期定位为"纯形态决策"；指标面板属后续阶段 |
| 无题库导致题目重复 | 训练新鲜度下降 | 接受；后续阶段再引入题库与去重 |
| 切片终点固定为数据末端（训练段总是最近行情） | 时间盲被削弱、题面重复度升高 | 有意接受（§5.1、§2.4）；若后续在意，只把终点改成"数据末端往前随机 0~30 个交易日" |
| 比例下单遇上跳空高开 | "全仓"被 broker 拒单、体验挫败 | 换算时预留佣金 + 滑点缓冲（§5.3）；仍被拒时前端明确提示"按当前可用资金重下"，不静默忽略 |
| 训练改动外溢到策略协议或智能体技能 | 现有策略被破坏 | 契约冻结清单（§4.4）+ 现有策略 / 回测 API 测试全绿 + `service/strategy/` 与 `plugin/` 零 diff |

---

## 附录：关键决策记录

| 决策 | 结论 | 理由 |
| --- | --- | --- |
| 引擎 | backtrader，共享宿主 `chatq_engine/backtrader_host.py` | 回测与训练共用 bar 循环、数据馈送与 analyzers |
| 适配器 | 两个：`backtest`（现状不变）+ `train`（新增） | 差异收敛在 §4.2 的三个接缝；不把训练绑在回测模块的私有符号上 |
| 撮合 | 全交给 backtrader（`BackBroker` + analyzers） | 本期不承担自研账本与 A 股规则层的成本 |
| 揭示与引擎的边界 | K 线由 service 按 `cursor` 读切片 + 脱敏后给前端；引擎只在结算点吐出账户与成交 | 引擎不产出展示数据、不落库；service 不碰撮合。两侧靠 `warmup_bars + cursor - 1` 对齐（§4.2） |
| 成交对齐 | 引擎在第 t 根开盘前收到动作、当场提交 → 第 t+1 根 close 成交（再叠加滑点）；service 在同一响应里揭示第 t+1 根 | "你看着第 t 根按的买入，成交价 = 第 t+1 根 close"，成交即结算、没有挂单，训练手感与 §5.3 口径一致（§9.2 有断言） |
| 下单口径 | 训练侧只传仓位比例（全仓、1/2、1/3、1/4、1/5，买入与卖出各一档），服务端换算成股数；只有市价单 | 面板给的是档位不是股数；去掉限价单少一个价格入口与一条撮合分支（§5.3） |
| 纯多头 | 只做多：卖单超过持仓整单拒掉；账户的现金与持仓直接用 backtrader 的值，服务端不算第二套口径 | 练的是"看多买、看空卖"的单边手感，不做空；持仓只有一个来源就不会出现"面板 -450 股"这种自相矛盾的状态（§5.3） |
| 收局 | 走完最后一根自动收局；`finish` 只用来提前结束，且不强制平仓（持仓按最后一根 close 计市值）；会话只有 `active / finished` | 不用"走完再点一下"才看到成绩；用户没卖就是没卖，报告里已实现与浮动分开列；不引入 `abandoned`，空闲回收不动作废（§5.3–§5.5、§10） |
| 指标 | 本期不做 | 先把"人看 K 线做决策"的闭环跑通 |
| 题库 | 本期不做，开局即时随机切片 | 少两张表、少一个定时任务；先验证玩法 |
| 切片与脱敏 | 末端切片（180 根展示段 + 随机 60~180 根训练段）；数据库正常存 symbol / 日期，脱敏只在 API 出口做 | 采样逻辑最简单；不上加密 / 哈希 / 拆表，够用即可（§5.1、§5.2） |
| 事件词表 | `event_type` 直接沿用 `ChatQAction.action` 的取值（`buy / sell / close / cancel / hold`），每行事件 = 一次点击 = 一根推进 | 不引入第二套词表；replay 就是重放 action 流，`hold` 即"只推进"（§6） |
| 信号传输 | `TrainingSignalTransport` 抽象 + 内存实现 | 桌面端零外部依赖；将来要多实例 / 多用户时再填 Redis 实现 |
| 部署 | `--workers 1` | 内存引擎与 worker 亲和的最小代价方案 |
