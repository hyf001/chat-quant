---
title: "movie_boxoffice_cinema_daily - 影院票房-日票房排行"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, others, parameters, returns, example]
sources: [raw/data-dictionary/others/others.md]
confidence: high
---
# movie_boxoffice_cinema_daily

- 分类: [[others-others|AKShare 另类数据]]
- 主题路径: AKShare 另类数据 > 电影票房 > 影院票房-日票房排行
- 描述: 指定日期的每日各影院的票房数据
- 目标地址: https://www.endata.com.cn/BoxOffice/BO/Cinema/day.html
- 限量: 指定日期各影院的票房数据, 注意当前日期的数据需要第二日才可以获取
- 来源页面: https://akshare.akfamily.xyz/data/others/others.html

## 相关

- [[others-others|AKShare 另类数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 影院票房-日票房排行

接口: movie_boxoffice_cinema_daily

目标地址: https://www.endata.com.cn/BoxOffice/BO/Cinema/day.html

描述: 指定日期的每日各影院的票房数据

限量: 指定日期各影院的票房数据, 注意当前日期的数据需要第二日才可以获取

说明: 接口已迁移至艺恩当前 `ys.endata.cn/enlib-api` 数据源

输入参数

| 名称   | 类型  | 描述                         |
|------|-----|----------------------------|
| date | str | date="20240219"; 输入具体的日期即可 |

输出参数

| 名称   | 类型      | 描述      |
|------|---------|---------|
| 排序   | int64   | 票房排名    |
| 影院名称 | object  | -       |
| 单日票房 | float64 | 注意单位: 元 |
| 单日场次 | int64   | -       |
| 场均人次 | float64 | -       |
| 场均票价 | float64 | -       |
| 上座率  | float64 | 注意单位: % |

接口示例

```python
import akshare as ak

movie_boxoffice_cinema_daily_df = ak.movie_boxoffice_cinema_daily(date="20240219")
print(movie_boxoffice_cinema_daily_df)
```

数据示例

```
     排序            影院名称       单日票房  单日场次   场均人次    场均票价    上座率
0     1       廊坊市橙天国际影城  381255.31    46  56.61  146.41  42.69
1     2       阜阳颍州万达广场店  254175.95    72  68.56   51.49  34.26
2     3       庆阳市M3电影城堡  234791.42    49  85.02   56.36  61.32
3     4  北京耀莱成龙影城（五棵松店）  231814.17   107  41.48   52.23  22.59
4     5     厦门万达影城SM广场店  218179.01    84  51.15   50.77  28.54
..  ...             ...        ...   ...    ...     ...    ...
95   96      长垣县艾影汇国际影城  127034.18    54  43.65   53.90  34.51
96   97       呼和浩特万达广场店  126514.62    58  41.71   52.30  24.82
97   98       西安高新万达广场店  126260.37   109  21.03   55.09  17.56
98   99  阜阳市星轶影城（吾悦广场店）  126209.61    34  61.76   60.10  38.07
99  100     中影国际影城燕郊永旺店  126176.63    52  46.17   52.55  23.97
[100 rows x 7 columns]
```
