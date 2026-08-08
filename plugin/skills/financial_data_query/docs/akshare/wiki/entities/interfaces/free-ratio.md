---
title: "free_ratio - 自由价比数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/fundamental.md]
confidence: high
---
# free_ratio

- 分类: [[qhkc-fundamental|基本面]]
- 主题路径: 基本面 > 自由价比数据
- 描述: 自由价比数据接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/fundamental.html

## 相关

- [[qhkc-fundamental|基本面]]
- [[_meta/topic-map]]

## 源文摘录

## 自由价比数据

### 接口名称

free_ratio

### 接口描述

自由价比数据接口

### 请求参数

|参数名|说明|举例|
|:-----  |:-----|-----                           |
|variety1 |品种编码1   |RB|
|code1 |合约月份1   |01|
|variety2 |品种编码2   |HC|
|code2 |合约月份2   |01|
|date |查询日期   |2018-08-08|

### 返回参数

|参数名|类型|说明|
|:-----  |:-----|-----                           |
|trans_date |string   |查询日期  |
|code1 |string   |合约代号1  |
|code2 |string   |合约代号2  |
|code1_close |float   |合约1价格  |
|code2_close |float   |合约2价格  |
|ratio |float   |价比，合约1价格 / 合约2价格  |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
free_ratio_df = pro.free_ratio(variety1="RB", code1="01", variety2="HC", code2="01", date="2018-08-08")
print(free_ratio_df)
```

### 返回示例

```
             free_ratio
trans_date   2018-08-08
code1            rb1901
code2            hc1901
code1_close        4094
code2_close        4100
ratio          0.998537
```
