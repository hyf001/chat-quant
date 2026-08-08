---
title: "inventory - 参数类型二"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/fundamental.md]
confidence: high
---
# inventory

- 分类: [[qhkc-fundamental|基本面]]
- 主题路径: 基本面 > 库存数据 > 参数类型二
- 描述: 库存数据接口-参数类型二
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/fundamental.html

## 相关

- [[qhkc-fundamental|基本面]]
- [[_meta/topic-map]]

## 源文摘录

### 参数类型二

#### 接口名称

inventory

#### 接口描述

库存数据接口-参数类型二

#### 请求参数

| 参数名         | 说明    | 举例   |
|:------------|:------|------|
| variety     | 品种编码  | RB   |
| year        | 查询年份  | 2019 |
| week_number | 该年第几周 | 10   |

#### 返回参数

| 参数名        | 类型    | 说明    |
|:-----------|:------|-------|
| trans_date | date  | 查询日期  |
| vol        | float | 库存数据量 |

#### 示例代码

```python
from akshare import pro_api

pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
inventory_df = pro.inventory(variety="RB", year="2019", week_number="10")
print(inventory_df)
```

#### 返回示例

```
             inventory
trans_date  2019-03-07
vol            1326.64
```
