---
title: "stock_zh_growth_comparison_em - 成长性比较"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_zh_growth_comparison_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 同行比较 > 成长性比较
- 描述: 东方财富-行情中心-同行比较-成长性比较
- 目标地址: https://emweb.securities.eastmoney.com/pc_hsf10/pages/index.html?type=web&code=000895&color=b#/thbj/czxbj
- 限量: 单次返回全部数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 成长性比较

接口: stock_zh_growth_comparison_em

目标地址: https://emweb.securities.eastmoney.com/pc_hsf10/pages/index.html?type=web&code=000895&color=b#/thbj/czxbj

描述: 东方财富-行情中心-同行比较-成长性比较

限量: 单次返回全部数据

输入参数

| 名称         | 类型  | 描述                    |
|------------|-----|-----------------------|
| symbol     | str | symbol="SZ000895"     |

输出参数

| 名称               | 类型      | 描述 |
|------------------|---------|----|
| 代码               | object  | -  |
| 简称               | object  | -  |
| 基本每股收益增长率-3年复合   | float64 | -  |
| 基本每股收益增长率-24A    | float64 | -  |
| 基本每股收益增长率-TTM    | float64 | -  |
| 基本每股收益增长率-25E    | float64 | -  |
| 基本每股收益增长率-26E    | float64 | -  |
| 基本每股收益增长率-27E    | float64 | -  |
| 营业收入增长率-3年复合     | float64 | -  |
| 营业收入增长率-24A      | float64 | -  |
| 营业收入增长率-TTM      | float64 | -  |
| 营业收入增长率-25E      | float64 | -  |
| 营业收入增长率-26E      | float64 | -  |
| 营业收入增长率-27E      | float64 | -  |
| 净利润增长率-3年复合      | float64 | -  |
| 净利润增长率-24A       | float64 | -  |
| 净利润增长率-TTM       | float64 | -  |
| 净利润增长率-25E       | float64 | -  |
| 净利润增长率-26E       | float64 | -  |
| 净利润增长率-27E       | float64 | -  |
| 基本每股收益增长率-3年复合排名 | float64 | -  |

接口示例

```python
import akshare as ak

stock_zh_growth_comparison_em_df = ak.stock_zh_growth_comparison_em(symbol="SZ000895")
print(stock_zh_growth_comparison_em_df)
```

数据示例

```
       代码    简称  基本每股收益增长率-3年复合  ...  净利润增长率-26E  净利润增长率-27E  基本每股收益增长率-3年复合排名
0    行业中值  行业中值       -8.790000  ...   21.290000   16.135000               NaN
1    行业平均  行业平均      -31.127395  ...   57.622875   18.847125               NaN
2  600530  交大昂立       81.710000  ...         NaN         NaN               1.0
3  600186  莲花控股       58.740000  ...   28.700000   22.480000               2.0
4  600962  国投中鲁       51.860000  ...         NaN         NaN               3.0
5  600737  中粮糖业       48.850000  ...   39.030000   22.690000               4.0
6  003000  劲仔食品       46.100000  ...   22.070000   17.520000               5.0
7  000895  双汇发展        0.840000  ...    4.320000    3.980000              38.0
[8 rows x 21 columns]
```
