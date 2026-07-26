---
title: "movie_boxoffice_yearly_first_week - 年度首周票房"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, others, parameters, returns, example]
sources: [raw/data-dictionary/others/others.md]
confidence: high
---
# movie_boxoffice_yearly_first_week

- 分类: [[others-others|AKShare 另类数据]]
- 主题路径: AKShare 另类数据 > 电影票房 > 年度首周票房
- 描述: 指定日期所在年度的年度首周票房数据
- 目标地址: https://www.endata.com.cn/BoxOffice/BO/Year/firstWeek.html
- 限量: 指定日期所在年度的年度首周票房数据, 只能获取最近年度的数据
- 来源页面: https://akshare.akfamily.xyz/data/others/others.html

## 相关

- [[others-others|AKShare 另类数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 年度首周票房

接口: movie_boxoffice_yearly_first_week

目标地址: https://www.endata.com.cn/BoxOffice/BO/Year/firstWeek.html

描述: 指定日期所在年度的年度首周票房数据

限量: 指定日期所在年度的年度首周票房数据, 只能获取最近年度的数据

说明: 接口已迁移至艺恩当前 `ys.endata.cn/enlib-api` 年榜数据源, 其中 `首周天数` 依据上映日期按首周自然周区间估算

输入参数

| 名称   | 类型  | 描述                         |
|------|-----|----------------------------|
| date | str | date="20201018"; 输入具体的日期即可 |

输出参数

| 名称     | 类型     | 描述      |
|--------|--------|---------|
| 排序     | int64  | 票房排名    |
| 影片名称   | object | -       |
| 类型     | object | -       |
| 首周票房   | int64  | 注意单位: 万 |
| 占总票房比重 | int64  | 注意单位: % |
| 场均人次   | int64  | -       |
| 国家及地区  | object | -       |
| 上映日期   | object | -       |
| 首周天数   | int64  | -       |

接口示例

```python
import akshare as ak

movie_boxoffice_yearly_first_week_df = ak.movie_boxoffice_yearly_first_week(date="20201018")
print(movie_boxoffice_yearly_first_week_df)
```

数据示例

```
   排序                 影片名称  类型  首周票房  占总票房比重  场均人次  国家及地区        上映日期  首周天数
0   1                 鲨海逃生  灾难  2473      52     5  美国/英国  2020-01-10     3
1   2  紫罗兰永恒花园外传：永远与自动手记人偶  剧情  2342      48     6     日本  2020-01-10     3
2   3                动物特工局  动画  1489      33     6  中国/法国  2020-01-11     2
3   4                 为家而战  动作  1364      79     3  美国/英国  2020-01-10     3
4   5                   灭绝  科幻   997      62    10     美国  2020-01-18     2
5   6                 别告诉她  剧情   205      50     5  美国/中国  2020-01-10     3
6   7                 致敬英雄  剧情   199      54     6     中国  2020-01-10     3
7   8                格萨尔藏戏  剧情     0       0     1     中国  2020-08-21  -186
```
