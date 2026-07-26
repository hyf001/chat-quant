---
title: "futures_comm_js - 金十数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, futures, parameters, returns, example]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# futures_comm_js

- 分类: [[futures-futures|AKShare 期货数据]]
- 主题路径: AKShare 期货数据 > 期货基础数据 > 期货手续费与保证金 > 金十数据
- 描述: 金十财经-期货手续费数据
- 目标地址: https://www.jin10.com/
- 限量: 单次返回指定日期的期货手续费数据
- 来源页面: https://akshare.akfamily.xyz/data/futures/futures.html

## 相关

- [[futures-futures|AKShare 期货数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 金十数据

接口: futures_comm_js

目标地址: https://www.jin10.com/

描述: 金十财经-期货手续费数据

限量: 单次返回指定日期的期货手续费数据

输入参数

| 名称   | 类型  | 描述                              |
|------|-----|---------------------------------|
| date | str | date="20260213"; 日期格式为 YYYYMMDD |

输出参数

| 名称      | 类型      | 描述 |
|---------|---------|----|
| 日期      | object  | -  |
| 合约品种    | str     | -  |
| 合约代码    | str     | -  |
| 手续费公布时间 | str     | -  |
| 价格公布时间  | str     | -  |
| 现价      | float64 | -  |
| 涨停板     | float64 | -  |
| 跌停板     | float64 | -  |
| 保证金/买开  | str     | -  |
| 保证金/卖开  | str     | -  |
| 保证金/每手  | str     | -  |
| 开仓      | str     | -  |
| 平今      | str     | -  |
| 平昨      | str     | -  |
| 每手跳数    | int64   | -  |
| 每跳毛利    | float64 | -  |
| 每跳净利    | float64 | -  |
| 交易所     | str     | -  |

接口示例

```python
import akshare as ak

futures_comm_js_df = ak.futures_comm_js(date="20260213")
print(futures_comm_js_df)
```

数据示例

```
    日期        合约品种    合约代码  ... 每跳毛利   每跳净利         交易所
0   2026-02-13      黄金2604  au2604  ...  NaN    0.0     上海期货交易所
1   2026-02-13      鸡蛋2604  jd2604  ...  NaN    0.5     大连商品交易所
2   2026-02-13    集运指数2604  ec2604  ...  NaN -105.5  上海国际能源交易中心
3   2026-02-13       锰硅605   SM605  ...  NaN    7.0     郑州商品交易所
4   2026-02-13     铸造铝2604  ad2604  ...  NaN   38.9     上海期货交易所
..         ...         ...     ...  ...  ...    ...         ...
85  2026-02-13   5年期国债2603  TF2603  ...  NaN   47.0   中国金融期货交易所
86  2026-02-13  30年期国债2603  TL2603  ...  NaN   97.0   中国金融期货交易所
87  2026-02-13   2年期国债2603  TS2603  ...  NaN   37.0   中国金融期货交易所
88  2026-02-13    20号胶2604  nr2604  ...  NaN   47.3  上海国际能源交易中心
89  2026-02-13   10年国债2603   T2603  ...  NaN   47.0   中国金融期货交易所
[90 rows x 18 columns]
```
