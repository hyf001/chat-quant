---
title: "stock_institute_hold - 机构持股一览表"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_institute_hold

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 机构持股 > 机构持股一览表
- 描述: 新浪财经-机构持股-机构持股一览表
- 目标地址: https://vip.stock.finance.sina.com.cn/q/go.php/vComStockHold/kind/jgcg/index.phtml
- 限量: 单次获取所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 机构持股一览表

接口: stock_institute_hold

目标地址: https://vip.stock.finance.sina.com.cn/q/go.php/vComStockHold/kind/jgcg/index.phtml

描述: 新浪财经-机构持股-机构持股一览表

限量: 单次获取所有历史数据

输入参数

| 名称     | 类型  | 描述                                                                                                              |
|--------|-----|-----------------------------------------------------------------------------------------------------------------|
| symbol | str | symbol="20051"; 从 2005 年开始, {"一季报":1, "中报":2 "三季报":3 "年报":4}, e.g., "20191", 其中的 1 表示一季报; "20193", 其中的 3 表示三季报; |

输出参数

| 名称       | 类型      | 描述      |
|----------|---------|---------|
| 证券代码     | object  | -       |
| 证券简称     | object  | -       |
| 机构数      | int64   | -       |
| 机构数变化    | int64   | -       |
| 持股比例     | float64 | 注意单位: % |
| 持股比例增幅   | float64 | 注意单位: % |
| 占流通股比例   | float64 | 注意单位: % |
| 占流通股比例增幅 | float64 | 注意单位: % |

接口示例

```python
import akshare as ak

stock_institute_hold_df = ak.stock_institute_hold(symbol="20201")
print(stock_institute_hold_df)
```

数据示例

```
      证券代码  证券简称 机构数  机构数变化   持股比例  持股比例增幅  占流通股比例  占流通股比例增幅
0     002296  辉煌科技    1      1   0.85    0.85    0.85      0.85
1     300354  东华测试    1      0   0.21   -0.59    0.21     -0.59
2     000656  金科股份    1      0   2.12    0.04    2.14      0.03
3     002859  洁美科技    1      0   0.97    0.00    2.28      0.00
4     603866  桃李面包    1      0   1.34    0.00    1.34      0.00
      ...   ...  ...    ...    ...     ...     ...       ...
1790  300782   卓胜微   10      2   6.00    2.02   24.00      8.07
1791  300788  中信出版   10      0  10.26    2.88   41.03     11.50
1792  300785   值得买   10      1  11.62    4.14   46.48     16.56
1793  688188  柏楚电子   10      0   5.17   -0.13   21.43     -1.70
1794  300003  乐普医疗   16      1  11.16    0.99   11.78      1.05
[1795 rows x 8 columns]
```
