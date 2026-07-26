---
title: "variety_net_money_chge - 合约净持仓保证金变化数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/commodity.md]
confidence: high
---
# variety_net_money_chge

- 分类: [[qhkc-commodity|商品]]
- 主题路径: 商品 > 合约净持仓保证金变化数据
- 描述: 合约净持仓保证金变化数据接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/commodity.html

## 相关

- [[qhkc-commodity|商品]]
- [[_meta/topic-map]]

## 源文摘录

## 合约净持仓保证金变化数据

### 接口名称

variety_net_money_chge

### 接口描述

合约净持仓保证金变化数据接口

### 请求参数

| 参数名  | 说明     | 举例         |
|:-----|:-------|------------|
| code | 具体合约代号 | rb1810     |
| date | 查询日期   | 2018-08-08 |

### 返回参数

| 参数名    | 类型     | 说明                      |
|:-------|:-------|-------------------------|
| broker | string | 席位                      |
| value  | float  | 沉淀资金变化量，正数为向多，负数为向空，单位元 |

### 示例代码

```python
from akshare import pro_api

pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
variety_net_money_chge_df = pro.variety_net_money_chge(code="rb1810", date="2018-08-08")
print(variety_net_money_chge_df)
```

### 返回示例

```
   broker     value
0    国海良时 -59991336
1    方正中期 -45593568
2    国泰君安 -10364256
3    瑞达期货  -7979256
4    南华期货  -7742664
5    东海期货  -6521544
6    中大期货  -5998752
7    一德期货  -5258448
8    光大期货  -3152016
9    浙商期货  -3117672
10   华安期货         0
11   鲁证期货    183168
12   东证期货   1885104
13   广发期货   1911816
14   中辉期货   2110248
15   徽商期货   2316312
16   中信建投   2385000
17   银河期货   5449248
18   国投安信   7036704
19   海通期货   9528552
20   申银万国   9982656
21   永安期货  15821136
22   华泰期货  16198920
23   中信期货  18721296
24   兴证期货  18748008
25   中国国际  48737952
26   大地期货  55812816
```
