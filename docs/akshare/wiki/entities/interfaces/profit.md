---
title: "profit - 利润数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/fundamental.md]
confidence: high
---
# profit

- 分类: [[qhkc-fundamental|基本面]]
- 主题路径: 基本面 > 利润数据
- 描述: 利润数据接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/fundamental.html

## 相关

- [[qhkc-fundamental|基本面]]
- [[_meta/topic-map]]

## 源文摘录

## 利润数据

### 接口名称

profit

### 接口描述

利润数据接口

### 请求参数

|参数名|说明|举例|
|:-----  |:-----|-----                           |
|variety |品种编码   |RB|
|date |查询日期   |2018-12-08|

### 返回参数

|参数名|类型|说明|
|:-----  |:-----|-----                           |
|trans_date |date   |查询日期  |
|profit |float   |利润，折盘面价格  |
|profit_rate |float   |利润率  |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
profit_df = pro.profit(variety="RB", date="2019-12-12")
print(profit_df)
```

### 返回示例

```
                 profit
trans_date   2019-12-12
profit              559
profit_rate       16.58
```
