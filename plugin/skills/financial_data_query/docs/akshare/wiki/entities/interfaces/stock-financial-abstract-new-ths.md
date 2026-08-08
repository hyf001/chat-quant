---
title: "stock_financial_abstract_new_ths - 关键指标-同花顺"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_financial_abstract_new_ths

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 关键指标-同花顺
- 描述: 同花顺-财务指标-重要指标；替换 stock_financial_abstract_ths 接口
- 目标地址: https://basic.10jqka.com.cn/new/000063/finance.html
- 限量: 单次获取指定 symbol 的所有数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 关键指标-同花顺

接口: stock_financial_abstract_new_ths

目标地址: https://basic.10jqka.com.cn/new/000063/finance.html

描述: 同花顺-财务指标-重要指标；替换 stock_financial_abstract_ths 接口

限量: 单次获取指定 symbol 的所有数据

输入参数

| 名称        | 类型  | 描述                                                                      |
|-----------|-----|-------------------------------------------------------------------------|
| symbol    | str | symbol="000063"; 股票代码                                                   |
| indicator | str | indicator="按报告期"; choice of {"按报告期", "一季度", "二季度", "三季度", "四季度", "按年度"} |

输出参数

| 名称            | 类型      | 描述 |
|---------------|---------|----|
| report_date   | object  | -  |
| report_name   | object  | -  |
| report_period | object  | -  |
| quarter_name  | object  | -  |
| metric_name   | object  | -  |
| value         | float64 | -  |
| single        | object  | -  |
| yoy           | float64 | -  |
| mom           | object  | -  |
| single_yoy    | object  | -  |

接口示例

```python
import akshare as ak

stock_financial_abstract_new_ths_df = ak.stock_financial_abstract_new_ths(symbol="000063", indicator="按报告期")
print(stock_financial_abstract_new_ths_df)
```

数据示例

```
     report_date report_name  ...           mom   single_yoy
0     2025-09-30     2025三季报  ...    1.86837607  -0.54398564
1     2025-09-30     2025三季报  ...  -14.45035019  -8.51550645
2     2025-09-30     2025三季报  ...   -0.89847408  -0.87837202
3     2025-09-30     2025三季报  ...          <NA>         <NA>
4     2025-09-30     2025三季报  ...          <NA>         <NA>
...          ...         ...  ...           ...          ...
1195  2013-06-30      2013中报  ...   -0.49016497   0.25253313
1196  2013-06-30      2013中报  ...   -0.67334254   1.13728066
1197  2013-06-30      2013中报  ...          <NA>         <NA>
1198  2013-06-30      2013中报  ...    0.77759490   0.07845025
1199  2013-06-30      2013中报  ...   -0.49473684   0.26315789
[1200 rows x 10 columns]
```
