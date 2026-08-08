---
title: "sunrise_monthly - 日出和日落-月"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, others, parameters, returns, example]
sources: [raw/data-dictionary/others/others.md]
confidence: high
---
# sunrise_monthly

- 分类: [[others-others|AKShare 另类数据]]
- 主题路径: AKShare 另类数据 > 日出和日落 > 日出和日落-月
- 描述: 中国各大城市-日出和日落时间, 数据区间从 19990101-至今, 推荐使用代理访问
- 目标地址: https://www.timeanddate.com/sun/china/
- 限量: 单次返回指定日期所在月份每天的数据, 如果是未来日期则为预测值
- 来源页面: https://akshare.akfamily.xyz/data/others/others.html

## 相关

- [[others-others|AKShare 另类数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 日出和日落-月

接口: sunrise_monthly

目标地址: https://www.timeanddate.com/sun/china/

描述: 中国各大城市-日出和日落时间, 数据区间从 19990101-至今, 推荐使用代理访问

限量: 单次返回指定日期所在月份每天的数据, 如果是未来日期则为预测值

输入参数

| 名称   | 类型  | 描述                         |
|------|-----|----------------------------|
| date | str | date="20240428"            |
| city | str | city="beijing"; 注意输入的城市的拼音 |

输出参数

| 名称         | 类型     | 描述                          |
|------------|--------|-----------------------------|
| date       | object | 日期-索引; XXXX-XX 格式           |
| feb        | object | 月份简称-随月份变化                  |
| Sunrise    | object | 日出                          |
| Sunset     | object | 日落                          |
| Length     | object | Daylength-Length            |
| Difference | object | Daylength-Difference        |
| Start      | object | Astronomical Twilight-Start |
| End        | object | Astronomical Twilight-End   |
| Start.1    | object | Nautical Twilight-Start     |
| End.1      | object | Nautical Twilight-End       |
| Start.2    | object | Civil Twilight-Start        |
| End.2      | object | Civil Twilight-End          |
| Time       | object | Solar Noon-Time             |
| Mil. km    | object | Solar Noon-Mil. km          |

接口示例

```python
import akshare as ak

sunrise_monthly_df = ak.sunrise_monthly(date="20240428", city="beijing")
print(sunrise_monthly_df)
```

数据示例

```
    date Apr          Sunrise  ...    End.2              Time Mil. mi
0   202404   1  5:58 am ↑ (83°)  ...  7:06 pm  12:18 pm (54.8°)  92.891
1   202404   2  5:56 am ↑ (83°)  ...  7:07 pm  12:17 pm (55.2°)  92.918
2   202404   3  5:55 am ↑ (82°)  ...  7:08 pm  12:17 pm (55.6°)  92.945
3   202404   4  5:53 am ↑ (82°)  ...  7:09 pm  12:17 pm (56.0°)  92.972
4   202404   5  5:52 am ↑ (81°)  ...  7:10 pm  12:17 pm (56.3°)  93.000
5   202404   6  5:50 am ↑ (81°)  ...  7:11 pm  12:16 pm (56.7°)  93.027
6   202404   7  5:48 am ↑ (80°)  ...  7:12 pm  12:16 pm (57.1°)  93.054
7   202404   8  5:47 am ↑ (80°)  ...  7:13 pm  12:16 pm (57.5°)  93.080
8   202404   9  5:45 am ↑ (79°)  ...  7:14 pm  12:15 pm (57.8°)  93.107
9   202404  10  5:44 am ↑ (79°)  ...  7:15 pm  12:15 pm (58.2°)  93.133
10  202404  11  5:42 am ↑ (78°)  ...  7:16 pm  12:15 pm (58.6°)  93.159
11  202404  12  5:41 am ↑ (78°)  ...  7:17 pm  12:15 pm (58.9°)  93.185
12  202404  13  5:39 am ↑ (77°)  ...  7:18 pm  12:14 pm (59.3°)  93.211
13  202404  14  5:38 am ↑ (77°)  ...  7:19 pm  12:14 pm (59.7°)  93.237
14  202404  15  5:36 am ↑ (76°)  ...  7:20 pm  12:14 pm (60.0°)  93.262
15  202404  16  5:35 am ↑ (76°)  ...  7:22 pm  12:14 pm (60.4°)  93.288
16  202404  17  5:33 am ↑ (75°)  ...  7:23 pm  12:13 pm (60.7°)  93.313
17  202404  18  5:32 am ↑ (75°)  ...  7:24 pm  12:13 pm (61.1°)  93.338
18  202404  19  5:30 am ↑ (75°)  ...  7:25 pm  12:13 pm (61.4°)  93.364
19  202404  20  5:29 am ↑ (74°)  ...  7:26 pm  12:13 pm (61.8°)  93.389
20  202404  21  5:27 am ↑ (74°)  ...  7:27 pm  12:13 pm (62.1°)  93.414
21  202404  22  5:26 am ↑ (73°)  ...  7:28 pm  12:12 pm (62.4°)  93.439
22  202404  23  5:25 am ↑ (73°)  ...  7:29 pm  12:12 pm (62.8°)  93.464
23  202404  24  5:23 am ↑ (72°)  ...  7:30 pm  12:12 pm (63.1°)  93.489
24  202404  25  5:22 am ↑ (72°)  ...  7:31 pm  12:12 pm (63.4°)  93.514
25  202404  26  5:21 am ↑ (71°)  ...  7:32 pm  12:12 pm (63.8°)  93.539
26  202404  27  5:19 am ↑ (71°)  ...  7:33 pm  12:12 pm (64.1°)  93.563
27  202404  28  5:18 am ↑ (71°)  ...  7:35 pm  12:11 pm (64.4°)  93.588
28  202404  29  5:17 am ↑ (70°)  ...  7:36 pm  12:11 pm (64.7°)  93.613
29  202404  30  5:15 am ↑ (70°)  ...  7:37 pm  12:11 pm (65.0°)  93.637
[30 rows x 14 columns]
```
