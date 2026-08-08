---
title: "term_structure - 期限结构"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/fundamental.md]
confidence: high
---
# term_structure

- 分类: [[qhkc-fundamental|基本面]]
- 主题路径: 基本面 > 期限结构
- 描述: 期限结构接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/fundamental.html

## 相关

- [[qhkc-fundamental|基本面]]
- [[_meta/topic-map]]

## 源文摘录

## 期限结构

### 接口名称

term_structure

### 接口描述

期限结构接口

### 请求参数

|参数名|说明|举例|
|:-----  |:-----|-----                           |
|variety |品种编码   |RB|
|date |查询日期   |2018-08-08|

### 返回参数

|参数名|类型|说明|
|:-----  |:-----|-----                           |
|code |string   |合约代号  |
|close |float   |收盘价  |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
term_structure_df = pro.term_structure(variety="RB", date="2018-08-08")
print(term_structure_df)
```

### 返回示例

```
    close    code
0    4200  rb1808
1    4322  rb1809
2    4236  rb1810
3    4191  rb1811
4    4139  rb1812
5    4094  rb1901
6    4017  rb1902
7    3987  rb1903
8    3977  rb1904
9    3918  rb1905
10   3889  rb1906
11   3881  rb1907
```
