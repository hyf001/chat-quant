---
title: "commodity_flow_long - 每日净流多列表(商品)"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/fund.md]
confidence: high
---
# commodity_flow_long

- 分类: [[qhkc-fund|资金]]
- 主题路径: 资金 > 每日净流多列表(商品)
- 描述: 每日净流多列表（商品）接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/fund.html

## 相关

- [[qhkc-fund|资金]]
- [[_meta/topic-map]]

## 源文摘录

## 每日净流多列表(商品)

### 接口名称

commodity_flow_long

### 接口描述

每日净流多列表（商品）接口

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
commodity_flow_long_df = pro.commodity_flow_long(date="2018-08-08")
print(commodity_flow_long_df)
```

### 返回示例

```
  broker       money variety
0   浙商期货  78975156.0       J
1   华泰期货  63497619.0      RB
2   大地期货  55812816.0      RB
3   中国国际  50224588.2      RB
4   海证期货  41670190.8      RB
5   新湖期货  39482177.0      CU
6   国投安信  39439456.2      RB
7   东海期货  34120575.0      RB
8   弘业期货  33741000.0       J
9   中辉期货  33432132.0       J
```
