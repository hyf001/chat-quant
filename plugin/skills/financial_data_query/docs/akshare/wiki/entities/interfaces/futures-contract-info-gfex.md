---
title: "futures_contract_info_gfex - 广州期货交易所"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, futures, parameters, returns, example]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# futures_contract_info_gfex

- 分类: [[futures-futures|AKShare 期货数据]]
- 主题路径: AKShare 期货数据 > 期货基础数据 > 合约信息 > 广州期货交易所
- 描述: 广州期货交易所-业务/服务-合约信息
- 目标地址: http://www.gfex.com.cn/gfex/hyxx/ywcs.shtml
- 限量: 单次返回最近交易日的期货合约信息数据
- 来源页面: https://akshare.akfamily.xyz/data/futures/futures.html

## 相关

- [[futures-futures|AKShare 期货数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 广州期货交易所

接口: futures_contract_info_gfex

目标地址: http://www.gfex.com.cn/gfex/hyxx/ywcs.shtml

描述: 广州期货交易所-业务/服务-合约信息

限量: 单次返回最近交易日的期货合约信息数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称     | 类型     | 描述 |
|--------|--------|----|
| 品种     | object | -  |
| 合约代码   | object | -  |
| 交易单位   | int64  | -  |
| 最小变动单位 | int64  | -  |
| 开始交易日  | object | -  |
| 最后交易日  | object | -  |
| 最后交割日  | object | -  |

接口示例

```python
import akshare as ak

futures_contract_info_gfex_df = ak.futures_contract_info_gfex()
print(futures_contract_info_gfex_df)
```

数据示例

```
     品种    合约代码  交易单位  最小变动单位       开始交易日       最后交易日       最后交割日
0   碳酸锂  lc2403     1      50  2023-07-21  2024-03-14  2024-03-19
1   碳酸锂  lc2404     1      50  2023-07-21  2024-04-16  2024-04-19
2   碳酸锂  lc2405     1      50  2023-07-21  2024-05-17  2024-05-22
3   碳酸锂  lc2406     1      50  2023-07-21  2024-06-17  2024-06-20
4   碳酸锂  lc2407     1      50  2023-07-21  2024-07-12  2024-07-17
5   碳酸锂  lc2408     1      50  2023-08-15  2024-08-14  2024-08-19
6   碳酸锂  lc2409     1      50  2023-09-15  2024-09-13  2024-09-20
7   碳酸锂  lc2410     1      50  2023-10-23  2024-10-21  2024-10-24
8   碳酸锂  lc2411     1      50  2023-11-15  2024-11-14  2024-11-19
9   碳酸锂  lc2412     1      50  2023-12-15  2024-12-13  2024-12-18
10  碳酸锂  lc2501     1      50  2024-01-16  2025-01-15  2025-01-20
11  碳酸锂  lc2502     1      50  2024-02-23  2025-02-24  2025-02-27
12  工业硅  si2403     5       5  2023-03-15  2024-03-14  2024-03-19
13  工业硅  si2404     5       5  2023-08-15  2024-04-16  2024-04-19
14  工业硅  si2405     5       5  2023-09-15  2024-05-17  2024-05-22
15  工业硅  si2406     5       5  2023-10-23  2024-06-17  2024-06-20
16  工业硅  si2407     5       5  2023-11-15  2024-07-12  2024-07-17
17  工业硅  si2408     5       5  2023-12-15  2024-08-14  2024-08-19
18  工业硅  si2409     5       5  2024-01-16  2024-09-13  2024-09-20
19  工业硅  si2410     5       5  2024-02-23  2024-10-21  2024-10-24
```
