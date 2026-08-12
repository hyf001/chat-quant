# SuperMind 帮助中心文档

来源: https://quant.10jqka.com.cn/view/help/4
下载时间: 2026-08-11T12:26:25.804Z
文档数: 10

## 文档列表

- 因子研究 (id: 8, headings: 52, code blocks: 1) - md/8_因子研究.md
- 回测引擎 (id: 12, headings: 121, code blocks: 27) - md/12_回测引擎.md
- 模拟仿真 (id: 10, headings: 49, code blocks: 5) - md/10_模拟仿真.md
- 研究环境/实盘 (id: 14, headings: 93, code blocks: 40) - md/14_研究环境_实盘.md
- API 文档 (id: 4, headings: 171, code blocks: 288) - md/4_API_文档.md
- 本地SDK (id: 3, headings: 5, code blocks: 0) - md/3_本地SDK.md
- 常见问题 (id: 16, headings: 86, code blocks: 0) - md/16_常见问题.md
- 因子数据产品 (id: 20, headings: 27, code blocks: 19) - md/20_因子数据产品.md
- 智能交易在线文档 (id: 22, headings: 543, code blocks: 0) - md/22_智能交易在线文档.md
- AI Lab (id: 24, headings: 102, code blocks: 24) - md/24_AI_Lab.md

## API 文档

# API文档

<p align="center">
  <img src="http://u.thsi.cn/imgsrc/pefile/b14f4bbd2763795db76ccdaf791c19f8.png" align="middle" width="500" />
</p>

如果您有任何意见建议或者您在使用过程中遇到说明文档中无法解答的问题，您可以:

