---
title: "broker_net_money_chge - 席位净持仓保证金变化数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/broker.md]
confidence: high
---
# broker_net_money_chge

- 分类: [[qhkc-broker|席位]]
- 主题路径: 席位 > 席位净持仓保证金变化数据
- 描述: 席位净持仓保证金变化数据接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/broker.html

## 相关

- [[qhkc-broker|席位]]
- [[_meta/topic-map]]

## 源文摘录

## 席位净持仓保证金变化数据

### 接口名称

broker_net_money_chge

### 接口描述

席位净持仓保证金变化数据接口

### 请求参数

| 参数名    | 说明   | 举例         |
|:-------|:-----|------------|
| broker | 席位   | 永安期货       |
| date   | 查询日期 | 2018-08-08 |

### 返回参数

| 参数名    | 类型     | 说明                        |
|:-------|:-------|---------------------------|
| symbol | string | 品种编码                      |
| value  | float  | 净持仓保证金变化量，正数为流多，负数为流空，单位元 |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
broker_net_money_chge_df = pro.broker_net_money_chge(broker="永安期货", date="2018-08-08")
print(broker_net_money_chge_df)
```

### 返回示例

```
   symbol        value
0       J -52131000.00
1      ZC -36507715.20
2      TA -28648310.40
3       I -17617080.00
4       C -14430302.50
5      RM  -8928432.00
6      MA  -4566014.60
7      IF  -4448322.00
8      AU  -4361850.00
9       Y  -3736382.00
10     PP  -3677985.00
11     IH  -3081456.00
12     SR  -2878634.00
13     AL  -2866627.75
14      B  -2269088.00
15      P  -2136599.00
16     FU  -1830276.00
17     SM  -1723621.90
18     CF  -1518107.50
19     RU  -1308532.50
20     FG  -1168420.00
21      A   -438953.50
22     CS   -356861.00
23     SN   -236251.40
24     PM         0.00
25     WH     79808.00
26     BU     95480.00
27     PB    167724.00
28     AG    374357.70
29     SF    402589.60
30     AP    980350.80
31     JD   1409305.80
32     OI   1551873.50
33      L   1565850.00
34     CU   3838632.00
35     HC   5459755.20
36     ZN   5643888.00
37      M   8834167.50
38     JM   8908188.00
39     IC  12419352.00
40      V  13557552.50
41     TF  14739000.00
42     NI  21465962.40
43     RB  26149929.30
44      T  28275580.00
```
