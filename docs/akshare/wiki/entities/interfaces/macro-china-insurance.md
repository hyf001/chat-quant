---
title: "macro_china_insurance - 保险业经营情况"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_insurance

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 保险业经营情况
- 描述: 新浪财经-中国宏观经济数据-保险业经营情况
- 目标地址: http://finance.sina.com.cn/mac/#fininfo-19-0-31-3
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 保险业经营情况

接口: macro_china_insurance

目标地址: http://finance.sina.com.cn/mac/#fininfo-19-0-31-3

描述: 新浪财经-中国宏观经济数据-保险业经营情况

限量: 单次返回所有历史数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称               | 类型      | 描述       |
|------------------|---------|----------|
| 统计时间             | object  | 年月       |
| 省市地区             | object  | 地区       |
| 原保险保费收入          | float64 | 注意单位: 万元 |
| 财产险保费收入          | float64 | 注意单位: 万元 |
| 人身险保费收入          | float64 | 注意单位: 万元 |
| 人身险-寿险保费收入       | float64 | 注意单位: 万元 |
| 人身险-健康险保费收入      | float64 | 注意单位: 万元 |
| 人身险-意外险保费收入      | float64 | 注意单位: 万元 |
| 养老保险公司企业年金缴费     | float64 | 注意单位: 万元 |
| 原保险赔付支出          | float64 | 注意单位: 万元 |
| 财产险保费赔付支出        | float64 | 注意单位: 万元 |
| 人身险保费赔付支出        | float64 | 注意单位: 万元 |
| 人身险-寿险赔付支出       | float64 | 注意单位: 万元 |
| 人身险-健康险赔付支出      | float64 | 注意单位: 万元 |
| 人身险-意外险赔付支出      | float64 | 注意单位: 万元 |
| 业务及管理费           | float64 | 注意单位: 万元 |
| 银行存款             | float64 | 注意单位: 万元 |
| 投资               | float64 | 注意单位: 万元 |
| 资产总额             | float64 | 注意单位: 万元 |
| 养老保险公司企业年金受托管理资产 | float64 | 注意单位: 万元 |
| 养老保险公司企业年金投资管理资产 | float64 | 注意单位: 万元 |

接口示例

```python
import akshare as ak

macro_china_insurance_df = ak.macro_china_insurance()
print(macro_china_insurance_df)
```

数据示例

```
        统计时间 省市地区     原保险保费收入  ...  资产总额  养老保险公司企业年金受托管理资产  养老保险公司企业年金投资管理资产
0     2023.7   新疆   5361100.0  ...   NaN               NaN               NaN
1     2023.7   宁夏   1718300.0  ...   NaN               NaN               NaN
2     2023.7   青海    806100.0  ...   NaN               NaN               NaN
3     2023.7   甘肃   3886700.0  ...   NaN               NaN               NaN
4     2023.7   陕西   8311200.0  ...   NaN               NaN               NaN
..       ...  ...         ...  ...   ...               ...               ...
305  2022.11   宁夏   2020200.0  ...   NaN               NaN               NaN
306  2022.11   青海    978500.0  ...   NaN               NaN               NaN
307  2022.11   甘肃   4591900.0  ...   NaN               NaN               NaN
308  2022.11   陕西  10225900.0  ...   NaN               NaN               NaN
309  2022.11   西藏    370100.0  ...   NaN               NaN               NaN
[310 rows x 21 columns]
```
