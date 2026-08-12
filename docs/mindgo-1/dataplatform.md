# 同花顺量化数据平台完整文档

来源: https://quant.10jqka.com.cn/view/dataplatform#1
下载时间: 2026-08-12T06:24:20.735Z
目录数: 55
数据文档数: 101
成功解析详情页: 101
解析失败详情页: 0

## 目录

- 股票 (id: 1, parentId: 0)
- 期货 (id: 2, parentId: 0)
- 期权 (id: 3, parentId: 0)
- 基金 (id: 4, parentId: 0)
- 指数 (id: 5, parentId: 0)
- 债券 (id: 6, parentId: 0)
- 外汇 (id: 7, parentId: 0)
- 风险模型 (id: 8, parentId: 0)
- 因子数据 (id: 9, parentId: 0)
  - A股 (id: 11, parentId: 1)
    - 基本信息(A股) (id: 14, parentId: 11)
    - 交易日历(A股) (id: 15, parentId: 11)
    - 行情数据(A股) (id: 16, parentId: 11)
    - 高频行情数据(A股) (id: 17, parentId: 11)
    - 行业分类 (id: 18, parentId: 11)
    - 同花顺概念(A股) (id: 19, parentId: 11)
    - 上市公司财务数据 (id: 20, parentId: 11)
    - 分析师一致预期 (id: 21, parentId: 11)
    - 上市公司资料 (id: 22, parentId: 11)
    - 市场资金数据 (id: 23, parentId: 11)
  - 内地期货 (id: 33, parentId: 2)
  - 延期交收合约(T+D合约) (id: 34, parentId: 2)
  - 金融期权 (id: 35, parentId: 3)
  - 场内基金 (id: 36, parentId: 4)
  - 场外基金 (id: 37, parentId: 4)
  - 可转债 (id: 38, parentId: 6)
- iFinD数据接口 (id: 44, parentId: 0)
    - 期货基本信息 (id: 48, parentId: 33)
    - 期货交易日历 (id: 49, parentId: 33)
    - 期货行情数据 (id: 50, parentId: 33)
    - TD合约基本信息 (id: 51, parentId: 34)
    - TD合约交易日历 (id: 52, parentId: 34)
    - TD合约行情数据 (id: 53, parentId: 34)
    - 期权基本信息 (id: 54, parentId: 35)
    - 期权交易日历 (id: 55, parentId: 35)
    - 期权行情数据 (id: 56, parentId: 35)
    - 可转债基本信息 (id: 57, parentId: 38)
    - 可转债行情 (id: 58, parentId: 38)
    - 可转债条款信息 (id: 59, parentId: 38)
  - CNE5风险模型 (id: 60, parentId: 8)
    - 基金基本信息 (id: 65, parentId: 36)
    - 基金净值数据 (id: 66, parentId: 36)
    - 基金行情数据 (id: 67, parentId: 36)
    - 基金基本信息 (id: 68, parentId: 37)
    - 基金净值数据 (id: 69, parentId: 37)
    - 基金持仓情况 (id: 70, parentId: 37)
  - 指数基本信息 (id: 73, parentId: 5)
  - 指数行情数据 (id: 74, parentId: 5)
  - 指数成分股数据 (id: 75, parentId: 5)
  - 外汇基本信息 (id: 76, parentId: 7)
  - 外汇交易日历 (id: 77, parentId: 7)
  - 外汇行情数据 (id: 78, parentId: 7)
    - 另类数据 (id: 79, parentId: 11)
- i问财接口 (id: 80, parentId: 0)
    - 期货市场信息 (id: 84, parentId: 33)

## 数据文档

### 风险模型 / CNE5风险模型

- [CNE5风险模型](dataplatform_details/md/244_CNE5风险模型.md) - 支持获取CNE5版本风险因子暴露数据、因子收益、特质收益率数据 (字段 0, 代码块 3)

### 股票 / A股 / 分析师一致预期

- [分析师一致预期(A股)](dataplatform_details/md/77_分析师一致预期(A股).md) - 分析师一致预期数据 (字段 12, 代码块 2)

### 股票 / A股 / 高频行情数据(A股)

- [历史行情快照(A股)](dataplatform_details/md/16_历史行情快照(A股).md) - A股历史行情快照数据 (字段 29, 代码块 1)
- [实时行情快照(A股)](dataplatform_details/md/20_实时行情快照(A股).md) - 股票实时行情快照接口 (字段 30, 代码块 1)

### 股票 / A股 / 基本信息(A股)

