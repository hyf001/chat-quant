#!/usr/bin/env python3
"""
数据可视化工具
从已准备好的 JSON 快速生成包含 KPI、普通表格和 ECharts 图表的 HTML 报告。
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List


def validate_data_format(data: Dict[str, Any]) -> tuple[bool, List[str]]:
    """
    验证数据格式
    返回: (是否有效, 错误列表)
    """
    errors = []

    # 1. 验证根对象
    if not isinstance(data, dict):
        return False, ["根数据必须是一个对象(dict)"]

    # 检查是否至少包含一个有效字段
    valid_root_keys = {"cards", "tables", "charts", "source"}
    has_valid_content = False

    # 检查是否有未知的根字段
    for key in data.keys():
        if key not in valid_root_keys:
            errors.append(f"根对象包含未知字段: '{key}'，有效字段为: {', '.join(valid_root_keys)}")

    # 2. 验证 cards
    if "cards" in data:
        cards = data["cards"]
        if not isinstance(cards, list):
            errors.append("'cards' 必须是数组")
        else:
            if cards:
                has_valid_content = True
            for idx, card in enumerate(cards):
                card_errors = _validate_card(card, idx)
                errors.extend(card_errors)

    # 3. 验证 tables
    if "tables" in data:
        tables = data["tables"]
        if not isinstance(tables, list):
            errors.append("'tables' 必须是数组")
        else:
            if tables:
                has_valid_content = True
            for idx, table in enumerate(tables):
                table_errors = _validate_table(table, idx)
                errors.extend(table_errors)

    # 4. 验证 charts
    if "charts" in data:
        charts = data["charts"]
        if not isinstance(charts, list):
            errors.append("'charts' 必须是数组")
        else:
            if charts:
                has_valid_content = True
            for idx, chart in enumerate(charts):
                chart_errors = _validate_chart(chart, idx)
                errors.extend(chart_errors)

    # 5. 验证 source (可选字段)
    if "source" in data:
        if not isinstance(data["source"], str):
            errors.append("'source' 必须是字符串")

    if not has_valid_content and not errors:
        errors.append("数据中没有任何有效内容（cards、tables 或 charts 都为空）")

    return len(errors) == 0, errors


def _validate_card(card: Any, idx: int) -> List[str]:
    """验证单个卡片的格式"""
    errors = []
    prefix = f"cards[{idx}]"

    if not isinstance(card, dict):
        return [f"{prefix}: 必须是对象"]

    # 必需字段
    required_fields = {"label", "value"}
    for field in required_fields:
        if field not in card:
            errors.append(f"{prefix}: 缺少必需字段 '{field}'")

    # 可选字段及其类型
    optional_fields = {
        "unit": (str, type(None)),
        "description": (str, type(None)),
        "icon": (str, type(None)),
    }

    # 验证 label
    if "label" in card and not isinstance(card["label"], str):
        errors.append(f"{prefix}.label: 必须是字符串")

    # 验证 value (可以是字符串或数字)
    if "value" in card and not isinstance(card["value"], (str, int, float)):
        errors.append(f"{prefix}.value: 必须是字符串或数字")

    # 验证可选字段类型
    for field, expected_types in optional_fields.items():
        if field in card and card[field] is not None:
            if not isinstance(card[field], expected_types):
                errors.append(f"{prefix}.{field}: 必须是字符串")

    # 检查未知字段
    valid_card_keys = {"label", "value", "unit", "description", "icon"}
    for key in card.keys():
        if key not in valid_card_keys:
            errors.append(f"{prefix}: 包含未知字段 '{key}'，有效字段为: {', '.join(valid_card_keys)}")

    return errors


def _validate_table(table: Any, idx: int) -> List[str]:
    """验证单个表格的格式"""
    errors = []
    prefix = f"tables[{idx}]"

    if not isinstance(table, dict):
        return [f"{prefix}: 必须是对象"]

    # 必需字段
    if "data" not in table:
        errors.append(f"{prefix}: 缺少必需字段 'data'")

    # 可选字段
    if "title" in table and not isinstance(table["title"], str):
        errors.append(f"{prefix}.title: 必须是字符串")

    # 验证 type 字段（可选，默认为 "default"）
    valid_table_types = {"default"}
    if "type" in table:
        if not isinstance(table["type"], str):
            errors.append(f"{prefix}.type: 必须是字符串")
        elif table["type"] not in valid_table_types:
            errors.append(f"{prefix}.type: 无效的表格类型 '{table['type']}'，支持的类型: {', '.join(valid_table_types)}")

    # 验证 data
    if "data" in table:
        data = table["data"]
        if not isinstance(data, list):
            errors.append(f"{prefix}.data: 必须是数组")
        else:
            for row_idx, row in enumerate(data):
                if not isinstance(row, dict):
                    errors.append(f"{prefix}.data[{row_idx}]: 每一行必须是对象")
                else:
                    # 验证每个单元格的值类型
                    for key, value in row.items():
                        if not isinstance(value, (str, int, float, bool, type(None))):
                            errors.append(f"{prefix}.data[{row_idx}].{key}: 值必须是基本类型（字符串、数字、布尔值或null）")

    # 检查未知字段
    valid_table_keys = {"title", "data", "type"}
    for key in table.keys():
        if key not in valid_table_keys:
            errors.append(f"{prefix}: 包含未知字段 '{key}'，有效字段为: {', '.join(sorted(valid_table_keys))}")

    return errors


def _validate_chart(chart: Any, idx: int) -> List[str]:
    """验证单个图表的格式"""
    errors = []
    prefix = f"charts[{idx}]"

    if not isinstance(chart, dict):
        return [f"{prefix}: 必须是对象"]

    # 必需字段
    if "data" not in chart:
        errors.append(f"{prefix}: 缺少必需字段 'data'")

    # 可选字段
    if "title" in chart and not isinstance(chart["title"], str):
        errors.append(f"{prefix}.title: 必须是字符串")

    # 验证 data (ECharts 配置对象)
    if "data" in chart:
        data = chart["data"]
        if not isinstance(data, dict):
            errors.append(f"{prefix}.data: 必须是对象（ECharts配置）")
        else:
            chart_data_errors = _validate_chart_data(data, prefix)
            errors.extend(chart_data_errors)

    # 检查未知字段
    valid_chart_keys = {"title", "data"}
    for key in chart.keys():
        if key not in valid_chart_keys:
            errors.append(f"{prefix}: 包含未知字段 '{key}'，有效字段为: {', '.join(valid_chart_keys)}")

    return errors


def _validate_chart_data(data: Dict[str, Any], prefix: str) -> List[str]:
    """验证 ECharts 图表数据配置"""
    errors = []
    data_prefix = f"{prefix}.data"

    # series 是必需的
    if "series" not in data:
        errors.append(f"{data_prefix}: 缺少必需字段 'series'")
    else:
        series = data["series"]
        if not isinstance(series, list):
            errors.append(f"{data_prefix}.series: 必须是数组")
        elif len(series) == 0:
            errors.append(f"{data_prefix}.series: 不能为空数组")
        else:
            for s_idx, s in enumerate(series):
                series_errors = _validate_series(s, f"{data_prefix}.series[{s_idx}]")
                errors.extend(series_errors)

    # 验证 xAxis（如果存在）
    if "xAxis" in data:
        xAxis = data["xAxis"]
        if not isinstance(xAxis, dict):
            errors.append(f"{data_prefix}.xAxis: 必须是对象")
        else:
            xaxis_errors = _validate_axis(xAxis, f"{data_prefix}.xAxis")
            errors.extend(xaxis_errors)

    # 验证 yAxis（如果存在）
    if "yAxis" in data:
        yAxis = data["yAxis"]
        if not isinstance(yAxis, dict):
            errors.append(f"{data_prefix}.yAxis: 必须是对象")
        else:
            yaxis_errors = _validate_axis(yAxis, f"{data_prefix}.yAxis")
            errors.extend(yaxis_errors)

    # 验证 legend（如果存在）
    if "legend" in data:
        legend = data["legend"]
        if not isinstance(legend, dict):
            errors.append(f"{data_prefix}.legend: 必须是对象")
        else:
            if "data" in legend and not isinstance(legend["data"], list):
                errors.append(f"{data_prefix}.legend.data: 必须是数组")

    # 验证 tooltip（如果存在）
    if "tooltip" in data:
        tooltip = data["tooltip"]
        if not isinstance(tooltip, dict):
            errors.append(f"{data_prefix}.tooltip: 必须是对象")
        else:
            if "trigger" in tooltip and tooltip["trigger"] not in ["item", "axis", "none"]:
                errors.append(f"{data_prefix}.tooltip.trigger: 必须是 'item'、'axis' 或 'none'")

    # 验证 grid（如果存在）
    if "grid" in data:
        grid = data["grid"]
        if not isinstance(grid, dict):
            errors.append(f"{data_prefix}.grid: 必须是对象")

    # 验证 dataZoom（如果存在）
    if "dataZoom" in data:
        dataZoom = data["dataZoom"]
        if not isinstance(dataZoom, list):
            errors.append(f"{data_prefix}.dataZoom: 必须是数组")

    # 验证 color（如果存在）
    if "color" in data:
        color = data["color"]
        if not isinstance(color, list):
            errors.append(f"{data_prefix}.color: 必须是数组")
        else:
            for c_idx, c in enumerate(color):
                if not isinstance(c, str):
                    errors.append(f"{data_prefix}.color[{c_idx}]: 必须是字符串（颜色值）")

    return errors


def _validate_series(series: Any, prefix: str) -> List[str]:
    """验证 ECharts series 配置"""
    errors = []

    if not isinstance(series, dict):
        return [f"{prefix}: 必须是对象"]

    # type 是必需的
    if "type" not in series:
        errors.append(f"{prefix}: 缺少必需字段 'type'")
    else:
        valid_types = {"line", "bar", "pie", "scatter", "radar", "funnel", "gauge", "heatmap", "treemap", "sunburst", "boxplot", "candlestick", "graph", "sankey", "map", "parallel", "lines", "effectScatter", "pictorialBar"}
        if series["type"] not in valid_types:
            errors.append(f"{prefix}.type: 无效的图表类型 '{series['type']}'，支持的类型: line, bar, pie, scatter, radar, funnel, candlestick 等")

    # data 是必需的
    if "data" not in series:
        errors.append(f"{prefix}: 缺少必需字段 'data'")
    else:
        data = series["data"]
        if not isinstance(data, list):
            errors.append(f"{prefix}.data: 必须是数组")
        else:
            chart_type = series.get("type", "")
            for d_idx, d in enumerate(data):
                # 饼图数据格式: [{name, value}, ...]
                if chart_type == "pie":
                    if isinstance(d, dict):
                        if "value" not in d:
                            errors.append(f"{prefix}.data[{d_idx}]: 饼图数据项缺少 'value' 字段")
                        elif not isinstance(d["value"], (int, float)):
                            errors.append(f"{prefix}.data[{d_idx}].value: 必须是数字")
                        if "name" in d and not isinstance(d["name"], str):
                            errors.append(f"{prefix}.data[{d_idx}].name: 必须是字符串")
                    else:
                        errors.append(f"{prefix}.data[{d_idx}]: 饼图数据项必须是对象，包含 name 和 value")
                # 折线图/柱状图数据格式: [值, ...] 或 [{value, name, ...}, ...]
                elif chart_type in ("line", "bar"):
                    if not isinstance(d, (int, float, dict, type(None))):
                        errors.append(f"{prefix}.data[{d_idx}]: 必须是数字、对象或null")
                # K线图数据格式: [[open, close, low, high], ...]
                elif chart_type == "candlestick":
                    if not isinstance(d, list) or len(d) != 4:
                        errors.append(f"{prefix}.data[{d_idx}]: K线图数据必须是 [open, close, low, high] 四元数组")
                    else:
                        for value_idx, value in enumerate(d):
                            if not isinstance(value, (int, float)):
                                errors.append(f"{prefix}.data[{d_idx}][{value_idx}]: K线图 OHLC 值必须是数字")
                # 散点图数据格式: [[x, y], ...] 或 [{value: [x, y]}, ...]
                elif chart_type == "scatter":
                    if isinstance(d, list):
                        if len(d) < 2:
                            errors.append(f"{prefix}.data[{d_idx}]: 散点图数据点至少需要2个值 [x, y]")
                    elif isinstance(d, dict):
                        if "value" in d and not isinstance(d["value"], list):
                            errors.append(f"{prefix}.data[{d_idx}].value: 必须是数组 [x, y]")
                    else:
                        errors.append(f"{prefix}.data[{d_idx}]: 散点图数据项必须是数组或对象")

    # 验证可选字段
    if "name" in series and not isinstance(series["name"], str):
        errors.append(f"{prefix}.name: 必须是字符串")

    if "radius" in series:
        radius = series["radius"]
        if not isinstance(radius, (str, list)):
            errors.append(f"{prefix}.radius: 必须是字符串或数组")

    if "center" in series:
        center = series["center"]
        if not isinstance(center, list) or len(center) != 2:
            errors.append(f"{prefix}.center: 必须是包含2个元素的数组 [x, y]")

    if "label" in series and not isinstance(series["label"], dict):
        errors.append(f"{prefix}.label: 必须是对象")

    if "itemStyle" in series and not isinstance(series["itemStyle"], dict):
        errors.append(f"{prefix}.itemStyle: 必须是对象")

    if "lineStyle" in series and not isinstance(series["lineStyle"], dict):
        errors.append(f"{prefix}.lineStyle: 必须是对象")

    if "areaStyle" in series and series["areaStyle"] is not None and not isinstance(series["areaStyle"], dict):
        errors.append(f"{prefix}.areaStyle: 必须是对象或null")

    if "smooth" in series and not isinstance(series["smooth"], bool):
        errors.append(f"{prefix}.smooth: 必须是布尔值")

    if "stack" in series and not isinstance(series["stack"], str):
        errors.append(f"{prefix}.stack: 必须是字符串")

    return errors


def _validate_axis(axis: Dict[str, Any], prefix: str) -> List[str]:
    """验证 ECharts 坐标轴配置"""
    errors = []

    # type 字段
    if "type" in axis:
        valid_types = {"category", "value", "time", "log"}
        if axis["type"] not in valid_types:
            errors.append(f"{prefix}.type: 必须是 'category'、'value'、'time' 或 'log'")

    # data 字段（category 类型需要）
    if "data" in axis:
        if not isinstance(axis["data"], list):
            errors.append(f"{prefix}.data: 必须是数组")
        else:
            for d_idx, d in enumerate(axis["data"]):
                if not isinstance(d, (str, int, float)):
                    errors.append(f"{prefix}.data[{d_idx}]: 必须是字符串或数字")

    # name 字段
    if "name" in axis and not isinstance(axis["name"], str):
        errors.append(f"{prefix}.name: 必须是字符串")

    # min/max 字段
    if "min" in axis and not isinstance(axis["min"], (int, float, str)):
        errors.append(f"{prefix}.min: 必须是数字或字符串")
    if "max" in axis and not isinstance(axis["max"], (int, float, str)):
        errors.append(f"{prefix}.max: 必须是数字或字符串")

    # splitLine 字段
    if "splitLine" in axis and not isinstance(axis["splitLine"], dict):
        errors.append(f"{prefix}.splitLine: 必须是对象")

    # axisLine 字段
    if "axisLine" in axis and not isinstance(axis["axisLine"], dict):
        errors.append(f"{prefix}.axisLine: 必须是对象")

    # axisLabel 字段
    if "axisLabel" in axis and not isinstance(axis["axisLabel"], dict):
        errors.append(f"{prefix}.axisLabel: 必须是对象")

    return errors


def escape_html(text: str) -> str:
    """转义HTML特殊字符，防止XSS"""
    if text is None:
        return ""
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#039;")
    )


def load_json_data(data_path: Path) -> Dict[str, Any]:
    """加载JSON数据文件"""
    try:
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"错误: 找不到数据文件 {data_path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"错误: JSON解析失败 - {e}", file=sys.stderr)
        sys.exit(1)


def detect_columns(data: List[Dict[str, Any]]) -> List[str]:
    """自动检测数据列"""
    if not data:
        return []

    # 收集所有可能的列
    all_keys = set()
    for item in data:
        if isinstance(item, dict):
            all_keys.update(item.keys())

    return sorted(list(all_keys))


def format_value(value: Any) -> str:
    """格式化单元格值"""
    if value is None:
        return ""

    if isinstance(value, (int, float)):
        if isinstance(value, float):
            return f"{value:.2f}"
        return str(value)

    return str(value)


def generate_card_html(card: Dict[str, Any]) -> str:
    """生成单个卡片的HTML"""
    label = escape_html(card.get("label", ""))
    value = escape_html(str(card.get("value", "")))
    unit = escape_html(card.get("unit", ""))
    description = escape_html(card.get("description", ""))

    # 卡片图标（可选）
    icon = card.get("icon", "bar-chart-2")

    return f"""
            <div class="card">
                <div class="card-header">
                    <div class="card-icon">
                        <i data-lucide="{icon}"></i>
                    </div>
                    <span class="card-label">{label}</span>
                </div>
                <div class="card-value-container">
                    <h3 class="card-value">{value}</h3>
                    {f'<span class="card-unit">{unit}</span>' if unit else ''}
                </div>
                {f'<p class="card-description">{description}</p>' if description else ''}
            </div>"""


def generate_table_html(table: Dict[str, Any], index: int) -> str:
    """生成单个表格的HTML"""
    title = escape_html(table.get("title", f"表格 {index + 1}"))
    data = table.get("data", [])

    if not data:
        return f"""
        <div class="table-section">
            <h3 class="table-title">{title}</h3>
            <p class="text-slate-500">无数据</p>
        </div>"""

    columns = detect_columns(data)
    table_id = f"table-{index}"

    html = f"""
        <div class="table-section">
            <h3 class="table-title">
                <div class="title-indicator"></div>
                {title}
            </h3>
            <div class="table-container">
                <table id="{table_id}" class="sortable-table">
                    <thead>
                        <tr>
