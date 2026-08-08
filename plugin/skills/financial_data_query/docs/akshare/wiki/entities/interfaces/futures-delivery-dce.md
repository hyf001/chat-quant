---
title: "futures_delivery_dce - 交割统计-大商所"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, futures, parameters, returns, example]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# futures_delivery_dce

- 分类: [[futures-futures|AKShare 期货数据]]
- 主题路径: AKShare 期货数据 > 期货基础数据 > 交割统计-大商所
- 描述: 大连商品交易所-交割统计
- 目标地址: http://www.dce.com.cn/dalianshangpin/xqsj/tjsj26/jgtj/jgsj/index.html
- 限量: 单次返回指定交易月份的交割统计数据
- 来源页面: https://akshare.akfamily.xyz/data/futures/futures.html

## 相关

- [[futures-futures|AKShare 期货数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 交割统计-大商所

接口: futures_delivery_dce

目标地址: http://www.dce.com.cn/dalianshangpin/xqsj/tjsj26/jgtj/jgsj/index.html

描述: 大连商品交易所-交割统计

限量: 单次返回指定交易月份的交割统计数据

输入参数

| 名称   | 类型  | 描述                  |
|------|-----|---------------------|
| date | str | date="202312"; 交易月份 |

输出参数

| 名称   | 类型     | 描述 |
|------|--------|----|
| 品种   | object | -  |
| 合约   | object | -  |
| 交割日期 | object | -  |
| 交割量  | int64  | -  |
| 交割金额 | int64  | -  |

接口示例

```python
import akshare as ak

futures_delivery_dce_df = ak.futures_delivery_dce(date="202312")
print(futures_delivery_dce_df)
```

数据示例

```
       品种    合约    交割日期    交割量       交割金额
0      豆二   b2312  2023-12-19   1400   61586000
1     苯乙烯  eb2312  2023-12-21   1220   49324600
2     乙二醇  eg2312  2023-12-05   1503   61021800
3     乙二醇  eg2312  2023-12-07    100    4027000
4     乙二醇  eg2312  2023-12-08    100    4027000
5     乙二醇  eg2312  2023-12-11    300   12081000
6     铁矿石   i2312  2023-12-05    100   10140000
7     铁矿石   i2312  2023-12-19   1100  111595000
8      焦炭   j2312  2023-12-05     50   12650000
9      鸡蛋  jd2312  2023-12-22      5     213350
10     鸡蛋  jd2312  2023-12-26      5     221800
11     鸡蛋  jd2312  2023-12-27      7     309470
12     鸡蛋  jd2312  2023-12-29     30    1299000
13     焦煤  jm2312  2023-12-14    200   29040000
14    聚乙烯   l2312  2023-12-19   1084   42525320
15     豆粕   m2312  2023-12-06   2751  107123940
16     豆粕   m2312  2023-12-11     14     550340
17     豆粕   m2312  2023-12-19    187    7242510
18    棕榈油   p2312  2023-12-19   1979  139499920
19  液化石油气  pg2312  2023-12-05    176   16892480
20  液化石油气  pg2312  2023-12-08     88    8349440
21  液化石油气  pg2312  2023-12-29    876   85550160
22    聚丙烯  pp2312  2023-12-19    329   12107200
23     粳米  rr2312  2023-12-06    350   12215000
24   聚氯乙烯   v2312  2023-12-19  20399  583717385
25     豆油   y2312  2023-12-11     28    2268000
26     豆油   y2312  2023-12-14      5     405000
27     豆油   y2312  2023-12-19     67    5496680
```
