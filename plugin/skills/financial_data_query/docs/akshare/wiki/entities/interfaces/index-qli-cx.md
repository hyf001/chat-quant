---
title: "index_qli_cx - 高质量因子"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# index_qli_cx

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 财新指数 > 高质量因子
- 描述: 财新指数-高质量因子
- 目标地址: https://yun.ccxe.com.cn/indices/qli
- 限量: 该接口返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 高质量因子

接口: index_qli_cx

目标地址: https://yun.ccxe.com.cn/indices/qli

描述: 财新指数-高质量因子

限量: 该接口返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称      | 类型      | 描述      |
|---------|---------|---------|
| 日期      | object  | -       |
| 高质量因子指数 | float64 | -       |
| 变化幅度    | float64 | 注意单位: % |

接口示例

```python
import akshare as ak

index_qli_cx_df = ak.index_qli_cx()
print(index_qli_cx_df)
```

数据示例

```
        日期     高质量因子指数   变化幅度
0     2018-05-02  100.015000  0.000000
1     2018-05-03  100.336541  0.321493
2     2018-05-04  101.048384  0.709455
3     2018-05-07  101.663083  0.608322
4     2018-05-08  103.734574  2.037603
...          ...         ...       ...
1475  2024-05-29  142.498375  0.345091
1476  2024-05-30  141.457371 -0.730537
1477  2024-05-31  140.915933 -0.382757
1478  2024-06-03  141.537175  0.440860
1479  2024-06-04  143.046574  1.066433
[1480 rows x 3 columns]
```
