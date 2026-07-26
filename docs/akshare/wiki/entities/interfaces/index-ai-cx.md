---
title: "index_ai_cx - AI策略指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# index_ai_cx

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 财新指数 > AI策略指数
- 描述: 财新指数-AI策略指数
- 目标地址: https://yun.ccxe.com.cn/indices/ai
- 限量: 该接口返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

#### AI策略指数

接口: index_ai_cx

目标地址: https://yun.ccxe.com.cn/indices/ai

描述: 财新指数-AI策略指数

限量: 该接口返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称     | 类型      | 描述      |
|--------|---------|---------|
| 日期     | object  | -       |
| AI策略指数 | float64 | -       |
| 变化幅度   | float64 | 注意单位: % |

接口示例

```python
import akshare as ak

index_ai_cx_df = ak.index_ai_cx()
print(index_ai_cx_df)
```

数据示例

```
      日期      AI策略指数      变化幅度
0    2020-12-31  100.002000  0.000000
1    2021-01-04  102.925670  2.923611
2    2021-01-05  105.666833  2.663245
3    2021-01-06  106.429747  0.722000
4    2021-01-07  108.591207  2.030880
..          ...         ...       ...
823  2024-05-29  135.800485  0.101018
824  2024-05-30  134.659844 -0.839939
825  2024-05-31  134.193064 -0.346637
826  2024-06-03  133.985240 -0.154869
827  2024-06-04  135.034790  0.783333
[828 rows x 3 columns]
```
