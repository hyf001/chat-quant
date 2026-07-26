---
title: "index_option_100etf_qvix - 深证100ETF 期权波动率指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# index_option_100etf_qvix

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 期权波动率指数 > 深证100ETF 期权波动率指数
- 描述: 深证100ETF 期权波动率指数 QVIX
- 目标地址: http://1.optbbs.com/s/vix.shtml?100ETF
- 限量: 单次返回所有数据
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 深证100ETF 期权波动率指数

接口: index_option_100etf_qvix

目标地址: http://1.optbbs.com/s/vix.shtml?100ETF

描述: 深证100ETF 期权波动率指数 QVIX

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

index_option_100etf_qvix_df = ak.index_option_100etf_qvix()
print(index_option_100etf_qvix_df)
```

数据示例

```
            date   open   high    low  close
0     2015-02-09    NaN    NaN    NaN    NaN
1     2015-02-10    NaN    NaN    NaN    NaN
2     2015-02-11    NaN    NaN    NaN    NaN
3     2015-02-12    NaN    NaN    NaN    NaN
4     2015-02-13    NaN    NaN    NaN    NaN
...          ...    ...    ...    ...    ...
2393  2024-12-24  25.46  25.46  24.05  24.21
2394  2024-12-25  24.49  24.61  23.72  24.01
2395  2024-12-26  24.40  24.40  22.18  22.46
2396  2024-12-27  22.81  23.10  22.04  22.05
2397  2024-12-30  23.15  23.15  22.23  22.44
[2398 rows x 5 columns]
```
