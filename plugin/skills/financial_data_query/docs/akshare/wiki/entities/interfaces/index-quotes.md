---
title: "index_quotes - 指数行情数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/index_data.md]
confidence: high
---
# index_quotes

- 分类: [[qhkc-index-data|指数]]
- 主题路径: 指数 > 指数行情数据
- 描述: 指数行情数据接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/index_data.html

## 相关

- [[qhkc-index-data|指数]]
- [[_meta/topic-map]]

## 源文摘录

## 指数行情数据

### 接口名称

index_quotes

### 接口描述

指数行情数据接口

### 请求参数

| 参数名      | 说明   | 举例                                        |
|:---------|:-----|-------------------------------------------|
| index_id | 指数id | index0070c0eb-93ba-2da9-6633-fa70cb90e959 |
| date     | 查询日期 | 2018-08-08                                |

### 返回参数

| 参数名        | 类型    | 说明    |
|:-----------|:------|-------|
| trans_date | date  | 日期    |
| volume     | int   | 指数成交量 |
| openint    | int   | 指数持仓量 |
| price      | float | 指数价格  |
| bbr        | float | 指数多空比 |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
index_quotes_df = pro.index_quotes(index_id="index0070c0eb-93ba-2da9-6633-fa70cb90e959", date="2018-08-08")
print(index_quotes_df)
```

### 返回示例

```
           index_quotes
trans_date   2018-08-08
volume          4119565
openint         3584323
price           1195.06
bbr               51.57
```
