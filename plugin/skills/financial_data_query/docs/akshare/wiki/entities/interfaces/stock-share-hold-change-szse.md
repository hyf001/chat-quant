---
title: "stock_share_hold_change_szse - 董监高及相关人员持股变动-深证"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_share_hold_change_szse

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 机构推荐 > 董监高及相关人员持股变动-深证
- 描述: 深圳证券交易所-信息披露-监管信息公开-董监高人员股份变动
- 目标地址: http://www.szse.cn/disclosure/supervision/change/index.html
- 限量: 单次获取指定 symbol 的数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 董监高及相关人员持股变动-深证

接口: stock_share_hold_change_szse

目标地址: http://www.szse.cn/disclosure/supervision/change/index.html

描述: 深圳证券交易所-信息披露-监管信息公开-董监高人员股份变动

限量: 单次获取指定 symbol 的数据

输入参数

| 名称     | 类型  | 描述                                          |
|--------|-----|---------------------------------------------|
| symbol | str | symbol="001308"; choice of {"全部", "具体股票代码"} |

输出参数

| 名称         | 类型      | 描述         |
|------------|---------|------------|
| 证券代码       | object  | -          |
| 证券简称       | object  | -          |
| 董监高姓名      | object  | -          |
| 变动日期       | object  | -          |
| 变动股份数量     | float64 | 注意单位: 万股   |
| 成交均价       | float64 | -          |
| 变动原因       | object  | -          |
| 变动比例       | float64 | 注意单位: 千分之一 |
| 当日结存股数     | float64 | 注意单位: 万股   |
| 股份变动人姓名    | object  | -          |
| 职务         | object  | -          |
| 变动人与董监高的关系 | object  | -          |

接口示例

```python
import akshare as ak

stock_share_hold_change_szse_df = ak.stock_share_hold_change_szse(symbol="001308")
print(stock_share_hold_change_szse_df)
```

数据示例

```
   证券代码  证券简称 董监高姓名 变动日期  ...    当日结存股数  股份变动人姓名     职务  变动人与董监高的关系
0  001308  康冠科技    凌斌  2023-08-21  ...  18752.80       凌斌     董事          本人
1  001308  康冠科技    凌斌  2023-08-18  ...  18743.80       凌斌     董事          本人
2  001308  康冠科技    凌斌  2023-08-17  ...  18737.80       凌斌     董事          本人
3  001308  康冠科技    凌斌  2023-08-16  ...  18734.80       凌斌     董事          本人
4  001308  康冠科技    江微  2023-08-09  ...      1.00       江微     监事          本人
5  001308  康冠科技    吴远  2023-08-08  ...      7.48       吴远     高管          本人
6  001308  康冠科技   孙建华  2023-08-08  ...      3.88      孙建华  董秘、高管          本人
7  001308  康冠科技    吴远  2022-08-24  ...      4.95       吴远     高管          本人
8  001308  康冠科技    吴远  2022-06-17  ...      3.55       吴远     高管          本人
[9 rows x 12 columns]
```
