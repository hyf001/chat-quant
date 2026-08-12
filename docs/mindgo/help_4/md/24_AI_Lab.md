# AI Lab

## 使用前必读

SuperMind即将分阶段推出一系列AI赋能功能，涵盖因子公式生成、策略代码编写等。为助力每位用户的投研工作，我们将提供每周50Credits的免费额度。对于有更高阶需求的用户，我们也将推出多种付费套餐以供选择。诚邀您体验，尽享AI时代带来的投研便利。

![26badc6fd14ed52551ae6f35c380a128.png](http://u.thsi.cn/imgsrc/pefile/26badc6fd14ed52551ae6f35c380a128.png)

## 研报复现

### 1.系统简介

这是一个面向量化因子研究的 Agent 系统，帮助您从研报中抽取因子逻辑并进行复现，构建因子表达式（语法详见[AI Lab](https://quant.10jqka.com.cn/view/help/24#1-%E5%9F%BA%E6%9C%AC%E8%A7%84%E5%88%99)）后进行回测。

### 2.快速开始

#### 2.1 上传研报并设置回测参数

![9eea851921566f0efc1283bfe6423c7c.png](http://u.thsi.cn/imgsrc/pefile/9eea851921566f0efc1283bfe6423c7c.png)

因子回测目前采用的收益率是次一日开盘价到再次一日开盘价的收益率。
回测参数如下（可自由变更）：

- 回测股票池，如000300.SH - 沪深300，000985.CSI - 中证全指，可参照[常用股票型指数](https://quant.10jqka.com.cn/view/dataplatform/detail/295)
- 开始时间
- 结束时间

#### 2.2 查看回测报告

![ad6a0610cb85af0116d26c159ce8263d.png](http://u.thsi.cn/imgsrc/pefile/ad6a0610cb85af0116d26c159ce8263d.png)

点击“查看”即可查看从每份研报中抽取出来的因子列表，如下

![244d1f14a9b8112a2b8afa739437b768.png](http://u.thsi.cn/imgsrc/pefile/244d1f14a9b8112a2b8afa739437b768.png)

点击因子名称可以查看详细每个因子的详细报告

![97cccf067fe95c19cfd9eb3679418615.png](http://u.thsi.cn/imgsrc/pefile/97cccf067fe95c19cfd9eb3679418615.png)

## 量化实验室

### 基础操作

**当前系统运行依赖python3.8/3.11环境，如遇打开页面失败的情况，请关闭研究环境后重试（关闭方法见[研究环境/实盘](https://quant.10jqka.com.cn/view/help/14#%E7%A0%94%E7%A9%B6%E7%8E%AF%E5%A2%83%E5%A6%82%E4%BD%95%E5%85%B3%E9%97%AD-)）**

#### 1. 新建或打开项目

**新建项目**

![0e97a327d1aac4eb7627456dbecaf471.png](http://u.thsi.cn/imgsrc/pefile/0e97a327d1aac4eb7627456dbecaf471.png)

**打开旧项目**
![332fe9482a243aca7bf5fe9e8807e091.png](http://u.thsi.cn/imgsrc/pefile/332fe9482a243aca7bf5fe9e8807e091.png)

量化实验室与研究环境共用文件系统，可以打开研究环境中文件夹，也可以在研究环境中下载实验结果

#### 2. 新建会话

![5766c6c9bbec2ca57705e23f921e7159.png](http://u.thsi.cn/imgsrc/pefile/5766c6c9bbec2ca57705e23f921e7159.png)

#### 3. 查看目录文件

![c275a71c631b89a0a6260480f3d8ef57.png](http://u.thsi.cn/imgsrc/pefile/c275a71c631b89a0a6260480f3d8ef57.png)

前端有时文件刷新会延迟，可以手动刷新

![9655998ee41878662e2d75ca8069bc37.png](http://u.thsi.cn/imgsrc/pefile/9655998ee41878662e2d75ca8069bc37.png)

#### 4. 查看变更

![084a3dd62174708b98ceb6e8b4f9e186.png](http://u.thsi.cn/imgsrc/pefile/084a3dd62174708b98ceb6e8b4f9e186.png)

---

### 因子研究

#### 1. 简介

因子研究Agent是一个面向量化因子研究的多 Agent 系统，帮助您把研究想法或已有公式转化为可执行、可回测的因子结果（因子表达式语法详见[AI Lab](https://quant.10jqka.com.cn/view/help/24#1-%E5%9F%BA%E6%9C%AC%E8%A7%84%E5%88%99)）。

系统主要有两个使用入口：

- `因子研究 Agent`：适合从研究想法出发，先形成假设，再生成因子。
- `因子复现 Agent`：适合已经有公式、伪代码或明确逻辑，直接翻译成可执行表达式。

核心流程通常是：研究想法或公式输入 → 因子生成/修改 → 回测

#### 2. 快速开始

##### 2.1 选择合适的Agent

![a5480ca5f9660328fed47bf059ffd6c3.png](http://u.thsi.cn/imgsrc/pefile/a5480ca5f9660328fed47bf059ffd6c3.png)

因子研究目前有2个Agent可用

###### 2.1.1 因子研究 Agent

适合以下场景：

- “我想研究基于量价关系的因子”
- “帮我设计一个结合资金流和波动率的选股因子”

它的特点是：

- 先理解研究方向，再组织成可测试的假设。
- 基于假设生成一批因子。
- 因子生成后会继续推动校验、修复、导出和回测确认。

工作流程：

- 第一步、生成因子假设`design.md`文件，主要包括构建因子的理论逻辑等
- 第二步、生成因子公式`factors.json`和`factors.md`文件，用户可自行审阅
- 第三步、回测，生成`run_*`文件夹，其中`summary_table.md`为所有因子回测结果概况，`detail_output.md`为每个因子的详细报告，`result.json`保存了回测的相关参数和结果

###### 2.1.2 因子复现 Agent

适合以下场景：

- “把过去20日振幅和成交量相关性作为因子进行回测”
- “我有一个因子公式，帮我落地成可执行语法”
- “把当前某个因子的滚动窗口从 10 改到 20”

它的特点是：

- 不要求先给研究假设。
- 更偏向公式翻译、表达式复现、因子局部修改。
- 同样会在修改后推动校验、修复、导出和回测确认。

工作流程：

- 第一步、生成因子公式`factors.json`和`factors.md`文件，用户可自行审阅
- 第二步、回测，生成`run_*`文件夹，其中`summary_table.md`为所有因子回测结果概况，`detail_output.md`为每个因子的详细报告，`result.json`保存了回测的相关参数和结果

##### 2.2 向系统描述你的需求

###### 2.2.1 研究型任务

**初始设计**

```text
我想研究基于量价关系的因子
```

**修改方向**

```text
我想把研究重点改为资金流向
```

**调整时间窗口**

```text
把时间窗口从短期改为中期，大约20天左右
```

**增加约束条件**

```text
希望因子不要太偏交易型，增加一些基本面因素
```

**重新开始**

```text
放弃当前方向，重新开始
```

###### 2.2.2 复现型任务

**翻译公式**

```text
把 TS_Corr(high-low, volume, 20) 翻译成 expression
```

**自然语言转表达式**

```text
我想表达过去10日收益率和换手率变化率的滚动相关性
```

**追加因子**

```text
再追加一个过去20日主力资金净流入强度因子
```

**修改已有因子**

```text
把第一个因子的窗口期从10天改为20天
```

###### 2.2.3 删除因子

**按名称删除**

```text
删除 Volatility_Factor_10D
```

**删除多个**

```text
删除第一个和第三个因子
```

###### 2.2.4 回测

因子回测目前采用的收益率是次一日开盘价到再次一日开盘价的收益率。
回测参数如下（可自由变更）：

- 回测股票池，如000300.SH - 沪深300，000985.CSI - 中证全指，默认为000300.SH，可参照[常用股票型指数](https://quant.10jqka.com.cn/view/dataplatform/detail/295)
- 开始时间，默认20250101
- 结束时间，默认20260101

**使用默认参数**

```text
使用默认值,开始回测
```

**指定参数**

```text
用中证500，时间从2022年开始
```

**使用默认参数**

```text
使用默认值,开始回测
```

**指定参数**

```text
用中证500，时间从2022年开始
```

##### 2.4 查看因子回测结果

每一轮回测完成之后，会在当前目录下生成`run_*`文件夹，里面是回测结果，包含：

* `summary_table.md`：所有因子的汇总报告
* `detail_output.md`：每个因子的详细回测报告
* `result.json`：原始回测计算结果
* `evaluate.log`：运行日志，方便排查问题

用户可以打开相应文件，查看具体内容。

![03b3982d1ab630e693e9b67c0b4e3b78.png](http://u.thsi.cn/imgsrc/pefile/03b3982d1ab630e693e9b67c0b4e3b78.png)

---

### 量化研究

#### 1. 简介

本系统加入了如下SKILL，支持生成策略源码并进行回测

* `ths-strategy-generator`: 生成同花顺指标公式策略，具体参照[指标策略 - SuperMind](https://quant.10jqka.com.cn/view/backtest/indexStrategy?stock_market=futures)功能。同花顺指标公式策略主要是对单标的进行回测，局限性较大。
* `quant-developer`：生成python策略。python策略自由度更高，支持包含选股、择时等逻辑。
* `supermind-cli`：与量化平台其他功能进行交互，例如推送策略到个人策略仓库、添加自选股等。

使用Agent时，需要说明生成python策略还是公式策略，否则agent可能无法正确识别您的意图。也可以键入`/`后显式选择SKILL，来确保生成正确的代码。

#### 2. 快速开始

##### 2.1 选择"量化助手"或“计划模式”Agent

![277e9994d5f9bcd3fff37a73e598e59f.png](http://u.thsi.cn/imgsrc/pefile/277e9994d5f9bcd3fff37a73e598e59f.png)

如果选择“计划模式”，Agent会输出详细开发方案，用户可以确认之后再进行开发。“计划模式”下的方案确认之后，需要手动切换到“量化助手”进行下一步代码生成。

##### 2.2 场景A：策略代码生成

###### 2.2.1 描述你的策略逻辑

使用自然语言尽可能清晰地描述策略逻辑，也可以通过与Agent的交流逐步完善策略逻辑。策略逻辑的关键要素包含：选股条件、开仓条件、平仓条件、回测起止时间、回测运算频率等

**例：python策略**

```
#### 1. 选股条件 (Universe)

* **标的范围**：沪深300指数成分股（或者你也可以简单设定为“全A股”剔除ST股和停牌股）。
* **资金分配**：采用等权重分配，即平均分配资金给所有触发买入信号的股票。

#### 2. 开仓条件 (Entry Signal)

**当股票的短期趋势强于长期趋势时，视为上涨行情确立，执行买入：**

* **技术指标**：计算5日收盘价简单移动平均线（MA5）和20日收盘价简单移动平均线（MA20）。
* **买入触发**：当 MA5 从下方向上穿过 MA20（即发生“金叉”），且当前账户中没有持有该股票时。
* **操作**：以当日收盘价（或次日开盘价）买入目标股票。

#### 3. 平仓条件 (Exit Signal)

**当股票的短期趋势弱于长期趋势时，视为上涨行情结束，执行卖出：**

* **卖出触发**：当 MA5 从上方向下穿过 MA20（即发生“死叉”），且当前账户中持有该股票时。
* **操作**：以当日收盘价（或次日开盘价）清仓卖出该股票。
* **兜底风控（可选）**：为了防止极端暴跌，可以额外增加一个硬性止损条件，例如“个股从最高点回撤超过10%无条件平仓”。
```

**例：公式策略**

```
写一个期货策略，当天如果涨幅向上突破近几日ATR的N倍，就做多；做空同理。
开仓后设置1%止损，以及从最高点回撤1.5%止盈。
使用5分钟频率计算，回测 RU8888 2023-2025年数据
```

```
写一个股票策略，当天如果涨幅向上突破近几日ATR的N倍，就开仓买入。
开仓后设置1%止损，以及从最高点回撤1.5%止盈。
使用5分钟频率计算，回测 同花顺 2023-2025年数据
```

Agent会根据用户提供的策略逻辑生成策略源码，并执行回测，策略源码和回测结果会保存到文件`funcat_backtest_*.md`（公式策略回测结果）或`strategy_backtest_*.md`（python策略回测结果）中。
如果对回测结果不满意，可以在后续的多轮对话中描述你的修改需求，Agent会根据需求对源码进行修改。
Agent生成的代码可以存在错误，请注意甄别！

###### 2.2.2 查看回测结果

打开文件`funcat_backtest_*.md`（公式策略回测结果）或`strategy_backtest_*.md`（python策略回测结果），可查看回测报告

![4d398c673ab15a0f02f983c8909ced38.png](http://u.thsi.cn/imgsrc/pefile/4d398c673ab15a0f02f983c8909ced38.png)

###### 2.2.3 调整回测参数重新回测

可以要求Agent修改回测参数重新进行回测，可调整的回测参数如：回测区间、回测标的、运行频率、手续率、滑点等。重新回测之后会生成新的回测结果文件

##### 2.3 场景B：通用代码生成

除策略代码外，量化实验室也支持生成通用python代码并执行，例如可以做数据处理、分析、可视化输出等。
![f18459103353477ba0aa43cdbe3c485f.png](http://u.thsi.cn/imgsrc/pefile/f18459103353477ba0aa43cdbe3c485f.png)

##### 2.4 场景C：与量化平台其他功能进行交互

`supermind-cli` 是Agent与SuperMind 量化平台进行交互的skill，可以让用户快速完成策略管理、回测与自选板块管理等。

###### 2.4.1 管理个人策略仓库

将AI 生成的策略同步至云端仓库，或拉取其他策略的代码。推送后可以在“我的策略”-“策略研究”中看到这个策略。
**示例：**“把刚才写好的双均线策略推送到策略仓库里，命名为神奇均线”、“帮我看看云端现在有哪些策略”
![aef6e1506b3298ad30f8a5f486a5cc63.png](http://u.thsi.cn/imgsrc/pefile/aef6e1506b3298ad30f8a5f486a5cc63.png)

###### 2.4.2 异步回测

推送完成后可以发起异步回测任务。回测完成之后可在“我的策略”-“策略研究”-“回测列表”中查看回测详情。

**示例：**“用过去两年的数据跑一下这个策略的回测，初始资金500W”

###### 2.4.3 维护自选板块

新增、更新或查询自选板块，添加后同花顺行情客户端可见。

**示例：**“帮我把这几只白酒股加到自选板块里”、“查一下我现在的自选板块都有哪些股票”

---

### 策略助手

“把问题说清楚，往往就已经解决了一半。”

策略助手旨在帮助用户把零散、模糊、尚未定型的策略想法，整理成一份可确认、可回测、可继续实现的策略逻辑文档。在真正进入回测、开发或实现之前，它先帮助你把策略目标、规则边界和关键条件说清楚。

#### 1. 功能简介

策略助手用于把尚未成型的策略想法整理成一份结构清晰的策略逻辑文档。最终通常会沉淀出以下几部分：

- 可确认的策略规则
- 可回测的策略逻辑
- 可继续修改和迭代的 Markdown 最终稿

如果你现在只有一个大致方向，或者已经有策略雏形但还缺少完整规则、过滤条件和退出逻辑，这个助手会更合适。

#### 2. 适合解决什么问题

策略助手更适合处理“规则如何成立、条件如何闭环、策略如何落地”这一类问题。它内置了一组面向策略研究的金融量化专家 skills，会从趋势跟踪、板块与主题轮动、形态确认、过滤条件、退出逻辑、回测配置和风险约束等角度，帮助你判断一套策略还缺什么、该先确认什么。

它更擅长回答的是：

- 一套策略应该由哪些规则组成
- 这些规则之间如何衔接
- 哪些条件必须明确，哪些可以作为默认补齐
- 哪些地方容易失真、过宽、过窄或难以回测

如果你的重点是“把一个想法整理成完整策略逻辑，并为后续回测或实现做准备”，更适合使用策略助手。
如果你的重点是“把某个指标、公式或信号定义清楚”，更适合使用指标助手。

#### 3. 使用流程

##### 第一步：选择“策略助手”

先在助手列表中切换到“策略助手”，再输入你的自然语言需求。

![965f38ba7d8cc7bed8e3d8c312b4ef41.png](http://u.thsi.cn/imgsrc/pefile/965f38ba7d8cc7bed8e3d8c312b4ef41.png)

##### 第二步：先把你的想法说出来

你不需要一开始就写得很专业，可以先用最接近真实想法的话描述，例如：

- 我想做一个热门个股趋势跟踪策略
- 我想跟踪强势股，但不想追高
- 我希望策略适合高换手热门股
- 我想先看趋势确认，再决定什么时候退出

##### 第三步：按问题卡片一步步补齐规则

如果你的描述还不完整，策略助手会继续追问关键问题。你只需要边看边选，逐步确认就可以。

这时候重点通常包括：

- 想做什么类型的策略
- 主要做什么标的
- 关注什么入场方式
- 更偏向什么退出方式
- 有没有特别在意的风险控制要求

![4aeea5626103655bcca36f86863d7324.png](http://u.thsi.cn/imgsrc/pefile/4aeea5626103655bcca36f86863d7324.png)

![24ee60b3f7410309d0c78c17015cb4f0.png](http://u.thsi.cn/imgsrc/pefile/24ee60b3f7410309d0c78c17015cb4f0.png)

##### 第四步：查看建议，决定是否调整

当规则整理得差不多后，先看系统给出的建议和优化项表格，再决定是否采纳。

如果建议符合你的想法，就继续；如果不符合，可以继续补要求或修改规则。

![fd920364d546fb68c1683ed7f8041465.png](http://u.thsi.cn/imgsrc/pefile/fd920364d546fb68c1683ed7f8041465.png)

##### 第五步：确认定稿

当你认可当前方案后，点击确认，系统会生成最终策略逻辑文件。

##### 第六步：查看最终输出文件

最终会生成 Markdown 策略文档，并写入：

`strategy_outputs/final_strategy_logic.md`

这个文件通常会包含：

- 策略目标
- 标的范围
- 触发逻辑
- 过滤条件
- 退出逻辑
- 回测配置
- 默认补齐项
- 风险与适用边界
- 公式附录

![253148d0a5b05f2970f439a2a00d2758.png](http://u.thsi.cn/imgsrc/pefile/253148d0a5b05f2970f439a2a00d2758.png)

#### 4. 如何写需求

你可以尽量说清楚下面几类信息：

- 你想做什么类型的策略
  - 例如趋势跟踪、突破跟随、回踩再起、板块轮动
- 你主要做什么标的
  - 例如个股、板块、主题、宽基指数、ETF
- 你更重视哪种入场方式
  - 例如均线确认、前高突破、放量确认、右侧跟随
- 你更偏向什么退出方式
  - 例如趋势走弱退出、固定止损、分批退出、移动止盈

如果你一开始还没想清楚，也没关系。
先把核心需求说出来就可以，后面在选择问题卡片时，想到什么再补什么。

#### 5. 结果产出说明

策略助手的最终目标不是直接替你写 Python 代码，而是先形成一份**可确认、可修改、可继续开发**的策略逻辑文档。

这份文档适合后续用于：

- 回测前的规则确认
- 与同事沟通策略逻辑
- 继续补充数据字段、公式和执行细节
- 作为后续开发或策略实现的基础稿

通常更自然的做法是：把策略助手产出的 Markdown 直接当成后续实现说明，在当前对话里继续补代码、补回测配置，或进一步转成可执行策略。
如果后面希望把“规则文档”继续推进到 Python 策略或公式策略开发，也可以把这份 Markdown 作为下一轮输入继续处理；这样既能延续当前思路，也能减少重新解释上下文的成本。

#### 6. 常见使用建议

- 如果你还不确定策略细节，先说“我想做什么”，不要一开始就纠结参数。
- 如果你已经有明确方向，可以直接说：标的范围、入场条件、退出条件。
- 如果你对建议不满意，不必重来，可以在优化阶段直接补充自己的要求。
- 如果你想要的是“指标公式”，请切换到“指标助手”。

---

### 指标助手

很多时候，用户并不是一开始就知道该有怎么样的指标，而是先知道自己想解决什么行情问题。指标助手就是为这样的场景准备的：它帮助你把模糊的指标想法逐步收敛成一份可确认、可计算、可继续实现的指标逻辑文档。

#### 1. 功能简介

指标助手的核心作用，是把对指标的模糊描述整理成一份可计算、可确认、可继续落地开发的指标逻辑文档。

最终它会帮你形成：

- 指标目标和用途
- 指标分类与适用场景
- 计算公式
- 参数定义
- 买卖/提示信号规则
- 可视化规格
- SuperMind 实现指引

#### 2. 适合解决什么问题

指标助手更适合处理“指标怎么定义、公式怎么计算、信号怎么表达”这一类问题。它内置了一组面向指标研究的金融量化专家 skills，能从趋势、动量、波动率、量价、情绪、复合信号以及参数与可视化表达等角度，帮助你判断一个指标应该怎样写，才能更清楚、更稳定、更方便实现。

它更擅长聚焦在指标层本身，例如：

- 这个指标的核心计算对象是什么
- 公式应该怎样写才清楚、稳定、可实现
- 参数、阈值和信号规则该如何设定
- 这个指标更适合作为主信号、过滤器还是辅助确认

如果你的重点是“把某个指标或信号公式说清楚，并为后续实现做准备”，更适合使用指标助手。
如果你的重点是“把选股、买入、卖出、回测和风险控制连成一套完整策略”，更适合使用策略助手。

#### 3. 使用流程

##### 第一步：选择“指标助手”

先在助手列表中切换到“指标助手”，再输入你的指标需求。

![ac24633acacd023198218ba68836c23c.png](http://u.thsi.cn/imgsrc/pefile/ac24633acacd023198218ba68836c23c.png)

##### 第二步：先把你的指标想法说出来

你可以直接说出最真实的需求，例如：

- 我想要一个震荡行情高抛低吸指标
- 我希望这个指标适用于个股
- 我想用布林带和 RSI 做反转识别
- 我想加一层趋势过滤，避免在趋势行情里逆势抄底

##### 第三步：按问题卡片确认核心框架

如果你的描述还不完整，指标助手会继续追问关键问题。你只需要边看边选，逐步确认即可。

通常会确认：

- 指标主要解决什么问题
- 指标用于什么标的
- 更偏向哪类指标框架
- 是否需要过滤器或确认条件

![f269b5e369cc21c316521354dcbf3ad0.png](http://u.thsi.cn/imgsrc/pefile/f269b5e369cc21c316521354dcbf3ad0.png)

![ba58d5ab68acc74897c4e854db97f641.png](http://u.thsi.cn/imgsrc/pefile/ba58d5ab68acc74897c4e854db97f641.png)

##### 第四步：查看当前方案并决定要不要调整

当关键问题确认完后，先看当前指标方案，再判断：

- 当前方案是否符合预期
- 是否需要改参数
- 是否要增加过滤条件
- 是否还要补信号规则

![30042394aabf742b88462a08dd273eae.png](http://u.thsi.cn/imgsrc/pefile/30042394aabf742b88462a08dd273eae.png)

##### 第五步：确认定稿

当你确认当前版本后，系统会生成最终 Markdown 文件，并同步写入：

`strategy_outputs/final_indicator_logic.md`

##### 第六步：查看最终输出文件

最终文档一般会包含：

- 指标目标
- 指标名称与分类
- 计算公式
- 参数定义
- 信号规则
- 可视化规格
- 适用周期与品种
- SuperMind 实现指引
- 使用说明与注意事项
- 公式附录

![778f50c9f715f78a54535139de77e261.png](http://u.thsi.cn/imgsrc/pefile/778f50c9f715f78a54535139de77e261.png)

#### 4. 如何写需求

你可以尽量说明以下几点：

- 指标是做什么用的
  - 例如趋势判断、震荡高抛低吸、超买超卖提示、趋势过滤
- 指标主要用于什么标的
  - 例如个股、指数 ETF、两者都适用
- 你更偏向哪类指标体系
  - 例如布林带、RSI、KDJ、CCI、MACD、ADX、多信号复合
- 你是否需要过滤器
  - 例如趋势过滤、量能过滤、波动率过滤

如果你一开始说不清楚，也没关系。
先把主要想法说出来，后面在选择问题卡片时，想到什么再补什么。

#### 5. 结果产出说明

指标助手最终交付的不是一句“这个指标可以用”，而是一份正式的指标逻辑文档。
这份文档适合后续用于：

- 指标实现前的逻辑确认
- 指标公式开发
- 与他人沟通指标定义
- 继续补参数、补信号、补可视化要求

更常见的用法是：在当前对话中继续把这份 Markdown 往下推进，转换成支持 SuperMind 的股票指标公式策略。
生成出股票指标公式策略代码之后，你既可以继续在当前对话里研究参数、阈值和信号规则，也可以把代码复制到 SuperMind 的“我的策略” - “指标策略”中继续研究和使用。

#### 6. 常见使用建议

- 如果你只知道“想解决什么行情问题”，直接说场景就可以。
- 如果你已经有指标组合想法，可以直接说“我想用什么指标 + 做什么用途”。
- 如果你不确定参数，先让系统给默认值，再决定是否继续微调。
- 如果你想整理的是完整交易策略，而不只是指标，请切换到“策略助手”。

---

## 表达式写法说明

### 1 基本规则

- 表达式使用严格函数式语法。
- 不使用中缀运算，例如 `a + b`、`x / y`。
- 要写成 `Add(X, Y)`、`Div(X, Y)` 这类形式。
- 表达式里至少要包含一个合法 operand。

---

### 2 Constant

可直接写入表达式的浮点数，例如：`1.5`、`0.5`、`1e-8`。

---

### 3 Bar

Bar 表示窗口长度或位移长度，例如：`2`、`10`。正值表示向过去回看，负值表示向未来看；预测型因子通常只使用正数。

---

### 4. Operators

#### 4.1 Unary Operators

- `Neg(X)`：对序列 X 逐元素取相反数。
- `Abs(X)`：对序列 X 逐元素取绝对值。
- `Inv(X)`：对序列 X 逐元素取倒数。
- `Sign(X)`：对序列 X 逐元素取符号。
- `Sqrt(X)`：对序列 X 逐元素开平方。
- `UnsignedSqrt(X)`：对序列 X 逐元素先取绝对值，再开平方。
- `SignedSqrt(X)`：对序列 X 逐元素先取绝对值开平方，再保留原符号。
- `Square(X)`：对序列 X 逐元素平方。
- `Curt(X)`：对序列 X 逐元素取立方根。
- `UnsignedCurt(X)`：对序列 X 逐元素先取绝对值，再取立方根。
- `SignedCurt(X)`：对序列 X 逐元素先取绝对值立方根，再保留原符号。
- `Cube(X)`：对序列 X 逐元素立方。
- `Log(X)`：对序列 X 逐元素取自然对数。
- `UnsignedLog(X)`：对序列 X 逐元素先取绝对值，再取自然对数。
- `SignedLog(X)`：对序列 X 逐元素先取绝对值自然对数，再保留原符号。
- `Exp(X)`：对序列 X 逐元素取指数。
- `TanH(X)`：对序列 X 逐元素计算双曲正切。
- `Sigmoid(X)`：对序列 X 逐元素计算 sigmoid。
- `ReLU(X)`：对序列 X 逐元素计算 ReLU。
- `GeLU(X)`：对序列 X 逐元素计算 GeLU。
- `UnaryCount(X)`：在横截面维度上统计 X 的非空元素个数。
- `UnarySum(X)`：在横截面维度上对 X 的所有元素求和。
- `UnaryProd(X)`：在横截面维度上对 X 的所有元素求积。
- `UnaryMean(X)`：在横截面维度上计算 X 的均值。
- `UnaryMed(X)`：在横截面维度上计算 X 的中位数。
- `UnaryMad(X)`：在横截面维度上计算 X 的中位绝对偏差。
- `UnaryVar(X)`：在横截面维度上计算 X 的方差。
- `UnaryStd(X)`：在横截面维度上计算 X 的标准差。
- `UnaryIncv(X)`：在横截面维度上计算 X 的逆变异系数。
- `UnarySkew(X)`：在横截面维度上计算 X 的偏度。
- `UnaryKurt(X)`：在横截面维度上计算 X 的峰度。
- `UnaryRank(X)`：在横截面维度上对 X 做升序排名。
- `UnaryDescendRank(X)`：在横截面维度上对 X 做降序排名。
- `UnaryMax(X)`：在横截面维度上取 X 的最大值。
- `UnaryMin(X)`：在横截面维度上取 X 的最小值。
- `UnaryCentral(X)`：在横截面维度上对 X 做去均值中心化。
- `UnaryZScoreNorm(X)`：在横截面维度上对 X 做 Z-score 标准化。
- `UnaryL1Norm(X)`：在横截面维度上对 X 做 L1 归一化。
- `UnaryL2Norm(X)`：在横截面维度上对 X 做 L2 归一化。
- `UnaryMinMaxNorm(X)`：在横截面维度上对 X 做 Min-Max 归一化。
- `UnarySoftmax(X)`：在横截面维度上对 X 做 Softmax 变换。

#### 4.2 Binary Operators

- `Add(X, Y)`：对 X 和 Y 逐元素相加。
- `Sub(X, Y)`：对 X 和 Y 逐元素相减，计算 X 减 Y。
- `Mul(X, Y)`：对 X 和 Y 逐元素相乘。
- `Div(X, Y)`：对 X 和 Y 逐元素相除，计算 X 除以 Y。
- `Pow(X, Y)`：对 X 和 Y 逐元素做幂运算，计算 X 的 Y 次幂。
- `UnsignedPow(X, Y)`：对 X 逐元素先取绝对值，再做 Y 次幂运算。
- `SignedPow(X, Y)`：对 X 逐元素先取绝对值做 Y 次幂，再乘回原始符号。
- `BinaryLog(X, Y)`：对 X 逐元素以 Y 为底取对数。
- `UnsignedBinaryLog(X, Y)`：对 X 和 Y 逐元素先取绝对值，再以 `Abs(Y)` 为底对 `Abs(X)` 取对数。
- `SignedBinaryLog(X, Y)`：对 X 和 Y 逐元素先按绝对值取对数，再乘回 X 的原始符号。
- `BinaryMax(X, Y)`：对 X 和 Y 逐元素比较，取两者中较大值。
- `BinaryMin(X, Y)`：对 X 和 Y 逐元素比较，取两者中较小值。
- `BinaryCov(X, Y)`：在横截面维度上计算 X 和 Y 的协方差。
- `BinaryPearson(X, Y)`：在横截面维度上计算 X 和 Y 的 Pearson 相关系数。
- `BinarySpearman(X, Y)`：在横截面维度上计算 X 和 Y 的 Spearman 秩相关系数。
- `BinaryAlpha(X, Y)`：在横截面维度上对 Y 关于 X 做线性回归，取 alpha 系数。
- `BinaryBeta(X, Y)`：在横截面维度上对 Y 关于 X 做线性回归，取 beta 系数。
- `BinaryResidual(X, Y)`：在横截面维度上对 Y 关于 X 做线性回归，取回归残差。

#### 4.3 Ternary Operators

- `PositiveCond(C, X, Y)`：若 `C` 为正，返回 `X`，否则返回 `Y`。
- `NonNegativeCond(C, X, Y)`：若 `C` 非负，返回 `X`，否则返回 `Y`。
- `NegativeCond(C, X, Y)`：若 `C` 为负，返回 `X`，否则返回 `Y`。
- `NonPositiveCond(C, X, Y)`：若 `C` 非正，返回 `X`，否则返回 `Y`。
- `FiniteCond(C, X, Y)`：若 `C` 有限，返回 `X`，否则返回 `Y`。

#### 4.4 Rolling Operators

- `RollingCount(X, Bar)`：对序列 X 在长度为 Bar 的滚动窗口内统计有效元素个数。
- `RollingSum(X, Bar)`：对序列 X 在长度为 Bar 的滚动窗口内所有元素求和。
- `RollingProd(X, Bar)`：对序列 X 在长度为 Bar 的滚动窗口内所有元素求积。
- `RollingMean(X, Bar)`：对序列 X 在长度为 Bar 的滚动窗口内计算均值。
- `RollingMed(X, Bar)`：对序列 X 在长度为 Bar 的滚动窗口内计算中位数。
- `RollingMad(X, Bar)`：对序列 X 在长度为 Bar 的滚动窗口内计算中位绝对偏差。
- `RollingVar(X, Bar)`：对序列 X 在长度为 Bar 的滚动窗口内计算方差。
- `RollingStd(X, Bar)`：对序列 X 在长度为 Bar 的滚动窗口内计算标准差。
- `RollingIncv(X, Bar)`：对序列 X 在长度为 Bar 的滚动窗口内计算逆变异系数。
- `RollingSkew(X, Bar)`：对序列 X 在长度为 Bar 的滚动窗口内计算偏度。
- `RollingKurt(X, Bar)`：对序列 X 在长度为 Bar 的滚动窗口内计算峰度。
- `RollingMax(X, Bar)`：对序列 X 在长度为 Bar 的滚动窗口内取最大值。
- `RollingMin(X, Bar)`：对序列 X 在长度为 Bar 的滚动窗口内取最小值。
- `Argmax(X, Bar)`：返回序列 X 在长度为 Bar 的滚动窗口内最大值所在位置。
- `Argmin(X, Bar)`：返回序列 X 在长度为 Bar 的滚动窗口内最小值所在位置。
- `ArgmaxArgmin(X, Bar)`：返回序列 X 在长度为 Bar 的滚动窗口内最大值位置与最小值位置之差。
- `RollingRank(X, Bar)`：对序列 X 在长度为 Bar 的滚动窗口内对当前值做升序排名。
- `RollingDescendRank(X, Bar)`：对序列 X 在长度为 Bar 的滚动窗口内对当前值做降序排名。
- `RollingCentral(X, Bar)`：对序列 X 在长度为 Bar 的滚动窗口内做去均值中心化。
- `RollingZScoreNorm(X, Bar)`：对序列 X 在长度为 Bar 的滚动窗口内做 Z-score 标准化。
- `RollingL1Norm(X, Bar)`：对序列 X 在长度为 Bar 的滚动窗口内做 L1 归一化。
- `RollingL2Norm(X, Bar)`：对序列 X 在长度为 Bar 的滚动窗口内做 L2 归一化。
- `RollingMinMaxNorm(X, Bar)`：对序列 X 在长度为 Bar 的滚动窗口内做 Min-Max 归一化。
- `RollingSoftmax(X, Bar)`：对序列 X 在长度为 Bar 的滚动窗口内做 Softmax 变换。
- `DecayLinear(X, Bar)`：对序列 X 在长度为 Bar 的滚动窗口内做线性衰减加权。
- `DescendDecayLinear(X, Bar)`：对序列 X 在长度为 Bar 的滚动窗口内做降序线性衰减加权。

#### 4.5 Shifting Operators

- `Ref(X, Bar)`：返回序列 X 向前偏移 Bar 期后的值。
- `Delta(X, Bar)`：返回序列 X 当前值与 Bar 期前数值的差。
- `Ratio(X, Bar)`：返回序列 X 当前值与 Bar 期前数值的比值。
- `DeltaRatio(X, Bar)`：返回序列 X 当前值相对 Bar 期前数值的变化率。

#### 4.6 Pair Rolling Operators

- `PairRollingCov(X, Y, Bar)`：对序列 X 和 Y 在长度为 Bar 的滚动窗口内计算协方差。
- `PairRollingPearson(X, Y, Bar)`：对序列 X 和 Y 在长度为 Bar 的滚动窗口内计算 Pearson 相关系数。
- `PairRollingSpearman(X, Y, Bar)`：对序列 X 和 Y 在长度为 Bar 的滚动窗口内计算 Spearman 秩相关系数。
- `PairRollingAlpha(X, Y, Bar)`：对序列 X 和 Y 在长度为 Bar 的滚动窗口内做线性回归，取 alpha 系数。
- `PairRollingBeta(X, Y, Bar)`：对序列 X 和 Y 在长度为 Bar 的滚动窗口内做线性回归，取 beta 系数。
- `PairRollingResidual(X, Y, Bar)`：对序列 X 和 Y 在长度为 Bar 的滚动窗口内做线性回归，取回归残差。

#### 4.7 Moving Average Operators

- `SMA(X, Constant1, Constant2)`：对序列 X 计算加权平滑移动平均，公式为 `SMA[i] = (SMA[i-1] * (Constant2 - Constant1) + X[i] * Constant1) / Constant2`。
- `EMA(X, Constant)`：对序列 X 计算指数移动平均，公式为 `EMA[i] = EMA[i-1] * (1 - Constant) + X[i] * Constant`。

### 5.  Operands

Operand 是表达式里可直接引用的数据字段。以下列表按数据类型分组整理。

#### 分析师一致预期

- `$forecast_basic_eps_current_year`：预测每股收益（本年度）
- `$forecast_basic_eps_next_year`：预测每股收益（次年）
- `$forecast_net_profit_current_year`：预测净利润（本年度）
- `$forecast_net_profit_next_year`：预测净利润（次年）
- `$forecast_operating_revenue_current_year`：预测营业收入（本年度）
- `$forecast_operating_revenue_next_year`：预测营业收入（次年）
- `$forward_pe_ratio_current_year`：预测市盈率（本年度）
- `$forward_pe_ratio_next_year`：预测市盈率（次年）
- `$number_of_rating_agencies_6m`：六个月内评级机构家数
- `$composite_rating_score_6m`：六个月内综合评级（数值）

#### 资产负债表

- `$cash`：货币资金
- `$trading_financial_assets`：交易性金融资产
- `$notes_receivable`：应收票据
- `$accounts_receivable`：应收账款
- `$advance_payments`：预付款项
- `$interest_receivable`：应收利息
- `$dividends_receivable`：应收股利
- `$other_receivables`：其他应收款
- `$inventory`：存货
- `$non_current_assets_due_within_one_year`：一年内到期的非流动资产
- `$other_current_assets`：其他流动资产
- `$special_item_current_assets`：流动资产特殊科目
- `$balancing_item_current_assets`：流动资产平衡科目
- `$total_current_assets`：流动资产合计
- `$funds_lent`：拆出资金
- `$insurance_premiums_receivable`：应收保费
- `$reinsurance_premiums_receivable`：应收分保账款
- `$reinsurance_reserves_receivable`：应收分保合同准备金
- `$available_for_sale_financial_assets`：可供出售金融资产
- `$held_to_maturity_investments`：持有至到期投资
- `$long_term_receivables`：长期应收款
- `$long_term_equity_investments`：长期股权投资
- `$investment_property`：投资性房地产
- `$fixed_assets`：固定资产
- `$construction_in_progress`：在建工程
- `$engineering_materials`：工程物资
- `$disposal_of_fixed_assets`：固定资产清理
- `$productive_biological_assets`：生产性生物资产
- `$oil_and_gas_assets`：油气资产
- `$intangible_assets`：无形资产
- `$development_expenditure`：开发支出
- `$goodwill`：商誉
- `$long_term_prepaid_expenses`：长期待摊费用
- `$deferred_tax_assets`：递延所得税资产
- `$other_non_current_assets`：其他非流动资产
- `$special_item_non_current_assets`：非流动资产特殊科目
- `$balancing_item_non_current_assets`：非流动资产平衡科目
- `$total_non_current_assets`：非流动资产合计
- `$loans_and_advances`：发放贷款和垫款
- `$cash_and_deposits_at_central_bank`：现金及存放中央银行款项
- `$interbank_deposits`：存放同业款项
- `$precious_metals`：贵金属
- `$derivative_financial_assets`：衍生金融资产
- `$buy_resale_financial_assets`：买入返售金融资产
- `$other_assets`：其他资产
- `$subrogation_receivables`：应收代位追偿款
- `$reinsurance_unearned_premium_reserve`：应收分保未到期责任准备金
- `$reinsurance_outstanding_claims_reserve`：应收分保未决赔款准备金
- `$reinsurance_life_reserve`：应收分保寿险责任准备金
- `$reinsurance_long_term_health_reserve`：应收分保长期健康险责任准备金
- `$policyholder_pledge_loans`：保户质押贷款
- `$time_deposits`：定期存款
- `$refundable_capital_deposits`：存出资本保证金
- `$independent_account_assets`：独立账户资产
- `$customer_provisions`：客户备付金
- `$margin_deposits_paid`：存出保证金
- `$trading_seat_fees`：交易席位费
- `$securities_lending_funds`：融出资金
- `$other_receivables_securities`：应收款项
- `$asset_special_account`：资产特殊科目
- `$asset_balancing_account`：资产平衡科目
- `$total_assets`：资产总计
- `$short_term_borrowings`：短期借款
- `$trading_financial_liabilities`：交易性金融负债
- `$notes_payable`：应付票据
- `$accounts_payable`：应付账款
- `$advances_from_customers`：预收账款
- `$employee_benefits_payable`：应付职工薪酬
- `$taxes_payable`：应交税费
- `$interest_payable`：应付利息
- `$dividends_payable`：应付股利
- `$other_payables`：其他应付款
- `$non_current_liabilities_due_within_one_year`：一年内到期的非流动负债
- `$other_current_liabilities`：其他流动负债
- `$special_item_current_liabilities`：流动负债特殊科目
- `$balancing_item_current_liabilities`：流动负债平衡科目
- `$total_current_liabilities`：流动负债合计
- `$borrowings_from_central_bank`：向中央银行借款
- `$interbank_borrowings`：拆入资金
- `$sale_and_repurchase_agreements`：卖出回购金融资产款
- `$customer_securities_deposits`：代理买卖证券款
- `$underwriting_proceeds_payable`：代理承销证券款
- `$deposits_and_interbank_placements`：吸收存款及同业存放
- `$insurance_contract_reserves`：保险合同准备金
- `$deferred_income_current`：流动负债递延收益
- `$short_term_bonds_payable`：应付短期债券
- `$long_term_borrowings`：长期借款
- `$bonds_payable`：应付债券
- `$long_term_payables`：长期应付款
- `$special_payables`：专项应付款
- `$provisions`：预计负债
- `$deferred_tax_liabilities`：递延所得税负债
- `$other_non_current_liabilities`：其他非流动负债
- `$special_item_non_current_liabilities`：非流动负债特殊科目
- `$balancing_item_non_current_liabilities`：非流动负债平衡科目
- `$total_non_current_liabilities`：非流动负债合计
- `$deferred_income_non_current`：非流动负债递延收益
- `$long_term_employee_benefits`：长期应付职工薪酬
- `$deposits_from_interbank`：同业及其他金融机构存放款项
- `$derivative_financial_liabilities`：衍生金融负债
- `$accepted_deposits`：吸收存款
- `$other_liabilities`：其他负债
- `$advance_premiums`：预收保费
- `$fees_and_commissions_payable`：应付手续费及佣金
- `$reinsurance_payables`：应付分保账款
- `$claims_payable`：应付赔付款
- `$policyholder_dividends_payable`：应付保单红利
- `$policyholder_deposits_and_investments`：保户储金及投资款
- `$unearned_premium_reserve`：未到期责任准备金
- `$outstanding_claims_reserve`：未决赔款准备金
- `$life_insurance_reserve`：寿险责任准备金
- `$long_term_health_insurance_reserve`：长期健康险责任准备金
- `$independent_account_liabilities`：独立账户负债
- `$pledged_borrowings`：其中：质押借款
- `$margin_deposits_received`：存入保证金
- `$short_term_financing_payable`：应付短期融资款
- `$other_payables_securities`：应付款项
- `$liability_special_account`：负债特殊科目
- `$liability_balancing_account`：负债平衡科目
- `$total_liabilities`：负债合计
- `$paid_in_capital_or_share_capital`：实收资本（或股本）
- `$capital_reserve`：资本公积金
- `$treasury_stock`：库存股
- `$special_reserves`：专项储备
- `$surplus_reserve`：盈余公积
- `$general_risk_reserve`：一般风险准备
- `$retained_earnings`：未分配利润
- `$foreign_currency_translation_differences`：外币报表折算差额
- `$special_item_equity`：股东权益特殊科目
- `$balancing_item_equity`：股东权益平衡科目
- `$equity_attributable_to_parent`：归属于母公司股东权益合计
- `$minority_interest`：少数股东权益
- `$total_equity`：股东权益合计
- `$total_share_capital`：股本总数
- `$other_consolidated_income`：其他综合收益
- `$other_equity_instruments`：其他权益工具
- `$preferred_shares`：其他权益工具：优先股
- `$perpetual_bonds`：其他权益工具：永续债
- `$trading_risk_reserve`：交易风险准备
- `$total_liabilities_and_equity`：负债和股东权益总计

#### 现金流量表

- `$cash_received_from_sales_of_goods_and_services`：销售商品、提供劳务收到的现金
- `$tax_refund_receipts`：收到的税费返还
- `$other_cash_received_from_operating_activities`：收到其他与经营活动有关的现金
- `$net_increase_in_customer_and_interbank_deposits`：客户存款和同业存放款项净增加额
- `$net_increase_in_borrowings_from_central_bank`：向中央银行借款净增加额
- `$net_increase_in_interbank_lending`：向其他金融机构拆入资金净增加额
- `$cash_received_for_interest_commissions_and_fees`：收取利息、手续费及佣金的现金
- `$cash_received_from_original_insurance_premiums`：收到原保险合同保费取得的现金
- `$net_cash_received_from_reinsurance`：收到再保业务现金净额
- `$net_increase_in_policyholder_deposits_and_investments`：保户储金及投资款净增加额
- `$net_increase_from_disposal_of_trading_financial_assets`：处置交易性金融资产净增加额
- `$net_increase_in_interbank_borrowings`：拆入资金净增加额
- `$net_increase_in_repurchase_agreements`：回购业务资金净增加额
- `$special_item_operating_cash_inflows`：经营活动现金流入差额（特殊科目）
- `$subtotal_of_cash_inflows_from_operating_activities`：经营活动现金流入小计
- `$cash_paid_for_goods_and_services`：购买商品、接受劳务支付的现金
- `$cash_paid_to_employees`：支付给职工以及为职工支付的现金
- `$tax_payments`：支付的各项税费
- `$other_cash_paid_for_operating_activities`：支付其他与经营活动有关的现金
- `$net_increase_in_loans_and_advances`：客户贷款及垫款净增加额
- `$net_increase_in_deposits_at_central_bank_and_interbank`：存放中央银行和同业款项净增加额
- `$cash_paid_for_interest_commissions_and_fees`：支付利息、手续费及佣金的现金
- `$cash_paid_for_original_insurance_claims`：支付原保险合同赔付款项的现金
- `$cash_paid_for_policyholder_dividends`：支付保单红利的现金
- `$special_item_operating_cash_outflows`：经营活动现金流出差额（特殊科目）
- `$subtotal_of_cash_outflows_from_operating_activities`：经营活动现金流出小计
- `$net_cash_flows_from_operating_activities`：经营活动产生的现金流量净额
- `$balancing_item_operating_cash_inflows`：经营活动现金流入差额（平衡科目）
- `$balancing_item_operating_cash_outflows`：经营活动现金流出差额（平衡科目）
- `$special_balancing_item_net_cash_flows_operating`：经营活动产生的现金流量净额特殊科目
- `$net_decrease_in_securities_lending`：融出资金净减少额
- `$net_cash_received_from_agent_securities_trading`：代理买卖证券收到的现金净额
- `$net_increase_in_securities_lending`：融出资金净增加额
- `$net_cash_paid_for_agent_securities_trading`：代理买卖证券支付的现金净额
- `$cash_received_from_disposal_of_investments`：收回投资收到的现金
- `$cash_received_from_investment_income`：取得投资收益收到的现金
- `$net_cash_received_from_disposal_of_fixed_assets`：处置固定资产、无形资产和其他长期资产收回的现金净额
- `$net_cash_received_from_disposal_of_subsidiaries`：处置子公司及其他营业单位收到的现金净额
- `$other_cash_received_from_investing_activities`：收到其他与投资活动有关的现金
- `$special_item_investing_cash_inflows`：投资活动现金流入特殊科目
- `$subtotal_of_cash_inflows_from_investing_activities`：投资活动现金流入小计
- `$cash_paid_for_acquisition_of_fixed_assets`：购建固定资产、无形资产和其他长期资产支付的现金
- `$cash_paid_for_investments`：投资支付的现金
- `$net_cash_paid_for_acquisition_of_subsidiaries`：取得子公司及其他营业单位支付的现金净额
- `$other_cash_paid_for_investing_activities`：支付其他与投资活动有关的现金
- `$net_increase_in_pledged_loans`：质押贷款净增加额
- `$special_item_investing_cash_outflows`：投资活动现金流出差额（特殊项目）
- `$subtotal_of_cash_outflows_from_investing_activities`：投资活动现金流出小计
- `$net_cash_flows_from_investing_activities`：投资活动产生的现金流量净额
- `$balancing_item_investing_cash_inflows`：投资活动现金流入差额（平衡科目）
- `$balancing_item_investing_cash_outflows`：投资活动现金流出差额（平衡科目）
- `$special_item_net_cash_flows_investing`：投资活动产生的现金流量净额特殊科目
- `$cash_received_from_issuance_of_equity`：吸收投资收到的现金
- `$cash_received_from_minority_shareholders`：子公司吸收少数股东投资收到的现金
- `$cash_received_from_borrowings`：取得借款收到的现金
- `$other_cash_received_from_financing_activities`：收到其他与筹资活动有关的现金
- `$proceeds_from_issuance_of_bonds`：发行债券收到的现金
- `$special_item_financing_cash_inflows`：筹资活动现金流入差额（特殊项目）
- `$subtotal_of_cash_inflows_from_financing_activities`：筹资活动现金流入小计
- `$cash_paid_for_repayment_of_debt`：偿还债务支付的现金
- `$cash_paid_for_dividends_and_interest`：分配股利、利润或偿付利息支付的现金
- `$dividends_paid_to_minority_shareholders`：子公司支付给少数股东的股利
- `$other_cash_paid_for_financing_activities`：支付其他与筹资活动有关的现金
- `$special_item_financing_cash_outflows`：筹资活动现金流出差额（特殊项目）
- `$subtotal_of_cash_outflows_from_financing_activities`：筹资活动现金流出小计
- `$net_cash_flows_from_financing_activities`：筹资活动产生的现金流量净额
- `$balancing_item_financing_cash_inflows`：筹资活动现金流入差额（平衡科目）
- `$balancing_item_financing_cash_outflows`：筹资活动现金流出差额（平衡科目）
- `$special_item_net_cash_flows_financing`：筹资活动产生的现金流量净额特殊科目
- `$effect_of_exchange_rate_changes_on_cce`：汇率变动对现金及现金等价物的影响
- `$net_increase_in_cash_and_cash_equivalents`：现金及现金等价物净增加额
- `$opening_balance_of_cash_and_cash_equivalents`：期初现金及现金等价物余额
- `$closing_balance_of_cash_and_cash_equivalents`：期末现金及现金等价物余额
- `$net_profit`：净利润
- `$asset_impairment_provision`：资产减值准备
- `$depreciation_and_amortization`：固定资产折旧、油气资产折耗、生产性生物资产折旧
- `$amortization_of_intangible_assets`：无形资产摊销
- `$amortization_of_long_term_prepaid_expenses`：长期待摊费用摊销
- `$loss_on_disposal_of_fixed_assets`：处置固定资产、无形资产和其他长期资产的损失
- `$loss_on_retirement_of_fixed_assets`：固定资产报废损失
- `$fair_value_change_losses`：公允价值变动损失
- `$financial_expenses`：财务费用
- `$investment_losses`：投资损失
- `$decrease_in_deferred_tax_assets`：递延所得税资产减少
- `$increase_in_deferred_tax_liabilities`：递延所得税负债增加
- `$decrease_in_inventory`：存货的减少
- `$decrease_in_operating_receivables`：经营性应收项目的减少
- `$increase_in_operating_payables`：经营性应付项目的增加
- `$other_adjustments`：其他
- `$special_item_indirect_operating_cash_flows`：间接法-经营活动现金流量净额差额（特殊科目）
- `$net_cash_flows_from_operating_activities_indirect`：间接法-经营活动产生的现金流量净额
- `$conversion_of_debt_to_equity`：债务转为资本
- `$convertible_bonds_due_within_one_year`：一年内到期的可转换公司债券
- `$acquisition_of_fixed_assets_via_finance_lease`：融资租入固定资产
- `$cash_balance_at_end`：现金的期末余额
- `$cash_balance_at_beginning`：现金的期初余额
- `$cash_equivalents_balance_at_end`：现金等价物的期末余额
- `$cash_equivalents_balance_at_beginning`：现金等价物的期初余额
- `$net_increase_in_cce_indirect_method`：间接法 - 现金及现金等价物净增加额
- `$special_item_cce_net_increase_direct_method`：直接法 - 现金及现金等价物净增加额差额（特殊科目）
- `$balancing_item_cce_net_increase_direct_method`：直接法 - 现金及现金等价物净增加额差额（平衡科目）
- `$balancing_item_indirect_operating_cash_flows`：间接法 - 经营活动现金流量净额平衡科目
- `$decrease_in_prepaid_expenses`：待摊费用减少
- `$increase_in_accrued_expenses`：预提费用增加
- `$special_balancing_item_cce_net_increase_indirect`：间接法-现金及现金等价物净增加额特殊科目
- `$balancing_item_cce_net_increase_indirect`：间接法-现金及现金等价物净增加额平衡科目
- `$special_item_closing_cce_balance`：期末现金及现金等价物余额特殊科目
- `$balancing_item_closing_cce_balance`：期末现金及现金等价物余额平衡科目
- `$foreign_exchange_losses`：汇兑损失

#### 偿债能力指标

- `$current_ratio_mrq`：流动比率MRQ
- `$quick_ratio_mrq`：速动比率MRQ
- `$conservative_quick_ratio_mrq`：保守速动比率MRQ
- `$cash_ratio_mrq`：现金比率MRQ
- `$equity_ratio_mrq`：产权比率MRQ
- `$equity_attributable_to_parent_to_total_liabilities_mrq`：归属母公司股东的权益／负债合计MRQ
- `$equity_attributable_to_parent_to_interest_bearing_debt_mrq`：归属母公司股东的权益／带息债务MRQ
- `$tangible_assets_to_total_liabilities_mrq`：有形资产／负债合计MRQ
- `$tangible_assets_to_interest_bearing_debt_mrq`：有形资产／带息债务MRQ
- `$tangible_assets_to_net_debt_mrq`：有形资产／净债务MRQ
- `$ebitda_to_total_liabilities_mrq`：息税折旧摊销前利润／负债合计MRQ
- `$net_cash_flows_from_operating_activities_to_interest_bearing_debt_mrq`：经营活动产生的现金流量净额／带息债务MRQ
- `$net_cash_flows_from_operating_activities_to_net_debt_mrq`：经营活动产生的现金流量净额／净债务MRQ
- `$long_term_debt_to_working_capital_ratio_mrq`：长期债务与营运资金比率MRQ
- `$net_debt_to_market_value_mrq`：净债务／总市值MRQ
- `$interest_bearing_debt_to_market_value_mrq`：带息债务／总市值MRQ

#### 资金流向数据

- `$act_buy_xl`：主动买入特大单金额（单位：元）
- `$pas_buy_xl`：被动买入特大单金额（单位：元）
- `$act_buy_l`：主动买入大单金额（单位：元）
- `$pas_buy_l`：被动买入大单金额（单位：元）
- `$act_buy_m`：主动买入中单金额（单位：元）
- `$pas_buy_m`：被动买入中单金额（单位：元）
- `$act_sell_xl`：主动卖出特大单金额（单位：元）
- `$pas_sell_xl`：被动卖出特大单金额（单位：元）
- `$act_sell_l`：主动卖出大单金额（单位：元）
- `$pas_sell_l`：被动卖出大单金额（单位：元）
- `$act_sell_m`：主动卖出中单金额（单位：元）
- `$pas_sell_m`：被动卖出中单金额（单位：元）
- `$buy_s`：小单买入金额（单位：元）
- `$sell_s`：小单卖出金额（单位：元）
- `$dde_l`：DDE 大单净额（单位：元），即大单主动买入与卖出的差额
- `$net_flow_rate`：金额流入率（单位：%），反映资金净流入占成交总额的比例
- `$l_net_value`：大单净量，通常指大单净买入量或净占比

#### 成长性指标

- `$basic_eps_growth_ratio`：基本每股收益(同比增长率)
- `$diluted_eps_growth_ratio`：稀释每股收益(同比增长率)
- `$operating_cash_flow_per_share_growth_ratio`：每股经营活动产生的现金流量净额(同比增长率)
- `$total_revenue_growth_ratio`：营业总收入(同比增长率)
- `$operating_income_growth_ratio`：营业收入(同比增长率)
- `$operating_profit_growth_ratio`：营业利润(同比增长率)
- `$profit_before_tax_growth_ratio`：利润总额(同比增长率)
- `$net_profit_growth_ratio`：净利润(同比增长率)
- `$net_profit_attributable_to_parent_growth_ratio`：归属母公司股东的净利润(同比增长率)
- `$net_profit_exclude_non_recurring_items_growth_ratio`：归属母公司股东的净利润-扣除非经常损益(同比增长率)
- `$operating_cash_flow_growth_ratio`：经营活动产生的现金流量净额(同比增长率)
- `$return_on_equity_diluted_growth_ratio`：净资产收益率(摊薄)(同比增长率)
- `$net_assets_growth_ratio`：净资产(同比增长率)
- `$total_liabilities_growth_ratio`：总负债(同比增长率)
- `$total_assets_yoy_growth_ratio`：总资产(同比增长率)
- `$net_cash_flow_growth_ratio`：现金净流量(同比增长率)
- `$operating_income_compound_annual_growth_ratio`：营业总收入复合年增长率
- `$net_profit_compound_annual_growth_ratio`：净利润复合增长率
- `$net_profit_attributable_to_parent_compound_annual_growth_ratio`：归属母公司股东的净利润复合年增长率
- `$book_value_per_share_growth_ratio`：每股净资产(相对年初增长率)
- `$total_assets_growth_ratio_since_beginning_of_year`：资产总计(相对年初增长率)
- `$equity_attributable_to_parent_growth_ratio_since_beginning_of_year`：归属母公司股东的权益(相对年初增长率)
- `$total_revenue_growth_ratio_3_years`：营业总收入(3年, 增长率)
- `$total_operating_costs_growth_ratio_3_years`：营业总成本(3年, 增长率)
- `$operating_income_growth_ratio_3_years`：营业收入(3年, 增长率)
- `$operating_profit_growth_ratio_3_years`：营业利润(3年, 增长率)
- `$operating_net_income_growth_ratio_3_years`：经营活动净收益(3年, 增长率)
- `$fair_value_changes_net_income_growth_ratio_3_years`：价值变动净收益(3年, 增长率)
- `$profit_before_tax_growth_ratio_3_years`：利润总额(3年, 增长率)
- `$net_profit_growth_ratio_3_years`：净利润(3年, 增长率)
- `$net_profit_attributable_to_parent_growth_ratio_3_years`：归属母公司股东的净利润(3年, 增长率)
- `$operating_cash_flow_growth_ratio_3_years`：经营活动产生的现金流量净额(3年, 增长率)
- `$total_assets_growth_ratio_3_years`：资产总计(3年, 增长率)
- `$shareholders_equity_growth_ratio_3_years`：股东权益(3年, 增长率)
- `$equity_attributable_to_parent_growth_ratio_3_years`：归属母公司股东的权益(3年, 增长率)
- `$return_on_equity_growth_ratio_3_years`：净资产收益率(3年, 增长率)

#### 利润表

- `$total_operating_revenue`：营业总收入
- `$operating_revenue`：营业收入
- `$net_interest_income`：利息净收入
- `$interest_income`：利息收入
- `$interest_expenses`：利息支出
- `$net_commission_and_fee_income`：手续费及佣金净收入
- `$commission_and_fee_income`：手续费及佣金收入
- `$commission_and_fee_expenses`：手续费及佣金支出
- `$other_business_income`：其他业务收入
- `$earned_premiums`：已赚保费
- `$insurance_revenue`：保险业务收入
- `$reinsurance_income`：分保费收入
- `$ceded_premiums`：分出保费
- `$change_in_unearned_premium_reserve`：提取未到期责任准备金
- `$net_brokerage_income`：经纪业务手续费净收入
- `$net_investment_banking_income`：投资银行业务手续费净收入
- `$net_asset_management_income`：资产管理业务手续费净收入
- `$special_item_total_revenue`：营业总收入差额（特殊科目）
- `$balancing_item_total_revenue`：营业总收入差额（平衡科目）
- `$total_operating_costs`：营业总成本
- `$operating_cost`：营业成本
- `$operating_taxes_and_surcharges`：营业税金及附加
- `$selling_expenses`：销售费用
- `$administrative_expenses`：管理费用
- `$financial_expenses`：财务费用
- `$asset_impairment_loss`：资产减值损失
- `$operating_expenses`：营业支出
- `$business_and_administrative_expenses`：业务及管理费
- `$other_business_expenses`：其他业务成本
- `$surrender_benefits`：退保金
- `$claims_paid`：赔付支出
- `$reinsurer_share_of_claims`：摊回赔付支出
- `$provision_for_insurance_liabilities`：提取保险责任准备金
- `$amortization_of_insurance_liabilities`：摊回保险责任准备金
- `$policyholder_dividend_expenses`：保单红利支出
- `$reinsurance_expenses`：分保费用
- `$amortization_of_reinsurance_expenses`：摊回分保费用
- `$special_item_total_cost`：营业总成本特殊科目
- `$fair_value_change_gain`：公允价值变动收益
- `$investment_income`：投资收益
- `$investment_income_from_associates`：对联营企业和合营企业的投资收益
- `$foreign_exchange_gain`：汇兑收益
- `$balancing_item_total_cost`：营业总成本差额（平衡科目）
- `$operating_profit`：营业利润
- `$special_item_operating_profit`：营业利润差额（特殊科目）
- `$balancing_item_operating_profit`：营业利润差额（平衡科目）
- `$non_operating_income`：营业外收入
- `$non_operating_expenses`：营业外支出
- `$gain_on_disposal_of_non_current_assets`：非流动资产处置利得
- `$loss_on_disposal_of_non_current_assets`：非流动资产处置损失
- `$profit_before_tax`：利润总额
- `$special_item_total_profit`：利润总额差额（特殊科目）
- `$balancing_item_total_profit`：利润总额差额（平衡科目）
- `$income_tax_expense`：所得税费用
- `$net_profit`：净利润
- `$special_item_net_profit`：净利润差额（特殊科目）
- `$balancing_item_net_profit`：净利润差额（平衡科目）
- `$net_profit_attributable_to_parent`：归属于母公司股东的净利润
- `$minority_interest_income`：少数股东损益
- `$other_comprehensive_income`：其他综合收益
- `$oci_attributable_to_parent`：归属母公司所有者的其他综合收益
- `$oci_attributable_to_minority`：归属于少数股东的其他综合收益
- `$total_comprehensive_income`：综合收益总额
- `$total_comprehensive_income_parent`：归属于母公司股东的综合收益总额
- `$total_comprehensive_income_minority`：归属于少数股东的综合收益总额
- `$basic_earnings_per_share`：基本每股收益
- `$diluted_earnings_per_share`：稀释每股收益
- `$non_recurring_gains_losses_parent`：归属于母公司的非经常性损益
- `$main_business_revenue`：主营业务收入
- `$main_business_cost`：主营业务成本
- `$main_business_profit`：主营业务利润
- `$oci_not_reclassifiable_to_pl`：以后不能重分类进损益的其他综合收益
- `$remeasurement_of_defined_benefit_plans`：重新计量设定受益计划净负债或净资产的变动
- `$share_of_unreclassifiable_oci_associates`：权益法下在被投资单位不能重分类进损益的其他综合收益中享有的份额
- `$other_non_reclassifiable_oci`：不可重分类其他综合收益中的其他项
- `$oci_reclassifiable_to_pl`：以后将重分类进损益的其他综合收益
- `$share_of_reclassifiable_oci_associates`：权益法下在被投资单位以后将重分类进损益的其他综合收益中享有的份额
- `$fv_changes_available_for_sale_assets`：可供出售金融资产公允价值变动损益
- `$gain_on_reclassification_htm_to_afs`：持有至到期投资重分类为可供出售金融资产损益
- `$effective_portion_of_cash_flow_hedges`：现金流量套期损益的有效部分
- `$foreign_currency_translation_reserve`：外币财务报表折算差额
- `$other_reclassifiable_oci`：可重分类其他综合收益中的其他项

#### 融资融券数据

- `$fin_value`：融资余额（单位：元）
- `$fin_buy_value`：融资买入额（单位：元）
- `$fin_refund_value`：融资偿还额（单位：元）
- `$sec_value`：融券余额（单位：元）
- `$sec_sell_value`：融券卖出额（单位：元）
- `$sec_refund_value`：融券偿还额（单位：元）
- `$fin_sec_value`：融资融券总余额（单位：元），即融资余额与融券余额之和

#### 行情数据

- `$open`：开盘价
- `$high`：最高价
- `$low`：最低价
- `$close`：收盘价
- `$factor`：复权因子，等于后复权价格除以不复权价格
- `$volume`：成交量
- `$turnover`：成交金额（单位：元）
- `$turnover_rate`：换手率（单位：%）
- `$is_paused`：是否停牌，0 表示未停牌，1 表示停牌
- `$high_limit`：涨停价（单位：元）
- `$low_limit`：跌停价（单位：元）
- `$avg_price`：均价（单位：元）
- `$prev_close`：前收盘价（单位：元）
- `$quote_rate`：涨跌幅（单位：%）
- `$amp_rate`：振幅（单位：%），计算公式为 (最高价 - 最低价) / 前收盘价
- `$is_st`：是否为ST股票，0 表示否，1 表示是

#### 运营效率指标

- `$inventory_turnover_ratio_ttm`：存货周转率TTM
- `$receivables_turnover_ratio_ttm`：应收账款周转率TTM
- `$payables_turnover_ratio_ttm`：应付账款周转率TTM
- `$working_capital_turnover_ratio_ttm`：营运资本周转率TTM
- `$current_assets_turnover_ratio_ttm`：流动资产周转率TTM
- `$non_current_assets_turnover_ratio_ttm`：非流动资产周转率TTM
- `$fixed_assets_turnover_ratio_ttm`：固定资产周转率TTM
- `$total_assets_turnover_ratio_ttm`：总资产周转率TTM
- `$operating_cycle_days`：营业周期
- `$cash_conversion_cycle_days`：现金循环周期
- `$days_of_inventory_outstanding`：存货周转天数
- `$days_sales_outstanding`：应收账款周转天数
- `$days_payable_outstanding`：应付账款周转天数
- `$days_of_current_assets_turnover`：流动资产周转天数
- `$inventory_turnover_ratio`：存货周转率
- `$receivables_turnover_ratio`：应收账款周转率
- `$payables_turnover_ratio`：应付账款周转率
- `$current_assets_turnover_ratio`：流动资产周转率
- `$fixed_assets_turnover_ratio`：固定资产周转率
- `$total_assets_turnover_ratio`：总资产周转率

#### 业绩预告

- `$net_profit_change_range_absolute`：预告净利润变动
- `$net_profit_change_lower_bound`：预告净利润变动下限
- `$net_profit_change_upper_bound`：预告净利润变动上限
- `$net_profit_lower_bound`：预告净利润下限
- `$net_profit_upper_bound`：预告净利润上限
- `$eps_upper_bound`：预告eps上限
- `$eps_lower_bound`：预告eps下限
- `$eps_change_upper_bound`：预告eps变动上限
- `$eps_change_lower_bound`：预告eps变动下限
- `$operating_income_exclude_non_recurring_upper_bound`：预告扣除后营业收入上限
- `$operating_income_exclude_non_recurring_lower_bound`：预告扣除后营业收入下限
- `$net_profit_exclude_non_recurring_upper_bound`：预告扣非净利润上限
- `$net_profit_exclude_non_recurring_lower_bound`：预告扣非净利润下限
- `$net_profit_exclude_non_recurring_change_upper_bound`：预告扣非净利润变动上限
- `$net_profit_exclude_non_recurring_change_lower_bound`：预告扣非净利润变动下限
- `$operating_income_upper_bound`：预告营业收入上限
- `$operating_income_lower_bound`：预告营业收入下限

#### 业绩快报

- `$main_business_revenue`：主营业务收入
- `$main_business_profit`：主营业务利润
- `$profit_before_tax`：利润总额
- `$net_profit_attributable_to_parent`：归属母公司股东的净利润
- `$diluted_earnings_per_share`：摊薄每股收益EPS
- `$basic_earnings_per_share`：基本每股收益EPS
- `$annualized_diluted_return_on_equity`：全面摊薄净资产收益率ROE
- `$weighted_average_return_on_equity`：加权净资产收益率ROE
- `$total_assets`：总资产
- `$net_assets`：净资产
- `$net_profit_exclude_non_recurring_items_parent`：归属母公司股东的扣非净利润

#### 盈利能力指标

- `$return_on_equity_ttm`：股东权益收益率(ROE)TTM
- `$return_on_assets_ebit_ttm`：总资产报酬率（EBIT/总资产）TTM
- `$return_on_assets_ttm`：总资产收益率(ROA)TTM
- `$return_on_invested_capital_ttm`：投入资本回报率(ROIC)TTM
- `$net_profit_margin_ttm`：销售净利率TTM
- `$gross_profit_margin_ttm`：销售毛利率TTM
- `$selling_general_administrative_expenses_ratio_ttm`：销售期间费用率TTM
- `$selling_expense_ratio_ttm`：销售费用率TTM
- `$administrative_expense_ratio_ttm`：管理费用率TTM
- `$financial_expense_ratio_ttm`：财务费用率TTM
- `$operating_profit_margin_ttm`：营业利润率TTM
- `$ebit_margin_ttm`：息税前利润率TTM
- `$cost_of_goods_sold_to_revenue_ratio_ttm`：营业总成本／营业总收入TTM
- `$return_on_equity_average`：净资产收益率-平均(%)
- `$return_on_equity_weighted`：净资产收益率-加权(%)
- `$return_on_equity_diluted`：净资产收益率-摊薄(%)
- `$return_on_equity_deduct_diluted`：净资产收益率-扣除/摊薄(%)
- `$return_on_equity_exclude_non_recurring_items`：净资产收益率-扣除非经常损益(%)
- `$return_on_equity_additional_share_offering`：净资产收益率-增发条件(%)
- `$net_return_on_assets`：总资产净利率(%)
- `$return_on_assets`：总资产报酬率(%)
- `$return_on_invested_capital`：投入资本回报率(%)
- `$return_on_equity_annualized`：净资产收益率-年化(%)
- `$return_on_assets_annualized`：总资产报酬率-年化(%)
- `$return_on_assets_net_profit_annualized`：总资产净利率-年化(%)
- `$net_profit_margin`：销售净利率(%)
- `$gross_profit_margin`：销售毛利率(%)
- `$cost_of_goods_sold_to_revenue_ratio`：销售成本率(%)
- `$selling_general_administrative_expenses_ratio`：销售期间费用率(%)
- `$net_profit_to_total_revenue_ratio`：净利润／营业总收入(%)
- `$operating_profit_to_total_revenue_ratio`：营业利润／营业总收入(%)
- `$ebit_to_total_revenue_ratio`：息税前利润／营业总收入(%)
- `$total_cost_to_total_revenue_ratio`：营业总成本／营业总收入(%)
- `$selling_expense_to_total_revenue_ratio`：销售费用／营业总收入(%)
- `$admin_and_rd_expense_to_total_revenue_ratio`：管理费用+研发费用／营业总收入(%)
- `$financial_expense_to_total_revenue_ratio`：财务费用／营业总收入(%)

#### 估值指标

- `$price_earnings_ratio_lyr`：市盈率LYR
- `$price_earnings_ratio_mrq`：市盈率MRQ
- `$price_earnings_ratio_ttm`：市盈率TTM
- `$forecast_pe_historical`：预测市盈率(PE, 历史预测)
- `$forecast_pe_next_12m`：预测市盈率(PE, 未来12个月)
- `$static_pe_csi`：静态市盈率(中证发布)
- `$rolling_pe_csi`：滚动市盈率(中证发布)
- `$historical_peg`：历史PEG
- `$forecast_peg`：预测PEG
- `$price_book_ratio_mrq`：市净率MRQ
- `$price_book_ratio_csi`：市净率(中证发布)
- `$price_to_operating_cash_flow_lyr`：市现率(PCF, 经营现金流)LYR
- `$price_to_operating_cash_flow_ttm`：市现率(PCF, 经营现金流)TTM
- `$price_to_net_cash_flow_lyr`：市现率(PCF, 现金净流量)LYR
- `$price_to_net_cash_flow_ttm`：市现率(PCF, 现金净流量)TTM
- `$price_to_sales_ratio_lyr`：市销率LYR
- `$price_to_sales_ratio_mrq`：市销率MRQ
- `$price_to_sales_ratio_ttm`：市销率TTM
- `$dividend_yield_ttm`：股息率TTM
- `$total_market_value`：总市值(元)
- `$market_value_by_security_type`：总市值(面向对象)(元)
- `$market_value_csrc_method`：总市值(证监会算法)(元)
- `$free_float_market_value`：流通市值(元)
- `$enterprise_value_including_cash`：企业价值(含货币资金)(元)
- `$enterprise_value_excluding_cash`：企业价值(剔除货币资金)(元)
- `$enterprise_value_to_ebitda`：企业倍数
- `$total_shares`：总股本(股)
- `$free_float_shares`：流通股本(股)
- `$a_share_total_shares`：A股总股本(股)
- `$a_share_free_float_shares`：A股流通股本(股)

### 6. API调用

需要先导入模块`api = get_shared_api('factorsrl.api')`

#### 计算：get_formula_value

- 👑调用方法：

  ```
  get_formula_value(formula, symbols, start_date, end_date)
  ```
- 🔧作用：

  - 计算表达式
- 📚参数说明：

  - `formula`: `str`，表达式
  - `symbols`: `list[str]`，股票代码列表
  - `start_date`: `str`，开始时间
  - `end_date`: `str`，结束时间
- 🔢返回值说明

  - `pd.DataFrame`，index为日期，column为股票代码`
- 📝示例：

  - 调用

    ```
    api = get_shared_api('factorsrl.api')
    api.get_formula_value('DeltaRatio($open, 5)', ['000001.SZ'], '20250101', '20250110')
    ```
  - 返回值

    ```
    000001.SZ
    2025-01-02	-0.010961
    2025-01-03	-0.040268
    2025-01-06	-0.041279
    2025-01-07	-0.030558
    2025-01-08	-0.036044
    2025-01-09	-0.019606
    ```

#### 回测：formula_backtest

- 👑调用方法：

  ```
  formula_backtest(start_date: str, end_date: str, formula: str, index: str = '000300.SH')
  ```
- 🔧作用：

  - 计算表达式
- 📚参数说明：

  - `start_date`: `str`，开始时间
  - `end_date`: `str`，结束时间
  - `formula`: `str`，表达式
  - `index`: `str`，回测股票池
- 🔢返回值说明

  - `dict`，回测结果
- 📝示例：

  - 调用

    ```
    api = get_shared_api('factorsrl.api')
    api.formula_backtest("20240101", "20250101", "DeltaRatio($close, 3)", "000300.SH")
    ```
  - 返回值

    ```
    {'png': '',
     'ic': 0.00610627606511116,
     'ric': 0.003960831556469202,
     'ic_ir': 0.02874748408794403,
     'ric_ir': 0.017184071242809296,
     'long_return': -0.0001597835507709533,
     'long_info_ratio': -0.006641531828790903,
     'long_cum_return': -0.038667596876621246,
     'long_max_drawdown': -0.282393217086792,
     'ls_return': -0.0006236198241822422,
     'ls_info_ratio': -0.03399030119180679,
     'ls_cum_return': -0.15091603994369507,
     'ls_max_drawdown': -0.4293464124202728}
    ```

## 使用技巧

### 1.会话管理

- **任务切换时新建会话**——一个会话应聚焦单一目标。若先写代码后转数据分析，或要写另外一个策略时，应避免在同一会话中延续，旧上下文会干扰新任务的判断。
- **试错陷入僵局时重置**——同一方案多次修改仍未解决，不如新建会话重新阐明目标，往往比在原会话中反复调整更高效。
- **及时关闭闲置会话**——挂起的会话同样占用研究环境资源，无需保留时应及时关闭。

### 2.研究环境资源

Agent 运行于用户的研究环境中，其文件读写、脚本执行及算力与内存占用均计入该研究环境的资源消耗，使用时应注意节制:

- **回测及计算任务受内存限制**——执行回测或其他计算任务时，运行环境的内存上限会直接影响任务能否跑通及运行速度。任务前应评估数据规模与内存占用，避免超出限制导致中断或失败。
- **大规模计算先小规模验证**——全量回测、大规模数据处理等任务，应先以小规模数据验证思路，确认方向正确后再全量执行，避免资源浪费。
- **文件复用研究环境**——可以在研究环境中进行文件相关操作。

### 3.把话说对

- **说明目标而非步骤**——以「修改量化策略xx逻辑」代替「修改某文件第 30 行」，明确期望结果，保留其判断空间。
- **一次性给出约束**——语言、输出格式、是否改动文件、范围边界等要求应在开头明确，减少来回返工。
- **提供充分背景**——相关报错、文件路径、已尝试的操作等应一并提供，优于让其自行推测。
- **精准指出偏差**——结果偏离预期时，明确指出「第三点应改为 XXX」优于笼统要求「重做」。

### 4.干活方式

- **复杂任务先确认方案**——先让其给出思路或示例，确认方向无误后再推进，纠正方向的成本远低于返工。
- **拆解为可验证的小步**——大任务拆分为独立可验证的单元，每完成一步即确认，避免最终才发现整体偏离。
- **完成后让其自行验证**——运行测试、构建或类型检查，不应仅以「应该没问题」为准。
