---
title: "stock_intraday_sina - 日内分时数据-新浪"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_intraday_sina

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 日内分时数据-新浪
- 描述: 新浪财经-日内分时数据
- 目标地址: https://vip.stock.finance.sina.com.cn/quotes_service/view/cn_bill.php?symbol=sz000001
- 限量: 单次返回指定交易日的分时数据；只能获取近期的数据，此处仅返回大单数据（成交量大于等于: 400手）
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 日内分时数据-新浪

接口: stock_intraday_sina

目标地址: https://vip.stock.finance.sina.com.cn/quotes_service/view/cn_bill.php?symbol=sz000001

描述: 新浪财经-日内分时数据

限量: 单次返回指定交易日的分时数据；只能获取近期的数据，此处仅返回大单数据（成交量大于等于: 400手）

输入参数

| 名称     | 类型  | 描述                            |
|--------|-----|-------------------------------|
| symbol | str | symbol="sz000001"; 带市场标识的股票代码 |
| date   | str | date="20240321"; 交易日          |

输出参数

| 名称         | 类型      | 描述            |
|------------|---------|---------------|
| symbol     | object  | -             |
| name       | object  | -             |
| ticktime   | object  | -             |
| price      | float64 | -             |
| volume     | int64   | 注意单位: 股       |
| prev_price | float64 | -             |
| kind       | object  | D 表示卖盘，表示 是买盘 |

接口示例

```python
import akshare as ak

stock_intraday_sina_df = ak.stock_intraday_sina(symbol="sz000001", date="20240321")
print(stock_intraday_sina_df)
```

数据示例

```
        symbol  name  ticktime  price   volume  prev_price kind
0    sz000001  平安银行  09:25:00  10.45   437400        0.00    U
1    sz000001  平安银行  09:30:00  10.44    29100       10.45    D
2    sz000001  平安银行  09:30:03  10.45   356400       10.44    U
3    sz000001  平安银行  09:30:06  10.45    65500       10.45    D
4    sz000001  平安银行  09:30:09  10.46    35800       10.45    U
..        ...   ...       ...    ...      ...         ...  ...
818  sz000001  平安银行  14:56:03  10.46    22100       10.46    D
819  sz000001  平安银行  14:56:18  10.47    20700       10.46    U
820  sz000001  平安银行  14:56:24  10.47   156000       10.47    U
821  sz000001  平安银行  14:56:45  10.46    78900       10.47    D
822  sz000001  平安银行  15:00:00  10.47  1472200       10.46    E
[823 rows x 7 columns]
```
