---
title: "fund_rating_ja - 济安金信评级"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_rating_ja

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金评级 > 济安金信评级
- 描述: 天天基金网-基金评级-济安金信评级
- 目标地址: https://fund.eastmoney.com/data/fundrating_4.html
- 限量: 单次返回指定交易日的所有基金评级数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 济安金信评级

接口: fund_rating_ja

目标地址: https://fund.eastmoney.com/data/fundrating_4.html

描述: 天天基金网-基金评级-济安金信评级

限量: 单次返回指定交易日的所有基金评级数据

输入参数

| 名称   | 类型  | 描述                                                                        |
|------|-----|---------------------------------------------------------------------------|
| date | str | date='20200930'; https://fund.eastmoney.com/data/fundrating_4.html 获取查询日期 |

输出参数

| 名称         | 类型      | 描述      |
|------------|---------|---------|
| 代码         | object  | -       |
| 简称         | object  | -       |
| 基金经理       | object  | -       |
| 基金公司       | object  | -       |
| 3年期评级-3年评级 | int64   | -       |
| 3年期评级-较上期  | float64 | -       |
| 单位净值       | float64 | -       |
| 日期         | object  | -       |
| 日增长率       | float64 | 注意单位: % |
| 近1年涨幅      | float64 | 注意单位: % |
| 近3年涨幅      | float64 | 注意单位: % |
| 近5年涨幅      | float64 | 注意单位: % |
| 手续费        | object  | -       |
| 类型         | object  | -       |

接口示例

```python
import akshare as ak

fund_rating_ja_df = ak.fund_rating_ja(date='20200930')
print(fund_rating_ja_df)
```

数据示例

```
          代码           简称     基金经理    基金公司  ...  近3年涨幅  近5年涨幅    手续费   类型
0     000005   嘉实增强信用定期债券       轩璇    嘉实基金  ...  10.34  25.83  0.08%  纯债型
1     000010   易方达天天理财货币B  石大怿,刘朝阳   易方达基金  ...   6.83  13.06  0.00%  货币型
2     000006  西部利得量化成长混合A      盛丰衍  西部利得基金  ...  46.57    NaN  0.15%  混合型
3     000011    华夏大盘精选混合A      陈伟彦    华夏基金  ...  12.92  48.80  0.15%  混合型
4     000009   易方达天天理财货币A  石大怿,刘朝阳   易方达基金  ...   6.06  11.71  0.00%  货币型
      ...          ...      ...     ...  ...    ...    ...    ...  ...
7718  690005   民生加银内需增长混合      柳世庆  民生加银基金  ...  -6.02  66.62  0.15%  混合型
7719  690010  民生加银现金增利货币A   张玓,郑雅洁  民生加银基金  ...   5.49  10.74  0.00%  货币型
7720  690009   民生加银红利回报混合   王亮,邓凯成  民生加银基金  ...  -0.87  37.61  0.15%  混合型
7721  690210  民生加银现金增利货币B   张玓,郑雅洁  民生加银基金  ...   6.25  12.09  0.00%  货币型
7722  690202    民生增强收益债券C      谢志华  民生加银基金  ...   0.41  24.72  0.00%  二级债
[7723 rows x 14 columns]
```
