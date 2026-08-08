---
title: "broker_profit - 席位的商品盈亏数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/broker.md]
confidence: high
---
# broker_profit

- 分类: [[qhkc-broker|席位]]
- 主题路径: 席位 > 席位的商品盈亏数据
- 描述: 席位的商品盈亏数据接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/broker.html

## 相关

- [[qhkc-broker|席位]]
- [[_meta/topic-map]]

## 源文摘录

## 席位的商品盈亏数据

### 接口名称

broker_profit

### 接口描述

席位的商品盈亏数据接口

### 请求参数

| 参数名        | 说明     | 举例         |
|:-----------|:-------|------------|
| broker     | 席位     | 永安期货       |
| start_date | 查询开始日期 | 2018-07-08 |
| end_date   | 查询结束日期 | 2018-07-08 |

### 返回参数

| 参数名          | 类型     | 说明       |
|:-------------|:-------|----------|
| symbol       | string | 品种编码     |
| total_profit | float  | 盈亏数据，单位元 |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
broker_profit_df = pro.broker_profit(broker="永安期货", start_date="2018-07-08", end_date="2018-08-08")
print(broker_profit_df)
```

### 返回示例

```
   symbol  total_profit
0       V     -48104250
1      MA     -44697020
2      ZC     -39435720
3       L     -30429900
4      PB     -23105875
5      RU     -22609450
6      AP     -15512460
7      CF     -13747625
8      AL     -13160850
9       Y     -12917280
10     NI      -9893720
11     AU      -9268650
12     TF      -9065400
13      C      -7829490
14     OI      -7340560
15      I      -6386050
16     IF      -5309736
17      A      -3110200
18     FU      -2245870
19     JM      -2199690
20      P      -2157100
21     JD       -981440
22      B       -813930
23     CS       -416630
24     PM         19200
25     WH         33600
26     SN        297220
27     FG        773020
28     RM       1176220
29     SF       2391770
30     IH       3532800
31     ZN       3822275
32     BU       4279600
33     SM       4757220
34     AG       5508285
35     IC      10934632
36     CU      23284400
37     SR      24980560
38      T      35304400
39     HC      51397670
40      M      76153330
41     PP     109996275
42     RB     200050400
43     TA     422540380
44      J     576955550
```
