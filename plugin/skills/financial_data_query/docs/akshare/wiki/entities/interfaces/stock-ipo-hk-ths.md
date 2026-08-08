---
title: "stock_ipo_hk_ths - 新股申购与中签-港股-同花顺"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_ipo_hk_ths

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 新股数据 > 新股申购与中签-港股-同花顺
- 描述: 同花顺-数据中心-新股申购与中签-港股
- 目标地址: https://data.10jqka.com.cn/ipo/xgsgyzq/
- 限量: 单次返回所有港股新股申购与中签数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 新股申购与中签-港股-同花顺

接口: stock_ipo_hk_ths

目标地址: https://data.10jqka.com.cn/ipo/xgsgyzq/

描述: 同花顺-数据中心-新股申购与中签-港股

限量: 单次返回所有港股新股申购与中签数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称           | 类型     | 描述 |
|--------------|--------|----|
| 股票代码         | object | -  |
| 股票简称         | object | -  |
| 申购代码         | object | -  |
| 发行总数（万股）     | object | -  |
| 网上发行（万股）     | object | -  |
| 申购上限（万股）     | object | -  |
| 顶格申购需配市值（万元） | object | -  |
| 发行价格         | object | -  |
| 发行市盈率        | object | -  |
| 行业市盈率        | object | -  |
| 申购日期         | object | -  |
| 中签率（%）       | object | -  |
| 中签号          | object | -  |
| 中签缴款日期       | object | -  |
| 上市日期         | object | -  |
| 打新收益（元）      | object | -  |
| 首日最高涨幅       | object | -  |
| 连板天数         | object | -  |

接口示例

```python
import akshare as ak

stock_ipo_hk_ths_df = ak.stock_ipo_hk_ths()
print(stock_ipo_hk_ths_df)
```

数据示例

```
     股票代码  股票简称    申购代码 发行总数（万股） 网上发行（万股） 申购上限（万股） 顶格申购需配市值（万元）   发行价格  发行市盈率  行业市盈率        申购日期 中签率（%）                                                                                                                                                                                                                                                 中签号 中签缴款日期 上市日期 打新收益（元） 首日最高涨幅 连板天数
0  920036  觅睿科技  920036  1360.55  1224.49    61.22       612.20  21.52  14.99  65.22  2026-02-26   0.03                                                                                                                                                                  -觅睿科技 网上定价发行摇号中签结果输入起始配号+查询恭喜! 您的配号中了中签结果以券商交易系统为准，仅供参考合计股，申购价缴款合计万元很遗憾，您的配号本次未中签！      -    -       -      -    -
```
