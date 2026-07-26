---
title: "bond_china_close_return - 收盘收益率曲线历史数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, bond, parameters, returns, example]
sources: [raw/data-dictionary/bond/bond.md]
confidence: high
---
# bond_china_close_return

- 分类: [[bond-bond|AKShare 债券数据]]
- 主题路径: AKShare 债券数据 > 收盘收益率曲线历史数据
- 描述: 收盘收益率曲线历史数据, 该接口只能获取近 3 个月的数据，且每次获取的数据不超过 1 个月
- 目标地址: https://www.chinamoney.com.cn/chinese/bkcurvclosedyhis/?bondType=CYCC000&reference=1
- 来源页面: https://akshare.akfamily.xyz/data/bond/bond.html

## 相关

- [[bond-bond|AKShare 债券数据]]
- [[_meta/topic-map]]

## 源文摘录

### 收盘收益率曲线历史数据

接口: bond_china_close_return

目标地址: https://www.chinamoney.com.cn/chinese/bkcurvclosedyhis/?bondType=CYCC000&reference=1

描述: 收盘收益率曲线历史数据, 该接口只能获取近 3 个月的数据，且每次获取的数据不超过 1 个月

输入参数

| 名称         | 类型  | 描述                                                                       |
|------------|-----|--------------------------------------------------------------------------|
| symbol     | str | symbol="政策性金融债(进出口行)"; 通过网页查询或调用 **ak.bond_china_close_return_map()** 获取 |
| period     | str | period: str = "1"; 期限间隔, choice of {'0.1', '0.5', '1'}                   |
| start_date | str | start_date="20231101"; 结束日期, 结束日期和开始日期不要超过 1 个月                          |
| end_date   | str | end_date="20231101"; 结束日期, 结束日期和开始日期不要超过 1 个月                            |

输出参数

| 名称    | 类型      | 描述  |
|-------|---------|-----|
| 日期    | object  | -   |
| 期限    | float64 | -   |
| 到期收益率 | float64 | -   |
| 即期收益率 | float64 | -   |
| 远期收益率 | float64 | -   |

接口示例

```python
import akshare as ak

bond_china_close_return_df = ak.bond_china_close_return(symbol="国债", period="1", start_date="20231101", end_date="20231101")
print(bond_china_close_return_df)
```

数据示例

```
       日期       期限   到期收益率 即期收益率  远期收益率
0   2023-11-01   0.083  1.7031  1.7031     NaN
1   2023-11-01   0.250  2.3102  2.3102     NaN
2   2023-11-01   0.500  2.3825  2.3825     NaN
3   2023-11-01   0.750  2.2547  2.2547     NaN
4   2023-11-01   1.000  2.2452  2.2452  2.5188
5   2023-11-01   2.000  2.3803  2.3819  2.5649
6   2023-11-01   3.000  2.4403  2.4429  2.6295
7   2023-11-01   4.000  2.4858  2.4895  2.7256
8   2023-11-01   5.000  2.5313  2.5367  3.0216
9   2023-11-01   6.000  2.6076  2.6174  3.1898
10  2023-11-01   7.000  2.6838  2.6989  2.6956
11  2023-11-01   8.000  2.6851  2.6985  2.6986
12  2023-11-01   9.000  2.6865  2.6985  2.7016
13  2023-11-01  10.000  2.6878  2.6988  2.9891
14  2023-11-01  11.000  2.7115  2.7252  3.0458
```
