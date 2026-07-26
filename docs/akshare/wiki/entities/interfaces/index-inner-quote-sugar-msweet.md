---
title: "index_inner_quote_sugar_msweet - 配额内进口糖估算指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# index_inner_quote_sugar_msweet

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 配额内进口糖估算指数
- 描述: 沐甜科技数据中心-配额内进口糖估算指数
- 目标地址: http://www.msweet.com.cn/mtkj/sjzx13/index.html
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

### 配额内进口糖估算指数

接口: index_inner_quote_sugar_msweet

目标地址: http://www.msweet.com.cn/mtkj/sjzx13/index.html

描述: 沐甜科技数据中心-配额内进口糖估算指数

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称     | 类型      | 描述  |
|--------|---------|-----|
| 日期     | object  | -   |
| 利润空间   | float64 | -   |
| 泰国糖    | float64 | -   |
| 泰国MA5  | float64 | -   |
| 巴西MA5  | float64 | -   |
| 利润MA5  | float64 | -   |
| 巴西MA10 | float64 | -   |
| 巴西糖    | float64 | -   |
| 柳州现货价  | float64 | -   |
| 广州现货价  | float64 | -   |
| 泰国MA10 | float64 | -   |
| 利润MA30 | float64 | -   |
| 利润MA10 | float64 | -   |

接口示例

```python
import akshare as ak

index_inner_quote_sugar_msweet_df = ak.index_inner_quote_sugar_msweet()
print(index_inner_quote_sugar_msweet_df)
```

数据示例

```
      日期      利润空间      泰国糖   泰国MA5  ...  广州现货价  泰国MA10      利润MA30  利润MA10
0     2010-11-01 -1240.220  8913.09     NaN  ...   7400     NaN         NaN     NaN
1     2010-11-02 -1247.110  9038.92     NaN  ...   7500     NaN         NaN     NaN
2     2010-11-03 -1226.750  9043.47     NaN  ...   7500     NaN         NaN     NaN
3     2010-11-04 -1544.135  9359.97     NaN  ...   7500     NaN         NaN     NaN
4     2010-11-05 -1560.100  9375.66     NaN  ...   7500     NaN         NaN     NaN
          ...       ...      ...     ...  ...    ...     ...         ...     ...
2881  2023-01-17   611.500  5140.00  5139.2  ...   5785  5207.4  332.383333  581.95
2882  2023-01-18   690.500  5071.00  5142.2  ...   5785  5179.9  351.883333  603.45
2883  2023-01-19   718.500  5036.00  5114.4  ...   5785  5153.9  374.000000  624.70
2884  2023-01-30   526.500  5336.00  5079.8  ...   5875  5129.7  395.450000  642.20
2885  2023-01-31   429.500  5456.00  5123.8  ...   5910  5140.7  410.283333  636.70
[2886 rows x 13 columns]
```
