---
title: "index_detail_cni - 指数样本详情"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# index_detail_cni

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 国证指数 > 指数样本详情
- 描述: 国证指数-指数样本详情数据；20251125 开始只能获取近期的数据
- 目标地址: http://www.cnindex.com.cn/module/index-detail.html?act_menu=1&indexCode=399001
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 指数样本详情

接口: index_detail_cni

目标地址: http://www.cnindex.com.cn/module/index-detail.html?act_menu=1&indexCode=399001

描述: 国证指数-指数样本详情数据；20251125 开始只能获取近期的数据

输入参数

| 名称     | 类型  | 描述                                                 |
|--------|-----|----------------------------------------------------|
| symbol | str | symbol='399001'; 从 **ak.index_all_cni()** 接口获取指数代码 |

输出参数

| 名称     | 类型      | 描述       |
|--------|---------|----------|
| 日期     | object  | -        |
| 样本代码   | object  | -        |
| 样本简称   | object  | -        |
| 所属行业   | object  | -        |
| 自由流通市值 | float64 | 注意单位: 亿元 |
| 总市值    | float64 | 注意单位: 亿元 |
| 权重     | float64 | 注意单位: %  |

接口示例

```python
import akshare as ak

index_detail_cni_df = ak.index_detail_cni(symbol='399001')
print(index_detail_cni_df)
```

数据示例

```
               日期    样本代码   样本简称  所属行业      总市值    权重
0      2025-11-28  000001   平安银行    金融  2253.03  0.67
1      2025-11-28  000002  万  科Ａ   房地产   523.16  0.25
2      2025-11-28  000009   中国宝安    工业   261.02  0.12
3      2025-11-28  000021    深科技  信息技术   375.94  0.17
4      2025-11-28  000027   深圳能源  公用事业   316.84  0.06
...           ...     ...    ...   ...      ...   ...
30495  2020-11-30  300773    拉卡拉    金融   266.81  0.12
30496  2020-11-30  300775   三角防务    工业   170.01  0.09
30497  2020-11-30  300777   中简科技   原材料   183.40  0.07
30498  2020-11-30  300782    卓胜微  信息技术  1013.40  0.25
30499  2020-11-30  300783   三只松鼠  主要消费   212.97  0.02
[30500 rows x 6 columns]
```
