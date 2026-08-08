---
title: "macro_china_xfzxx - 消费者信心指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_xfzxx

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 消费者信心指数
- 描述: 东方财富网-消费者信心指数
- 目标地址: https://data.eastmoney.com/cjsj/xfzxx.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 消费者信心指数

接口: macro_china_xfzxx

目标地址: https://data.eastmoney.com/cjsj/xfzxx.html

描述: 东方财富网-消费者信心指数

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称           | 类型      | 描述      |
|--------------|---------|---------|
| 月份           | object  | -       |
| 消费者信心指数-指数值  | float64 | -       |
| 消费者信心指数-同比增长 | float64 | 注意单位: % |
| 消费者信心指数-环比增长 | float64 | 注意单位: % |
| 消费者满意指数-指数值  | float64 | -       |
| 消费者满意指数-同比增长 | float64 | 注意单位: % |
| 消费者满意指数-环比增长 | float64 | 注意单位: % |
| 消费者预期指数-指数值  | float64 | -       |
| 消费者预期指数-同比增长 | float64 | 注意单位: % |
| 消费者预期指数-环比增长 | float64 | 注意单位: % |

接口示例

```python
import akshare as ak

macro_china_xfzxx_df = ak.macro_china_xfzxx()
print(macro_china_xfzxx_df)
```

数据示例

```
      月份  消费者信心指数-指数值  ...  消费者预期指数-同比增长  消费者预期指数-环比增长
0    2022年09月份         87.2  ...    -28.995984      0.568828
1    2022年08月份         87.0  ...    -26.134454     -1.897321
2    2022年07月份         87.9  ...    -25.581395     -1.538462
3    2022年06月份         88.9  ...    -27.949327      3.762828
4    2022年05月份         86.8  ...    -30.063796      1.036866
..         ...          ...  ...           ...           ...
184  2007年05月份        112.8  ...      2.975654      0.351494
185  2007年04月份        112.3  ...      2.430243      1.426025
186  2007年03月份        111.0  ...      0.718133     -1.232394
187  2007年02月份        111.8  ...      2.805430     -0.525394
188  2007年01月份        112.4  ...      3.442029     -0.609225
```
