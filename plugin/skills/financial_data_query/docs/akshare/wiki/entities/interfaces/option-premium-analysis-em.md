---
title: "option_premium_analysis_em - 期权折溢价-金融期权"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, option, parameters, returns, example]
sources: [raw/data-dictionary/option/option.md]
confidence: high
---
# option_premium_analysis_em

- 分类: [[option-option|AKShare 期权数据]]
- 主题路径: AKShare 期权数据 > 期权折溢价-金融期权
- 描述: 东方财富网-数据中心-特色数据-期权折溢价
- 目标地址: https://data.eastmoney.com/other/premium.html
- 限量: 单次返回所有数据
- 来源页面: https://akshare.akfamily.xyz/data/option/option.html

## 相关

- [[option-option|AKShare 期权数据]]
- [[_meta/topic-map]]

## 源文摘录

### 期权折溢价-金融期权

接口: option_premium_analysis_em

目标地址: https://data.eastmoney.com/other/premium.html

描述: 东方财富网-数据中心-特色数据-期权折溢价

限量: 单次返回所有数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称    | 类型      | 描述                                                  |
|-------|---------|-----------------------------------------------------|
| 期权代码  | object  | -                                                   |
| 期权名称  | object  | -                                                   |
| 最新价   | float64 | -                                                   |
| 涨跌幅   | float64 | 注意单位: %;                                            |
| 行权价   | float64 | -                                                   |
| 折溢价率  | float64 | 注意: 折溢价反映的是投资者以现价买入某期权并持有至到期时，标的需要上升或下跌多少才能使这笔投资保本。 |
| 标的名称  | object  | -                                                   |
| 标的最新价 | float64 | -                                                   |
| 标的涨跌幅 | float64 | -                                                   |
| 盈亏平衡价 | float64 | 注意: 指期权投资者实现投资收益为零时标的证券的价格。                         |
| 到期日   | object  | -                                                   |

接口示例

```python
import akshare as ak

option_premium_analysis_em_df = ak.option_premium_analysis_em()
print(option_premium_analysis_em_df)
```

数据示例

```
     期权代码       期权名称     最新价   涨跌幅  ... 标的最新价  标的涨跌幅 盈亏平衡价 到期日
0    10007852     科创50沽3月450  0.0002   0.00  ...  1.157   6.05  0.450  2025-03-26
1    10007830    科创板50沽3月450  0.0002   0.00  ...  1.122   6.05  0.450  2025-03-26
2    10007708     科创50沽3月500  0.0003  50.00  ...  1.157   6.05  0.500  2025-03-26
3    10007688    科创板50沽3月500  0.0003  50.00  ...  1.122   6.05  0.500  2025-03-26
4    10007658     科创50沽3月550  0.0005  66.67  ...  1.157   6.05  0.550  2025-03-26
..        ...            ...     ...    ...  ...    ...    ...    ...         ...
659  10007651     科创50购3月650  0.4869  10.41  ...  1.157   6.05  1.137  2025-03-26
660  10008359    科创板50购6月750  0.3520  14.29  ...  1.122   6.05  1.102  2025-06-25
661  10008357     科创50购6月800  0.3361  15.50  ...  1.157   6.05  1.136  2025-06-25
662  10008883     科创50购9月800  0.3339  14.74  ...  1.157   6.05  1.134  2025-09-24
663  10008768  500ETF购6月4900  0.9787  -6.97  ...  6.054   1.71  5.879  2025-06-25
[664 rows x 11 columns]
```
