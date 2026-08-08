---
title: "variety_all_positions - 商品持仓数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/commodity.md]
confidence: high
---
# variety_all_positions

- 分类: [[qhkc-commodity|商品]]
- 主题路径: 商品 > 商品持仓数据
- 描述: 商品持仓数据接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/commodity.html

## 相关

- [[qhkc-commodity|商品]]
- [[_meta/topic-map]]

## 源文摘录

## 商品持仓数据

### 接口名称

variety_all_positions

#### 接口描述

商品持仓数据接口

#### 请求参数

| 参数名    | 说明    | 举例                            |
|--------|-------|-------------------------------|
| fields | 多头/空头 | longs: 返回多头数据; shorts: 返回空头数据 |
| symbol | 合约代号  | RB                            |
| date   | 查询日期  | 2018-08-08                    |

#### 返回参数

| 参数名        | 类型     | 说明         |
|:-----------|:-------|:-----------|
| longs      | array  | 多头龙虎榜      |
| shorts     | array  | 空头龙虎榜      |
| broker     | string | 席位         |
| long       | int    | 该席位多头持仓量   |
| long_chge  | int    | 该席位多头持仓变化量 |
| short      | int    | 该席位空头持仓量   |
| short_chge | int    | 该席位空头持仓变化量 |
| code       | string | 具体合约       |

#### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
variety_all_positions_df = pro.variety_all_positions(fields="shorts", symbol="RB", date="2018-08-08")
print(variety_all_positions_df)
```

#### 返回示例

```
   broker   long  long_chge    code
0    东证期货      0        -60  rb1808
1    永安期货  80565       3075  rb1810
2    申银万国  65572       2992  rb1810
3    华泰期货  49279      -1552  rb1810
4    中信期货  46272       4286  rb1810
5    海通期货  42596       -286  rb1810
6    方正中期  41839      -7504  rb1810
7    鲁证期货  41520       -550  rb1810
8    银河期货  38892      -2800  rb1810
9    一德期货  34618      -1378  rb1810
10   国泰君安  25854      -2188  rb1810
11   广发期货  21496      -1695  rb1810
12   国投安信  21494       2193  rb1810
13   大地期货  20705         23  rb1810
14   兴证期货  20166       4071  rb1810
15   浙商期货  20001       -817  rb1810
16   南华期货  19311      -2173  rb1810
17   东海期货  18912      -1259  rb1810
18   东证期货  15956       -192  rb1810
19   瑞达期货  15648      -2091  rb1810
20   光大期货  14758       -910  rb1810
21   中国国际  12772      12772  rb1810
22   国海良时      0     -15721  rb1810
23   永安期货  76193       6726  rb1901
24   国泰君安  57533      10549  rb1901
25   东海期货  44408       2666  rb1901
26   华泰期货  43165      11233  rb1901
27   鲁证期货  33941        711  rb1901
28   银河期货  32133       2862  rb1901
29   一德期货  26147       4950  rb1901
30   方正中期  24644      -2103  rb1901
31   海通期货  23176       2234  rb1901
32   新湖期货  22354       -193  rb1901
33   金瑞期货  21595        229  rb1901
34   中信期货  20821       -226  rb1901
35   瑞达期货  20450       -768  rb1901
36   中国国际  20158        402  rb1901
37   华鑫期货  15665       5134  rb1901
38   海证期货  15444       -202  rb1901
39   中粮期货  13506        913  rb1901
40   东航期货  13312        600  rb1901
41   弘业期货  13267       -246  rb1901
42   申银万国  13233        631  rb1901
43   光大期货  10128      10128  rb1901
44   国投安信   8762       8762  rb1901
```
