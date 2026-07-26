---
title: "futures_stock_shfe_js - 上海期货交易所"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, futures, parameters, returns, example]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# futures_stock_shfe_js

- 分类: [[futures-futures|AKShare 期货数据]]
- 主题路径: AKShare 期货数据 > 期货基础数据 > 库存周报 > 上海期货交易所
- 描述: 金十财经-上海期货交易所指定交割仓库库存周报
- 目标地址: https://datacenter.jin10.com/reportType/dc_shfe_weekly_stock
- 限量: 单次返回指定 date 的库存周报数据
- 来源页面: https://akshare.akfamily.xyz/data/futures/futures.html

## 相关

- [[futures-futures|AKShare 期货数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 上海期货交易所

接口: futures_stock_shfe_js

目标地址: https://datacenter.jin10.com/reportType/dc_shfe_weekly_stock

描述: 金十财经-上海期货交易所指定交割仓库库存周报

限量: 单次返回指定 date 的库存周报数据

输入参数

| 名称   | 类型  | 描述                                    |
|------|-----|---------------------------------------|
| date | str | date="20240419"; 库存周报只在每周的最后一个交易日公布数据 |

输出参数

| 名称           | 类型      | 描述 |
|--------------|---------|----|
| 商品           | object  | -  |
| 期货总量{随日期变动}  | int64   | -  |
| 期货总量{随日期变动}} | int64   | -  |
| 增减           | int64   | -  |
| 增减幅度         | float64 | -  |

接口示例

```python
import akshare as ak

futures_stock_shfe_js_df = ak.futures_stock_shfe_js(date="20240419")
print(futures_stock_shfe_js_df)
```

数据示例

```
           商品  期货总量2024-04-19  期货总量2024-04-12      增减   增减幅度
0          黄金            3078            3105     -27  -0.87
1           镍           23200           22774     426   1.87
2           锡           14486           14098     388   2.75
3           锌          131747          127634    4113   3.22
4           铝          228537          231765   -3228  -1.39
5           铜          300045          299723     322   0.11
6           铅           51746           60215   -8469 -14.06
7         螺纹钢          523732          521700    2032   0.39
8          线材          162052          162502    -450  -0.28
9          纸浆          451596          436461   15135   3.47
10     白银(千克)         4544581         4494032   50549   1.12
11        燃料油          183300          183300       0   0.00
12       热轧卷板          749487          744419    5068   0.68
13       沥青厂库          672180          672180       0   0.00
14       沥青仓库           75553           82453   -6900  -8.37
15       天然橡胶          216891          217721    -830  -0.38
16  中质含硫原油(桶)         5628000         6308000 -680000 -10.78
17       20号胶          141624          140737     887   0.63
```
