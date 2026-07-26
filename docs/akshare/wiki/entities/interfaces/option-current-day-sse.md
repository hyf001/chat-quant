---
title: "option_current_day_sse - 当日合约-上海证券交易所"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, option, parameters, returns, example]
sources: [raw/data-dictionary/option/option.md]
confidence: high
---
# option_current_day_sse

- 分类: [[option-option|AKShare 期权数据]]
- 主题路径: AKShare 期权数据 > 金融期权-三大交易所 > 当日合约-上海证券交易所
- 描述: 上海证券交易所-产品-股票期权-信息披露-当日合约
- 目标地址: https://www.sse.com.cn/assortment/options/disclo/preinfo/
- 限量: 单次返回所有数据
- 来源页面: https://akshare.akfamily.xyz/data/option/option.html

## 相关

- [[option-option|AKShare 期权数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 当日合约-上海证券交易所

接口: option_current_day_sse

目标地址: https://www.sse.com.cn/assortment/options/disclo/preinfo/

描述: 上海证券交易所-产品-股票期权-信息披露-当日合约

限量: 单次返回所有数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称       | 类型     | 描述 |
|----------|--------|----|
| 合约编码     | object | -  |
| 合约交易代码   | object | -  |
| 合约简称     | object | -  |
| 标的券名称及代码 | object | -  |
| 类型       | object | -  |
| 行权价      | object | -  |
| 合约单位     | object | -  |
| 期权行权日    | object | -  |
| 行权交收日    | object | -  |
| 到期日      | object | -  |
| 开始日期     | object | -  |

接口示例

```python
import akshare as ak

option_current_day_sse_df = ak.option_current_day_sse()
print(option_current_day_sse_df)
```

数据示例

```
      合约编码  合约交易代码         合约简称  ...     行权交收日      到期日     开始日期
0    10009163  510050C2509M02350  50ETF购9月2350  ...  20250925  20250924  20250408
1    10008793  510050C2509M02400  50ETF购9月2400  ...  20250925  20250924  20250123
2    10008794  510050C2509M02450  50ETF购9月2450  ...  20250925  20250924  20250123
3    10008795  510050C2509M02500  50ETF购9月2500  ...  20250925  20250924  20250123
4    10008796  510050C2509M02550  50ETF购9月2550  ...  20250925  20250924  20250123
..        ...                ...           ...  ...       ...       ...       ...
639  10009808  588080P2603M01400  科创板50沽3月1400  ...  20260326  20260325  20250821
640  10009863  588080P2603M01450  科创板50沽3月1450  ...  20260326  20260325  20250825
641  10009864  588080P2603M01500  科创板50沽3月1500  ...  20260326  20260325  20250825
642  10009888  588080P2603M01550  科创板50沽3月1550  ...  20260326  20260325  20250826
643  10010006  588080P2603M01600  科创板50沽3月1600  ...  20260326  20260325  20250829
[644 rows x 11 columns]
```
