---
title: "index_detail_hist_adjust_cni - 历史调样"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# index_detail_hist_adjust_cni

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 国证指数 > 历史调样
- 描述: 国证指数-样本详情-历史调样
- 目标地址: http://www.cnindex.com.cn/module/index-detail.html?act_menu=1&indexCode=399001
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 历史调样

接口: index_detail_hist_adjust_cni

目标地址: http://www.cnindex.com.cn/module/index-detail.html?act_menu=1&indexCode=399001

描述: 国证指数-样本详情-历史调样

输入参数

| 名称     | 类型  | 描述                                                 |
|--------|-----|----------------------------------------------------|
| symbol | str | symbol='399005'; 从 **ak.index_all_cni()** 接口获取指数代码 |

输出参数

| 名称   | 类型     | 描述  |
|------|--------|-----|
| 开始日期 | object | -   |
| 结束日期 | object | -   |
| 样本代码 | object | -   |
| 样本简称 | object | -   |
| 所属行业 | object | -   |
| 调整类型 | object | -   |

接口示例

```python
import akshare as ak

index_detail_hist_adjust_cni_df = ak.index_detail_hist_adjust_cni(symbol='399005')
print(index_detail_hist_adjust_cni_df)
```

数据示例

```
      开始日期        结束日期  样本代码  样本简称 所属行业 调整类型
0     2024-06-17  2024-12-13  002001  新 和 成  医药卫生  OLD
1     2024-06-17  2024-12-13  002007   华兰生物  医药卫生  OLD
2     2024-06-17  2024-12-13  002008   大族激光  信息技术  OLD
3     2024-06-17  2024-12-13  002025   航天电器  信息技术  OLD
4     2024-06-17  2024-12-13  002027   分众传媒  可选消费  OLD
...          ...         ...     ...    ...   ...  ...
1185  2019-12-16  2020-06-12  002926   华西证券    金融  OLD
1186  2019-12-16  2020-06-12  002938   鹏鼎控股  信息技术  OLD
1187  2019-12-16  2020-06-12  002939   长城证券    金融  OLD
1188  2019-12-16  2020-06-12  002958   青农商行    金融    +
1189  2019-12-16  2020-06-12  003816   中国广核  公用事业  OLD
[1190 rows x 6 columns]
```
