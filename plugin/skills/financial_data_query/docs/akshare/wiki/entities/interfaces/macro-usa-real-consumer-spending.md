---
title: "macro_usa_real_consumer_spending - 美国实际个人消费支出季率初值报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_usa_real_consumer_spending

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 美国宏观 > 劳动力市场 > 消费者收入与支出 > 美国实际个人消费支出季率初值报告
- 描述: 美国实际个人消费支出季率初值报告, 数据区间从 20131107-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_usa_real_consumer_spending
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 美国实际个人消费支出季率初值报告

接口: macro_usa_real_consumer_spending

目标地址: https://datacenter.jin10.com/reportType/dc_usa_real_consumer_spending

描述: 美国实际个人消费支出季率初值报告, 数据区间从 20131107-至今

限量: 单次返回所有历史数据

输入参数

| 名称 | 类型   | 描述 |
|----|------|----|
| -  | -  - |

输出参数

| 名称  | 类型      | 描述      |
|-----|---------|---------|
| 商品  | object  | -       |
| 日期  | object  | -       |
| 今值  | float64 | 注意单位: % |
| 预测值 | float64 | 注意单位: % |
| 前值  | float64 | 注意单位: % |

接口示例

```python
import akshare as ak

macro_usa_real_consumer_spending_df = ak.macro_usa_real_consumer_spending()
print(macro_usa_real_consumer_spending_df)
```

数据示例

```
                 商品          日期   今值  预测值   前值
0    美国实际个人消费支出季率初值  2013-11-07  1.5  1.6  1.8
1    美国实际个人消费支出季率初值  2013-12-05  1.4  1.5  1.5
2    美国实际个人消费支出季率初值  2013-12-20  2.0  1.4  1.4
3    美国实际个人消费支出季率初值  2014-01-30  3.3  3.7  2.0
4    美国实际个人消费支出季率初值  2014-02-28  2.6  2.9  3.3
..              ...         ...  ...  ...  ...
124  美国实际个人消费支出季率初值  2023-12-21  3.1  3.6  3.6
125  美国实际个人消费支出季率初值  2024-01-25  2.8  NaN  3.1
126  美国实际个人消费支出季率初值  2024-02-28  3.0  2.8  3.1
127  美国实际个人消费支出季率初值  2024-03-28  3.3  3.0  3.1
128  美国实际个人消费支出季率初值  2024-04-25  NaN  NaN  3.3
[129 rows x 5 columns]
```
