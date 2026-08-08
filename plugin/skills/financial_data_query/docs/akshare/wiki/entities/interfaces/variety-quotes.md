---
title: "variety_quotes - 合约行情数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/commodity.md]
confidence: high
---
# variety_quotes

- 分类: [[qhkc-commodity|商品]]
- 主题路径: 商品 > 合约行情数据
- 描述: 合约行情数据接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/commodity.html

## 相关

- [[qhkc-commodity|商品]]
- [[_meta/topic-map]]

## 源文摘录

## 合约行情数据

### 接口名称

variety_quotes

### 接口描述

合约行情数据接口

### 请求参数

| 参数名  | 说明     | 举例         |
|:-----|:-------|------------|
| code | 具体合约代号 | rb1810     |
| date | 查询日期   | 2018-08-08 |

### 返回参数

| 参数名     | 类型    | 说明  |
|:--------|:------|-----|
| open    | float | 开盘价 |
| close   | float | 收盘价 |
| high    | float | 最高价 |
| low     | float | 最低价 |
| volume  | int   | 成交量 |
| openint | int   | 持仓量 |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
variety_quotes_df = pro.variety_quotes(code="rb1810", date="2018-08-08")
print(variety_quotes_df)
```

### 返回示例

```
              variety_quotes
open                    4237
close                   4236
high                    4278
low                     4205
volume               2620386
openint              2160052
settle_price            4240
```
