---
title: "stock_dzjy_yybph - 营业部排行"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_dzjy_yybph

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 大宗交易 > 营业部排行
- 描述: 东方财富网-数据中心-大宗交易-营业部排行
- 目标地址: https://data.eastmoney.com/dzjy/dzjy_yybph.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 营业部排行

接口: stock_dzjy_yybph

目标地址: https://data.eastmoney.com/dzjy/dzjy_yybph.html

描述: 东方财富网-数据中心-大宗交易-营业部排行

限量: 单次返回所有历史数据

输入参数

| 名称     | 类型  | 描述                                                   |
|--------|-----|------------------------------------------------------|
| symbol | str | symbol='近三月'; choice of {'近一月', '近三月', '近六月', '近一年'} |

输出参数

| 名称          | 类型      | 描述      |
|-------------|---------|---------|
| 序号          | int64   | -       |
| 营业部名称       | object  | -       |
| 上榜后1天-买入次数  | float64 | -       |
| 上榜后1天-平均涨幅  | float64 | 注意单位: % |
| 上榜后1天-上涨概率  | float64 | -       |
| 上榜后5天-买入次数  | float64 | -       |
| 上榜后5天-平均涨幅  | float64 | 注意单位: % |
| 上榜后5天-上涨概率  | float64 | -       |
| 上榜后10天-买入次数 | float64 | -       |
| 上榜后10天-平均涨幅 | float64 | 注意单位: % |
| 上榜后10天-上涨概率 | float64 |         |
| 上榜后20天-买入次数 | float64 | -       |
| 上榜后20天-平均涨幅 | float64 | 注意单位: % |
| 上榜后20天-上涨概率 | float64 |         |

接口示例

```python
import akshare as ak

stock_dzjy_yybph_df = ak.stock_dzjy_yybph(symbol='近三月')
print(stock_dzjy_yybph_df)
```

数据示例

```
        序号               营业部名称  ...  上榜后20天-平均涨幅  上榜后20天-上涨概率
0        1                机构专用  ...     4.105711    52.522101
1        2     华泰证券营业总部(非营业场所)  ...     2.933068    51.394422
2        3       中信证券总部(非营业场所)  ...     7.533781    60.317460
3        4            国泰君安证券总部  ...     6.994607    60.606061
4        5      招商证券西安北大街证券营业部  ...     7.372532    67.346939
...    ...                 ...  ...          ...          ...
1226  1227           华福证券浙江分公司  ...          NaN          NaN
1227  1228    财通证券杭州富阳公望街证券营业部  ...          NaN          NaN
1228  1229   申万宏源证券重庆中山一路证券营业部  ...          NaN          NaN
1229  1230  国泰君安证券苏州苏州大道东证券营业部  ...          NaN          NaN
1230  1231           兴业证券莆田分公司  ...          NaN          NaN
[1231 rows x 14 columns]
```
