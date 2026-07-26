---
title: "stock_lhb_jgzz_sina - 龙虎榜-机构席位追踪"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_lhb_jgzz_sina

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 营业部详情数据-东财 > 龙虎榜-机构席位追踪
- 描述: 新浪财经-龙虎榜-机构席位追踪
- 目标地址: https://vip.stock.finance.sina.com.cn/q/go.php/vLHBData/kind/jgzz/index.phtml
- 限量: 单次返回指定 symbol 的所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 龙虎榜-机构席位追踪

接口: stock_lhb_jgzz_sina

目标地址: https://vip.stock.finance.sina.com.cn/q/go.php/vLHBData/kind/jgzz/index.phtml

描述: 新浪财经-龙虎榜-机构席位追踪

限量: 单次返回指定 symbol 的所有历史数据

输入参数

| 名称     | 类型  | 描述                                                                                |
|--------|-----|-----------------------------------------------------------------------------------|
| symbol | str | symbol="5"; choice of {"5": 最近 5 天; "10": 最近 10 天; "30": 最近 30 天; "60": 最近 60 天;} |

输出参数

| 名称    | 类型      | 描述      |
|-------|---------|---------|
| 股票代码  | object  | -       |
| 股票名称  | object  | -       |
| 累积买入额 | float64 | 注意单位: 万 |
| 买入次数  | float64 | -       |
| 累积卖出额 | float64 | 注意单位: 万 |
| 卖出次数  | float64 | -       |
| 净额    | float64 | 注意单位: 万 |

接口示例

```python
import akshare as ak

stock_lhb_jgzz_sina_df = ak.stock_lhb_jgzz_sina(symbol="5")
print(stock_lhb_jgzz_sina_df)
```

数据示例

```
     股票代码  股票名称  累积买入额  买入次数  累积卖出额  卖出次数  净额
0    688498  源杰科技  19589.28     6   3035.09     2  16554.19
1    300308  中际旭创  19269.73     1   9088.94     1  10180.79
2    603135  中重科技   5824.15     1      0.00     0   5824.15
3    003032  传智教育   5388.51     4    118.46     0   5270.05
4    688601   力芯微  10427.99     6   5463.37     4   4964.62
..      ...   ...       ...   ...       ...   ...       ...
192  000628  高新发展   8635.84     2  21545.41     3 -12909.57
193  300063  天龙集团   7426.88     1  20736.26     5 -13309.38
194  002463  沪电股份   4700.87     1  18997.89     3 -14297.02
195  300781  因赛集团  13758.05     2  39308.41     8 -25550.36
196  603259  药明康德      0.00     0  54874.30     3 -54874.30
[197 rows x 7 columns]
```
