---
title: "stock_hk_index_spot_em - 实时行情数据-东财"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# stock_hk_index_spot_em

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 港股股票指数 > 实时行情数据-东财
- 描述: 东方财富网-行情中心-港股-指数实时行情
- 目标地址: https://quote.eastmoney.com/center/gridlist.html#hk_index
- 限量: 单次返回所有数据
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 实时行情数据-东财

接口: stock_hk_index_spot_em

目标地址: https://quote.eastmoney.com/center/gridlist.html#hk_index

描述: 东方财富网-行情中心-港股-指数实时行情

限量: 单次返回所有数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称   | 类型      | 描述       |
|------|---------|----------|
| 序号   | int64   | -        |
| 内部编号 | int64   | -        |
| 代码   | object  | -        |
| 名称   | object  | -        |
| 最新价  | float64 | -        |
| 涨跌额  | float64 | -        |
| 涨跌幅  | float64 | 注意单位: %  |
| 今开   | float64 | -        |
| 最高   | float64 | -        |
| 最低   | float64 | -        |
| 昨收   | float64 | -        |
| 成交量  | float64 | -        |
| 成交额  | float64 | 注意单位: 港元 |

接口示例

```python
import akshare as ak

stock_hk_index_spot_em_df = ak.stock_hk_index_spot_em()
print(stock_hk_index_spot_em_df)
```

数据示例

```
      序号  内部编号        代码  ...       昨收          成交量           成交额
0      1   124      HSSH  ...  3193.38          0.0  3.222019e+09
1      2   124  HSTECF2S  ...  3012.59          0.0           NaN
2      3   124    HST2SI  ...   669.27          0.0           NaN
3      4   124    HSCATI  ...  2948.24          0.0  8.038308e+09
4      5   124    HSCIEN  ...  9125.68  398107136.0  1.974318e+09
..   ...   ...       ...  ...      ...          ...           ...
354  355   124    HSCASI  ...  2444.56          0.0  1.127230e+10
355  356   124    HSSCID  ...  2102.39          0.0  3.358686e+09
356  357   124    HSSCPB  ...  1477.63          0.0  3.409686e+09
357  358   124     HSIDI  ...  1879.83          0.0  3.344741e+09
358  359   125    CESHKB  ...  5000.55          0.0  2.768274e+09
[359 rows x 13 columns]
```
