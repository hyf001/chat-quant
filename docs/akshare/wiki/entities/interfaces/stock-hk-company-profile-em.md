---
title: "stock_hk_company_profile_em - 公司资料"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_hk_company_profile_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 港股 > 公司资料
- 描述: 东方财富-港股-公司资料
- 目标地址: https://emweb.securities.eastmoney.com/PC_HKF10/pages/home/index.html?code=03900&type=web&color=w#/CompanyProfile
- 限量: 单次返回全部数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 公司资料

接口: stock_hk_company_profile_em

目标地址: https://emweb.securities.eastmoney.com/PC_HKF10/pages/home/index.html?code=03900&type=web&color=w#/CompanyProfile

描述: 东方财富-港股-公司资料

限量: 单次返回全部数据

输入参数

| 名称     | 类型  | 描述             |
|--------|-----|----------------|
| symbol | str | symbol="03900" |

输出参数

| 名称     | 类型     | 描述 |
|--------|--------|----|
| 公司名称   | object | -  |
| 英文名称   | object | -  |
| 注册地    | object | -  |
| 公司成立日期 | object | -  |
| 所属行业   | object | -  |
| 董事长    | object | -  |
| 公司秘书   | object | -  |
| 员工人数   | int64  | -  |
| 办公地址   | object | -  |
| 公司网址   | object | -  |
| E-MAIL | object | -  |
| 年结日    | object | -  |
| 联系电话   | object | -  |
| 核数师    | object | -  |
| 传真     | object | -  |
| 公司介绍   | object | -  |

接口示例

```python
import akshare as ak

stock_hk_company_profile_em_df = ak.stock_hk_company_profile_em(symbol="03900")
print(stock_hk_company_profile_em_df)
```

数据示例

```
         公司名称  ...                                               公司介绍
0  绿城中国控股有限公司  ...      绿城中国控股有限公司(以下简称“绿城中国”)(股票代码03900.HK),1995年...
[1 rows x 17 columns]
```
