---
title: "macro_china_postal_telecommunicational - 邮电业务基本情况"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_postal_telecommunicational

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 邮电业务基本情况
- 描述: 国家统计局-邮电业务基本情况-非累计
- 目标地址: http://finance.sina.com.cn/mac/#industry-11-0-31-1
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 邮电业务基本情况

接口: macro_china_postal_telecommunicational

目标地址: http://finance.sina.com.cn/mac/#industry-11-0-31-1

描述: 国家统计局-邮电业务基本情况-非累计

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称            | 类型    | 描述       |
|---------------|-------|----------|
| 统计时间          | str   | 年月       |
| 邮电业务总量        | float | 注意单位: 亿元 |
| 邮电业务总量同比增长    | float | 注意单位: %  |
| 邮政业务总量        | float | 注意单位: 亿元 |
| 邮政业务总量同比增长    | float | 注意单位: %  |
| 电信业务总量        | float | 注意单位: 亿元 |
| 电信业务总量同比增长    | float | 注意单位: %  |
| 函件总数          | float | 注意单位: 万件 |
| 函件总数同比增长      | float | 注意单位: %  |
| 包件            | float | 注意单位: 万件 |
| 包件同比增长        | float | 注意单位: %  |
| 特快专递          | float | 注意单位: 万件 |
| 特快专递同比增长      | float | 注意单位: %  |
| 汇票            | float | 注意单位: 万张 |
| 汇票同比增长        | float | 注意单位: %  |
| 订销报纸累计数       | float | 注意单位: 万份 |
| 订销报纸累计数同比增长   | float | 注意单位: %  |
| 订销杂志累计数       | float | 注意单位: 万份 |
| 订销杂志累计数同比增长   | float | 注意单位: %  |
| 集邮业务          | float | 注意单位: 万枚 |
| 集邮业务同比增长      | float | 注意单位: %  |
| 邮政储蓄期末余额      | float | 注意单位: 亿元 |
| 邮政储蓄期末余额同比增长  | float | 注意单位: %  |
| 长途电话通话时长      | float | 注意单位: 万  |
| 钟长途电话通话时长同比增长 | float | 注意单位: %  |
| 本地电话期末用户数     | float | 注意单位: %  |
| 本地电话期末用户数同比增长 | float | 注意单位: %  |
| 城市电话用户数       | float | 注意单位: 万户 |
| 城市电话用户数同比增长   | float | 注意单位: %  |
| 乡村电话用户数       | float | 注意单位: 万户 |
| 乡村电话用户数同比增长   | float | 注意单位: %  |
| 无线寻呼用户数       | float | 注意单位: 万户 |
| 无线寻呼用户数同比增长   | float | 注意单位: %  |
| 移动电话用户数       | float | 注意单位: 万户 |
| 移动电话用户数同比增长   | float | 注意单位: %  |
| 固定电话用         | float | 注意单位: 万户 |
| 固定电话用户数同比增长   | float | 注意单位: %  |
| 城市住宅电话用户      | float | 注意单位: 万户 |
| 城市住宅电话用户同比增长  | float | 注意单位: %  |
| 乡村住宅电话用户      | float | 注意单位: 万户 |
| 乡村住宅电话用户同比增长  | float | 注意单位: %  |

接口示例

```python
import akshare as ak

macro_china_postal_telecommunicational_df = ak.macro_china_postal_telecommunicational()
print(macro_china_postal_telecommunicational_df)
```

数据示例

```
        统计时间  邮电业务总量  邮电业务总量同比增长  ...  城市住宅电话用户同比增长  乡村住宅电话用户  乡村住宅电话用户同比增长
0     2023.7     NaN         NaN  ...           NaN       NaN           NaN
1     2023.6     NaN         NaN  ...           NaN       NaN           NaN
2     2023.5     NaN         NaN  ...           NaN       NaN           NaN
3     2023.4     NaN         NaN  ...           NaN       NaN           NaN
4     2023.3     NaN         NaN  ...           NaN       NaN           NaN
..       ...     ...         ...  ...           ...       ...           ...
299  1970.12     NaN         NaN  ...           NaN       NaN           NaN
300  1965.12     NaN         NaN  ...           NaN       NaN           NaN
301  1962.12     NaN         NaN  ...           NaN       NaN           NaN
302  1957.12     NaN         NaN  ...           NaN       NaN           NaN
303  1952.12     NaN         NaN  ...           NaN       NaN           NaN
[304 rows x 41 columns]
```
