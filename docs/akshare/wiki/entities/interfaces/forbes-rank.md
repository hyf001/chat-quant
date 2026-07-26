---
title: "forbes_rank - 福布斯中国榜单"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, others, parameters, returns, example]
sources: [raw/data-dictionary/others/others.md]
confidence: high
---
# forbes_rank

- 分类: [[others-others|AKShare 另类数据]]
- 主题路径: AKShare 另类数据 > 福布斯中国榜单
- 描述: 福布斯中国-榜单数据, 一共 87 个指标的数据可以获取
- 目标地址: https://www.forbeschina.com/lists
- 限量: 单次返回指定 symbol 的数据
- 来源页面: https://akshare.akfamily.xyz/data/others/others.html

## 相关

- [[others-others|AKShare 另类数据]]
- [[_meta/topic-map]]

## 源文摘录

### 福布斯中国榜单

接口: forbes_rank

目标地址: https://www.forbeschina.com/lists

描述: 福布斯中国-榜单数据, 一共 87 个指标的数据可以获取

限量: 单次返回指定 symbol 的数据

输入参数

| 名称     | 类型  | 描述                                                                                                  |
|--------|-----|-----------------------------------------------------------------------------------------------------|
| symbol | str | symbol="2020年福布斯中国400富豪榜"; 参考 **福布斯中国指标一览表**, 也可以访问 https://www.forbeschina.com/lists 获取所需要的 symbol |

福布斯中国指标一览表

