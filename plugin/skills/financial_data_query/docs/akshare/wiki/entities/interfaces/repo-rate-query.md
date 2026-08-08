---
title: "repo_rate_query - 回购定盘利率-近期"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, interest-rate, parameters, returns, example]
sources: [raw/data-dictionary/interest_rate/interest_rate.md]
confidence: high
---
# repo_rate_query

- 分类: [[interest-rate-interest-rate|AKShare 利率数据]]
- 主题路径: AKShare 利率数据 > 回购定盘利率-近期
- 描述: 回购定盘利率数据
- 目标地址: https://www.chinamoney.com.cn/chinese/bkfrr/
- 限量: 单次返回指定 symbol 的近期数据
- 来源页面: https://akshare.akfamily.xyz/data/interest_rate/interest_rate.html

## 相关

- [[interest-rate-interest-rate|AKShare 利率数据]]
- [[_meta/topic-map]]

## 源文摘录

### 回购定盘利率-近期

接口: repo_rate_query

目标地址: https://www.chinamoney.com.cn/chinese/bkfrr/

描述: 回购定盘利率数据

限量: 单次返回指定 symbol 的近期数据

输入参数

| 名称     | 类型  | 描述                                                 |
|--------|-----|----------------------------------------------------|
| symbol | str | symbol="回购定盘利率"; choice of {"回购定盘利率", "银银间回购定盘利率"} |

输出参数

| 名称     | 类型      | 描述      |
|--------|---------|---------|
| date   | object  | -       |
| FR001  | float64 | 注意单位: % |
| FR007  | float64 | 注意单位: % |
| FR014  | float64 | 注意单位: % |

接口示例

```python
import akshare as ak

repo_rate_query_df = ak.repo_rate_query(symbol="回购定盘利率")
print(repo_rate_query_df)
```

数据示例

```
           date   FR001  FR007  FR014
0    2021-01-19  2.3000   2.46   2.55
1    2021-01-20  2.5000   2.65   2.80
2    2021-01-21  2.6500   2.60   2.70
3    2021-01-22  2.5500   2.40   2.70
4    2021-01-25  2.5000   2.50   2.78
..          ...     ...    ...    ...
746  2024-01-15  1.8300   2.25   2.20
747  2024-01-16  1.9528   2.25   2.38
748  2024-01-17  2.0107   2.30   2.55
749  2024-01-18  1.8800   2.20   2.30
750  2024-01-19  1.8600   2.15   2.40
[751 rows x 4 columns]
```
