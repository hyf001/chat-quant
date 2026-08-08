---
title: "stock_info_a_code_name - 股票列表-A股"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_info_a_code_name

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 股票列表-A股
- 描述: 沪深京 A 股股票代码和股票简称数据
- 目标地址: 沪深京三个交易所
- 限量: 单次获取所有 A 股股票代码和简称数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 股票列表-A股

接口: stock_info_a_code_name

目标地址: 沪深京三个交易所

描述: 沪深京 A 股股票代码和股票简称数据

限量: 单次获取所有 A 股股票代码和简称数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称   | 类型     | 描述  |
|------|--------|-----|
| code | object | -   |
| name | object | -   |

接口示例

```python
import akshare as ak

stock_info_a_code_name_df = ak.stock_info_a_code_name()
print(stock_info_a_code_name_df)
```

数据示例

```
        code   name
0     000001   平安银行
1     000002  万  科Ａ
2     000004   国华网安
3     000005   ST星源
4     000006   深振业Ａ
      ...    ...
4623  871396   常辅股份
4624  871553   凯腾精工
4625  871642   通易航天
4626  871981   晶赛科技
4627  872925   锦好医疗
```
