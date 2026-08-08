---
title: "option_margin - 商品期权保证金"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, option, parameters, returns, example]
sources: [raw/data-dictionary/option/option.md]
confidence: high
---
# option_margin

- 分类: [[option-option|AKShare 期权数据]]
- 主题路径: AKShare 期权数据 > 商品期权 > 商品期权保证金
- 描述: 唯爱期货-期权保证金
- 目标地址: https://www.iweiai.com/qiquan/yuanyou
- 限量: 单次返回指定 symbol 的所有数据
- 来源页面: https://akshare.akfamily.xyz/data/option/option.html

## 相关

- [[option-option|AKShare 期权数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 商品期权保证金

接口: option_margin

目标地址: https://www.iweiai.com/qiquan/yuanyou

描述: 唯爱期货-期权保证金

限量: 单次返回指定 symbol 的所有数据

输入参数

| 名称     | 类型  | 描述                                                    |
|--------|-----|-------------------------------------------------------|
| symbol | str | symbol="原油"; 可以通过 ak.option_margin_symbol() 所有 symbol |

输出参数

| 名称        | 类型      | 描述 |
|-----------|---------|----|
| 合约标的      | object  | -  |
| 合约代码      | object  | -  |
| 结算价       | float64 | -  |
| 交易乘数      | int64   | -  |
| 买方权利金     | int64   | -  |
| 卖方保证金     | float64 | -  |
| 手续费单位     | object  | -  |
| 开仓手续费     | int64   | -  |
| 平今手续费     | int64   | -  |
| 平昨手续费     | int64   | -  |
| 手续费(开+平今) | int64   | -  |
| 更新时间      | object  | -  |

接口示例

```python
import akshare as ak

option_margin_df = ak.option_margin(symbol="原油期权")
print(option_margin_df)
```

数据示例

```
     合约标的     合约代码     结算价  ...  平昨手续费  手续费(开+平今)  更新时间
0    原油sc2508  sc2508C385  129.45  ...     10         10  2025-06-13 20:33:52
1    原油sc2508  sc2508C390  124.50  ...     10         10  2025-06-13 20:33:52
2    原油sc2508  sc2508C395  119.60  ...     10         10  2025-06-13 20:33:52
3    原油sc2508  sc2508C400  114.70  ...     10         10  2025-06-13 20:33:52
4    原油sc2508  sc2508C405  109.80  ...     10         10  2025-06-13 20:33:52
..        ...         ...     ...  ...    ...        ...                  ...
101  原油sc2509  sc2509P510   31.80  ...     10         10  2025-06-13 20:33:52
102  原油sc2509  sc2509P520   37.20  ...     10         10  2025-06-13 20:33:52
103  原油sc2509  sc2509P530   43.10  ...     10         10  2025-06-13 20:33:52
104  原油sc2509  sc2509P540   49.40  ...     10         10  2025-06-13 20:33:52
105  原油sc2509  sc2509P550   56.10  ...     10         10  2025-06-13 20:33:52
[106 rows x 12 columns]
```
