---
title: "stock_irm_cninfo - 互动易-提问"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_irm_cninfo

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 股票热度 > 互动平台 > 互动易-提问
- 描述: 互动易-提问
- 目标地址: https://irm.cninfo.com.cn/
- 限量: 单次返回近期 10000 条提问数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 互动易-提问

接口: stock_irm_cninfo

目标地址: https://irm.cninfo.com.cn/

描述: 互动易-提问

限量: 单次返回近期 10000 条提问数据

输入参数

| 名称     | 类型  | 描述                |
|--------|-----|-------------------|
| symbol | str | symbol="002594";  |

输出参数

| 名称    | 类型             | 描述 |
|-------|----------------|----|
| 股票代码  | object         | -  |
| 公司简称  | object         | -  |
| 行业    | object         | -  |
| 行业代码  | object         | -  |
| 问题    | object         | -  |
| 提问者   | object         | -  |
| 来源    | object         | -  |
| 提问时间  | datetime64[ns] | -  |
| 更新时间  | datetime64[ns] | -  |
| 提问者编号 | object         | -  |
| 问题编号  | object         | -  |
| 回答ID  | object         | -  |
| 回答内容  | object         | -  |
| 回答者   | object         | -  |

接口示例

```python
import akshare as ak

stock_irm_cninfo_df = ak.stock_irm_cninfo(symbol="002594")
print(stock_irm_cninfo_df)
```

数据示例

```
      股票代码 公司简称  ...                                               回答内容   回答者
0     002594  比亚迪  ...                                               None  None
1     002594  比亚迪  ...                                               None  None
2     002594  比亚迪  ...                                               None  None
3     002594  比亚迪  ...                                               None  None
4     002594  比亚迪  ...                                               None  None
...      ...  ...  ...                                                ...   ...
9995  002594  比亚迪  ...                                            感谢您的建议！   比亚迪
9996  002594  比亚迪  ...             感谢对公司的关注，未来公司将综合各个基地的产能协调生产，保证产能充足，谢谢！   比亚迪
9997  002594  比亚迪  ...  目前电动叉车项目还在产品推广的初期，市场尚不够熟悉，未来公司会通过创新销售方式、拓宽销售渠道...   比亚迪
9998  002594  比亚迪  ...                                         请见之前回复，谢谢！   比亚迪
9999  002594  比亚迪  ...                                                谢谢！   比亚迪
[10000 rows x 14 columns]
```
