---
title: "variety_net_positions - 商品净持仓数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/commodity.md]
confidence: high
---
# variety_net_positions

- 分类: [[qhkc-commodity|商品]]
- 主题路径: 商品 > 商品净持仓数据
- 描述: 商品净持仓数据接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/commodity.html

## 相关

- [[qhkc-commodity|商品]]
- [[_meta/topic-map]]

## 源文摘录

## 商品净持仓数据

### 接口名称

variety_net_positions

### 接口描述

商品净持仓数据接口

### 请求参数

| 参数名    | 说明     | 举例         |
|:-------|:-------|------------|
| symbol | 查询品种编码 | RB         |
| broker | 席位     | 永安期货       |
| date   | 查询日期   | 2018-08-08 |

### 返回参数

| 参数名          | 类型   | 说明    |
|:-------------|:-----|-------|
| trans_date   | date | 查询日期  |
| net_position | int  | 净持仓数据 |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
variety_net_positions_df = pro.variety_net_positions(symbol="RB", broker="永安期货", date="2018-08-08")
print(variety_net_positions_df)
```

### 返回示例

```
             variety_net_positions
trans_date              2018-08-08
net_position                 58463
```
