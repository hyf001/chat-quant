---
title: "option_value_analysis_em - 期权价值分析-金融期权"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, option, parameters, returns, example]
sources: [raw/data-dictionary/option/option.md]
confidence: high
---
# option_value_analysis_em

- 分类: [[option-option|AKShare 期权数据]]
- 主题路径: AKShare 期权数据 > 期权价值分析-金融期权
- 描述: 东方财富网-数据中心-特色数据-期权价值分析
- 目标地址: https://data.eastmoney.com/other/valueAnal.html
- 限量: 单次返回所有数据
- 来源页面: https://akshare.akfamily.xyz/data/option/option.html

## 相关

- [[option-option|AKShare 期权数据]]
- [[_meta/topic-map]]

## 源文摘录

### 期权价值分析-金融期权

接口: option_value_analysis_em

目标地址: https://data.eastmoney.com/other/valueAnal.html

描述: 东方财富网-数据中心-特色数据-期权价值分析

限量: 单次返回所有数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称       | 类型      | 描述                                                        |
|----------|---------|-----------------------------------------------------------|
| 期权代码     | object  | -                                                         |
| 期权名称     | object  | -                                                         |
| 最新价      | float64 | -                                                         |
| 时间价值     | float64 | 注意: 指在期权剩余有效期内，合约标的价格变动有利于期权权利方的可能性。时间价值和内在价值共同构成期权的总价值。  |
| 内在价值     | float64 | 注意: 指假如期权立即履行时该期权的价值，只能为正数或者为零。内在价值与时间价值共同构成期权的总价值。       |
| 隐含波动率    | float64 | 注意: 指期权市场投资者在进行期权交易时对未来波动率的认识，且该认识已反映在期权的定价过程中。           |
| 理论价格     | float64 | 注意: 采用 Black-Scholes 期权定价模型，推导出的期权理论价格。                   |
| 标的名称     | object  | -                                                         |
| 标的最新价    | float64 | -                                                         |
| 标的近一年波动率 | float64 | 注意: 指一种衡量股票价格变化剧烈程度的指标，一般用百分数表示。股价波动率与认购期权、认沽期权价值均为正相关关系。 |
| 到期日      | object  | -                                                         |

接口示例

```python
import akshare as ak

option_value_analysis_em_df = ak.option_value_analysis_em()
print(option_value_analysis_em_df)
```

数据示例

```
     期权代码       期权名称     最新价  ...  标的最新价  标的近一年波动率  到期日
0    10008904  500ETF沽9月7000  1.1278  ...  6.054     26.54  2025-09-24
1    10008903  500ETF购9月7000  0.0863  ...  6.054     26.54  2025-09-24
2    10008896   50ETF沽9月2900  0.2159  ...  2.744     19.41  2025-09-24
3    10008895   50ETF购9月2900  0.0998  ...  2.744     19.41  2025-09-24
4    10008894    科创50沽9月1300  0.2361  ...  1.157     41.15  2025-09-24
..        ...            ...     ...  ...    ...       ...         ...
659  10008577   50ETF购2月2750  0.0153  ...  2.744     19.41  2025-02-26
660  10008576   50ETF购2月2700  0.0479  ...  2.744     19.41  2025-02-26
661  10008575   50ETF购2月2650  0.0946  ...  2.744     19.41  2025-02-26
662  10008574   50ETF购2月2600  0.1445  ...  2.744     19.41  2025-02-26
663  10008573   50ETF购2月2550  0.1933  ...  2.744     19.41  2025-02-26
[664 rows x 11 columns]
```
