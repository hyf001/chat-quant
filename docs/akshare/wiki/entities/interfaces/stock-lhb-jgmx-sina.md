---
title: "stock_lhb_jgmx_sina - 龙虎榜-机构席位成交明细"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_lhb_jgmx_sina

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 营业部详情数据-东财 > 龙虎榜-机构席位成交明细
- 描述: 新浪财经-龙虎榜-机构席位成交明细
- 目标地址: https://vip.stock.finance.sina.com.cn/q/go.php/vLHBData/kind/jgzz/index.phtml
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 龙虎榜-机构席位成交明细

接口: stock_lhb_jgmx_sina

目标地址: https://vip.stock.finance.sina.com.cn/q/go.php/vLHBData/kind/jgzz/index.phtml

描述: 新浪财经-龙虎榜-机构席位成交明细

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称      | 类型      | 描述      |
|---------|---------|---------|
| 股票代码    | object  | -       |
| 股票名称    | object  | -       |
| 交易日期    | object  | -       |
| 机构席位买入额 | float64 | 注意单位: 万 |
| 机构席位卖出额 | float64 | 注意单位: 万 |
| 类型      | object  | -       |

接口示例

```python
import akshare as ak

stock_lhb_jgmx_sina_df = ak.stock_lhb_jgmx_sina()
print(stock_lhb_jgmx_sina_df)
```

数据示例

```
    股票代码  股票名称    交易日期  机构席位买入额(万)  机构席位卖出额(万)   类型
0    001300   三柏硕  2024-02-23     2231.89     5214.88   换手率达20%的证券
1    301378   通达海  2024-02-23      249.88     2318.76          NaN
2    300781  因赛集团  2024-02-23     7237.09    20345.79          NaN
3    300486  东杰智能  2024-02-23     3921.15     7344.49          NaN
4    300078  思创医惠  2024-02-23     2423.62     4956.84          NaN
..      ...   ...         ...         ...         ...          ...
235  301516   中远通  2024-02-19     1606.70       78.07          NaN
236  300624  万兴科技  2024-02-19        0.00    10913.05          NaN
237  002281  光迅科技  2024-02-19      224.76     2618.77  涨幅偏离值达7%的证券
238  300067   安诺其  2024-02-19     1329.52     2784.87          NaN
239  002621   美吉姆  2024-02-19      833.72     1391.98   振幅值达15%的证券
[240 rows x 6 columns]
```
