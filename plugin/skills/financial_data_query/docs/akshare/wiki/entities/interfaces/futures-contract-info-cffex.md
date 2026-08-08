---
title: "futures_contract_info_cffex - 中国金融期货交易所"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, futures, parameters, returns, example]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# futures_contract_info_cffex

- 分类: [[futures-futures|AKShare 期货数据]]
- 主题路径: AKShare 期货数据 > 期货基础数据 > 合约信息 > 中国金融期货交易所
- 描述: 中国金融期货交易所-数据-交易参数
- 目标地址: http://www.gfex.com.cn/gfex/hyxx/ywcs.shtml
- 限量: 单次返回指定 date 的期货合约信息数据
- 来源页面: https://akshare.akfamily.xyz/data/futures/futures.html

## 相关

- [[futures-futures|AKShare 期货数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 中国金融期货交易所

接口: futures_contract_info_cffex

目标地址: http://www.gfex.com.cn/gfex/hyxx/ywcs.shtml

描述: 中国金融期货交易所-数据-交易参数

限量: 单次返回指定 date 的期货合约信息数据

输入参数

| 名称   | 类型  | 描述                   |
|------|-----|----------------------|
| date | str | date="20240228"; 交易日 |

输出参数

| 名称    | 类型      | 描述 |
|-------|---------|----|
| 合约代码  | object  | -  |
| 合约月份  | object  | -  |
| 挂盘基准价 | float64 | -  |
| 上市日   | object  | -  |
| 最后交易日 | object  | -  |
| 涨停板幅度 | object  | -  |
| 跌停板幅度 | object  | -  |
| 涨停板价位 | float64 | -  |
| 跌停板价位 | float64 | -  |
| 持仓限额  | int64   | -  |
| 品种    | object  | -  |
| 查询交易日 | object  | -  |

接口示例

```python
import akshare as ak

futures_contract_info_cffex_df = ak.futures_contract_info_cffex(date="20240228")
print(futures_contract_info_cffex_df)
```

数据示例

```
        合约代码    合约月份    挂盘基准价 上市日  ...  跌停板价位 持仓限额 品种  查询交易日
0           TS2409  2409  100.974  2023-12-11  ...  101.056  2000  TS  2024-02-28
1           TS2406  2406  101.065  2023-09-11  ...  101.020  2000  TS  2024-02-28
2           TS2403  2403  101.145  2023-06-12  ...  100.858  2000  TS  2024-02-28
3           TL2409  2409   99.330  2023-12-11  ...  102.990  2000  TL  2024-02-28
4           TL2406  2406   98.750  2023-09-11  ...  102.870  2000  TL  2024-02-28
..             ...   ...      ...         ...  ...      ...   ...  ..         ...
831  HO2403-C-2075  2403  193.200  2023-12-18  ...   83.800  1200  HO  2024-02-28
832  HO2403-C-2050  2403  253.400  2023-12-06  ...  115.000  1200  HO  2024-02-28
833  HO2403-C-2025  2403  234.800  2023-12-18  ...  133.600  1200  HO  2024-02-28
834  HO2403-C-2000  2403  286.200  2023-12-08  ...  158.600  1200  HO  2024-02-28
835  HO2403-C-1975  2403  241.200  2024-01-18  ...  189.600  1200  HO  2024-02-28
[836 rows x 12 columns]
```
