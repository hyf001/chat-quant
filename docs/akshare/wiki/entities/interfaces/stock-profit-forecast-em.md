---
title: "stock_profit_forecast_em - 盈利预测-东方财富"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_profit_forecast_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 盈利预测-东方财富
- 描述: 东方财富网-数据中心-研究报告-盈利预测; 该数据源网页端返回数据有异常, 本接口已修复该异常
- 目标地址: http://data.eastmoney.com/report/profitforecast.jshtml
- 限量: 单次返回指定 symbol 的数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

### 盈利预测-东方财富

接口: stock_profit_forecast_em

目标地址: http://data.eastmoney.com/report/profitforecast.jshtml

描述: 东方财富网-数据中心-研究报告-盈利预测; 该数据源网页端返回数据有异常, 本接口已修复该异常

限量: 单次返回指定 symbol 的数据

输入参数

| 名称     | 类型  | 描述                                                                                                 |
|--------|-----|----------------------------------------------------------------------------------------------------|
| symbol | str | symbol="", 默认为获取全部数据; symbol="船舶制造", 则获取具体行业板块的数据; 行业板块可以通过 ak.stock_board_industry_name_em() 接口获取 |

输出参数

| 名称              | 类型      | 描述  |
|-----------------|---------|-----|
| 序号              | int64   | -   |
| 代码              | object  | -   |
| 名称              | object  | -   |
| 研报数             | int64   | -   |
| 机构投资评级(近六个月)-买入 | float64 | -   |
| 机构投资评级(近六个月)-增持 | float64 | -   |
| 机构投资评级(近六个月)-中性 | float64 | -   |
| 机构投资评级(近六个月)-减持 | int64   | -   |
| 机构投资评级(近六个月)-卖出 | int64   | -   |
| xxxx预测每股收益      | float64 | -   |
| xxxx预测每股收益      | float64 | -   |
| xxxx预测每股收益      | float64 | -   |
| xxxx预测每股收益      | float64 | -   |

接口示例

```python
import akshare as ak

stock_profit_forecast_em_df = ak.stock_profit_forecast_em()
print(stock_profit_forecast_em_df)
```

数据示例

```
      序号  代码    名称  研报数  ...  2022预测每股收益  2023预测每股收益  2024预测每股收益  2025预测每股收益
0        1  600519  贵州茅台   57  ...   49.925612   58.933509   69.944737   81.378268
1        2  603605   珀莱雅   53  ...    2.060203    2.832283    3.571340    4.412750
2        3  000858   五粮液   52  ...    6.876187    7.795654    8.837846   10.038078
3        4  300957   贝泰妮   50  ...    2.481654    3.066469    3.869959    4.834542
4        5  300896   爱美客   47  ...    5.840074    8.793660   12.255915   16.379000
    ...     ...   ...  ...  ...         ...         ...         ...         ...
3026  3027  002428  云南锗业    1  ...   -0.095546    0.020000    0.050000    0.060000
3027  3028  688058   宝兰德    1  ...   -0.618857    1.060000    1.710000    2.660000
3028  3029  688309  恒誉环保    1  ...    0.182819    0.720000    0.810000    0.910000
3029  3030  300552  万集科技    1  ...   -0.136009   -0.050000    0.380000    0.670000
3030  3031  600637  东方明珠    1  ...    0.051296    0.280000    0.290000         NaN
[3031 rows x 13 columns]
```