- [股票基本信息(A股)](dataplatform_details/md/1_股票基本信息(A股).md) - 全市场股票基本信息数据，包含股票代码、中文简称、上市日期、退市日期等数据 (字段 7, 代码块 3)

### 股票 / A股 / 交易日历(A股)

- [交易日历(A股)](dataplatform_details/md/5_交易日历(A股).md) - 沪京深交易所交易日历数据 (字段 0, 代码块 1)

### 股票 / A股 / 另类数据

- [新闻评级数据](dataplatform_details/md/393_新闻评级数据.md) - 记录了新闻标题、新闻来源、新闻评级、新闻发布时间、新闻评级时间、对应股票代码数据 (字段 6, 代码块 2)
- [举牌事件](dataplatform_details/md/394_举牌事件.md) - 记录了A股上市公司举牌事件数据 (字段 7, 代码块 2)
- [实控人变更事件](dataplatform_details/md/395_实控人变更事件.md) - 记录A股上市公司实控人变更事件相关数据 (字段 4, 代码块 2)
- [定向增发事件](dataplatform_details/md/396_定向增发事件.md) - 记录了A股上市公司定向增发事件相关数据 (字段 7, 代码块 2)
- [机构调研数据](dataplatform_details/md/397_机构调研数据.md) - 记录A股上市公司机构调研事件相关数据 (字段 21, 代码块 2)
- [龙虎榜](dataplatform_details/md/538_龙虎榜.md) - 记录A股上市公司进入龙虎榜相关数据 (字段 33, 代码块 2)

### 股票 / A股 / 上市公司财务数据

- [资产负债表](dataplatform_details/md/64_资产负债表.md) - A股上市公司合并资产负债表数据 (字段 157, 代码块 3)
- [利润表](dataplatform_details/md/341_利润表.md) - A股上市公司合并利润表数据 (字段 98, 代码块 3)
- [现金流量表](dataplatform_details/md/342_现金流量表.md) - A股上市公司合并现金流量表数据 (字段 123, 代码块 3)
- [业绩快报](dataplatform_details/md/343_业绩快报.md) - A股上市公司业绩快报数据 (字段 15, 代码块 2)
- [业绩预告](dataplatform_details/md/344_业绩预告.md) - A股上市公司业绩预告数据 (字段 21, 代码块 2)
- [估值指标表](dataplatform_details/md/345_估值指标表.md) - A股上市公司估值相关计算财务指标 (字段 59, 代码块 2)
- [偿还能力表](dataplatform_details/md/346_偿还能力表.md) - A股上市公司偿还能力相关计算财务指标 (字段 41, 代码块 2)
- [运营能力表](dataplatform_details/md/355_运营能力表.md) - A股上市公司运营能力相关计算财务指标 (字段 30, 代码块 2)
- [盈利能力表](dataplatform_details/md/356_盈利能力表.md) - A股上市公司盈利能力计算财务指标
 (字段 48, 代码块 2)
- [成长能力表](dataplatform_details/md/357_成长能力表.md) - A股上市公司成长能力计算财务指标 (字段 40, 代码块 2)
- [成长能力表(单季度)](dataplatform_details/md/358_成长能力表(单季度).md) - A股上市公司单季度成长能力计算财务指标数据 (字段 5, 代码块 2)
- [现金流量表(单季度)](dataplatform_details/md/359_现金流量表(单季度).md) - A股上市公司单季度合并现金流量表数据都 (字段 113, 代码块 2)
- [盈利能力表(单季度)](dataplatform_details/md/360_盈利能力表(单季度).md) - A股上市公司单季度盈利能力计算财务指标数据 (字段 10, 代码块 2)
- [利润表(单季度)](dataplatform_details/md/361_利润表(单季度).md) - A股上市公司单季度利润表 (字段 88, 代码块 2)

### 股票 / A股 / 上市公司资料

