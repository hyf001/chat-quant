---
title: "stock_institute_recommend_detail - 股票评级记录"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_institute_recommend_detail

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 机构推荐 > 股票评级记录
- 描述: 新浪财经-机构推荐池-股票评级记录
- 目标地址: http://stock.finance.sina.com.cn/stock/go.php/vIR_StockSearch/key/sz000001.phtml
- 限量: 单次获取新浪财经-机构推荐池-股票评级记录的所有数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 股票评级记录

接口: stock_institute_recommend_detail

目标地址: http://stock.finance.sina.com.cn/stock/go.php/vIR_StockSearch/key/sz000001.phtml

描述: 新浪财经-机构推荐池-股票评级记录

限量: 单次获取新浪财经-机构推荐池-股票评级记录的所有数据

输入参数

| 名称     | 类型  | 描述              |
|--------|-----|-----------------|
| symbol | str | symbol="000001" |

输出参数

| 名称   | 类型  | 描述  |
|------|-----|-----|
| 股票代码 | str | -   |
| 股票名称 | str | -   |
| 目标价  | str | -   |
| 最新评级 | str | -   |
| 评级机构 | str | -   |
| 分析师  | str | -   |
| 行业   | str | -   |
| 评级日期 | str | -   |

接口示例

```python
import akshare as ak

stock_institute_recommend_detail_df = ak.stock_institute_recommend_detail(symbol="002709")
print(stock_institute_recommend_detail_df)
```

数据示例

```
       股票代码  股票名称    目标价 最新评级  评级机构        分析师    行业        评级日期
0    002709  天赐材料    NaN   增持  国海证券      谭倩,尹斌  化学制品  2020-05-27
1    002709  天赐材料    NaN   增持  光大证券     吴裕,裘孝锋  化学制品  2020-05-07
2    002709  天赐材料  35.20   买入  华创证券  杨达伟,于潇,邱迪  化学制品  2020-05-06
3    002709  天赐材料  33.25   买入  东吴证券        曾朵红  化学制品  2020-05-06
4    002709  天赐材料  35.50   买入  招商证券    游家训,刘珺涵  化学制品  2020-05-01
..      ...   ...    ...  ...   ...        ...   ...         ...
241  002709  天赐材料    NaN   买入  招商证券    游家训,陈雁冰  化学制品  2017-09-07
242  002709  天赐材料    NaN   买入  方正证券        韩振国  化学制品  2017-09-07
243  002709  天赐材料  61.82   买入  招商证券    游家训,陈雁冰  化学制品  2017-09-07
244  002709  天赐材料  59.82   买入  中泰证券        邵晶鑫  化学制品  2017-09-06
245  002709  天赐材料    NaN   买入  国海证券        代鹏举  化学制品  2017-09-04
```
