---
title: "warehouse_receipt - 仓单数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/fundamental.md]
confidence: high
---
# warehouse_receipt

- 分类: [[qhkc-fundamental|基本面]]
- 主题路径: 基本面 > 仓单数据
- 描述: 仓单数据接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/fundamental.html

## 相关

- [[qhkc-fundamental|基本面]]
- [[_meta/topic-map]]

## 源文摘录

## 仓单数据

### 接口名称

warehouse_receipt

### 接口描述

仓单数据接口

### 请求参数

|参数名|说明|举例|
|:-----  |:-----|-----                           |
|variety |品种编码   |RB|
|date |查询日期   |2018-08-08|

### 返回参数

|参数名|类型|说明|
|:-----  |:-----|-----                           |
|trans_date |date   |查询日期  |
|total_vol |float   |仓单数据  |
|total_chge |float   |仓单变化量  |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
warehouse_receipt_df = pro.warehouse_receipt(variety="RB", date="2018-08-08")
print(warehouse_receipt_df)
```

### 返回示例

```
           warehouse_receipt
trans_date        2018-08-08
total_vol               3856
total_chge                 0
```
