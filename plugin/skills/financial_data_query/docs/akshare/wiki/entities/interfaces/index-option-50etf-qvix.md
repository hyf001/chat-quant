---
title: "index_option_50etf_qvix - 50ETF 期权波动率指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# index_option_50etf_qvix

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 期权波动率指数 > 50ETF 期权波动率指数
- 描述: 50ETF 期权波动率指数 QVIX; 又称中国版的恐慌指数
- 目标地址: http://1.optbbs.com/s/vix.shtml?50ETF
- 限量: 单次返回所有数据
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 50ETF 期权波动率指数

接口: index_option_50etf_qvix

目标地址: http://1.optbbs.com/s/vix.shtml?50ETF

描述: 50ETF 期权波动率指数 QVIX; 又称中国版的恐慌指数

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

index_option_50etf_qvix_df = ak.index_option_50etf_qvix()
print(index_option_50etf_qvix_df)
```

数据示例

```
            date       open       high        low  close
0     2015-02-09  28.800000  28.756878  27.829555  28.63
1     2015-02-10  28.630000  29.435024  28.499700  28.75
2     2015-02-11  26.470710  26.470710  26.176691  26.44
3     2015-02-12  26.389094  26.389094  25.773367  25.80
4     2015-02-13  24.286958  24.286958  22.810473  23.41
          ...        ...        ...        ...    ...
2108  2023-10-13  15.290000  15.780000  15.180000  15.61
2109  2023-10-16  16.270000  16.720000  16.060000  16.41
2110  2023-10-17  16.470000  16.580000  15.800000  15.80
2111  2023-10-18  15.810000  16.110000  15.450000  15.70
2112  2023-10-19  16.060000  18.280000  16.060000  17.95
[2113 rows x 5 columns]
```
