---
title: "stock_flow_short - 每日净流空列表(指数)"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/fund.md]
confidence: high
---
# stock_flow_short

- 分类: [[qhkc-fund|资金]]
- 主题路径: 资金 > 每日净流空列表(指数)
- 描述: 每日净流空列表(指数)接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/fund.html

## 相关

- [[qhkc-fund|资金]]
- [[_meta/topic-map]]

## 源文摘录

## 每日净流空列表(指数)

### 接口名称

stock_flow_short

### 接口描述

每日净流空列表(指数)接口

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
stock_flow_short_df = pro.stock_flow_short(date="2018-08-08")
print(stock_flow_short_df)
```

### 返回示例

```
  broker       money variety
0   兴证期货 -58628808.0      IC
1   银河期货 -25623004.0       T
2   中信建投 -22801228.8      IC
3   中国国际 -22069300.0       T
4   广发期货 -21033230.4      IC
5   海通期货 -19759036.8      IC
6   鲁证期货 -19506972.0       T
7   海通期货 -17856834.0      IF
8   中金期货 -17410272.0      IF
9   南华期货 -13345152.0      IF
```
