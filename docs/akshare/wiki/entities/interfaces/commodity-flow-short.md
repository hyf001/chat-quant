---
title: "commodity_flow_short - 每日净流空列表(商品)"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/fund.md]
confidence: high
---
# commodity_flow_short

- 分类: [[qhkc-fund|资金]]
- 主题路径: 资金 > 每日净流空列表(商品)
- 描述: 每日净流空列表(商品)接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/fund.html

## 相关

- [[qhkc-fund|资金]]
- [[_meta/topic-map]]

## 源文摘录

## 每日净流空列表(商品)

### 接口名称

commodity_flow_short

### 接口描述

每日净流空列表(商品)接口

### 请求参数

| 参数名  | 说明   | 举例         |
|:-----|:-----|------------|
| date | 查询日期 | 2018-08-08 |

### 返回参数

| 参数名     | 类型     | 说明       |
|:--------|:-------|----------|
| broker  | string | 席位       |
| money   | float  | 流空资金，单位元 |
| variety | string | 品种编码     |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
commodity_flow_short_df = pro.commodity_flow_short(date="2018-08-08")
print(commodity_flow_short_df)
```

### 返回示例

```
  broker       money variety
0   方正中期 -98550360.0      RB
1   国海良时 -59991336.0      RB
2   永安期货 -52131000.0       J
3   南华期货 -47408484.6      RB
4   迈科期货 -42165963.0      CU
5   永安期货 -36507715.2      ZC
6   光大期货 -35340900.0       J
7   申银万国 -32120996.0       I
8   申银万国 -31075680.0       J
9   国海良时 -30726828.0       I
```
