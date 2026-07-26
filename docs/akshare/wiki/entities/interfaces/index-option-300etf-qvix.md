---
title: "index_option_300etf_qvix - 300ETF 期权波动率指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# index_option_300etf_qvix

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 期权波动率指数 > 300ETF 期权波动率指数
- 描述: 300ETF 期权波动率指数 QVIX
- 目标地址: https://1.optbbs.com/s/vix.shtml?300ETF
- 限量: 单次返回所有数据
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 300ETF 期权波动率指数

接口: index_option_300etf_qvix

目标地址: https://1.optbbs.com/s/vix.shtml?300ETF

描述: 300ETF 期权波动率指数 QVIX

限量: 单次返回所有数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称    | 类型      | 描述  |
|-------|---------|-----|
| date  | object  | -   |
| open  | float64 | -   |
| high  | float64 | -   |
| low   | float64 | -   |
| close | float64 | -   |

接口示例

```python
import akshare as ak

index_option_300etf_qvix_df = ak.index_option_300etf_qvix()
print(index_option_300etf_qvix_df)
```

数据示例

```
            date   open   high    low  close
0     2015-02-09    NaN    NaN    NaN    NaN
1     2015-02-10    NaN    NaN    NaN    NaN
2     2015-02-11    NaN    NaN    NaN    NaN
3     2015-02-12    NaN    NaN    NaN    NaN
4     2015-02-13    NaN    NaN    NaN    NaN
          ...    ...    ...    ...    ...
2108  2023-10-13  15.18  15.70  15.00  15.46
2109  2023-10-16  16.06  17.04  15.89  16.67
2110  2023-10-17  16.73  16.96  16.18  16.19
2111  2023-10-18  16.42  16.42  15.92  16.25
2112  2023-10-19  16.59  18.46  16.59  18.06
[2113 rows x 5 columns]
```
