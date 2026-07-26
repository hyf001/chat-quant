---
title: "stock_flow_long - 每日净流多列表(指数)"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/fund.md]
confidence: high
---
# stock_flow_long

- 分类: [[qhkc-fund|资金]]
- 主题路径: 资金 > 每日净流多列表(指数)
- 描述: 每日净流多列表(指数)接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/fund.html

## 相关

- [[qhkc-fund|资金]]
- [[_meta/topic-map]]

## 源文摘录

## 每日净流多列表(指数)

### 接口名称

stock_flow_long

### 接口描述

每日净流多列表(指数)接口

### 请求参数

| 参数名  | 说明   | 举例         |
|:-----|:-----|------------|
| date | 查询日期 | 2018-08-08 |

### 返回参数

| 参数名     | 类型     | 说明       |
|:--------|:-------|----------|
| broker  | string | 席位       |
| money   | float  | 流多资金，单位元 |
| variety | string | 品种编码     |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
stock_flow_long_df = pro.stock_flow_long(date="2018-08-08")
print(stock_flow_long_df)
```

### 返回示例

```
  broker       money variety
0   浙商期货  43487544.0       T
1   华信期货  32456851.2      IC
2   永安期货  28275580.0       T
3   宏源期货  25465190.4      IC
4   华泰期货  24695284.0       T
5   东吴期货  19973982.0      IF
6   国投安信  16403899.2      IC
7   东证期货  16318434.0      IF
8   光大期货  16102408.0       T
9   国泰君安  15661356.0      IF
```
