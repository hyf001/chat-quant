---
title: "stock_profit_forecast_ths - 盈利预测-同花顺"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_profit_forecast_ths

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 盈利预测-同花顺
- 描述: 同花顺-盈利预测
- 目标地址: http://basic.10jqka.com.cn/new/600519/worth.html
- 限量: 单次返回指定 symbol 和 indicator 的数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

### 盈利预测-同花顺

接口: stock_profit_forecast_ths

目标地址: http://basic.10jqka.com.cn/new/600519/worth.html

描述: 同花顺-盈利预测

限量: 单次返回指定 symbol 和 indicator 的数据

输入参数

| 名称        | 类型  | 描述                                                                                    |
|-----------|-----|---------------------------------------------------------------------------------------|
| symbol    | str | symbol="600519"; 股票代码                                                                 |
| indicator | str | indicator="预测年报每股收益"; choice of {"预测年报每股收益", "预测年报净利润", "业绩预测详表-机构", "业绩预测详表-详细指标预测"} |

输出参数-预测年报每股收益

| 名称    | 类型      | 描述  |
|-------|---------|-----|
| 年度    | object  | -   |
| 预测机构数 | int64   | -   |
| 最小值   | float64 | -   |
| 均值    | float64 | -   |
| 最大值   | float64 | -   |
| 行业平均数 | float64 | -   |

接口示例-预测年报每股收益

```python
import akshare as ak

stock_profit_forecast_ths_df = ak.stock_profit_forecast_ths(symbol="600519", indicator="预测年报每股收益")
print(stock_profit_forecast_ths_df)
```

数据示例-预测年报每股收益

```
     年度  预测机构数    最小值     均值    最大值  行业平均数
0  2022     48  48.46  49.73  50.58   7.00
1  2023     48  56.01  58.31  61.53   8.45
2  2024     48  63.79  67.59  73.67  10.12
```

输出参数-预测年报净利润

| 名称    | 类型      | 描述  |
|-------|---------|-----|
| 年度    | object  | -   |
| 预测机构数 | int64   | -   |
| 最小值   | float64 | -   |
| 均值    | float64 | -   |
| 最大值   | float64 | -   |
| 行业平均数 | float64 | -   |

接口示例-预测年报净利润

```python
import akshare as ak

stock_profit_forecast_ths_df = ak.stock_profit_forecast_ths(symbol="600519", indicator="预测年报净利润")
print(stock_profit_forecast_ths_df)
```

数据示例-预测年报净利润

```
     年度  预测机构数     最小值      均值     最大值   行业平均数
0  2022     48  608.70  624.70  635.37   92.07
1  2023     48  703.55  732.50  772.89  109.92
2  2024     48  801.30  849.09  925.44  130.04
```

输出参数-业绩预测详表-机构

| 名称             | 类型      | 描述  |
|----------------|---------|-----|
| 机构名称           | object  | -   |
| 研究员            | object  | -   |
| 预测年报每股收益2022预测 | float64 | -   |
| 预测年报每股收益2023预测 | float64 | -   |
| 预测年报每股收益2024预测 | float64 | -   |
| 预测年报净利润2022预测  | object  | -   |
| 预测年报净利润2023预测  | object  | -   |
| 预测年报净利润2024预测  | object  | -   |
| 报告日期           | object  | -   |

接口示例-业绩预测详表-机构

```python
import akshare as ak

stock_profit_forecast_ths_df = ak.stock_profit_forecast_ths(symbol="600519", indicator="业绩预测详表-机构")
print(stock_profit_forecast_ths_df)
```

数据示例-业绩预测详表-机构

```
       机构名称          研究员  ...  预测年报净利润2024预测        报告日期
0      东方证券          叶书怀  ...        829.14亿  2023-03-07
1      中泰证券          范劲松  ...        848.80亿  2023-02-13
2      中信证券           李鑫  ...        832.79亿  2023-02-13
3      招银证券  Joseph Wong  ...        866.26亿  2023-02-06
4      华鑫证券          孙山山  ...        860.24亿  2023-01-03
5      开源证券          张宇光  ...        860.49亿  2023-01-03
6  群益证券(香港)          顾向君  ...        845.28亿  2023-01-03
7      财通证券           苏铖  ...        850.53亿  2023-01-02
8      东吴证券           汤军  ...        845.27亿  2022-12-30
9      东莞证券          魏红梅  ...        846.24亿  2022-12-30
```

输出参数-业绩预测详表-详细指标预测

| 名称        | 类型     | 描述  |
|-----------|--------|-----|
| 预测指标      | object | -   |
| 2019-实际值  | object | -   |
| 2020-实际值  | object | -   |
| 2021-实际值  | object | -   |
| 预测2022-平均 | object | -   |
| 预测2023-平均 | object | -   |
| 预测2024-平均 | object | -   |

接口示例-业绩预测详表-详细指标预测

```python
import akshare as ak

stock_profit_forecast_ths_df = ak.stock_profit_forecast_ths(symbol="600519", indicator="业绩预测详表-详细指标预测")
print(stock_profit_forecast_ths_df)
```

数据示例-业绩预测详表-详细指标预测

```
       预测指标 2019-实际值 2020-实际值  2021-实际值 预测2022-平均 预测2023-平均 预测2024-平均
0   营业收入(元)  854.30亿  949.15亿  1061.90亿  1268.88亿  1471.77亿  1691.60亿
1   营业收入增长率   15.10%   10.29%    11.71%    19.49%    15.99%    14.93%
2   利润总额(元)  587.83亿  661.97亿   745.28亿   883.27亿  1034.55亿  1198.90亿
3    净利润(元)  412.06亿  466.97亿   524.60亿   624.70亿   732.50亿   849.09亿
4    净利润增长率   17.05%   13.33%    12.34%    18.92%    17.23%    15.96%
5  每股现金流(元)    35.99    41.13     50.97     55.46     59.37     72.57
6  每股净资产(元)   108.27   128.42    150.88    177.18    210.97    251.11
7    净资产收益率   33.09%   31.41%    29.90%    28.62%    28.26%    27.64%
8   市盈率(动态)    53.98    47.63     42.40     35.65     30.41     26.24
```
