---
title: "broker_total_money - 席位总持仓保证金数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/broker.md]
confidence: high
---
# broker_total_money

- 分类: [[qhkc-broker|席位]]
- 主题路径: 席位 > 席位总持仓保证金数据
- 描述: 席位总持仓保证金数据接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/broker.html

## 相关

- [[qhkc-broker|席位]]
- [[_meta/topic-map]]

## 源文摘录

## 席位总持仓保证金数据

### 接口名称

broker_total_money

### 接口描述

席位总持仓保证金数据接口

### 请求参数

| 参数名    | 说明   | 举例         |
|:-------|:-----|------------|
| broker | 席位   | 永安期货       |
| date   | 查询日期 | 2018-08-08 |

### 返回参数

| 参数名    | 类型     | 说明         |
|:-------|:-------|------------|
| symbol | string | 品种编码       |
| value  | float  | 总持仓保证金，单位元 |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
broker_total_money_df = pro.broker_total_money(broker="永安期货", date="2018-08-08")
print(broker_total_money_df)
```

### 返回示例

```
   symbol      value
0       C   84535414
1       L  100876943
2      CF  348457275
3      RU  441062073
4       V   62613259
5       P   68744951
6      FG   29085142
7      AG   65751126
8      SR  121266350
9      BU  118354280
10     MA  188504328
11     JM   65540875
12      I  173409484
13     RM   30997475
14     HC  165703202
15     SF   21051245
16      Y  180289358
17     IC  355803249
18     FU   49778988
19      T  328004328
20      B     313600
21     WH    1695920
22     PM      17340
23     IH   33529176
24     IF  279349824
25     SN    5680305
26     CS    8618401
27     CU  309904039
28     AP  225718060
29     TF   49680256
30      A   21727647
31     AU   43322325
32     JD   19585812
33     ZN  195664900
34     ZC   66069647
35     SM   13684950
36     NI  280050806
37     PB   36902798
38     AL   34360301
39      J  533383080
40     OI  111939375
41     PP  163976343
42     TA  245508829
43     RB  959491721
44      M  399846143
```
