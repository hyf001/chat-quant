---
title: "stock_comment_detail_scrd_desire_em - 市场参与意愿"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_comment_detail_scrd_desire_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 千股千评详情 > 市场热度 > 市场参与意愿
- 描述: 东方财富网-数据中心-特色数据-千股千评-市场热度-市场参与意愿
- 目标地址: https://data.eastmoney.com/stockcomment/stock/600000.html
- 限量: 单次获取所有数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 市场参与意愿

接口: stock_comment_detail_scrd_desire_em

目标地址: https://data.eastmoney.com/stockcomment/stock/600000.html

描述: 东方财富网-数据中心-特色数据-千股千评-市场热度-市场参与意愿

限量: 单次获取所有数据

输入参数

| 名称     | 类型  | 描述              |
|--------|-----|-----------------|
| symbol | str | symbol="600000" |

输出参数

| 名称       | 类型      | 描述 |
|----------|---------|----|
| 交易日期     | object  | -  |
| 股票代码     | object  | -  |
| 参与意愿     | float64 | -  |
| 5日平均参与意愿 | float64 | -  |
| 参与意愿变化   | float64 | -  |
| 5日平均变化   | float64 | -  |

接口示例

```python
import akshare as ak

stock_comment_detail_scrd_desire_em_df = ak.stock_comment_detail_scrd_desire_em(symbol="600000")
print(stock_comment_detail_scrd_desire_em_df)
```

数据示例

```
   交易日期    股票代码   参与意愿  5日平均参与意愿  参与意愿变化  5日平均变化
0  2025-12-25  600000  47.31     51.41   -9.50   -4.04
1  2025-12-26  600000  35.05     50.74  -12.26    1.00
2  2025-12-29  600000  65.52     54.55   30.47    3.81
3  2025-12-30  600000  52.52     51.44  -13.00   -3.10
4  2025-12-31  600000  51.85     50.45    1.00    1.00
```
