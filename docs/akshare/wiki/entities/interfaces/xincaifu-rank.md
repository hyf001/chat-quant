---
title: "xincaifu_rank - 新财富富豪榜"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, others, parameters, returns, example]
sources: [raw/data-dictionary/others/others.md]
confidence: high
---
# xincaifu_rank

- 分类: [[others-others|AKShare 另类数据]]
- 主题路径: AKShare 另类数据 > 新财富富豪榜
- 描述: 新财富 500 富豪榜, 从 2003 年至今
- 目标地址: http://www.xcf.cn/zhuanti/ztzz/hdzt1/500frb/index.html
- 限量: 单次返回指定年份的富豪榜数据
- 来源页面: https://akshare.akfamily.xyz/data/others/others.html

## 相关

- [[others-others|AKShare 另类数据]]
- [[_meta/topic-map]]

## 源文摘录

### 新财富富豪榜

接口: xincaifu_rank

目标地址: http://www.xcf.cn/zhuanti/ztzz/hdzt1/500frb/index.html

描述: 新财富 500 富豪榜, 从 2003 年至今

限量: 单次返回指定年份的富豪榜数据

输入参数

| 名称   | 类型  | 描述                      |
|------|-----|-------------------------|
| year | str | year="2020"; 从 2003 年至今 |

输出参数

| 名称   | 类型      | 描述       |
|------|---------|----------|
| 排名   | int64   | -        |
| 财富   | float64 | 注意单位: 亿元 |
| 姓名   | object  | -        |
| 主要公司 | object  | -        |
| 相关行业 | object  | -        |
| 公司总部 | object  | -        |
| 性别   | object  | -        |
| 年龄   | object  | -        |
| 年份   | int64   | -        |

接口示例

```python
import akshare as ak

xincaifu_rank_df = ak.xincaifu_rank(year="2022")
print(xincaifu_rank_df)
```

数据示例

```
      排名      财富       姓名       主要公司        相关行业     公司总部   性别     年龄    年份
0      1  4983.5      钟睒睒  农夫山泉/万泰生物  矿泉水饮料、医药生物  浙江杭州/北京    男     68  2022
1      2  3348.2      曾毓群       宁德时代        动力电池     福建宁德    男     54  2022
2      3  3010.8      马化腾       腾讯控股     互联网综合服务     广东深圳    男     51  2022
3      4  2916.0      张一鸣       今日头条  推荐引擎产品、短视频       北京    男     39  2022
4      5  1972.0       黄峥        拼多多          电商       上海    男     42  2022
..   ...     ...      ...        ...         ...      ...  ...    ...   ...
495  496    94.7      崔志祥     方圆有色金属     铜、金、银生产     山东东营    男     59  2022
496  497    94.6    胡成中家族        德力西  低压电器、仪器仪表等     浙江温州    男     61  2022
497  498    94.2  张宏亮/张秀根       曙光股份        汽车整车     辽宁丹东  男/男  38,61  2022
498  499    94.0       金磊       长春高新        生长激素     吉林长春    男     57  2022
499  500    93.7    赵轶/徐昕       长川科技    集成电路测试装备     浙江杭州  男/女  56,56  2022
```
