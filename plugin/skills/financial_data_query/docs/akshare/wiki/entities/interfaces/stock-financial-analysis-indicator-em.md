---
title: "stock_financial_analysis_indicator_em - 主要指标-东方财富"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_financial_analysis_indicator_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 主要指标-东方财富
- 描述: 东方财富-A股-财务分析-主要指标
- 目标地址: https://emweb.securities.eastmoney.com/pc_hsf10/pages/index.html?type=web&code=SZ301389&color=b#/cwfx
- 限量: 单次获取指定 symbol 的所有数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 主要指标-东方财富

接口: stock_financial_analysis_indicator_em

目标地址: https://emweb.securities.eastmoney.com/pc_hsf10/pages/index.html?type=web&code=SZ301389&color=b#/cwfx

描述: 东方财富-A股-财务分析-主要指标

限量: 单次获取指定 symbol 的所有数据

输入参数

| 名称        | 类型  | 描述                                           |
|-----------|-----|----------------------------------------------|
| symbol    | str | symbol="301389.SZ"; 股票代码                     |
| indicator | str | indicator="按报告期"; choice of {"按报告期", "按单季度"} |

输出参数

| 名称                 | 类型      | 描述               |
|--------------------|---------|------------------|
| SECUCODE           | object  | 股票代码(带后缀)        |
| SECURITY_CODE      | object  | 股票代码             |
| SECURITY_NAME_ABBR | object  | 股票名称             |
| REPORT_DATE        | object  | 报告日期             |
| REPORT_TYPE        | object  | 报告类型             |
| REPORT_DATE_NAME   | object  | 报告日期名称           |
| EPSJB              | float64 | 基本每股收益(元)        |
| EPSKCJB            | float64 | 扣非每股收益(元)        |
| EPSXS              | float64 | 稀释每股收益(元)        |
| BPS                | float64 | 每股净资产(元)         |
| MGZBGJ             | float64 | 每股公积金(元)         |
| MGWFPLR            | float64 | 每股未分配利润(元)       |
| MGJYXJJE           | float64 | 每股经营现金流(元)       |
| TOTALOPERATEREVE   | float64 | 营业总收入(元)         |
| MLR                | float64 | 毛利润(元)           |
| PARENTNETPROFIT    | float64 | 归属净利润(元)         |
| KCFJCXSYJLR        | float64 | 扣非净利润(元)         |
| TOTALOPERATEREVETZ | float64 | 营业总收入同比增长(%)     |
| PARENTNETPROFITTZ  | float64 | 归属净利润同比增长(%)     |
| KCFJCXSYJLRTZ      | float64 | 扣非净利润同比增长(%)     |
| YYZSRGDHBZC        | float64 | 营业总收入滚动环比增长(%)   |
| NETPROFITRPHBZC    | float64 | 归属净利润滚动环比增长(%)   |
| KFJLRGDHBZC        | float64 | 扣非净利润滚动环比增长(%)   |
| ROEJQ              | float64 | 净资产收益率(加权)(%)    |
| ROEKCJQ            | float64 | 净资产收益率(扣非/加权)(%) |
| ZZCJLL             | float64 | 总资产收益率(加权)(%)    |
| XSJLL              | float64 | 净利率(%)           |
| XSMLL              | float64 | 毛利率(%)           |
| YSZKYYSR           | float64 | 预收账款/营业收入        |
| XSJXLYYSR          | float64 | 销售净现金流/营业收入      |
| JYXJLYYSR          | float64 | 经营净现金流/营业收入      |
| TAXRATE            | float64 | 实际税率(%)          |
| LD                 | float64 | 流动比率             |
| SD                 | float64 | 速动比率             |
| XJLLB              | float64 | 现金流量比率           |
| ZCFZL              | float64 | 资产负债率(%)         |
| QYCS               | float64 | 权益系数             |
| CQBL               | float64 | 产权比率             |
| ZZCZZTS            | float64 | 总资产周转天数(天)       |
| CHZZTS             | float64 | 存货周转天数(天)        |
| YSZKZZTS           | float64 | 应收账款周转天数(天)      |
| TOAZZL             | float64 | 总资产周转率(次)        |
| CHZZL              | float64 | 存货周转率(次)         |
| YSZKZZL            | float64 | 应收账款周转率(次)       |
| ...                | ...     | ...              |

接口示例

```python
import akshare as ak

stock_financial_analysis_indicator_em_df = ak.stock_financial_analysis_indicator_em(symbol="301389.SZ", indicator="按报告期")
print(stock_financial_analysis_indicator_em_df)
```

数据示例

```
     SECUCODE SECURITY_CODE  ... NET_ASSETS_LIABILITIES PROPRIETARY_CAPITAL
0   301389.SZ        301389  ...                   None                None
1   301389.SZ        301389  ...                   None                None
2   301389.SZ        301389  ...                   None                None
3   301389.SZ        301389  ...                   None                None
4   301389.SZ        301389  ...                   None                None
5   301389.SZ        301389  ...                   None                None
6   301389.SZ        301389  ...                   None                None
7   301389.SZ        301389  ...                   None                None
8   301389.SZ        301389  ...                   None                None
9   301389.SZ        301389  ...                   None                None
10  301389.SZ        301389  ...                   None                None
11  301389.SZ        301389  ...                   None                None
12  301389.SZ        301389  ...                   None                None
13  301389.SZ        301389  ...                   None                None
14  301389.SZ        301389  ...                   None                None
15  301389.SZ        301389  ...                   None                None
16  301389.SZ        301389  ...                   None                None
17  301389.SZ        301389  ...                   None                None
18  301389.SZ        301389  ...                   None                None
19  301389.SZ        301389  ...                   None                None
[20 rows x 140 columns]
```
