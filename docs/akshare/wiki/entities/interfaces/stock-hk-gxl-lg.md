---
title: "stock_hk_gxl_lg - 恒生指数股息率"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_hk_gxl_lg

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 恒生指数股息率
- 描述: 乐咕乐股-股息率-恒生指数股息率
- 目标地址: https://legulegu.com/stockdata/market/hk/dv/hsi
- 限量: 单次获取所有月度历史数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 恒生指数股息率

接口: stock_hk_gxl_lg

目标地址: https://legulegu.com/stockdata/market/hk/dv/hsi

描述: 乐咕乐股-股息率-恒生指数股息率

限量: 单次获取所有月度历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称  | 类型      | 描述  |
|-----|---------|-----|
| 日期  | object  | -   |
| 股息率 | float64 | -   |

接口示例

```python
import akshare as ak

stock_hk_gxl_lg_df = ak.stock_hk_gxl_lg()
print(stock_hk_gxl_lg_df)
```

数据示例

```
          日期   股息率
0    1973-05-31  0.00
1    1973-06-30  0.00
2    1973-07-31  0.00
3    1973-08-31  0.00
4    1973-09-30  0.00
..          ...   ...
606  2023-11-30  4.10
607  2023-12-31  3.97
608  2024-01-31  4.37
609  2024-02-28  4.45
610  2024-03-31  4.34
[611 rows x 2 columns]
```
