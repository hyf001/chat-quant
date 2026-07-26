---
title: "fund_fh_rank_em - 基金分红排行"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_fh_rank_em

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 分红送配 > 基金分红排行
- 描述: 天天基金网-基金数据-分红送配-基金分红排行
- 目标地址: http://fund.eastmoney.com/data/fundleijifenhong.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 基金分红排行

接口: fund_fh_rank_em

目标地址: http://fund.eastmoney.com/data/fundleijifenhong.html

描述: 天天基金网-基金数据-分红送配-基金分红排行

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称   | 类型      | 描述        |
|------|---------|-----------|
| 序号   | int64   | -         |
| 基金代码 | object  | -         |
| 基金简称 | object  | -         |
| 累计分红 | float64 | 注意单位: 元/份 |
| 累计次数 | int64   | -         |
| 成立日期 | object  | -         |

接口示例

```python
import akshare as ak

fund_fh_rank_em_df = ak.fund_fh_rank_em()
print(fund_fh_rank_em_df)
```

数据示例

```
        序号  基金代码            基金简称      累计分红  累计次数   成立日期
0        1  511220      海富通上证城投债ETF  32.760000    27  2014-11-13
1        2  184801      鹏华前海万科REITS  32.528400     5  2015-07-06
2        3  511880            银华日利A  27.060000     9  2013-04-01
3        4  003816            银华日利B  25.794000     6  2016-11-23
4        5  511270     海富通上证10年期ETF   9.770000    12  2018-10-12
    ...     ...              ...        ...   ...         ...
4616  4617  009678  浙商智多益稳健一年持有期混合C   0.001000     1  2021-01-29
4617  4618  010539     浙商智多金稳健一年持有A   0.001000     1  2021-06-24
4618  4619  006792     鹏华港美互联股票美元现汇   0.000607     1  2019-04-15
4619  4620  159937          博时黄金ETF   0.000200     1  2014-08-13
4620  4621  008139        鑫元一年中高等级债   0.000100     1  2020-03-18
```
