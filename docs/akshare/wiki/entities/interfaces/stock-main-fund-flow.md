---
title: "stock_main_fund_flow - 主力净流入排名"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_main_fund_flow

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 资金流向 > 东方财富 > 主力净流入排名
- 描述: 东方财富网-数据中心-资金流向-主力净流入排名
- 目标地址: https://data.eastmoney.com/zjlx/list.html
- 限量: 单次获取指定 symbol 的主力净流入排名数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 主力净流入排名

接口: stock_main_fund_flow

目标地址: https://data.eastmoney.com/zjlx/list.html

描述: 东方财富网-数据中心-资金流向-主力净流入排名

限量: 单次获取指定 symbol 的主力净流入排名数据

输入参数

| 名称     | 类型  | 描述                                                                                     |
|--------|-----|----------------------------------------------------------------------------------------|
| symbol | str | symbol="全部股票"；choice of {"全部股票", "沪深A股", "沪市A股", "科创板", "深市A股", "创业板", "沪市B股", "深市B股"} |

输出参数

| 名称           | 类型      | 描述      |
|--------------|---------|---------|
| 序号           | int64   | -       |
| 代码           | object  | -       |
| 名称           | object  | -       |
| 最新价          | float64 | -       |
| 今日排行榜-主力净占比  | float64 | 注意单位: % |
| 今日排行榜-今日排名   | float64 | -       |
| 今日排行榜-今日涨跌   | float64 | 注意单位: % |
| 5日排行榜-主力净占比  | float64 | 注意单位: % |
| 5日排行榜-5日排名   | int64   | -       |
| 5日排行榜-5日涨跌   | float64 | 注意单位: % |
| 10日排行榜-主力净占比 | float64 | 注意单位: % |
| 10日排行榜-10日排名 | int64   | -       |
| 10日排行榜-10日涨跌 | float64 | 注意单位: % |
| 所属板块         | object  | -       |


接口示例

```python
import akshare as ak

stock_main_fund_flow_df = ak.stock_main_fund_flow(symbol="全部股票")
print(stock_main_fund_flow_df)
```

数据示例

```
        序号  代码     名称  ...  10日排行榜-10日排名  10日排行榜-10日涨跌   所属板块
0        0  200017   深中华B  ...            10          7.77   交运设备
1        1  001366   播恩集团  ...           124         22.84   农牧饲渔
2        2  900943   开开Ｂ股  ...            27          2.88   医药商业
3        3  200771   杭汽轮Ｂ  ...           361          0.28   通用设备
4        4  002861   瀛通通讯  ...            98         23.18   消费电子
    ...     ...    ...  ...           ...           ...    ...
5198  5198  301536   星宸科技  ...          1187          0.00   电子元件
5199  5199  002089  *ST新海  ...          1180          0.00   通信设备
5200  5200  001389   广合科技  ...          1185          0.00   电子元件
5201  5201  001359   平安电工  ...          1184          0.00  非金属材料
5202  5202  000005   ST星源  ...          1179          0.00   环保行业
[5203 rows x 14 columns]
```
