---
title: "macro_cons_opec_month - 欧佩克报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_cons_opec_month

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 重要机构 > 欧佩克报告
- 描述: 欧佩克报告, 数据区间从 20170118-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_opec_report
- 限量: 单次返回所有历史数据, 以网页数据为准.
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 欧佩克报告

接口: macro_cons_opec_month

目标地址: https://datacenter.jin10.com/reportType/dc_opec_report

描述: 欧佩克报告, 数据区间从 20170118-至今

限量: 单次返回所有历史数据, 以网页数据为准.

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称    | 类型      | 描述  |
|-------|---------|-----|
| 日期    | object  | -   |
| 阿尔及利亚 | float64 | -   |
| 安哥拉   | float64 | -   |
| 厄瓜多尔  | float64 | -   |
| 加蓬    | float64 | -   |
| 伊朗    | float64 | -   |
| 伊拉克   | float64 | -   |
| 科威特   | float64 | -   |
| 利比亚   | float64 | -   |
| 尼日利亚  | float64 | -   |
| 沙特    | float64 | -   |
| 阿联酋   | float64 | -   |
| 委内瑞拉  | float64 | -   |
| 欧佩克产量 | float64 | -   |

接口示例

```python
import akshare as ak

macro_cons_opec_month_df = ak.macro_cons_opec_month()
print(macro_cons_opec_month_df)
```

数据示例

```
      日期  阿尔及利亚  安哥拉 加蓬  伊朗  ...   尼日利亚  沙特    阿联酋  委内瑞拉 欧佩克产量
0   2016/12  108.7  167.4  20.9  372.5  ...  147.4  1044.3  309.0  203.4  3302.9
1   2017/01  105.3  165.8  20.3  378.0  ...  153.3   980.9  295.8  200.7  3202.6
2   2017/02  105.7  163.9  19.8  381.9  ...  156.4   995.2  293.3  199.8  3208.6
3   2017/03  105.1  159.9  20.2  379.2  ...  145.6   990.5  290.9  198.2  3177.0
4   2017/04  105.6  166.7  20.5  379.2  ...  149.6   993.4  290.6  196.7  3197.4
..      ...    ...    ...   ...    ...  ...    ...     ...    ...    ...     ...
70  2023/01  101.5  115.5  18.3  255.7  ...  133.6  1031.9  304.5   68.6  2887.6
71  2023/02  101.7  108.4  19.6  257.1  ...  138.0  1036.1  304.2   70.0  2892.4
72  2023/03  101.3  100.7  20.3  256.7  ...  135.4  1040.5  303.8   69.5  2879.7
73  2023/04  100.5  108.5  20.5  263.0  ...  118.0  1050.0  302.8   72.4  2860.3
74  2023/05   97.4  114.5  21.0  267.9  ...  126.9   997.7  289.4   73.5  2806.5
[75 rows x 13 columns]
```
