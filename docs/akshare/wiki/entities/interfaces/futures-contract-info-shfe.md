---
title: "futures_contract_info_shfe - 上海期货交易所"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, futures, parameters, returns, example]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# futures_contract_info_shfe

- 分类: [[futures-futures|AKShare 期货数据]]
- 主题路径: AKShare 期货数据 > 期货基础数据 > 合约信息 > 上海期货交易所
- 描述: 上海期货交易所-交易所服务-业务数据-交易参数汇总查询
- 目标地址: https://tsite.shfe.com.cn/bourseService/businessdata/summaryinquiry/
- 限量: 单次返回指定 date 的期货合约信息数据
- 来源页面: https://akshare.akfamily.xyz/data/futures/futures.html

## 相关

- [[futures-futures|AKShare 期货数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 上海期货交易所

接口: futures_contract_info_shfe

目标地址: https://tsite.shfe.com.cn/bourseService/businessdata/summaryinquiry/

描述: 上海期货交易所-交易所服务-业务数据-交易参数汇总查询

限量: 单次返回指定 date 的期货合约信息数据

输入参数

| 名称   | 类型  | 描述                   |
|------|-----|----------------------|
| date | str | date="20240513"; 交易日 |

输出参数

| 名称    | 类型      | 描述 |
|-------|---------|----|
| 合约代码  | object  | -  |
| 上市日   | object  | -  |
| 到期日   | object  | -  |
| 开始交割日 | object  | -  |
| 最后交割日 | object  | -  |
| 挂牌基准价 | float64 | -  |
| 交易日   | object  | -  |
| 更新时间  | object  | -  |

接口示例

```python
import akshare as ak

futures_contract_info_shfe_df = ak.futures_contract_info_shfe(date="20240513")
print(futures_contract_info_shfe_df)
```

数据示例

```
     合约代码  上市日       到期日  ...    挂牌基准价    交易日               更新时间
0    cu2405  2023-05-16  2024-05-15  ...  64490.0  2024-05-13  2024-05-13 18:21:10
1    cu2406  2023-06-16  2024-06-17  ...  66930.0  2024-05-13  2024-05-13 18:21:10
2    cu2407  2023-07-18  2024-07-15  ...  68220.0  2024-05-13  2024-05-13 18:21:10
3    cu2408  2023-08-16  2024-08-15  ...  67270.0  2024-05-13  2024-05-13 18:21:10
4    cu2409  2023-09-18  2024-09-18  ...  68900.0  2024-05-13  2024-05-13 18:21:10
..      ...         ...         ...  ...      ...         ...                  ...
271  ec2408  2023-08-18  2024-08-26  ...    780.0  2024-05-13  2024-05-13 18:21:10
272  ec2410  2023-08-18  2024-10-28  ...    780.0  2024-05-13  2024-05-13 18:21:10
273  ec2412  2023-08-18  2024-12-30  ...    780.0  2024-05-13  2024-05-13 18:21:10
274  ec2502  2024-02-27  2025-02-24  ...   1359.8  2024-05-13  2024-05-13 18:21:10
275  ec2504  2024-04-30  2025-04-28  ...   2158.3  2024-05-13  2024-05-13 18:21:10
[276 rows x 8 columns]
```
