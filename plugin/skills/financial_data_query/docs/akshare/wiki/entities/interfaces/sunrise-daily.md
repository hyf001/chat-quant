---
title: "sunrise_daily - 日出和日落-天"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, others, parameters, returns, example]
sources: [raw/data-dictionary/others/others.md]
confidence: high
---
# sunrise_daily

- 分类: [[others-others|AKShare 另类数据]]
- 主题路径: AKShare 另类数据 > 日出和日落 > 日出和日落-天
- 描述: 中国各大城市-日出和日落时间, 数据区间从 19990101-至今, 推荐使用代理访问
- 目标地址: https://www.timeanddate.com/sun/china/
- 限量: 单次返回指定日期和指定城市的数据
- 来源页面: https://akshare.akfamily.xyz/data/others/others.html

## 相关

- [[others-others|AKShare 另类数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 日出和日落-天

接口: sunrise_daily

目标地址: https://www.timeanddate.com/sun/china/

描述: 中国各大城市-日出和日落时间, 数据区间从 19990101-至今, 推荐使用代理访问

限量: 单次返回指定日期和指定城市的数据

输入参数

| 名称   | 类型  | 描述                         |
|------|-----|----------------------------|
| date | str | date="20240428"            |
| city | str | city="beijing"; 注意输入的城市的拼音 |

输出参数

| 名称         | 类型     | 描述                          |
|------------|--------|-----------------------------|
| date       | object | 日期                          |
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

sunrise_daily_df = ak.sunrise_daily(date="20240428", city="beijing")
print(sunrise_daily_df)
```

数据示例

```
         date Apr          Sunrise  ...    End.2              Time Mil. mi
0  2024-04-28  28  5:18 am ↑ (71°)  ...  7:35 pm  12:11 pm (64.4°)  93.588
[1 rows x 14 columns]
```