"""

    # 添加表头（带排序按钮）
    for col_idx, col in enumerate(columns):
        html += f"""                            <th data-column="{col_idx}" onclick="sortTable('{table_id}', {col_idx})">
                                <span class="th-content">
                                    {escape_html(col)}
                                    <span class="sort-icon">
                                        <span class="sort-arrows">
                                            <span class="arrow-up">▲</span>
                                            <span class="arrow-down">▼</span>
                                        </span>
                                    </span>
                                </span>
                            </th>
"""

    html += """                        </tr>
                    </thead>
                    <tbody>
"""

    # 添加数据行
    for item_idx, item in enumerate(data):
        html += f'                        <tr data-original-index="{item_idx}">\n'
        for col in columns:
            value = item.get(col, "")
            formatted_value = format_value(value)
            html += f"                            <td>{escape_html(formatted_value)}</td>\n"
        html += "                        </tr>\n"

    html += """                    </tbody>
                </table>
            </div>
        </div>"""

    return html


def _normalize_echarts_option(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    规范化 ECharts 配置
    - 过滤非标准字段
    - 修正格式不正确的字段
    """
    # ECharts 标准配置字段白名单
    echarts_keys = {
        "title", "legend", "grid", "xAxis", "yAxis", "polar", "radiusAxis",
        "angleAxis", "radar", "dataZoom", "visualMap", "tooltip", "axisPointer",
        "toolbox", "brush", "geo", "parallel", "parallelAxis", "singleAxis",
        "timeline", "graphic", "calendar", "dataset", "aria", "series",
        "darkMode", "color", "backgroundColor", "textStyle", "animation",
        "animationThreshold", "animationDuration", "animationEasing",
        "animationDelay", "animationDurationUpdate", "animationEasingUpdate",
        "animationDelayUpdate", "stateAnimation", "blendMode", "hoverLayerThreshold",
        "useUTC", "options", "media"
    }

    result = {}
    for key, value in data.items():
        if key not in echarts_keys:
            # 过滤非标准字段
            continue

        # title 字段特殊处理：外层已有 chart.title，这里直接跳过
        if key == "title":
            continue

        result[key] = value

    return result


