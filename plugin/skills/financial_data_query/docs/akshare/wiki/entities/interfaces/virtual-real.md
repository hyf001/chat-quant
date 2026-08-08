---
title: "virtual_real - 虚实盘比数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/fundamental.md]
confidence: high
---
# virtual_real

- 分类: [[qhkc-fundamental|基本面]]
- 主题路径: 基本面 > 虚实盘比数据
- 描述: 虚实盘比数据接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/fundamental.html

## 相关

- [[qhkc-fundamental|基本面]]
- [[_meta/topic-map]]

## 源文摘录

## 虚实盘比数据

### 接口名称

virtual_real

### 接口描述

虚实盘比数据接口

### 请求参数

|参数名|说明|举例|
|:-----  |:-----|-----                           |
|variety |品种编码   |RB|
|code |合约月份   |10|
|date |查询日期   |2018-08-08|

### 返回参数

|参数名|类型|说明|
|:-----  |:-----|-----                           |
|trans_date |date   |查询日期  |
|code |string   |合约代号  |
|virtual |float   |虚盘量  |
|real |float   |实盘量  |
|rate |float   |虚实盘比  |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
virtual_real_df = pro.virtual_real(variety="RB", code="10", date="2018-08-08")
print(virtual_real_df)
```

### 返回示例

```
           virtual_real
trans_date   2018-08-08
code             rb1810
virtual         1080026
real              385.6
rate             2800.9
```
