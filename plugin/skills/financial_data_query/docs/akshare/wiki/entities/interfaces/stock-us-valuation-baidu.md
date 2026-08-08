---
title: "stock_us_valuation_baidu - 美股估值指标"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_us_valuation_baidu

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 美股估值指标
- 描述: 百度股市通-美股-财务报表-估值数据
- 目标地址: https://gushitong.baidu.com/stock/us-NVDA
- 限量: 单次获取指定 symbol 的指定 indicator 的特定 period 的历史数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 美股估值指标

接口: stock_us_valuation_baidu

目标地址: https://gushitong.baidu.com/stock/us-NVDA

描述: 百度股市通-美股-财务报表-估值数据

限量: 单次获取指定 symbol 的指定 indicator 的特定 period 的历史数据

输入参数

| 名称        | 类型  | 描述                                                                     |
|-----------|-----|------------------------------------------------------------------------|
| symbol    | str | symbol="NVDA"; 美股代码                                                    |
| indicator | str | indicator="总市值"; choice of {"总市值", "市盈率(TTM)", "市盈率(静)", "市净率", "市现率"} |
| period    | str | period="近一年"; choice of {"近一年", "近三年", "全部"}                           |

输出参数

| 名称    | 类型      | 描述  |
|-------|---------|-----|
| date  | object  | -   |
| value | float64 | -   |

接口示例

```python
import akshare as ak

stock_us_valuation_baidu_df = ak.stock_us_valuation_baidu(symbol="NVDA", indicator="总市值", period="近一年")
print(stock_us_valuation_baidu_df)
```

数据示例

```
           date     value
0    2024-12-24  34339.88
1    2024-12-26  34268.86
2    2024-12-27  33553.75
3    2024-12-30  33671.30
4    2024-12-31  32887.62
..          ...       ...
245  2025-12-17  41538.42
246  2025-12-18  42316.02
247  2025-12-19  43980.57
248  2025-12-22  44636.67
249  2025-12-23  45978.03
[250 rows x 2 columns]
```
