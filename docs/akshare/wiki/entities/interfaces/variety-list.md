---
title: "variety_list - 合约索引"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/commodity.md]
confidence: high
---
# variety_list

- 分类: [[qhkc-commodity|商品]]
- 主题路径: 商品 > 合约索引
- 描述: 合约索引数据接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/commodity.html

## 相关

- [[qhkc-commodity|商品]]
- [[_meta/topic-map]]

## 源文摘录

## 合约索引

### 接口名称

variety_list

### 接口描述

合约索引数据接口

### 请求参数

| 参数名  | 说明   | 举例         |
|:-----|:-----|------------|
| date | 查询日期 | 2018-08-08 |

### 返回参数

| 参数名 | 类型     | 说明 |
|:----|:-------|----|
| -   | string | 合约 |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
variety_list_df = pro.variety_list(date="2018-08-08")
print(variety_list_df)
```

### 返回示例

```
          0
0     a1809
1     a1811
2     a1901
3     a1903
4     a1905
..      ...
495  zn1903
496  zn1904
497  zn1905
498  zn1906
499  zn1907
```
