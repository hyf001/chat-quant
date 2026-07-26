---
title: "futures_gfex_warehouse_receipt - 仓单日报-广州期货交易所"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, futures, parameters, returns, example]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# futures_gfex_warehouse_receipt

- 分类: [[futures-futures|AKShare 期货数据]]
- 主题路径: AKShare 期货数据 > 期货基础数据 > 仓单日报 > 仓单日报-广州期货交易所
- 描述: 广州期货交易所-行情数据-仓单日报
- 目标地址: http://www.gfex.com.cn/gfex/cdrb/hqsj_tjsj.shtml
- 限量: 单次返回当前交易日的所有仓单日报数据
- 来源页面: https://akshare.akfamily.xyz/data/futures/futures.html

## 相关

- [[futures-futures|AKShare 期货数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 仓单日报-广州期货交易所

接口: futures_gfex_warehouse_receipt

目标地址: http://www.gfex.com.cn/gfex/cdrb/hqsj_tjsj.shtml

描述: 广州期货交易所-行情数据-仓单日报

限量: 单次返回当前交易日的所有仓单日报数据

输入参数

| 名称   | 类型  | 描述                   |
|------|-----|----------------------|
| date | str | date="20240122"; 交易日 |

输出参数

| 名称    | 类型   | 描述                                     |
|-------|------|----------------------------------------|
| 键值对字典 | dict | 键值对, 键为品种代码, 值为 pandas.DataFrame 格式的数据 |

接口示例

```python
import akshare as ak

futures_gfex_warehouse_receipt_df = ak.futures_gfex_warehouse_receipt(date="20240122")
print(futures_gfex_warehouse_receipt_df)
```

数据示例

```
{'SI':      品种        仓库/分库  昨日仓单量  今日仓单量   增减
0   工业硅         中储吴淞    696    696    0
1   工业硅      中储大场137    732    732    0
2   工业硅      中储大场310   3192   3204   12
3   工业硅       中远海运宝山    828    828    0
4   工业硅       象屿速传上海   3144   3144    0
5   工业硅         中储无锡    240    240    0
6   工业硅         江苏诚通   2870   2906   36
7   工业硅        尖峰供应链    958   1210  252
8   工业硅        广州港物流    204    204    0
9   工业硅        国储830   2483   2483    0
10  工业硅         建发东莞   2096   2096    0
11  工业硅         广东炬申   1116   1116    0
12  工业硅         中储成都   1330   1330    0
13  工业硅         成都中集    500    500    0
14  工业硅         外运新都   1297   1297    0
15  工业硅        外运龙泉驿   1284   1320   36
16  工业硅         中储新港   1632   1668   36
17  工业硅         外运天津   1116   1164   48
18  工业硅       中远海运滨海    952    952    0
19  工业硅         建发天津   1968   2004   36
20  工业硅         外运昆明   3383   3323    0
21  工业硅        青岛港物流   2924   2924    0
22  工业硅       国贸泰达昆明    648    828  180
23  工业硅         云铝物流   4741   4729    0
24  工业硅  厦门国贸（青岛港物流）   1200   1200    0
25  工业硅   厦门国贸（国贸泰达）    840    840    0
26  工业硅   厦门国贸（外运天津）    660    660    0, 'LC':      品种       仓库/分库  昨日仓单量  今日仓单量   增减
0   碳酸锂      象屿速传上海   1954   2054  100
1   碳酸锂       外运龙泉驿    561    561    0
2   碳酸锂        中储临港    120    120    0
3   碳酸锂        建发上海    619    665   90
4   碳酸锂      中远海运镇江   1161   1151    0
5   碳酸锂        五矿无锡   1346   1346    0
6   碳酸锂      江苏奔牛港务     67     67    0
7   碳酸锂        遂宁天诚     87     87    0
8   碳酸锂  九岭锂业（宜春奉新）   1500   1500    0
9   碳酸锂        永兴特钢    280    280    0
10  碳酸锂    盛新锂能（遂宁）    970    970    0
11  碳酸锂      中远海运南昌   3389   3399   10
12  碳酸锂  九岭锂业（宜春宜丰）   1500   1500    0}
```
