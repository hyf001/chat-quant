---
title: "macro_china_consumer_goods_retail - 社会消费品零售总额"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_consumer_goods_retail

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 社会消费品零售总额
- 描述: 东方财富-经济数据-社会消费品零售总额
- 目标地址: http://data.eastmoney.com/cjsj/xfp.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 社会消费品零售总额

接口: macro_china_consumer_goods_retail

目标地址: http://data.eastmoney.com/cjsj/xfp.html

描述: 东方财富-经济数据-社会消费品零售总额

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称      | 类型      | 描述       |
|---------|---------|----------|
| 月份      | object  | -        |
| 当月      | float64 | 注意单位: 亿元 |
| 同比增长    | float64 | 注意单位: %  |
| 环比增长    | float64 | 注意单位: %  |
| 累计      | float64 | 注意单位: 亿元 |
| 累计-同比增长 | float64 | 注意单位: %  |

接口示例

```python
import akshare as ak

macro_china_consumer_goods_retail_df = ak.macro_china_consumer_goods_retail()
print(macro_china_consumer_goods_retail_df)
```

数据示例

```
     月份       当月  同比增长       环比增长        累计  累计-同比增长
0    2022年10月份  40271.0  -0.5   6.692277  360575.0      0.6
1    2022年09月份  37745.0   2.5   4.101164  320305.0      0.7
2    2022年08月份  36258.0   5.4   1.081684  282560.0      0.5
3    2022年07月份  35870.0   2.7  -7.413143  246302.0     -0.2
4    2022年06月份  38742.0   3.1  15.485736  210432.0     -0.7
..         ...      ...   ...        ...       ...      ...
162  2008年05月份   8703.5  21.6   6.896340   42400.7     21.1
163  2008年04月份   8142.0  22.0   0.231436   33697.2     21.0
164  2008年03月份   8123.2  21.5  -2.770895   25555.2     20.6
165  2008年02月份   8354.7  19.1  -7.960517   17432.0     20.2
166  2008年01月份   9077.3  21.2   0.687720    9077.3     21.2
```
