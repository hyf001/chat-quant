---
title: "stock_lhb_yytj_sina - 龙虎榜-营业上榜统计"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_lhb_yytj_sina

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 营业部详情数据-东财 > 龙虎榜-营业上榜统计
- 描述: 新浪财经-龙虎榜-营业上榜统计
- 目标地址: https://vip.stock.finance.sina.com.cn/q/go.php/vLHBData/kind/yytj/index.phtml
- 限量: 单次返回指定 symbol 的所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 龙虎榜-营业上榜统计

接口: stock_lhb_yytj_sina

目标地址: https://vip.stock.finance.sina.com.cn/q/go.php/vLHBData/kind/yytj/index.phtml

描述: 新浪财经-龙虎榜-营业上榜统计

限量: 单次返回指定 symbol 的所有历史数据

输入参数

| 名称     | 类型  | 描述                                                                                |
|--------|-----|-----------------------------------------------------------------------------------|
| symbol | str | symbol="5"; choice of {"5": 最近 5 天; "10": 最近 10 天; "30": 最近 30 天; "60": 最近 60 天;} |

输出参数

| 名称     | 类型      | 描述      |
|--------|---------|---------|
| 营业部名称  | object  | -       |
| 上榜次数   | int64   | -       |
| 累积购买额  | float64 | 注意单位: 万 |
| 买入席位数  | int64   | -       |
| 累积卖出额  | float64 | 注意单位: 万 |
| 卖出席位数  | int64   | -       |
| 买入前三股票 | object  | -       |

接口示例

```python
import akshare as ak

stock_lhb_yytj_sina_df = ak.stock_lhb_yytj_sina(symbol="5")
print(stock_lhb_yytj_sina_df)
```

数据示例

```
                营业部名称  上榜次数    累积购买额  ...    累积卖出额  卖出席位数           买入前三股票
0      渤海证券股份有限公司天津滨海新区第一分公司     1     0.00  ...   116.29      1             ST星源
1       平安证券股份有限公司深圳香蜜湖证券营业部     3   879.44  ...   522.60      1   科新发展,ST星源,中重科技
2       华泰证券股份有限公司姜堰东大街证券营业部     2     0.00  ...   165.14      2       ST星源,*ST西发
3       海通证券股份有限公司庆阳西大街证券营业部     2     0.00  ...   504.69      2             ST星源
4    东方财富证券股份有限公司山南香曲东路证券营业部    26  5593.35  ...  5962.82     17  亚世光电,中视传媒,光大嘉宝,
..                       ...   ...      ...  ...      ...    ...              ...
315          华泰证券股份有限公司湖南分公司     7  6542.40  ...  3553.71      2        哈森股份,开元教育
316  上海证券有限责任公司绍兴新昌人民西路证券营业部     1  1458.00  ...     0.00      0             昂立教育
317     华安证券股份有限公司合肥高新区证券营业部     5  1868.41  ...  1788.15      2   中科金财,昀冢科技,普路通,
318     兴业证券股份有限公司福州湖东路证券营业部     1  1047.27  ...     0.00      0              香飘飘
319  申万宏源证券有限公司上海徐汇区龙漕路证券营业部     1   678.26  ...     0.00      0            *ST碳元
[320 rows x 7 columns]
```
