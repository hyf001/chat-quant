---
title: "basis - 基差数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/fundamental.md]
confidence: high
---
# basis

- 分类: [[qhkc-fundamental|基本面]]
- 主题路径: 基本面 > 基差数据
- 描述: 基差数据接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/fundamental.html

## 相关

- [[qhkc-fundamental|基本面]]
- [[_meta/topic-map]]

## 源文摘录

## 基差数据

### 接口名称

basis

### 接口描述

基差数据接口

### 请求参数

|参数名|说明|举例|
|:-----  |:-----|-----                           |
|variety |品种编码   |RB|
|date |查询日期   |2018-08-08|

### 返回参数

|参数名|类型|说明|
|:-----  |:-----|-----                           |
|trans_date |date   |查询日期  |
|spot |float   |现货价格  |
|basis |float   |基差，基差 = 现货价格 - 期货价格  |
|basis_rate |float   |基差率，基差率 = (现货价格 - 期货价格) / 现货价格 x 100%  |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
basis_df = pro.basis(variety="RB", date="2018-08-08")
print(basis_df)
```

### 返回示例

```
                 basis
trans_date  2018-08-08
spot              4429
basis              193
basis_rate     4.35764
```
