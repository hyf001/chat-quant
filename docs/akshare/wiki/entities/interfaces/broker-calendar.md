---
title: "broker_calendar - 席位盈亏数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/broker.md]
confidence: high
---
# broker_calendar

- 分类: [[qhkc-broker|席位]]
- 主题路径: 席位 > 席位盈亏数据
- 描述: 席位盈亏数据接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/broker.html

## 相关

- [[qhkc-broker|席位]]
- [[_meta/topic-map]]

## 源文摘录

## 席位盈亏数据

### 接口名称

broker_calendar

### 接口描述

席位盈亏数据接口

### 请求参数

| 参数名        | 说明     | 举例         |
|:-----------|:-------|------------|
| broker     | 席位     | 永安期货       |
| start_date | 查询开始日期 | 2018-07-08 |
| end_date   | 查询结束日期 | 2018-08-08 |

### 返回参数

| 参数名        | 类型    | 说明       |
|:-----------|:------|----------|
| trans_date | date  | 查询日期     |
| profit     | float | 席位盈亏，单位元 |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
broker_calendar_df = pro.broker_calendar(broker="永安期货", start_date="2018-07-08", end_date="2018-08-08")
print(broker_calendar_df)
```

### 返回示例

```
       profit  trans_date
0    28534980  2018-07-09
1     -793730  2018-07-10
2   116090590  2018-07-11
3    71637460  2018-07-12
4   -67672690  2018-07-13
5  -101844070  2018-07-16
6    12677005  2018-07-17
7    28082910  2018-07-18
8    13328330  2018-07-19
9   152125816  2018-07-20
10   85702590  2018-07-23
11  111615970  2018-07-24
12   66728815  2018-07-25
13  -20638805  2018-07-26
14  106367725  2018-07-27
15  170801705  2018-07-30
16   16650180  2018-07-31
17  -11149860  2018-08-01
18    7460090  2018-08-02
19  153065340  2018-08-03
20  157935930  2018-08-06
21   95817915  2018-08-07
22   34925715  2018-08-08
```
