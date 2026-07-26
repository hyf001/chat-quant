---
title: "movie_boxoffice_daily - 单日票房"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, others, parameters, returns, example]
sources: [raw/data-dictionary/others/others.md]
confidence: high
---
# movie_boxoffice_daily

- 分类: [[others-others|AKShare 另类数据]]
- 主题路径: AKShare 另类数据 > 电影票房 > 单日票房
- 描述: 指定日期的电影票房数据, 每日 10:30, 12:30更新日票房，16:30 同时补充前 7 日票房
- 目标地址: https://www.endata.com.cn/BoxOffice/BO/Day/index.html
- 限量: 只能指定最近的日期
- 来源页面: https://akshare.akfamily.xyz/data/others/others.html

## 相关

- [[others-others|AKShare 另类数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 单日票房

接口: movie_boxoffice_daily

目标地址: https://www.endata.com.cn/BoxOffice/BO/Day/index.html

描述: 指定日期的电影票房数据, 每日 10:30, 12:30更新日票房，16:30 同时补充前 7 日票房

限量: 只能指定最近的日期

说明: 接口已迁移至艺恩当前 `ys.endata.cn/enlib-api` 数据源; 由于新站公开列表未返回口碑字段, `口碑指数` 当前统一返回空值

输入参数

| 名称   | 类型  | 描述                         |
|------|-----|----------------------------|
| date | str | date="20240219"; 只能选择最近的日期 |

输出参数

| 名称   | 类型      | 描述      |
|------|---------|---------|
| 排序   | int64   | 票房排名    |
| 影片名称 | object  | -       |
| 单日票房 | int64   | 注意单位: 万 |
| 环比变化 | float64 | 注意单位: % |
| 累计票房 | int64   | 注意单位: 万 |
| 平均票价 | int64   | 注意单位: 元 |
| 场均人次 | int64   | -       |
| 口碑指数 | float64 | -       |
| 上映天数 | int64   | -       |

接口示例

```python
import akshare as ak

movie_boxoffice_daily_df = ak.movie_boxoffice_daily(date="20240219")
print(movie_boxoffice_daily_df)
```

数据示例

```
   排序             影片名称   单日票房  环比变化    累计票房  平均票价  场均人次  口碑指数  上映天数
0   1             第二十条  12808 -23.0  158075    45    10  8.99    21
1   2            飞驰人生2  12693 -26.0  264702    46    10  9.04    17
2   3             热辣滚烫  13094 -29.0  297624    45    10  8.98    17
3   4         熊出没·逆转时空   9263 -27.0  156650    44    10  8.78    22
4   5               秋田     15  47.0      68    42    26  0.00    27
5   6           年会不能停！     17  18.0  128754    41    53  9.05     3
6   7        海王2：失落的王国     10  10.0   46449    39    62   NaN     6
7   8               孤军      7  14.0    2516    41    54  0.00   102
8   9  泰勒·斯威夫特：时代巡回演唱会      6   0.0    9590    48    51  0.00    11
9  10          八戒之天蓬下界     14 -64.0     342    42    10  0.00     2
```
