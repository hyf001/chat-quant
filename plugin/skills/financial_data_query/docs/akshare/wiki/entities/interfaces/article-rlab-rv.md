---
title: "article_rlab_rv - Risk-Lab"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, article, parameters, returns, example]
sources: [raw/data-dictionary/article/article.md]
confidence: high
---
# article_rlab_rv

- 分类: [[article-article|AKShare 波动率数据]]
- 主题路径: AKShare 波动率数据 > 已实现波动率数据 > Risk-Lab
- 描述: 获取 Risk-Lab 已实现波动率数据
- 目标地址: https://dachxiu.chicagobooth.edu/
- 限量: 单次返回某个指数所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/article/article.html

## 相关

- [[article-article|AKShare 波动率数据]]
- [[_meta/topic-map]]

## 源文摘录

#### Risk-Lab

接口: article_rlab_rv

目标地址: https://dachxiu.chicagobooth.edu/

描述: 获取 Risk-Lab 已实现波动率数据

限量: 单次返回某个指数所有历史数据

输入参数

| 名称     | 类型  | 描述                                           |
|--------|-----|----------------------------------------------|
| symbol | str | symbol="39693", 某个具体指数 help(article_rlab_rv) |

输出参数

Risk-Lab-已实现波动率数据

| 名称    | 类型                | 描述  |
|-------|-------------------|-----|
| index | datetime.datetime | 日期  |
| data  | float             | 数据  |

接口示例

```python
import akshare as ak

article_rlab_rv_df = ak.article_rlab_rv(symbol="39693")
print(article_rlab_rv_df)
```

数据示例

```
1996-01-02    0.000000
1996-01-04    0.000000
1996-01-05    0.000000
1996-01-09    0.000000
1996-01-10    0.000000
                ...
2019-11-04    0.175107
2019-11-05    0.185112
2019-11-06    0.210373
2019-11-07    0.240808
2019-11-08    0.199549
```
