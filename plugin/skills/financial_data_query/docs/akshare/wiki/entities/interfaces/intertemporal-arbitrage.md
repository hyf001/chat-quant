---
title: "intertemporal_arbitrage - 跨期套利数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/fundamental.md]
confidence: high
---
# intertemporal_arbitrage

- 分类: [[qhkc-fundamental|基本面]]
- 主题路径: 基本面 > 跨期套利数据
- 描述: 跨期套利数据接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/fundamental.html

## 相关

- [[qhkc-fundamental|基本面]]
- [[_meta/topic-map]]

## 源文摘录

## 跨期套利数据

### 接口名称

intertemporal_arbitrage

### 接口描述

跨期套利数据接口

### 请求参数

|参数名|说明|举例|
|:-----  |:-----|-----                           |
|variety |品种编码   |RB|
|code1 |合约月份1   |01|
|code2 |合约月份2   |05|
|date |查询日期   |2018-08-08|

### 返回参数

|参数名|类型|说明|
|:-----  |:-----|-----                           |
|trans_date |date   |查询日期  |
|code1 |string   |合约1  |
|code2 |string   |合约2  |
|close1 |float   |合约1价格  |
|close2 |float   |合约2价格  |
|spread |float   |价差，合约1价格 - 合约2价格  |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
intertemporal_arbitrage_df = pro.intertemporal_arbitrage(variety="RB", code1="01", code2="05", date="2018-08-08")
print(intertemporal_arbitrage_df)
```

### 返回示例

```
           intertemporal_arbitrage
trans_date              2018-08-08
code1                       rb1901
code2                       rb1905
close1                        4109
close2                        3930
spread                         179
```