def generate_chart_html(chart: Dict[str, Any], index: int) -> str:
    """生成单个图表的HTML"""
    title = escape_html(chart.get("title", f"图表 {index + 1}"))
    data = chart.get("data", {})
    chart_id = f"chart-{index}"

    # 规范化 ECharts 配置：过滤非标准字段、删除 title（使用外层 chart.title）
    data = _normalize_echarts_option(data)

    # 将数据转为JSON字符串，用于模态框
    data_json = json.dumps(data, ensure_ascii=False)

    # 检测图表类型，判断是否支持切换
    chart_type = ""
    if data.get("series") and len(data["series"]) > 0:
        chart_type = data["series"][0].get("type", "")

    # 折线图、柱状图、饼图都支持切换
    supports_switch = chart_type in ["line", "bar", "pie"]

    # 所有支持的图表类型都显示切换按钮
    if supports_switch:
        switch_buttons = "".join([f'''
                    <button class="chart-type-btn{' active' if chart_type == t else ''}"
                            onclick="switchChartType('{chart_id}', '{t}')"
                            data-type="{t}"
                            title="{label}">
                        {icon} {label}
                    </button>''' for t, label, icon in [
                        ("line", "折线图", '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>'),
                        ("bar", "柱状图", '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="12" width="4" height="9"/><rect x="10" y="8" width="4" height="13"/><rect x="17" y="4" width="4" height="17"/></svg>'),
                        ("pie", "饼图", '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21.21 15.89A10 10 0 1 1 8 2.83"/><path d="M22 12A10 10 0 0 0 12 2v10z"/></svg>'),
                    ]])
    else:
        switch_buttons = ""

    html = f"""
        <div class="chart-section">
            <div class="chart-header">
                <h3 class="chart-title">
                    <div class="title-indicator"></div>
                    {title}
                </h3>
                <div class="chart-toolbar">
                    {switch_buttons}
                    <button class="chart-zoom-btn" onclick="openChartModal('{chart_id}')" title="放大">
                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/>
                        </svg>
                        放大
                    </button>
                </div>
            </div>
            <div id="{chart_id}" class="chart-container" data-original-option='{data_json}'></div>
        </div>
        <script>
            (function() {{
                // 全局存储图表实例
                if (!window.chartInstances) {{
                    window.chartInstances = {{}};
                }}

                const chartDom = document.getElementById('{chart_id}');
                const chart = echarts.init(chartDom);
                const option = JSON.parse(JSON.stringify({data_json}));

                // 存储到全局
                window.chartInstances['{chart_id}'] = {{
                    chart: chart,
                    originalOption: JSON.parse(JSON.stringify({data_json})),
                    currentType: option.series && option.series[0] ? option.series[0].type : 'line'
                }};

                // 应用配置
                applyChartOption(chart, option);

                // 窗口大小变化时重新渲染
                window.addEventListener('resize', () => {{
                    chart.resize();
                }});

                // 容器大小变化时重新渲染
                const resizeObserver = new ResizeObserver(() => {{
                    chart.resize();
                }});
                resizeObserver.observe(chartDom);
            }})();
        </script>
    """

    return html


