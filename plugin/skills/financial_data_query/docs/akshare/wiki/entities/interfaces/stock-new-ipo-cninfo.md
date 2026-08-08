---
title: "stock_new_ipo_cninfo - 新股发行"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_new_ipo_cninfo

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 机构推荐 > 新股发行
- 描述: 巨潮资讯-数据中心-新股数据-新股发行
- 目标地址: https://webapi.cninfo.com.cn/#/xinguList
- 限量: 单次获取近三年所有新股发行的数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 新股发行

接口: stock_new_ipo_cninfo

目标地址: https://webapi.cninfo.com.cn/#/xinguList

描述: 巨潮资讯-数据中心-新股数据-新股发行

限量: 单次获取近三年所有新股发行的数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称      | 类型      | 描述       |
|---------|---------|----------|
| 证劵代码    | object  | -        |
| 证券简称    | object  | -        |
| 上市日期    | object  | -        |
| 申购日期    | object  | -        |
| 发行价     | float64 | 注意单位: 元  |
| 总发行数量   | float64 | 注意单位: 万股 |
| 发行市盈率   | float64 | -        |
| 上网发行中签率 | float64 | 注意单位: %  |
| 摇号结果公告日 | object  | -        |
| 中签公告日   | object  | -        |
| 中签缴款日   | object  | -        |
| 网上申购上限  | float64 | -        |
| 上网发行数量  | float64 | -        |

接口示例

```python
import akshare as ak

stock_new_ipo_cninfo_df = ak.stock_new_ipo_cninfo()
print(stock_new_ipo_cninfo_df)
```

数据示例

```
     证劵代码  证券简称   上市日期  ...   中签缴款日  网上申购上限 上网发行数量
0    301592  六九一二         NaT  ...  2024-10-15    1.75  1750.00
1    301613  新铝时代         NaT  ...  2024-10-18    0.65  1162.70
2    301626  苏州天脉         NaT  ...  2024-10-17    0.70  1258.05
3    301628  强达电路         NaT  ...  2024-10-23    1.85  1884.40
4    603205   健尔康         NaT  ...  2024-10-29     NaN  1200.00
..      ...   ...         ...  ...         ...     ...      ...
926  301087  可孚医疗  2021-10-25  ...  2021-10-15    1.10  1918.55
927  605566  福莱蒽特  2021-10-25  ...  2021-10-13    1.30  3000.60
928  688255   凯尔达  2021-10-25  ...  2021-10-14    0.45   674.75
929  872925  锦好医疗  2021-10-25  ...  2021-10-08   51.63  1032.60
930  688737  中自科技  2021-10-22  ...  2021-10-14    0.50   734.70
[931 rows x 13 columns]
```
