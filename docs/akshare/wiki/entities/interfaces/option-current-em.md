---
title: "option_current_em - 期权实时行情-东方财富"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, option, parameters, returns, example]
sources: [raw/data-dictionary/option/option.md]
confidence: high
---
# option_current_em

- 分类: [[option-option|AKShare 期权数据]]
- 主题路径: AKShare 期权数据 > 期权实时行情-东方财富
- 描述: 东方财富网-行情中心-期权市场
- 目标地址: https://quote.eastmoney.com/center/qqsc.html
- 限量: 单次返回全部合约的实时行情
- 来源页面: https://akshare.akfamily.xyz/data/option/option.html

## 相关

- [[option-option|AKShare 期权数据]]
- [[_meta/topic-map]]

## 源文摘录

### 期权实时行情-东方财富

接口: option_current_em

目标地址: https://quote.eastmoney.com/center/qqsc.html

描述: 东方财富网-行情中心-期权市场

限量: 单次返回全部合约的实时行情

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称   | 类型      | 描述      |
|------|---------|---------|
| 代码   | object  | -       |
| 名称   | object  | -       |
| 最新价  | float64 | -       |
| 涨跌额  | float64 | -       |
| 涨跌幅  | float64 | 注意单位: % |
| 成交量  | float64 | -       |
| 成交额  | float64 | -       |
| 持仓量  | float64 | -       |
| 行权价  | float64 | -       |
| 剩余日  | float64 | -       |
| 日增   | float64 | -       |
| 昨结   | float64 | -       |
| 今开   | float64 | -       |
| 市场标识 | int64   | -       |

接口示例

```python
import akshare as ak

option_current_em_df = ak.option_current_em()
print(option_current_em_df)
```

数据示例

```
          序号     代码                名称   最新价  ...      日增    昨结    今开  市场标识
0          1    pg2406p3500     LPG24年06月沽3500  19.0  ...    16.0   0.2   9.8   140
1          2     b2406c4500      豆二24年06月购4500  40.5  ...     1.0   0.5  40.5   140
2          3    pg2406p3600     LPG24年06月沽3600  11.8  ...     0.0   0.2  11.8   140
3          4    pg2406p3550     LPG24年06月沽3550   9.6  ...     0.0   0.2   9.6   140
4          5    pg2403p3800     LPG24年03月沽3800   9.2  ...   511.0   0.2   1.2   140
      ...            ...                ...   ...  ...     ...   ...   ...   ...
16835  16836  MO2402-C-5500  中证1000购24年02月5500   5.8  ...   381.0  11.4  10.0   221
16836  16837  MO2402-C-5100  中证1000购24年02月5100  38.2  ...   982.0  75.6  71.0   221
16837  16838  MO2402-C-5200  中证1000购24年02月5200  24.6  ...  1606.0  50.0  45.2   221
16838  16839  MO2402-C-5600  中证1000购24年02月5600   3.2  ...   448.0   6.6   6.6   221
16839  16840  MO2402-C-5400  中证1000购24年02月5400   9.2  ...    32.0  19.0  16.4   221
[16840 rows x 15 columns]
```
