---
title: "variety_positions - 合约持仓数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/commodity.md]
confidence: high
---
# variety_positions

- 分类: [[qhkc-commodity|商品]]
- 主题路径: 商品 > 合约持仓数据
- 描述: 合约持仓数据接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/commodity.html

## 相关

- [[qhkc-commodity|商品]]
- [[_meta/topic-map]]

## 源文摘录

## 合约持仓数据

### 接口名称

variety_positions

### 接口描述

合约持仓数据接口

### 请求参数

| 参数名    | 说明    | 举例                            |
|--------|-------|-------------------------------|
| fields | 多头/空头 | longs: 返回多头数据; shorts: 返回空头数据 |
| code   | 合约代号  | rb1810                        |
| date   | 查询日期  | 2018-08-08                    |

### 返回参数

| 参数名        | 类型     | 说明         |
|:-----------|:-------|:-----------|
| longs      | array  | 多头龙虎榜      |
| shorts     | array  | 空头龙虎榜      |
| broker     | string | 席位         |
| long       | int    | 该席位多头持仓量   |
| long_chge  | int    | 该席位多头持仓变化量 |
| short      | int    | 该席位空头持仓量   |
| short_chge | int    | 该席位空头持仓变化量 |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
variety_positions_df = pro.variety_positions(fields="longs", code="rb1810", date="2018-08-08")
print(variety_positions_df)
```

### 返回示例

```
   broker   long  long_chge
0    永安期货  80565       3075
1    申银万国  65572       2992
2    华泰期货  49279      -1552
3    中信期货  46272       4286
4    海通期货  42596       -286
5    方正中期  41839      -7504
6    鲁证期货  41520       -550
7    银河期货  38892      -2800
8    一德期货  34618      -1378
9    国泰君安  25854      -2188
10   广发期货  21496      -1695
11   国投安信  21494       2193
12   大地期货  20705         23
13   兴证期货  20166       4071
14   浙商期货  20001       -817
15   南华期货  19311      -2173
16   东海期货  18912      -1259
17   东证期货  15956       -192
18   瑞达期货  15648      -2091
19   光大期货  14758       -910
20   中国国际  12772      12772
21   国海良时      0     -15721
```