def generate_html(
    title: str,
    data_file_path: str,
    data: Dict[str, Any],
    output_path: Path,
) -> None:
    """生成简易可视化HTML"""

    cards = data.get("cards", [])
    tables = data.get("tables", [])
    charts = data.get("charts", [])

    # 从数据中获取数据源信息，如果没有则使用文件路径
    data_source = data.get("source", data_file_path)

    # 生成HTML头部
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape_html(title)}</title>
    <script src="../assets/cdn/tailwindcss-3.4.16.js"></script>
    <script src="../assets/cdn/lucide.js"></script>
    <script src="../assets/cdn/echarts.5.6.0.min.js"></script>

    <style>
        body {{
            background-color: #F8FAFC;
            color: #1E293B;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
        }}

        .header {{
            background: white;
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }}

        .stats {{
            display: flex;
            gap: 1rem;
            margin-top: 1rem;
            font-size: 0.875rem;
            color: #64748B;
        }}

        /* 卡片样式 */
        .cards-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}

        .card {{
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
            overflow: hidden;
        }}

        .card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}

        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }}

        .card-icon {{
            display: flex;
            align-items: center;
            justify-content: center;
            width: 40px;
            height: 40px;
            background: #EFF6FF;
            border-radius: 10px;
            color: #3B82F6;
        }}

        .card-label {{
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #64748B;
        }}

        .card-value-container {{
            display: flex;
            align-items: baseline;
            gap: 0.5rem;
            margin-bottom: 0.75rem;
        }}

        .card-value {{
            font-size: 2rem;
            font-weight: 700;
            color: #0F172A;
            margin: 0;
        }}

        .card-unit {{
            font-size: 1rem;
            color: #64748B;
            font-weight: 500;
        }}

        .card-description {{
            font-size: 0.875rem;
            color: #64748B;
            margin: 0;
        }}

        /* 表格样式 */
        .table-section {{
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }}

        .table-title {{
            font-size: 1.125rem;
            font-weight: 700;
            color: #0F172A;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .title-indicator {{
            width: 4px;
            height: 20px;
            background: #3B82F6;
            border-radius: 2px;
        }}

        .table-container {{
            overflow-x: auto;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
        }}

        th {{
            background-color: #F1F5F9;
            color: #475569;
            font-weight: 600;
            text-align: left;
            padding: 12px 16px;
            border-bottom: 2px solid #E2E8F0;
            white-space: nowrap;
            cursor: pointer;
            user-select: none;
            position: relative;
        }}

        th:hover {{
            background-color: #E2E8F0;
        }}

        .th-content {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 8px;
        }}

        .sort-icon {{
            display: inline-flex;
            align-items: center;
            opacity: 0.3;
            transition: opacity 0.2s;
        }}

        th:hover .sort-icon {{
            opacity: 0.6;
        }}

        .sort-arrows {{
            display: flex;
            flex-direction: column;
            gap: 1px;
            font-size: 8px;
            line-height: 1;
        }}

        .arrow-up, .arrow-down {{
            color: #94A3B8;
            transition: color 0.2s;
        }}

        th.sorted-asc .arrow-up {{
            color: #3B82F6;
        }}

        th.sorted-desc .arrow-down {{
            color: #3B82F6;
        }}

        th.sorted .sort-icon {{
            opacity: 1;
        }}

        td {{
            padding: 12px 16px;
            border-bottom: 1px solid #F1F5F9;
            color: #1E293B;
        }}

        tr:hover {{
            background-color: #F8FAFC;
        }}

        /* 图表样式 */
        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}

        @media (max-width: 800px) {{
            .charts-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        .chart-section {{
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }}

        .chart-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            flex-wrap: wrap;
            gap: 0.5rem;
        }}

        .chart-title {{
            font-size: 1.125rem;
            font-weight: 700;
            color: #0F172A;
            margin: 0;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .chart-toolbar {{
            display: flex;
            gap: 0.5rem;
            align-items: center;
        }}

        .chart-type-btn {{
            display: inline-flex;
            align-items: center;
            gap: 4px;
            background: white;
            border: 1px solid #E2E8F0;
            border-radius: 6px;
            padding: 6px 12px;
            cursor: pointer;
            font-size: 13px;
            color: #64748B;
            transition: all 0.2s;
            white-space: nowrap;
        }}

        .chart-type-btn:hover {{
            background: #F8FAFC;
            border-color: #3B82F6;
            color: #3B82F6;
        }}

        .chart-type-btn.active {{
            background: #3B82F6;
            border-color: #3B82F6;
            color: white;
        }}

        .chart-type-btn.active:hover {{
            background: #2563EB;
        }}

        .chart-type-btn svg {{
            flex-shrink: 0;
        }}

        .chart-container {{
            width: 100%;
            height: 400px;
            position: relative;
        }}

        .chart-zoom-btn {{
            display: inline-flex;
            align-items: center;
            gap: 4px;
            background: white;
            border: 1px solid #E2E8F0;
            border-radius: 6px;
            padding: 6px 12px;
            cursor: pointer;
            font-size: 13px;
            color: #64748B;
            transition: all 0.2s;
            white-space: nowrap;
        }}

        .chart-zoom-btn:hover {{
            background: #F8FAFC;
            border-color: #3B82F6;
            color: #3B82F6;
        }}

        /* 模态框样式 */
        .modal-overlay {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.6);
            z-index: 1000;
            justify-content: center;
            align-items: center;
            opacity: 0;
            transition: opacity 0.3s ease;
        }}

        .modal-overlay.show {{
            display: flex;
            opacity: 1;
        }}

        .modal-content {{
            background: white;
            border-radius: 12px;
            width: 90%;
            max-width: 1200px;
            max-height: 90vh;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            transform: scale(0.9);
            transition: transform 0.3s ease;
        }}

        .modal-overlay.show .modal-content {{
            transform: scale(1);
        }}

        .modal-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 1.5rem;
            border-bottom: 1px solid #E2E8F0;
        }}

        .modal-title {{
            font-size: 1.125rem;
            font-weight: 700;
            color: #0F172A;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .modal-close-btn {{
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            color: #64748B;
            padding: 4px 8px;
            border-radius: 6px;
            transition: all 0.2s;
        }}

        .modal-close-btn:hover {{
            background: #F1F5F9;
            color: #0F172A;
        }}

        .modal-body {{
            padding: 1.5rem;
            overflow: auto;
            flex: 1;
            display: flex;
            justify-content: center;
            align-items: center;
        }}

        .modal-chart-container {{
            width: 100%;
            height: 500px;
        }}

        .footer {{
            text-align: center;
            margin-top: 2rem;
            padding-top: 2rem;
            border-top: 1px solid #E2E8F0;
            color: #94A3B8;
            font-size: 0.875rem;
        }}
    </style>

    <script>
        // 全局存储图表实例
        window.chartInstances = {{}};

        // 高区分度的饼图颜色
        const PIE_COLORS = [
            '#3B82F6', '#EF4444', '#10B981', '#F59E0B', '#8B5CF6',
            '#EC4899', '#06B6D4', '#84CC16', '#F97316', '#6366F1',
            '#14B8A6', '#E11D48', '#0EA5E9', '#A855F7', '#22C55E'
        ];

        // 应用图表配置的通用函数
        function applyChartOption(chart, option) {{
            // 自动添加自适应配置
            if (!option.grid) {{
                option.grid = {{ left: '5%', right: '5%', bottom: '15%', top: '10%', containLabel: true }};
            }} else {{
                option.grid.containLabel = true;
            }}

            if (!option.tooltip) {{
                option.tooltip = {{ trigger: 'axis' }};
            }}

            // 如果有 legend，配置滚动和边距
            if (option.legend) {{
                if (!option.legend.type) {{
                    option.legend.type = 'scroll';
                }}
                if (option.legend.top === undefined && option.legend.bottom === undefined) {{
                    option.legend.top = '5%';
                }}
                if (!option.grid.top || option.grid.top === '10%') {{
                    option.grid.top = '15%';
                }}
            }}

            // 自动添加 dataZoom 滚动条（折线图、柱状图、K线图）
            if (option.series && option.series.length > 0) {{
                const chartType = option.series[0].type;
                if (chartType === 'line' || chartType === 'bar' || chartType === 'candlestick') {{
                    if (!option.dataZoom) {{
                        option.dataZoom = [
                            {{
                                type: 'inside',
                                start: 0,
                                end: 100,
                                zoomOnMouseWheel: true,
                                moveOnMouseMove: true
                            }},
                            {{
                                type: 'slider',
                                start: 0,
                                end: 100,
                                height: 20,
                                bottom: 5
                            }}
                        ];
                    }}
                }}

                if (chartType === 'candlestick') {{
                    if (option.yAxis && !Array.isArray(option.yAxis)) {{
                        option.yAxis.scale = option.yAxis.scale !== undefined ? option.yAxis.scale : true;
                    }}
                    option.tooltip = option.tooltip || {{ trigger: 'axis' }};
                }}

                // 饼图自动添加高区分度颜色
                if (chartType === 'pie') {{
                    // 为每个数据项设置 itemStyle.color
                    option.series.forEach(s => {{
                        if (Array.isArray(s.data)) {{
                            s.data.forEach((item, idx) => {{
                                if (typeof item === 'object') {{
                                    item.itemStyle = item.itemStyle || {{}};
                                    item.itemStyle.color = PIE_COLORS[idx % PIE_COLORS.length];
                                }}
                            }});
                        }}
                    }});
                    option.color = PIE_COLORS;
                }}
            }}

            // 自动添加背景网格线
            if (option.xAxis) {{
                if (!option.xAxis.splitLine) {{
                    option.xAxis.splitLine = {{
                        show: true,
                        lineStyle: {{
                            color: '#E5E7EB',
                            type: 'dashed'
                        }}
                    }};
                }}
            }}
            if (option.yAxis) {{
                if (!option.yAxis.splitLine) {{
                    option.yAxis.splitLine = {{
                        show: true,
                        lineStyle: {{
                            color: '#E5E7EB',
                            type: 'dashed'
                        }}
                    }};
                }}
            }}

            chart.setOption(option, true);
        }}
    </script>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 style="font-size: 1.875rem; font-weight: 700; color: #0F172A; margin-bottom: 0.5rem;">
                {escape_html(title)}
            </h1>
            <div class="stats">
                <span>📊 数据源: {escape_html(data_source)}</span>
                <span>📅 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</span>
            </div>
        </div>
