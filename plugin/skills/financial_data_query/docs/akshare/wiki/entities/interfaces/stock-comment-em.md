---
title: "stock_comment_em - 千股千评"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_comment_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 千股千评
- 描述: 东方财富网-数据中心-特色数据-千股千评
- 目标地址: https://data.eastmoney.com/stockcomment/
- 限量: 单次获取所有数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

### 千股千评

接口: stock_comment_em

目标地址: https://data.eastmoney.com/stockcomment/

描述: 东方财富网-数据中心-特色数据-千股千评

限量: 单次获取所有数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称    | 类型      | 描述      |
|-------|---------|---------|
| 序号    | int64   | -       |
| 代码    | object  | -       |
| 名称    | object  | -       |
| 最新价   | float64 | -       |
| 涨跌幅   | float64 | -       |
| 换手率   | float64 | 注意单位: % |
| 市盈率   | float64 | -       |
| 主力成本  | float64 | -       |
| 机构参与度 | float64 | -       |
| 综合得分  | float64 | -       |
| 上升    | int64   | 注意: 正负号 |
| 目前排名  | int64   | -       |
| 关注指数  | float64 | -       |
| 交易日   | float64 | -       |

接口示例

```python
import akshare as ak

stock_comment_em_df = ak.stock_comment_em()
print(stock_comment_em_df)
```

数据示例

```
        序号    代码    名称    最新价  ...    上升  目前排名  关注指数  交易日
0        1  000001     平安银行  10.50  ...  1090  1608  87.6  2024-09-25
1        2  000002    万  科Ａ   7.31  ...  -675   293  90.4  2024-09-25
2        3  000004     国华网安  15.28  ...  -643  4283  91.6  2024-09-25
3        4  000006     深振业Ａ   4.38  ...   704  4043  83.2  2024-09-25
4        5  000007      全新好   5.62  ...   -86  2940  73.2  2024-09-25
...    ...     ...      ...    ...  ...   ...   ...   ...         ...
5076  5077  688799     华纳药厂  40.10  ...  1005  2019  63.2  2024-09-25
5077  5078  688800      瑞可达  21.11  ...  -326  1166  63.6  2024-09-25
5078  5079  688819     天能股份  27.86  ...  -504   568  74.8  2024-09-25
5079  5080  688981     中芯国际  44.90  ...  1274  2669  79.6  2024-09-25
5080  5081  689009  九号公司-WD  40.34  ...  -519   574  70.8  2024-09-25
[5081 rows x 14 columns]
```
