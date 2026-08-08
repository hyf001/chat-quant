---
title: "movie_boxoffice_weekly - 单周票房"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, others, parameters, returns, example]
sources: [raw/data-dictionary/others/others.md]
confidence: high
---
# movie_boxoffice_weekly

- 分类: [[others-others|AKShare 另类数据]]
- 主题路径: AKShare 另类数据 > 电影票房 > 单周票房
- 描述: 指定日期所在完整周的票房数据, 影片周票房数据初始更新周期为每周二，下周二补充数据
- 目标地址: https://www.endata.com.cn/BoxOffice/BO/Week/oneWeek.html
- 限量: 指定日期所在完整周的票房数据
- 来源页面: https://akshare.akfamily.xyz/data/others/others.html

## 相关

- [[others-others|AKShare 另类数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 单周票房

接口: movie_boxoffice_weekly

目标地址: https://www.endata.com.cn/BoxOffice/BO/Week/oneWeek.html

描述: 指定日期所在完整周的票房数据, 影片周票房数据初始更新周期为每周二，下周二补充数据

限量: 指定日期所在完整周的票房数据

说明: 艺恩新站公开周榜接口当前返回权限限制, 调用时会抛出明确的上游权限异常, 不再返回旧版 `JSONDecodeError`

输入参数

| 名称   | 类型  | 描述                             |
|------|-----|--------------------------------|
| date | str | date="20240218"; 指定日期所在周必须已经完整 |

输出参数

| 名称   | 类型      | 描述      |
|------|---------|---------|
| 排序   | int64   | 票房排名    |
| 影片名称 | object  | -       |
| 排名变化 | int64   | -       |
| 单周票房 | int64   | 注意单位: 万 |
| 环比变化 | int64   | 注意单位: % |
| 累计票房 | int64   | 注意单位: 万 |
| 平均票价 | int64   | -       |
| 场均人次 | int64   | -       |
| 口碑指数 | float64 | -       |
| 上映天数 | int64   | -       |

接口示例

```python
import akshare as ak

movie_boxoffice_weekly_df = ak.movie_boxoffice_weekly(date="20240218")
print(movie_boxoffice_weekly_df)
```

数据示例

```
   排序     影片名称  排名变化  单周票房 环比变化 累计票房  平均票价 场均人次 口碑指数 上映天数
0   1       热辣滚烫  9999  208829  163  288355    49    40  9.02     9
1   2      飞驰人生2  9999  180105  139  255362    49    39  9.08     9
2   3       第二十条     1  114864  244  148245    48    39  9.03     9
3   4   熊出没·逆转时空    -1  106105  142  149889    47    41  8.98     9
4   5    我们一起摇太阳     2    4926    7    9512    49    16  9.20     9
5   6       红毯先生  9999    2977  -46    8488    54     8  8.52     9
6   7     年会不能停！    -2     264  -96  128733    45     9  9.06    52
7   8    八戒之天蓬下界    15     225  102     337    43     3   NaN     9
8   9  海王2：失落的王国     1     119  -88   46438    41    12  8.10    61
9  10   还是觉得你最好2     0      75    0      75    61    95   NaN    -5
```
