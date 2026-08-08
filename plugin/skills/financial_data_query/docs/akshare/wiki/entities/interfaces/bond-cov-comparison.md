---
title: "bond_cov_comparison - 可转债比价表"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, bond, parameters, returns, example]
sources: [raw/data-dictionary/bond/bond.md]
confidence: high
---
# bond_cov_comparison

- 分类: [[bond-bond|AKShare 债券数据]]
- 主题路径: AKShare 债券数据 > 沪深可转债 > 可转债比价表
- 描述: 东方财富网-行情中心-债券市场-可转债比价表
- 目标地址: https://quote.eastmoney.com/center/fullscreenlist.html#convertible_comparison
- 限量: 单次返回当前交易时刻的所有可转债比价数据
- 来源页面: https://akshare.akfamily.xyz/data/bond/bond.html

## 相关

- [[bond-bond|AKShare 债券数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 可转债比价表

接口: bond_cov_comparison

目标地址: https://quote.eastmoney.com/center/fullscreenlist.html#convertible_comparison

描述: 东方财富网-行情中心-债券市场-可转债比价表

限量: 单次返回当前交易时刻的所有可转债比价数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称    | 类型      | 描述      |
|-------|---------|---------|
| 序号    | int32   | -       |
| 转债代码  | object  | -       |
| 转债名称  | object  | -       |
| 转债最新价 | object  | -       |
| 转债涨跌幅 | object  | 注意单位: % |
| 正股代码  | object  | -       |
| 正股名称  | object  | -       |
| 正股最新价 | object  | -       |
| 正股涨跌幅 | object  | 注意单位: % |
| 转股价   | object  | -       |
| 转股价值  | object  | -       |
| 转股溢价率 | object  | 注意单位: % |
| 纯债溢价率 | object  | 注意单位: % |
| 回售触发价 | object  | -       |
| 强赎触发价 | object  | -       |
| 到期赎回价 | object  | -       |
| 纯债价值  | float64 | -       |
| 开始转股日 | object  | -       |
| 上市日期  | object  | -       |
| 申购日期  | object  | -       |

接口示例

```python
import akshare as ak

bond_cov_comparison_df = ak.bond_cov_comparison()
print(bond_cov_comparison_df)
```

数据示例

```
      序号 转债代码  转债名称  转债最新价  ... 纯债价值   开始转股日  上市日期   申购日期
0      1  127105   龙星转债        -  ...   87.5843  20240807  20240306  20240201
1      2  123240   楚天转债        -  ...   95.2117  20240806  20240229  20240131
2      3  127104   姚记转债  145.688  ...   78.7398  20240731  20240226  20240125
3      4  123239   锋工转债   120.99  ...   77.9967  20240725  20240222  20240119
4      5  123238  卡倍转02  120.322  ...   78.1354  20240717  20240201  20240111
..   ...     ...    ...      ...  ...       ...       ...       ...       ...
545  546  127006   敖东转债  105.995  ...  104.9099  20180919  20180511  20180313
546  547  127005   长证转债   104.89  ...  104.9193  20180917  20180411  20180312
547  548  128036   金农转债  105.732  ...  105.6951  20180917  20180402  20180309
548  549  113505   杭电转债   107.85  ...  107.9525  20180912  20180327  20180306
549  550  113504   艾华转债  105.924  ...  105.9800  20180910  20180323  20180302
[550 rows x 20 columns]
```
