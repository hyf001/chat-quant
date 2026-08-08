---
title: "currency_boc_safe - 人民币汇率中间价"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fx, parameters, returns, example]
sources: [raw/data-dictionary/fx/fx.md]
confidence: high
---
# currency_boc_safe

- 分类: [[fx-fx|AKShare 外汇数据]]
- 主题路径: AKShare 外汇数据 > 人民币汇率中间价
- 描述: 外汇管理局-人民币汇率中间价
- 目标地址: https://www.safe.gov.cn/safe/rmbhlzjj/index.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/fx/fx.html

## 相关

- [[fx-fx|AKShare 外汇数据]]
- [[_meta/topic-map]]

## 源文摘录

### 人民币汇率中间价

接口: currency_boc_safe

目标地址: https://www.safe.gov.cn/safe/rmbhlzjj/index.html

描述: 外汇管理局-人民币汇率中间价

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称   | 类型      | 描述  |
|------|---------|-----|
| 日期   | object  | -   |
| 美元   | float64 | -   |
| 欧元   | float64 | -   |
| 日元   | float64 | -   |
| 港元   | float64 | -   |
| 英镑   | float64 | -   |
| 林吉特  | float64 | -   |
| 卢布   | float64 | -   |
| 澳元   | float64 | -   |
| 加元   | float64 | -   |
| 新西兰元 | float64 | -   |
| 新加坡元 | float64 | -   |
| 瑞士法郎 | float64 | -   |
| 兰特   | float64 | -   |
| 韩元   | float64 | -   |
| 迪拉姆  | float64 | -   |
| 里亚尔  | float64 | -   |
| 福林   | float64 | -   |
| 兹罗提  | float64 | -   |
| 丹麦克朗 | float64 | -   |
| 瑞典克朗 | float64 | -   |
| 挪威克朗 | float64 | -   |
| 里拉   | float64 | -   |
| 比索   | float64 | -   |
| 泰铢   | float64 | -   |

P.S. 人民币对马来西亚林吉特、俄罗斯卢布、南非兰特、韩元、阿联酋迪拉姆、沙特里亚尔、匈牙利福林、波兰兹罗提、丹麦克朗、瑞典克朗、挪威克朗、土耳其里拉、墨西哥比索、泰铢汇率中间价采取间接标价法，即100人民币折合多少外币。人民币对其它10种货币汇率中间价仍采取直接标价法，即100外币折合多少人民币。

接口示例

```python
import akshare as ak

currency_boc_safe_df = ak.currency_boc_safe()
print(currency_boc_safe_df)
```

数据示例

```
       日期        美元      欧元   日元  ...    挪威克朗     里拉      比索    泰铢
0     1994-01-01  870.00     NaN  7.7800  ...     NaN      NaN     NaN     NaN
1     1994-01-03  870.00     NaN  7.7800  ...     NaN      NaN     NaN     NaN
2     1994-01-04  870.00     NaN  7.7196  ...     NaN      NaN     NaN     NaN
3     1994-01-05  870.00     NaN  7.7196  ...     NaN      NaN     NaN     NaN
4     1994-01-06  870.00     NaN  7.7196  ...     NaN      NaN     NaN     NaN
          ...     ...     ...     ...  ...     ...      ...     ...     ...
7318  2023-09-11  721.48  781.40  4.9710  ...  145.79  368.808  242.47  484.82
7319  2023-09-12  719.86  779.52  4.9573  ...  146.60  371.740  239.65  487.87
7320  2023-09-13  718.94  779.19  4.9356  ...  147.20  372.274  238.83  489.51
7321  2023-09-14  718.74  776.11  4.9174  ...  148.01  372.886  238.35  492.54
7322  2023-09-15  717.86  768.65  4.9064  ...  148.78  373.622  237.86  493.03
[7323 rows x 25 columns]
```
