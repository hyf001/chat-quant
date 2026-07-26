---
title: "stock_zh_a_minute - 分时数据-新浪"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_zh_a_minute

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: AKShare 股票数据 > A股 > 历史行情数据 > 分时数据-新浪
- 描述: 新浪财经-沪深京 A 股股票或者指数的分时数据，目前可以获取 1, 5, 15, 30, 60 分钟的数据频率, 可以指定是否复权
- 目标地址: http://finance.sina.com.cn/realstock/company/sh600519/nc.shtml
- 限量: 单次返回指定股票或指数的指定频率的最近交易日的历史分时行情数据; 注意调用频率
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 分时数据-新浪

接口: stock_zh_a_minute

目标地址: http://finance.sina.com.cn/realstock/company/sh600519/nc.shtml

描述: 新浪财经-沪深京 A 股股票或者指数的分时数据，目前可以获取 1, 5, 15, 30, 60 分钟的数据频率, 可以指定是否复权

限量: 单次返回指定股票或指数的指定频率的最近交易日的历史分时行情数据; 注意调用频率

输入参数

| 名称     | 类型  | 描述                                                         |
|--------|-----|------------------------------------------------------------|
| symbol | str | symbol='sh000300'; 同日频率数据接口                                |
| period | str | period='1'; 获取 1, 5, 15, 30, 60 分钟的数据频率                    |
| adjust | str | adjust=""; 默认为空: 返回不复权的数据; qfq: 返回前复权后的数据; hfq: 返回后复权后的数据; |

输出参数

| 名称     | 类型      | 描述  |
|--------|---------|-----|
| day    | object  | -   |
| open   | float64 | -   |
| high   | float64 | -   |
| low    | float64 | -   |
| close  | float64 | -   |
| volume | float64 | -   |
| amount | float64 | -   |

接口示例

```python
import akshare as ak

stock_zh_a_minute_df = ak.stock_zh_a_minute(symbol='sh600751', period='1', adjust="qfq")
print(stock_zh_a_minute_df)
```

数据示例

```
                      day  open  high   low  close  volume        amount
0     2026-02-05 13:53:00  3.91  3.91  3.90   3.90   20900    81593.0000
1     2026-02-05 13:54:00  3.91  3.91  3.90   3.91   18700    73076.0000
2     2026-02-05 13:55:00  3.91  3.91  3.90   3.91   12500    48832.0000
3     2026-02-05 13:56:00  3.90  3.91  3.90   3.90   13600    53093.0000
4     2026-02-05 13:57:00  3.90  3.91  3.90   3.90   36200   141190.0000
...                   ...   ...   ...   ...    ...     ...           ...
1965  2026-02-25 14:54:00  4.20  4.20  4.19   4.20  113600   476800.9888
1966  2026-02-25 14:55:00  4.19  4.20  4.19   4.19  255900  1073360.9803
1967  2026-02-25 14:56:00  4.20  4.21  4.19   4.21  745311  3132349.1281
1968  2026-02-25 14:57:00  4.21  4.22  4.20   4.21  367300  1545926.9902
1969  2026-02-25 15:00:00  4.20  4.20  4.20   4.20  845635  3551666.8430
[1970 rows x 7 columns]
```
