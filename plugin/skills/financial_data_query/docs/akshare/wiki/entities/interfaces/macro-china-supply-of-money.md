---
title: "macro_china_supply_of_money - 货币供应量"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_supply_of_money

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 货币供应量
- 描述: 新浪财经-中国宏观经济数据-货币供应量
- 目标地址: http://finance.sina.com.cn/mac/#fininfo-1-0-31-1
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 货币供应量

接口: macro_china_supply_of_money

目标地址: http://finance.sina.com.cn/mac/#fininfo-1-0-31-1

描述: 新浪财经-中国宏观经济数据-货币供应量

限量: 单次返回所有历史数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称                 | 类型      | 描述       |
|--------------------|---------|----------|
| 统计时间               | object  | 年月       |
| 货币和准货币（广义货币M2）     | float64 | 注意单位: 亿元 |
| 货币和准货币（广义货币M2）同比增长 | float64 | 注意单位: %  |
| 货币(狭义货币M1)         | float64 | 注意单位: 亿元 |
| 货币(狭义货币M1)同比增长     | float64 | 注意单位: %  |
| 流通中现金(M0)          | float64 | 注意单位: 亿元 |
| 流通中现金(M0)同比增长      | float64 | 注意单位: %  |
| 活期存款               | float64 | 注意单位: 亿元 |
| 活期存款同比增长           | float64 | 注意单位: %  |
| 准货币                | float64 | 注意单位: 亿元 |
| 准货币同比增长            | float64 | 注意单位: %  |
| 定期存款               | float64 | 注意单位: 亿元 |
| 定期存款同比增长           | float64 | 注意单位: %  |
| 储蓄存款出              | float64 | 注意单位: 亿元 |
| 储蓄存款同比增长           | float64 | 注意单位: %  |
| 其他存款               | float64 | 注意单位: 亿元 |
| 其他存款同比增长           | float64 | 注意单位: %  |

接口示例

```python
import akshare as ak

macro_china_supply_of_money_df = ak.macro_china_supply_of_money()
print(macro_china_supply_of_money_df)
```

数据示例

```
       统计时间 货币和准货币（广义货币M2） 货币和准货币（广义货币M2）同比增长  ... 储蓄存款同比增长       其他存款 其他存款同比增长
0    2020.8     2136800.00              10.40  ...     None  235344.24     None
1    2020.7     2125458.46              10.70  ...     None  240538.49     None
2    2020.6     2134948.66              11.10  ...     None  228402.91     None
3    2020.5     2100183.74              11.10  ...     None  233222.73     None
4    2020.4     2093533.83              11.10  ...     None  241313.38     None
..      ...            ...                ...  ...      ...        ...      ...
507  1978.5           None               None  ...     None       None     None
508  1978.4           None               None  ...     None       None     None
509  1978.3           None               None  ...     None       None     None
510  1978.2           None               None  ...     None       None     None
511  1978.1           None               None  ...     None       None     None
```
