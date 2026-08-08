---
title: "stock_rank_forecast_cninfo - 投资评级"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_rank_forecast_cninfo

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 机构推荐 > 投资评级
- 描述: 巨潮资讯-数据中心-评级预测-投资评级
- 目标地址: https://webapi.cninfo.com.cn/#/thematicStatistics
- 限量: 单次获取指定交易日的所有数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 投资评级

接口: stock_rank_forecast_cninfo

目标地址: https://webapi.cninfo.com.cn/#/thematicStatistics

描述: 巨潮资讯-数据中心-评级预测-投资评级

限量: 单次获取指定交易日的所有数据

输入参数

| 名称   | 类型  | 描述                   |
|------|-----|----------------------|
| date | str | date="20210910"; 交易日 |

输出参数

| 名称      | 类型      | 描述  |
|---------|---------|-----|
| 证券代码    | object  | -   |
| 证券简称    | object  | -   |
| 发布日期    | object  | -   |
| 研究机构简称  | object  | -   |
| 研究员名称   | object  | -   |
| 投资评级    | object  | -   |
| 是否首次评级  | object  | -   |
| 评级变化    | object  | -   |
| 前一次投资评级 | object  | -   |
| 目标价格-下限 | float64 | -   |
| 目标价格-上限 | float64 | -   |

接口示例

```python
import akshare as ak

stock_rank_forecast_cninfo_df = ak.stock_rank_forecast_cninfo(date="20230817")
print(stock_rank_forecast_cninfo_df)
```

数据示例

```
     证券代码  证券简称   发布日期 研究机构简称  ... 评级变化 前一次投资评级 目标价格-下限 目标价格-上限
0    000552  甘肃能化  2023-08-17   民生证券  ...   维持      增持     NaN     NaN
1    000552  甘肃能化  2023-08-17   山西证券  ...   未知     不评级     NaN     NaN
2    000552  甘肃能化  2023-08-17   开源证券  ...   维持      买入     NaN     NaN
3    000567  海德股份  2023-08-17   中信证券  ...   未知     不评级     NaN     NaN
4    000682  东方电子  2023-08-17   光大证券  ...   维持      买入     NaN     NaN
..      ...   ...         ...    ...  ...  ...     ...     ...     ...
329  688668  鼎通科技  2023-08-17   民生证券  ...   维持      增持     NaN     NaN
330  688981  中芯国际  2023-08-17   中信建投  ...   未知     不评级     NaN     NaN
331  688981  中芯国际  2023-08-17   中泰证券  ...   维持      买入     NaN     NaN
332  836419  万德股份  2023-08-17   开源证券  ...   未知     不评级     NaN     NaN
333  839371  欧福蛋业  2023-08-17   开源证券  ...   维持      增持     NaN     NaN
[334 rows x 11 columns]
```
