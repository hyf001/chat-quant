---
title: "fund_rating_all - 基金评级总汇"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_rating_all

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金评级 > 基金评级总汇
- 描述: 天天基金网-基金评级-基金评级总汇
- 目标地址: https://fund.eastmoney.com/data/fundrating.html
- 限量: 单次返回所有基金评级数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 基金评级总汇

接口: fund_rating_all

目标地址: https://fund.eastmoney.com/data/fundrating.html

描述: 天天基金网-基金评级-基金评级总汇

限量: 单次返回所有基金评级数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称     | 类型      | 描述  |
|--------|---------|-----|
| 代码     | object  | -   |
| 简称     | object  | -   |
| 基金经理   | object  | -   |
| 基金公司   | object  | -   |
| 5星评级家数 | int64   | -   |
| 上海证券   | float64 | -   |
| 招商证券   | float64 | -   |
| 济安金信   | float64 | -   |
| 手续费    | float64 | -   |
| 类型     | object  | -   |

接口示例

```python
import akshare as ak

fund_rating_all_df = ak.fund_rating_all()
print(fund_rating_all_df)
```

数据示例

```
           代码               简称     基金经理 基金公司  ...  济安金信  晨星评级     手续费       类型
0      270007             广发大盘成长混合       李巍   广发  ...   2.0   2.0  0.0015    混合型-灵活
1      270009              广发增强债券C    张芊,方抗   广发  ...   3.0   2.0  0.0000  债券型-混合一级
2      270010        广发沪深300ETF联接A      霍华明   广发  ...   4.0   3.0  0.0012    指数型-股票
3      270014                广发货币B      温秀娟   广发  ...   4.0   NaN  0.0000  货币型-普通货币
4      270025            广发行业领先混合A       程琨   广发  ...   5.0   3.0  0.0015    混合型-偏股
...       ...                  ...      ...  ...  ...   ...   ...     ...       ...
14518  004170            万家现金增利货币B   郅元,黄倩倩   万家  ...   4.0   NaN  0.0000  货币型-普通货币
14519  007201          民生加银聚益纯债债券A  李文君,赵小强   民生  ...   4.0   4.0  0.0008    债券型-长债
14520  161831  银华恒生国企指数(QDII-LOF)A      李宜璇   银华  ...   2.0   2.0  0.0012  指数型-海外股票
14521  004238              永赢瑞益债券A  杨凡颖,余国豪   永赢  ...   4.0   3.0  0.0008    债券型-长债
14522  000436           易方达裕惠定开混合A       胡剑  易方达  ...   5.0   NaN  0.0010    混合型-偏债
[14523 rows x 11 columns]
```
