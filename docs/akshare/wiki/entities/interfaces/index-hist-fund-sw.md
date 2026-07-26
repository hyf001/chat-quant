---
title: "index_hist_fund_sw - 基金指数历史行情"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# index_hist_fund_sw

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 申万宏源研究 > 基金指数历史行情
- 描述: 申万宏源研究-申万指数-指数发布-基金指数-历史行情
- 目标地址: https://www.swsresearch.com/institute_sw/allIndex/releasedIndex/fundDetail?code=807100
- 限量: 该接口返回指定 symbol 的数据
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 基金指数历史行情

接口: index_hist_fund_sw

目标地址: https://www.swsresearch.com/institute_sw/allIndex/releasedIndex/fundDetail?code=807100

描述: 申万宏源研究-申万指数-指数发布-基金指数-历史行情

限量: 该接口返回指定 symbol 的数据

输入参数

| 名称     | 类型  | 描述                                               |
|--------|-----|--------------------------------------------------|
| symbol | str | symbol="807200"; 基金指数代码                          |
| period | str | period="day"; choice of {"day", "week", "month"} |

输出参数

| 名称   | 类型      | 描述      |
|------|---------|---------|
| 日期   | object  | -       |
| 收盘指数 | float64 | -       |
| 开盘指数 | float64 | -       |
| 最高指数 | float64 | -       |
| 最低指数 | float64 | -       |
| 涨跌幅  | float64 | 注意单位: % |

接口示例

```python
import akshare as ak

index_hist_fund_sw_df = ak.index_hist_fund_sw(symbol="807200", period="day")
print(index_hist_fund_sw_df)
```

数据示例

```
        日期     收盘指数  开盘指数  最高指数  最低指数   涨跌幅
0     2005-12-30   369.78   0.0   0.0   0.0  0.00
1     2006-01-04   370.80   0.0   0.0   0.0  0.27
2     2006-01-05   371.72   0.0   0.0   0.0  0.25
3     2006-01-06   372.28   0.0   0.0   0.0  0.15
4     2006-01-09   372.64   0.0   0.0   0.0  0.10
          ...      ...   ...   ...   ...   ...
4430  2024-03-27  1041.49   0.0   0.0   0.0  0.01
4431  2024-03-28  1041.83   0.0   0.0   0.0  0.03
4432  2024-03-29  1042.52   0.0   0.0   0.0  0.07
4433  2024-04-01  1042.91   0.0   0.0   0.0  0.04
4434  2024-04-02  1043.30   0.0   0.0   0.0  0.04
[4435 rows x 6 columns]
```
