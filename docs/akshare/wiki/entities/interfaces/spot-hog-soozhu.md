---
title: "spot_hog_soozhu - 各省均价实时排行榜"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, spot, parameters, returns, example]
sources: [raw/data-dictionary/spot/spot.md]
confidence: high
---
# spot_hog_soozhu

- 分类: [[spot-spot|AKShare 现货数据]]
- 主题路径: AKShare 现货数据 > 生猪大数据 > 各省均价实时排行榜
- 描述: 搜猪-生猪大数据-各省均价实时排行榜
- 目标地址: https://www.soozhu.com/price/data/center/
- 限量: 单次返回所有实时数据
- 来源页面: https://akshare.akfamily.xyz/data/spot/spot.html

## 相关

- [[spot-spot|AKShare 现货数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 各省均价实时排行榜

接口: spot_hog_soozhu

目标地址: https://www.soozhu.com/price/data/center/

描述: 搜猪-生猪大数据-各省均价实时排行榜

限量: 单次返回所有实时数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称  | 类型      | 描述 |
|-----|---------|----|
| 省份  | object  | -  |
| 价格  | float64 | -  |
| 涨跌幅 | float64 | -  |

接口示例

```python
import akshare as ak

spot_hog_soozhu_df = ak.spot_hog_soozhu()
print(spot_hog_soozhu_df)
```

数据示例

```
     省份  价格   涨跌幅
0    河北  19.49  0.12
1    辽宁  19.25  0.28
2    山东  19.68  0.21
3   黑龙江  18.79  0.04
4    河南  19.53  0.41
5    湖南  20.64  0.72
6    吉林  19.28  0.26
7    山西  19.43  0.43
8    安徽  20.00  0.39
9    四川  19.20  0.24
10   江西  21.10  0.65
11   甘肃  19.00 -0.15
12   湖北  19.70  0.14
13   浙江  21.00  0.94
14   江苏  20.15  0.55
15   陕西  20.00  0.70
16   广东  20.80 -0.36
17   新疆  17.80 -0.28
18   北京  19.44  0.14
19   天津  19.34  0.14
20  内蒙古  18.86  0.04
21   福建  20.44  0.10
22   广西  20.33  0.14
23   海南  20.98  0.14
24   宁夏  19.20  0.00
25   重庆  18.76  0.14
26   云南  18.98  0.07
27   贵州  19.18 -0.16
```
