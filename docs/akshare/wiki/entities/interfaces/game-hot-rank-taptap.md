---
title: "game_hot_rank_taptap - TapTap 游戏榜单"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, others, parameters, returns, example]
sources: [raw/data-dictionary/others/others.md]
confidence: high
---
# game_hot_rank_taptap

- 分类: [[others-others|AKShare 另类数据]]
- 主题路径: AKShare 另类数据 > 彭博亿万富豪指数 > TapTap 游戏榜单
- 描述: 按照榜单类型查询 TapTap 平台游戏排行榜数据
- 目标地址: https://www.taptap.cn/top/played
- 限量: 单次返回指定榜单的全部游戏排名数据
- 来源页面: https://akshare.akfamily.xyz/data/others/others.html

## 相关

- [[others-others|AKShare 另类数据]]
- [[_meta/topic-map]]

## 源文摘录

#### TapTap 游戏榜单

接口: game_hot_rank_taptap

目标地址: https://www.taptap.cn/top/played

描述: 按照榜单类型查询 TapTap 平台游戏排行榜数据

限量: 单次返回指定榜单的全部游戏排名数据

输入参数

| 名称     | 类型  | 描述                                                          |
|--------|-----|-------------------------------------------------------------|
| symbol | str | symbol="热玩榜"; choice of {"热玩榜", "热门榜", "新品榜", "预约榜", "热卖榜"} |

输出参数

| 名称   | 类型             | 描述                        |
|------|----------------|---------------------------|
| 排名   | int            | 榜单排名                      |
| 游戏名称 | str            | 游戏名称                      |
| 评分   | float          | TapTap 玩家评分 (0-10 分制)     |
| 总点击量 | int            | 游戏页面累计点击量                 |
| 游玩次数 | int            | 累计游玩次数                    |
| 评论数  | int            | 评论总数                      |
| 粉丝数  | int            | 关注/粉丝数                    |
| 标签   | str            | 游戏标签 (逗号分隔, 如 "模拟经营, 治愈") |
| 推荐语  | str            | 编辑/官方推荐语                  |
| 发布时间 | datetime64[ns] | 游戏发布时间                    |
| 游戏ID | str            | TapTap 平台游戏唯一 ID          |
| 图标链接 | str            | 游戏图标 URL                  |
| 简介   | str            | 游戏简介文本 (已清洗 HTML 标签)      |

接口示例

```python
import akshare as ak

game_hot_rank_taptap_df = ak.game_hot_rank_taptap(symbol="热玩榜")
print(game_hot_rank_taptap_df)
```

数据示例

```
      排名  ...                                                 简介
0      1  ...  直播时间：18:00-23:00\n《心动小镇》是一款慢节奏生活模拟游戏。无论拥有什么样的爱...
1      2  ...  这片银河中有名为「星神」的存在，祂们造就现实，抹消星辰，在无数「世界」中留下祂们的痕迹。你—...
2      3  ...  鹅鸭杀S2赛季［瀚漠迷踪］上线！黄沙漫天，神谕低语，全新地图「古代沙漠」、角色「决斗呆呆鸟」...
3      4  ...  神明娘爆涂乱射副副副游《乱涂！彩世界》4月28日正式上线！洛天依限时联动开启签到就送，首周爆...
4      5  ...  14W人打出96%好评如潮的《潜水员戴夫》国服手机版&TapPC版三端现已正式发售！白天潜水...
..   ...  ...                                                ...
145  146  ...  欢迎来到危机四伏的核污染海域，这里的一切生物都在悄然发生异变。你将化身为一条普通的小鱼，在这...
146  147  ...  【简介】\n玩家扮演一位家族老祖，开创一个家族，然后在大陆或者海域中，占领一个修仙灵山或小岛...
147  148  ...  【游戏介绍】\n《太空杀》是一款多人社交推理手游，在这里，你可能会收获一群黑心伙伴，一些爆笑...
148  149  ...  你睁开眼睛，\n发现自己身处于一个完全陌生的世界上——\n这是一场无限轮回的游戏，\n只有获...
149  150  ...  你说得对，但是《星落》是一款探险队沿途对抗大魔王的异世界冒险扫荡RPG。（绝赞发行中^^）\...
[150 rows x 13 columns]
```
