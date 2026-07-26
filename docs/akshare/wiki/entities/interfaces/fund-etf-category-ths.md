---
title: "fund_etf_category_ths - 基金实时行情-同花顺"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_etf_category_ths

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金行情 > 基金实时行情-同花顺
- 描述: 同花顺理财-基金数据-每日净值-实时行情
- 目标地址: https://fund.10jqka.com.cn/datacenter/jz/kfs/etf/
- 限量: 单次返回指定 date 和 symbol 的所有数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 基金实时行情-同花顺

接口: fund_etf_category_ths

目标地址: https://fund.10jqka.com.cn/datacenter/jz/kfs/etf/

描述: 同花顺理财-基金数据-每日净值-实时行情

限量: 单次返回指定 date 和 symbol 的所有数据

输入参数

| 名称     | 类型  | 描述                                                                                             |
|--------|-----|------------------------------------------------------------------------------------------------|
| symbol | str | symbol="ETF"; choice of {"股票型", "债券型", "混合型", "ETF", "LOF", "QDII", "保本型", "指数型", ""}; "" 表示全部 |
| date   | str | date=""; 默认返回当前最新的数据                                                                           |

输出参数

| 名称       | 类型      | 描述      |
|----------|---------|---------|
| 序号       | int64   | -       |
| 基金代码     | object  | -       |
| 基金名称     | object  | -       |
| 当前-单位净值  | float64 | -       |
| 当前-累计净值  | float64 | -       |
| 前一日-单位净值 | float64 | -       |
| 前一日-累计净值 | float64 |         |
| 增长值      | float64 | -       |
| 增长率      | float64 | 注意单位: % |
| 赎回状态     | object  | -       |
| 申购状态     | object  | -       |
| 最新-交易日   | object  | -       |
| 最新-单位净值  | float64 | -       |
| 最新-累计净值  | float64 | -       |
| 基金类型     | object  | -       |
| 查询日期     | object  | -       |

接口示例

```python
import akshare as ak

fund_etf_category_ths_df = ak.fund_etf_category_ths(symbol="ETF", date="20240620")
print(fund_etf_category_ths_df)
```

数据示例

```
      序号    基金代码         基金名称  ...  最新-累计净值  基金类型    查询日期
0      1  159691            高股息ETF港股  ...   1.2039   股票型  2024-06-20
1      2  588200        嘉实上证科创板芯片ETF  ...   1.0000   股票型  2024-06-20
2      3  588290        华安上证科创板芯片ETF  ...   0.9775   股票型  2024-06-20
3      4  588890        南方上证科创板芯片ETF  ...   1.1194   股票型  2024-06-20
4      5  513530                港股红利  ...   1.3692   股票型  2024-06-20
..   ...     ...                 ...  ...      ...   ...         ...
979  980  560360         万家中证软件服务ETF  ...   1.0000   股票型  2024-06-20
980  981  588500  易方达上证科创板100增强策略ETF  ...      NaN   股票型  2024-06-20
981  982  588680   广发上证科创板100增强策略ETF  ...      NaN   股票型  2024-06-20
982  983  588860             科创医药ETF  ...      NaN   股票型  2024-06-20
983  984  588990        博时上证科创板芯片ETF  ...      NaN   股票型  2024-06-20
[984 rows x 16 columns]
```
