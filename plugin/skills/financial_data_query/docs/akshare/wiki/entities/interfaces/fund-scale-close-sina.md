---
title: "fund_scale_close_sina - 封闭式基金"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_scale_close_sina

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金规模 > 封闭式基金
- 描述: 基金数据中心-基金规模-封闭式基金
- 目标地址: https://vip.stock.finance.sina.com.cn/fund_center/index.html#jjhqetf
- 限量: 单次返回所有封闭式基金的基金规模数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 封闭式基金

接口: fund_scale_close_sina

目标地址: https://vip.stock.finance.sina.com.cn/fund_center/index.html#jjhqetf

描述: 基金数据中心-基金规模-封闭式基金

限量: 单次返回所有封闭式基金的基金规模数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称    | 类型      | 描述       |
|-------|---------|----------|
| 序号    | int64   | -        |
| 基金代码  | object  | -        |
| 基金简称  | object  | -        |
| 单位净值  | float64 | 注意单位: 元  |
| 总募集规模 | float64 | 注意单位: 万份 |
| 最近总份额 | float64 | 注意单位: 份  |
| 成立日期  | object  | -        |
| 基金经理  | object  | -        |
| 更新日期  | object  | -        |

接口示例

```python
import akshare as ak

fund_scale_close_sina_df = ak.fund_scale_close_sina()
print(fund_scale_close_sina_df)
```

数据示例

```
      序号    基金代码            基金简称  ...        成立日期  基金经理        更新日期
0      1  017800     招商恒鑫30个月封闭债  ...  2023-02-22   李家辉  2023-10-16
1      2  001369    兴业稳固收益两年理财债券  ...  2015-06-10   唐丁祥  2023-11-06
2      3  017798  易方达恒固18个月封闭债券A  ...  2023-03-06   纪玲云  2023-10-16
3      4  017792      工银泰丰一年封闭债券  ...  2023-03-21   张略钊         NaT
4      5  163418    兴全合兴混合(LOF)A  ...  2021-01-12    陈宇  2023-11-06
..   ...     ...             ...  ...         ...   ...         ...
135  136  165809       东吴中证可转债指数  ...  2014-05-09    邵笛         NaN
136  137  519059      海富通可转债优选债券  ...  2014-05-06    何谦         NaN
137  138  000631        中银聚利分级债券  ...  2014-06-05    陈玮         NaN
138  139  005863    华夏鼎禄三个月定开债券C  ...  2018-10-11    孙蕾         NaN
139  140  006394  招商添德3个月定开债发起式C  ...  2018-09-12   黄晓婷         NaN
[140 rows x 9 columns]
```
