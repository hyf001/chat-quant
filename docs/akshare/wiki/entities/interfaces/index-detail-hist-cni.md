---
title: "index_detail_hist_cni - 历史样本"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# index_detail_hist_cni

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 国证指数 > 历史样本
- 描述: 国证指数-历史样本数据，返回所有历史数据
- 目标地址: http://www.cnindex.com.cn/module/index-detail.html?act_menu=1&indexCode=399001
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 历史样本

接口: index_detail_hist_cni

目标地址: http://www.cnindex.com.cn/module/index-detail.html?act_menu=1&indexCode=399001

描述: 国证指数-历史样本数据，返回所有历史数据

输入参数

| 名称     | 类型  | 描述                                                           |
|--------|-----|--------------------------------------------------------------|
| symbol | str | symbol='399005'; 从 **ak.index_all_cni()** 接口获取指数代码           |

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

index_detail_hist_cni_df = ak.index_detail_hist_cni(symbol='399005')
print(index_detail_hist_cni_df)
```

数据示例

```
      日期    样本代码   样本简称  所属行业      总市值    权重
0      2025-12-31  000001   平安银行    金融  2214.22  0.62
1      2025-12-31  000002  万  科Ａ   房地产   452.18  0.20
2      2025-12-31  000009   中国宝安    工业   254.05  0.11
3      2025-12-31  000021    深科技  信息技术   397.84  0.17
4      2025-12-31  000027   深圳能源  公用事业   310.18  0.05
...           ...     ...    ...   ...      ...   ...
30495  2020-12-31  300782    卓胜微  信息技术  1026.97  0.46
30496  2020-12-31  300783   三只松鼠  主要消费   164.77  0.03
30497  2020-12-31  300803    指南针  信息技术   132.03  0.06
30498  2020-12-31  300815    玉禾田    工业   128.57  0.03
30499  2020-12-31  300999    金龙鱼  主要消费  5872.67  0.34
[30500 rows x 6 columns]
```
