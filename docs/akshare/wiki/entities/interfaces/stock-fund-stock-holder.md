---
title: "stock_fund_stock_holder - 基金持股"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_fund_stock_holder

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 基金持股
- 描述: 新浪财经-股本股东-基金持股
- 目标地址: https://vip.stock.finance.sina.com.cn/corp/go.php/vCI_FundStockHolder/stockid/600004.phtml
- 限量: 新浪财经-股本股东-基金持股所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 基金持股

接口: stock_fund_stock_holder

目标地址: https://vip.stock.finance.sina.com.cn/corp/go.php/vCI_FundStockHolder/stockid/600004.phtml

描述: 新浪财经-股本股东-基金持股

限量: 新浪财经-股本股东-基金持股所有历史数据

输入参数

| 名称     | 类型  | 描述                    |
|--------|-----|-----------------------|
| symbol | str | symbol="600004"; 股票代码 |

输出参数

| 名称     | 类型      | 描述      |
|--------|---------|---------|
| 基金名称   | object  | -       |
| 基金代码   | object  | -       |
| 持仓数量   | int64   | 注意单位: 股 |
| 占流通股比例 | float64 | 注意单位: % |
| 持股市值   | int64   | 注意单位: 元 |
| 占净值比例  | float64 | 注意单位: % |
| 截止日期   | object  | -       |

接口示例

```python
import akshare as ak

stock_fund_stock_holder_df = ak.stock_fund_stock_holder(symbol="601318")
print(stock_fund_stock_holder_df)
```

数据示例

```
    基金名称    基金代码      持仓数量  占流通股比例        持股市值  占净值比例        截止日期
0      银华沪深300价值ETF  562320    265300  0.0015    12981100   3.85  2023-01-05
1    华安沪深300增强策略ETF  561000     91200  0.0005     4425940   0.53  2023-01-04
2         华夏上证50ETF  510050  92794672  0.5076  4361350000   7.48  2022-12-31
3      华泰柏瑞沪深300ETF  510300  44522018  0.2436  2092530000   2.70  2022-12-31
4     易方达沪深300非银ETF  512070  34406219  0.1882  1617090000  29.08  2022-12-31
..              ...     ...       ...     ...         ...    ...         ...
995       安信民稳增长混合A  008809   1125037  0.0062    46779000   2.68  2022-09-30
996       建信上证50ETF  510800   1084221  0.0059    45081900   6.86  2022-09-30
997   国寿安保沪港深300ETF  517300   1016300  0.0056    42257800   2.09  2022-09-30
998      泰达宏利市值优选混合  162209   1013832  0.0055    42155100   6.45  2022-09-30
999      南方沪深300ETF  159925    961652  0.0053    39985500   2.52  2022-09-30
```
