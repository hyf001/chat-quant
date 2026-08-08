---
title: "bond_cb_redeem_jsl - 可转债强赎"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, bond, parameters, returns, example]
sources: [raw/data-dictionary/bond/bond.md]
confidence: high
---
# bond_cb_redeem_jsl

- 分类: [[bond-bond|AKShare 债券数据]]
- 主题路径: AKShare 债券数据 > 可转债强赎
- 描述: 集思录可转债-强赎
- 目标地址: https://www.jisilu.cn/data/cbnew/#redeem
- 限量: 单次返回所有数据
- 来源页面: https://akshare.akfamily.xyz/data/bond/bond.html

## 相关

- [[bond-bond|AKShare 债券数据]]
- [[_meta/topic-map]]

## 源文摘录

### 可转债强赎

接口: bond_cb_redeem_jsl

目标地址: https://www.jisilu.cn/data/cbnew/#redeem

描述: 集思录可转债-强赎

限量: 单次返回所有数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称    | 类型      | 描述      |
|-------|---------|---------|
| 代码    | object  | -       |
| 名称    | object  | -       |
| 现价    | float64 | -       |
| 正股代码  | object  | -       |
| 正股名称  | object  | -       |
| 规模    | float64 | 注意单位: 亿 |
| 剩余规模  | float64 | -       |
| 转股起始日 | object  | -       |
| 最后交易日 | object  | -       |
| 到期日   | object  | -       |
| 转股价   | float64 | -       |
| 强赎触发比 | int64   | 注意单位: % |
| 强赎触发价 | float64 | -       |
| 正股价   | float64 | -       |
| 强赎价   | float64 | -       |
| 强赎天计数 | object  | -       |
| 强赎条款  | object  | -       |
| 强赎状态  | object  | -       |

接口示例

```python
import akshare as ak

bond_cb_redeem_jsl_df = ak.bond_cb_redeem_jsl()
print(bond_cb_redeem_jsl_df)
```

数据示例

```
         代码    名称       现价  ...       强赎天计数                           强赎条款   强赎状态
0    123084  高澜转债  144.600  ...  25/15 | 30  如果公司股票在任意连续三十个交易日中至少十五个交易日...  已公告强赎
1    123070  鹏辉转债  369.543  ...  30/20 | 30  如果公司A股股票连续30个交易日中至少有20个交易日...  已公告强赎
2    113599  嘉友转债  139.980  ...  22/15 | 30  如果公司股票连续三十个交易日中至少有十五个交易日的收...  已公告强赎
3    113630  赛伍转债  131.550  ...  20/15 | 30  如果公司 A 股股票连续 30 个交易日中至少有15...  已公告强赎
4    123073  同和转债  148.460  ...  25/20 | 30  如果公司A股股票连续三十个交易日中至少有二十个交易日...  已公告强赎
..      ...   ...      ...  ...         ...                            ...    ...
439  113639  华正转债  113.270  ...   0/15 | 30  如果公司股票在任何连续三十个交易日中至少十五个交易日...
440  123136  城市转债  244.200  ...   0/15 | 30  如果公司股票在任意连续三十个交易日中至少有十五个交易...
441  123137  锦浪转债  166.490  ...   0/15 | 30  如果公司股票在任意连续三十个交易日中至少十五个交易日...
442  123138  丝路转债  144.700  ...   0/15 | 30  如果公司股票在任何连续三十个交易日中至少十五个交易日...
443  113646  永吉转债  253.950  ...   0/15 | 30  公司股票在任何连续三十个交易日中至少有十五个交易日的...
```
