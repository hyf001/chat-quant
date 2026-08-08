---
title: "index_hog_spot_price - 生猪市场价格指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, futures, parameters, returns, example]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# index_hog_spot_price

- 分类: [[futures-futures|AKShare 期货数据]]
- 主题路径: 此处的合约需要是近期的合约, 否则会报错 > 生猪市场价格指数
- 描述: 行情宝-生猪市场价格指数
- 目标地址: https://hqb.nxin.com/pigindex/index.shtml
- 限量: 单次返回所有数据
- 来源页面: https://akshare.akfamily.xyz/data/futures/futures.html

## 相关

- [[futures-futures|AKShare 期货数据]]
- [[_meta/topic-map]]

## 源文摘录

### 生猪市场价格指数

接口: index_hog_spot_price

目标地址: https://hqb.nxin.com/pigindex/index.shtml

描述: 行情宝-生猪市场价格指数

限量: 单次返回所有数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称     | 类型      | 描述         |
|--------|---------|------------|
| 日期     | object  | -          |
| 指数     | float64 | -          |
| 4个月均线  | float64 | -          |
| 6个月均线  | float64 | -          |
| 12个月均线 | float64 | -          |
| 预售均价   | float64 | 注意单位: 元/公斤 |
| 成交均价   | float64 | 注意单位: 元/公斤 |
| 成交均重   | int64   | 注意单位: kg   |

接口示例

```python
import akshare as ak

index_hog_spot_price_df = ak.index_hog_spot_price()
print(index_hog_spot_price_df)
```

数据示例

```
       日期        指数   4个月均线   6个月均线  12个月均线  预售均价   成交均价  成交均重
0    2015-01-05   92.88     NaN     NaN     NaN   0.00  13.49     0
1    2015-01-12   92.82     NaN     NaN     NaN   0.00  13.48     0
2    2015-01-19   93.29     NaN     NaN     NaN   0.00  13.55     0
3    2015-01-26   93.48     NaN     NaN     NaN   0.00  13.57     0
4    2015-02-02   92.12     NaN     NaN     NaN   0.00  13.38     0
..          ...     ...     ...     ...     ...    ...    ...   ...
460  2024-02-05  107.08  100.72  105.82  103.19  16.06  15.55   116
461  2024-02-26   95.14   99.63  103.68  103.25  15.64  13.81   122
462  2024-03-04   96.85   99.31  102.08  103.02  15.60  14.06   120
463  2024-03-11   98.45   99.10  101.32  102.79  15.69  14.30   122
464  2024-03-18  100.62   99.07  100.69  102.65  15.76  14.61   125
[465 rows x 8 columns]
```
