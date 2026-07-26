---
title: "movie_boxoffice_cinema_weekly - 影院票房-周票房排行"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, others, parameters, returns, example]
sources: [raw/data-dictionary/others/others.md]
confidence: high
---
# movie_boxoffice_cinema_weekly

- 分类: [[others-others|AKShare 另类数据]]
- 主题路径: AKShare 另类数据 > 电影票房 > 影院票房-周票房排行
- 描述: 指定日期的完整周各影院的票房数据
- 目标地址: https://www.endata.com.cn/BoxOffice/BO/Cinema/week.html
- 限量: 指定日期的完整周各影院的票房数据, 注意当前日期的数据只能返回上周的数据
- 来源页面: https://akshare.akfamily.xyz/data/others/others.html

## 相关

- [[others-others|AKShare 另类数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 影院票房-周票房排行

接口: movie_boxoffice_cinema_weekly

目标地址: https://www.endata.com.cn/BoxOffice/BO/Cinema/week.html

描述: 指定日期的完整周各影院的票房数据

限量: 指定日期的完整周各影院的票房数据, 注意当前日期的数据只能返回上周的数据

说明: 艺恩新站公开影院周榜接口当前返回系统错误, 调用时会抛出明确的上游权限异常, 不再返回旧版 `JSONDecodeError`

输入参数

| 名称   | 类型  | 描述                         |
|------|-----|----------------------------|
| date | str | date="20240219"; 输入具体的日期即可 |

输出参数

| 名称     | 类型      | 描述      |
|--------|---------|---------|
| 排序     | int64   | 票房排名    |
| 影院名称   | object  | -       |
| 当周票房   | float64 | 注意单位: 万 |
| 单银幕票房  | float64 | 注意单位: 元 |
| 场均人次   | float64 | -       |
| 单日单厅票房 | float64 | -       |
| 单日单厅场次 | float64 | -       |

接口示例

```python
import akshare as ak

movie_boxoffice_cinema_weekly_df = ak.movie_boxoffice_cinema_weekly(date="20240219")
print(movie_boxoffice_cinema_weekly_df)
```

数据示例

```
     排序     影院名称   当周票房   单银幕票房   场均人次  单日单厅票房  单日单厅场次
0     1      鄢陵奥斯卡国际影城  672.0  112.00   4.00   22.40    0.20
1     2      睢县奥斯卡天空影城  528.0  528.00  22.00   88.00    0.17
2     3         台山天悦影城  489.3   69.90   1.00   13.98    0.20
3     4  东莞中影南方国际影城地王店  462.0   33.00   1.00    9.43    0.29
4     5      三明永安华夏大剧院  454.0   75.67   1.67   15.13    0.20
..  ...            ...    ...     ...    ...     ...     ...
95   96  乳源瑶族自治县华景汇聚影城    0.0    0.00   0.00    0.00    0.20
96   97      来宾金秀县秀河影院    0.0    0.00   0.00    0.00    1.00
97   98        灵川县大唐影院    0.0    0.00   0.00    0.00    0.33
98   99      闽清县六都国际影城    0.0    0.00   0.00    0.00    0.33
99  100         建瓯市电影院    0.0    0.00   0.00    0.00    0.25
[100 rows x 7 columns]
```
