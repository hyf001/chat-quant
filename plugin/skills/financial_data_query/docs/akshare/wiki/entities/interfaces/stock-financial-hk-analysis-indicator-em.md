---
title: "stock_financial_hk_analysis_indicator_em - 港股财务指标"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_financial_hk_analysis_indicator_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 港股财务指标
- 描述: 东方财富-港股-财务分析-主要指标
- 目标地址: https://emweb.securities.eastmoney.com/PC_HKF10/NewFinancialAnalysis/index?type=web&code=00700
- 限量: 单次获取财务指标所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 港股财务指标

接口: stock_financial_hk_analysis_indicator_em

目标地址: https://emweb.securities.eastmoney.com/PC_HKF10/NewFinancialAnalysis/index?type=web&code=00700

描述: 东方财富-港股-财务分析-主要指标

限量: 单次获取财务指标所有历史数据

输入参数

| 名称        | 类型  | 描述                                      |
|-----------|-----|-----------------------------------------|
| symbol    | str | symbol="00700"; 股票代码                    |
| indicator | str | indicator="年度"; choice of {"年度", "报告期"} |

输出参数

| 名称                  | 类型      | 描述             |
|---------------------|---------|----------------|
| SECUCODE            | object  | 股票代码(带HK后缀)    |
| SECURITY_CODE       | object  | 股票代码(不带HK后缀)   |
| SECURITY_NAME_ABBR  | object  | 股票名称           |
| ORG_CODE            | object  | ORG_CODE       |
| REPORT_DATE         | object  | 报告日期           |
| DATE_TYPE_CODE      | object  | 报告日期类型         |
| PER_NETCASH_OPERATE | float64 | 每股经营现金流(元)     |
| PER_OI              | float64 | 每股营业收入(元)      |
| BPS                 | float64 | 每股净资产(元)       |
| BASIC_EPS           | float64 | 基本每股收益(元)      |
| DILUTED_EPS         | float64 | 稀释每股收益(元)      |
| OPERATE_INCOME      | int64   | 营业总收入(元)       |
| OPERATE_INCOME_YOY  | float64 | 营业总收入同比增长(%)   |
| GROSS_PROFIT        | int64   | 毛利润(元)         |
| GROSS_PROFIT_YOY    | float64 | 毛利润同比增长(%)     |
| HOLDER_PROFIT       | int64   | 归母净利润(元)       |
| HOLDER_PROFIT_YOY   | float64 | 归母净利润同比增长(%)   |
| GROSS_PROFIT_RATIO  | float64 | 毛利率(%)         |
| EPS_TTM             | float64 | TTM每股收益(元)     |
| OPERATE_INCOME_QOQ  | float64 | 营业总收入滚动环比增长(%) |
| NET_PROFIT_RATIO    | float64 | 净利率(%)         |
| ROE_AVG             | float64 | 平均净资产收益率(%)    |
| GROSS_PROFIT_QOQ    | float64 | 毛利润滚动环比增长(%)   |
| ROA                 | float64 | 总资产净利率(%)      |
| HOLDER_PROFIT_QOQ   | float64 | 归母净利润滚动环比增长(%) |
| ROE_YEARLY          | float64 | 年化净资产收益率(%)    |
| ROIC_YEARLY         | float64 | 年化投资回报率(%)     |
| TAX_EBT             | float64 | 所得税/利润总额(%)    |
| OCF_SALES           | float64 | 经营现金流/营业收入(%)  |
| DEBT_ASSET_RATIO    | float64 | 资产负债率(%)       |
| CURRENT_RATIO       | float64 | 流动比率(倍)        |
| CURRENTDEBT_DEBT    | float64 | 流动负债/总负债(%)    |
| START_DATE          | object  | START_DATE     |
| FISCAL_YEAR         | object  | 年结日            |
| CURRENCY            | object  | CURRENCY       |
| IS_CNY_CODE         | int64   | IS_CNY_CODE    |

接口示例

```python
import akshare as ak

stock_financial_hk_analysis_indicator_em_df = ak.stock_financial_hk_analysis_indicator_em(symbol="00700", indicator="年度")
print(stock_financial_hk_analysis_indicator_em_df)
```

数据示例

```
   SECUCODE SECURITY_CODE SECURITY_NAME_ABBR  ... FISCAL_YEAR CURRENCY IS_CNY_CODE
0  00700.HK         00700               腾讯控股  ...       12-31      HKD           0
1  00700.HK         00700               腾讯控股  ...       12-31      HKD           0
2  00700.HK         00700               腾讯控股  ...       12-31      HKD           0
3  00700.HK         00700               腾讯控股  ...       12-31      HKD           0
4  00700.HK         00700               腾讯控股  ...       12-31      HKD           0
5  00700.HK         00700               腾讯控股  ...       12-31      HKD           0
6  00700.HK         00700               腾讯控股  ...       12-31      HKD           0
7  00700.HK         00700               腾讯控股  ...       12-31      HKD           0
8  00700.HK         00700               腾讯控股  ...       12-31      HKD           0
[9 rows x 36 columns]
```
