---
title: "bond_china_yield - 国债及其他债券收益率曲线"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, bond, parameters, returns, example]
sources: [raw/data-dictionary/bond/bond.md]
confidence: high
---
# bond_china_yield

- 分类: [[bond-bond|AKShare 债券数据]]
- 主题路径: AKShare 债券数据 > 中国债券市场行情数据 > 国债及其他债券收益率曲线
- 描述: 中国债券信息网-国债及其他债券收益率曲线
- 目标地址: https://yield.chinabond.com.cn/cbweb-pbc-web/pbc/historyQuery?startDate=2019-02-07&endDate=2020-02-04&gjqx=0&qxId=ycqx&locale=cn_ZH
- 限量: 单次返回所有指定日期间 start_date 到 end_date 需要小于一年的所有数据
- 来源页面: https://akshare.akfamily.xyz/data/bond/bond.html

## 相关

- [[bond-bond|AKShare 债券数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 国债及其他债券收益率曲线

接口: bond_china_yield

目标地址: https://yield.chinabond.com.cn/cbweb-pbc-web/pbc/historyQuery?startDate=2019-02-07&endDate=2020-02-04&gjqx=0&qxId=ycqx&locale=cn_ZH

描述: 中国债券信息网-国债及其他债券收益率曲线

限量: 单次返回所有指定日期间 start_date 到 end_date 需要小于一年的所有数据

输入参数

| 名称         | 类型  | 描述                                                          |
|------------|-----|-------------------------------------------------------------|
| start_date | str | start_date="20190204", 指定开始日期; start_date 到 end_date 需要小于一年 |
| end_date   | str | end_date="20200204", 指定结束日期; start_date 到 end_date 需要小于一年   |

输出参数

| 名称   | 类型      | 描述  |
|------|---------|-----|
| 曲线名称 | object  |     |
| 日期   | object  |     |
| 3月   | float64 |     |
| 6月   | float64 |     |
| 1年   | float64 |     |
| 3年   | float64 |     |
| 5年   | float64 |     |
| 7年   | float64 |     |
| 10年  | float64 |     |
| 30年  | float64 |     |

接口示例

```python
import akshare as ak

bond_china_yield_df = ak.bond_china_yield(start_date="20210201", end_date="20220201")
print(bond_china_yield_df)
```

数据示例

```
                    曲线名称          日期      3月  ...      7年     10年     30年
0      中债中短期票据收益率曲线(AAA)  2021-02-01  3.2000  ...  3.9929  4.1465     NaN
1    中债商业银行普通债收益率曲线(AAA)  2021-02-01  3.1085  ...  3.8172  3.9554  4.5813
2              中债国债收益率曲线  2021-02-01  2.4501  ...  3.1725  3.1712  3.7342
3              中债国债收益率曲线  2021-02-02  2.4001  ...  3.1829  3.1862  3.7415
4      中债中短期票据收益率曲线(AAA)  2021-02-02  3.0242  ...  3.9707  4.1243     NaN
..                   ...         ...     ...  ...     ...     ...     ...
748  中债商业银行普通债收益率曲线(AAA)  2022-01-29  2.3008  ...  3.3258  3.4677  3.8345
749            中债国债收益率曲线  2022-01-29  1.7876  ...  2.6521  2.7013  3.2750
750    中债中短期票据收益率曲线(AAA)  2022-01-30  2.4486  ...  3.4477  3.6091     NaN
751  中债商业银行普通债收益率曲线(AAA)  2022-01-30  2.2908  ...  3.3122  3.4541  3.8209
752            中债国债收益率曲线  2022-01-30  1.7756  ...  2.6555  2.6997  3.2718
[753 rows x 10 columns]
```
