---
title: "broker_all - 所有席位数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/broker.md]
confidence: high
---
# broker_all

- 分类: [[qhkc-broker|席位]]
- 主题路径: 席位 > 所有席位数据
- 描述: 所有席位数据接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/broker.html

## 相关

- [[qhkc-broker|席位]]
- [[_meta/topic-map]]

## 源文摘录

## 所有席位数据

### 接口名称

broker_all

### 接口描述

所有席位数据接口

### 请求参数

| 参数名         | 说明               | 举例                |
|:------------|:-----------------|-------------------|
| offset_days | 过滤阈值，N个交易日内上过龙虎榜 | 默认为365，即一年内上过榜的席位 |

### 返回参数

| 参数名    | 类型     | 说明             |
|:-------|:-------|----------------|
| broker | string | 席位             |
| grade  | string | 盈利评级，最好为A，最差为E |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
broker_all_df = pro.broker_all(offset_days="365")
print(broker_all_df)
```

### 返回示例

```
    broker grade
0     安粮期货     C
1     渤海期货     B
2     北京首创     C
3     倍特期货     C
4     宝城期货     B
5     长江期货     D
6     创元期货     D
7     长安期货     D
8     长城期货     D
9     财达期货     D
10    东航期货     B
11    德盛期货     D
12    道通期货     C
13    东方期货     C
14    大地期货     B
15    东亚期货     B
16    东海期货     B
17    大通期货     D
18    大连良运     D
19    第一创业     D
20    东吴期货     D
21    东方财富     E
22    大越期货     B
23    东华期货     D
24    东证期货     D
25    东方汇金     D
26    大有期货     D
27    东兴期货     D
28    方正中期     E
29    福能期货     C
..     ...   ...
131   银河期货     B
132   永安期货     A
133   英大期货     D
134   云晨期货     B
135   一德期货     A
136  云财富期货     D
137   浙商期货     C
138   中天期货     C
139   中融汇信     D
140   中信期货     C
141   中投期货     D
142   中辉期货     E
143   中大期货     C
144   中航期货     D
145   中银国际     B
146   中信建投     E
147   中投天琪     D
148   中财期货     B
149   中国国际     D
150   中粮期货     B
151   中钢期货     C
152   招金期货     E
153    中电投     D
154  浙江新世纪     D
155   中州期货     D
156   中衍期货     C
157   中原期货     D
158  中电投先融     C
159   中金期货     B
160   招商期货     D
```
