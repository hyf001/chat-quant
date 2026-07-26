---
title: "macro_china_gdzctz - 中国城镇固定资产投资"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_gdzctz

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 中国城镇固定资产投资
- 描述: 中国城镇固定资产投资, 数据区间从 200802 至今, 月度数据
- 目标地址: http://data.eastmoney.com/cjsj/gdzctz.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 中国城镇固定资产投资

接口: macro_china_gdzctz

目标地址: http://data.eastmoney.com/cjsj/gdzctz.html

描述: 中国城镇固定资产投资, 数据区间从 200802 至今, 月度数据

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称    | 类型      | 描述       |
|-------|---------|----------|
| 月份    | object  | -        |
| 当月    | float64 | 注意单位: 亿元 |
| 同比增长  | float64 | 注意单位: %  |
| 环比增长  | float64 | 注意单位: %  |
| 自年初累计 | float64 | 注意单位: 亿元 |

接口示例

```python
import akshare as ak

macro_china_gdzctz_df = ak.macro_china_gdzctz()
print(macro_china_gdzctz_df)
```

数据示例

```
        月份        当月   同比增长   环比增长      自年初累计
0    2022年10月份  50047.00   4.27  -7.84  471459.00
1    2022年09月份  54306.00   6.66  14.83  421412.00
2    2022年08月份  47294.00   6.57  -2.25  367106.00
3    2022年07月份  48382.00   3.75 -26.10  319812.00
4    2022年06月份  65466.00   5.62  24.89  271430.00
..         ...       ...    ...    ...        ...
158  2008年06月份  18171.78  29.49  53.29   58435.98
159  2008年05月份  11854.13  25.44  17.45   40264.20
160  2008年04月份  10093.14  25.37  -1.01   28410.07
161  2008年03月份  10195.65  27.31    NaN   18316.94
162  2008年02月份       NaN    NaN    NaN    8121.29
```
