---
title: "futures_to_spot_shfe - 期转现-上期所"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, futures, parameters, returns, example]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# futures_to_spot_shfe

- 分类: [[futures-futures|AKShare 期货数据]]
- 主题路径: AKShare 期货数据 > 期货基础数据 > 期转现-上期所
- 描述: 上海期货交易所-期转现数据
- 目标地址: https://tsite.shfe.com.cn/statements/dataview.html?paramid=kx
- 限量: 单次返回指定交易月份的期转现数据
- 来源页面: https://akshare.akfamily.xyz/data/futures/futures.html

## 相关

- [[futures-futures|AKShare 期货数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 期转现-上期所

接口: futures_to_spot_shfe

目标地址: https://tsite.shfe.com.cn/statements/dataview.html?paramid=kx

描述: 上海期货交易所-期转现数据

限量: 单次返回指定交易月份的期转现数据

输入参数

| 名称   | 类型  | 描述                  |
|------|-----|---------------------|
| date | str | date="202312"; 交易月份 |

输出参数

| 名称   | 类型      | 描述 |
|------|---------|----|
| 日期   | object  | -  |
| 合约   | object  | -  |
| 交割量  | float64 | -  |
| 期转现量 | float64 | -  |

注意:

1 铜、铜(BC)、铝、锌、铅、镍、锡、螺纹钢、线材、热轧卷板、天然橡胶、20号胶、低硫燃料油、燃料油、石油沥青、纸浆、不锈钢的数量单位为：吨；黄金的数量单位为：克；白银的数量单位为：千克；原油的数量单位为：桶。
2 交割量、期转现量为单向计算。

接口示例

```python
import akshare as ak

futures_to_spot_shfe_df = ak.futures_to_spot_shfe(date="202312")
print(futures_to_spot_shfe_df)
```

数据示例

```
       日期      合约       交割量    期转现量
0   2023-12-15  cu2312    7950.0     0.0
1   2023-12-11  bc2312    2750.0  2750.0
2   2023-12-13  bc2312     700.0   700.0
3   2023-12-15  bc2312    1900.0     0.0
4   2023-12-08  bc2312    1500.0  1500.0
5   2023-12-15  al2312    9400.0     0.0
6   2023-12-25  al2401     400.0   400.0
7   2023-12-26  al2401      25.0    25.0
8   2023-12-15  zn2312    4375.0     0.0
9   2023-12-15  pb2312   37800.0     0.0
10  2023-12-15  ni2312    2442.0     0.0
11  2023-12-15  sn2312     470.0     0.0
12  2023-12-15  au2312  702000.0     0.0
13  2023-12-15  ag2312  141990.0     0.0
14  2023-12-15  rb2312    5100.0     0.0
15  2023-12-15  hc2312   46200.0     0.0
16  2023-12-19  hc2401     900.0   900.0
17  2023-12-15  ss2312   11040.0     0.0
18  2023-12-12  ss2312     120.0   120.0
19  2023-12-29  sc2401  105000.0     0.0
20  2023-12-29  lu2401   15700.0     0.0
21  2023-12-29  fu2401  124540.0     0.0
22  2023-12-15  bu2312    5180.0     0.0
23  2023-12-01  nr2312    2000.0  2000.0
24  2023-12-04  nr2312     900.0   900.0
25  2023-12-15  nr2312    3600.0     0.0
26  2023-12-11  nr2312     900.0   900.0
27  2023-12-13  nr2402    1000.0  1000.0
28  2023-12-15  ao2312   28800.0     0.0
29  2023-12-15  sp2312   70060.0     0.0
```
