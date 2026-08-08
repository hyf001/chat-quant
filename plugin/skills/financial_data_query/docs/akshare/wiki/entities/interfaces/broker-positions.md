---
title: "broker_positions - 席位持仓数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/broker.md]
confidence: high
---
# broker_positions

- 分类: [[qhkc-broker|席位]]
- 主题路径: 席位 > 席位持仓数据
- 描述: 席位持仓数据接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/broker.html

## 相关

- [[qhkc-broker|席位]]
- [[_meta/topic-map]]

## 源文摘录

## 席位持仓数据

### 接口名称

broker_positions

### 接口描述

席位持仓数据接口

### 请求参数

| 参数名    | 说明   | 举例         |
|:-------|:-----|------------|
| broker | 席位   | 永安期货       |
| date   | 查询日期 | 2018-08-08 |

### 返回参数

| 参数名        | 类型     | 说明      |
|:-----------|:-------|---------|
| code       | string | 合约代号    |
| long       | int    | 多头持仓    |
| short      | int    | 空头持仓    |
| long_chge  | int    | 多头持仓变化量 |
| short_chge | int    | 空头持仓变化量 |
| symbol     | string | 品种编码    |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
broker_positions_df = pro.broker_positions(broker="永安期货", date="2018-08-08")
print(broker_positions_df)
```

### 返回示例

```
       code   long  long_chge  short  short_chge symbol
0     a1809   2354       -175      0           0      A
1     a1901   4247        426   5159         493      A
2    ag1812   6155        212  13692          99     AG
3    al1808    455         -5      0           0     AL
4    al1809   2284       -181      0           0     AL
5    al1810   2451        158      0           0     AL
6    al1811    633          0    544         544     AL
7    al1812    419          8      0           0     AL
8    ap1810   1311        -38   1506        -205     AP
9    ap1811      0          0    194         -14     AP
10   ap1901   4090         58   4735         233     AP
11   ap1905   4017         65   2386         -17     AP
12   au1812   2381       -226    837          98     AU
13    b1809      0      -1153      0           0      B
14    b1901      0          0    175         175      B
15   bu1812  18412       -654  24973        -689     BU
16    c1809   9137        966  11309        -613      C
17    c1811     23         16      0           0      C
18    c1901  13987     -12150  47226        5144      C
19    c1905   1928        429   6739          15      C
20   cf1809   7983        729   2337         -40     CF
21   cf1901  10338       -336  35354        -798     CF
22   cf1905  14971       1429   9244        2901     CF
23   cs1809   1768       -654   2343         629     CS
24   cs1901   2169        939   1108         -22     CS
25   cu1808      0          0      0           0     CU
26   cu1809   4197       -104   2658         -11     CU
27   cu1810   2288        436   3520         167     CU
28   cu1811   1021         33   2057           6     CU
29   cu1812    391          7      0           0     CU
..      ...    ...        ...    ...         ...    ...
82   ru1905    553        -33   2218         149     RU
83   sf1809   2117        161   4946         269     SF
84   sf1901   1373        351     74          74     SF
85   sm1809   2794       -609      0           0     SM
86   sm1901    958        135    816          91     SM
87   sn1809    401        -15    152           8     SN
88   sr1809      0          0  14071       -1029     SR
89   sr1901  16912      -1215  12602         634     SR
90   sr1905   3261       -263    920          -2     SR
91    t1809   3784        606    729        -992      T
92    t1812    376         -4   3688         855      T
93   ta1809  23345       2469   9325       -1143     TA
94   ta1811   3180       -165   3441       -1042     TA
95   ta1901  57249     -12008  22708        7136     TA
96   ta1903    373         69    338          34     TA
97   ta1905    451          5    401        -241     TA
98   tf1809   1264        375      0           0     TF
99    v1809   3182       -485  15277       -7299      V
100   v1901   7957       3085   7496        2581      V
101  wh1809     20          8    150           0     WH
102   y1809   2575       -326   7995         520      Y
103   y1901  25191        838  13977        1369      Y
104   y1905   2615        132   9344          53      Y
105  zc1809   5558      -6447   2611         616     ZC
106  zc1811    690        -81    710        -115     ZC
107  zc1901   3908      -2077   4385         769     ZC
108  zn1808    175        -15   1465        -230     ZN
109  zn1809   3858       -335   3482         353     ZN
110  zn1810   6913       1081   4272         -79     ZN
111  zn1811   1463          5   1057          34     ZN
```
