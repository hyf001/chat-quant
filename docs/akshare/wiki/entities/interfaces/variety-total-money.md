---
title: "variety_total_money - 合约总持仓保证金数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/commodity.md]
confidence: high
---
# variety_total_money

- 分类: [[qhkc-commodity|商品]]
- 主题路径: 商品 > 合约总持仓保证金数据
- 描述: 合约总持仓保证金数据接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/commodity.html

## 相关

- [[qhkc-commodity|商品]]
- [[_meta/topic-map]]

## 源文摘录

## 合约总持仓保证金数据

### 接口名称

variety_total_money

### 接口描述

合约总持仓保证金数据接口

### 请求参数

| 参数名  | 说明     | 举例         |
|:-----|:-------|------------|
| code | 具体合约代号 | rb1810     |
| date | 查询日期   | 2018-08-08 |

### 返回参数

| 参数名    | 类型     | 说明           |
|:-------|:-------|--------------|
| broker | string | 席位           |
| value  | float  | 总持仓保证金数据，单位元 |

### 示例代码

```python
from akshare import pro_api

pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
variety_total_money_df = pro.variety_total_money(code="rb1810", date="2018-08-08")
print(variety_total_money_df)
```

### 返回示例

```
   broker      value
0    中辉期货   99601416
1    中大期货   90671976
2    银河期货  381138264
3    徽商期货   72374256
4    中信建投   70912728
5    光大期货  164912256
6    国泰君安  237935232
7    东海期货  183786192
8    南华期货  179977824
9    东证期货  143599896
10   兴证期货  161905248
11   华安期货          0
12   国海良时          0
13   国投安信  146160432
14   广发期货  137696544
15   中信期货  322039872
16   方正中期  282170304
17   中国国际   48737952
18   海通期货  275644944
19   瑞达期货   59712768
20   鲁证期货  244304136
21   浙商期货   76323816
22   大地期货   79010280
23   永安期货  526932360
24   华泰期货  253210680
25   一德期货  132102288
26   申银万国  306989568
```