- [公司更名信息](dataplatform_details/md/81_公司更名信息.md) - 记录A股上市公司简称变更情况，可用来判断ST、退市情况 (字段 7, 代码块 2)
- [公司员工数量表](dataplatform_details/md/85_公司员工数量表.md) - 记录公司在职、退休员工数量 (字段 8, 代码块 2)
- [十大股东信息表](dataplatform_details/md/89_十大股东信息表.md) - 记录A股上市公司十大股东信息 (字段 14, 代码块 2)
- [十大流通股东信息表](dataplatform_details/md/93_十大流通股东信息表.md) - 记录A股上市公司十大流通股东信息 (字段 12, 代码块 2)
- [上市公司所在地](dataplatform_details/md/97_上市公司所在地.md) - 记录了A股上市公司所在的省(自治区、直辖市)、市、县(区) (字段 5, 代码块 2)
- [公司股本变动表](dataplatform_details/md/101_公司股本变动表.md) - 记录了公司股本变动情况，可根据此计算市值等数据 (字段 14, 代码块 2)
- [机构股东持股情况表](dataplatform_details/md/105_机构股东持股情况表.md) - 记录了A股上市公司机构股东持股数据 (字段 9, 代码块 2)
- [解禁明细表](dataplatform_details/md/109_解禁明细表.md) - 记录A股上市公司限售股解禁明细数据 (字段 10, 代码块 2)
- [配股信息表](dataplatform_details/md/113_配股信息表.md) - 记录上市公司配股信息 (字段 3, 代码块 2)
- [分红送股信息](dataplatform_details/md/117_分红送股信息.md) - 记录A股上市公司历史分红送股数据 (字段 20, 代码块 3)

### 股票 / A股 / 市场资金数据

- [融资融券数据](dataplatform_details/md/121_融资融券数据.md) - 获取A股融资融券数据 (字段 7, 代码块 3)
- [日频资金流向数据](dataplatform_details/md/558_日频资金流向数据.md) - 记录了日频主动买入、大单特大单等资金流向数据 (字段 17, 代码块 3)
- [半小时资金流向数据](dataplatform_details/md/566_半小时资金流向数据.md) - 记录了半小时级别主动买入、大单特大单等资金流向数据 (字段 17, 代码块 3)
- [五分钟资金流向数据](dataplatform_details/md/574_五分钟资金流向数据.md) - 记录了五分钟级别主动买入、大单特大单等资金流向数据 (字段 17, 代码块 3)

### 股票 / A股 / 同花顺概念(A股)

- [同花顺概念分类](dataplatform_details/md/66_同花顺概念分类.md) - 同花顺概念分类数据 (字段 8, 代码块 2)
- [概念股数据(A股)](dataplatform_details/md/70_概念股数据(A股).md) - A股概念股数据，可跟据概念代码查询相关概念股 (字段 0, 代码块 2)
- [个股概念数据](dataplatform_details/md/73_个股概念数据.md) - A股个股概念数据表，可根据股票代码与日期查询股票所属全部概念 (字段 3, 代码块 2)

### 股票 / A股 / 行情数据(A股)

- [股票日行情数据(A股)](dataplatform_details/md/8_股票日行情数据(A股).md) - A股股票日频行情数据 (字段 16, 代码块 3)
- [股票分钟行情数据(A股)](dataplatform_details/md/12_股票分钟行情数据(A股).md) - A股股票分钟行情数据 (字段 9, 代码块 3)
- [开盘竞价成交信息](dataplatform_details/md/435_开盘竞价成交信息.md) - 记录A股开盘集合竞价成交信息数据 (字段 2, 代码块 3)

### 股票 / A股 / 行业分类

- [行业分类信息](dataplatform_details/md/24_行业分类信息.md) - 同花顺一级行业分类信息 (字段 9, 代码块 2)

### 基金 / 场内基金 / 基金基本信息

- [场内基金基本信息](dataplatform_details/md/249_场内基金基本信息.md) - 场内基金(ETF、LOF等)基本信息，包括代码、简称、上市日期、退市日期等数据 (字段 7, 代码块 3)

### 基金 / 场内基金 / 基金净值数据

- [基金净值数据](dataplatform_details/md/253_基金净值数据.md) - 场内基金对应场外基金净值数据 (字段 3, 代码块 3)

### 基金 / 场内基金 / 基金行情数据

- [基金日频行情数据](dataplatform_details/md/257_基金日频行情数据.md) - 场内基金日频行情数据 (字段 15, 代码块 3)
- [基金分钟行情数据](dataplatform_details/md/258_基金分钟行情数据.md) - 场内基金分钟行情数据 (字段 8, 代码块 3)
- [基金实时行情数据](dataplatform_details/md/259_基金实时行情数据.md) - 场内基金实时行情数据 (字段 52, 代码块 1)

### 基金 / 场外基金 / 基金持仓情况

- [基金十大持仓](dataplatform_details/md/277_基金十大持仓.md) - 基金季报披露的十大持仓数据 (字段 11, 代码块 2)
- [基金持仓明细](dataplatform_details/md/278_基金持仓明细.md) - 基金半年报、年报披露的持仓明细数据 (字段 11, 代码块 2)

### 基金 / 场外基金 / 基金基本信息

- [场外基金基本信息](dataplatform_details/md/269_场外基金基本信息.md) - 场外基金基本信息数据，包括代码、简称、发行日期、解散日期等数据 (字段 7, 代码块 3)

