---
title: "trader_prices - 现货贸易商报价"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/fundamental.md]
confidence: high
---
# trader_prices

- 分类: [[qhkc-fundamental|基本面]]
- 主题路径: 基本面 > 现货贸易商报价
- 描述: 现货贸易商报价接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/fundamental.html

## 相关

- [[qhkc-fundamental|基本面]]
- [[_meta/topic-map]]

## 源文摘录

## 现货贸易商报价

### 接口名称

trader_prices

### 接口描述

现货贸易商报价接口

### 请求参数

|参数名|说明|举例|
|:-----  |:-----|-----                           |
|variety |品种编码   |RB|
|date |查询日期   |2018-08-08|

### 返回参数

|参数名|类型|说明|
|:-----  |:-----|-----                           |
|name |string   |品种名称  |
|price |float   |贸易商报价  |
|band |string   |品牌  |
|model |string   |型号、规格  |
|unit |string   |单位  |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
trader_prices_df = pro.trader_prices(variety="RB", date="2020-03-30")
print(trader_prices_df)
```

### 返回示例

```
  band                      model name  price unit
0   永钢  品种:Ⅲ级螺纹钢;牌号:HRB400;规格:Φ16  螺纹钢   3500  元/吨
1   永钢  品种:Ⅲ级螺纹钢;牌号:HRB400;规格:Φ16  螺纹钢   3440  元/吨
2   永钢  品种:Ⅲ级螺纹钢;牌号:HRB400;规格:Φ16  螺纹钢   3440  元/吨
3   中新  品种:Ⅲ级螺纹钢;牌号:HRB400;规格:Φ16  螺纹钢   3320  元/吨
4   镔鑫  品种:Ⅲ级螺纹钢;牌号:HRB400;规格:Φ16  螺纹钢   3380  元/吨
5   永钢  品种:Ⅲ级螺纹钢;牌号:HRB400;规格:Φ16  螺纹钢   3470  元/吨
6   中天  品种:Ⅲ级螺纹钢;牌号:HRB400;规格:Φ16  螺纹钢   3490  元/吨
7   长达  品种:Ⅲ级螺纹钢;牌号:HRB400;规格:Φ16  螺纹钢   3400  元/吨
8   兴鑫  品种:Ⅲ级螺纹钢;牌号:HRB400;规格:Φ16  螺纹钢   3380  元/吨
```
