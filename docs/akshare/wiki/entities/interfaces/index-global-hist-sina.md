---
title: "index_global_hist_sina - 全球指数-历史行情数据-新浪"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# index_global_hist_sina

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 全球指数 > 全球指数-历史行情数据-新浪
- 描述: 新浪财经-行情中心-环球市场-历史行情
- 目标地址: https://finance.sina.com.cn/stock/globalindex/quotes/UKX
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 全球指数-历史行情数据-新浪

接口: index_global_hist_sina

目标地址: https://finance.sina.com.cn/stock/globalindex/quotes/UKX

描述: 新浪财经-行情中心-环球市场-历史行情

限量：单次返回最近的 1000 条数据

输入参数

| 名称     | 类型  | 描述                                                    |
|--------|-----|-------------------------------------------------------|
| symbol | str | symbol="瑞士股票指数"; 可以通过 ak.index_global_name_table() 获取 |

输出参数

| 名称     | 类型      | 描述 |
|--------|---------|----|
| date   | object  | -  |
| open   | object  | -  |
| high   | object  | -  |
| low    | float64 | -  |
| close  | float64 | -  |
| volume | float64 | -  |

接口示例

```python
import akshare as ak

index_global_hist_sina_df = ak.index_global_hist_sina(symbol="瑞士股票指数")
print(index_global_hist_sina_df)
```

数据示例

```
           date      open      high       low     close    volume
0    2021-03-22  10931.56  11048.58  10928.34  11048.58  51627000
1    2021-03-23  11030.89  11118.33  11016.21  11098.66  48422000
2    2021-03-24  11048.59  11106.94  11033.37  11063.87  43812000
3    2021-03-25  11026.65  11102.78  11017.32  11098.81  52086000
4    2021-03-26  11113.90  11143.86  11091.63  11116.81  46264000
..          ...       ...       ...       ...       ...       ...
995  2025-03-03  13032.86  13199.05  12956.84  13166.68  30859832
996  2025-03-04  13099.49  13146.92  12991.81  13006.74  38551012
997  2025-03-05  13081.21  13161.90  13066.22  13112.75  38270072
998  2025-03-06  13090.73  13105.02  12928.22  13056.91  36533732
999  2025-03-07  12959.80  12965.30  12888.30  12904.70   4468362
[1000 rows x 6 columns]
```
