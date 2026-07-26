---
title: "broker_net_money - 席位净持仓保证金数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/broker.md]
confidence: high
---
# broker_net_money

- 分类: [[qhkc-broker|席位]]
- 主题路径: 席位 > 席位净持仓保证金数据
- 描述: 席位净持仓保证金数据接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/broker.html

## 相关

- [[qhkc-broker|席位]]
- [[_meta/topic-map]]

## 源文摘录

## 席位净持仓保证金数据

### 接口名称

broker_net_money

### 接口描述

席位净持仓保证金数据接口

### 请求参数

| 参数名    | 说明   | 举例         |
|:-------|:-----|------------|
| broker | 席位   | 永安期货       |
| date   | 查询日期 | 2018-08-08 |

### 返回参数

| 参数名    | 类型     | 说明                     |
|:-------|:-------|------------------------|
| symbol | string | 品种编码                   |
| value  | float  | 净持仓保证金，正数为净多，负数为净空，单位元 |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
broker_net_money_df = pro.broker_net_money(broker="永安期货", date="2018-08-08")
print(broker_net_money_df)
```

### 返回示例

```
   symbol      value
0      RU -126518247
1      IC  -73082712
2      CF  -59002530
3       L  -38443465
4       C  -37922269
5      JM  -27913493
6       P  -25204953
7      AG  -24969327
8       V  -21574018
9      BU  -17898408
10      I  -17824820
11     SR  -17713710
12     FG  -14825526
13     MA  -14759199
14      T   -9789992
15     HC   -6135685
16     SF   -3881907
17     RM   -3477467
18      Y   -2180168
19     WH   -1296880
20     FU   -1029732
21      B    -313600
22     PM     -17340
23     CS     581311
24      A    2531008
25     SN    2557678
26     IH    5062392
27     JD    5589189
28     AP    8217133
29     IF    8381628
30     SM    8913145
31     ZC    9053171
32     CU    9817385
33     ZN   18126276
34     AU   20786100
35     PB   24281126
36     NI   28679642
37     AL   28819661
38     TF   49680256
39     PP   63960902
40     OI   79174077
41     TA   98338372
42      M  158924122
43      J  199714680
44     RB  218919026
```
