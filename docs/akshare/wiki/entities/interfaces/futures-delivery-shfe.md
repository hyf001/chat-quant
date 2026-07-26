---
title: "futures_delivery_shfe - 交割统计-上期所"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, futures, parameters, returns, example]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# futures_delivery_shfe

- 分类: [[futures-futures|AKShare 期货数据]]
- 主题路径: AKShare 期货数据 > 期货基础数据 > 交割统计-上期所
- 描述: 上海期货交易所-交割统计
- 目标地址: https://tsite.shfe.com.cn/statements/dataview.html?paramid=kx
- 限量: 单次返回指定交易月份的交割统计数据
- 来源页面: https://akshare.akfamily.xyz/data/futures/futures.html

## 相关

- [[futures-futures|AKShare 期货数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 交割统计-上期所

接口: futures_delivery_shfe

目标地址: https://tsite.shfe.com.cn/statements/dataview.html?paramid=kx

描述: 上海期货交易所-交割统计

限量: 单次返回指定交易月份的交割统计数据

输入参数

| 名称   | 类型  | 描述                  |
|------|-----|---------------------|
| date | str | date="202312"; 交易月份 |

输出参数

| 名称       | 类型      | 描述                                        |
|----------|---------|-------------------------------------------|
| 品种       | object  | -                                         |
| 交割量-本月   | int64   | 注意单位: 手; 交割量单边计算; 交割数据统计期为上月 16 日到本月 15 日 |
| 交割量-比重   | float64 | 注意单位: %                                   |
| 交割量-本年累计 | int64   | 注意单位: 手; 交割量单边计算; 交割数据统计期为上月 16 日到本月 15 日 |
| 交割量-累计同比 | float64 | 注意单位: %                                   |

接口示例

```python
import akshare as ak

futures_delivery_shfe_df = ak.futures_delivery_shfe(date="202312")
print(futures_delivery_shfe_df)
```

数据示例

```
         品种  交割量-本月  交割量-比重  交割量-本年累计    交割量-累计同比
0         铜    1590    3.399833     57280    6.527804
1     铜(BC)    1470    3.143242     21835    4.398757
2         铝    1880    4.019929     74710  -33.431346
3         锌     875    1.870977     34845  -49.216644
4         铅    7560   16.165245     77230   16.126607
5         镍    2442    5.221631     26634   41.234489
6         锡     470    1.004982     24122   33.432902
7       氧化铝    1440    3.079094      5250         NaN
8        黄金    1365    2.918725      5418    5.552309
9        白银    9466   20.240768    124720   -6.371990
10      螺纹钢     510    1.090513     42330   95.700416
11       线材       0    0.000000       180         NaN
12     热轧卷板    4620    9.878761     92520   44.044839
13      不锈钢    2232    4.772596     73932   66.558529
14       原油     301    0.643616     40608   68.700926
15    低硫燃料油     372    0.795433     14172  -48.957320
16      燃料油    1730    3.699190     41964  406.200241
17     石油沥青     518    1.107619     24412  -41.923205
18    丁二烯橡胶       0         NaN         0         NaN
19     天然橡胶       0         NaN     32656  123.456959
20     20号胶     920    1.967199     16681    5.850625
21       纸浆    7006   14.980649    107528   73.214343
22  SCFIS欧线       0         NaN         0         NaN
23       总计   46767  100.000000    939027   14.213102
```
