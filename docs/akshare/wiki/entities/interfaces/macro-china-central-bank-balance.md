---
title: "macro_china_central_bank_balance - 央行货币当局资产负债"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_central_bank_balance

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 央行货币当局资产负债
- 描述: 新浪财经-中国宏观经济数据-央行货币当局资产负债
- 目标地址: http://finance.sina.com.cn/mac/#fininfo-8-0-31-2
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 央行货币当局资产负债

接口: macro_china_central_bank_balance

目标地址: http://finance.sina.com.cn/mac/#fininfo-8-0-31-2

描述: 新浪财经-中国宏观经济数据-央行货币当局资产负债

限量: 单次返回所有历史数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称         | 类型      | 描述       |
|------------|---------|----------|
| 统计时间       | object  | 年月       |
| 国外资产       | float64 | 注意单位: 亿元 |
| 外汇         | float64 | 注意单位: 亿元 |
| 货币黄金       | float64 | 注意单位: 亿元 |
| 其他国外资产     | float64 | 注意单位: 亿元 |
| 对政府债权      | float64 | 注意单位: 亿元 |
| 其中:中央政府    | float64 | 注意单位: 亿元 |
| 对其他存款性公司债权 | float64 | 注意单位: 亿元 |
| 对其他金融性公司债权 | float64 | 注意单位: 亿元 |
| 对非货币金融机构债权 | float64 | 注意单位: 亿元 |
| 对非金融性公司债权  | float64 | 注意单位: 亿元 |
| 其他资产       | float64 | 注意单位: 亿元 |
| 总资产        | float64 | 注意单位: 亿元 |
| 储备货币       | float64 | 注意单位: 亿元 |
| 发行货币       | float64 | 注意单位: 亿元 |
| 金融性公司存款    | float64 | 注意单位: 亿元 |
| 其他存款性公司    | float64 | 注意单位: 亿元 |
| 其他金融性公司    | float64 | 注意单位: 亿元 |
| 对金融机构负债    | float64 | 注意单位: 亿元 |
| 准备金存款      | float64 | 注意单位: 亿元 |
| 非金融性公司存款   | float64 | 注意单位: 亿元 |
| 活期存款       | float64 | 注意单位: 亿元 |
| 债券         | float64 | 注意单位: 亿元 |
| 国外负债       | float64 | 注意单位: 亿元 |
| 政府存款       | float64 | 注意单位: 亿元 |
| 自有资金       | float64 | 注意单位: 亿元 |
| 其他负债       | float64 | 注意单位: 亿元 |
| 总负债        | float64 | 注意单位: 亿元 |

接口示例

```python
import akshare as ak

macro_china_central_bank_balance_df = ak.macro_china_central_bank_balance()
print(macro_china_central_bank_balance_df)
```

数据示例

```
        统计时间  国外资产         外汇  ...    自有资金     其他负债        总负债
0     2023.7  231736.57  217824.72  ...  219.75  6064.21  408091.68
1     2023.6  231574.38  217733.71  ...  219.75  6544.37  418062.84
2     2023.5  231469.31  217822.22  ...  219.75  6674.58  406420.84
3     2023.4  231338.37  217895.06  ...  219.75  6784.49  412654.20
4     2023.3  230941.18  217893.63  ...  219.75  6690.57  421007.27
..       ...        ...        ...  ...     ...      ...        ...
314   1994.3    2437.60    2253.80  ...  280.50  -298.60        NaN
315  1993.12    1549.50    1431.80  ...  310.30  -255.00        NaN
316   1993.9    1451.00    1332.20  ...  310.30  -286.50        NaN
317   1993.6    1286.50    1183.00  ...  310.30  -411.60        NaN
318   1993.3    1324.00    1222.00  ...  310.30  -384.10        NaN
[319 rows x 28 columns]
```
