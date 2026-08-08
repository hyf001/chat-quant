---
title: "variety_all - 商品列表数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/commodity.md]
confidence: high
---
# variety_all

- 分类: [[qhkc-commodity|商品]]
- 主题路径: 商品 > 商品列表数据
- 描述: 商品列表数据接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/commodity.html

## 相关

- [[qhkc-commodity|商品]]
- [[_meta/topic-map]]

## 源文摘录

## 商品列表数据

### 接口名称

variety_all

### 接口描述

商品列表数据接口

### 请求参数

| 参数名        | 说明   | 举例         |
|:-----------|:-----|------------|
| csymbolode | 品种编码 | RB         |
| date       | 查询日期 | 2018-08-08 |

### 返回参数

| 参数名    | 类型     | 说明   |
|:-------|:-------|------|
| name   | string | 品种名称 |
| symbol | string | 品种编码 |
| market | string | 所在市场 |

### 示例代码

```python
from akshare import pro_api

pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
variety_all_df = pro.variety_all()
print(variety_all_df)
```

### 返回示例

```
   market name symbol
0     上期所  螺纹钢     RB
1     大商所  铁矿石      I
2     大商所   焦煤     JM
3     大商所   焦炭      J
4     郑商所   棉纱     CY
5     上期所   热卷     HC
6     郑商所   苹果     AP
7     郑商所   棉花     CF
8     郑商所   玻璃     FG
9     郑商所   甲醇     MA
10    郑商所   菜油     OI
11    郑商所   菜粕     RM
12    郑商所   硅铁     SF
13    郑商所   锰硅     SM
14    郑商所   白糖     SR
15    郑商所  PTA     TA
16    郑商所  动力煤     ZC
17    上期所   沪铜     CU
18    上期所   沪铝     AL
19    上期所   沪锌     ZN
20    上期所   沪铅     PB
21    上期所   沪镍     NI
22    上期所   沪锡     SN
23    上期所   沪金     AU
24    上期所   沪银     AG
25    上期所  燃料油     FU
26    上期所   沥青     BU
27    上期所   橡胶     RU
28    大商所   豆一      A
29    大商所   豆二      B
..    ...  ...    ...
35    大商所  棕榈油      P
36    大商所   PP     PP
37    大商所  PVC      V
38    大商所   豆油      Y
39    郑商所   强麦     WH
40    大商所  胶合板     BB
41    大商所  纤维板     FB
42    郑商所   稻谷     RI
43    郑商所  油菜籽     RS
44    郑商所   粳稻     JR
45    郑商所  晚籼稻     LR
46    上期所   线材     WR
47    上期所   原油     SC
48    郑商所   普麦     PM
49    上期所   纸浆     SP
50    大商所  乙二醇     EG
51    中金所   IF     IF
52    中金所   IC     IC
53    中金所   IH     IH
54    郑商所   红枣     CJ
55    郑商所   尿素     UR
56    上期所   NR     NR
57    大商所   粳米     RR
58    上期所  不锈钢     SS
59    大商所  苯乙烯     EB
60    郑商所   纯碱     SA
61    中金所   二债     TS
62    中金所   五债     TF
63    中金所   十债      T
64    大商所  LPG     PG
```
