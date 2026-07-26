---
title: "index_bloomberg_billionaires_hist - 历史彭博亿万富豪指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, others, parameters, returns, example]
sources: [raw/data-dictionary/others/others.md]
confidence: high
---
# index_bloomberg_billionaires_hist

- 分类: [[others-others|AKShare 另类数据]]
- 主题路径: AKShare 另类数据 > 彭博亿万富豪指数 > 历史彭博亿万富豪指数
- 描述: 按照年份查询彭博亿万富豪指数; 该接口需要使用代理访问
- 目标地址: https://stats.areppim.com/stats/links_billionairexlists.htm
- 限量: 单次返回当年所有数据彭博亿万富豪排名数据
- 来源页面: https://akshare.akfamily.xyz/data/others/others.html

## 相关

- [[others-others|AKShare 另类数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 历史彭博亿万富豪指数

接口: index_bloomberg_billionaires_hist

目标地址: https://stats.areppim.com/stats/links_billionairexlists.htm

描述: 按照年份查询彭博亿万富豪指数; 该接口需要使用代理访问

限量: 单次返回当年所有数据彭博亿万富豪排名数据

输入参数

| 名称   | 类型  | 描述                                                   |
|------|-----|------------------------------------------------------|
| year | str | year="2021"; choice of {"2021", "2019", "2018", ...} |

输出参数

| 名称              | 类型  | 描述              |
|-----------------|-----|-----------------|
| rank            | str | Rank            |
| name            | str | Name            |
| total_net_worth | str | Total net worth |
| last_change     | str | $ Last change   |
| YTD_change      | str | $ YTD change    |
| country         | str | Country         |
| industry        | str | Industry        |
| age             | str | Age             |

接口示例

```python
import akshare as ak

index_bloomberg_billionaires_hist_df=ak.index_bloomberg_billionaires_hist(year='2019')
print(index_bloomberg_billionaires_hist_df)
```

数据示例

```
    rank                        name  ...             country     industry
0      1                  Jeff Bezos  ...       United States   Technology
1      2                  Bill Gates  ...       United States   Technology
2      3             Mark Zuckerberg  ...       United States   Technology
3      4             Bernard Arnault  ...              France     Consumer
4      5               Steve Ballmer  ...       United States   Technology
..   ...                         ...  ...                 ...          ...
494  496                 Ira Rennert  ...       United States  Commodities
495  497  Traudl Engelhorn-Vechiatto  ...         Switzerland  Diversified
496  498            Sergey Galitskiy  ...  Russian Federation       Retail
497  499                  Xu Jingren  ...               China  Health Care
498  500                Shi Yonghong  ...           Singapore     Consumer
```
