---
title: "news_economic_baidu - 全球宏观事件"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# news_economic_baidu

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 全球宏观 > 全球宏观事件
- 描述: 全球宏观指标重大事件
- 目标地址: https://gushitong.baidu.com/calendar
- 限量: 单次返回指定 date 的所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 全球宏观事件

接口: news_economic_baidu

目标地址: https://gushitong.baidu.com/calendar

描述: 全球宏观指标重大事件

限量: 单次返回指定 date 的所有历史数据

输入参数

| 名称   | 类型  | 描述              |
|------|-----|-----------------|
| date | str | date="20241107" |

输出参数

| 名称  | 类型      | 描述      |
|-----|---------|---------|
| 日期  | object  | -       |
| 时间  | object  | -       |
| 地区  | object  | -       |
| 事件  | object  | -       |
| 公布  | float64 | -       |
| 预期  | float64 | -       |
| 前值  | float64 | -       |
| 重要性 | float64 | 数值越大越重要 |

接口示例

```python
import akshare as ak

news_economic_baidu_df = ak.news_economic_baidu(date="20241107")
print(news_economic_baidu_df)
```

数据示例

```
        日期     时间   地区  ...      预期       前值  重要性
0   2024-11-07  01:30   巴西  ...     NaN      -16.72    1
1   2024-11-07  02:00   巴西  ...   49.76       50.23    1
2   2024-11-07  05:30   巴西  ...   11.25       10.75    1
3   2024-11-07  06:30   美国  ...     NaN  3091171.16    1
4   2024-11-07  06:30   美国  ...     NaN     6004.39    1
..         ...    ...  ...  ...     ...         ...  ...
95  2024-11-07  20:00   英国  ...    4.75        5.00    2
96  2024-11-07  21:00  俄罗斯  ...     NaN     6285.00    1
97  2024-11-07  21:00   巴西  ...     NaN      -11.40    1
98  2024-11-07  21:00   巴西  ...     NaN       -0.40    1
99  2024-11-07  21:30   美国  ...  187.50      186.20    2
[100 rows x 8 columns]
```
