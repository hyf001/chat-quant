---
title: "option_comm_info - 商品期权手续费"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, option, parameters, returns, example]
sources: [raw/data-dictionary/option/option.md]
confidence: high
---
# option_comm_info

- 分类: [[option-option|AKShare 期权数据]]
- 主题路径: AKShare 期权数据 > 商品期权 > 商品期权手续费
- 描述: 九期网-商品期权手续费数据
- 目标地址: https://www.9qihuo.com/qiquanshouxufei
- 限量: 单次返回指定 symbol 的所有数据
- 来源页面: https://akshare.akfamily.xyz/data/option/option.html

## 相关

- [[option-option|AKShare 期权数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 商品期权手续费

接口: option_comm_info

目标地址: https://www.9qihuo.com/qiquanshouxufei

描述: 九期网-商品期权手续费数据

限量: 单次返回指定 symbol 的所有数据

输入参数

| 名称     | 类型  | 描述                                                     |
|--------|-----|--------------------------------------------------------|
| symbol | str | symbol="工业硅期权"; 可以通过 ak.option_comm_symbol() 所有 symbol |

输出参数

| 名称       | 类型     | 描述 |
|----------|--------|----|
| 期权品种     | object | -  |
| 现价       | int64  | -  |
| 涨/跌停板    | object | -  |
| 成交量      | int64  | -  |
| 类型       | object | -  |
| 权利金      | object | -  |
| 开仓       | object | -  |
| 平昨       | object | -  |
| 平今       | object | -  |
| 行权       | object | -  |
| 每跳毛利/元   | int64  | -  |
| 手续费(开+平) | object | -  |
| 每跳净利/元   | int64  | -  |
| 备注       | object | -  |
| 交易所      | object | -  |
| 手续费更新时间  | object | -  |
| 价格更新时间   | object | -  |

接口示例

```python
import akshare as ak

option_comm_info_df = ak.option_comm_info(symbol="工业硅期权")
print(option_comm_info_df)
```

数据示例

```
                                  期权品种  ...                   价格更新时间
0    工业硅期权2409--10000 (si2409-C-10000)  ...  2024-07-05 15:00:49.769
1    工业硅期权2409--10200 (si2409-C-10200)  ...  2024-07-05 15:00:49.769
2    工业硅期权2409--10400 (si2409-C-10400)  ...  2024-07-05 15:00:49.769
3    工业硅期权2409--10600 (si2409-C-10600)  ...  2024-07-05 15:00:49.769
4    工业硅期权2409--10800 (si2409-C-10800)  ...  2024-07-05 15:00:49.769
..                                 ...  ...                      ...
303  工业硅期权2506--14400 (si2506-P-14400)  ...  2024-07-05 15:00:49.769
304  工业硅期权2506--16000 (si2506-P-16000)  ...  2024-07-05 15:00:49.769
305  工业硅期权2506--16200 (si2506-P-16200)  ...  2024-07-05 15:00:49.769
306  工业硅期权2506--16400 (si2506-P-16400)  ...  2024-07-05 15:00:49.769
307  工业硅期权2506--16600 (si2506-P-16600)  ...  2024-07-05 15:00:49.769
[308 rows x 17 columns]
```
