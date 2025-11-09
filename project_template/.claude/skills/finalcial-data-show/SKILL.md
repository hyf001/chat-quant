---
name: final-data-show
description: 金融数据可视化
allowed-tools: Read, Grep, Glob, Bash, LS,Write,Edit,MultiEdit,WebFetch,WebSearch,TodoWrite
---

# Business Data Show Skill

## 概述

本Skill通过生成html文件，实现专业精美的金融数据可视化。

### 适用场景

用于展示金融数据查询分析结果

---

## 工作流程

1. **预览金融数据查询结果文件，结果文件一般是在`{project_path}/data_file/final/` 目录下**

2. **成结果html**
  - html存放目录：`{project_path}/dashboard/`
  - html设计原则：ECharts 图表组件、Tailwind CSS 响应式设计
```
1. Bento Grid 布局
   - 使用网格系统组织内容
   - 卡片化展示不同维度数据
   - 响应式设计适配多种屏幕

2. 视觉层级
   - 核心指标使用大字体突出显示
   - 重要图表放置在视觉焦点位置
   - 使用颜色和大小建立信息层级

3. 交互设计
   - 图表支持 hover 显示详情
   - 提供筛选和钻取功能
   - 实现平滑的动画过渡

4. 数据加载
   - 必须从结果文件动态加载数据
   - 禁止在代码中静态写死数据
   - 确保数据源的灵活性和可维护性
```
  - html样例
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>数据分析报告 - ${report_title}</title>
    <!--使用私有的静态资源-->
    <script src="https://o.thsi.cn/easyfetch-platform.summary-analysis/cdn/tailwindcss-3.4.16.js"></script>
    <script src="https://o.thsi.cn/easyfetch-platform.summary-analysis/cdn/lucide.js"></script>
	  <script src="https://o.thsi.cn/easyfetch-platform.summary-analysis/cdn/echarts.5.6.0.min.js"></script>
</head>
<body class="bg-gray-50">
    <!-- Bento Grid 容器 -->
    <div class="container mx-auto p-6">
        <!-- 标题区域 -->
        <div class="mb-8">
            <h1 class="text-4xl font-bold text-gray-900">${report_title}</h1>
            <p class="text-gray-600 mt-2">${report_description}</p>
        </div>

        <!-- 核心指标卡片 -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <!-- 指标卡片模板 -->
            <div class="bg-white rounded-xl shadow-sm p-6">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-sm text-gray-600">${metric_name}</p>
                        <p class="text-3xl font-bold text-gray-900 mt-2">${metric_value}</p>
                        <p class="text-sm ${trend_color} mt-2">
                            <span class="lucide-${trend_icon}"></span>
                            ${trend_text}
                        </p>
                    </div>
                    <div class="lucide-${metric_icon} text-blue-500 text-2xl"></div>
                </div>
            </div>
        </div>

        <!-- 图表区域 -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- 图表容器 -->
            <div class="bg-white rounded-xl shadow-sm p-6">
                <h3 class="text-lg font-semibold text-gray-900 mb-4">${chart_title}</h3>
                <div id="${chart_id}" style="height: 400px;"></div>
            </div>
        </div>
    </div>

    <script>
        //加载数据文件，path是相对路径，可能需要加载多个文件
        async function loadData(path) {
            const res = await fetch(path);
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            const data = await res.json();
            if (!data) throw new Error('数据文件为空');
            return data;
        }
        // ECharts 配置
        const chart = echarts.init(document.getElementById('${chart_id}'));
        const option = ${chart_option};
        chart.setOption(option);

        // 响应式处理
        window.addEventListener('resize', () => {
            chart.resize();
        });

    </script>
</body>
</html>
```

  - 可视化设计建议
```
1. 数据少于5个类别用饼图，多于5个用柱状图
2. 时间序列超过30个点考虑使用面积图
3. 需要展示相关性时优先使用散点图
4. 股价走势使用K线图（蜡烛图）

| 数据类型 | 推荐图表 | 使用场景 |
|---------|---------|---------|
| 时间序列 | 折线图、面积图、K线图 | 趋势分析、变化追踪 |
| 分类对比 | 柱状图、条形图 | 类别比较、排名展示 |
| 占比分布 | 饼图、环形图 | 构成分析、比例展示 |
| 相关性 | 散点图、气泡图 | 关联分析、聚类展示 |
| 地理分布 | 地图、热力图 | 区域分析、密度展示 |
| 多维度 | 雷达图、平行坐标 | 综合评估、多维对比 |
```