### 基金 / 场外基金 / 基金净值数据

- [基金净值数据](dataplatform_details/md/273_基金净值数据.md) - 场外基金净值数据 (字段 3, 代码块 3)

### 期货 / 内地期货 / 期货基本信息

- [期货基本信息(商品)](dataplatform_details/md/159_期货基本信息(商品).md) - 商品期货基本信息，包含合约代码、中文简称、上市日期、退市日期等数据 (字段 7, 代码块 3)
- [期货基本信息(金融)](dataplatform_details/md/160_期货基本信息(金融).md) - 金融期货基本信息，包含合约代码、中文简称、上市日期、退市日期等数据 (字段 7, 代码块 3)
- [期货基本信息(国债)](dataplatform_details/md/161_期货基本信息(国债).md) - 国债期货基本信息，包含合约代码、中文简称、上市日期、退市日期等数据 (字段 7, 代码块 3)

### 期货 / 内地期货 / 期货交易日历

- [期货交易日历](dataplatform_details/md/171_期货交易日历.md) - 内地期货交易所交易日历 (字段 0, 代码块 1)

### 期货 / 内地期货 / 期货市场信息

- [期货日交易排名](dataplatform_details/md/426_期货日交易排名.md) - 期货日交易排名表，包含持仓龙虎榜、多头持仓龙虎榜、空头持仓龙虎榜数据 (字段 7, 代码块 2)
- [期货库存情况](dataplatform_details/md/427_期货库存情况.md) - 期货库存情况表，包含库存量、库存变动、注册仓单数量、注册仓单变动、可用库存量、可用库存变动数据 (字段 10, 代码块 2)

### 期货 / 内地期货 / 期货行情数据

- [期货日频行情数据](dataplatform_details/md/174_期货日频行情数据.md) - 期货日频行情数据 (字段 14, 代码块 3)
- [期货分钟行情数据](dataplatform_details/md/422_期货分钟行情数据.md) - 记录了内地交易所期货分钟频行情数据 (字段 7, 代码块 3)

### 期货 / 延期交收合约(T+D合约) / TD合约基本信息

- [TD合约基本信息](dataplatform_details/md/178_TD合约基本信息.md) - T+D合约基本信息，包含合约代码、中文简称、上市日期、退市日期等数据 (字段 7, 代码块 3)

### 期货 / 延期交收合约(T+D合约) / TD合约交易日历

- [TD合约交易日历](dataplatform_details/md/182_TD合约交易日历.md) - T+D合约交易日历 (字段 0, 代码块 1)

### 期货 / 延期交收合约(T+D合约) / TD合约行情数据

- [TD合约日频行情数据](dataplatform_details/md/185_TD合约日频行情数据.md) - T+D合约日频行情数据 (字段 7, 代码块 3)

### 期权 / 金融期权 / 期权基本信息

- [期权基本信息](dataplatform_details/md/189_期权基本信息.md) - 沪深交易所期权合约基本信息，包含合约代码、合约简称、合约上市时间、退市时间等信息 (字段 7, 代码块 3)

### 期权 / 金融期权 / 期权交易日历

- [期权交易日历](dataplatform_details/md/193_期权交易日历.md) - 沪深交易所交易日历 (字段 0, 代码块 1)

### 期权 / 金融期权 / 期权行情数据

- [期权日频行情数据](dataplatform_details/md/196_期权日频行情数据.md) - 沪深交易所ETF期权日频行情数据 (字段 5, 代码块 3)
- [期权分钟行情数据](dataplatform_details/md/197_期权分钟行情数据.md) - 沪深交易所ETF期权分钟行情数据 (字段 5, 代码块 3)

### 外汇 / 外汇基本信息

- [外汇基本信息](dataplatform_details/md/332_外汇基本信息.md) - 记录了外汇(中国银行双向宝合约)的基本信息 (字段 7, 代码块 3)

### 外汇 / 外汇交易日历

- [外汇交易日历](dataplatform_details/md/336_外汇交易日历.md) - 中国银行双向宝合约交易日历数据 (字段 0, 代码块 1)

### 外汇 / 外汇行情数据

- [外汇日行情数据](dataplatform_details/md/324_外汇日行情数据.md) - 外汇日频行情数据 (字段 4, 代码块 3)
- [外汇分钟行情数据](dataplatform_details/md/325_外汇分钟行情数据.md) - 外汇分钟频行情数据 (字段 4, 代码块 3)

### 因子数据

