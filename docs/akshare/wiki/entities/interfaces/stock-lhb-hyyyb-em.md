---
title: "stock_lhb_hyyyb_em - 每日活跃营业部"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_lhb_hyyyb_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 龙虎榜 > 龙虎榜-东财 > 每日活跃营业部
- 描述: 东方财富网-数据中心-龙虎榜单-每日活跃营业部
- 目标地址: https://data.eastmoney.com/stock/hyyyb.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 每日活跃营业部

接口: stock_lhb_hyyyb_em

目标地址: https://data.eastmoney.com/stock/hyyyb.html

描述: 东方财富网-数据中心-龙虎榜单-每日活跃营业部

限量: 单次返回所有历史数据

输入参数

| 名称         | 类型  | 描述                    |
|------------|-----|-----------------------|
| start_date | str | start_date="20220311" |
| end_date   | str | end_date="20220315"   |

输出参数

| 名称    | 类型      | 描述      |
|-------|---------|---------|
| 序号    | int64   | -       |
| 营业部名称 | object  | -       |
| 上榜日   | object  | -       |
| 买入个股数 | float64 | -       |
| 卖出个股数 | float64 | -       |
| 买入总金额 | float64 | 注意单位: 元 |
| 卖出总金额 | float64 | 注意单位: 元 |
| 总买卖净额 | float64 | 注意单位: 元 |
| 买入股票  | object  | -       |

接口示例

```python
import akshare as ak

stock_lhb_hyyyb_em_df = ak.stock_lhb_hyyyb_em(start_date="20220324", end_date="20220324")
print(stock_lhb_hyyyb_em_df)
```

数据示例

```
       序号  ...                                               买入股票
0        1  ...  中信海直 高新发展 张裕A 新乡化纤 宗申动力 湖南黄金 桂林三金 科华数据 柘中股份 *S...
1        2  ...  中信海直 焦作万方 北方铜业 钱江摩托 新乡化纤 ST中南 百通能源 宗申动力 万丰奥威 百...
2        3  ...                                               宗申动力
3        4  ...                                               罗博特科
4        5  ...                                          中科通达 神州信息
...    ...  ...                                                ...
7532  7533  ...  万科A 中信海直 神州信息 高新发展 康冠科技 宗申动力 万丰奥威 沃尔核材 江特电机 雪迪...
7533  7534  ...  中信海直 我爱我家 长安汽车 高新发展 天保基建 万丰奥威 荣盛发展 百川股份 万安科技 奥...
7534  7535  ...                                               长安汽车
7535  7536  ...  双良节能 鲁信创投 江苏银行 太平洋 东方材料 日出东方 金域医学 国盾量子 信安世纪 财富...
7536  7537  ...                                          长安汽车 荣盛发展
[7537 rows x 9 columns]
```
