---
title: "stock_js_weibo_report - 微博舆情报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, others, parameters, returns, example]
sources: [raw/data-dictionary/others/others.md]
confidence: high
---
# stock_js_weibo_report

- 分类: [[others-others|AKShare 另类数据]]
- 主题路径: AKShare 另类数据 > 微博舆情报告
- 描述: 微博舆情报告中近期受关注的股票
- 目标地址: https://datacenter.jin10.com/market
- 限量: 单次返回指定时间内微博舆情报告中近期受关注的股票
- 来源页面: https://akshare.akfamily.xyz/data/others/others.html

## 相关

- [[others-others|AKShare 另类数据]]
- [[_meta/topic-map]]

## 源文摘录

### 微博舆情报告

接口: stock_js_weibo_report

目标地址: https://datacenter.jin10.com/market

描述: 微博舆情报告中近期受关注的股票

限量: 单次返回指定时间内微博舆情报告中近期受关注的股票

输入参数

| 名称          | 类型  | 描述                                                                                     |
|-------------|-----|----------------------------------------------------------------------------------------|
| time_period | str | time_period="CNHOUR12"; 详见下表**time_period参数一览表**, 可通过调用 **stock_js_weibo_nlp_time** 获取 |

time_period 参数一览表

| 参数       | 说明   |
|----------|------|
| CNHOUR2  | 2小时  |
| CNHOUR6  | 6小时  |
| CNHOUR12 | 12小时 |
| CNHOUR24 | 1天   |
| CNDAY7   | 1周   |
| CNDAY30  | 1月   |

输出参数

| 名称   | 类型  | 描述     |
|------|-----|--------|
| name | str | 股票名称   |
| rate | str | 人气排行指数 |

接口示例

```python
import akshare as ak

stock_js_weibo_report_df = ak.stock_js_weibo_report(time_period="CNHOUR12")
print(stock_js_weibo_report_df)
```

数据示例

```
    name   rate
0   黄河旋风   9.86
1   东方财富   6.91
2   海王生物  10.09
3   秀强股份   4.56
4   江淮汽车  10.08
5    欧菲光  10.00
6   中兴通讯   9.98
7   鲁抗医药   9.97
8   海陆重工  10.07
9   中通客车   9.75
10  华天科技  10.02
11  亚星客车   7.70
12  中国平安  -0.66
13  新日恒力   9.98
14   同花顺  -0.90
15  赣锋锂业  10.00
16  北玻股份  10.09
17   比亚迪   7.02
18  沪电股份  10.00
19   太平洋   9.92
20  深康佳A  -8.02
21  天齐锂业   9.34
22  泰达股份   9.99
23  中信证券   0.68
24  欣龙控股  10.00
25  均胜电子  10.00
26   安居宝   9.98
27  联环药业  10.00
28  乾照光电   2.93
29  山东黄金  -3.38
30  国海证券   7.20
31  永鼎股份  10.00
32   漫步者  -4.51
33  江苏吴中  10.03
34  国农科技  10.00
35  中环股份   9.98
36  阳普医疗  10.01
37   新宙邦   8.91
38  兴森科技   9.98
39  南大光电   7.46
40  四环生物   9.98
41  海特高新  10.01
42  光环新网   7.97
43  晶方科技  -2.73
44  铜峰电子  10.04
45  华力创通  10.00
46  复星医药   9.41
47  力帆股份  10.14
48  永太科技   9.65
49  四维图新   8.76
```
