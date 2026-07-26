---
title: "stock_sector_fund_flow_hist - 行业历史资金流"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_sector_fund_flow_hist

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 资金流向 > 东方财富 > 行业历史资金流
- 描述: 东方财富网-数据中心-资金流向-行业资金流-行业历史资金流
- 目标地址: https://data.eastmoney.com/bkzj/BK1034.html
- 限量: 单次获取指定行业的行业历史资金流数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 行业历史资金流

接口: stock_sector_fund_flow_hist

目标地址: https://data.eastmoney.com/bkzj/BK1034.html

描述: 东方财富网-数据中心-资金流向-行业资金流-行业历史资金流

限量: 单次获取指定行业的行业历史资金流数据

输入参数

| 名称     | 类型  | 描述            |
|--------|-----|---------------|
| symbol | str | symbol="汽车服务" |

输出参数

| 名称         | 类型      | 描述      |
|------------|---------|---------|
| 日期         | object  | 注意单位: % |
| 主力净流入-净额   | float64 | -       |
| 主力净流入-净占比  | float64 | 注意单位: % |
| 超大单净流入-净额  | float64 | -       |
| 超大单净流入-净占比 | float64 | 注意单位: % |
| 大单净流入-净额   | float64 | -       |
| 大单净流入-净占比  | float64 | 注意单位: % |
| 中单净流入-净额   | float64 | -       |
| 中单净流入-净占比  | float64 | 注意单位: % |
| 小单净流入-净额   | float64 | -       |
| 小单净流入-净占比  | float64 | 注意单位: % |

接口示例

```python
import akshare as ak

stock_sector_fund_flow_hist_df = ak.stock_sector_fund_flow_hist(symbol="汽车服务")
print(stock_sector_fund_flow_hist_df)
```

数据示例

```
      日期    主力净流入-净额  主力净流入-净占比  ...  中单净流入-净占比 小单净流入-净额  小单净流入-净占比
0    2024-08-20 -54471010.0     -10.09  ...       2.28  37641239.0       6.97
1    2024-08-21  10178690.0       1.91  ...      -0.79 -10308872.0      -1.94
2    2024-08-22 -44754582.0      -8.39  ...       1.49  32534534.0       6.10
3    2024-08-23 -27649222.0      -6.52  ...      -0.86  29341810.0       6.92
4    2024-08-26 -42767862.0     -10.11  ...      -2.63  53748702.0      12.70
..          ...         ...        ...  ...        ...         ...        ...
116  2025-02-18 -93269892.0      -6.56  ...       1.78  58625760.0       4.12
117  2025-02-19  21681328.0       1.51  ...       1.97 -32209872.0      -2.25
118  2025-02-20  11260284.0       0.89  ...       0.43  -6260576.0      -0.50
119  2025-02-21 -81443762.0      -5.66  ...       3.29  47217792.0       3.28
120  2025-02-24  20329299.0       1.44  ...       1.47 -58079088.0      -4.12
[121 rows x 11 columns]
```
