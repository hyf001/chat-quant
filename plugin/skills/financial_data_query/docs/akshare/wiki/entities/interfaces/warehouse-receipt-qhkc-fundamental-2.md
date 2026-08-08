---
title: "warehouse_receipt - 仓单汇总数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/fundamental.md]
confidence: high
---
# warehouse_receipt

- 分类: [[qhkc-fundamental|基本面]]
- 主题路径: 基本面 > 仓单汇总数据
- 描述: 仓单汇总数据接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/fundamental.html

## 相关

- [[qhkc-fundamental|基本面]]
- [[_meta/topic-map]]

## 源文摘录

## 仓单汇总数据

### 接口名称

warehouse_receipt

### 接口描述

仓单汇总数据接口

### 请求参数

|参数名|说明|举例|
|:-----  |:-----|-----                           |
|date |查询日期   |2018-08-08|

### 返回参数

| 参数名        | 类型     | 说明    |
|:-----------|:-------|-------|
| symbol     | string | 品种编码  |
| total_vol  | float  | 仓单数据  |
| total_chge | float  | 仓单变化量 |

### 示例代码

```python
from akshare import pro_api

pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
warehouse_receipt_sum_df = pro.warehouse_receipt(date="2018-08-08")
print(warehouse_receipt_sum_df)
```

### 返回示例

```
   symbol  total_chge  total_vol
0      RB           0       3856
1       J           0         10
2      HC           0        310
3      CF          39       9905
4      FG           0       1378
5      OI           0       4323
6      RM           0        200
7      SF           0        594
8      SR         402      37828
9      TA       -1009      11795
10     CU       -1658      79843
11     AL        1446     731544
12     ZN        -125       6950
13     PB         -25       7697
14     NI           0      15215
15     SN          29       5823
16     AU           0       1530
17     AG        1292    1394784
18     BU           0     128970
19     RU         720     491780
20      A           0      32586
21      C           0      37968
22     JD          -3          0
23      L           0        284
24      M           0       6543
25     PP           0        765
26      V           0        180
27      Y           0      33215
28     WH           0        414
```
