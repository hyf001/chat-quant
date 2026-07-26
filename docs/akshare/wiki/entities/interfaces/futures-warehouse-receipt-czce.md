---
title: "futures_warehouse_receipt_czce - 仓单日报-郑州商品交易所"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, futures, parameters, returns, example]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# futures_warehouse_receipt_czce

- 分类: [[futures-futures|AKShare 期货数据]]
- 主题路径: AKShare 期货数据 > 期货基础数据 > 仓单日报 > 仓单日报-郑州商品交易所
- 描述: 郑州商品交易所-交易数据-仓单日报
- 目标地址: http://www.czce.com.cn/cn/jysj/cdrb/H770310index_1.htm
- 限量: 单次返回当前交易日的所有仓单日报数据
- 来源页面: https://akshare.akfamily.xyz/data/futures/futures.html

## 相关

- [[futures-futures|AKShare 期货数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 仓单日报-郑州商品交易所

接口: futures_warehouse_receipt_czce

目标地址: http://www.czce.com.cn/cn/jysj/cdrb/H770310index_1.htm

描述: 郑州商品交易所-交易数据-仓单日报

限量: 单次返回当前交易日的所有仓单日报数据

输入参数

| 名称   | 类型  | 描述                   |
|------|-----|----------------------|
| date | str | date="20200702"; 交易日 |

输出参数

| 名称    | 类型   | 描述                                     |
|-------|------|----------------------------------------|
| 键值对字典 | dict | 键值对, 键为品种代码, 值为 pandas.DataFrame 格式的数据 |

接口示例

```python
import akshare as ak

futures_warehouse_receipt_czce_df = ak.futures_warehouse_receipt_czce(date="20200702")
print(futures_warehouse_receipt_czce_df)
```

数据示例

```
{'SR':     仓库编号       仓库简称    年度   等级   品牌   仓单数量 当日增减 有效预报   升贴水
0   0103       藁城永安   NaN  NaN  NaN      0    0  NaN   100
1   0112       津军粮城   NaN  NaN  NaN      0    0  NaN    80
2   0201      南京铁心桥   NaN  NaN  NaN      0    0  NaN   200
3   0404       荣桂钦州   NaN  NaN  NaN      0    0  NaN     0
4   0407       柳州桂糖   NaN  NaN  NaN      0    0  NaN     0
5   0409       云南广大  1920    1   康白    180    0  NaN  -170
6    NaN        NaN  1920    1  黎山雪     80    0  NaN   NaN
7    NaN        NaN  1920    1  三菁山     20    0  NaN   NaN
8    NaN        NaN  1920    1  仙人山     50    0  NaN   NaN
9     小计        NaN   NaN  NaN  NaN    330    0    0   NaN
10  0411       佛山华商   NaN  NaN  NaN      0    0  NaN    80
11  0415       营口港务   NaN  NaN  NaN      0    0  NaN    50
12  0417       中糖湖北  1920    1   绿原    407    0  NaN   240
13   NaN        NaN  1920    1   西沁    363    0  NaN   NaN
14    小计        NaN   NaN  NaN  NaN    770    0  230   NaN
15  0428      郑州南阳寨  1920    1   中糖   1431    0  NaN   140
16    小计        NaN   NaN  NaN  NaN   1431    0   79   NaN
17  0433       荣桂来宾   NaN  NaN  NaN      0    0  NaN     0
18  0434       广西贵港   NaN  NaN  NaN      0    0  NaN     0
19  0435       广西弘信   NaN  NaN  NaN      0    0  NaN     0
20  0436       营口北方   NaN  NaN  NaN      0    0  NaN    50
21  0437  日照凌云海(厂库)  1920    1  ALL    440  -50  NaN    50
22    小计        NaN   NaN  NaN  NaN    440  -50    0   NaN
23  0438      广东北部湾  1920    1   甘岭   1640    0  NaN     0
24    小计        NaN   NaN  NaN  NaN   1640    0    0   NaN
25  0440      中粮曹妃甸   NaN  NaN  NaN      0    0  NaN    50
26  0441       弘信扶绥   NaN  NaN  NaN      0    0  NaN     0
27  0444       中糖南通   NaN  NaN  NaN      0    0  NaN   180
28  0445   中粮屯河(厂库)  1920    1  ALL   5000    0  NaN    50
29    小计        NaN   NaN  NaN  NaN   5000    0    0   NaN
30  0447   星光糖业(厂库)   NaN  NaN  NaN      0    0  NaN   100
31  0449       陕西咸阳  1920    1   晶菱     50    0  NaN    80
32   NaN        NaN  1920    1   中糖   1490    0  NaN   NaN
33    小计        NaN   NaN  NaN  NaN   1540    0    0   NaN
34  0450       冀盛物流   NaN  NaN  NaN      0    0  NaN    50
35  0451       中糖北京   NaN  NaN  NaN      0    0  NaN    50
36  0452       云南陆航  1920    1  大湾江     40   40  NaN  -100
37    小计        NaN   NaN  NaN  NaN     40   40    0   NaN
38  0454       云鸥物流   NaN  NaN  NaN      0    0  NaN     0
39  0508       平湖华瑞   NaN  NaN  NaN      0    0  NaN   180
40    总计        NaN   NaN  NaN  NaN  11191  -10  309   NaN, 'CF':      仓库编号  仓库简称    年度    等级   产地   仓单数量  当日增减  有效预报
0    0301  河南国储  1920  1128   新疆      1     0   NaN
1     NaN   NaN  1920  1129   新疆      1     0   NaN
2     NaN   NaN  1920  1228   新疆      7     0   NaN
3     NaN   NaN  1920  1229   新疆      5     0   NaN
4     NaN   NaN  1920  2127   新疆      2     0   NaN
..    ...   ...   ...   ...  ...    ...   ...   ...
368   NaN   NaN  1920  3129   新疆     41     0   NaN
369   NaN   NaN  1920  3130   新疆      8     0   NaN
370   NaN   NaN  1920  4129   新疆      5     0   NaN
371    小计   NaN   NaN   NaN  NaN     86     0     1
372    总计   NaN   NaN   NaN  NaN  20641  -261  2203}
```
