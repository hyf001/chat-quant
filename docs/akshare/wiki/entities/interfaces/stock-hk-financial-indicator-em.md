---
title: "stock_hk_financial_indicator_em - 财务指标"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_hk_financial_indicator_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 港股 > 财务指标
- 描述: 东方财富-港股-核心必读-最新指标
- 目标地址: https://emweb.securities.eastmoney.com/PC_HKF10/pages/home/index.html?code=03900&type=web&color=w#/CoreReading
- 限量: 单次返回全部数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 财务指标

接口: stock_hk_financial_indicator_em

目标地址: https://emweb.securities.eastmoney.com/PC_HKF10/pages/home/index.html?code=03900&type=web&color=w#/CoreReading

描述: 东方财富-港股-核心必读-最新指标

限量: 单次返回全部数据

输入参数

| 名称     | 类型  | 描述             |
|--------|-----|----------------|
| symbol | str | symbol="03900" |

输出参数

| 名称             | 类型     | 描述 |
|----------------|--------|----|
| 基本每股收益(元)      | object | -  |
| 每股净资产(元)       | object | -  |
| 法定股本(股)        | object | -  |
| 每手股            | object | -  |
| 每股股息TTM(港元)    | object | -  |
| 派息比率(%)        | object | -  |
| 已发行股本(股)       | object | -  |
| 已发行股本-H股(股)    | int64  | -  |
| 每股经营现金流(元)     | object | -  |
| 股息率TTM(%)      | object | -  |
| 总市值(港元)        | object | -  |
| 港股市值(港元)       | object | -  |
| 营业总收入          | object | -  |
| 营业总收入滚动环比增长(%) | object | -  |
| 销售净利率(%)       | object | -  |
| 净利润            | object | -  |
| 净利润滚动环比增长(%)   | object | -  |
| 股东权益回报率(%)     | object | -  |
| 市盈率            | object | -  |
| 市净率            | object | -  |
| 总资产回报率(%)      | object | -  |

接口示例

```python
import akshare as ak

stock_hk_financial_indicator_em_df = ak.stock_hk_financial_indicator_em(symbol="03900")
print(stock_hk_financial_indicator_em_df)
```

数据示例

```
   基本每股收益(元)   每股净资产(元)      法定股本(股)  每手股  每股股息TTM(港元)   派息比率(%)    已发行股本(股)  ...  销售净利率(%)        净利润  净利润滚动环比增长(%)  股东权益回报率(%)        市盈率       市净率  总资产回报率(%)
0       0.08  14.006448  10000000000  500        0.328 -322.1807  2539598690  ...  2.270029  209907000   -114.943944    0.583899 -87.240653  0.640675   0.040922
[1 rows x 21 columns]
```
