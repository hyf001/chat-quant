---
title: "video_variety_show - 综艺节目"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, others, parameters, returns, example]
sources: [raw/data-dictionary/others/others.md]
confidence: high
---
# video_variety_show

- 分类: [[others-others|AKShare 另类数据]]
- 主题路径: AKShare 另类数据 > 视频播映 > 综艺节目
- 描述: 艺恩-视频放映-综艺节目
- 目标地址: https://www.endata.com.cn/Video/index.html
- 限量: 返回前一日的综艺播映数据
- 来源页面: https://akshare.akfamily.xyz/data/others/others.html

## 相关

- [[others-others|AKShare 另类数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 综艺节目

接口: video_variety_show

目标地址: https://www.endata.com.cn/Video/index.html

描述: 艺恩-视频放映-综艺节目

限量: 返回前一日的综艺播映数据

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

video_variety_show_df = ak.video_variety_show()
print(video_variety_show_df)
```

数据示例

```
   排序         名称      类型   播映指数   媒体热度   用户热度    好评度  观看度    统计日期
0   1         声生不息家年华     真人秀  81.62  73.82  94.64  68.00  67.75  2024-02-18
1   2       你好星期六2024     真人秀  71.46  66.35  78.16  51.66  66.63  2024-02-18
2   3  声生不息·家年华 舞台纯享版  真人秀/衍生  71.35  73.82  94.64  49.75  47.48  2024-02-18
3   4          奔跑吧第七季     真人秀  70.35  73.40  73.98  72.00  56.05  2024-02-18
4   5        名侦探学院第七季     真人秀  64.80  73.86  68.72  50.51  55.14  2024-02-18
5   6     花儿与少年丝路季第五季     真人秀  63.89  64.07  65.74  91.00  42.49  2024-02-18
6   7         极限挑战第九季     真人秀  63.42  70.93  71.96  54.00  47.89  2024-02-18
7   8             毛雪汪     真人秀  62.93  41.64  65.67  74.00  56.81  2024-02-18
8   9        王牌对王牌第八季     真人秀  62.48  63.42  64.12  53.00  56.81  2024-02-18
9  10      极限挑战宝藏行第四季     真人秀  62.34  56.96  67.96  50.64  56.37  2024-02-18
```
