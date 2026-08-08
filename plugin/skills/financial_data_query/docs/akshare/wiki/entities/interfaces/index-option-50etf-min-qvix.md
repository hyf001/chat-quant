---
title: "index_option_50etf_min_qvix - 50ETF 期权波动率指数-分时"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# index_option_50etf_min_qvix

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 期权波动率指数 > 50ETF 期权波动率指数-分时
- 描述: 50ETF 期权波动率指数-分时
- 目标地址: http://1.optbbs.com/s/vix.shtml?50ETF
- 限量: 单次返回最近交易日的分时数据
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 50ETF 期权波动率指数-分时

接口: index_option_50etf_min_qvix

目标地址: http://1.optbbs.com/s/vix.shtml?50ETF

描述: 50ETF 期权波动率指数-分时

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

index_option_50etf_min_qvix_df = ak.index_option_50etf_min_qvix()
print(index_option_50etf_min_qvix_df)
```

数据示例

```
         time   qvix
0     9:30:00  16.06
1     9:31:11  16.52
2     9:32:11  16.52
3     9:33:11  16.70
4     9:34:11  16.64
..        ...    ...
234  14:53:19  18.14
235  14:54:19  18.06
236  14:55:19  17.99
237  14:56:19  17.95
238  15:00:00    NaN
[239 rows x 2 columns]
```