- 📢在[SuperMind官方社区](https://quant.10jqka.com.cn/view/community)发帖提问交流
- 💌给我们发送邮件： SuperMind@myhexin.com
- 新文档还在不断完善中，想暂时使用旧的版本可以查看：[旧的文档](https://quant.10jqka.com.cn/platform/html/help-api.html?t=null#7/0)






























## 回测引擎专用API
目前，SuperMind策略API跟据标的、回测模式不同分为七种类型：

- 股票API：用于股票、场内基金、可转债策略回测
- 股票日内API：用于股票日内回转交易策略回测
- 期货期权API：用于期货期权策略回测
- 股票期货API：用户股票和期货对冲策略的回测
- 场外基金API：用于场外基金申赎策略回测
- 外汇API：用于回测外汇合约策略
- T+D合约API：用于回测延期交收合约策略

### [重要！！]写在最前面

若出现'****'未定义的情况，请先引入包，建议默认都加上，更方便：

```python
from mindgo_api import *
```

### 基本函数


| function                                                                                                                                                 | 股票 | 股票日内 | 期货期权 | 股票期货 | 场外基金 | 外汇 | T+D合约 |
| :------------------------------------------------------------------------------------------------------------------------------------------------------- | ---- | -------- | -------- | -------- | -------- | ---- | ------- |
| [init](https://quant.10jqka.com.cn/view/help/4#%E5%88%9D%E5%A7%8B%E5%8C%96%E5%87%BD%E6%95%B0-init)                                                       | ✅   | ✅       | ✅       | ✅       | ✅       | ✅   | ✅      |
| [handle_bar](https://quant.10jqka.com.cn/view/help/4#%E6%8C%89%E4%BA%A4%E6%98%93%E9%A2%91%E7%8E%87%E8%B0%83%E7%94%A8%E5%87%BD%E6%95%B0-handle-bar)       | ✅   | ✅       | ✅       | ✅       | ✅       | ✅   | ✅      |
| [handle_tick](https://quant.10jqka.com.cn/view/help/4#tick%E8%A1%8C%E6%83%85%E6%95%B0%E6%8D%AE%E5%8F%98%E5%8C%96%E6%97%B6%E8%B0%83%E7%94%A8-handle-tick) | ✅   | ✅       | ❌       | ❌       | ❌       | ❌   | ❌      |
| [open_auction](https://quant.10jqka.com.cn/view/help/4#%E9%9B%86%E5%90%88%E7%AB%9E%E4%BB%B7%E5%90%8E-9-26-%E8%B0%83%E7%94%A8-open-auction)               | ✅   | ❌       | ❌       | ❌       | ❌       | ❌   | ❌      |
| [before_trading](https://quant.10jqka.com.cn/view/help/4#%E5%BC%80%E7%9B%98%E5%89%8D%E5%8D%8A%E5%B0%8F%E6%97%B6%E8%B0%83%E7%94%A8-before-trading)        | ✅   | ✅       | ✅       | ✅       | ✅       | ✅   | ✅      |
| [after_trading](https://quant.10jqka.com.cn/view/help/4#%E6%94%B6%E7%9B%98%E5%90%8E%E5%8D%8A%E5%B0%8F%E6%97%B6%E8%B0%83%E7%94%A8-after-trading)          | ✅   | ✅       | ✅       | ✅       | ✅       | ✅   | ✅      |
| [on_order](https://quant.10jqka.com.cn/view/help/4#%E5%A7%94%E6%89%98%E5%9B%9E%E8%B0%83%E5%87%BD%E6%95%B0-on-order)                                      | ✅   | ❌       | ❌       | ❌       | ❌       | ❌   | ❌      |
| [on_trade](https://quant.10jqka.com.cn/view/help/4#%E6%88%90%E4%BA%A4%E5%9B%9E%E8%B0%83%E5%87%BD%E6%95%B0-on-trade)                                      | ✅   | ❌       | ❌       | ❌       | ❌       | ❌   | ❌      |

- ❗注意事项：

  - 股票策略目前仅在研究环境的回测接口中支持 `handle_tick`
  - `handle_tick`与 `handle_bar`不能并存

---

#### 初始化函数 init

- 👑调用方法
  ```python
  def init(context): ...
  ```
- 🔧作用
  - 初始化函数，进行策略回测与模拟交易时在最开始时执行一次。在研究环境中，使用 `research_trade` 进行仿真交易时，只在第一次运行策略时执行一次 `init`，因此修改 `init` 里代码不会生效。
  - 用于初始化账户信息、回测参数、全局变量等。
- 📚参数说明
  - `context`: [context对象](https://quant.10jqka.com.cn/view/help/4#context)，用于存放当前账户资金、持仓信息等数据
- ❗注意事项
  - 该函数用于初始化账户，任何一个策略都必须有该函数。
  - 在该函数下，你可以设置很多初始条件，例如：基准、交易费、滑点、合约池等等。
- 📝示例：
  - 调用
    ```python
    from mindgo_api import *

    def init(context):   
        #设置要交易的标的(平安银行) ,命名的时候注意不要覆盖系统变量
        context.stock = '000001.SZ'
    ```

#### 按交易频率调用函数 handle_bar

- 👑调用方法
  ```python
  def handle_bar(context, bar_dict): ...
  ```
- 🔧作用
  - 用于定时执行买卖条件，根据策略设定的交易频率（日/分钟）自动调用。
- 📚参数说明
  - `context`: [context对象](https://quant.10jqka.com.cn/view/help/4#context)，用来存放当前账户资金、持仓信息等数据。
  - `bar_dict`: [bar_dict对象](https://quant.10jqka.com.cn/view/help/4#bar-dict)，用于存放当前订阅所有合约的bar行情数据。
- ❗注意事项
  - **尽可能保证此函数中的代码效率，避免在此函数下查询大量数据**，特别是在模拟、仿真交易中，避免出现执行时间过长，导致产生延时成本。
  - 此函数在非交易时间不会触发(例如1月1日至3日是非交易日，则handle_bar在1日至3日不触发，直到下一个交易日4号触发)。
  - 此函数的调用频率根据策略的交易频率确定。
  - 在该函数中，可以传入其他函数的运行结果，用来判断买卖条件。
- 📝示例：
  - 调用
    ```python
    # 每个交易频率买入100股平安银行
    def handle_bar(context, bar_dict):
        order('000001.SZ', 100)
    ```

#### tick行情数据变化时调用 handle_tick

- 👑调用方法
  ```python
  def handle_tick(context, tick): ...
  ```
- 🔧作用
  - 用于在所订阅的股票tick行情数据发生变化时调用。
- 📚参数说明
  - `context`: [context对象](https://quant.10jqka.com.cn/view/help/4#context)，用来存放当前账户资金、持仓信息等数据。
  - `tick`: [tick对象](https://quant.10jqka.com.cn/view/dataplatform/detail/16)，用于存放当前推送合约的tick行情数据。
- ❗注意事项
  - **尽可能保证此函数中的代码效率，避免在此函数下查询大量数据**，特别是在模拟、仿真交易中，避免出现执行时间过长，导致产生延时成本。
  - 当同时订阅了多只股票时，遵循“时间优先，顺序优先”的规则，即首先执行时间戳靠前的股票，如果时间戳相同，则按照订阅列表中的顺序执行。
  - tick行情的更新会自动触发该方法的调用。策略具体逻辑可在该方法内实现，包括交易信号的产生、订单的创建等。在实时模拟交易中，该函数有tick行情则被触发一次。
  - **仅在T0策略、股票策略(研究环境)中有效**。
- 📝示例：
  - 调用
    ```python
    # 打印当前推送tick行情的股票代码，并下单买入100股
    def handle_tick(context, tick):
        log.info(tick.order_book_id)
        order(tick.order_book_id, 100)
    ```

#### 集合竞价后(9:26)调用 open_auction

- 👑调用方法
  ```python
  def open_auction(context, bar_dict): ...
  ```
- 🔧作用
  - 用于在集合竞价后(9:26)调用一次。
- 📚参数说明
  - `context`: [context对象](https://quant.10jqka.com.cn/view/help/4#context)，用来存放当前账户资金、持仓信息等数据。
  - `bar_dict`: [bar_dict对象](https://quant.10jqka.com.cn/view/help/4#bar-dict)，用于存放当前订阅所有合约的bar行情数据。
- ❗注意事项
  - **尽可能保证此函数中的代码效率**，特别是在模拟、仿真交易中，避免出现执行时间过长。
  - 在回测、模拟交易中，在此阶段下单会使用集合竞价成交数据对订单进行撮合，可用于回测集合竞价策略；但在仿真交易中，此时下的订单会在9:30进行撮合。
  - **仅在股票策略中有效**。
- 📝示例：
  - 调用
    ```python
    # 下单买入100股平安银行
    def open_auction(context, bar_dict):
        order('000001.SZ', 100)
    ```

#### 开盘前半小时调用 before_trading

- 👑调用方法
  ```python
  def before_trading(context): ...
  ```
- 🔧作用
  - 用于在当天开盘前半小时调用一次，常用于使用前日数据计算因子、信号；储存自定义参数、全局变量等。
- 📚参数说明
  - `context`: [context对象](https://quant.10jqka.com.cn/view/help/4#context)，用来存放当前账户资金、持仓信息等数据。
- ❗注意事项
  - 该函数在回测中的非交易日不触发。
  - 在该函数中，你可以自由储存自定义函数的运行结果、全局变量数据等,并在 `handle_bar`等函数中使用。
- 📝示例：
  - 调用
    ```python
    # 每个交易日开市前，打印出目前的账户信息
    def before_trading(context):
        log.info(context.portfolio)
    ```

#### 收盘后半小时调用 after_trading

- 👑调用方法
  ```python
  def after_trading(context): ...
  ```
- 🔧作用
  - 用于在当天收盘后半小时调用一次，常用于根据前日数据计算；储存自定义参数、全局变量等。
- 📚参数说明
  - `context`: [context对象](https://quant.10jqka.com.cn/view/help/4#context)，用来存放当前账户资金、持仓信息等数据。
- ❗注意事项
  - 该函数在回测中的非交易日不触发。
  - 在该函数中，你可以自由储存自定义函数的运行结果、全局变量数据等，用来总结今日的交易，并计划明天的交易。
- 📝示例：
  - 调用
    ```python
    # 交易日结束后，打印组合盈亏
    def after_trading(context):
        log.info(context.portfolio.pnl)
    ```

#### 委托回调函数 on_order

- 👑调用方法
  ```python
  def on_order(context, odr): ...
  ```
- 🔧作用
  - 用于在委托状态更新后进行回调。
- 📚参数说明
  - `context`: [context对象](https://quant.10jqka.com.cn/view/help/4#context)，用来存放当前账户资金、持仓信息等数据。
  - `odr`: [`Order`对象](https://quant.10jqka.com.cn/view/help/4#%E8%AE%A2%E5%8D%95%E5%AF%B9%E8%B1%A1-Order%E7%B1%BB)，包含委托详情。
- ❗注意事项
  - 回测时下单后立刻触发，仿真交易时会在handle_bar执行完后触发。
- 📝示例：
  - 调用
    ```python
    # 打印委托对象信息
    def on_order(context, odr):
        log.info(odr)
    ```

#### 成交回调函数 on_trade

- 👑调用方法
  ```python
  def on_trade(context, trade): ...
  ```
- 🔧作用
  - 用于在有成交后进行回调。
- 📚参数说明
  - `context`: [context对象](https://quant.10jqka.com.cn/view/help/4#context)，用来存放当前账户资金、持仓信息等数据。
  - `trade`: [`Trade`对象](https://quant.10jqka.com.cn/view/help/4#%E6%88%90%E4%BA%A4%E5%AF%B9%E8%B1%A1-Trade%E7%B1%BB)，包含成交详情。
- ❗注意事项
  - 回测时下单后立刻触发，仿真交易时会在handle_bar执行完后触发。
- 📝示例：
  - 调用
    ```python
    # 打印成交对象信息
    def on_trade(context, trade):
        log.info(trade)
    ```

### 自定义运行函数

#### 每日定时运行函数：run_daily

- 👑调用方法
  ```python
  run_daily(func, time_rule='every_bar', hours=None, minutes=None, reference_security=None)
  ```
- 🔧作用
  - 用于每日定时运行指定的函数。通常在分钟级策略中，用于在特定时间点执行任务。
- 📚参数说明
  - `func`: `callable`，需要执行的函数。
  - `time_rule`: `str`，默认为`'every_bar'`时间计算规则。可选值：
    - `'after_open'`: 开盘后运行。配合`hours`和`minutes`参数设置开盘后多久运行，取值范围为1分钟至4小时。
    - `'before_close'`: 收盘前运行。配合`hours`和`minutes`参数设置收盘前多久运行，取值范围为1分钟至4小时。
    - `'every_bar'`: 每分钟都会运行。使用此规则时，`hours`和`minutes`参数会被忽略。
  - `hours`: `Optional[int]`，运行时间(小时)。与`minutes`配合使用。
  - `minutes`: `Optional[int]`，运行时间(分钟)。与`hours`配合使用。
  - `reference_security`: `Optional[str]`，参考标的，用于确定交易时间。默认为`None`。例如：
    - 股票: `'000001.SZ'`，交易时间为9:30-15:00。
    - 股指期货: `'IC1508'`，交易时间在20160101之前为9:15-15:15，之后为9:30-15:00。
    - `None`:等同于股票
- ❗注意事项
  - 如果在日频策略中使用该函数，不需要传入 `time_rule`, `hours`, `minutes`，默认在9点31分执行，实际和日频 `handle_bar`效果相同。
  - 此函数中 `reference_security`参数，如果以股票为标的，则传入任何一个股票代码都是可以的，期货同理。
  - 该函数的 `time_rule`参数，如果填写 `'every_bar'`，则不需要填写 `hours`和`minutes`两个参数，如果填写了，是无效的，不会报错，也不影响运行。
- 📝示例：
  - 在每个交易日开盘后30分钟执行一次
    ```python
    def init(context):
        # 每个交易日开盘后30分执行一次
        run_daily(func=test_day, time_rule='after_open', hours=0, minutes=30, reference_security='000856.SZ')

    def test_day(context, bar_dict):
        log.info('定时运行')
    ```

#### 每周定时运行函数：run_weekly

- 👑调用方法
  ```python
  run_weekly(func, date_rule, reference_security=None)
  ```
- 🔧作用
  - 用于每周定时运行函数,在指定日的开盘时执行。
- 📚参数说明
  - `func`: `callable`，要执行的函数，通常为自定义函数，用于实现特定目标。
  - `date_rule`: `int`，时间计算规则。正数(取值范围为[1,5])表示每周的第几个交易日，负数(取值范围为[-5,-1])表示每周倒数第几个交易日。
  - `reference_security`: `Optional[str]`，参考标的，用于确定交易时间。默认为`None`
    - 若为股票代码(如'000001.SZ')，交易时间为9:30-15:00；
    - 若为股指期货代码(如'IC1508')，则交易时间分为9:15-15:15和9:30-15:00两种，并以20160101为界划分。
    - `None`：等同于股票标的。
- ❗注意事项
  - 该函数既可以用于分钟级策略，也可以用于日级策略。
  - `reference_security` 参数不填写时，自动默认为股票标的。
  - `reference_security` 参数以股票为标的时，传入任何一个有效的股票代码均可；期货同理。
  - `date_rule` 参数必须填写，取值范围为 1 至 5 或 -5 至 -1。如果大于 5，则会报错；如果小于 -5，策略会继续运行，但该函数不生效。
- 📝示例：
  - 调用
    ```python
    def init(context):
        # 每周第一个交易日执行
        run_weekly(func=test_week, date_rule=1, reference_security='000001.SZ')

    def test_week(context, bar_dict):
        log.info('定时运行')
    ```

#### 每月定时运行函数：run_monthly

- 👑调用方法
  ```python
  run_monthly(func, date_rule, reference_security=None)
  ```
- 🔧作用
  - 用于每月定时运行函数，在指定日开盘时执行。
- 📚参数说明
  - `func`: `callable`，表示执行的函数，一般为自定义函数，用于实现特定目标。
  - `date_rule`: `int`，表示时间计算规则。正数(取值范围为[1,23])表示为每月的第几个交易日，负数(取值范围为[-23,-1])表示为每月倒数第几个交易日。
  - `reference_security`: `Optional[str]`，表示参考标的，用于确定交易时间。默认为`None`
    - 若为股票(如'000001.SZ')，交易时间为9:30-15:00；
    - 若为股指期货(如'IC1508')，交易时间分为9:15-15:15和9:30-15:00两种，以20160101划分。
    - `None`：等同于股票
- ❗注意事项
  - 该函数既可以用于分钟级策略，也可以用于日级策略。
  - 此函数中 `reference_security`参数不填写，则自动默认为股票标的。
  - 此函数中 `reference_security`参数，如果以股票为标的，则传入任何一个股票代码都是可以的，期货同理。
  - 该函数的 `date_rule`参数，必须填写(取值范围为1至23或-23至-1)，输入数值超出范围，则会报错。
- 📝示例：
  - 调用
    ```python
    def init(context):
        # 每月第5个交易日执行
        run_monthly(func=test_month, date_rule=5, reference_security='000001.SZ')

    def test_month(context, bar_dict):
        log.info('定时运行')
    ```

### 设置函数

#### 设置基准收益：set_benchmark

- 👑调用方法
  ```python
  set_benchmark(symbol)
  ```
- 🔧作用
  - 用于设置基准收益，其不影响策略的运行。
- 📚参数说明
  - `symbol`: `str`，表示股票或者其他品种代码。例如：'000300.SH' (沪深300) 或 '511010.SH' (国债ETF)。
- ❗注意事项
  - 必须在 `init(context)` 函数下设置，否则无效。
  - `symbol` 参数必须输入字符串，且只能输入一个代码（例如：'000300.SH' 正确，['000300.SH'] 错误）。
  - 如果策略中未设置该函数，则默认基准为沪深300指数。
- 📝示例：
  - 调用
    ```python
    def init(context):
        # 初始化策略时设置基准为沪深300指数
        set_benchmark('000300.SH')
    ```

#### 设置策略滑点：set_slippage

- 👑调用方法
  ```python
  set_slippage(slippage)
  ```
- 🔧作用
  - 用于设置策略滑点，该设置不影响策略的运行，默认为0.002的可变滑点。
- 📚参数说明
  - `slippage`: `PriceSlippage` 或 `FixedSlippage`，表示滑点对象。
    - `PriceSlippage`：可变滑点对象，例如`PriceSlippage(0.1)`，表示买入价为实际价格乘1.05，卖出价为实际价格乘0.95。
    - `FixedSlippage`：固定滑点对象，例如`FixedSlippage(10)`，表示买入价为实际价格加5，卖出价为实际价格减5。
- ❗注意事项
  - 该函数为初始设置函数，必须在 `init(context)` 中调用，否则设置无效。
- 📝示例：
  - 调用
    ```python
    def init(context):
        #设置可变滑点2%，表示买入价为实际价格乘101%，卖出价为实际价格乘99%
        set_slippage(PriceSlippage(0.02))
    ```

#### 设置交易手续费：set_commission

- 👑调用方法：
  `set_commission(cal_style)`
- 📚参数说明：

  - cal_style:PerShare或PerTrade对象
    - PerShare：**比例交易手续费**，例如 `PerShare(type='stock',cost=0.0002)`，表示手续费为交易额的0.02%
    - PerTrade：**固定交易手续费**，例如 `PerTrade(type='future',cost=5.0)`，表示每笔交易手续费5元
- 🔧作用：

  - set_commission函数用来设置交易手续费，其不影响策略的运行,默认交易手续费为：交易额的0.02%
- ❗注意事项：

  - 该函数必须在 `init(context)`函数下设置, 否则无效
- 📝示例：

  ```python
  def init(context):
      #设置股票手续费为交易额的0.01%(万一)，最低手续费为0元(免5)
      set_commission(PerShare(type='stock',cost=0.0001,min_trade_cost=0.0))
  ```

---

#### 设置回测策略账户初始持仓：set_holding_stocks

- 👑调用方法：
  `set_holding_stocks(holdings)`
- 📚参数说明：

  - holdings:dict对象，key为持仓的symbol，value为持仓的数量(必须为正整数)
- 🔧作用：

  - set_holding_stocks函数用来设置回测策略账户初始持仓(设置初始持仓并不会减少账户的初始资金)
- ❗注意事项：

  - 若进行策略回测, 则该函数默认使用回测开始日期的前一个交易日收盘价持有初始持仓
  - 若回测起始日期小于等于所添加股票的上市日期或股票已经退市, 则无法添加该股票持仓
  - 该函数必须在init函数下设置,否则是无效的
- 📝示例：

  ```python
  def init(context):
      #设置策略初始持仓
      set_holding_stocks({'000001.SZ': 200,'300033.SZ': 500,'600519.SH': 700})
  ```

---

#### 设置设置子账户：set_subportfolios

- 👑调用方法：
  `set_subportfolios([dict_1,dict_2,...])`
- 📚参数说明：

  - dict_1:dict对象，key为 `cash`、`type`的字典
    - cash:子账户初始资金,例如:'cash':500000,设置子账户初始资金为50万
    - type:子账户类型,例如： 'type': 'future',设置该子账户为期货账户.配合'cash'一起使用:{'cash':500000,'type':'future'}
- 🔧作用：

  - set_subportfolios函数用来设置设置子账户
- ❗注意事项：

  - 该函数设置后，子账户初始资金之和必须等于总的初始资金(回测时需要填写总的初始资金)
  - 模拟交易时，函数设置的期货和股票账户资金必须对应模拟交易中期货和股票账户的资金。设置函数或者创建模拟账户时,必须考虑到这点,不然无法正常模拟交易
  - 如果整个策略没有该函数,则无法进行期货交易
  - 该函数必须在init函数下设置,否则是无效的
- 📝示例：

  ```python
  def init(context):
      #设置子账户,股票账户50万，期货账户50万.
      set_subportfolios([{'cash':500000,'type':'stock'},{'cash':500000,'type':'future'}])
  ```

  ---

#### 设置最大成交比例：set_volume_limit

- 👑调用方法：
  `set_volume_limit(daily, minute)`
- 📚参数说明：

  - daily:float，例如 `daily=0.25`,则意味着下单数量超过日线级成交量25%的部分无法成交；`daily=None`,则表示不做成交量限制
  - minute:float，例如 `minute=0.5`,则意味着下单数量超过分钟线级成交量50%的部分就无法成交；`minute=None`,则表示不做成交量限制
- 🔧作用：

  - set_volume_limit函数用来设置最大成交比例,若下单数量超过当前时间周期的成交量一定比例，则按允许的最大数量成交
- ❗注意事项：

  - 如果策略没有该函数，则默认daily=0.25，minute=0.5
  - 该函数设置后，一旦触发，则本次下单可能会部分成交
- 📝示例：

  ```python
  def init(context):
      #设置最大成交比例日级成交量比例50%,分钟级成交量比例50%
      set_volume_limit(daily=0.5, minute=0.5)
  ```

---

#### 设置下单后延迟成交时间：set_trade_delay

- 👑调用方法：
  `set_trade_delay(delay_time)`
- 📚参数说明：

  - delay_time:int，延迟delay_time个bar后成交，例如 `delay_time=5`
    - 在日级回测中下单后，延迟5个交易日成交
    - 在分钟级回测中下单后，推迟5分钟成交
- 🔧作用：

  - 设置下单后延迟成交时间
- ❗注意事项：

  - 该函数在模拟交易中无效，只能在回测环境中使用它
  - 该函数必须在init(context)函数下设置,否则无效
- 📝示例：

  ```python
  def init(context):
      #下单后推迟3分钟/交易日成交
      set_trade_delay(delay_time=3)
  ```

---

#### 设置log输出级别：set_log_level

- 👑调用方法：
  `set_log_level(level,is_limit=True,filename=None)`
- 📚参数说明：

  - level:str，log对应的级别，如果设定level为'warn',则log打印函数只会打印'warn'、'error'级别
  - is_limit:bool,日志数量限制，默认True为10000条
  - filename:str，重定向日志文件路径(仅研究平台有效)
- 🔧作用：

  - set_log_level函数用来设置log输出级别,log打印一般有三种log.info()、log.warn()、log.error(),优先级排序为：error>warn>info
- ❗注意事项：

  - 该函数不仅可以在 `init(context)`函数下设置,也可以在 `handle_bar(context, bar_dict)`函数下设置
  - 当log.error()打印数据时,整个回测就会停止,类似一个报错终止机制
- 📝示例：

  ```python
  def init(context):
      #设置日志级别:warn
      set_log_level(level='warn')
  ```

---

#### 设置回测成交机制：set_execution

- 👑调用方法：
  `set_execution(str)`
- 📚参数说明：

  - str:撮合成交机制，可选'close','next_open'
    - 'close':当前bar收盘价撮合
    - 'next_open':下一个bar开盘价撮合
- 🔧作用：

  - set_execution函数用来设置回测成交机制, 不同的设置会采用不同的价格进行撮合成交(只在分钟回测中有效，默认next_open)
- ❗注意事项：

  - 该函数必须在 `init(context)`函数下设置, 否则无效
  - 该函数的str参数, 必须输入字符串, 且只能输入一个，例如: `set_execution('next_open')`
  - 如果整个策略没有该函数, 则默认策略采用next_open模式进行回测
- 📝示例：

```python
def init(context):
    #初始化策略时设置撮合机制为下一个bar的open
    set_execution('next_open')
```

---

#### 调整handle_bar运行时间：enable_open_bar

- 👑调用方法：
  `enable_open_bar()`
- 🔧作用：

  - 该函数在init调用，功能为在股票日级回测中，handle_bar执行时间调整为9:30；在分钟级回测中，handle_bar在9:30增加一次运行
- 📝示例：

  ```python
  # 股票策略模版
  # 初始化函数,全局只运行一次
  def init(context):
      enable_open_bar()

  #每日开盘前9:00被调用一次,用于储存自定义参数、全局变量,执行盘前选股等
  def before_trading(context):
      pass

  ## 开盘时运行函数
  def handle_bar(context, bar_dict):
      order("300033.SZ", 100)

  ## 收盘后运行函数,用于储存自定义参数、全局变量,执行盘后选股等
  def after_trading(context):
      pass
  ```

---

#### 定义列式计算的信号名以及计算方式：reg_signal

- 👑调用方法：
  `reg_signal(name,func)`
- 📚参数说明：

  - name:指标计算名称
  - func:指标的计算方式,定义方式为 `def func(data):`,data代表订阅的tick数据,格式为pd.DataFrame,返回值为一个索引与data对齐的pd.Series
- 🔧作用：

  - 定义列式计算的信号名以及计算方式
  -
- ❗注意事项：

  - 若订阅了多只股票，则对每只股票分别进行计算
  - 需要与get_signal配合使用
- 📝示例：

```python
#定义一个名为’big’的信号，算法为tick数据大于10等于True，否则等于False.
def init(context):
    reg_signal('big',get_big)

def get_big(data):
    return data[‘current’]>10
```

---

#### 设置某一品种的保证金比例：set_margin_rate

- 👑调用方法：
  `set_margin_rate(symbol,long_value,short_value)`
- 📚参数说明：

  - symbol:标的代码
  - long_value:做多保证金比例
  - short_value:做空保证金比例
- 🔧作用：
- 该函数用于设置某一品种的保证金比例
- 📝示例：

  ```python
  # 设置螺纹钢的保证金比例为9%
  def init(context):
      set_margin_rate('RB',0.09,0.09)
  ```

---

#### 设置期权手续费：set_option_commission

- 👑调用方法：
  `set_option_commission(cost)`
- 📚参数说明：

  - cost:单张期权合约的手续费(元)
- 🔧作用：

  - 该函数设置期权手续费（元/单张10000份），默认为5元
- ❗注意事项：

  - 该函数必须在 `init(context)`函数下设置, 否则无效
- 📝示例：

  ```python
  # 设置期权手续费为10元/张
  def init(context):
      set_option_commission(10)
  ```

---

#### 设置期权交易滑点：set_option_slippage

- 👑调用方法：
  `set_option_slippage(rate)`
- 📚参数说明：

  - rate:设置的期权交易浮动滑点比例
- 🔧作用：

  - 该函数设置期权交易滑点, 其不影响策略的运行，默认为0.001
- ❗注意事项：

  - 该函数必须在 `init(context)`函数下设置, 否则无效
- 📝示例：

  ```python
  # 设置期权交易滑点为双边0.004(单边0.002)
  def init(context):
      set_option_slippage(0.004)
  ```

---

#### 设置场外基金申购折扣率：set_discount_rate

- 👑调用方法：
  `set_discount_rate(rate)`
- 📚参数说明：

  - rate:基金申购折扣率，在0到1之间，默认为0.1
- 🔧作用：

  - 该函数设置场外基金申购折扣率
- ❗注意事项：

  - 该函数必须在 `init(context)`函数下设置, 否则无效
- 📝示例：

  ```python
  def init(context):
      # 初始化策略时设置折扣率10%
      set_discount_rate(0.1)
  ```

---

#### 设置场外基金申购折扣率：set_dividend_mode

- 👑调用方法：
  `set_dividend_mode(mode)`
- 📚参数说明：

  - mode:基金分红处理模式，可选 `cash`/`invest`
    - `cash`:现金分红
    - `invest`:红利再投资
- 🔧作用：

  - 该函数设置场外基金申购折扣率
- ❗注意事项：

  - 该函数必须在 `init(context)`函数下设置, 否则无效
  - 如果未设置，系统默认为红利再投资
- 📝示例：

  ```python
  def init(context):
      #初始化策略时设置分红模式为红利再投资
      set_dividend_mode(invest)
  ```

---

<!--

#### 设置中国银行”双向宝“合约交易的保证金比例：set_margin_rate_fx

- 👑调用方法：
  `set_margin_rate_fx(rate)`
- 📚参数说明：
  
  - rate:中国银行"双向宝"合约保证金比例(%),默认100%
- 🔧作用：
  
  - 此函数函数用于设置中国银行”双向宝“合约交易的保证金比例
- ❗注意事项：
  
  - 此函数须在 `init(context)`函数下设置，否则无效
  - 如未进行此设置，则按银行规定的交易保证金比例执行
- 📝示例：
  
  ```python
  #设置双向宝合约保证金比例设为50%
  def init(context):
      set_margin_rate_fx(rate=50)
  ```

---

#### 设置"双向宝"交易手续费：set_commission_fx

- 👑调用方法：
  `set_commission_fx(cal_style)`
- 📚参数说明：
  
  - cal_style:PerShare或PerTrade对象
    - PerShare：**比例交易手续费**，例如 `PerTrade(cost=0.0002)`，表示手续费为交易额的0.02%
    - PerTrade：**固定交易手续费**，例如 `PerTrade(cost=5.0)`，表示每笔交易手续费5元
- 🔧作用：
  
  - set_commission_fx函数用来设置"双向宝"交易手续费，其不影响策略的运行
- ❗注意事项：
  
  - 该函数必须在 `init(context)`函数下设置, 否则无效
  - 如果整个双向宝策略没有该函数, 则默认交易手续费为0
- 📝示例：
  
  ```python
  def init(context):
      #初始化策略时设置双向宝交易手续费为交易额的0.02%
      set_commission_fx(PerShare(cost=0.0002))
  ```

---

#### 设置最大成交比例：set_volume_limit_fx

- 👑调用方法：
  `set_volume_limit_fx(volume_percent)`
- 📚参数说明：
  
  - volume_percent:最大成交量比例，如果set_volume_limit_fx(0.25), 则意味着若下单数量超过当前时间周期内的历史真实成交量的25%, 则全部不成交
- 🔧作用：
  
  - 该函数用来设置最大成交比例, 若下单数量超过当前时间周期的历史真实成交量一定比例, 则全部不成交
- ❗注意事项：
  
  - 该函数必须在 `init(context)`函数下设置, 否则无效
  - 如果策略没有该函数，则默认回测中下单量不能超过当前时间周期的历史真实成交量的25%, 策略模拟交易中不能超过前一时间周期的历史真实成交量的25%
- 📝示例：
  
  ```python
  def init(context):
      #设置"双向宝"最大成交比例25%
      set_volume_limit_fx(0.25)
  ```

---

#### 设置滑点：set_spread（不推荐使用）

- 👑调用方法：
  `set_spread(dif)`
- 📚参数说明：
  
  - dif:买卖价差比例(滑点)，如果set_sread(0.004), 则意味买入价为行情均价 * 1.002, 卖出价为行情均价 * 0.998
- 🔧作用：
  
  - 设置滑点（不推荐使用）
- ❗注意事项：
  
  - 该函数必须在 `init(context)`函数下设置, 否则无效
  - 如果策略没有该函数，则默认买入价为行情均价 * 1.002, 卖出价为行情均价 * 0.998
- 📝示例：
  
  ```python
  def init(context):
      #设置买卖价差比例为千分之五
      set_spread(0.005)
  ```

---

#### 风险度阈值设置函数：set_risk_border_fx

- 👑调用方法：
  `set_risk_border_fx(risk_border)`
- 📚参数说明：
  
  - risk_border:风险度阈值，例如set_risk_border_fx(1.4)表示风险度超过140%时将会不允许开新仓, 默认值为1.4
- 🔧作用：
  
  - 该函数是风险度阈值设置函数, 通过保证金占比判断能否开新仓
- ❗注意事项：
  
  - 该函数必须在 `init(context)`函数下设置, 否则无效
  - 若用户未使用该函数, 则默认风险度上限为140%
- 📝示例：
  
  ```python
  def init(context):
      #设置风险度上限为150%
      set_risk_border_fx(1.5)
  ```

---

#### 设置贵金属T+D合约的保证金比例：set_margin_rate_td

- 👑调用方法：
  `set_margin_rate_fx(autd=8.4, mautd=8.4, agtd=9.8)`
- 📚参数说明：
  
  - autd:Au(T+D)的保证金比例(%),默认8.4(%)
  - mautd:	mAu(T+D)的保证金比例(%),默认8.4(%)
  - agtd:Ag(T+D)的保证金比例(%),默认9.8(%)
- 🔧作用：
  
  - 用来设置贵金属T+D合约的保证金比例, 该函数的默认参数为中国银行的规定保证金比例
- ❗注意事项：
  
  - 此函数须在 `init(context)`函数下设置，否则无效
  - 如未进行此设置，则按银行规定的交易保证金比例执行
- 📝示例：
  
  ```python
  def init(context):
      #设置Au(T+D)合约保证金比例设为9.8%
      #mAu(T+D)合约保证金比例设为9.8%
      #Ag(T+D)合约保证金比例设为12.6%
      set_margin_rate_td(autd=9.8, mautd=9.8, agtd=12.6)
  ```

---

#### 设置T+D合约交易手续费：set_commission_td

- 👑调用方法：
  `set_commission_td(cal_style)`
- 📚参数说明：
  
  - cal_style:PerShare或PerTrade对象
    - PerShare：**比例交易手续费**，例如 `PerTrade(cost=0.0002)`，表示手续费为交易额的0.02%
    - PerTrade：**固定交易手续费**，例如 `PerTrade(cost=5.0)`，表示每笔交易手续费5元
- 🔧作用：
  
  - 此函数用来设置T+D合约交易手续费，其不影响策略的运行
- ❗注意事项：
  
  - 该函数必须在 `init(context)`函数下设置, 否则无效
  - 如果整个策略没有该函数, 则默认交易手续费为交易额的0.02%
- 📝示例：
  
  ```python
  def init(context):
      #初始化策略时设置T+D合约交易手续费为交易额的0.02%
      set_commission_td(PerShare(cost=0.0002))
  ```

---

#### 设置最大成交比例：set_volume_limit_td

- 👑调用方法：
  `set_volume_limit_td(volume_percent)`
- 📚参数说明：
  
  - volume_percent:最大成交量比例，如果set_volume_limit_td(0.25), 则意味着若下单数量超过当前时间周期内的历史真实成交量的25%, 则全部不成交
- 🔧作用：
  
  - 该函数用来设置最大成交比例, 若下单数量超过当前时间周期的历史真实成交量一定比例, 则全部不成交
- ❗注意事项：
  
  - 该函数必须在 `init(context)`函数下设置, 否则无效
  - 如果策略没有该函数，则默认回测中下单量不能超过当前时间周期的历史真实成交量的25%, 策略模拟交易中不能超过前一时间周期的历史真实成交量的25%
- 📝示例：
  
  ```python
  def init(context):
      #设置T+D合约回测最大成交比例25%
      set_volume_limit_td(0.25)
  ```

---

#### 设置T+D合约交易滑点：set_slippage_td

- 👑调用方法：
  `set_slippage_td(slippage)`
  
  - slippage:PriceSlippage或FixedSlippage对象
    - PriceSlippage：**可变滑点对象**，例如PriceSlippage(0.1)，表示买入价为实际价格乘1.05，卖出价为实际价格乘0.95
    - FixedSlippage：**固定滑点对象**，例如FixedSlippage(10)，表示买入价为实际价格加5，卖出价为实际价格减5
- 🔧作用：
  
  - 该函数用来设置T+D合约交易滑点，其不影响策略的运行
- ❗注意事项：
  
  - 该函数必须在 `init(context)`函数下设置, 否则无效
  - 如果整个策略没有该函数，则默认无滑点
- 📝示例：
  
  ```python
  def init(context):
      #设置可变滑点2%
      set_slippage_td(PriceSlippage(0.02))
  ```

---

#### 风险度阈值设置函数：set_risk_border_td

- 👑调用方法：
  `set_risk_border_td(risk_border)`
- 📚参数说明：
  
  - risk_border:风险度阈值，例如set_risk_border_td(1.4)表示风险度超过140%时将会不允许开新仓, 默认值为1.4
- 🔧作用：
  
  - 该函数是风险度阈值设置函数, 通过保证金占比判断能否开新仓
- ❗注意事项：
  
  - 该函数必须在 `init(context)`函数下设置, 否则无效
  - 若用户未使用该函数, 则默认风险度上限为140%
- 📝示例：
  
  ```python
  def init(context):
      #设置风险度上限为150%
      set_risk_border_td(1.5)
  ```
---
-->

### 数据函数

#### 订阅标的：subscribe

- 👑调用方法
  ```python
  subscribe(id_or_symbols)
  ```
- 🔧作用
  - 订阅标的，使合约池内合约增加
- 📚参数说明
  - `id_or_symbols`: `str` 或 `list`，需要订阅的标的代码，支持单个订阅或多个订阅
- 🔢返回值说明
  - `None`
- ❗注意事项
  - 策略会根据订阅的标的所属的交易所交易时间的并集确定策略执行 `handle_bar`、`before_trading`、`after_trading`运行时间，默认为沪深交易所时间
  - 在tick级回测中必须订阅合约，否则不会触发tick行情事件
  - 在外汇(双向宝)策略中必须订阅合约
  - 在T+D合约策略中必须订阅合约
- 📝示例：
  - 调用
    ```python
    def init(context):
        #订阅螺纹主力合约
        subscribe('RB9999')
    ```
  - 返回值
    ```python
    None
    ```

#### 取消订阅标的：unsubscribe

- 👑调用方法
  ```python
  unsubscribe(id_or_symbols)
  ```
- 🔧作用
  - 取消订阅标的，使合约池内合约减少
- 📚参数说明
  - `id_or_symbols`: `str`或`list`，需要取消订阅的标的代码，支持单个取消订阅或多个取消订阅
- 🔢返回值说明
  - `None`
- 📝示例：
  - 调用
    ```python
    # 取消订阅螺纹主力合约
    unsubscribe('RB9999')

    # 批量取消订阅多个合约
    unsubscribe(['RB9999', 'HC9999'])
    ```
  - 返回值
    ```python
    None
    None
    ```

#### 获取当前bar的时间：get_datetime

- 👑调用方法
  ```python
  get_datetime()
  ```
- 🔧作用
  - 用于获取当前bar的时间。
- 📚参数说明
  - 无
- 🔢返回值说明
  - `datetime.datetime`，表示当前bar的时间。
- ❗注意事项
  - 该函数没有参数，直接使用。
  - 在tick级策略中使用时，返回当前交易日的开盘时间。
- 📝示例：
  - 调用
    ```python
    time = get_datetime()
    ```
  - 返回值
    ```python
    datetime.datetime(2024, 11, 13, 9, 31)
    ```

#### 获取上一个bar的时间：get_last_datetime

- 👑调用方法
  ```python
  get_last_datetime()
  ```
- 🔧作用
  - 用于获取上一个bar的时间。
- 📚参数说明
  - 无
- 🔢返回值说明
  - `pandas.Timestamp`，表示上一个bar的时间。
- ❗注意事项
  - 该函数没有参数，直接使用。
  - 在tick级策略中使用时，返回前一交易日的收盘时间。
- 📝示例：
  - 调用
    ```python
    last_datetime = get_last_datetime()
    ```
  - 返回值
    ```python
    Timestamp('2024-11-12 09:31:00')
    ```

#### 获取股票历史行情：history

- 👑调用方法
  ```python
  history(symbol_list, fields, bar_count, fre_step, skip_paused=False, fq='pre', df=True, is_panel=False)
  ```
- 🔧作用
  - 获取股票多属性的历史行情数据，仅可在策略API内使用
- 📚参数说明
  - `symbol_list`: `str`或`list`，标的代码，取单个股票数据时可以传入字符串，若需要取多个标的，需传入列表
  - `fields`: `list`，数据字段，支持字段可参考[A股日行情数据](https://quant.10jqka.com.cn/view/dataplatform/detail/8)、[A股分钟行情数据](https://quant.10jqka.com.cn/view/dataplatform/detail/12)
  - `bar_count`: `int`，历史长度，例如 `bar_count = 5`，表示获取过去5个时间步长的历史数据
  - `fre_step`: `str`，时间步长'Xd'/'Xm'，X必须为正整数，`fre_step = '1d'`表示时间步长为1天
  - `skip_paused`: `bool`，是否跳过停牌数据，默认`False`
  - `fq`: `Optional[str]`，复权选项
    - `fq='pre'`: 前复权
    - `fq='post'`: 后复权
    - `fq=None`: 不复权
  - `df`: `bool`，与`is_panel`共同决定返回值类型，详见返回值说明
  - `is_panel`: `bool`，与`df`共同决定返回值类型，详见返回值说明
- 🔢返回值说明
  - `symbol_list`为`list`，`is_panel`为True时，df`不生效，返回pd.Panel
  - `symbol_list`为`list`，`df`为True，`is_panel`为False时，返回`dict`，key为标的代码，value为`pd.DataFrame`(index是日期，columns为字段)
  - `symbol_list`为`list`，`df`为False，`is_panel`为False时，返回`dict`，key是标的代码，value是`dict`(key为字段，value为1维np.ndarray)
  - `symbol_list`为`str`，`df`为True时，`is_panel`不生效，返回`pd.DataFrame`，index是日期，columns为字段
  - `symbol_list`为`str`，`df`为False时，`is_panel`不生效，返回`dict`，key为字段，value为1维np.ndarray
- ❗注意事项
  - 由于策略框架的运行机制，取日频历史行情时，不包含当前bar的数据；取分钟频历史行情，包含当前bar数据
  - 当`fre_step`的X不等于1时，field仅支持'open','high','low','close','volume','turnover'这几个字段
- 📝示例：
  - 调用
    ```python
    history('000001.SZ',['close'],5,'1m',False,'pre',True,True)
    ```
  - 返回值
    ```python
    close
    2024-11-15 14:57:00  11.44
    2024-11-15 14:58:00  11.44
    2024-11-15 14:59:00  11.44
    2024-11-15 15:00:00  11.44
    2024-11-18 09:31:00  11.69
    ```

#### 当前bar行情数据：get_current

- 👑调用方法
  ```python
  get_current(inst_id_list)
  ```
- 🔧作用
  - 用于获取多只证券当前bar的行情数据。仅在策略框架内可用。
- 📚参数说明
  - `inst_id_list`: `str或list`，表示标的代码
- 🔢返回值说明
  - `dict`，key为标的代码，value为[`Bar`对象](https://quant.10jqka.com.cn/view/help/4#Bar%E7%B1%BB)
- 📝示例：
  - 调用
    ```python
    get_current(inst_id_list=['300033.SZ'])
    ```
  - 返回值
    ```python
    {'300033.SZ': Bar(symbol: '300033.SZ', datetime: datetime.datetime(2024, 11, 18, 9, 31), open: 271.0, high: 275.55, low: 270.3, close: 275.2, volume: 2021272.0, turnover: 550619639.86, high_limit: 327.0, low_limit: 218.0, prev_close: 272.5, avg_price: 272.41244120534003, is_st: False, is_paused: False)}
    ```

#### 获取期货历史行情：history_future

- 👑调用方法
  ```python
  history_future(symbol_list, fields, bar_count, fre_step, skip_paused=False, fq='pre', is_panel=False)
  ```
- 🔧作用
  - 获取股票多属性的历史行情数据，仅可在策略API内使用
- 📚参数说明
  - `symbol_list`: `str`或`list`，标的代码，取单个股票数据时可以传入字符串，若需要取多个标的，需传入列表
  - `fields`: `list`，数据字段，支持字段可参考[期货日行情数据](https://quant.10jqka.com.cn/view/dataplatform/detail/174)、[期货分钟行情数据](https://quant.10jqka.com.cn/view/dataplatform/detail/422)
  - `bar_count`: `int`，历史长度，例如 `bar_count = 5`，表示获取过去5个时间步长的历史数据
  - `fre_step`: `str`，时间步长'Xd'/'Xm'，X必须为正整数，`fre_step = '1d'`表示时间步长为1天
  - `skip_paused`: `bool`，是否跳过停牌数据，默认`False`
  - `fq`: `Optional[str]`，复权选项
    - `fq='pre'`: 前复权
    - `fq='post'`: 后复权
    - `fq=None`: 不复权
  - `is_panel`: `bool`，决定返回值类型，详见返回值说明
- 🔢返回值说明
  - `is_panel`为True时，返回pd.Panel
  - `is_panel`为False时，返回`dict`，key为标的代码，value为`pd.DataFrame`(index是日期，columns为字段)
- ❗注意事项
  - 由于策略框架的运行机制，取日频历史行情时，不包含当前bar的数据；取分钟频历史行情，包含当前bar数据
  - 当`fre_step`的X不等于1时，field仅支持'open','high','low','close','volume','turnover'这几个字段
- 📝示例：
  - 调用
    ```python
    history_future('RB8888', ['close'], 5, '1m', False, 'pre')
    ```
  - 返回值
    ```python
    {'RB8888':                          close
    2024-11-18 09:28:00  3283.0085
    2024-11-18 09:29:00  3283.1423
    2024-11-18 09:30:00  3284.7830
    2024-11-18 09:31:00  3285.0599
    2024-11-18 09:32:00  3284.9491}
    ```

#### 获取历史tick行情快照：history_ticks

- 🔧作用：

  - 获取历史tick行情快照数据,仅可在策略API内使用
- 👑调用方法：

  ```python
  history_ticks(
      symbol_list,
      fields,
      bar_count, 
      is_panel=0
  )
  ```
- 📚参数说明：

  - symbol_list:str或list，标的代码,取单个合约数据时可以传入字符串，若需要取多个合约，需传入列表
  - fields:list,数据字段,支持字段可参考[历史行情快照数据](https://quant.10jqka.com.cn/view/dataplatform/detail/16)
  - bar_count:历史长度，例如 `bar_count = 5`，表示获取过去5个时间步长的历史数据
  - is_panel:返回数据格式是否为panel，默认 `is_panel = 0`
    - `is_panel = 0`: 返回 `dict`对象，其key是symbol即证券代码、值是 `pandas.Dataframe`，行索引是 `datetime.datetime`对象，列索引是字段名称
    - `is_panel = 1`: 返回 `Panel`对象，key为fileds字段。`Panel`为 `pandas.DataFrame`的三维结构，选定字段后输出的便是 `pandas.DataFrame`对象
- ❗注意事项：

  - 只能在tick级策略中使用
- 📝示例：

  ```python
  def init(context):
      #设定标的代码
      context.symbol = ['000001.SZ']
      subscribe(context.symbol)

  def handle_tick(context,tick):
      price=history_ticks(context.symbol, ['open','prev_close'], 10, is_panel=0)
      log.info(price)
  ```

---

<!--

#### 获取中国银行'双向宝'合约历史行情：history_fx

- 🔧作用：
  
  - 获取中国银行'双向宝'合约多属性的历史行情数据,仅可在外汇策略内使用
- 👑调用方法：
  
  ```python
  history_fx(
      symbol_list,
      fields,
      bar_count, 
      fre_step,
      is_panel=0
  )
  ```
- 📚参数说明：
  
  - symbol_list:str或list，标的代码,取单个合约数据时可以传入字符串，若需要取多个合约，需传入列表
  - fields:list,数据字段,支持字段可参考[外汇日行情数据](https://quant.10jqka.com.cn/view/dataplatform/detail/324)、[外汇分钟行情数据](https://quant.10jqka.com.cn/view/dataplatform/detail/325)
  - bar_count:历史长度，例如 `bar_count = 5`，表示获取过去5个时间步长的历史数据
  - fre_step:时间步长'Xd'/'Xm',X必须为正整数，`fre_step = '1d'`表示时间步长为1天
  - is_panel:返回数据格式是否为panel，默认 `is_panel = 0`
    - `is_panel = 0`: 返回 `dict`对象，其key是symbol即证券代码、值是 `pandas.Dataframe`，行索引是 `datetime.datetime`对象，列索引是字段名称
    - `is_panel = 1`: 返回 `Panel`对象，key为fileds字段。`Panel`为 `pandas.DataFrame`的三维结构，选定字段后输出的便是 `pandas.DataFrame`对象
- ❗注意事项：
  
  - 由于策略框架的运行机制，取日频历史行情时，不包含当前bar的数据；取分钟频历史行情，包含当前bar数据
- 📝示例：
  
  ```python
  def init(context):
      #设定期货品种代码
      subscribe('XAUUSD')
  
  def handle_bar(context,bar_dict):
      price = history_fx(['USDJPY','XAUUSD'], ['open','close'], 3, '1d', is_panel=0)
      log.info(price['XAUUSD'])
  ```

---

#### 获取当前bar的时间：get_datetime_fx

- 👑调用方法：
  `get_datetime_fx()`
- 🔧作用：
  
  - 获取当前bar的时间,外汇策略中专用
- ❗注意事项：
  
  - 该函数没有参数，直接使用
- 📝示例：
  
  ```python
  from datetime import timedelta as td
  
  def init(context):
      subscribe('USDJPY') 
  
  def handle_bar(context,bar_dict):
      # 获取当前bar的时间
      time = get_datetime()
      log.info(time)
      # 获取回测前一天日期
      yesterday_time = get_datetime_fx()-td(days=1)
      yesterday_date = yesterday_time.strftime("%Y%m%d")
      log.info(yesterday_date)
  ```

---

#### 获取上一个bar的时间：get_last_datetime_fx

- 👑调用方法：
  `get_last_datetime_fx()`
- 🔧作用：
  
  - 获取上一个bar的时间,外汇策略中专用
- ❗注意事项：
  
  - 该函数没有参数，直接使用
- 📝示例：
  
  ```python
  def init(context):
      subscribe('USDJPY')
  
  def handle_bar(context,bar_dict):
      # 获取上一个bar的时间
      last_datetime = get_last_datetime_fx()
      log.info('回测前一个handle_bar调用时间：'+str(last_datetime))
  ```

---

#### 获取T+D合约历史行情：history_td

- 🔧作用：
  
  - 获取T+D合约多属性的历史行情数据,仅可在T+D策略内使用
- 👑调用方法：
  
  ```python
  history_td(
      symbol_list,
      fields,
      bar_count, 
      fre_step,
      is_panel=0
  )
  ```
- 📚参数说明：
  
  - symbol_list:str或list，标的代码,取单个合约数据时可以传入字符串，若需要取多个合约，需传入列表
  - fields:list,数据字段,支持字段可参考[T+D合约日行情数据](https://quant.10jqka.com.cn/view/dataplatform/detail/185)、[T+D合约分钟行情数据]()
  - bar_count:历史长度，例如 `bar_count = 5`，表示获取过去5个时间步长的历史数据
  - fre_step:时间步长'Xd'/'Xm',X必须为正整数，`fre_step = '1d'`表示时间步长为1天
  - is_panel:返回数据格式是否为panel，默认 `is_panel = 0`
    - `is_panel = 0`: 返回 `dict`对象，其key是symbol即证券代码、值是 `pandas.Dataframe`，行索引是 `datetime.datetime`对象，列索引是字段名称
    - `is_panel = 1`: 返回 `Panel`对象，key为fileds字段。`Panel`为 `pandas.DataFrame`的三维结构，选定字段后输出的便是 `pandas.DataFrame`对象
- ❗注意事项：
  
  - 由于策略框架的运行机制，取日频历史行情时，不包含当前bar的数据；取分钟频历史行情，包含当前bar数据
- 📝示例：
  
  ```python
  def init(context):
      #设定期货品种代码
      subscribe('AUTD')
  
  def handle_bar(context,bar_dict):
      price = history_td(['AUTD','AGTD'], ['open','close'], 3, '1d', is_panel=0)
      log.info(price['AUTD'])
  ```

---

#### 获取当前bar的时间：get_datetime_td

- 👑调用方法：
  `get_datetime_td()`
- 🔧作用：
  
  - 获取当前bar的时间,仅在T+D合约策略中可用
- ❗注意事项：
  
  - 该函数没有参数，直接使用
- 📝示例：
  
  ```python
  from datetime import timedelta as td
  
  def init(context):
      subscribe('AUTD') 
  
  def handle_bar(context,bar_dict):
      # 获取当前bar的时间
      time = get_datetime()
      log.info(time)
      # 获取回测前一天日期
      yesterday_time = get_datetime_td()-td(days=1)
      yesterday_date = yesterday_time.strftime("%Y%m%d")
      log.info(yesterday_date)
  ```

---

#### 获取上一个bar的时间：get_last_datetime_td

- 👑调用方法：
  `get_last_datetime_td()`
- 🔧作用：
  
  - 获取上一个bar的时间,仅在T+D合约策略中可用
- ❗注意事项：
  
  - 该函数没有参数，直接使用
- 📝示例：
  
  ```python
  def init(context):
      subscribe('AUTD')  
  
  def handle_bar(context,bar_dict):
      # 获取上一个bar的时间
      last_datetime = get_last_datetime_td()
      log.info('回测前一个handle_bar调用时间：'+str(last_datetime))
  ```

---

-->

### 交易函数

#### 股票

##### 下单函数，根据数量下单：order

- 👑调用方法
  ```python
  order(id_or_ins, amount, price=None)
  ```
- 🔧作用
  - 用于下单，根据数量下单
- 📚参数说明
  - `id_or_ins`: `str`，表示合约代码
  - `amount`: `int`，表示下单数量，负数为卖出
  - `price`: `Optional[float]`，表示限价单价格上界，`None`表示市价
- 🔢返回值说明
  - `str`或`None`，如果订单有效，则返回订单唯一编号，如`ord8a8d6e4bad7441679eb1f34164c9c6dd`，否则返回`None`
- ❗注意事项
  - **下单失败可能由于如下原因**
    - 标的不存在
    - 可用资金不足或可用持仓不足
  - **下单设置和实际下单存在差异，会在日志中添加警告信息**
    - 买入股票时，下单数量受到当前账户可用资金的限制
    - 卖出股票时，下单数量受到持仓可卖数量的影响
  - **下单数量为0时，会在日志中添加警告信息**
- 📝示例：
  - 调用
    ```python
    order('510300.SH', 100, price=2.8)
    ```
  - 返回值
    ```python
    'ord8a8d6e4bad7441679eb1f34164c9c6dd'
    ```

##### 下单函数，根据金额下单：order_value

- 👑调用方法
  ```python
  order_value(id_or_ins, cash_amount, price=None)
  ```
- 🔧作用
  - 用于根据指定金额下单，支持买入（正数）或卖出（负数），自动计算可交易数量
- 📚参数说明
  - `id_or_ins`: `str`，表示合约代码
  - `cash_amount`: `float`，表示下单金额，负数表示卖出
  - `price`: `float`或`None`，表示限价单价格上界，`None`表示市价
- 🔢返回值说明
  - `str`或`None`，如果订单有效，则返回订单唯一编号，如`ord8a8d6e4bad7441679eb1f34164c9c6dd`，否则返回`None`
- ❗注意事项
  - **下单失败可能由于如下原因**：
    - 标的不存在
    - 可用资金不足或可用持仓不足
  - **下单设置和实际下单存在差异，会在log中添加警告信息**：
    - 买入股票时，下单数量受到当前账户可用资金的限制
    - 卖出股票时，下单数量受到持仓可卖数量的影响
- 📝示例：
  - 调用
    ```python
    order_value('510300.SH', 100000, price=2.8)
    ```
  - 返回值
    ```python
    'ord8a8d6e4bad7441679eb1f34164c9c6dd'
    ```

##### 下单函数，根据比例下单：order_percent

- 👑调用方法
  ```python
  order_percent(id_or_ins, percent, price=None)
  ```
- 🔧作用
  - 根据当前总资产比例确定下单金额，执行买入或卖出操作
- 📚参数说明
  - `id_or_ins`: `str`，表示合约代码
  - `percent`: `float`，表示下单比例，负数为卖出
  - `price`: `float`或`None`，表示限价单价格上界，`None`表示市价
- 🔢返回值说明
  - `str`或`None`，如果订单有效，则返回订单唯一编号，如`ord8a8d6e4bad7441679eb1f34164c9c6dd`，否则返回`None`
- ❗注意事项
  - **下单失败可能由于如下原因：**
    - 标的不存在
    - 可用资金不足（买入时）或可用持仓不足（卖出时）
  - **下单设置和实际下单存在差异，系统会在log中添加警告信息：**
    - 买入股票时，下单数量受当前账户可用资金限制
    - 卖出股票时，下单数量受持仓可卖数量限制
- 📝示例：
  - 调用
    ```python
    order_percent('510300.SH', 0.1, price=2.8)
    ```
  - 返回值
    ```python
    'ord8a8d6e4bad7441679eb1f34164c9c6dd'
    ```

##### 下单函数，根据目标持仓下单：order_target

- 👑调用方法
  ```python
  order_target(id_or_ins, amount, price=None)
  ```
- 🔧作用
  - 下单函数，根据目标持仓数量确定下单数量
- 📚参数说明
  - `id_or_ins`: `str`，合约代码
  - `amount`: `int`，目标持仓数量
  - `price`: `float`或`None`，表示限价单价格上界，`None`表示市价
- 🔢返回值说明
  - `str`或`None`，如果订单有效，则返回订单唯一编号，如`ord8a8d6e4bad7441679eb1f34164c9c6dd`，否则返回`None`
- ❗注意事项
  - **下单失败可能由于如下原因**
    - 标的不存在
    - 可用资金不足或可用持仓不足
  - **下单设置和实际下单存在差异，会在log中添加警告信息**
    - 买入股票时，下单数量受到当前账户可用资金的限制
    - 卖出股票时，下单数量受到持仓可卖数量的影响
- 📝示例：
  - 调用
    ```python
    order_target('510300.SH', 1000, price=2.8)
    ```
  - 返回值
    ```python
    'ord8a8d6e4bad7441679eb1f34164c9c6dd'
    ```

##### 下单函数，根据目标持有金额下单：order_target_value

- 👑调用方法
  ```python
  order_target_value(id_or_ins, cash_amount, price=None)
  ```
- 🔧作用
  - 下单函数，根据目标持有的金额确定下单数量
- 📚参数说明
  - `id_or_ins`: `str`，合约代码
  - `cash_amount`: `float`，目标持仓金额
  - `price`: `float`或`None`，表示限价单价格上界，`None`表示市价
- 🔢返回值说明
  - `str`或`None`，如果订单有效，则返回订单唯一编号，如`ord8a8d6e4bad7441679eb1f34164c9c6dd`，否则返回`None`
- ❗注意事项
  - **下单失败可能由于如下原因**
    - 标的不存在
    - 可用资金不足或可用持仓不足
  - **下单设置和实际下单存在差异，会在log中添加警告信息**
    - 买入股票时，下单数量受到当前账户可用资金的限制
    - 卖出股票时，下单数量受到持仓可卖数量的影响
- 📝示例：
  - 调用
    ```python
    order_target_value('510300.SH', 100000, price=2.8)
    ```
  - 返回值
    ```python
    'ord8a8d6e4bad7441679eb1f34164c9c6dd'
    ```

##### 下单函数，根据目标持仓比例下单：order_target_percent

- 👑调用方法
  ```python
  order_target_percent(id_or_ins, percent, price=None)
  ```
- 🔧作用
  - 下单函数，根据目标持仓比例确定下单数量
- 📚参数说明
  - `id_or_ins`: `str`，合约代码
  - `percent`: `float`，目标持仓比例
  - `price`: `float`或`None`，表示限价单价格上界，`None`表示市价
- 🔢返回值说明
  - `str`或`None`，如果订单有效，则返回订单唯一编号，如`ord8a8d6e4bad7441679eb1f34164c9c6dd`，否则返回`None`
- ❗注意事项
  - **下单失败可能由于如下原因**
    - 标的不存在
    - 可用资金不足或可用持仓不足
  - **下单设置和实际下单存在差异，会在log中添加警告信息**
    - 买入股票时，下单数量受到当前账户可用资金的限制
    - 卖出股票时，下单数量受到持仓可卖数量的影响
- 📝示例：
  - 调用
    ```python
    order_target_percent('510300.SH', 0.1, price=2.8)
    ```
  - 返回值
    ```python
    'ord8a8d6e4bad7441679eb1f34164c9c6dd'
    ```

##### 获得委托详情：get_orders

- 👑调用方法
  ```python
  get_orders(order_id=None, order_book_id=None)
  ```
- 🔧作用
  - 查询函数，用于获得委托详情，支持指定订单编号或标的代码，仅返回当日委托
- 📚参数说明
  - `order_id`: `Optional[str]`，指定订单编号，由下单函数返回
  - `order_book_id`: `Optional[str]`，指定标的代码
- 🔢返回值说明
  - `list`或`None`，当日无委托则返回`None`，否则返回[`Order`](https://quant.10jqka.com.cn/view/help/4#%E8%AE%A2%E5%8D%95%E5%AF%B9%E8%B1%A1-Order%E7%B1%BB)对象的列表，若不传入`order_id`和`order_book_id`，则返回当天所有委托
- 📝示例：
  - 调用
    ```python
    odr_id = order('000001.SZ', 200)
    print(get_orders(odr_id))
    ```
  - 返回值
    ```python
    [Order({'order_id': 'aade994938b64871a4191971e8501eaf', 'symbol': '000001.SZ', 'created': datetime.datetime(2024, 11, 18, 9, 31), 'order_type': 'LONG', 'limit_price': 0, 'amount': 8500, 'filled_amount': 8500, 'type': ORDER_TYPE.MARKET, 'transaction_cost': 19.820427500000005, 'avg_price': 11.659075000000001, 'status': ORDER_STATUS.FILLED, 'datetime': datetime.datetime(2024, 11, 18, 9, 31), 'offset_flag': None})]
    ```

##### 获取当日所有未完成委托详情：get_open_orders

- 👑调用方法
  ```python
  get_open_orders(order_id=None, order_book_id=None)
  ```
- 🔧作用
  - 查询函数，用于获得当日所有未完成的委托详情，支持指定订单编号或标的代码
- 📚参数说明
  - `order_id`: `Optional[str]`，指定订单编号，由下单函数返回
  - `order_book_id`: `Optional[str]`，指定标的代码
- 🔢返回值说明
  - `list`或`None`，当日无未完成委托则返回`None`，否则返回[`Order`](https://quant.10jqka.com.cn/view/help/4#%E8%AE%A2%E5%8D%95%E5%AF%B9%E8%B1%A1-Order%E7%B1%BB)对象的列表，若不传入`order_id`和`order_book_id`，则返回当天所有未完成委托
- 📝示例：
  - 调用
    ```python
    odr_id = order('000001.SZ', 200)
    print(get_open_orders(odr_id))
    ```
  - 返回值
    ```python
    [Order({'order_id': 'aade994938b64871a4191971e8501eaf', 'symbol': '000001.SZ', 'created': datetime.datetime(2024, 11, 18, 9, 31), 'order_type': 'LONG', 'limit_price': 0, 'amount': 8500, 'filled_amount': 8500, 'type': ORDER_TYPE.MARKET, 'transaction_cost': 19.820427500000005, 'avg_price': 11.659075000000001, 'status': ORDER_STATUS.FILLED, 'datetime': datetime.datetime(2024, 11, 18, 9, 31), 'offset_flag': None})]
    ```

##### 获取当日所有成交详情：get_tradelogs

```python
get_tradelogs(order_id=None, order_book_id=None)
```

- 🔧作用
  - 查询函数，用于获取当日所有成交详情，支持指定订单编号或标的代码
- 📚参数说明
  - `order_id`: `Optional[str]`，表示订单ID
  - `order_book_id`: `Optional[str]`，表示证券代码
- 🔢返回值说明
  - `list`或`None`，当日无成交则返回`None`，否则返回[`Trade`](https://quant.10jqka.com.cn/view/help/4#%E6%88%90%E4%BA%A4%E5%AF%B9%E8%B1%A1-Trade%E7%B1%BB)对象的列表，若不传入`order_id`和`order_book_id`，则返回当天所有成交
- 📝示例：
  - 调用
    ```python
    def init(context):   
        pass

    def handle_bar(context, bar_dict):
        odr_id_1 = order('000001.SZ', 200)
        log.info(get_tradelogs())
    ```
  - 返回值
    ```python
    [Trade({'order_book_id': '000001.SZ', 'trading_datetime': datetime.datetime(2024, 11, 19, 9, 31), 'datetime': datetime.datetime(2024, 11, 19, 9, 31), 'order_id': '97ae3e30206d4d3fa5d28a15d0b08018', 'last_price': 11.779375, 'last_quantity': 8400, 'commission': 19.789350000000002, 'tax': 0, 'transaction_cost': 19.789350000000002, 'side': SIDE.BUY, 'position_effect': None, 'exec_id': 'e4815a0f45954586b221d4a2ae4530d1', 'frozen_price': 11.75, 'close_today_amount': 0, 'pnl': None})]
    ```

##### 撤销未完成委托订单：cancel_order

- 👑调用方法
  ```python
  cancel_order(order)
  ```
- 🔧作用
  - 用于撤销未完成委托订单
- 📚参数说明
  - `order`: 可以是`Order`对象，也可以是订单id
- 🔢返回值说明
  - `None`或`list`，撤单失败返回`None`，否则返回`Order`对象列表，里面的元素是撤单指定委托
- 📝示例：
  - 调用
    ```python
    # 以开盘价买入平安银行股票1000股  
    oid = order('000001.SZ', 1000)
    cancel_order(orders)
    ```
  - 返回值
    ```python
    None # 委托已经成交，撤单失败，返回None
    ```

##### 撤销所有未完成委托订单：cancel_order_all

- 👑调用方法
  ```python
  cancel_order_all()
  ```
- 🔧作用
  - 用于撤销所有未完成委托订单
- 🔢返回值说明
  - `None`或`list`，撤单失败返回`None`，否则返回`Order`对象列表，里面的元素是撤单指定委托
- 📝示例：
  - 调用
    ```python
    # 以开盘价买入平安银行股票1000股  
    oid = order('000001.SZ', 1000)
    cancel_order_all()
    ```
  - 返回值
    ```python
    None # 委托已经成交，撤单失败，返回None
    ```

#### 期货

##### 下单函数，根据数量下单：order_future

- 👑调用方法：
  `order_future(symbol,amount,offset_flag,order_type,limit_price=None)`
- 🔧作用：

  - 下单函数，根据手数下单购买期货合约
- 📚参数说明：

  - symbol：合约代码，str
  - amount：委托数量（手），float
  - offset\_flag：开平仓标识，str，'open'为开仓，'close'为平仓
  - order\_type：多空仓标识，str，'long'为多仓，'short'为空仓
  - limit\_price：限定价格，float，默认为None，表示市价即时单，否则委托单变为限价即时单
- 📝示例：

  ```python
  #初始化账户  
  def init(context):  
      set_subportfolios([{'type':'FUTURE','cash':10000000}])
      #设定期货品种代码  
      context.symbol = 'RB1812'  

  def handle_bar(context,bar_dict):  
      #下单10手螺纹钢1812合约，开多仓
      order_future(context.symbol,10,"open","long",limit_price=None)
  ```

---

##### 下单函数，平今仓单：order_close_today

- 👑调用方法：
  `order_close_today(symbol,amount,order_type,limit_price=None)`
- 🔧作用：

  - 平今仓单，仅仅能够平掉今天新开的仓位
- 📚参数说明：

  - symbol：合约代码，str
  - amount：委托数量（手），float
  - order\_type：多空仓标识，str，'long'为多仓，'short'为空仓
  - limit\_price：限定价格，float，默认为None，表示市价即时单，否则委托单变为限价即时单
- 📝示例：

  ```python
  #初始化账户  
  def init(context):  
      set_subportfolios([{'type':'FUTURE','cash':10000000}])
      #设定期货品种代码  
      context.symbol=    'RB1812'  

  def handle_bar(context,bar_dict):  
      #下单10手螺纹钢1812合约，开多仓
      order_future(context.symbol,10,"open","long")
      #平今仓5手螺纹钢1812合约
      order_close_today(context.symbol, 5,'long',limit_price=None)
  ```

---

#### 期权

##### 下单函数，根据数量下单：order_option

- 👑调用方法：
  `order_option(order_book_id, amount, side, position_effect, price=None)`
- 🔧作用：

  - 期权下单函数
- 📚参数说明：

  - order\_book\_id：期权代码，str
  - amount：委托数量（手），float
  - side：方向，str，'buy'为多仓，'sell'为空仓
  - position\_effect：开平仓，str，'open'为开仓，'close'为平仓
  - price：限定价格，float，默认为None，表示市价即时单，否则委托单变为限价即时单
- 📝示例：

  ```python
  def init(context):
      set_subportfolios([{'cash': 100000, 'type': 'option'}])
      set_option_commission(5)        # 默认也是5
      g.ins= '10001485.SH'            # 看跌，20181128行权价2.7
      g.day = 1

  def handle_bar(context, bar_dict):
      if g.day == 1:
          order_option(g.ins, 10, 'buy', 'open')
      elif g.day == 2:
          order_option(g.ins, 10, 'sell', 'close')
      g.day += 1
  ```

---

<!--

#### 外汇

##### 下单函数：order_fx

- 👑调用方法：
  `order_fx(symbol, amount, side=’buy’, position_effect=’open’, close_today=False, price=None)`
- 🔧作用：
  
  - 外汇API中的下单函数,根据手数下单购买双向宝合约，1手为100单位目标货币，下单手数必须为整数
- 📚参数说明：
  
  - order\_book\_id：期权代码，str
  - amount：委托数量（手），float
  - side：方向，str，'buy'为多仓，'sell'为空仓，默认为'buy'
  - position\_effect：开平仓，str，'open'为开仓，'close'为平仓
  - close_today:是否平今，bool，True表示若平仓会平今仓, False表示若平仓不会平今仓, 默认为False
  - price：限定价格，float，默认为None，表示市价即时单，否则委托单变为限价即时单
- ❗注意事项：
  
  - **下单失败可能由于如下原因**
    - 标的不存在
    - 可用资金不足或可用持仓不足
  - **下单设置和实际下单存在差异，会在log中添加警告信息**
    - 买入股票时，下单数量受到当前账户可用资金的限制
    - 卖出股票时，下单数量受到持仓可卖数量的影响
- 📝示例：
  
  ```python
  def init(context):   
      #设置要交易的合约(美日货币对合约) 
      g.contract = 'USDJPY'  
      subscribe(g.contract)
  
  #设置买卖条件，每个交易频率（日/分钟）调用一次   
  def handle_bar(context, bar_dict):
      #做多开仓买入1手
      order_fx(g.contract, 1, 'buy', 'open')
  ```

---

##### 获取订单详情：get_order_fx

- 👑调用方法：
  `get_order_fx(id)`
- 🔧作用：
  
  - 外汇API中获取订单详情
- 📚参数说明：
  
  - id:订单编号，由下单函数返回
- ❗注意事项：
  
  - 该函数用来获取订单详情，只需要在下单函数植入id即可.随后将id放入get_order_fx(id)
  - 如需查看详情，还需要log.info(get_order_fx(id))来打印数据
- 📝示例：
  
  ```python
  def init(context):   
      #设置要交易的合约  
      subscribe(id_or_symbols = ['USDJPY', 'AUDUSD'])
  
  #设置买卖条件，每个交易频率（日/分钟/tick）调用一次   
  def handle_bar(context, bar_dict):   
      order_id = order_fx('AUDUSD', 10, 'buy', 'open')
      log.info(get_order_fx(order_id))
  ```

---

##### 获取当日所有未完成订单：get_open_orders_fx

- 👑调用方法：
  `get_open_orders_fx()`
- 🔧作用：
  
  - 外汇API中一次性获取当日所有未完成订单
- ❗注意事项：
  
  - 一般回测时，下单都是全部完全的，当没有未完成订单时，会返回None

---

##### 撤销未完成委托订单：cancel_order_fx

- 👑调用方法：
  `cancel_order_fx(order)`
- 🔧作用：
  
  - 在外汇API中，用于撤销未完成委托订单
- 📚参数说明：
  
  - order:可以是order订单对象，也可以是订单id
- ❗注意事项：
  
  - 若订单处于不可撤销的状态，此函数会报错，可配合try关键字使用
- 📝示例：
  
  ```python
  def init(context):  
      #设置要交易的合约  
      g.contract = 'USDJPY'  
      subscribe('USDJPY')
  
  #设置买卖条件，每个交易频率（日/分钟/tick）调用一次  
  def handle_bar(context, bar_dict):  
      order_id = order_fx(g.contract, 1, 'buy', 'open', price=0.1)
      log.info(get_open_orders_fx(order_id))
      cancel_order_fx(order_id)
  ```

---

#### T+D

##### 下单函数，根据数量下单：order_td

- 👑调用方法：
  `order_td(symbol, amount, side='buy', position_effect='open', close_today=False, price=None)`
- 🔧作用：
  
  - T+D API中的下单函数,根据数量下单，支持交易Au(T+D)、mAu(T+D)、Ag(T+D)
- 📚参数说明：
  
  - symbol：期权代码，str
  - amount：委托数量（手），float
  - side：方向，str，'buy'为多仓，'sell'为空仓，默认为'buy'
  - position\_effect：开平仓，str，'open'为开仓，'close'为平仓
  - close_today:是否平今，bool，True表示若平仓会平今仓, False表示若平仓不会平今仓, 默认为False
  - price：限定价格，float，默认为None，表示市价即时单，否则委托单变为限价即时单
- ❗注意事项：
  
  - **下单失败可能由于如下原因**
    - 标的不存在
    - 可用资金不足或可用持仓不足
  - **下单设置和实际下单存在差异，会在log中添加警告信息**
    - 买入股票时，下单数量受到当前账户可用资金的限制
    - 卖出股票时，下单数量受到持仓可卖数量的影响
- 📝示例：
  
  ```python
  def init(context):   
      #设置要交易的合约(AuT+D合约)   
      g.contract = 'AUTD'   
      subscribe('AUTD')
  
  #设置买卖条件，每个交易频率（日/分钟）调用一次   
  def handle_bar(context, bar_dict):
      #做多开仓买入1手Au(T+D)合约
      order_td(g.contract, 1, 'buy', 'open')
  ```

---

##### 获取订单详情：get_order_td

- 👑调用方法：
  `get_order_td(id)`
- 🔧作用：
  
  - T+D API中获取订单详情
- 📚参数说明：
  
  - id:订单编号，由下单函数返回
- ❗注意事项：
  
  - 该函数用来获取订单详情，只需要在下单函数植入id即可.随后将id放入get_order_td(id)
  - 如需查看详情，还需要log.info(get_order_td(id))来打印数据
- 📝示例：
  
  ```python
  def init(context):   
      #设置要交易的合约(AuT+D合约)   
      g.contract = 'AUTD'   
      subscribe('AUTD')
  
  #设置买卖条件，每个交易频率（日/分钟）调用一次   
  def handle_bar(context, bar_dict):
      #做多开仓买入1手Au(T+D)合约
      order_id = order_td(g.contract, 1, 'buy', 'open')
      log.info(get_order_td(order_id))
  ```

---

##### 获取当日所有未完成订单：get_open_orders_td

- 👑调用方法：
  `get_open_orders_td()`
- 🔧作用：
  
  - T+D API中一次性获取当日所有未完成订单
- ❗注意事项：
  
  - 一般回测时，下单都是全部完全的，当没有未完成订单时，会返回None

---

##### 撤销未完成委托订单：cancel_order_td

- 👑调用方法：
  `cancel_order_td(order)`
- 🔧作用：
  
  - 在外汇API中，用于撤销未完成委托订单
- 📚参数说明：
  
  - order:可以是order订单对象，也可以是订单id
- ❗注意事项：
  
  - 若订单处于不可撤销的状态，此函数会报错，可配合try关键字使用
- 📝示例：
  
  ```python
  def init(context):  
      #设置要交易的合约  
      g.contract = 'AUTD'  
      subscribe('AUTD')
  
  #设置买卖条件，每个交易频率（日/分钟/tick）调用一次  
  def handle_bar(context, bar_dict):  
      order_id = order_td(g.contract, 1, 'buy', 'open', price=0.1)
      log.info(get_open_orders_td(order_id))
      cancel_order_td(order_id)
  ```

---

-->

#### 场外基金

##### 申购基金：order_fund

- 👑调用方法：
  `order_fund(order_book_id, value)`
- 🔧作用：

  - 在场外基金API中，用于申购基金
- 📚参数说明：

  - order\_book\_id：基金代码，str
  - value：下单金额，float
- ❗注意事项：

  - 只支持金额下单
  - 下单成功返回order_id，下单失败返回None
- 📝示例：

  ```python
  def init(context):
      # 设置3个子账户，股票，期货，场外基金初始资金都为100000
      set_subportfolios([{'cash': 100000, 'type': 'fund'}, {'cash': 100000, 'type': 'future'}, {'cash': 100000, 'type': 'stock'}])
      context.ins = '000717.OF'

  def handle_bar(context, bar_dict):
      order_id = order_fund(context.ins, 1000)
      log.info('申购', order_id)
  ```

---

##### 赎回基金：redeem_fund

- 👑调用方法：
  `redeem_fund(order_book_id, amount)`
- 🔧作用：

  - 在场外基金API中，用于赎回基金
- 📚参数说明：

  - order\_book\_id：基金代码，str
  - amount：下单份额，float
- ❗注意事项：

  - 只支持份额下单
  - 下单成功返回order_id，下单失败返回None
- 📝示例：

  ```python
  def init(context):
      # 设置3个子账户，股票，期货，场外基金初始资金都为100000
      set_subportfolios([{'cash': 100000, 'type': 'fund'}, {'cash': 100000, 'type': 'future'}, {'cash': 100000, 'type': 'stock'}])
      context.ins = '000717.OF'

  def handle_bar(context, bar_dict):
      order_id = order_fund(context.ins, 1000)
      log.info('申购', order_id)
      order_id = redeem_fund(context.ins, 500)
      log.info('赎回', order_id)
  ```

---

### 枚举常量

#### ORDER_STATUS - 委托状态


| 枚举值           | 含义   |
| ---------------- | ------ |
| `PENDING_NEW`    | 创建中 |
| `ACTIVE`         | 未成交 |
| `FILLED`         | 已成交 |
| `REJECTED`       | 废单   |
| `PENDING_CANCEL` | 取消中 |
| `CANCELLED`      | 已取消 |

#### ORDER_TYPE - 委托类型


| 枚举值   | 含义     |
| -------- | -------- |
| `MARKET` | 市价委托 |
| `LIMIT`  | 限价委托 |

#### SIDE- 交易方向


| 枚举值 | 含义 |
| ------ | ---- |
| `BUY`  | 买入 |
| `SELL` | 卖出 |

#### POSITION_EFFECT - 仓位类型


| 枚举值             | 含义     |
| ------------------ | -------- |
| `OPEN`             | 开仓     |
| `CLOSE`            | 平仓     |
| `CLOSE_TODAY`      | 平今仓   |
| `CLOSE_ONLY_TODAY` | 只平今仓 |

---

### 重要对象

#### 上下文对象

##### context

- 🔧作用：

  - 全局对象，存储策略信息(context.run_info),账户持仓数据(context.portfolio)，也可用于储存自定义全局变量。仅在策略框架内可用
- ⛺数据结构


  | 字段名      | 含义                                                                                                             |
  | ----------- | ---------------------------------------------------------------------------------------------------------------- |
  | `run_info`  | 策略运行的配置信息（起止时间、初始资金、频率等），见[run_info](https://quant.10jqka.com.cn/view/help/4#run-info) |
  | `portfolio` | 当前投资组合总览，包含股票和期货账户及持仓汇总，见[portfolio](https://quant.10jqka.com.cn/view/help/4#portfolio) |
- ❗注意事项：

  - 自定义的全局变量尽可能存在 `g`中而不是 `context`,避免系统变量被覆盖
- 📝示例：

```python
def init(context):
    context.fired=True
    log.info(context.run_info)
    log.info(context.portfolio)
    log.info(context.fired)
  
def handle_bar(context,bar_dict):
    if context.fired:
        odr_id = order('000001.SZ',100)
        context.fired = False
        log.info(context.run_info)
        log.info(context.portfolio)
        log.info(context.fired)
  
        log.info(context.portfolio.positions) #输出看起来像个列表,实际类似于字典
        log.info(context.portfolio.stock_account.positions)
  
        log.info(context.portfolio.positions['000001.SZ'])
        log.info(context.portfolio.stock_account.positions['000001.SZ'])
```

##### run_info


| 字段名                 | 类型            | 含义                                   |
| ---------------------- | --------------- | -------------------------------------- |
| `start_date`           | `datetime.date` | 策略运行起始日期                       |
| `end_date`             | `datetime.date` | 策略运行结束日期                       |
| `frequency`            | `str`           | 行情频率（如`'1d'` 表示日频）          |
| `stock_starting_cash`  | `float`         | 股票账户初始资金（期货回测中可能为 0） |
| `future_starting_cash` | `float`         | 期货账户初始资金（股票回测中可能为 0） |
| `benchmark`            | `str`或`None`   | 基准指数代码，未设置时为`None`         |

##### portfolio


| 字段名            | 类型                | 含义                                                                                                                                                                                                       |
| ----------------- | ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `available_cash`  | `float`             | 可用现金                                                                                                                                                                                                   |
| `frozen_cash`     | `float`             | 冻结资金                                                                                                                                                                                                   |
| `returns`         | `float`             | 收益率                                                                                                                                                                                                     |
| `market_value`    | `float`             | 持仓总市值                                                                                                                                                                                                 |
| `portfolio_value` | `float`             | 总资产                                                                                                                                                                                                     |
| `starting_value`  | `float`             | 初始总资产                                                                                                                                                                                                 |
| `pnl`             | `float`             | 累计盈亏（元）                                                                                                                                                                                             |
| `start_date`      | `datetime.date`     | 组合起始日期                                                                                                                                                                                               |
| `positions`       | 类似`dict`          | 持仓情况，key为标的代码，value为[StockPosition](https://quant.10jqka.com.cn/view/help/4#StockPosition%E7%B1%BB)对象或[FuturePosition](https://quant.10jqka.com.cn/view/help/4#FuturePosition%E7%B1%BB)对象 |
| `datetime`        | `datetime.datetime` | 当前行情时间戳                                                                                                                                                                                             |
| `stock_account`   | `StockAccount`      | 股票子账户详情，**期货回测中为`None`**，见[`stock_account`](https://quant.10jqka.com.cn/view/help/4#stock-account)                                                                                         |
| `future_account`  | `FutureAccount`     | 期货子账户详情，**股票回测中为`None`**，见[`future_account`]()                                                                                                                                             |

##### StockPosition类


| 字段名             | 类型                | 含义         |
| ------------------ | ------------------- | ------------ |
| `symbol`           | `str`               | 股票代码     |
| `amount`           | `int`               | 持仓总数量   |
| `available_amount` | `int`               | 可用数量     |
| `pnl`              | `float`             | 盈亏         |
| `market_value`     | `float`             | 持仓市值     |
| `cost_basis`       | `float`             | 持仓成本     |
| `last_price`       | `float`             | 最新市场价格 |
| `pre_price`        | `float`             | 前一收盘价   |
| `datetime`         | `datetime.datetime` | 当前时间     |
| `position_days`    | `int`               | 持仓天数     |
| `profit_rate`      | `float`             | 收益率       |
| `draw_down`        | `float`             | 回撤比例     |
| `markup`           | `float`             | 当日收益率   |

##### stock_account


| 字段名           | 类型       | 含义                                                                                                                |
| ---------------- | ---------- | ------------------------------------------------------------------------------------------------------------------- |
| `available_cash` | `float`    | 股票账户可用资金                                                                                                    |
| `frozen_cash`    | `float`    | 股票账户冻结资金                                                                                                    |
| `market_value`   | `float`    | 股票持仓总市值                                                                                                      |
| `total_value`    | `float`    | 股票账户总资产                                                                                                      |
| `positions`      | 类似`dict` | 持仓情况，key为标的代码，value为[StockPosition](https://quant.10jqka.com.cn/view/help/4#StockPosition%E7%B1%BB)对象 |
| `pnl`            | `float`    | 股票账户累计盈亏                                                                                                    |

##### FuturePosition类


| 字段名               | 类型                | 含义             |
| -------------------- | ------------------- | ---------------- |
| `symbol`             | `str`               | 期货合约代码     |
| `pnl`                | `float`             | 盈亏             |
| `daily_pnl`          | `float`             | 当日盈亏         |
| `margin`             | `float`             | 当前总占用保证金 |
| `market_value`       | `float`             | 持仓合约价值     |
| `long_amount`        | `int`               | 多头总手数       |
| `long_today_amount`  | `int`               | 多头今仓手数     |
| `long_cost_basis`    | `float`             | 多头开仓均价     |
| `long_margin`        | `float`             | 多头占用保证金   |
| `short_amount`       | `int`               | 空头总手数       |
| `short_today_amount` | `int`               | 空头今仓手数     |
| `short_cost_basis`   | `float`             | 空头开仓均价     |
| `short_margin`       | `float`             | 空头占用保证金   |
| `last_price`         | `float`             | 最新市场价格     |
| `datetime`           | `datetime.datetime` | 当前时间         |
| `position_days`      | `int`               | 持仓天数         |
| `profit_rate`        | `float`             | 收益率           |
| `draw_down`          | `float`             | 回撤比例         |
| `markup`             | `float`             | 当日收益率       |

##### future_account


| 字段名             | 类型       | 含义                                                                                                                    |
| ------------------ | ---------- | ----------------------------------------------------------------------------------------------------------------------- |
| `available_cash`   | `float`    | 可用资金                                                                                                                |
| `frozen_cash`      | `float`    | 冻结资金                                                                                                                |
| `market_value`     | `float`    | 持仓合约价值                                                                                                            |
| `total_value`      | `float`    | 账户总资产                                                                                                              |
| `transaction_cost` | `float`    | 账户累计交易费用（所有合约手续费之和）                                                                                  |
| `positions`        | 类似`dict` | 持仓情况，key为标的代码，value为[`FuturePosition`](https://quant.10jqka.com.cn/view/help/4#FuturePosition%E7%B1%BB)对象 |
| `margin`           | `float`    | 总占用保证金                                                                                                            |
| `long_margin`      | `float`    | 多头方向保证金占用                                                                                                      |
| `short_margin`     | `float`    | 空头方向总保证金占用                                                                                                    |
| `pnl`              | `float`    | 盈亏                                                                                                                    |
| `daily_pnl`        | `float`    | 当日盈亏                                                                                                                |
| `profit_rate`      | `float`    | 收益率                                                                                                                  |
| `draw_down`        | `float`    | 回撤比例                                                                                                                |

#### 订阅行情对象

##### bar_dict

- 🔧作用：

  - 全局对象，用于储存当前时间的bar行情数据。仅在策略框架内可用
- ⛺数据结构:

  - 类似`dict`，key为标的代码，value为[`Bar`](https://quant.10jqka.com.cn/view/help/4#Bar%E7%B1%BB)对象
- ❗注意事项：

  - 使用股票API时，无需订阅
  - 使用期货API时，需要使用 `subscribe`函数订阅
- 📝示例：

```python
def init(context):
    subscribe('IF9999')

def handle_bar(context, bar_dict):
    print(bar_dict['IF9999'].open)
```

##### Bar类


| 字段名        | 类型                | 含义                               |
| ------------- | ------------------- | ---------------------------------- |
| `symbol`      | `str`               | 标的代码                           |
| `datetime`    | `datetime.datetime` | 数据对应时间                       |
| `open`        | `float`             | 开盘价                             |
| `high`        | `float`             | 最高价                             |
| `low`         | `float`             | 最低价                             |
| `close`       | `float`             | 收盘价                             |
| `volume`      | `float`             | 成交量（单位：期货为手，股票为股） |
| `turnover`    | `float`             | 成交额（单位：元）                 |
| `high_limit`  | `float`             | 涨停价                             |
| `low_limit`   | `float`             | 跌停价                             |
| `prev_close`  | `float`             | 前收盘价                           |
| `avg_price`   | `float`             | 成交均价                           |
| `settle`      | `float`             | **仅期货日频**：当日结算价         |
| `prev_settle` | `float`             | **仅期货日频**：前一交易日结算价   |
| `is_st`       | `bool`              | **仅股票**：是否为ST               |
| `is_paused`   | `bool`              | **仅股票**：是否处于停牌状态       |

#### 订单对象：Order类

- 🔧作用：
  - on_order函数推送,或使用get_order/get_orders/get_open_orders函数查询。仅在策略框架内可用
- ⛺数据结构:


| 字段名             | 类型                | 含义                                                                                                                      |
| ------------------ | ------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `order_id`         | `str`               | 订单唯一标识                                                                                                              |
| `symbol`           | `str`               | 标的代码                                                                                                                  |
| `created`          | `datetime.datetime` | 订单创建时间                                                                                                              |
| `datetime`         | `datetime.datetime` | 同`created`                                                                                                               |
| `order_type`       | `str`               | 交易方向：`'LONG'` - 买入、`'SHORT'` - 卖出                                                                               |
| `type`             | `ORDER_TYPE`        | 委托类型，见[`ORDER_TYPE`](https://quant.10jqka.com.cn/view/help/4#ORDER-TYPE---%E5%A7%94%E6%89%98%E7%B1%BB%E5%9E%8B)     |
| `limit_price`      | `float`             | 委托价格，市价单为`0`                                                                                                     |
| `amount`           | `int`               | 委托数量                                                                                                                  |
| `filled_amount`    | `int`               | 已成交数量                                                                                                                |
| `avg_price`        | `float`             | 成交均价，未成交时为`0`                                                                                                   |
| `transaction_cost` | `float`             | 手续费，未成交时为`0`                                                                                                     |
| `status`           | `ORDER_STATUS`      | 订单状态，见[`ORDER_STATUS`](https://quant.10jqka.com.cn/view/help/4#ORDER-STATUS---%E5%A7%94%E6%89%98%E7%8A%B6%E6%80%81) |
| `offset_flag`      | `str`或`None`       | 开平仓标志，**仅期货有效**，股票订单此字段为 `None`。`'OPEN'` - 开仓，`'CLOSE_TODAY'` - 平今仓，`'CLOSE'` - 平仓          |

- ❗注意事项：

  - 可结合委托数量、成交数量、委托状态来判断区分未成交、部分成交、全撤、部成部撤的状态
- 📝示例：

```python
def init(context):
    g.fired = True

def handle_bar(context,bar_dict):
    if g.fired:
        odr_id = order('000001.SZ',100)
        print(get_order(odr_id))
        g.fired=False

def on_order(context,odr):
    print(odr)
```

#### 成交对象：Trade类

- 🔧作用：
  - on_trade函数推送,或使用get_tradelogs函数查询。仅在策略框架内可用
- ⛺数据结构:


| 字段名               | 类型                        | 含义                                                                                                                                                        |
| -------------------- | --------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `order_book_id`      | `str`                       | 标的代码                                                                                                                                                    |
| `trading_datetime`   | `datetime.datetime`         | 成交时间                                                                                                                                                    |
| `datetime`           | `datetime.datetime`         | 同`trading_datetime`                                                                                                                                        |
| `order_id`           | `str`                       | 关联的订单 ID，用于追踪来源订单                                                                                                                             |
| `exec_id`            | `str`                       | 成交唯一标识                                                                                                                                                |
| `last_price`         | `float`                     | 成交价格，包含交易成本                                                                                                                                      |
| `last_quantity`      | `int`                       | 成交数量                                                                                                                                                    |
| `side`               | `SIDE`                      | 交易方向，见[`SIDE`](https://quant.10jqka.com.cn/view/help/4#SIDE--%E4%BA%A4%E6%98%93%E6%96%B9%E5%90%91)                                                    |
| `commission`         | `float`                     | 手续费                                                                                                                                                      |
| `tax`                | `float`                     | 税费                                                                                                                                                        |
| `transaction_cost`   | `float`                     | 总交易成本 =`commission + tax`                                                                                                                              |
| `position_effect`    | `POSITION_EFFECT` 或 `None` | 仓位类型，**期货有效**，股票为`None`，见[`POSITION_EFFECT`](https://quant.10jqka.com.cn/view/help/4#POSITION-EFFECT---%E4%BB%93%E4%BD%8D%E7%B1%BB%E5%9E%8B) |
| `close_today_amount` | `int`                       | 平今仓数量                                                                                                                                                  |
| `pnl`                | `float`或`None`             | 本次成交实现的盈亏，**仅平仓有效**，开仓为`None`                                                                                                            |

- ❗注意事项：

  - 有成交时就会推送，不代表订单完全成交
- 📝示例：

```python
def init(context):
    g.fired = True

def handle_bar(context,bar_dict):
    if g.fired:
        odr_id = order('000001.SZ',100)
        print(get_tradelogs())
        g.fired=False

def on_trade(context,trade):
    print(trade)
```

#### 全局变量对象：g

- 🔧作用：

  - 全局对象，用于储存全局变量。仅在策略框架内可用
- ❗注意事项：

  - 自定义的全局变量尽可能存在 `g`中而不是 `context`,避免系统变量被覆盖
- 📝示例：

  ```python
  def init(context):   
      #设置要交易的股票 
      g.contract = '300033.SZ'

  def handle_bar(context, bar_dict):
      order(g.contract, 1000)
  ```

### 辅助函数

#### 日志函数：log

- 👑调用方法：

  ```python
  log.info(content)
  log.warn(content)
  log.error(content)
  ```
- 📚参数说明：

  - content：需要打印输出的日志内容，可以是字符串，也可以是某个对象
- 🔧作用：

  - log.info，log.warn，log.error是三种不同级别的打印函数,级别排序(先后)：error>warn>info
- ❗注意事项：

  - log.error是一个打印输出结果函数,当该函数执行后,整个策略会终止回测运行
  - 需要将日志另存为文件持久化的话可以通过set_log_level函数进行设置
  - 研究环境中同样可以使用
- 📝示例：

  ```python
  def init(context):
      pass

  def handle_bar(context,bar_dict):
      # 获得当前Bar时间
      time =get_datetime()
      log.info('目前Bar时间:'+str(time))
  ```

#### 画图函数：record

- 👑调用方法：

  ```python
  record(**kwargs)
  ```
- 📚参数说明：

  可变参数：key为曲线名称，value为当前日期下曲线对应的值
- 🔧作用：

  - 画图函数，根据策略需求，自定义画图
- ❗注意事项：

  - 该函数可以画出多条key线图走势，也可以是一条
- 📝示例：

  ```python
  #画出平安银行的5.10.20日均线走势图.
  def init(context):
      pass

  def handle_bar(context,bar_dict):
      value = history('000001.SZ', ['close'], 20, '1d', True, fq='pre')
      MA5=value['close'].iloc[-5:].mean()
      MA10=value['close'].iloc[-10:].mean()
      MA20=value['close'].iloc[-20:].mean()
      record(MA5=MA5, MA10=MA10,MA20=MA20)
  ```

#### 性能分析函数：enable_profile

- 👑调用方法：

  ```python
  enable_profile(func_list)
  ```
- 📚参数说明：

  - func_list：所需分析函数的名称,一般根据实际需求填写需要分析的函数名,不填默认分析所有函数
- 🔧作用：

  - 性能分析函数,获取策略中各个函数的运行时间
- ❗注意事项：

  - 该函数在策略框架函数之外执行
  - 性能分析结果再日志的最后部分显示
  - func_list参数如果不填写，则默认为分析所有函数
- 📝示例：

```python
#将初始双均线策略进行函数性能分析.
#初始化账户
def init(context):
    context.security = '600519.SH'

def handle_bar(context,bar_dict):
    close = history(context.security, ['close'], 20, '1d')
    MA5 = close.values[-5:].mean()
    MA20 = close.values.mean()
    if MA5 > MA20:
        order_target_percent(context.security,1)
    if MA5 < MA20:
        order_target(context.security,0)

enable_profile()
```









## 工具函数
### 股票代码格式转换：normalize_symbol

- 👑调用方法
  
  ```python
  normalize_symbol(symbol, ty=None)
  ```
- 🔧作用
  
  - 将不同格式的股票或基金代码，转换为 SuperMind 平台的标准格式代码。
- 📚参数说明：
  
  - `symbol`: `str`: 待转换的股票或基金代码，例如 `'300033'`。
  - `ty`:  `str`，可选，指定代码类型。`'stock'` 代表股票，`'ota'` 代表基金。如果为 `None`，则函数会自动判断。默认为 `None`。
- 🔢返回值说明：
  
  - `str`: 返回 SuperMind 平台下的标准格式代码，例如 `'300033.SZ'`。
- ❗注意事项：
  
  - 输入的代码 `symbol` 必须为字符串格式。
  - 即使不指定 `ty` 参数（即使用默认值 `None`），函数通常也能正确识别并转换代码。
  - 在研究环境和策略环境中均可使用。
- 📝示例：
  
  - **调用**
    ```python
    # 指定类型转换
    normalize_symbol('300033', ty='stock')
    
    # 使用默认参数转换
    normalize_symbol('300033')
    ```
  - **返回值**
    ```
    '300033.SZ'
    ```

### 保存文件函数：write_file

- 👑调用方法：
  ```python
  write_file(path, content, append=False)
  ```
- 🔧作用：
  - 将内容保存到研究环境的指定文件路径中。
- 📚参数说明：
  - `path`: `str`，文件保存的相对路径。例如，'test.txt'表示在研究环境根目录下创建或写入文件。
  - `content`：`str` 或 `bytes`，需要保存的内容。可以是字符串或二进制内容。如果是字符串，将使用UTF-8编码后存储。
  - `append`：`bool`，是否为追加模式。默认为 `False`。
    - `True`: 在文件末尾追加内容，保留原有内容。
    - `False`: 覆盖文件原有内容。
- 🔢返回值说明：
  - `int`，写入的字节长度。
- ❗注意事项：
  - 保存的内容需要是 `str` 或 `bytes` 类型。
  - 该函数在研究环境中可用。
- 📝示例：
  - **调用：**
    ```python
    write_file('log.txt', 'Hello, this is a log message.')
    ```
  - **返回值：**
    ```python
    24
    ```

### 读取文件函数：read_file

- 👑调用方法
  ```python
  read_file(path)
  ```
- 🔧作用
  - 读取研究环境中的指定文件。
- 📚参数说明：
  - `path`: `str`，文件的相对路径。例如，`'folder/file.txt'` 代表读取 `folder` 文件夹下的 `file.txt` 文件；`'file.txt'` 代表读取根目录下的 `file.txt` 文件。
- 🔢返回值说明：
  - `bytes`，返回文件内容的字节流。
- ❗注意事项：
  - 文件保存在文件夹中，则`path`的格式必须是`'文件夹名/文件名'`。
  - 文件保存在根目录下，则`path`格式为`'文件名'`。
  - 返回值为 `bytes` 类型，如果需要字符串，可能需要使用 `decode()` 方法进行解码。
- 📝示例：
  - 调用
    ```python
    # 首先，创建一个文件用于读取
    write_file('example.txt', '你好，世界')
    
    # 调用 read_file 读取文件
    data = read_file('example.txt')
    
    # 打印查看返回值类型和内容
    print(type(data))
    print(data)
    
    # 如果需要字符串，可以解码
    print(data.decode('utf-8'))
    ```
  - 返回值
    ```
    <class 'bytes'>
    b'\xe4\xbd\xa0\xe5\xa5\xbd\xef\xbc\x8c\xe4\xb8\x96\xe7\x95\x8c'
    你好，世界
    ```

### 查询研究环境指定路径下的文件：list_file

- 👑调用方法
  
  ```python
  list_file(path, isfile=None, isdir=None, abspath=False)
  ```
- 🔧作用
  
  - 查询研究环境指定路径下的文件和目录列表，可按文件或目录进行筛选。
- 📚参数说明：
  
  - `path`: `str`，研究环境文件路径，例如，'test'代表在研究环境根目录中名为test的文件夹。
  - `isfile`: `bool`，是否只返回文件，默认为`None`。
  - `isdir`: `bool`，是否只返回文件夹，默认为`None`。
  - `abspath`: `bool`，是否返回绝对路径，默认为`False`。
- 🔢返回值说明：
  
  - `list`，包含文件/目录路径字符串的列表。
- ❗注意事项：
  
  - `isfile`和`isdir`都为`None`时，表示同时返回文件和文件夹。
  - 当`isfile`与`isdir`同时为`True`时，同样返回文件和文件夹。
  - `abspath`参数默认为`False`，即返回相对路径。
  - 此函数同样可用于查询研究环境内的文件。
- 📝示例：
  
  - 调用：
    ```python
    list_file('')
    ```
  - 返回值：
    ```python
    ['crontabs/requirements.txt', 'crontabs/infer_daban (every 1minutes from 7.00am to 7.00am).html', 'crontabs/c4 (every 1minutes from 9.01am to 9.01am).py.output.txt', 'crontabs/crontabs.log', 'crontabs/model.toml', 'crontabs/c4 (every 1minutes from 9.01am to 9.01am).py', ... ]
    ```

### 复制/剪贴文件或文件夹：copy_file

- 👑调用方法
  ```python
  copy_file(src, dst, move=False)
  ```
- 🔧作用
  - 复制/剪贴文件或文件夹
- 📚参数说明：
  - `src`: `str`，需要操作的文件或文件夹的路径
  - `dst`: `str`，目标路径(研究环境),例如，'test'代表在研究环境根目录中名为test的文件夹
  - `move`: `bool`，是否剪贴，默认为`False`
- 🔢返回值说明：
  - `str`，值为被操作文件的源路径。
- ❗注意事项：
  - 迁移单个文件时，设置目标路径时也需要具体到文件名
  - 可以利用此函数新建文件夹：copy_file(None,'new_folder')，代表在根目录下新建名为‘new_folder’的文件夹
  - 研究环境中同样可以使用
- 📝示例：
  - 调用
    ```python
    copy_file('test.txt', 'new_folder/abc.txt', move=True)
    ```
  - 返回值
    ```python
    'test.txt'
    ```

### 删除文件或文件夹：remove_file

- 👑调用方法
  ```python
  remove_file(path, trash=True)
  ```
- 🔧作用
  - 删除文件或文件夹
- 📚参数说明：
  - `path`: `str`，表示需要删除文件/文件夹的路径
  - `trash`: `bool`，表示是否移入回收站，默认为True，为False时意味着彻底删除
- 🔢返回值说明：
  - `NoneType`，无返回值
- ❗注意事项：
  - `trash=False`时意味着彻底删除文件，不可恢复
  - 研究环境中同样可以使用
- 📝示例：
  - 调用：
    ```python
    remove_file('test.txt')
    ```
  - 返回值：
    ```
    None
    ```

### 消息推送函数：notify_push

- 👑调用方法：
  
  ```python
  notify_push(
      content, 
      channel='wxpusher', 
      subject='SuperMind消息提醒', 
      email_list=None, 
      uids=None, 
      topic_ids=None, 
      group_id=None,
      url=None,
      payload=None,
  )
  ```
- 📚参数说明：
  
  - content：需要推送的消息文本
  - channel: 目前支持微信推送、webhook，参数值分别为 `"wxpusher"`、`"webhook"`
  - subject: 消息主题
  - uids: `list`，`channel`为 `wxpusher`需要填写，用户的UID，关注公众号，点击“我的－我的UID”获取用户UID信息
  - url: `str`，`channel`为 `webhook`需要填写，webhook地址
  - payload: `dict`，`channel`为 `webhook`需要填写，消息格式，如钉钉的消息格式为 `{"msgtype": "text", "text": {"content": "$content"}}`，其中 `$content`会被替换为 `content`参数传入的值
- 🔧作用：
  
  - 消息推送函数，在研究环境、策略编辑等模块均可使用
- ❗注意事项：
  
  - `channel='wxpusher'`时，需要先关注公众号：
    ![](http://wxpusher.zjiecode.com/api/qrcode/jGYu4SdkDOTGPRz5ZgZbusvFYq7AfAeBK7DziHDHpytBajgaVoI7VBrHrwxodE5d.jpg)
  - webhook教程见：[模拟仿真 (10jqka.com.cn)](https://quant.10jqka.com.cn/view/help/10#%E4%BB%80%E4%B9%88%E6%98%AFWebhook-)
- 📝示例：

```python
try:
    raise
except:
    # 微信推送
    notify_push(
        '程序报错', 
        channel='wxpusher', 
        subject='SuperMind消息提醒', 
        uids='XXXXXX',
    )
    # 钉钉webhook推送
    notify_push(
        '程序报错', 
        channel='webhook',   
        url='XXXXXX',
        payload={"msgtype": "text", "text": {"content": "$content"}},
    )
```

### 自选板块：custom_sector

- 👑调用方法：
  
  ```python
  custom_sector(name=None, action='query', symbol=None, rename=None)
  ```
- 📚参数说明：
  
  - name：str，板块名称
  - action: str，insert - 新建name的板块，update - 更新指定板块的股票列表或重命名，append - 在指定板块中新增股票，pop - 移除指定板块内的个别股票，remove - 移除指定板块
  - symbol：list，股票列表
  - rename: str，重命名板块名称
- 🔧作用：
  
  - 读取或修改自选板块
- 📝示例：

```python
custom_sector() # 返回所有板块的dataframe

custom_sector('板块1') # 返回 板块1 的属性和股票

custom_sector('板块1', 'insert', ['000001.SZ']) # 新建板块1的股票列表

custom_sector('板块1', 'update', ['000001.SZ'], '新名字') # 更新板块1的股票列表或名字

custom_sector('板块1', 'append', ['000001.SZ']) # 增加板块1的股票列表

custom_sector('板块1', 'pop', ['000001.SZ']) # 移除板块1的股票

custom_sector('板块1', 'remove') # 删除板块1
```

### 文件加密：compile_pyfile

- 👑调用方法：
  
  ```python
  open_api = get_open_api('public')
  open_api.compile_pyfile('xxx.py')
  open_api.import_cpyfile('xxx.cpython-38-x86_64-linux-gnu.cpy')
  ```
- 🔧作用：
  
  - 对指定的 py 源文件进行编译与加密，加密完成后可删除原始 `.py` 文件，从而实现策略源代码的保护。
  - 生成的xxx.cpython-38-x86\_64-linux-gnu.cpy加密文件可在不同用户间进行分发与使用。
  - 文件需上传至研究平台目录中方可调用，注意无法跨py版本使用。
- 📝示例：

```python
# 编译加密py文件
open_api = get_open_api('public')
open_api.compile_pyfile('untitled1.py')

#初始化cpy加密文件，该操作仅需执行一次，之后即可通过 import untitled1 进行调用
open_api = get_open_api('public') 
open_api.import_cpyfile('untitled1.cpython-38-x86_64-linux-gnu.cpy')
```




## 行情资金数据接口
### 行情数据：get_price

- 👑调用方法
  ```python
  get_price(
      securities,
      start_date,
      end_date,
      fre_step,
      fields,
      skip_paused=False,
      fq='pre',
      bar_count=0,
      is_panel=False,
  )
  ```
- 🔧作用
  - 获取多只证券多属性历史行情数据
- 📚参数说明
  - `securities`: `str`或`list`，标的代码
  - `start_date`: `None`、`str`或`datetime-like`，起始时间
  - `end_date`: `str`、`datetime-like`，结束时间
  - `fre_step`: `str`，时间步长，支持分钟、日
    - `fre_step = 'xd'`：x为正整数，代表x天，例如'1d'代表1天
    - `fre_step = 'xm'`：x为正整数，代表x分钟，例如'1m'代表1分钟
  - `fields`: `list`，需要获取的字段，可参考
    - 日频：[股票日行情数据(A股)](http://quant.10jqka.com.cn/view/dataplatform/detail/8)
    - 分钟：[股票分钟行情数据(A股)](http://quant.10jqka.com.cn/view/dataplatform/detail/12)
    - 当步长不为'1m'或'1d'时，fields仅支持'open', 'close', 'high', 'low', 'volume', 'turnover'这几个字段
  - `skip_paused`: `bool`，是否跳过停牌，默认为不跳过
  - `fq`: `str`，复权模式
    - `fq=None`: 不复权
    - `fq='post'`: 后复权
    - `fq='pre'`: 动态前复权
  - `bar_count`: `int`，历史长度。`start_date`为 `None`时，`bar_count`必须为正整数；`start_date`不为 `None`时，`bar_count`必须为0
  - `is_panel`: `bool`，返回数据格式，默认为False
- 🔢返回值说明
  - `dict`或`pd.Panel`或`pd.DataFrame`，根据参数返回不同格式的数据
    - 当取多个标的行情数据且`is_panel=False`时，返回`dict`，key为股票代码，value为`pd.DataFrame`，索引为时间，列名为字段
    - 当取多个标的行情数据且`is_panel=True`时，返回`pd.Panel`
    - 当取单个标的行情数据时，返回`pd.DataFrame`，索引为时间，列名为字段
- ❗注意事项
  - 该函数支持获取实时行情
  - 该函数还支持查询场内基金、指数、可转债等标的的行情数据，支持字段可查询[SuperMind数据平台](http://quant.10jqka.com.cn/view/dataplatform)
  - 返回panel格式数据时，可以用to_frame()方法将数据转换为一个具有mutilindex的二维dataframe
  - 暂不支持获取CSI结尾指数的历史分钟行情数据
- 📝示例：
  - 调用（多只股票，is_panel=False）
    
    ```python
    get_price(['000001.SZ','000002.SZ'], None, '20230201', '1d', ['close', 'high', 'low'], True, None, 3)
    ```
  - 返回值
    
    ```python
    {'000001.SZ':             close   high    low
    2023-01-30  15.15  15.74  14.89
    2023-01-31  14.99  15.51  14.96
    2023-02-01  14.70  15.08  14.51, '000002.SZ':             close   high    low
    2023-01-30  18.09  19.00  18.00
    2023-01-31  18.29  18.35  17.95
    2023-02-01  18.19  18.28  17.90}
    ```
  - 调用（多只股票，is_panel=True）
    
    ```python
    get_price(['000001.SZ','000002.SZ'], None, '20230201', '1d', ['close', 'high', 'low'], True, None, 3, is_panel=True)
    ```
  - 返回值
    
    ```python
    <class 'pd.Panel'>
    Dimensions: 3 (items) x 3 (major_axis) x 2 (minor_axis)
    Items axis: close to low
    Major_axis axis: 2023-01-30T00:00:00.000000000 to 2023-02-01T00:00:00.000000000
    Minor_axis axis: 000001.SZ to 000002.SZ
    ```
  - 调用（单只股票）
    
    ```python
    get_price('000001.SZ', None, '20230201', '1d', ['close', 'high', 'low'], True, None, 3)
    ```
  - 返回值
    
    ```python
    close   high    low
    2023-01-30  15.15  15.74  14.89
    2023-01-31  14.99  15.51  14.96
    2023-02-01  14.70  15.08  14.51
    ```

### 开盘竞价成交信息：get_call_auction

- 👑调用方法
  ```python
  get_call_auction(symbol, dt=None)
  ```
- 🔧作用
  - 用于获取指定标的在指定日期的集合竞价行情数据。
- 📚参数说明
  - `symbol`: `str`或`list[str]`，表示标的代码
  - `dt`: `str`, `datetime-like`或`None`，表示日期
- 🔢返回值说明
  - `pandas.core.frame.DataFrame`，返回一个DataFrame，包含'price'和'turnover'列，分别表示集合竞价价格和成交量，索引为'symbol'
- ❗注意事项
  - 当`symbol`为字符串列表时，可一次查询多个标的的数据
- 📝示例：
  - 调用
    ```python
    get_call_auction(['000001.SZ', '600000.SH'], '20230613')
    ```
  - 返回值
    ```python
    price   turnover
    symbol         
    600000.SH   7.43   704364.0
    000001.SZ  11.76  3988992.0
    ```
  - 调用
    ```python
    get_call_auction('000001.SZ', '20230613')
    ```
  - 返回值
    ```python
    price   turnover
    symbol         
    000001.SZ  11.76  3988992.0
    ```

### 期货行情数据：get_price_future

- 👑调用方法
  ```python
  get_price_future(
      symbol_list,
      start_date,
      end_date,
      fre_step,
      fields,
      skip_paused=False,
      fq=None,
      bar_count=0,
      is_panel=0,
  )
  ```
- 🔧作用
  - 用于获取期货合约的历史行情数据。
- 📚参数说明
  - `symbol_list`: `str`或`list[str]`，表示标的代码。
  - `start_date`: `str`、`datetime-like`，表示起始时间。
  - `end_date`: `str`、`datetime-like`，表示结束时间。
  - `fre_step`: `str`，表示时间步长，支持分钟、日。
    - `fre_step = 'xd'`：x为正整数，代表x天，例如'1d'代表1天。
    - `fre_step = 'xm'`：x为正整数，代表x分钟，例如'1m'代表1分钟。
  - `fields`: `list[str]`，表示需要获取的字段。可参考
    - 日频：[期货日行情数据(A股)](http://quant.10jqka.com.cn/view/dataplatform/detail/174)
    - 分钟：[期货分钟行情数据(A股)](http://quant.10jqka.com.cn/view/dataplatform/detail/422)
    - 当步长不为'1m'或'1d'时，fields仅支持'open', 'close', 'high', 'low', 'volume', 'turnover'这几个字段。
  - `skip_paused`: `bool`，表示是否跳过停牌。默认为`False`。
  - `fq`: `str`，表示复权类型
    - `fq='pre'`：前复权
    - `fq='post'`：后复权
    - `fq=None`：不复权
  - `bar_count`: `int`，表示历史长度。`start_date`为 `None`时，`bar_count`必须为正整数；`start_date`不为 `None`时，`bar_count`必须为0
  - `is_panel`: `bool`，表示返回数据格式。默认为`False`。
- 🔢返回值说明
  - 根据输入参数的不同，返回值类型会变化：
    - 当`is_panel=True`且`symbol_list`为多个标的时，返回`pd.Panel`
    - 当`is_panel=False`且`symbol_list`为多个标的时，返回`dict[str, pandas.DataFrame]`，key为标的代码，value为对应标的的DataFrame行情数据，索引为时间，列名为字段名。
    - 当`symbol_list`为单个标的时，返回`pandas.DataFrame`，包含该标的的历史行情数据，索引为时间，列名为字段名。
- ❗注意事项
  - 该函数支持获取实时行情。
  - 返回panel格式数据时，可以用`to_frame()`方法将数据转换为一个具有mutilindex的二维dataframe。
- 📝示例：
  - 调用
    ```python
    # 获取IC2304、IF2304两个标的在2023年4月6日前3天的收盘价、最高价、最低价，返回Panel格式
    value_panel = get_price_future(
        symbol_list=['IC2304', 'IF2304'],
        start_date=None,
        end_date='20230406',
        fre_step='1d',
        fields=['close', 'high', 'low'],
        bar_count=3,
        is_panel=1
    )
    print(value_panel)
    ```
  - 返回值
    ```python
    <class 'mgquant_mod_mindgo.utils.compat.panel.pd_Panel'>
    Dimensions: 3 (items) x 3 (major_axis) x 2 (minor_axis)
    Items axis: close to low
    Major_axis axis: 2023-04-03T00:00:00.000000000 to 2023-04-06T00:00:00.000000000
    Minor_axis axis: IC2304 to IF2304
    ```
  - 调用
    ```python
    # 获取IC2304、IF2304两个标的在2023年4月6日前3天的收盘价、最高价、最低价，返回字典格式
    value_dict = get_price_future(
        symbol_list=['IC2304', 'IF2304'],
        start_date=None,
        end_date='20230406',
        fre_step='1d',
        fields=['close', 'high', 'low'],
        bar_count=3,
        is_panel=0
    )
    print(value_dict)
    ```
  - 返回值
    ```python
    {'IC2304':               close    high     low
     2023-04-03  6406.0  6429.6  6353.0
     2023-04-04  6415.0  6417.2  6382.2
     2023-04-06  6411.4  6427.2  6391.0, 'IF2304':               close    high     low
     2023-04-03  4091.2  4104.4  4063.8
     2023-04-04  4111.8  4114.0  4082.0
     2023-04-06  4098.0  4105.8  4085.6}
    ```
  - 调用
    ```python
    # 获取单个标的IC2304在2023年4月6日前3天的收盘价、最高价、最低价
    value_df = get_price_future(
        symbol_list='IC2304',
        start_date=None,
        end_date='20230406',
        fre_step='1d',
        fields=['close', 'high', 'low'],
        bar_count=3
    )
    print(value_df)
    ```
  - 返回值
    ```python
    close    high     low
    2023-04-03  6406.0  6429.6  6353.0
    2023-04-04  6415.0  6417.2  6382.2
    2023-04-06  6411.4  6427.2  6391.0
    ```

### 蜡烛图数据：get_candle_stick

- 👑调用方法：
  ```python
  get_candle_stick(
      securities,
      end_date='20180101',
      fre_step='1d',
      fields=None,
      skip_paused=False,
      fq='pre',
      bar_count=0,
      is_panel=False,
  )
  ```
- 📚参数说明：
  - securities：str或list, 标的代码
  - end_date：str,int,float,datetime-like，结束时间
  - fre\_step：str，时间步长，支持分钟、日、周、月、年
    
    - 分钟：支持'1m','5m','15m','30m','60m'
    - 日频：支持自定义天数，'nd'，例如'2d'代表2天
    - 周：'week'
    - 月：'month'
    - 年：'year'
  - fields：list，需要获取的字段，仅支持'open','high','low','close','volume','turnover'
  - skip_paused：bool，是否跳过停牌，默认为不跳过
  - fq：str，复权模式
    
    - `fq=None`: 不复权
    - `fq='post'`: 后复权
    - `fq='pre'`: 动态前复权
  - bar_count：int，历史长度，`bar_count`必须为正整数。
  - is_panel：bool，返回数据格式，默认为False
    
    - 当取多个标的行情数据时，`is_panel=False`时，返回key为股票代码，value为dataframe的字典
    - 当取多个标的行情数据时，`is_panel=True`时，返回panel格式数据
    - 当取单个标的行情数据时，返回dataframe
- 🔧作用：
  - 获取股票、债券、基金的历史蜡烛图数据
- ❗注意事项：
  - 返回panel格式数据时，可以用to_frame()方法将数据转换为一个具有mutilindex的二维dataframe
- 📝示例：
  ```python
  # 获取600519.SH、000002.SZ两个标的在2023年8月1日前3个月线的行情数据
  data = get_candle_stick(
      ['600519.SH','000002.SZ'], 
      end_date='20230801',
      fre_step='month',
      fields=['open', 'close', 'high', 'low', 'volume'],
      skip_paused=False,
      fq='pre',
      bar_count=3,
      is_panel=0
  )
  # 打印收盘价数据
  print(value['close'])
  ```
- 返回数据示例：

### 获取实时行情快照数据：get_last_tick

- 👑调用方法
  ```python
  get_last_tick(securities, fields, level=None)
  ```
- 🔧作用
  - 用于获取多只证券的实时行情快照数据。
- 📚参数说明
  - `securities`: `str`或`list[str]`，表示标的代码。
  - `fields`: `list[str]`，表示需要获取的字段，可参考[实时行情快照](http://quant.10jqka.com.cn/view/dataplatform/detail/20)。
  - `level`: `Optional[str]`，表示数据级别。
- 🔢返回值说明
  - `pandas.DataFrame`，返回数据框，包含所请求的字段和标的代码。
- ❗注意事项
  - 获取当日数据时，响应时间超过六秒会报超时错误。
- 📝示例：
  - 调用（传入单只股票）
    ```python
    from mindgo_api import *
    data = get_last_tick('000001.SZ', ['current'])
    ```
  - 返回值
    ```python
    id_stock  current
    0  000001.SZ     11.7
    ```
  - 调用（传入多只股票）
    ```python
    from mindgo_api import *
    data = get_last_tick(['000001.SZ', '600000.SH'], ['current'])
    ```
  - 返回值
    ```python
    id_stock  current
    0  000001.SZ    11.70
    1  600000.SH    11.66
    ```

### 获取历史行情快照数据：get_tick

- 👑调用方法
  ```python
  get_tick(securities, start_date, end_date, fields, level=None)
  ```
- 🔧作用
  - 用于获取指定证券在特定时间范围内的历史行情快照数据。
- 📚参数说明
  - `securities`: `str`或`list[str]`，表示标的代码。
  - `start_date`: `str`或`datetime-like`，表示起始时间。
  - `end_date`: `str`或`datetime-like`，表示结束时间。
  - `fields`: `list[str]`，表示需要获取的字段，可参考[历史行情快照](http://quant.10jqka.com.cn/view/dataplatform/detail/16)。
  - `level`: `Optional[str]`，表示数据级别。
- 🔢返回值说明
  - `pandas.DataFrame`，返回包含指定字段的历史行情快照数据的 DataFrame。
- ❗注意事项
  - 该函数也支持获取日内快照数据。
  - 获取当日数据时，响应时间超过六秒会报超时错误。
- 📝示例：
  - 调用
    ```python
    data = get_tick('000001.SZ', '20230801 09:23', '20230801 09:30', ['current'])
    ```
  - 返回值
    ```python
    id_stock          trade_date  current
    0   000001.SZ 2023-08-01 09:23:00    12.28
    1   000001.SZ 2023-08-01 09:23:09    12.28
    2   000001.SZ 2023-08-01 09:23:18    12.28
    ...
    15  000001.SZ 2023-08-01 09:30:00    12.26
    ```

### 统计涨跌区间个股数量：get_stats

- 👑调用方法
  ```python
  get_stats(date=None)
  ```
- 🔧作用
  - 用于获取每日/实时行情中各个涨跌区间的个股数量。
- 📚参数说明
  - `date`: `Optional[str]`，表示查询日期，默认为当日。
- 🔢返回值说明
  - `list`，返回一个列表，列表中的每个元素代表对应涨跌区间的个股数量。
- ❗注意事项
  - 一共有21个涨跌幅区间： (无穷小,-9)，[-9,-8)...[-1,0),[0],(0,1]...(9,无穷大)
- 📝示例：
  - 调用
    ```python
    data = get_stats('20230810')
    ```
  - 返回值
    ```python
    [10, 2, 5, 13, 13, 26, 76, 113, 418, 1175, 222, 1706, 737, 245, 106, 77, 28, 18, 8, 3, 31]
    ```

### 压力支撑位数据：get_resistance_support

- 👑调用方法
  ```python
  get_resistance_support(
      symbol_list,
      start_date,
      end_date,
      fre_step,
      fields,
      bar_count=0,
      is_panel=0,
  )
  ```
- 🔧作用
  - 用于获取多只证券股价压力位、支撑位数据
- 📚参数说明
  - `symbol_list`: `str`或`list`，表示标的代码
  - `start_date`: `None`,`str`或`datetime-like`，表示起始时间。
  - `end_date`: `str`或`datetime-like`，表示结束时间
  - `fre_step`: `str`，表示时间步长，支持'1d','30m','5m'三种步长
  - `fields`: `list`，表示需要获取的字段
    - `'resistance_line'`：价格压力位(元)
    - `'support_line'`：价格支撑位(元)
  - `bar_count`: `int`，表示历史长度。`start_date`为 `None`时，`bar_count`必须为正整数；`start_date`不为 `None`时，`bar_count`必须为0。
  - `is_panel`: `bool`，表示返回数据格式，默认为False
- 🔢返回值说明
  - `dict`：当`is_panel=0`时，返回一个字典，key为股票代码，value为包含相应数据的`DataFrame`。
  - `pd_Panel`：当`is_panel=1`时，返回一个Panel格式的数据。
- ❗注意事项
  - 返回panel格式数据时，可以用to_frame()方法将数据转换为一个具有mutilindex的二维dataframe
- 📝示例：
  - 调用（返回`dict`）
    ```python
    data_dict = get_resistance_support(
        symbol_list=['600000.SH', '000001.SZ'],
        start_date='20230801',
        end_date='20230810',
        fields=['support_line', 'resistance_line'],
        is_panel=0
    )
    ```
  - 返回值（`dict`）
    ```python
    {'600000.SH':             support_line  resistance_line
    trade_date                     
    2023-08-01          6.82             7.85
    2023-08-02          6.82             7.63, '000001.SZ':             support_line  resistance_line
    trade_date                     
    2023-08-01         11.15           12.500
    2023-08-02         11.15           12.500}
    ```
  - 调用（返回`pd_Panel`）
    ```python
    panel_data = get_resistance_support(
        symbol_list=['600000.SH', '000001.SZ'],
        start_date='20230801',
        end_date='20230810',
        fields=['support_line', 'resistance_line'],
        is_panel=1
    )
    ```
  - 返回值（`pd_Panel`）
    ```python
    <class 'mgquant_mod_mindgo.utils.compat.panel.pd_Panel'>
    Dimensions: 2 (items) x 8 (major_axis) x 2 (minor_axis)
    Items axis: support_line to resistance_line
    Major_axis axis: 2023-08-01T00:00:00.000000000 to 2023-08-10T00:00:00.000000000
    Minor_axis axis: 600000.SH to 000001.SZ
    ```

### 获取基金净值数据：get_extras

- 👑调用方法
  
  ```python
  get_extras(
      security_list,
      start_date,
      end_date,
      fields,
      count=None,
      is_panel=False,
  )
  ```
- 🔧作用
  
  - 用于获取多只基金的净值数据。
- 📚参数说明
  
  - `security_list`: `list`，表示标的代码列表。
  - `start_date`: `None`、`str`或`datetime-like`，表示起始时间。
  - `end_date`: `str`或`datetime-like`，表示结束时间，默认为`'20180101'`。
  - `fields`: `list`，表示需要获取的字段列表。
    - `'unit_net_value'`：单位净值(元/份)
    - `'acc_net_value'`：累计净值(元/份)
    - `'pre_net_value'`：复权净值(元/份)
  - `count`: `Optional[int]`，表示历史长度。`start_date`为 `None`时，`count`必须为正整数时；`start_date`不为 `None`时，`count`必须为0或`None`。
  - `is_panel`: `bool`，表示返回数据格式，默认为`False`。
- 🔢返回值说明
  
  - `dict[str, pandas.DataFrame]`：当`is_panel=False`时，返回一个字典，键为证券代码，值为包含所请求字段的DataFrame。
  - `pd_Panel`：当`is_panel=True`时，返回panel格式数据。
- ❗注意事项
  
  - `start_date` 和 `count` 参数不能同时使用。
  - 返回panel格式数据时，可以用`to_frame()`方法将数据转换为一个具有MultiIndex的二维DataFrame。
- 📝示例：
  
  - 调用
    ```python
    # 获取沪深300ETF和中证500ETF在指定日期的单位净值和累计净值，返回字典格式
    data = get_extras(['510300.SH', '510500.SH'], start_date='20230801', end_date='20230805', fields=['unit_net_value', 'acc_net_value'])
    ```
  - 返回值
    ```python
    {'510300.SH':             unit_net_value  acc_net_value
    2023-08-01          4.0679         1.7316
    2023-08-02          4.0396         1.7211
    2023-08-03          4.0750         1.7342
    2023-08-04          4.0911         1.7402, '510500.SH':             unit_net_value  acc_net_value
    2023-08-01          6.2086         1.9935
    2023-08-02          6.1866         1.9864
    2023-08-03          6.2080         1.9933
    2023-08-04          6.2400         2.0035}
    ```
  - 调用
    ```python
    # 获取沪深300ETF和中证500ETF在指定日期的单位净值和累计净值，返回Panel格式
    panel_data = get_extras(['510300.SH', '510500.SH'], start_date='20230801', end_date='20230805', fields=['unit_net_value', 'acc_net_value'], is_panel=True)
    ```
  - 返回值
    ```python
    <class 'mgquant_mod_mindgo.utils.compat.panel.pd_Panel'>
    Dimensions: 2 (items) x 4 (major_axis) x 2 (minor_axis)
    Items axis: unit_net_value to acc_net_value
    Major_axis axis: 2023-08-01 00:00:00 to 2023-08-04 00:00:00
    Minor_axis axis: 510300.SH to 510500.SH
    ```

### 融资融券数据：get_mtss

- 👑调用方法
  ```python
  get_mtss(
      security_list,
      start_date,
      end_date,
      fields,
      count=None,
      is_panel=False,
  )
  ```
- 🔧作用
  - 用于获取股票的历史融资融券数据。
- 📚参数说明
  - `security_list`: `str`、`list[str]`，表示标的代码。
  - `start_date`: `None`、`str`或`datetime-like`，表示起始时间。
  - `end_date`: `str` 或 `datetime-like`，表示结束时间。
  - `fields`: `list[str]`，表示需要获取的字段。
    - `'fin_value'`：融资余额(元)
    - `'fin_buy_value'`：融资买入额(元)
    - `'fin_refund_value'`：融资偿还额(元)
    - `'sec_value'`：融券余额(元)
    - `'sec_sell_value'`：融券卖出额(元)
    - `'sec_refund_value'`：融券偿还额(元)
    - `'fin_sec_value'`：融资融券余额(元)
  - `count`: `Optional[int]`，表示历史长度。`start_date`为 `None`时，`count`必须为正整数时；`start_date`不为 `None`时，`count`必须为0或`None`。
  - `is_panel`: `bool`，表示返回数据格式，默认为 `False`。为 `True` 时返回 `Panel` 格式，为 `False` 时返回字典格式。
- 🔢返回值说明
  - `dict` 或 `pandas.Panel`，根据 `is_panel` 参数返回不同格式的数据。
    - 当 `is_panel=False` 时，返回 `dict[str, pandas.DataFrame]`，键为股票代码，值为对应股票的融资融券数据 `DataFrame`。
    - 当 `is_panel=True` 时，返回 `pandas.Panel`。
- ❗注意事项
  - 返回 `Panel` 格式数据时，可以用 `to_frame()` 方法将数据转换为一个具有 `MultiIndex` 的二维 `DataFrame`。
  - 仅支持日频数据。
- 📝示例：
  - 调用 (返回字典格式)
    ```python
    # 获取单只股票过去20天的融资融券数据
    data = get_mtss(['000001.SZ'], end_date='20230801', fields=['fin_value', 'sec_value'], count=20)
    ```
  - 返回值
    ```python
    # {'000001.SZ':                fin_value   sec_value
    # 2023-07-05  4.303148e+09  28070628.0
    # 2023-07-06  4.311947e+09  30216087.0
    # 2023-07-07  4.321500e+09  30577837.0
    # ...}
    ```
  - 调用 (返回Panel格式)
    ```python
    # 获取多只股票的融资融券Panel数据
    panel_data = get_mtss(['000001.SZ', '600000.SH'], end_date='20230801', fields=['fin_value', 'sec_value'], count=20, is_panel=True)
    ```
  - 返回值
    ```python
    # <class 'pd_Panel'>
    # Dimensions: 2 (items) x 20 (major_axis) x 2 (minor_axis)
    # Items axis: fin_value to sec_value
    # Major_axis axis: 2023-07-05 00:00:00 to 2023-08-01 00:00:00
    # Minor_axis axis: 000001.SZ to 600000.SH
    ```

### 获取历史资金数据：get_money_flow_step

- 👑调用方法
  
  ```python
  get_money_flow_step(
      security_list,
      start_date,
      end_date,
      fre_step,
      fields,
      count=None,
      is_panel=False
  )
  ```
- 🔧作用
  
  - 用于获取股票的历史资金流向数据
- 📚参数说明
  
  - `security_list`: `list[str]`，表示标的代码列表
  - `start_date`:`None`、`str`或`datetime-like`，表示起始时间。
  - `end_date`: `str`、`int`、`float`或`datetime-like`，表示结束时间，默认为'20180101'
  - `fre_step`: `str`，表示时间步长，支持'1d'、'30m'、'5m'三种步长，默认为'1d'
  - `fields`: `list`，表示需要获取的字段，可参考[资金流向数据](http://quant.10jqka.com.cn/view/dataplatform/detail/125)，默认为全部字段
  - `count`: `Optional[int]`，表示历史长度。`start_date`为 `None`时，`count`必须为正整数时；`start_date`不为 `None`时，`count`必须为0或`None`。
  - `is_panel`: `bool`，表示返回数据格式，默认为False
- 🔢返回值说明
  
  - 当`is_panel=False`时返回`dict`，key为股票代码，value为DataFrame；
  - 当`is_panel=True`时返回`pd_Panel`
- ❗注意事项
  
  - 返回panel格式数据时，可以用to_frame()方法将数据转换为一个具有mutilindex的二维dataframe
  - 大单、中单、小单的标准如下：
    
    A.上证A股、深证主板大单标准：
    
    | 类型   | 标准                                      |
| ------ | ----------------------------------------- |
| 小单   | 1万股以下         或     5万元以下        |
| 中单   | 1万股到6万股       或     5万元—30万元   |
| 大单   | 6万股到20万股      或     30万元—100万元 |
| 特大单 | 20万股以上        或     100万元以上      |
    
    B.中小板、创业板大单标准：
    
    | 类型   | 金额                                 |
| ------ | ------------------------------------ |
| 小单   | 5万元以下                            |
| 中单   | 5万元—20万元(包括5万，不包括20万)   |
| 大单   | 20万元—50万元(包括20万，不包括50万) |
| 特大单 | 50万元以上                           |
    
    
- 📝示例：
  
  - 调用（返回字典格式）
    ```python
    data = get_money_flow_step(
        security_list=['000001.SZ', '600000.SH'],
        start_date='20230801',
        end_date='20230810',
        fields=['act_buy_xl'],
        is_panel=False
    )
    ```
  - 返回值（字典格式）
    ```python
    {'000001.SZ':              act_buy_xl
    2023-08-01   77794210.0
    2023-08-02  144867230.0
    2023-08-03  271395280.0
    2023-08-04  174036910.0
    2023-08-07   26917745.0
    2023-08-08   72404551.0
    2023-08-09   90129986.0
    2023-08-10   29415443.0, '600000.SH':             act_buy_xl
    2023-08-01  18543544.0
    2023-08-02  28330619.0
    2023-08-03  19100554.0
    2023-08-04  16758347.0
    2023-08-07   3185453.0
    2023-08-08   6347852.0
    2023-08-09   5820379.6
    2023-08-10   7758793.8}
    ```
  - 调用（返回Panel格式）
    ```python
    data = get_money_flow_step(
        security_list=['000001.SZ', '600000.SH'],
        start_date='20230801',
        end_date='20230810',
        fields=['act_buy_xl'],
        is_panel=True
    )
    ```
  - 返回值（Panel格式）
    ```python
    <class 'pd_Panel'>
    Dimensions: 1 (items) x 8 (major_axis) x 2 (minor_axis)
    Items axis: act_buy_xl to act_buy_xl
    Major_axis axis: 2023-08-01T00:00:00.000000000 to 2023-08-10T00:00:00.000000000
    Minor_axis axis: 000001.SZ to 600000.SH
    ```






## 证券信息数据接口
### 获取单只证券的基本信息：get_security_info

- 👑调用方法
  
  ```
  get_security_info(symbol)
  ```
- 🔧作用
  
  - 用于获取单只证券的基本信息
- 📚参数说明：
  
  - `symbol`: `str`，表示股票、期货、基金、指数等证券标的对应的同花顺代码
- 🔢返回值说明：
  
  - `Instrument`，返回一个`Instrument`对象，包含证券的各项基本信息，如证券名称、上市交易所、证券类型、上市日期等，通过取类属性来使用，如`instrument.display_name`
- ❗注意事项：
  
  - `symbol`需要满足同花顺的格式，否则无法正常取到数据
  - 该函数获取的标的简称在回测中不可用于判断是否为ST股
- 📝示例：
  
  - 调用：
    
    ```python
    data = get_security_info('000001.SZ')
    ```
  - 返回值：
    
    ```python
    Instrument(benchmark=None, de_listed_date=datetime.datetime(2200, 1, 1, 0, 0), display_name='平安银行', end_date=datetime.datetime(2200, 1, 1, 0, 0), exchange='深交所', listed_date=datetime.datetime(1991, 4, 3, 0, 0), market1='212100', market2='001001', market_hq='33', min_round_lot=0, name='payh', order_book_id='000001.SZ', parent='nan', price_limit=0.0, round_lot=100, start_date=datetime.datetime(1991, 4, 3, 0, 0), symbol='000001.SZ', symbol_hq='000001', type='stock', underlying_symbol=None)
    ```

### 获取所有证券信息：get_all_securities

- 👑调用方法
  
  ```
  get_all_securities(ty=None, date=None)
  ```
- 🔧作用
  
  - 获取指定日期所有上市证券列表及其基本信息。
- 📚参数说明：
  
  - `ty`: `Optional[str]`，证券类型，默认取所有证券类型
    - `ty='stock'`：A股
    - `ty='hstock'`：港股
    - `ty='ustock'`：美股
    - `ty='index'`：指数
    - `ty='etf'`：ETF基金
    - `ty='lof'`：LOF基金
    - `ty='fja'`：分级A基金
    - `ty='fjb'`：分级B基金
    - `ty='qdii'`：qdii基金
    - `ty='ota'`：场外基金
    - `ty='fund'`：资产支持证券
    - `ty='futures'`：金融期货
    - `ty='commodity_futures'`：商品期货
    - `ty='bond_futures'`：国债期货
    - `ty='option'`：ETF期权
    - `ty='cbond'`：A股可转债
    - `ty='forex'`：外汇（中国银行双向宝）合约
    - `ty='metal'`：T+D延期交收合约
  - `date`: `Optional[str]`，查询日期，格式为 'YYYYMMDD'。回测时默认为当前回测时间的前一交易日，研究环境中默认为前一交易日
- 🔢返回值说明：
  
  - `pandas.DataFrame`，返回一个DataFrame，索引为证券代码，列包括证券简称、上市日期、退市日期、类型等信息。
- ❗注意事项：
  
  - 该函数获取的标的简称在回测中不可用于判断是否为ST股。
- 📝示例：
  
  - 调用：
    ```python
    #查询2023年8月1日处于上市状态的沪京深股票信息
    data = get_all_securities('stock','20230801')
    print(data)
    ```
  - 返回值：
    ```
    benchmark de_listed_date display_name   end_date exchange  \
    symbol                                                  
    002789.SZ      None     2200-01-01        *ST建艺 2200-01-01      深交所   
    600562.SH      None     2200-01-01         国睿科技 2200-01-01      上交所   
    ...             ...            ...          ...        ...      ...   
    
             listed_date market1 market2 market_hq  min_round_lot  name  \
    symbol                                                   
    002789.SZ  2016-03-11  212100  001001        33              0  stjy   
    600562.SH  2003-01-28  212001  001001        17              0  grkj   
    ...               ...     ...     ...       ...            ...   ...   
    
             order_book_id parent  price_limit  round_lot start_date symbol_hq  \
    symbol                                                          
    002789.SZ     002789.SZ    nan         0.00        100 2016-03-11    002789   
    600562.SH     600562.SH    nan         0.00        100 2003-01-28    600562   
    ...                 ...    ...          ...        ...        ...       ...   
    
                type underlying_symbol  
    symbol                
    002789.SZ  stock              None  
    600562.SH  stock              None  
    ...          ...               ...  
    
    [5453 rows x 19 columns]
    ```

### 获取期货期权品种相关信息：get_futures_info

- 👑调用方法
  
  ```
  get_futures_info(symbol, date=None)
  ```
- 🔧作用
  
  - 用于获取期货品种的相关信息。
- 📚参数说明：
  
  - `symbol`: `str`，表示期货品种类型。
  - `date`: `Optional[str]`，表示查询日期，回测时默认为当前回测时间的前一交易日，研究环境中默认为前一交易日。
- 🔢返回值说明：
  
  - `dict`，返回一个字典，包含期货品种的详细信息。字典的键值说明如下：
    - `'symbol'`: `str`，期货合约代码。
    - `'name'`: `str`，期货合约名称。
    - `'commission'`: `float`，手续费率。
    - `'margin_rate'`: `float`，保证金率。
    - `'contract_multiplier'`: `float`，合约乘数。
    - `'exchange'`: `str`，交易所名称。
    - `'unit'`: `float`，交易单位。
- 📝示例：
  
  - 调用
    ```python
    # 查询螺纹钢期货的2023年8月1日的品种信息
    data = get_futures_info('RB', '20230801')
    ```
  - 返回值
    ```python
    {'symbol': 'RB', 'name': '螺纹钢', 'commission': 0.0001, 'margin_rate': 0.05, 'contract_multiplier': 10.0, 'exchange': '上海期货交易所', 'unit': 1.0}
    ```

### 获取主力合约代码：get_futures_dominate

- 👑调用方法：
  ```
  get_futures_dominate(symbol, date=None, seq=0)
  ```
- 🔧作用：
  - 获取指定期货品种的主力合约代码
- 📚参数说明：
  - `symbol`: `str`，期货合约品种代码，例如螺纹钢期货为'RB'
  - `date`: `Optional[str]`，查询日期，回测时默认为当前回测时间的前一交易日，研究环境中默认为前一交易日
  - `seq`: `int`，序列号，用于指定返回第几个主力合约，默认为0表示主力合约
- 🔢返回值说明：
  - `str`，返回字符串，表示主力合约代码
- ❗注意事项：
  - 当seq=0时返回当前主力合约代码
- 📝示例：
  - 调用：`get_futures_dominate('RB', '20230801', 0)`
  - 返回值：`'RB2310'`

### 获取指定品种所有可交易的合约：get_future_code

- 👑调用方法：
  
  ```python
  get_future_code(underlying_symbol, date=None)
  ```
- 🔧作用
  
  - 获取指定品种所有可交易的期货合约
- 📚参数说明：必须根据函数签名，保证参数完整
  
  - `underlying_symbol`: `str`，品种名称，例如：'RB'
  - `date`: `Optional[str]`，获取合约的时间，时间格式：'%Y%m%d'
- 🔢返回值说明
  
  - `list`，返回合约代码列表，例如：['RB1809', 'RB1810', 'RB1811', ...]
- ❗注意事项：若无可省略
- 📝示例：
  
  - 调用
    
    ```python
    future_code_all = get_future_code('RB', '20180910')
    ```
  - 返回值
    
    ```python
    ['RB1809', 'RB1810', 'RB1811', 'RB1812', 'RB1901', 'RB1902', 'RB1903', 'RB1904', 'RB1905', 'RB1906', 'RB1907', 'RB1908']
    ```

### 获取可交易的期权合约列表：get_option_code

- 👑调用方法
  ```python
  get_option_code(date=None)
  ```
- 🔧作用
  - 用于获取当前所有可交易的沪深交易所ETF期权合约。
- 📚参数说明
  - `date`: `Optional[str]`，表示查询日期。
- 🔢返回值说明
  - `DataFrame`，返回一个DataFrame，包含可交易的期权合约代码(symbol)和到期月份(month)信息。
- 📝示例：
  - 调用
    ```python
    # 获取指定日期的期权合约代码
    options_all = get_option_code('20230801')
    ```
  - 返回值
    ```python
    symbol month
    0    90001832.SZ  None
    1    90001824.SZ  None
    2    90002275.SZ  None
    3    90002114.SZ  None
    4    90002105.SZ  None
    ```

### 获取指数成份股：get_index_stocks

- 👑调用方法
  
  ```python
  get_index_stocks(symbol, date=None)
  ```
- 🔧作用
  
  - 用于获取指定指数在指定日期的成分股股票代码列表
- 📚参数说明
  
  - `symbol`: `str`，表示指数代码，如 `'000016.SH'`
  - `date`: `Optional[str]`，表示查询日期，格式为 'YYYYMMDD'，回测时默认为当前回测时间的前一交易日，研究环境中默认为前一交易日
- 🔢返回值说明
  
  - `list`，返回字符串列表，每个元素为一个成分股的股票代码（如 `'600519.SH'`）
- ❗注意事项
  
  - 该函数若在模拟交易的 init 函数中使用，则必须填写 date 参数
- 📝示例：
  
  - 调用
    
    ```python
    stock_list = get_index_stocks('000016.SH', '20230801')
    ```
  - 返回值
    
    ```python
    ['600436.SH', '603288.SH', '600519.SH', '601857.SH', '600036.SH', '600050.SH', '603260.SH', '601288.SH', '601166.SH', '600900.SH', '601012.SH', '600309.SH', '600406.SH', '600031.SH', '600010.SH', '600048.SH', '600809.SH', '688111.SH', '601088.SH', '603799.SH', '601398.SH', '601066.SH', '600887.SH', '600111.SH', '601669.SH', '601318.SH', '600690.SH', '600276.SH', '600028.SH', '603501.SH', '600745.SH', '601888.SH', '601728.SH', '600905.SH', '600438.SH', '603986.SH', '600089.SH', '601919.SH', '600030.SH', '601668.SH', '603259.SH', '601390.SH', '601225.SH', '601628.SH', '600893.SH', '600104.SH', '601899.SH', '601633.SH', '688599.SH', '600196.SH']
    ```

### 获取指数成份股权重：get_index_weight

- 👑调用方法
  
  ```python
  get_index_weight(symbol, date=None)
  ```
- 🔧作用
  
  - 用于获取指定指数在指定日期的成分股权重数据，返回包含股票代码和对应权重的DataFrame
- 📚参数说明
  
  - `symbol`: `str`，表示指数代码，如'000016.SH'
  - `date`: `Optional[str]`，表示查询日期，格式为'YYYYMMDD'；回测时默认为当前回测时间的前一交易日，研究环境中默认为前一交易日
- 🔢返回值说明
  
  - `pandas.core.frame.DataFrame`，返回包含两列的DataFrame：'symbol'（股票代码）和'weight'（权重值），权重为百分比形式
- ❗注意事项
  
  - 部分等权指数会返回空的DataFrame，例如同花顺指数
  - 该函数若在模拟交易的init函数中使用，则必须填写date参数
- 📝示例：
  
  - 调用
    
    ```python
    weight = get_index_weight('000016.SH', '20230801')
    ```
  - 返回值
    
    ```python
    symbol  weight
    0  600309.SH   2.627
    1  600104.SH   1.033
    2  600030.SH   3.356
    ...
    49 600893.SH   0.769
    ```

### 获取指数列表：get_index_list

- 👑调用方法
  ```python
  get_index_list(suffix, date=None)
  ```
- 🔧作用
  - 根据指数代码后缀查询对应的指数列表
- 📚参数说明
  - `suffix`: `str`，表示指数代码后缀，如 'TI'
  - `date`: `Optional[str]`，表示查询日期，格式为 'YYYYMMDD'，回测时默认为当前回测时间的前一交易日，研究环境中默认为前一交易日
- 🔢返回值说明
  - `list`，返回字符串列表，每个元素为完整的指数代码（如 '885760.TI'）
- ❗注意事项
  - 返回列表中的指数代码格式为「六位数字+后缀」，后缀由 `suffix` 参数指定
  - 若无匹配指数，返回空列表
- 📝示例：
  - 调用
    ```python
    index_list = get_index_list('TI', '20230801')
    ```
  - 返回值
    ```python
    ['885760.TI', '883400.TI', '885423.TI', ...]
    ```

### 获取行业成份股：get_industry_stocks

- 👑调用方法
  ```python
  get_industry_stocks(symbol, date=None)
  ```
- 🔧作用
  - 用于获取指定行业指数代码在指定日期的成分股股票代码列表
- 📚参数说明
  - `symbol`: `str`，表示行业指数代码，如'CI311000'
  - `date`: `Optional[str]`，表示查询日期，格式为'YYYYMMDD'；回测时默认为当前回测时间的前一交易日，研究环境中默认为前一交易日
- 🔢返回值说明
  - `list`，返回字符串列表，每个元素为一个股票代码（如'600693.SH'）
- ❗注意事项
  - 返回的股票代码包含交易所后缀（如'.SH'或'.SZ'），请确保与目标系统兼容
- 📝示例：
  - 调用
    ```python
    index_list = get_industry_stocks('CI311000', '20230801')
    ```
  - 返回值
    ```python
    ['600693.SH', '601366.SH', '600694.SH', '002251.SZ', '601116.SH', '000759.SZ', '600697.SH', '601010.SH', '000564.SZ', '002561.SZ', '002336.SZ', '600712.SH', '600280.SH', '603031.SH', '002419.SZ', '600729.SH', '002187.SZ', '603123.SH', '600738.SH', '600628.SH', '000501.SZ', '605188.SH', '600778.SH', '603708.SH', '603101.SH', '002697.SZ', '600785.SH', '601086.SH', '000419.SZ', '600814.SH', '000417.SZ', '600306.SH', '600824.SH', '600827.SH', '600828.SH', '600838.SH', '000679.SZ', '600858.SH', '600859.SH', '600861.SH', '000715.SZ', '600865.SH', '000882.SZ', '002277.SZ', '601933.SH', '002264.SZ']
    ```

### 获取行业分类信息：get_industry_relate

- 👑调用方法
  ```python
  get_industry_relate(date='now', types='industryid1', fields=None)
  ```
- 🔧作用
  - 用于获取A股行业分类信息，可查到行业分类及对应代码。
- 📚参数说明
  - `date`: `str`，表示查询日期，默认为 `'now'`。
  - `types`: `str`，表示行业分类类型，可以参考[行业分类信息字段](http://quant.10jqka.com.cn/view/dataplatform/detail/24)，默认为 `'industryid1'`。
  - `fields`: `Optional[list[str]]`，表示字段名，默认为 `None` 即返回所有字段。可以参考[行业分类信息字段](http://quant.10jqka.com.cn/view/dataplatform/detail/24)。
- 🔢返回值说明
  - `pandas.DataFrame`，返回DataFrame，包含行业分类的详细信息，如行业名称、代码、类型等。
- 📝示例：
  - 调用
    ```python
    # 查询2023年8月1日中信二级行业分类信息
    industry_info = get_industry_relate(date='20230801', types='ci_industryid2')
    print(industry_info.head())
    ```
  - 返回值
    ```python
    available_date disabled_date industry_index  industry_rank  \
    industry_name
    一般零售                    None          None       CI005811            2.0
    专业市场经营Ⅱ           2019-12-02          None       CI005815            2.0
    专用机械                    None          None       CI005805            2.0
    专用材料Ⅱ             2019-12-02          None       CI005800            2.0
    专营连锁              2019-12-02          None       CI005813            2.0
    
                                  industry_symbol industry_thscode industry_type industry_typecode
    industry_name
    一般零售                 CI311000      CI005811.CI          中信行业            002012
    专业市场经营Ⅱ              CI315000      CI005815.CI          中信行业            002012
    专用机械                 CI262000      CI005805.CI          中信行业            002012
    专用材料Ⅱ                CI246000      CI005800.CI          中信行业            002012
    专营连锁                 CI313000      CI005813.CI          中信行业            002012
    ```

### 获取股票所属行业数据：get_symbol_industry

- 👑调用方法
  ```python
  get_symbol_industry(symbol, date=None)
  ```
- 🔧作用
  - 用于获取个股的行业分类信息，支持同花顺行业分类、申万行业分类、中信行业分类、证监会行业分类、标普行业分类。
- 📚参数说明
  - `symbol`: `str`，表示股票代码
  - `date`: `Optional[str]`，表示查询日期，默认为None
- 🔢返回值说明
  - `Symbol_Industry`，返回一个Symbol_Industry对象，包含多个行业分类信息。
- 📝示例：
  - 调用
    ```python
    # 查询指定股票在特定日期的行业分类信息
    get_symbol_industry('300033.SZ', date='20230801')
    ```
  - 返回值
    ```python
    Symbol_Industry(date=Timestamp('2023-08-01 00:00:00'), industryid1='T10', industryid2='T1003', industryid3='T100301', s_industryid1='S71', s_industryid2='S7104', s_industryid3='S710401', c_industryid='69', c_industryid2='J', ci_industryid1='CI620000', ci_industryid2='CI625000', ci_industryid3='CI625010', gi_industryid1='45', gi_industryid2='4510', gi_industryid3='451030', gi_industryid4='45103010')
    ```

### 获取所有同花顺概念成分股：get_concept_stocks

- 👑调用方法
  ```python
  get_concept_stocks(symbol, date=None)
  ```
- 🔧作用
  - 用于获取指定概念下的成分股。
- 📚参数说明
  - `symbol`: `str`，概念代码或者概念指数代码。
  - `date`: `Optional[str]`，查询日期，格式为 'YYYYMMDD'，如 '20230801'。回测时默认为当前回测时间的前一交易日，研究环境中默认为前一交易日。
- 🔢返回值说明
  - `list`，返回一个列表，包含指定概念的成分股代码。
- ❗注意事项
  - 通常在同花顺行情软件上能看到行情的都是概念指数，代码以TI结尾。
  - 概念不一定有对应的概念指数。
  - 概念指数的成分股也可以通过 `get_index_stocks`函数获取。
- 📝示例：
  - 调用
    ```python
    stock_list = get_concept_stocks('886031.TI', date='20230801')
    ```
  - 返回值
    ```python
    ['300235.SZ', '002722.SZ', '300229.SZ', '688609.SH', ...]
    ```

### 获取所有同花顺概念信息：get_concept_relate

- 👑调用方法
  ```python
  get_concept_relate(date='now', levels=None, fields=None)
  ```
- 🔧作用
  - 用于获取所有同花顺概念分类信息及对应的指数代码。
- 📚参数说明
  - `date`: `str`，表示查询日期，默认为'now'
  - `levels`: `Optional[str | list]`，表示概念类型，默认为None，即获取所有概念
  - `fields`: `Optional[list[str]]`，表示需要查询的字段，默认为None，即返回所有字段，参照[同花顺概念分类](https://quant.10jqka.com.cn/view/dataplatform/detail/66)
- 🔢返回值说明
  - `pandas.DataFrame`，返回一个DataFrame，包含同花顺概念的名称、代码、类型、级别等信息。
- ❗注意事项
  - 通常在同花顺行情软件上能看到行情的都是概念指数，代码以TI结尾
  - 概念不一定有对应的概念指数
- 📝示例：
  - 调用
    ```python
    concept_info = get_concept_relate(date='20230801')
    ```
  - 返回值
    ```python
    concept_symbol concept_code ... concept_thscode available_date
    concept_name                                          ...                         
    2021年送转填权概念              308986     00090126 ...       883402.TI     2022-07-01
    3D打印                         301963     00060044 ...            None           None
    3D打印                         300127     00030035 ...       885537.TI     2014-04-25
    3D打印[US]                     306516     00040130 ...       865045.TI     2019-01-28
    3D玻璃                         302116     00032341 ...            None           None
    ```

### 获取指定时间段交易日：get_trade_days

- 👑调用方法
  ```python
  get_trade_days(start_date=None, end_date='20180101', count=None)
  ```
- 🔧作用
  - 获取沪深京交易所指定时间段交易日
- 📚参数说明
  - `start_date`: `None`、`str`、 `int`、`datetime_like`，起始日期，默认为None
  - `end_date`: `str, int, datetime_like`，结束日期，默认为'20180101'
  - `count`: `Optional[int]`，交易日数量
- 🔢返回值说明
  - `pandas.core.indexes.datetimes.DatetimeIndex`，返回指定时间段的交易日
- ❗注意事项
  - 当start_date、end_date全部不为None时，count参数不生效
- 📝示例：
  - 调用
    ```python
    tdays_list = get_trade_days('20230101', '20230801')
    ```
  - 返回值
    ```python
    DatetimeIndex(['2023-01-03', '2023-01-04', '2023-01-05', '2023-01-06',
                   '2023-01-09', '2023-01-10', '2023-01-11', '2023-01-12',
                   '2023-01-13', '2023-01-16',
                   ...
                   '2023-07-19', '2023-07-20', '2023-07-21', '2023-07-24',
                   '2023-07-25', '2023-07-26', '2023-07-27', '2023-07-28',
                   '2023-07-31', '2023-08-01'],
                  dtype='datetime64[ns]', length=140, freq=None)
    ```

### 获取所有交易日：get_all_trade_days

- 👑调用方法
  ```python
  get_all_trade_days()
  ```
- 🔧作用
  - 用于获取沪深京交易所所有交易日。
- 🔢返回值说明
  - `pandas.core.indexes.datetimes.DatetimeIndex`，返回一个时间索引对象，包含了从历史至今的所有交易日日期。
- 📝示例：
  - 调用
    ```python
    tdays = get_all_trade_days()
    ```
  - 返回值
    ```python
    DatetimeIndex(['1990-12-19', '1990-12-20', '1990-12-21', '1990-12-24',
                   '1990-12-25', '1990-12-26', '1990-12-27', '1990-12-28',
                   '1990-12-31', '1991-01-02',
                   ...
                   '2028-12-18', '2028-12-19', '2028-12-20', '2028-12-21',
                   '2028-12-22', '2028-12-25', '2028-12-26', '2028-12-27',
                   '2028-12-28', '2028-12-29'],
                  dtype='datetime64[ns]', length=9285, freq=None)
    ```

### 获取因子数据：get_sfactor_data

- 👑调用方法
  ```python
  get_sfactor_data(start_date, end_date, stocks, factor_names)
  ```
- 🔧作用
  - 用于获取经过数据处理（去极值、标准化）后的因子数据。
- 📚参数说明
  - `start_date`: `str, int, datetime_like`，表示起始日期
  - `end_date`: `str, int, datetime_like`，表示结束日期
  - `stocks`: `list`，表示股票池
  - `factor_names`: `list`，表示因子池
    - [技术指标类因子](http://quant.10jqka.com.cn/view/dataplatform/detail/285)
    - [财务指标类因子](http://quant.10jqka.com.cn/view/dataplatform/detail/289)
- 🔢返回值说明
  - `dict`，返回字典，表示因子数据。字典的键为因子名，值为一个 pandas.DataFrame，该 DataFrame 的索引为股票代码，列为日期，值为处理后的因子值。
- ❗注意事项
  - 此函数支持获取自定义因子
- 📝示例：
  - 调用
    ```python
    start_date, end_date = '20230801', '20230805'
    stocks, factor_names = ['600519.SH','300033.SZ'], ['macd']
    result = get_sfactor_data(start_date, end_date, stocks, factor_names)
    ```
  - 返回值
    ```python
    {'macd':            2023-08-01  2023-08-02  2023-08-03  2023-08-04
    600519.SH     32.4820     28.7126     24.1070     21.2735
    300033.SZ      6.0546      5.8856      6.6241      6.9331}
    ```













## 表数据接口
#### 构建数据表查询对象：query

- 👑调用方法：
  
  ```
  query(*args, **kwargs)
  ```
- 🔧作用：
  
  - 构造query对象，传入需要取数的信息，支持的数据可在[SuperMind数据平台](http://quant.10jqka.com.cn/view/dataplatform)中查询
- 📚参数说明
  
  - 传入数据表对象，或数据表的个别字段
- 🔢返回值说明
  
  - `Query`，在[`run_query`](https://quant.10jqka.com.cn/view/help/4#%E5%8F%96%E8%A1%A8%E6%95%B0%E6%8D%AE-run-query)和[`get_fundamentals`](https://quant.10jqka.com.cn/view/help/4#%E5%8F%96%E8%B4%A2%E5%8A%A1%E8%A1%A8%E6%95%B0%E6%8D%AE-get-fundamentals)中使用
- 🚀️使用方法：
  
  - 取整张表
    
    ```python
    #取concept_classification表
    q = query(concept_classification)
    ```
  - 仅取某字段：有时候不需要把整张表取出，仅仅想取表中的某几个字段
    
    ```python
    #只取concept_classification表的symbol、date、concept三个字段
    q = query(
        concept_classification.symbol,#格式为：表名.字段
        concept_classification.date,
        concept_classification.concept
    )
    ```
  - filter操作：设置条件，相当于SQL中的where方法
    
    ```python
    #只取concept_classification表的symbol、date、concept三个字段，并只取同花顺2023年2月1日之后的数据
    q = query(
        concept_classification.symbol,#格式为：表名.字段
        concept_classification.date,
        concept_classification.concept
    ).filter(
        concept_classification.symbol=='300033.SZ',
        concept_classification.date>'20230201'
    )
    ```
    
    ```python
    #只取concept_classification表的symbol、date、concept三个字段，并取同花顺、贵州茅台在2023年2月1日当天的数据
    q = query(
        concept_classification.symbol,#格式为：表名.字段
        concept_classification.date,
        concept_classification.concept
    ).filter(
        concept_classification.symbol.in_(['300033.SZ','600519.SH']),
        concept_classification.date=='20230201'
    )
    ```
  - limit操作：指定查询前n行数据
    
    ```python
    #只取concept_classification表的symbol、date、concept三个字段的前10行
    q = query(
        concept_classification.symbol,#格式为：表名.字段
        concept_classification.date,
        concept_classification.concept
    ).limit(10)
    ```
  - order_by操作：指定一列数据进行排序
    
    ```python
    #只取concept_classification表的symbol、date、concept，并跟据date降序排列
    q = query(
        concept_classification.symbol,#格式为：表名.字段
        concept_classification.date,
        concept_classification.concept
    ).order_by(
        concept_classification.date.desc()
    )
    ```
- ❗注意事项：
  
  - order_by从大到小排序则使用：.desc(),从小到大排序则使用：.asc()
  - 更多详细使用方法可以参考[sqlalchemy官方文档](https://docs.sqlalchemy.org/en/20/orm/query.html)
  - 构造完query对象后需要用 `run_query`或者 `get_fundamentals`取数

#### 取表数据：run_query

- 👑调用方法：
  
  ```
  run_query(query_object)
  ```
- 🔧作用：
  
  - 查询函数，可查询除财务数据表以外的所有数据表
- 📚参数说明：
  
  - `query_object`: `Query`，构造方法可参考[query](https://quant.10jqka.com.cn/view/help/4#%E6%9E%84%E5%BB%BA%E6%95%B0%E6%8D%AE%E8%A1%A8%E6%9F%A5%E8%AF%A2%E5%AF%B9%E8%B1%A1-query)
- 🔢返回值说明
  
  - `pd.DataFrame`，index为序号，column为`f"{表名}_{字段名称}"`
- ❗注意事项：
  
  - 财务数据表不支持使用此函数查询
  - 支持的数据可在[SuperMind数据平台](http://quant.10jqka.com.cn/view/dataplatform)中查询
- 📝示例：
  
  - 调用
    
    ```
    data = run_query(query(concept_classification).limit(5))
    ```
  - 返回值
    
    ```
    concept_classification_symbol concept_classification_date
    0                     000001.SZ                    20130221
    1                     000001.SZ                    20130225
    2                     000001.SZ                    20130227
    3                     000001.SZ                    20130304
    4                     000001.SZ                    20130306
    
    concept_classification_concept
    0                           融资融券
    1                           融资融券
    2                     融资融券,转融券标的
    3                     融资融券,转融券标的
    4                     融资融券,转融券标的
    ```

#### 取财务表数据：get_fundamentals

- 👑调用方法：
  
  ```
  get_fundamentals(query_object, date=None, statDate=None, latest=False)
  ```
- 🔧作用：
  
  - 查询函数，可查询财务数据表
- 📚参数说明：
  
  - `query_object`: `Query`，构造方法可参考[query](https://quant.10jqka.com.cn/view/help/4#%E6%9E%84%E5%BB%BA%E6%95%B0%E6%8D%AE%E8%A1%A8%E6%9F%A5%E8%AF%A2%E5%AF%B9%E8%B1%A1-query)
  - `date`: `str`，`date`和`statDate`只能并且必须填写一个，格式'%Y%m%d'。例如：'20170808'(必须是交易日)
  - `statDate`: `str`，`date`和`statDate`只能并且必须填写一个，
    - 季报：'年+q+季度序号'，例如：'2015q1'表示2015年一季报年报：
    - 年报，例如：'2015'表示2015年年报
  - `latest`：`bool`，是否返回最新的财报，个别情况下可能存在财报修正
- 🔢返回值说明
  
  - `pd.DataFrame`，index为序号，column为`f"{表名}_{字段名称}"`
- ❗注意事项：
  
  - 此函数仅支持查询财务数据表，列表如下：
    - `valuation` - 估值指标表
    - `balance` - 资产负债表
    - `cashflow` - 现金流量表
    - `income` - 利润表
    - `operating` - 运营能力表
    - `debtrepay` - 偿还能力表
    - `profit_report` - 业绩快报
    - `profit` - 盈利能力表
    - `growth` - 成长能力表
    - `asharevalue` - 估值指标表
    - `ashareoperate` - 运营能力表
    - `asharedebt` - 偿还能力表
    - `ashareprofit` - 盈利能力表
    - `cashflow_sq` - 现金流量表(单季度)
    - `income_sq` - 利润表(单季度)
    - `profit_sq` - 盈利能力表(单季度)
    - `growth_sq` - 成长能力表(单季度)
    - `profit_forecast` - 业绩预告
  - date和statDate参数传其中之一即可
  - date和statDate全为None时，date默认取当前时间的前一日
  - 支持的数据可在[SuperMind数据平台](http://quant.10jqka.com.cn/view/dataplatform)中查询
- 📝示例：
  
  - 调用
    
    ```python
    #查询2023年8月1日的总市值数据，并降序排列
    data = get_fundamentals(
    	query(
    		valuation.symbol,
    		valuation.market_cap
    	).order_by(
    		valuation.market_cap.desc()
    	),
    	date = '20230810'
    )
    print(data.head())
    ```
  - 返回值
    
    ```python
    valuation_symbol  valuation_market_cap
    0        600519.SH          2.355371e+12
    1        601398.SH          1.550490e+12
    2        601857.SH          1.396562e+12
    3        600941.SH          1.212461e+12
    4        601288.SH          1.199709e+12
    ```









## 问财接口
### 问财接口使用前必读

问财选股接口因为他的便利和速度而广受喜欢。

然而问财的诞生之初是用于实时选股，而非回测。所以在回测的场景必然会存在一些问题。这些问题解决需要时间和精力，如果你发现问题记得及时反馈给supermind官方。我们会持续推动解决。

建议用问财来快速验证想法，然后自己用pyhton实现代码是比较好的方式。

`query_iwencai` 和 `get_iwencai` 的结果是不一样的，因为二者调用的服务是不一样的：`query_iwencai`，基于[i问财智能投顾](https://www.iwencai.com/)，主要用于实时选股，注意，目前iwencai分为2套，API返回结果与旧版是一致的；`get_iwencai`基于[BackTest 量化策略平台 (10jqka.com.cn)](https://backtest.10jqka.com.cn/)，主要用于历史回测，`get_iwencai` 为了避免一些未来函数，会再回测环境对某些语句不可用，会出现iwencai初始化失败的提示。

自然语言解析较为复杂，最好先到对应的问财网站对问句进行试验，确认解析结果没有问题之后，再应用到策略当中。

### 问财实时数据：query_iwencai (研究环境使用)

- 👑调用方法
  ```python
  query_iwencai(query, domain='股票', timeout=6, df=True)
  ```
- 🔧作用
  - 用于通过输入自然语言，执行智能选股并获取股票列表
- 📚参数说明
  - `query`: `str`，表示自然语句
  - `domain`: `str`，可选'股票'、'基金'、'指数'、'新三板'、'港股'、'美股'，默认为'股票'
  - `timeout`: `int`，表示超时时间，默认为6
  - `df`: `bool`，表示是否格式化为DataFrame，默认为True
- 🔢返回值说明
  - `pandas.DataFrame`或`list`，当df=True时返回DataFrame，当df=False时返回list，包含选股结果
- ❗注意事项
  - 该函数可获得和网页版问财相同的结果
  - 该函数有调用次数限制，每15分钟内限制调用5000次
  - 该函数不是为回测而设计，回测中慎用
- 📝示例：
  - 调用
    ```python
    query_iwencai("市值>1000亿，日成交额>30亿，换手率大于4.5%")
    ```
  - 返回值
    ```python
    股票代码     股票简称     总市值       成交额       换手率
    0  301308.SZ  江波龙  1.517310e+12   4395865700.00   4.52
    1  000988.SZ  华工科技  1.221896e+12   9411697100.00   7.85
    2  688525.SH  佰维存储  1.156106e+12   5972511300.00   5.15
    ```
  - 调用
    ```python
    query_iwencai("市值>1000亿，日成交额>30亿，换手率大于4.5%", df=False)
    ```
  - 返回值
    ```python
    [{'股票代码': '301308.SZ', '股票简称': '江波龙','总市值': 123398012088.76, '成交额': '4346865700.00', '换手率: '4.52'}]
    ```

### 问财昨日数据：get_iwencai(回测环境使用)

- 👑调用方法
  
  ```python
  get_iwencai(question, set_attr='iwencai_securities', version=None)
  ```
- 🔧作用
  
  - 用于通过输入自然语言执行智能选股并获取股票列表
- 📚参数说明
  
  - `question`: `str`，表示自然语句
  - `set_attr`: `str`，表示用于存储股票列表结果的`context`对象的属性名，默认为'iwencai_securities'
  - `version`: `Optional[str]`，表示版本，'stable'为稳定版，'online'为正式版。若希望与问财官网保持一致，请使用'online'。默认为`None`，表示稳定版
- 🔢返回值说明
  
  - `None`: 函数无直接返回值，选股结果会保存在由`set_attr`参数指定的`context`对象的属性中，默认为`context.iwencai_securities`，选股结果为`list[str]`，为股票列表。
- ❗注意事项
  
  - 该函数必须在`init`初始化函数中调用。
  - 该函数会在每个交易日自动执行选股，并将结果保存至`context`对象中。
  - 该函数有调用次数限制，每15分钟内限制调用5000次。
- 📝示例：
  
  - 调用
    ```python
    def init(context):
        # 选出非ST且市值大于100亿的股票
        get_iwencai('非ST，市值大于100亿')
    
    def handle_bar(context, bar_dict):
        # 打印前一日收盘后的选股结果
        log.info(context.iwencai_securities)
    ```
  - 返回值
    ```python
    # 假设选出的股票如下
    ['000001.SZ', '600519.SH']
    ```
- 💥特殊用法
  当前已经支持在研究环境调用`get_iwencai`
  
  - 调用
    
    ```python
    # 研究环境中使用get_iwencai
    get_iwencai = get_open_api('public').get_iwencai
    stk_pool = get_iwencai('净利润增长大于20%,股价位于20日均线上方','20230701','20230801',version='stable')
    ```
  - 返回值
    
    ```python
    {'20230710': ['301292.SZ', '300780.SZ', '301192.SZ', '301016.SZ', '301398.SZ'], '20230707': ['300817.SZ', '301192.SZ', '300657.SZ', '301488.SZ', '301141.SZ'], '20230706': ['301202.SZ', '920505.BJ', '300128.SZ', '300127.SZ', '301141.SZ'], '20230705': ['301488.SZ', '920533.BJ', '301007.SZ', '301255.SZ', '301221.SZ'], '20230704': ['920204.BJ', '300827.SZ', '300254.SZ', '300282.SZ', '688663.SH'], '20230703': ['688582.SH', '300769.SZ', '300503.SZ', '688609.SH', '300412.SZ'], '20230630': ['688429.SH', '920378.BJ', '920663.BJ', '920221.BJ', '300780.SZ']}
    ```

### 问财接口是否支持本地接口调用？

不支持。supermind 中只有极少的数据支持本地接口调用，详见：[https://quant.10jqka.com.cn/view/help/3](https://quant.10jqka.com.cn/view/help/3)

### 市面ZUI全！一文讲透问财语句深度使用技巧（含50个案例）

[https://quant.10jqka.com.cn/view/article/2183](https://quant.10jqka.com.cn/view/article/2183)


## 组合优化器

### 构造组合优化

#### 初始化组合优化器

* 👑调用方法：
  
  ```python
  OptimizePort(stock_return, trade_date, return_expect, opt_focus='UI', benchmark='000905.SH', loss_aversion=0.5, cost=0.003, period='d', holds=0, long_short='long-only')
  ```
* 📚参数说明：
  
  * stock\_return：股票预期收益率，支持pd.Series或dict格式
    * pd.Series格式：index表示股票代码，values为预期收益率
    * dict格式：key表示股票代码，value为预期收益率
  * trade\_date：str，表示优化日期，例如'2022-12-14'
  * return\_expect： bool，预期收益计算方式
    * `return_expect = True`：采用个股历史平均值作为预期收益率
    * `return_expect = False`：按stock\_return作为预期收益率
  * opt\_focus：str,优化方式
    * `opt_focus='UI'`：效用最大化，默认
    * `opt_focus='IR'`：为最大信息比率
    * `opt_focus='MVO'`：为夏普比率
  * benchmark：str，基准指数，目前仅支持'000905.SH' (默认)，'000300.SH' 、 '000016.SH' 、'000906.SH'、'000010.SH' 、'000001.SH'
  * loss\_aversion：float，风险厌恶系数，默认为0.5
  * cost：float，交易成本，默认为0.003
  * period：str，调仓周期
    * `period='d'`：按天调仓
    * `period='w'`：按周调仓
    * `period='m'`：按月调仓
  * holds:当前持仓权重，支持pd.Series或dict格式
    * pd.Series格式：index表示股票代码，values为持仓权重
    * dict格式：key表示股票代码，value为持仓权重
    * int(0)：代表没有持仓(默认)
  * long_short：str，表示是否做空
    * `long_short='long-only'`：只能做多
    * `long_short='short-long'`：可以做多也可以做空
* 🔧作用：
  
  * 用来构造组合优化器
* ❗注意事项：
  
  * 该函数在策略框架函数之外执行
  * 性能分析结果再日志的最后部分显示
  * func\_list参数如果不填写，则默认为分析所有函数

#### 添加约束条件

- 👑调用方法：

```python
opt.add_constraint(con_type, args=())
```

- 📚参数说明：
  
  * stock\_return：str，约束类型
    
    * `stock_return='turnover_target'`：换手率约束
    * `stock_return='tracking_error'`：跟踪误差约束
    * `stock_return='port_risk'`：组合风险约束
    * `stock_return='stock_weight'`：个股权重约束
    * `stock_return='special_style'`：风格因子暴露度约束
    * `stock_return='industry'`：行业因子暴露度约束
  * args：不同约束类型传的参数不同
    
    * `stock_return='turnover_target'`：输入tuple(换手率上限，换手率下限)，默认为(0.0, 100.0)，100表示100%
    * `stock_return='tracking_error'`：输入tuple(跟踪误差下限，跟踪误差上限)，默认为(0.0, inf)
    * `stock_return='port_risk'`：输入tuple(组合风险下限，组合风险上限)。默认为(0.0, inf)
    * `stock_return='stock_weight'`：输入pd.Series或dict. key为股票代码，value为权重
    * `stock_return='special_style'`：输入dict，且key为因子名，value为list: [暴露度下限，暴露度上限]，该约束没有默认值，必须传参数，例如{'size':[0,0.5]}
    * `stock_return='industry'`：输入str或dict. 当为str且为'industry_neutralize'时所有行业下限为0，上限为0.1;否则key为行业代码，value为list:[暴露度下限，暴露度上限]，该约束没有默认值，必须传参数，例如{'ci4000000':[0.0, 0.5]}

🔧作用：

* 通过约束类型来添加约束条件

❗注意事项：

* 可同时添加多种约束

#### 组合优化器应用示例

```python
# 从中证500中随机选取50股票，模拟中证500走势，周频调仓
# Stratified Sampling 方法优点：
#1.当指数标的过多时，完全复制的资金量要求较高
#2.指数标的中很多股票的成交量过小，交易成本较高，甚至无法完全复制中证500标的成分股权重
import random
def init(context):
    # 设置基准收益：中证500指数
    set_benchmark('000905.SH')
    # 打印日志
    log.info('策略开始运行,初始化函数全局只运行一次')
    # 设置股票每笔交易的手续费为万分之二(手续费在买卖成交后扣除,不包括税费,税费在卖出成交后扣除)
    set_commission(PerShare(type='stock',cost=0.0002))
    # 设置股票交易滑点0.5%,表示买入价为实际价格乘1.005,卖出价为实际价格乘0.995
    set_slippage(PriceSlippage(0.002))
    # 设置日级最大成交比例25%,分钟级最大成交比例50%
    # 日频运行时，下单数量超过当天真实成交量25%,则全部不成交
    # 分钟频运行时，下单数量超过当前分钟真实成交量50%,则全部不成交
    set_volume_limit(0.25,0.5)
    # 从中证500中随机选取50股票
    stocks=random.sample(list(get_index_stocks('000905.SH','2017-12-21')), 50)
    #构建股票列表，形式为dict，以便后续使用组合优化器
    context.security={ia:0 for ia in stocks} 
    #构建初始股票权重
    context.hold={ia:0 for ia in stocks}
    #股票权重限制
    context.weight={ia :[0.0,100.0] for ia in stocks}
    #周频调仓
    run_weekly(func=optmize, date_rule=1, reference_security='000001.SZ')

def optmize(context, bar_dict):
    time=get_datetime().strftime('%Y%m%d')
    #构造组合优化器，优化目标设置为最大化效用，使用历史收益率作为预期收益率
    opt=OptimizePort(context.security, '2017-12-21', True, opt_focus='UI', benchmark='000905.SH', period='w', holds=context.hold, long_short='long-only')
    opt.add_constraint('stock_weight',context.weight)
    #添加跟踪误差约束
    opt.add_constraint('tracking_error',(-0.02,0.02))
    # opt.add_constraint('industry','industry_neutralize')
    #使用组合优化器进行求解
    stock_weight = opt.optimized_weight()
    #根据组合优化器结果进行权重调整
    for ia in stock_weight.keys():
        order_target_percent(ia, stock_weight[ia]/100)
```
