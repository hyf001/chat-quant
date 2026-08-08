---
title: "variety_strategies - 自研指标数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/commodity.md]
confidence: high
---
# variety_strategies

- 分类: [[qhkc-commodity|商品]]
- 主题路径: 商品 > 自研指标数据
- 描述: 自研指标数据接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/commodity.html

## 相关

- [[qhkc-commodity|商品]]
- [[_meta/topic-map]]

## 源文摘录

## 自研指标数据

### 接口名称

variety_strategies

### 接口描述

自研指标数据接口

### 请求参数

| 参数名  | 说明   | 举例         |
|:-----|:-----|------------|
| code | 合约代号 | rb1810     |
| date | 查询日期 | 2018-08-08 |

### 返回参数

| 参数名        | 类型    | 说明   |
|:-----------|:------|------|
| trans_date | date  | 查询日期 |
| longhu     | float | 龙虎比  |
| niuxiong   | float | 牛熊线  |

### 示例代码

```python
from akshare import pro_api

pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
variety_strategies_df = pro.variety_strategies(code="rb1810", date="2018-08-08")
print(variety_strategies_df)
```

### 返回示例

```
           variety_strategies
trans_date         2018-08-08
longhu                  7.954
niuxiong                   10
```
