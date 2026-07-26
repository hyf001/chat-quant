---
title: "variety_money - 商品沉淀资金数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/commodity.md]
confidence: high
---
# variety_money

- 分类: [[qhkc-commodity|商品]]
- 主题路径: 商品 > 商品沉淀资金数据
- 描述: 商品沉淀资金数据接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/commodity.html

## 相关

- [[qhkc-commodity|商品]]
- [[_meta/topic-map]]

## 源文摘录

## 商品沉淀资金数据

### 接口名称

variety_money

### 接口描述

商品沉淀资金数据接口

### 请求参数

| 参数名    | 说明   | 举例         |
|:-------|:-----|------------|
| symbol | 品种编码 | RB         |
| date   | 查询日期 | 2018-08-08 |

### 返回参数

| 参数名         | 类型    | 说明        |
|:------------|:------|-----------|
| trans_date  | date  | 查询日期      |
| total_value | float | 沉淀资金量，单位元 |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
variety_money_df = pro.variety_money(symbol="RB", date="2018-08-08")
print(variety_money_df)
```

### 返回示例

```
            variety_money
trans_date     2018-08-08
total_value   7.46824e+09
```
