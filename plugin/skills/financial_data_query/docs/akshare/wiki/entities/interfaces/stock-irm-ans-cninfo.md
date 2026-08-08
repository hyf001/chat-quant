---
title: "stock_irm_ans_cninfo - 互动易-回答"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_irm_ans_cninfo

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 股票热度 > 互动平台 > 互动易-回答
- 描述: 互动易-回答
- 目标地址: https://irm.cninfo.com.cn/
- 限量: 单次返回指定 symbol 的回答数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 互动易-回答

接口: stock_irm_ans_cninfo

目标地址: https://irm.cninfo.com.cn/

描述: 互动易-回答

限量: 单次返回指定 symbol 的回答数据

输入参数

| 名称     | 类型  | 描述                                                               |
|--------|-----|------------------------------------------------------------------|
| symbol | str | symbol="1495108801386602496"; 通过 ak.stock_irm_cninfo 来获取具体的提问者编号 |

输出参数

| 名称   | 类型             | 描述 |
|------|----------------|----|
| 股票代码 | object         | -  |
| 公司简称 | object         | -  |
| 问题   | object         | -  |
| 回答内容 | object         | -  |
| 提问者  | object         | -  |
| 提问时间 | datetime64[ns] | -  |
| 回答时间 | datetime64[ns] | -  |

接口示例

```python
import akshare as ak

stock_irm_ans_cninfo_df = ak.stock_irm_ans_cninfo(symbol="1495108801386602496")
print(stock_irm_ans_cninfo_df)
```

数据示例

```
     股票代码 公司简称  ...                提问时间                回答时间
0  002594  比亚迪  ... 2023-07-08 04:12:53 2023-07-12 00:34:31
[1 rows x 7 columns]
```
