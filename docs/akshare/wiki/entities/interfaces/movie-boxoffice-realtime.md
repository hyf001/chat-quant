---
title: "movie_boxoffice_realtime - 实时票房"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, others, parameters, returns, example]
sources: [raw/data-dictionary/others/others.md]
confidence: high
---
# movie_boxoffice_realtime

- 分类: [[others-others|AKShare 另类数据]]
- 主题路径: AKShare 另类数据 > 电影票房 > 实时票房
- 描述: 当前时刻的实时电影票房数据, 每 5 分钟更新一次数据, 实时票房包含今天未开映场次已售出的票房
- 目标地址: https://ys.endata.cn/BoxOffice/Movie
- 限量: 当前时刻的实时票房数据
- 来源页面: https://akshare.akfamily.xyz/data/others/others.html

## 相关

- [[others-others|AKShare 另类数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 实时票房

接口: movie_boxoffice_realtime

目标地址: https://ys.endata.cn/BoxOffice/Movie

描述: 当前时刻的实时电影票房数据, 每 5 分钟更新一次数据, 实时票房包含今天未开映场次已售出的票房

限量: 当前时刻的实时票房数据

说明: 接口已切换至艺恩当前 `ys.endata.cn/enlib-api` 影片榜单接口, 输出金额统一按 `万` 进行换算

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称   | 类型      | 描述      |
|------|---------|---------|
| 排序   | int64   | 票房排名    |
| 影片名称 | object  | -       |
| 实时票房 | float64 | 注意单位: 万 |
| 票房占比 | float64 | 注意单位: % |
| 上映天数 | int64   | -       |
| 累计票房 | float64 | 注意单位: 万 |

接口示例

```python
import akshare as ak

movie_boxoffice_realtime_df = ak.movie_boxoffice_realtime()
print(movie_boxoffice_realtime_df)
```

数据示例

```
    排序            影片名称 实时票房   票房占比  上映天数  累计票房
0    1             第二十条  2773.21  27.29    11  160845.76
1    2            飞驰人生2  2499.77  24.60    11  267199.76
2    3         熊出没·逆转时空  2429.72  23.91    11  159079.03
3    4             热辣滚烫  2413.96  23.76    11  300038.28
4    5               孤军    11.60   0.11    55    2528.30
5    6           年会不能停！     7.36   0.07    54  128760.85
6    7  泰勒·斯威夫特：时代巡回演唱会     4.73   0.05    52    9594.50
7    8         还是觉得你最好2     4.45   0.04    -3      82.60
8    9          八戒之天蓬下界     2.98   0.03    11     345.28
9   10        舒克贝塔·五角飞碟     2.87   0.03    53    6548.90
10  11               其它    10.25   1.00     0       0.00
```
