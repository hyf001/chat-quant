---
title: "futures_news_shmet - 期货资讯"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, futures, parameters, returns, example]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# futures_news_shmet

- 分类: [[futures-futures|AKShare 期货数据]]
- 主题路径: 此处的合约需要是近期的合约, 否则会报错 > 期货资讯
- 描述: 上海金属网-快讯
- 目标地址: https://www.shmet.com/newsFlash/newsFlash.html?searchKeyword=
- 限量: 指定 symbol 的数据
- 来源页面: https://akshare.akfamily.xyz/data/futures/futures.html

## 相关

- [[futures-futures|AKShare 期货数据]]
- [[_meta/topic-map]]

## 源文摘录

### 期货资讯

接口: futures_news_shmet

目标地址: https://www.shmet.com/newsFlash/newsFlash.html?searchKeyword=

描述: 上海金属网-快讯

限量: 指定 symbol 的数据

输入参数

| 名称     | 类型  | 描述                                                                                           |
|--------|-----|----------------------------------------------------------------------------------------------|
| symbol | str | symbol="全部"; choice of {"全部", "要闻", "VIP", "财经", "铜", "铝", "铅", "锌", "镍", "锡", "贵金属", "小金属"} |

输出参数

| 名称   | 类型     | 描述  |
|------|--------|-----|
| 发布时间 | object | -   |
| 内容   | object | -   |

接口示例

```python
import akshare as ak

futures_news_shmet_df = ak.futures_news_shmet(symbol="铜")
print(futures_news_shmet_df)
```

数据示例

```
                   发布时间                                                 内容
0   2024-02-05 14:02:44+08:00  【金诚信资源：Lonshi铜矿增储情况】金诚信近日接受机构调研时表示，公司在2022年4月发...
1   2024-02-05 14:02:44+08:00  【金诚信资源项目进展情况】金诚信近日接受机构调研时表示，公司两岔河磷矿南采区已投产，2023...
2   2024-02-05 14:02:44+08:00  【金诚信资源：雨季对Dikulushi铜矿和Lonshi铜矿的影响】金诚信近日接受机构调研时...
3   2024-02-05 14:02:44+08:00  【金诚信：整体来看，铜价存在长期持续震荡上行可能】金诚信近日接受机构调研时表示，从中长期来看...
4   2024-02-05 14:19:22+08:00  【江苏省雨雪天气或影响该地区铜杆厂生产销售】2月3日11时12分，江苏省气象台变更发布道路结...
..                        ...                                                ...
995 2024-03-21 11:39:32+08:00  【中科铜箔2023年铜箔年产量超过34500吨】2023年，湖北中科铜箔的铜箔年产量由原来的...
996 2024-03-21 11:39:32+08:00  【江西新越年产40万吨电解铜项目环评批准公示】根据建设项目环境影响评价审批程序的有关规定，经...
997 2024-03-21 11:39:32+08:00  【铜陵有色铜基新材料项目空分制氧项目1号主冷箱顺利封顶】3月16日上午8点18分，随着300...
998 2024-03-21 11:39:32+08:00  【电工合金：2023年净利润1.36亿元，同比增19.98%】近日，电工合金发布2023年年...
999 2024-03-21 12:10:40+08:00  【SHMET铜现货报价】上海金属网讯：截止11:30分，上海金属网1#电解铜报72700-7...
[1000 rows x 2 columns]
```
