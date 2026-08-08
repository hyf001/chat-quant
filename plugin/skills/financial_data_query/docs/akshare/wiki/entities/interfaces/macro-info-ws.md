---
title: "macro_info_ws - 宏观日历"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_info_ws

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 全球宏观 > 宏观日历
- 描述: 华尔街见闻-日历-宏观
- 目标地址: https://wallstreetcn.com/calendar
- 限量: 单次返回指定 date 的数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 宏观日历

接口: macro_info_ws

目标地址: https://wallstreetcn.com/calendar

描述: 华尔街见闻-日历-宏观

限量: 单次返回指定 date 的数据

输入参数

| 名称   | 类型  | 描述              |
|------|-----|-----------------|
| date | str | date="20240514" |

输出参数

| 名称  | 类型      | 描述 |
|-----|---------|----|
| 时间  | object  | -  |
| 地区  | object  | -  |
| 事件  | object  | -  |
| 重要性 | int64   | -  |
| 今值  | float64 | -  |
| 预期  | float64 | -  |
| 前值  | float64 | -  |
| 链接  | object  | -  |

接口示例

```python
import akshare as ak

macro_info_ws_df = ak.macro_info_ws(date="20240514")
print(macro_info_ws_df)
```

数据示例

```
                     时间  ...                                                 链接
0   2024-05-14 01:00:00  ...
1   2024-05-14 07:50:00  ...  https://wallstreetcn.com/calendar/JP111746/ove...
2   2024-05-14 07:50:00  ...  https://wallstreetcn.com/calendar/JP111747/ove...
3   2024-05-14 10:00:00  ...
4   2024-05-14 12:02:00  ...
5   2024-05-14 14:00:00  ...  https://wallstreetcn.com/calendar/UK121576/ove...
6   2024-05-14 14:00:00  ...  https://wallstreetcn.com/calendar/UK121563/ove...
7   2024-05-14 14:00:00  ...  https://wallstreetcn.com/calendar/UK121574/ove...
8   2024-05-14 14:00:00  ...  https://wallstreetcn.com/calendar/UK121573/ove...
9   2024-05-14 14:00:00  ...  https://wallstreetcn.com/calendar/UK121578/ove...
10  2024-05-14 14:00:00  ...  https://wallstreetcn.com/calendar/UK121577/ove...
11  2024-05-14 14:00:00  ...  https://wallstreetcn.com/calendar/DE112128/ove...
12  2024-05-14 14:00:00  ...  https://wallstreetcn.com/calendar/DE112139/ove...
13  2024-05-14 14:00:00  ...  https://wallstreetcn.com/calendar/DE112152/ove...
14  2024-05-14 14:00:00  ...  https://wallstreetcn.com/calendar/DE112151/ove...
15  2024-05-14 17:00:00  ...  https://wallstreetcn.com/calendar/EA152021/ove...
16  2024-05-14 17:00:00  ...  https://wallstreetcn.com/calendar/DE152230/ove...
17  2024-05-14 17:00:00  ...  https://wallstreetcn.com/calendar/DE152229/ove...
18  2024-05-14 18:00:00  ...  https://wallstreetcn.com/calendar/US151153/ove...
19  2024-05-14 20:30:00  ...  https://wallstreetcn.com/calendar/US111043/ove...
20  2024-05-14 20:30:00  ...  https://wallstreetcn.com/calendar/US111042/ove...
21  2024-05-14 20:30:00  ...  https://wallstreetcn.com/calendar/US111049/ove...
22  2024-05-14 20:30:00  ...  https://wallstreetcn.com/calendar/US111048/ove...
23  2024-05-14 20:30:00  ...  https://wallstreetcn.com/calendar/CA173202/ove...
24  2024-05-14 21:15:00  ...
25  2024-05-14 22:00:00  ...
26  2024-05-15 00:00:00  ...
27  2024-05-15 00:00:00  ...
[28 rows x 8 columns]
```