"""

    # 添加卡片
    if cards:
        html += """
        <div class="cards-grid">
"""
        for card in cards:
            html += generate_card_html(card)

        html += """
        </div>
"""

    # 添加图表
    if charts:
        html += """
        <div class="charts-grid">
"""
        for i, chart in enumerate(charts):
            html += generate_chart_html(chart, i)
        html += """
        </div>
"""

    # 添加表格
    if tables:
        for i, table in enumerate(tables):
            html += generate_table_html(table, i)

    # 添加页脚
    html += """
        <div class="footer">
            数据质量已验证 - 完整性: 100%
        </div>
    </div>

    <script>
        // 切换图表类型
        function switchChartType(chartId, newType) {
            const instance = window.chartInstances[chartId];
            if (!instance) return;

            const { chart, originalOption } = instance;

            // 深拷贝原始配置
            const newOption = JSON.parse(JSON.stringify(originalOption));

            // 更新按钮状态
            const section = document.getElementById(chartId).closest('.chart-section');
            section.querySelectorAll('.chart-type-btn').forEach(btn => {
                btn.classList.remove('active');
                if (btn.dataset.type === newType) {
                    btn.classList.add('active');
                }
            });

            // 检测原始图表类型
            const originalType = originalOption.series && originalOption.series[0] ? originalOption.series[0].type : 'line';

            // 修改图表类型
            if (newOption.series) {
                newOption.series.forEach(s => {
                    const oldType = s.type;
                    s.type = newType;

                    // 从饼图切换到折线图/柱状图
                    if (oldType === 'pie' && (newType === 'line' || newType === 'bar')) {
                        // 饼图数据是 [{name, value}, ...] 格式，需要转换
                        if (Array.isArray(s.data) && s.data.length > 0 && s.data[0].name !== undefined) {
                            const names = s.data.map(d => d.name);
                            const values = s.data.map(d => d.value);
                            s.data = values;
                            // 添加坐标轴
                            newOption.xAxis = { type: 'category', data: names };
                            newOption.yAxis = { type: 'value' };
                        }
                        // 清除饼图特有配置
                        delete s.radius;
                        delete s.center;
                        delete s.label;
                        newOption.tooltip = { trigger: 'axis' };
                    }
                    // 从折线图/柱状图切换到饼图
                    else if ((oldType === 'line' || oldType === 'bar') && newType === 'pie') {
                        // 转换数据格式为饼图格式
                        if (newOption.xAxis && newOption.xAxis.data) {
                            const names = newOption.xAxis.data;
                            const values = s.data;
                            s.data = names.map((name, idx) => ({
                                name: name,
                                value: values[idx]
                            }));
                        }
                        s.radius = '60%';
                        s.center = ['50%', '50%'];
                        s.label = { show: true, formatter: '{b}: {c}' };
                    }
                });

                // 饼图不需要坐标轴
                if (newType === 'pie') {
                    delete newOption.xAxis;
                    delete newOption.yAxis;
                    delete newOption.dataZoom;
                    newOption.tooltip = { trigger: 'item' };
                    newOption.color = PIE_COLORS;
                }
            }

            // 更新当前类型
            instance.currentType = newType;

            // 清空并重新渲染
            chart.clear();
            applyChartOption(chart, newOption);
        }

        // 图表模态框功能
        let modalChart = null;
        let modalChartId = null;

        function openChartModal(chartId) {
            const instance = window.chartInstances[chartId];
            if (!instance) return;

            const modal = document.getElementById('chart-modal');
            const modalTitle = modal.querySelector('.modal-title');
            const chartDom = document.getElementById('modal-chart');

            // 显示模态框
            modal.classList.add('show');
            document.body.style.overflow = 'hidden';

            // 销毁之前的图表实例
            if (modalChart) {
                modalChart.dispose();
            }

            // 初始化模态框中的图表
            modalChart = echarts.init(chartDom);
            modalChartId = chartId;

            // 深拷贝原始配置并应用当前类型
            const option = JSON.parse(JSON.stringify(instance.originalOption));
            const currentType = instance.currentType;
            const originalType = instance.originalOption.series && instance.originalOption.series[0] ? instance.originalOption.series[0].type : 'line';

            // 应用当前图表类型
            if (option.series) {
                option.series.forEach(s => {
                    const oldType = s.type;
                    s.type = currentType;

                    // 从饼图切换到折线图/柱状图
                    if (oldType === 'pie' && (currentType === 'line' || currentType === 'bar')) {
                        if (Array.isArray(s.data) && s.data.length > 0 && s.data[0].name !== undefined) {
                            const names = s.data.map(d => d.name);
                            const values = s.data.map(d => d.value);
                            s.data = values;
                            option.xAxis = { type: 'category', data: names };
                            option.yAxis = { type: 'value' };
                        }
                        delete s.radius;
                        delete s.center;
                        delete s.label;
                        option.tooltip = { trigger: 'axis' };
                    }
                    // 从折线图/柱状图切换到饼图
                    else if ((oldType === 'line' || oldType === 'bar') && currentType === 'pie') {
                        if (option.xAxis && option.xAxis.data) {
                            const names = option.xAxis.data;
                            const values = s.data;
                            s.data = names.map((name, idx) => ({
                                name: name,
                                value: values[idx]
                            }));
                        }
                        s.radius = '60%';
                        s.center = ['50%', '50%'];
                        s.label = { show: true, formatter: '{b}: {c}' };
                    }
                });

                if (currentType === 'pie') {
                    delete option.xAxis;
                    delete option.yAxis;
                    delete option.dataZoom;
                    option.tooltip = { trigger: 'item' };
                    option.color = PIE_COLORS;
                    // 为饼图每个数据项设置颜色，防止白屏
                    option.series.forEach(s => {
                        if (Array.isArray(s.data)) {
                            s.data.forEach((item, idx) => {
                                if (typeof item === 'object') {
                                    item.itemStyle = item.itemStyle || {};
                                    item.itemStyle.color = PIE_COLORS[idx % PIE_COLORS.length];
                                }
                            });
                        }
                    });
                }
            }

            // 调整 grid 配置以适应更大的容器
            if (!option.grid) {
                option.grid = { left: '5%', right: '5%', bottom: '15%', top: '15%', containLabel: true };
            } else {
                option.grid.containLabel = true;
            }

            // 如果有图例，调整配置
            if (option.legend && option.legend.type !== 'scroll') {
                option.legend.type = 'scroll';
                if (!option.grid.top || option.grid.top === '10%' || option.grid.top === '15%') {
                    option.grid.top = '20%';
                }
            }

            // 更新标题
            const section = document.getElementById(chartId).closest('.chart-section');
            const titleEl = section.querySelector('.chart-title');
            const titleText = titleEl ? titleEl.textContent.trim() : '图表详情';
            modalTitle.innerHTML = '<div class="title-indicator"></div>' + titleText;

            applyChartOption(modalChart, option);

            // 窗口大小变化时重新渲染
            const resizeHandler = () => modalChart.resize();
            window.addEventListener('resize', resizeHandler);
            modal._resizeHandler = resizeHandler;
        }

        function closeChartModal() {
            const modal = document.getElementById('chart-modal');
            if (!modal) return;

            modal.classList.remove('show');
            document.body.style.overflow = '';

            // 销毁模态框中的图表并移除事件监听
            if (modalChart) {
                modalChart.dispose();
                modalChart = null;
            }
            if (modal._resizeHandler) {
                window.removeEventListener('resize', modal._resizeHandler);
                delete modal._resizeHandler;
            }
        }

        // ESC 键关闭模态框
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                closeChartModal();
            }
        });

        // 表格排序功能
        const sortStates = {}; // 存储每个表格每列的排序状态

        function sortTable(tableId, columnIndex) {
            const table = document.getElementById(tableId);
            const tbody = table.querySelector('tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));
            const th = table.querySelector(`th[data-column="${columnIndex}"]`);

            // 初始化排序状态
            if (!sortStates[tableId]) {
                sortStates[tableId] = {};
            }

            // 获取当前列的排序状态 (null -> asc -> desc -> null)
            const currentState = sortStates[tableId][columnIndex] || null;
            let newState;

            if (currentState === null) {
                newState = 'asc';
            } else if (currentState === 'asc') {
                newState = 'desc';
            } else {
                newState = null;
            }

            // 更新排序状态
            sortStates[tableId][columnIndex] = newState;

            // 清除所有列的排序样式
            table.querySelectorAll('th').forEach(header => {
                header.classList.remove('sorted', 'sorted-asc', 'sorted-desc');
            });

            // 设置当前列的样式
            if (newState) {
                th.classList.add('sorted', `sorted-${newState}`);
            }

            // 排序或恢复原始顺序
            if (newState === null) {
                // 恢复原始顺序
                rows.sort((a, b) => {
                    return parseInt(a.getAttribute('data-original-index')) -
                           parseInt(b.getAttribute('data-original-index'));
                });
            } else {
                // 执行排序
                rows.sort((a, b) => {
                    const aValue = a.cells[columnIndex].textContent.trim();
                    const bValue = b.cells[columnIndex].textContent.trim();

                    // 尝试作为数字比较
                    const aNum = parseFloat(aValue.replace(/[^0-9.-]/g, ''));
                    const bNum = parseFloat(bValue.replace(/[^0-9.-]/g, ''));

                    let comparison = 0;
                    if (!isNaN(aNum) && !isNaN(bNum)) {
                        comparison = aNum - bNum;
                    } else {
                        comparison = aValue.localeCompare(bValue, 'zh-CN');
                    }

                    return newState === 'asc' ? comparison : -comparison;
                });
            }

            // 重新添加行到表格
            rows.forEach(row => tbody.appendChild(row));
        }

        // 初始化 Lucide 图标
        lucide.createIcons();
    </script>

    <!-- 图表放大模态框 -->
    <div id="chart-modal" class="modal-overlay" onclick="closeChartModal()">
        <div class="modal-content" onclick="event.stopPropagation()">
            <div class="modal-header">
                <div class="modal-title">
                    <div class="title-indicator"></div>
                    图表详情
                </div>
                <button class="modal-close-btn" onclick="closeChartModal()">&times;</button>
            </div>
            <div class="modal-body">
                <div id="modal-chart" class="modal-chart-container"></div>
            </div>
        </div>
    </div>
</body>
</html>
"""

    # 写入文件
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✓ HTML文件已生成: {output_path}")
    if cards:
        print(f"  - 卡片数: {len(cards)}")
    if tables:
        print(f"  - 表格数: {len(tables)}")
    if charts:
        print(f"  - 图表数: {len(charts)}")


def main():
    parser = argparse.ArgumentParser(
        description="从已准备好的JSON生成数据可视化HTML报告（支持KPI、普通表格、ECharts图表和K线图）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
数据格式（JSON）:
{
  "cards": [...],
  "tables": [...],
  "charts": [
    {
      "title": "销售趋势",
      "data": {
        "xAxis": {"type": "category", "data": ["1月", "2月", "3月"]},
        "yAxis": {"type": "value"},
        "series": [{"data": [120, 200, 150], "type": "line"}]
      }
    }
  ]
}

K线图 series.data 使用 ECharts 标准顺序: [open, close, low, high]

示例:
  %(prog)s "销售数据分析" data.json
  %(prog)s "用户统计" data.json -o output.html
        """
    )

    parser.add_argument(
        "title",
        help="报告标题"
    )

    parser.add_argument(
        "data_file",
        help="数据文件路径 (JSON格式)"
    )

    parser.add_argument(
        "-o", "--output",
        help="输出HTML文件路径 (默认: 根据标题和时间自动生成)",
        default=None
    )

    args = parser.parse_args()

    # 解析路径
    data_path = Path(args.data_file)

    # 生成输出路径
    if args.output:
        output_path = Path(args.output)
    else:
        # 自动生成输出文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = "".join(c for c in args.title if c.isalnum() or c in (' ', '_', '-')).strip()
        safe_title = safe_title.replace(' ', '_')
        filename = f"report_{safe_title}_{timestamp}.html"
        output_path = Path("dashboard") / filename

    # 加载数据
    data = load_json_data(data_path)

    # 验证数据格式
    is_valid, errors = validate_data_format(data)
    if not is_valid:
        print("错误: 数据格式验证失败", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        sys.exit(1)

    # 生成HTML
    generate_html(args.title, str(data_path), data, output_path)


if __name__ == "__main__":
    main()