|     | name                     | url                                    |
|----:|:-------------------------|:---------------------------------------|
|   0 | 2020福布斯中国400富豪榜          | https://www.forbeschina.com/lists/1750 |
|   1 | 2020福布斯菲律宾富豪榜            | https://www.forbeschina.com/lists/1746 |
|   2 | 2020福布斯美国富豪榜             | https://www.forbeschina.com/lists/1745 |
|   3 | 2020福布斯中国名人榜             | https://www.forbeschina.com/lists/1744 |
|   4 | 2020福布斯新加坡富豪榜            | https://www.forbeschina.com/lists/1743 |
|   5 | 2020福布斯中国最佳CEO榜          | https://www.forbeschina.com/lists/1741 |
|   6 | 2020福布斯中国医疗健康富豪榜         | https://www.forbeschina.com/lists/1740 |
|   7 | 2020福布斯中国慈善榜             | https://www.forbeschina.com/lists/1739 |
|   8 | 2020福布斯韩国富豪榜             | https://www.forbeschina.com/lists/1738 |
|   9 | 2020福布斯中国科技女性榜           | https://www.forbeschina.com/lists/1737 |
|  10 | 2020福布斯全球亿万富豪榜中国子榜       | https://www.forbeschina.com/lists/1734 |
|  11 | 2020福布斯全球亿万富豪榜           | https://www.forbeschina.com/lists/1733 |
|  12 | 2019福布斯中国400富豪榜          | https://www.forbeschina.com/lists/1728 |
|  13 | 2019福布斯中国最佳创投人TOP100     | https://www.forbeschina.com/lists/1747 |
|  14 | 2019福布斯全球最有影响力体育经纪人      | https://www.forbeschina.com/lists/1727 |
|  15 | 2019福布斯中国30位30岁以下精英榜     | https://www.forbeschina.com/lists/1725 |
|  16 | 2019福布斯美国400富豪榜          | https://www.forbeschina.com/lists/1722 |
|  17 | 2019福布斯菲律宾富豪榜            | https://www.forbeschina.com/lists/1721 |
|  18 | 2019福布斯中国慈善榜             | https://www.forbeschina.com/lists/1718 |
|  19 | 2019福布斯100名人榜            | https://www.forbeschina.com/lists/1717 |
|  20 | 2019福布斯韩国富豪榜             | https://www.forbeschina.com/lists/1716 |
|  21 | 2019福布斯马来西亚50富豪榜         | https://www.forbeschina.com/lists/19   |
|  22 | 2019福布斯中国最杰出商界女性排行榜      | https://www.forbeschina.com/lists/1165 |
|  23 | 2019福布斯全球亿万富豪榜           | https://www.forbeschina.com/lists/21   |
|  24 | 2018福布斯中国商界25位潜力女性       | https://www.forbeschina.com/lists/13   |
|  25 | 2018福布斯中国慈善榜             | https://www.forbeschina.com/lists/1156 |
|  26 | 2018福布斯中国最佳创投人TOP100     | https://www.forbeschina.com/lists/1258 |
|  27 | 2018福布斯中国最富有女性Top25      | https://www.forbeschina.com/lists/11   |
|  28 | 2018福布斯中国最佳女性创投人TOP25    | https://www.forbeschina.com/lists/12   |
|  29 | 2018中国最杰出商界女性排行榜         | https://www.forbeschina.com/lists/1145 |
|  30 | 2018中国分析师最佳价值发现榜         | https://www.forbeschina.com/lists/1147 |
|  31 | 2018中国最佳分析师50强榜          | https://www.forbeschina.com/lists/1148 |
|  32 | 2018福布斯中国分析师最佳预测盈利能力榜    | https://www.forbeschina.com/lists/1149 |
|  33 | 2018全球亿万富豪榜              | https://www.forbeschina.com/lists/1151 |
|  34 | 2018福布斯中国30位30岁以下精英榜     | https://www.forbeschina.com/lists/1157 |
|  35 | 2018福布斯中国上市公司最佳CEO       | https://www.forbeschina.com/lists/1159 |
|  36 | 2018福布斯中国400富豪榜          | https://www.forbeschina.com/lists/1162 |
|  37 | 2017福布斯全球科技界100富豪榜       | https://www.forbeschina.com/lists/1618 |
|  38 | 2017福布斯中国30位30岁以下精英榜     | https://www.forbeschina.com/lists/1617 |
|  39 | 2017华人富豪榜                | https://www.forbeschina.com/lists/1131 |
|  40 | 2017全球亿万富豪榜              | https://www.forbeschina.com/lists/1132 |
|  41 | 2017福布斯全球运动员收入榜          | https://www.forbeschina.com/lists/1644 |
|  42 | 2017福布斯台湾50富豪榜           | https://www.forbeschina.com/lists/1133 |
|  43 | 2017福布斯中国上市公司最佳CEO       | https://www.forbeschina.com/lists/1134 |
|  44 | 2017福布斯中国名人榜             | https://www.forbeschina.com/lists/1135 |
|  45 | 2017中国慈善榜                | https://www.forbeschina.com/lists/1681 |
|  46 | 2017分析师最佳预测盈利能力榜         | https://www.forbeschina.com/lists/1253 |
|  47 | 2017福布斯中国最佳创投人TOP100     | https://www.forbeschina.com/lists/1254 |
|  48 | 2017中国最佳分析师50强榜          | https://www.forbeschina.com/lists/1252 |
|  49 | 2020年福布斯世界最佳雇主TOP100     | https://www.forbeschina.com/lists/1749 |
|  50 | 2020福布斯中国上市公司潜力企业榜       | https://www.forbeschina.com/lists/1748 |
|  51 | 2020福布斯亚州中小上市企业榜         | https://www.forbeschina.com/lists/1742 |
|  52 | 2020福布斯中国最具创新力企业榜        | https://www.forbeschina.com/lists/1736 |
|  53 | 2020福布斯全球企业2000强榜        | https://www.forbeschina.com/lists/1735 |
|  54 | 2019福布斯全球最具价值的体育经纪机构     | https://www.forbeschina.com/lists/1726 |
|  55 | 2019福布斯全球数字经济100强榜       | https://www.forbeschina.com/lists/1724 |
|  56 | 2019福布斯中国最具创新力企业榜        | https://www.forbeschina.com/lists/1715 |
|  57 | 2018福布斯中国新三板企业融资能力榜TOP50 | https://www.forbeschina.com/lists/14   |
|  58 | 2018福布斯中国最具创新力企业榜        | https://www.forbeschina.com/lists/17   |
|  59 | 2018非上市公司潜力企业榜           | https://www.forbeschina.com/lists/18   |
|  60 | 2018福布斯中国最佳创投机构          | https://www.forbeschina.com/lists/20   |
|  61 | 2018上市公司潜力企业榜            | https://www.forbeschina.com/lists/1152 |
|  62 | 2018福布斯中国新三板TOP100       | https://www.forbeschina.com/lists/1155 |
|  63 | 2018福布斯中国最佳PE机构          | https://www.forbeschina.com/lists/1257 |
|  64 | 2017福布斯中国家族企业            | https://www.forbeschina.com/lists/1136 |
|  65 | 2017福布斯全球企业2000强         | https://www.forbeschina.com/lists/1139 |
|  66 | 2017值得关注的新三板企业           | https://www.forbeschina.com/lists/1459 |
|  67 | 2017中国非上市公司潜力企业榜         | https://www.forbeschina.com/lists/1460 |
|  68 | 2017福布斯中国最佳PE机构          | https://www.forbeschina.com/lists/1255 |
|  69 | 2017福布斯中国最佳创投机构          | https://www.forbeschina.com/lists/1256 |
|  70 | 2019福布斯美国大学排行榜           | https://www.forbeschina.com/lists/1720 |
|  71 | 2018福布斯创新力最强的30个城市       | https://www.forbeschina.com/lists/15   |
|  72 | 2018福布斯最适合新生活的宜居城市       | https://www.forbeschina.com/lists/16   |
|  73 | 2018福布斯中国大陆最佳商业城市        | https://www.forbeschina.com/lists/1163 |
|  74 | 2017福布斯中国大陆最佳商业城市        | https://www.forbeschina.com/lists/1138 |
|  75 | 2017福布斯中国大陆最佳地级城市30强     | https://www.forbeschina.com/lists/1140 |
|  76 | 2017福布斯中国大陆最佳县级城市30强     | https://www.forbeschina.com/lists/1141 |
|  77 | 2017福布斯创新力最强的30个城市       | https://www.forbeschina.com/lists/1142 |
|  78 | 2017福布斯经营成本最高的30个城市      | https://www.forbeschina.com/lists/1143 |
|  79 | 2015福布斯全球最适宜经商的国家和地区     | https://www.forbeschina.com/lists/1120 |
|  80 | 2015美国最适宜经商和就业的城市        | https://www.forbeschina.com/lists/1453 |
|  81 | 2015美国就业增长最快城市100强       | https://www.forbeschina.com/lists/1525 |
|  82 | 2015美国最适合经商和就业的州         | https://www.forbeschina.com/lists/1526 |
|  83 | 2014美国最适宜经商和就业的地区        | https://www.forbeschina.com/lists/1515 |
|  84 | 2014福布斯美国最适合经商和就业的州      | https://www.forbeschina.com/lists/1516 |
|  85 | 2014年世界最负盛名城市榜           | https://www.forbeschina.com/lists/1517 |
|  86 | 2014福布斯全球最适宜经商的国家和地区     | https://www.forbeschina.com/lists/1524 |

输出参数

| 名称  | 类型  | 描述              |
|-----|-----|-----------------|
| 排名  | str | -               |
| -   | -   | 根据不同的 symbol 而异 |

接口示例

```python
import akshare as ak

forbes_rank_df = ak.forbes_rank(symbol="2020福布斯中国400富豪榜")
print(forbes_rank_df)
```

数据示例

```
      排名     姓名  财富（亿元）       财富来源  年龄 居住城市
0      1     马云  4377.2       阿里巴巴  56   杭州
1      2    马化腾  3683.2         腾讯  49   深圳
2      3    钟睒睒  3596.5  农夫山泉/万泰生物  65   杭州
3      4  孙飘扬家族  2335.4  恒瑞医药/翰森制药  62  连云港
4      5  何享健家族  2148.5       美的集团  78   佛山
..   ...    ...     ...        ...  ..  ...
395  394  李文美家族   105.4       万孚生物  58   广州
396  397    郭梓文   104.8       中国奥园  56   香港
397  398  袁建栋家族   104.1       博瑞医药  50   苏州
398  399     王帅   103.4       蚂蚁集团   /   杭州
399  399    卢竑岩   103.4        吉比特  43   厦门
```
