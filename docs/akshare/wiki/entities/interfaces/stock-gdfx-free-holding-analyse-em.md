---
title: "stock_gdfx_free_holding_analyse_em - 股东持股分析-十大流通股东"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_gdfx_free_holding_analyse_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 股东持股分析-十大流通股东
- 描述: 东方财富网-数据中心-股东分析-股东持股分析-十大流通股东
- 目标地址: https://data.eastmoney.com/gdfx/HoldingAnalyse.html
- 限量: 单次获取返回所有数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 股东持股分析-十大流通股东

接口: stock_gdfx_free_holding_analyse_em

目标地址: https://data.eastmoney.com/gdfx/HoldingAnalyse.html

描述: 东方财富网-数据中心-股东分析-股东持股分析-十大流通股东

限量: 单次获取返回所有数据

输入参数

| 名称   | 类型  | 描述                         |
|------|-----|----------------------------|
| date | str | date="20230930"; 财报发布季度最后日 |

输出参数

| 名称             | 类型      | 描述      |
|----------------|---------|---------|
| 序号             | int64   | -       |
| 股东名称           | object  | -       |
| 股东类型           | object  | -       |
| 股票代码           | object  | -       |
| 股票简称           | object  | -       |
| 报告期            | object  | -       |
| 期末持股-数量        | float64 | 注意单位: 股 |
| 期末持股-数量变化      | float64 | 注意单位: 股 |
| 期末持股-数量变化比例    | float64 | 注意单位: % |
| 期末持股-持股变动      | float64 | -       |
| 期末持股-流通市值      | float64 | 注意单位: 元 |
| 公告日            | object  | -       |
| 公告日后涨跌幅-10个交易日 | float64 | 注意单位: % |
| 公告日后涨跌幅-30个交易日 | float64 | 注意单位: % |
| 公告日后涨跌幅-60个交易日 | float64 | 注意单位: % |

接口示例

```python
import akshare as ak

stock_gdfx_free_holding_analyse_em_df = ak.stock_gdfx_free_holding_analyse_em(date="20230930")
print(stock_gdfx_free_holding_analyse_em_df)
```

数据示例

```
          序号  ... 公告日后涨跌幅-60个交易日
0          1  ...      -0.959312
1          2  ...      -0.959312
2          3  ...      -0.959312
3          4  ...      -0.959312
4          5  ...      -0.959312
      ...  ...            ...
53269  53270  ...       2.169464
53270  53271  ...       2.169464
53271  53272  ...       2.169464
53272  53273  ...       2.169464
53273  53274  ...       2.169464
[53274 rows x 15 columns]
```
