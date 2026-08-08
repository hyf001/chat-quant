---
title: "fund_etf_hist_sina - 基金历史行情-新浪"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_etf_hist_sina

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金行情 > 基金历史行情-新浪
- 描述: 新浪财经-基金行情的日频率行情数据
- 目标地址: http://vip.stock.finance.sina.com.cn/fund_center/index.html#jjhqetf
- 限量: 单次返回指定基金的所有数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 基金历史行情-新浪

接口: fund_etf_hist_sina

目标地址: http://vip.stock.finance.sina.com.cn/fund_center/index.html#jjhqetf

描述: 新浪财经-基金行情的日频率行情数据

限量: 单次返回指定基金的所有数据

输入参数

| 名称     | 类型  | 描述                                                                                                      |
|--------|-----|---------------------------------------------------------------------------------------------------------|
| symbol | str | symbol="sh510050"; 基金列表可以通过 **ak.fund_etf_category_sina(symbol="LOF基金")** 可选参数为: 封闭式基金, ETF基金, LOF基金 查询 |

输出参数

| 名称     | 类型      | 描述      |
|--------|---------|---------|
| date   | object  | -       |
| open   | float64 | -       |
| high   | float64 | -       |
| low    | float64 | -       |
| close  | float64 | -       |
| volume | int64   | 注意单位: 手 |

接口示例

```python
import akshare as ak

fund_etf_hist_sina_df = ak.fund_etf_hist_sina(symbol="sh510050")
print(fund_etf_hist_sina_df)
```

数据示例

```
            date   open   high    low  close      volume
0     2005-02-23  0.881  0.882  0.866  0.876  1269742542
1     2005-02-24  0.876  0.876  0.868  0.876   451614223
2     2005-02-25  0.877  0.887  0.875  0.880   506460695
3     2005-02-28  0.878  0.879  0.870  0.872   187965193
4     2005-03-01  0.870  0.873  0.865  0.867   208094456
...          ...    ...    ...    ...    ...         ...
4796  2024-11-15  2.808  2.821  2.777  2.778  1394418910
4797  2024-11-18  2.789  2.835  2.776  2.790  1199619816
4798  2024-11-19  2.786  2.793  2.743  2.778   919468916
4799  2024-11-20  2.772  2.794  2.764  2.784   854979945
4800  2024-11-21  2.780  2.795  2.772  2.791   738982704
[4801 rows x 6 columns]
```
