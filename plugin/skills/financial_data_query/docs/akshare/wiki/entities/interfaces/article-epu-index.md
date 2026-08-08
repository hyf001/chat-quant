---
title: "article_epu_index - 国家和地区指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, article, parameters, returns, example]
sources: [raw/data-dictionary/article/article.md]
confidence: high
---
# article_epu_index

- 分类: [[article-article|AKShare 波动率数据]]
- 主题路径: AKShare 政策不确定性数据 > 国家和地区指数
- 描述: 国家或地区的经济政策不确定性(EPU)数据
- 目标地址: https://www.policyuncertainty.com/index.html
- 限量: 单次返回某个具体国家或地区的所有月度经济政策不确定性数据
- 来源页面: https://akshare.akfamily.xyz/data/article/article.html

## 相关

- [[article-article|AKShare 波动率数据]]
- [[_meta/topic-map]]

## 源文摘录

### 国家和地区指数

接口: article_epu_index

目标地址: https://www.policyuncertainty.com/index.html

描述: 国家或地区的经济政策不确定性(EPU)数据

限量: 单次返回某个具体国家或地区的所有月度经济政策不确定性数据

输入参数

| 名称     | 类型  | 描述                                    |
|--------|-----|---------------------------------------|
| symbol | str | symbol="China"; 按 **国家和地区一览表** 输入相应参数 |

国家和地区一览表

| 英文名词        | 说明              |
|-------------|-----------------|
| Global      |                 |
| Australia   |                 |
| Canada      |                 |
| China       |                 |
| Europe      | 欧洲              |
| Germany     | 欧洲              |
| Hong Kong   |                 |
| Ireland     |                 |
| Japan       |                 |
| Mexico      |                 |
| Russia      |                 |
| Spain       |                 |
| UK          |                 |
| USA         |                 |
| Brazil      |                 |
| Chile       |                 |
| Colombia    | 有两种, 默认第一种(FKT) |
| France      | 欧洲              |
| Greece      |                 |
| India       |                 |
| Italy       | 欧洲              |
| South Korea |                 |
| Netherlands |                 |
| Singapore   |                 |
| Sweden      |                 |

输出参数

| 名称 | 类型 | 描述        |
|----|----|-----------|
| -  | -  | 每个国家或地区不同 |

接口示例

```python
import akshare as ak

article_epu_index_df = ak.article_epu_index(symbol="China")  # 注意单词第一个字母大写
print(article_epu_index_df)
```

数据示例

```
     year  month  China_Policy_Index
0    1995      1          192.911910
1    1995      2          193.987850
2    1995      3           88.227035
3    1995      4          131.034710
4    1995      5          177.096860
..    ...    ...                 ...
342  2023      7          704.566080
343  2023      8          709.881990
344  2023      9          819.746150
345  2023     10          603.739890
346  2023     11          743.397580
[347 rows x 3 columns]
```
