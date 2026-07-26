---
title: "futures_hist_em - 内盘-历史行情数据-东财"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, futures, parameters, returns, example]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# futures_hist_em

- 分类: [[futures-futures|AKShare 期货数据]]
- 主题路径: 此处的合约需要是近期的合约, 否则会报错 > 内盘-历史行情数据-东财
- 描述: 东方财富网-期货行情-行情数据；其中 weekly, monthly 获取的成交额和持仓量未经验证
- 目标地址: https://qhweb.eastmoney.com/quote
- 限量: 单次返回指定 symbol 的所有数据; 只能获取当期合约;
- 来源页面: https://akshare.akfamily.xyz/data/futures/futures.html

## 相关

- [[futures-futures|AKShare 期货数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 内盘-历史行情数据-东财

接口: futures_hist_em

目标地址: https://qhweb.eastmoney.com/quote

描述: 东方财富网-期货行情-行情数据；其中 weekly, monthly 获取的成交额和持仓量未经验证

限量: 单次返回指定 symbol 的所有数据; 只能获取当期合约;

输入参数

| 名称         | 类型  | 描述                                                                 |
|------------|-----|--------------------------------------------------------------------|
| symbol     | str | symbol="热卷主连"; 具体合约可以通过 ak.futures_hist_table_em() 获取所有当期能获取数据的合约表 |
| period     | str | period="daily"; choice of {"daily", "weekly", "monthly"}           |
| start_date | str | start_date="19900101";                                             |
| end_date   | str | end_date="20500101";                                               |

输出参数

| 名称  | 类型      | 描述      |
|-----|---------|---------|
| 时间  | object  | -       |
| 开盘  | int64   | -       |
| 最高  | int64   | -       |
| 最低  | int64   | -       |
| 收盘  | int64   | -       |
| 涨跌  | int64   | -       |
| 涨跌幅 | float64 | 注意单位: % |
| 成交量 | int64   | -       |
| 成交额 | int64   | -       |
| 持仓量 | int64   | -       |

接口示例

```python
import akshare as ak

futures_hist_em_df = ak.futures_hist_em(symbol="热卷主连", period="daily")
print(futures_hist_em_df)
```

数据示例

```
          时间    开盘    最高    最低  ...   涨跌幅     成交量   成交额   持仓量
0     2014-03-21  3252  3336  3230  ...  0.00   93739            0    26015
1     2014-03-24  3314  3330  3266  ...  0.18   43405            0    23808
2     2014-03-25  3326  3400  3320  ...  1.44   59927            0    30628
3     2014-03-26  3370  3382  3354  ... -0.06   18938            0    30280
4     2014-03-27  3368  3386  3350  ... -0.41   20115            0    30715
...          ...   ...   ...   ...  ...   ...     ...          ...      ...
2636  2025-01-13  3316  3365  3313  ...  1.45  507472  16973149696  1170370
2637  2025-01-14  3357  3416  3348  ...  1.94  510296  17280815616  1167989
2638  2025-01-15  3400  3428  3391  ...  0.92  415364  14167324160  1158782
2639  2025-01-16  3415  3450  3411  ...  1.09  465334  15972707584  1157046
2640  2025-01-17  3447  3488  3436  ...  1.52  471470  16326870760  1196880
[2641 rows x 10 columns]
```
