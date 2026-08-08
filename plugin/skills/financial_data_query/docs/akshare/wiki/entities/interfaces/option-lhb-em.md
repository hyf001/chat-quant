---
title: "option_lhb_em - 期权龙虎榜-金融期权"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, option, parameters, returns, example]
sources: [raw/data-dictionary/option/option.md]
confidence: high
---
# option_lhb_em

- 分类: [[option-option|AKShare 期权数据]]
- 主题路径: AKShare 期权数据 > 期权龙虎榜-金融期权
- 描述: 东方财富网-数据中心-期货期权-期权龙虎榜单-金融期权
- 目标地址: https://data.eastmoney.com/other/qqlhb.html
- 限量: 单次返回指定 symbol, indicator 和 trade_date 的所有数据
- 来源页面: https://akshare.akfamily.xyz/data/option/option.html

## 相关

- [[option-option|AKShare 期权数据]]
- [[_meta/topic-map]]

## 源文摘录

### 期权龙虎榜-金融期权

接口: option_lhb_em

目标地址: https://data.eastmoney.com/other/qqlhb.html

描述: 东方财富网-数据中心-期货期权-期权龙虎榜单-金融期权

限量: 单次返回指定 symbol, indicator 和 trade_date 的所有数据

输入参数

| 名称         | 类型  | 描述                                                                                                  |
|------------|-----|-----------------------------------------------------------------------------------------------------|
| symbol     | str | symbol="510050"; choice of {"510050", "510300", "159919"}                                           |
| indicator  | str | indicator="期权交易情况-认沽交易量"; choice of {"期权交易情况-认沽交易量","期权持仓情况-认沽持仓量", "期权交易情况-认购交易量", "期权持仓情况-认购持仓量"} |
| trade_date | str | trade_date="20220121"                                                                               |

输出参数

| 名称      | 类型      | 描述                   |
|---------|---------|----------------------|
| 交易类型    | object  | -                    |
| 交易日期    | object  | -                    |
| 证券代码    | object  | -                    |
| 标的名称    | object  | -                    |
| 名次      | float64 | -                    |
| 机构      | object  | -                    |
| XX量     | float64 | 注意: 根据 indicator 而变化 |
| 增减      | float64 | -                    |
| 净XX量    | float64 | 注意: 根据 indicator 而变化 |
| 占总交易量比例 | float64 | -                    |

接口示例

```python
import akshare as ak

option_lhb_em_df = ak.option_lhb_em(symbol="510300", indicator="期权持仓情况-认沽持仓量", trade_date="20220121")
print(option_lhb_em_df)
```

数据示例

```
    交易类型        交易日期    证券代码    标的名称  ...      持仓量    增减   净持仓量  占总交易量比例
0  认沽持仓量  2022-01-21  510300  300ETF  ...   173021.0 -11602.0   -4494.0  0.083968
1  认沽持仓量  2022-01-21  510300  300ETF  ...   153486.0  14177.0  -35428.0  0.074487
2  认沽持仓量  2022-01-21  510300  300ETF  ...   127108.0  -4549.0  -29379.0  0.061686
3  认沽持仓量  2022-01-21  510300  300ETF  ...   125984.0    -20.0       NaN  0.061140
4  认沽持仓量  2022-01-21  510300  300ETF  ...   121145.0  -2193.0       NaN  0.058792
5  认沽持仓量  2022-01-21  510300  300ETF  ...  2060568.0 -25036.0 -350814.0  1.000000
6  认沽持仓量  2022-01-21  510300  300ETF  ...   700744.0  -4187.0  -65535.0  0.340073
```
