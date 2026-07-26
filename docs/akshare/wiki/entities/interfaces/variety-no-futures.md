---
title: "variety_no_futures - 非期货公司净持仓"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/commodity.md]
confidence: high
---
# variety_no_futures

- 分类: [[qhkc-commodity|商品]]
- 主题路径: 商品 > 非期货公司净持仓
- 描述: 非期货公司净持仓数据接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/commodity.html

## 相关

- [[qhkc-commodity|商品]]
- [[_meta/topic-map]]

## 源文摘录

## 非期货公司净持仓

### 接口名称

variety_no_futures

### 接口描述

非期货公司净持仓数据接口

### 请求参数

| 参数名    | 说明    | 举例         |
|:-------|:------|------------|
| symbol | 品种编码	 | RB         |
| date   | 查询日期  | 2018-08-08 |

### 返回参数

| 参数名        | 类型   | 说明         |
|:-----------|:-----|------------|
| trans_date | date | 查询日期       |
| net_value  | int  | 非期货公司净持仓数据 |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
variety_no_futures_df = pro.variety_no_futures(symbol="RB", date="2018-08-08")
print(variety_no_futures_df)
```

### 返回示例

```
           variety_no_futures
trans_date         2018-08-08
net_value               -1000
```
