---
name: financial-data-query
description: 金融数据查询
allowed-tools: Read, Grep, Glob, Bash, LS,Write,Edit,MultiEdit,WebFetch,WebSearch,TodoWrite
---

# financial Data query Skill

## 概述

本Skill基于akshare查询金融数据，并提供基于python代码做数据分析的能力

### 适用场景

当查询分析金融数据包括股票、基金、期货等数据时，可以使用本工具。

---

## 工作流程

1. **检索akshare api文档**
在`{project_path}/reference/apis/akshare/`目录下检索可能会用到的api
2. **阅读akshare api文档**
3. **编写python代码**
编写python代码处理用户需求，代码主要逻辑如下：
 - 调用akshare api获取数据
 - 数据清洗：去除空值、异常值
 - 数据转换：类型转换、格式统
 - 特征工程：计算衍生指标
 - 数据聚合：按维度聚合统计
 - 处理好的数据保存成文件到 
 
 最终的文件保存到`{project_path}/data_file/final/`目录下，过程文件保存在`{project_path}/data_file/intermediate/`目录下

4. **执行python代码**

## 环境和限制
1. python版本 3.12
2. 已经安装好的包及其版本
    akshare                   1.17.76
    numpy                     2.3.4
    pandas                    2.3.3
    TA-lib                    0.6.8
3. 使用已有的包，不要去下载新的包
4. 绝对禁止没有数据伪造数据

