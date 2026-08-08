---
title: "futures_spot_sys - 现期图"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, futures, parameters, returns, example]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# futures_spot_sys

- 分类: [[futures-futures|AKShare 期货数据]]
- 主题路径: AKShare 期货数据 > 期货基础数据 > 现期图
- 描述: 生意社-商品与期货-现期图
- 目标地址: https://www.100ppi.com/sf/792.html
- 限量: 单次返回指定品种的现期图数据
- 来源页面: https://akshare.akfamily.xyz/data/futures/futures.html

## 相关

- [[futures-futures|AKShare 期货数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 现期图

接口: futures_spot_sys

目标地址: https://www.100ppi.com/sf/792.html

描述: 生意社-商品与期货-现期图

限量: 单次返回指定品种的现期图数据

输入参数

| 名称       | 类型  | 描述                                                  |
|----------|-----|-----------------------------------------------------|
| symbol   | str | symbol="铜"; 期货品种                                    |
| contract | str | indicator="市场价格"; choice of {"市场价格", "基差率", "主力基差"} |

输出参数-市场价格

| 名称   | 类型      | 描述 |
|------|---------|----|
| 日期   | object  | -  |
| 现货价格 | float64 | -  |
| 主力合约 | float64 | -  |
| 最近合约 | float64 | -  |

接口示例-市场价格

```python
import akshare as ak

futures_spot_sys_df = ak.futures_spot_sys(symbol="铜", indicator="市场价格")
print(futures_spot_sys_df)
```

数据示例-市场价格

```
     日期   现货价格    主力合约     最近合约
0   11-26  68661.67      NaN      NaN
1   12-05  69005.00  68200.0  68570.0
2   12-14  68613.33  68030.0  68570.0
3   12-23  69418.33      NaN      NaN
4   01-01  69250.00      NaN      NaN
5   01-10  68200.00  67920.0  68110.0
6   01-19  67813.33  67630.0  67680.0
7   01-28  68943.33      NaN      NaN
8   02-06  68001.67  68130.0  68010.0
9   02-15  67710.00      NaN      NaN
10  02-24  69351.67      NaN      NaN
```

输出参数-基差率

| 名称  | 类型      | 描述 |
|-----|---------|----|
| 日期  | object  | -  |
| 基差率 | float64 | -  |

接口示例-基差率

```python
import akshare as ak

futures_spot_sys_df = ak.futures_spot_sys(symbol="铜", indicator="基差率")
print(futures_spot_sys_df)
```

数据示例-基差率

```
     日期   基差率
0   11-26   NaN
1   12-05  1.17
2   12-14  0.85
3   12-23   NaN
4   01-01   NaN
5   01-10  0.41
6   01-19  0.27
7   01-28   NaN
8   02-06 -0.19
9   02-15   NaN
10  02-24   NaN
```

输出参数-主力基差

| 名称   | 类型      | 描述 |
|------|---------|----|
| 日期   | object  | -  |
| 主力基差 | float64 | -  |

接口示例-主力基差

```python
import akshare as ak

futures_spot_sys_df = ak.futures_spot_sys(symbol="铜", indicator="主力基差")
print(futures_spot_sys_df)
```

数据示例-主力基差

```
    日期    主力基差
0   11-26     NaN
1   12-05  805.00
2   12-14  583.33
3   12-23     NaN
4   01-01     NaN
5   01-10  280.00
6   01-19  183.33
7   01-28     NaN
8   02-06 -128.33
9   02-15     NaN
10  02-24     NaN
```
