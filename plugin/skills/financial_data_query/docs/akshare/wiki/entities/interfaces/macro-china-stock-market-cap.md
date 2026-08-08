---
title: "macro_china_stock_market_cap - 全国股票交易统计表"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_stock_market_cap

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 全国股票交易统计表
- 描述: 全国股票交易统计表, 数据区间从 200801 至今, 月度数据
- 目标地址: http://data.eastmoney.com/cjsj/gpjytj.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 全国股票交易统计表

接口: macro_china_stock_market_cap

目标地址: http://data.eastmoney.com/cjsj/gpjytj.html

描述: 全国股票交易统计表, 数据区间从 200801 至今, 月度数据

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称            | 类型      | 描述       |
|---------------|---------|----------|
| 数据日期          | object  | 年度和月份    |
| 发行总股本-上海      | float64 | 注意单位: 亿元 |
| 发行总股本-深圳      | float64 | 注意单位: 亿元 |
| 市价总值-上海       | float64 | 注意单位: 亿元 |
| 市价总值-深圳       | float64 | 注意单位: 亿元 |
| 成交金额-上海       | float64 | 注意单位: 亿元 |
| 成交金额-深圳       | float64 | 注意单位: 亿元 |
| 成交量-上海        | float64 | -        |
| 成交量-深圳        | float64 | -        |
| A股最高综合股价指数-上海 | float64 | -        |
| A股最高综合股价指数-深圳 | float64 | -        |
| A股最低综合股价指数-上海 | float64 | -        |
| A股最低综合股价指数-深圳 | float64 | -        |

接口示例

```python
import akshare as ak

macro_china_stock_market_cap_df = ak.macro_china_stock_market_cap()
print(macro_china_stock_market_cap_df)
```

数据示例

```
          数据日期  发行总股本-上海  ...  A股最低综合股价指数-上海  A股最低综合股价指数-深圳
0    2022年11月份       NaN  ...      2896.7572      2032.0920
1    2022年10月份  47240.00  ...      2885.0894      1974.9663
2    2022年09月份  47205.00  ...      3021.9309      2032.3677
3    2022年08月份  47038.00  ...      3155.1866      2231.3209
4    2022年07月份  46908.00  ...      3226.2315      2284.0597
..         ...       ...  ...            ...            ...
174  2008年05月份  14980.19  ...      3333.9510      1086.0100
175  2008年04月份  14785.95  ...      2990.7880       963.8400
176  2008年03月份  14476.47  ...      3357.2290      1186.6000
177  2008年02月份  14300.84  ...      4123.3050      1385.0400
178  2008年01月份  14198.16  ...      4330.6970      1424.3500
```
