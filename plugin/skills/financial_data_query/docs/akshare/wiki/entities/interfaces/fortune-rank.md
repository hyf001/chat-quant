---
title: "fortune_rank - 财富排行榜-中文"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, others, parameters, returns, example]
sources: [raw/data-dictionary/others/others.md]
confidence: high
---
# fortune_rank

- 分类: [[others-others|AKShare 另类数据]]
- 主题路径: AKShare 另类数据 > 财富排行榜-中文
- 描述: 指定年份财富世界 500 强公司排行榜
- 目标地址: https://www.fortunechina.com/fortune500/node_65.htm
- 限量: 单次返回某一个年份的所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/others/others.html

## 相关

- [[others-others|AKShare 另类数据]]
- [[_meta/topic-map]]

## 源文摘录

### 财富排行榜-中文

接口: fortune_rank

目标地址: https://www.fortunechina.com/fortune500/node_65.htm

描述: 指定年份财富世界 500 强公司排行榜

限量: 单次返回某一个年份的所有历史数据

输入参数

| 名称   | 类型  | 描述          |
|------|-----|-------------|
| year | str | year="2023" |

输出参数

| 名称  | 类型  | 描述                |
|-----|-----|-------------------|
| -   | -   | 以当年的数据为准, 输出的字段不一 |

接口示例

```python
import akshare as ak

fortune_rank_df = ak.fortune_rank(year="2023")
print(fortune_rank_df)
```

数据示例

```
      排名                                         公司名称(中文)  ...     国家  关键数据
0      1                                       沃尔玛（WALMART)  ...     美国     +
1      2                               沙特阿美公司（SAUDI ARAMCO)  ...  沙特阿拉伯     +
2      3                               国家电网有限公司（STATE GRID)  ...     中国     +
3      4                                    亚马逊（AMAZON.COM)  ...     美国     +
4      5            中国石油天然气集团有限公司（CHINA NATIONAL PETROLEUM)  ...     中国     +
..   ...                                                ...  ...    ...   ...
495  496                     三星人寿保险（SAMSUNG LIFE INSURANCE)  ...     韩国     +
496  497                  住友生命保险公司（SUMITOMO LIFE INSURANCE)  ...     日本     +
497  498                                   CarMax公司（CARMAX)  ...     美国     +
498  499         日本三菱重工业股份有限公司（MITSUBISHI HEAVY INDUSTRIES)  ...     日本     +
499  500  新疆广汇实业投资（集团）有限责任公司（XINJIANG GUANGHUI INDUSTRY ...  ...     中国     +
[500 rows x 6 columns]
```
