---
title: "video_tv - 电视剧集"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, others, parameters, returns, example]
sources: [raw/data-dictionary/others/others.md]
confidence: high
---
# video_tv

- 分类: [[others-others|AKShare 另类数据]]
- 主题路径: AKShare 另类数据 > 视频播映 > 电视剧集
- 描述: 艺恩-视频放映-电视剧集
- 目标地址: https://www.endata.com.cn/Video/index.html
- 限量: 返回前一日的电视剧播映数据
- 来源页面: https://akshare.akfamily.xyz/data/others/others.html

## 相关

- [[others-others|AKShare 另类数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 电视剧集

接口: video_tv

目标地址: https://www.endata.com.cn/Video/index.html

描述: 艺恩-视频放映-电视剧集

限量: 返回前一日的电视剧播映数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称   | 类型      | 描述  |
|------|---------|-----|
| 排序   | int64   | -   |
| 名称   | object  | -   |
| 类型   | object  | -   |
| 播映指数 | float64 | -   |
| 媒体热度 | float64 | -   |
| 用户热度 | float64 | -   |
| 好评度  | float64 | -   |
| 观看度  | float64 | -   |
| 统计日期 | float64 | -   |

接口示例

```python
import akshare as ak

video_tv_df = ak.video_tv()
print(video_tv_df)
```

数据示例

```
   排序    名称     类型   播映指数   媒体热度  用户热度 好评度  观看度     统计日期
0   1    在暴雪时分  爱情/都市  79.44  74.46  75.72  68.00  80.43  2024-02-18
1   2     南来北往     爱情  78.67  76.24  75.63  53.39  83.90  2024-02-18
2   3     烟火人家  剧情/爱情  72.98  72.04  71.43  52.47  74.73  2024-02-18
3   4      莲花楼     古装  72.84  68.92  76.22  85.00  56.97  2024-02-18
4   5       繁花  剧情/爱情  72.40  75.92  65.39  86.00  63.16  2024-02-18
5   6     一念关山     古装  69.52  60.02  79.51  64.00  57.42  2024-02-18
6   7     要久久爱     剧情  69.45  63.88  71.14  72.00  60.50  2024-02-18
7   8   长相思第一季  爱情/奇幻  68.41  62.20  67.88  78.00  59.09  2024-02-18
8   9   乡村爱情16  喜剧/乡村  67.16  65.22  62.70  52.07  70.66  2024-02-18
9  10  繁花[沪语版]     剧情  66.96  75.93  65.39  51.32  63.16  2024-02-18
```
