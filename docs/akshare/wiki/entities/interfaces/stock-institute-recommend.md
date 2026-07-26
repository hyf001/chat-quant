---
title: "stock_institute_recommend - 机构推荐池"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_institute_recommend

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 机构推荐 > 机构推荐池
- 描述: 新浪财经-机构推荐池-具体指标的数据
- 目标地址: http://stock.finance.sina.com.cn/stock/go.php/vIR_RatingNewest/index.phtml
- 限量: 单次获取新浪财经-机构推荐池-具体指标的所有数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 机构推荐池

接口: stock_institute_recommend

目标地址: http://stock.finance.sina.com.cn/stock/go.php/vIR_RatingNewest/index.phtml

描述: 新浪财经-机构推荐池-具体指标的数据

限量: 单次获取新浪财经-机构推荐池-具体指标的所有数据

输入参数

| 名称     | 类型  | 描述                                                                                                                 |
|--------|-----|--------------------------------------------------------------------------------------------------------------------|
| symbol | str | symbol="行业关注度"; choice of {'最新投资评级', '上调评级股票', '下调评级股票', '股票综合评级', '首次评级股票', '目标涨幅排名', '机构关注度', '行业关注度', '投资评级选股'} |

输出参数

| 名称  | 类型  | 描述                |
|-----|-----|-------------------|
| -   | -   | 根据特定 indicator 而定 |

接口示例

```python
import akshare as ak

stock_institute_recommend_df = ak.stock_institute_recommend(symbol="投资评级选股")
print(stock_institute_recommend_df)
```

数据示例

```
        股票代码   股票名称 最新评级     目标价       评级日期↓ 综合评级    平均涨幅    行业
0     000001   平安银行   买入   19.73  2020-05-27   买入  51.75%    银行
1     300403   汉宇集团   中性    5.70  2020-05-27   中性  18.26%  白色家电
2     603288   海天味业   买入  112.85  2020-05-27   买入  -1.32%  食品加工
3     601238   广汽集团   买入   12.72  2020-05-27   买入  34.62%  汽车整车
4     002709   天赐材料   增持   34.24  2020-05-27   买入   18.1%  化学制品
      ...    ...  ...     ...         ...  ...     ...   ...
1053  601398   工商银行   买入    7.14  2020-05-27   买入  39.54%    银行
1054  002078   太阳纸业   买入   11.22  2020-05-27   买入  35.64%    造纸
1055  002080   中材科技   买入   14.59  2020-05-27   买入  22.61%  化学制品
1056  002081  金 螳 螂   增持   12.55  2020-05-27   买入  55.51%  装修装饰
1057  601658   邮储银行   增持    6.52  2020-05-27   买入  28.25%    银行
```
