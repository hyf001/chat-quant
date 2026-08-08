---
title: "movie_boxoffice_monthly - 单月票房"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, others, parameters, returns, example]
sources: [raw/data-dictionary/others/others.md]
confidence: high
---
# movie_boxoffice_monthly

- 分类: [[others-others|AKShare 另类数据]]
- 主题路径: AKShare 另类数据 > 电影票房 > 单月票房
- 描述: 获取指定日期所在月份的票房数据, 每月5号更新上月票房，并补充之前两个月票房
- 目标地址: https://www.endata.com.cn/BoxOffice/BO/Month/oneMonth.html
- 限量: 指定日期所在月份的票房数据, 只能获取最近月份的数据
- 来源页面: https://akshare.akfamily.xyz/data/others/others.html

## 相关

- [[others-others|AKShare 另类数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 单月票房

接口: movie_boxoffice_monthly

目标地址: https://www.endata.com.cn/BoxOffice/BO/Month/oneMonth.html

描述: 获取指定日期所在月份的票房数据, 每月5号更新上月票房，并补充之前两个月票房

限量: 指定日期所在月份的票房数据, 只能获取最近月份的数据

说明: 接口已迁移至艺恩当前 `ys.endata.cn/enlib-api` 数据源; 由于新站公开列表未返回口碑字段, `口碑指数` 当前统一返回空值

输入参数

| 名称   | 类型  | 描述                         |
|------|-----|----------------------------|
| date | str | date="20201019"; 输入具体的日期即可 |

输出参数

| 名称   | 类型      | 描述      |
|------|---------|---------|
| 排序   | int64   | 票房排名    |
| 影片名称 | object  | -       |
| 单月票房 | int64   | 注意单位: 万 |
| 月度占比 | float64 | 注意单位: % |
| 平均票价 | int64   | -       |
| 场均人次 | int64   | -       |
| 上映日期 | object  | -       |
| 口碑指数 | float64 | -       |
| 月内天数 | float64 | -       |

接口示例

```python
import akshare as ak

movie_boxoffice_monthly_df = ak.movie_boxoffice_monthly(date="20240218")
print(movie_boxoffice_monthly_df)
```

数据示例

```
     排序      影片名称 单月票房  月度占比 平均票价  场均人次  上映日期  口碑指数  月内天数
0     1       热辣滚烫  297624  31.8    49    42  2024-02-10  9.05  20.0
1     2      飞驰人生2  264702  28.3    49    40  2024-02-10  9.12  20.0
2     3       第二十条  158075  16.9    48    36  2024-02-10  9.06  20.0
3     4   熊出没·逆转时空  156645  16.8    47    43  2024-02-10  9.03  20.0
4     5     年会不能停！   14940   1.6    38     5  2023-12-29  9.07  29.0
5     6    我们一起摇太阳    9513   1.0    50    14  2024-02-10  9.24  20.0
6     7       红毯先生    8492   0.9    52    11  2024-02-10  8.54  20.0
7     8        金手指    5326   0.6    39     4  2023-12-30  8.10  29.0
8     9       临时劫案    5295   0.6    38     2  2024-01-19  7.95  29.0
9    10  海王2：失落的王国    2021   0.2    38     4  2023-12-20  8.12  29.0
10  999         其他   12222   1.3    38     2        None   NaN   NaN
```
