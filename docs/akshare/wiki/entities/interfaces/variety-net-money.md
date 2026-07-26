---
title: "variety_net_money - 合约净持仓保证金数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/commodity.md]
confidence: high
---
# variety_net_money

- 分类: [[qhkc-commodity|商品]]
- 主题路径: 商品 > 合约净持仓保证金数据
- 描述: 合约净持仓保证金数据接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/commodity.html

## 相关

- [[qhkc-commodity|商品]]
- [[_meta/topic-map]]

## 源文摘录

## 合约净持仓保证金数据

### 接口名称

variety_net_money

### 接口描述

合约净持仓保证金数据接口

### 请求参数

| 参数名  | 说明     | 举例         |
|:-----|:-------|------------|
| code | 具体合约代号 | rb1810     |
| date | 查询日期   | 2018-08-08 |

### 返回参数

| 参数名    | 类型     | 说明                       |
|:-------|:-------|--------------------------|
| broker | string | 席位                       |
| value  | float  | 净持仓保证金数据，正数为净多，负数为净空，单位元 |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
variety_net_money_df = pro.variety_net_money(code="rb1810", date="2018-08-08")
print(variety_net_money_df)
```

### 返回示例

```
   broker      value
0    中辉期货  -99601416
1    中大期货  -90671976
2    银河期货  -84314520
3    徽商期货  -72374256
4    中信建投  -70912728
5    光大期货  -52279200
6    国泰君安  -40617504
7    东海期货  -39449808
8    南华期货  -32596272
9    东证期货  -21823704
10   兴证期货   -7998336
11   华安期货          0
12   国海良时          0
13   国投安信   17881776
14   广发期货   26360928
15   中信期货   31108032
16   方正中期   37144944
17   中国国际   48737952
18   海通期货   49447728
19   瑞达期货   59712768
20   鲁证期货   72576504
21   浙商期货   76323816
22   大地期货   79010280
23   永安期货   87939720
24   华泰期货  122886648
25   一德期货  132102288
26   申银万国  193455936
```