- [技术因子](dataplatform_details/md/285_技术因子.md) - 常见量价指标类因子 (字段 61, 代码块 2)
- [基本面因子](dataplatform_details/md/289_基本面因子.md) - 常见的财务指标因子 (字段 66, 代码块 2)

### 债券 / 可转债 / 可转债基本信息

- [可转债基本信息](dataplatform_details/md/204_可转债基本信息.md) - 包含可转债代码、简称、上市日期、退市日期等数据 (字段 7, 代码块 3)

### 债券 / 可转债 / 可转债条款信息

- [可转债条款信息](dataplatform_details/md/224_可转债条款信息.md) - 记录可转债条款数据，包含日期条款、利率条款、转股价下修条款、赎回条款、回售条款数据 (字段 34, 代码块 2)
- [可转债转股价变更表](dataplatform_details/md/228_可转债转股价变更表.md) - 记录可转债历史转股价变更信息 (字段 5, 代码块 2)
- [可转债余额变动表](dataplatform_details/md/229_可转债余额变动表.md) - 记录可转债余额变动情况以及变动原因 (字段 4, 代码块 2)
- [可转债转股数量表](dataplatform_details/md/230_可转债转股数量表.md) - 记录可转债转股数量、户数、价格数据 (字段 10, 代码块 2)
- [可转债特殊条款预计价格表](dataplatform_details/md/231_可转债特殊条款预计价格表.md) - 可转债特殊条款预计执行价格数据 (字段 4, 代码块 2)

### 债券 / 可转债 / 可转债行情

- [可转债日行情数据](dataplatform_details/md/208_可转债日行情数据.md) - 沪深交易所上市可转债日频行情数据 (字段 12, 代码块 3)
- [可转债分钟行情数据](dataplatform_details/md/209_可转债分钟行情数据.md) - 沪深交易所上市可转债分钟行情数据 (字段 8, 代码块 3)
- [可转债实时行情快照](dataplatform_details/md/210_可转债实时行情快照.md) - 沪深交易所上市可转债实时行情快照 (字段 52, 代码块 1)
- [可转债历史行情快照](dataplatform_details/md/211_可转债历史行情快照.md) - 沪深交易所上市可转债历史行情快照 (字段 53, 代码块 1)

### 指数 / 指数成分股数据

- [指数成分股及权重](dataplatform_details/md/300_指数成分股及权重.md) - 包含了常见加权指数的成分股权重 (字段 2, 代码块 0)

### 指数 / 指数基本信息

- [指数基本信息](dataplatform_details/md/293_指数基本信息.md) - 主流指数基本信息，包括代码、简称、启用日期等数据 (字段 7, 代码块 3)
- [常用股票型指数](dataplatform_details/md/295_常用股票型指数.md) - 记录了常用股票型指数代码 (字段 0, 代码块 0)
- [常用基金型指数](dataplatform_details/md/488_常用基金型指数.md) - 记录了常用基金型指数  (字段 0, 代码块 0)
- [常用债券型指数](dataplatform_details/md/498_常用债券型指数.md) - 记录了常用债券型指数 (字段 0, 代码块 0)
- [常用期货型指数](dataplatform_details/md/504_常用期货型指数.md) - 记录了常用期货型指数 (字段 0, 代码块 0)
- [常用港股指数](dataplatform_details/md/510_常用港股指数.md) - 记录了常用港股指数 (字段 0, 代码块 0)
- [常用全球指数](dataplatform_details/md/512_常用全球指数.md) - 记录了常用全球指数 (字段 0, 代码块 0)

### 指数 / 指数行情数据

- [指数日行情数据](dataplatform_details/md/296_指数日行情数据.md) - 常用指数日频行情数据 (字段 16, 代码块 3)
- [指数分钟行情数据](dataplatform_details/md/297_指数分钟行情数据.md) - 常用指数分钟频行情数据 (字段 9, 代码块 3)
- [指数实时行情快照](dataplatform_details/md/298_指数实时行情快照.md) - 常用指数实时行情快照数据 (字段 52, 代码块 1)

### i问财接口

- [query_iwencai](dataplatform_details/md/398_query_iwencai.md) - 问财接口服务，结果与问财网页版相同 (字段 0, 代码块 1)
- [get_iwencai](dataplatform_details/md/399_get_iwencai.md) - 自然语言选股接口服务，选股结果与问财backtest等同。仅支持在股票策略初始化阶段调用。 (字段 0, 代码块 2)

### iFinD数据接口

- [iFinD数据接口](dataplatform_details/md/419_iFinD数据接口.md) - iFinD金融数据终端提供Python数据接口 (字段 0, 代码块 7)

