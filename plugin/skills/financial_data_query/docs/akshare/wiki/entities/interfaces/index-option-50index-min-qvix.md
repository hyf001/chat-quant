---
title: "index_option_50index_min_qvix - 上证50股指 期权波动率指数-分时"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# index_option_50index_min_qvix

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 期权波动率指数 > 上证50股指 期权波动率指数-分时
- 描述: 上证50股指 期权波动率指数-分时
- 目标地址: http://1.optbbs.com/s/vix.shtml?50index
- 限量: 单次返回最近交易日的分时数据
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 上证50股指 期权波动率指数-分时

接口: index_option_50index_min_qvix

目标地址: http://1.optbbs.com/s/vix.shtml?50index

描述: 上证50股指 期权波动率指数-分时

限量: 单次返回最近交易日的分时数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称    | 类型      | 描述  |
|-------|---------|-----|
| time  | object  | -   |
| qvix  | float64 | -   |

接口示例

```python
import akshare as ak

index_option_50index_min_qvix_df = ak.index_option_50index_min_qvix()
print(index_option_50index_min_qvix_df)
```

数据示例

```
         time   qvix
0     9:30:00  20.05
1     9:31:51  20.24
2     9:32:51  20.25
3     9:33:51  20.15
4     9:34:51  20.13
..        ...    ...
234  14:53:59  19.61
235  14:54:59  19.73
236  14:55:59  19.70
237  14:56:59  19.62
238  15:00:59  19.57
[239 rows x 2 columns]
```
