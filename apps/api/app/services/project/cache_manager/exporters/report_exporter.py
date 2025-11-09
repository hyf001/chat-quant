"""
Report Exporter - 报表导出器
"""
import asyncio
import logging
import os
from datetime import datetime
from typing import List, Optional, Dict, Any, Callable
from pathlib import Path

from .base_exporter import BaseExporter
from ..client.easyfetch_https_client import EasyFetchHttpsClient
from ..config.config_manager import ConfigManager
from ..utils.file_manager import FileManager
from ..utils.data_processor import sanitize_filename

logger = logging.getLogger(__name__)


class ReportExporter(BaseExporter):
    """报表导出器"""

    def __init__(self, config: ConfigManager, agent_type: str = "data_analysis"):
        """
        初始化报表导出器

        Args:
            config: 配置管理器
            agent_type: 智能体类型
        """
        super().__init__(config, agent_type)

        # 初始化文件管理器
        self.file_manager = FileManager(str(self.output_dir))

        # 初始化HTTPS客户端（替代MCP客户端）
        # 所有参数从环境变量自动读取，也可以通过config传入
        self.https_client = EasyFetchHttpsClient(
            email=config.get("default_email"),
            tenant_id=config.get("tenant_id")
            # base_url, cert_path, cert_password 自动从环境变量读取
        )

    async def export(self,
                    business_lines: Optional[List[str]] = None,
                    dry_run: bool = False,
                    verbose: bool = False,
                    query: Optional[str] = None,
                    use_atomic_replace: bool = True) -> bool:
        """
        导出报表

        Args:
            business_lines: 业务线过滤
            dry_run: 是否为预览模式
            verbose: 是否详细输出
            query: 查询关键字
            use_atomic_replace: 是否使用原子性替换（默认True）

        Returns:
            是否成功
        """
        start_time = datetime.now()

        try:
            logger.info("🚀 开始导出报表...")

            if dry_run:
                logger.info("📋 预览模式 - 不会实际写入文件")

            if use_atomic_replace and not dry_run:
                logger.info("🔄 使用原子性替换模式（先写入临时目录，完成后原子性替换）")

            # 初始化统计信息
            processed_count = 0
            saved_count = 0
            business_line_stats = {}
            saved_files = []
            affected_business_lines = set()  # 记录受影响的业务线

            # 获取报表目录树
            tree_data = await self._fetch_report_tree(query)
            if not tree_data:
                logger.error("获取报表目录树失败")
                return False

            # 遍历目录树，提取所有报表
            root_node = tree_data.get("root")
            if not root_node:
                logger.error("报表目录树根节点不存在")
                return False

            # 递归处理子节点
            async def process_node(node: Dict[str, Any], path_parts: List[str]):
                nonlocal processed_count, saved_count

                # 获取节点信息
                node_id = node.get("id")
                node_name = node.get("name")
                node_type = node.get("type")
                unique_id = node.get("unique_id")
                parent_unique_id = node.get("parent_unique_id")
                sub_node_list = node.get("sub_node_list", [])

                # 如果是报表节点（type="REPORT"）
                if node_type == "REPORT":
                    processed_count += 1

                    # 构建路径：业务线/数据类型/子目录/报表名称
                    # path_parts[0] 是业务线
                    # path_parts[1] 是数据类型（如果有的话）
                    # path_parts[2:] 是子目录
                    business_line = path_parts[0] if len(path_parts) > 0 else "unknown"

                    # 特殊逻辑：将 "dream" 替换为 "dreamface"
                    if business_line == "dream":
                        business_line = "dreamface"

                    # 业务线过滤
                    if business_lines and business_line not in business_lines:
                        return

                    if verbose:
                        logger.info(f"📊 处理报表 [{processed_count}]: {'/'.join(path_parts + [node_name])}")

                    # 获取报表详情
                    report_detail = await self._fetch_report_detail(node_id)
                    if not report_detail:
                        logger.warning(f"获取报表详情失败: {node_name} (ID: {node_id})")
                        return

                    # 过滤条件：只导出 enable_tag=true 的报表
                    enable_tag = report_detail.get("enable_tag", False)
                    if not enable_tag:
                        if verbose:
                            logger.debug(f"跳过报表 {node_name}: enable_tag={enable_tag}")
                        return

                    # 构建YAML数据
                    export_time = datetime.now().isoformat()
                    yaml_data = self._build_report_yaml_data(
                        node=node,
                        report_detail=report_detail,
                        path_parts=path_parts,
                        export_time=export_time
                    )

                    # 更新业务线统计
                    business_line_stats[business_line] = business_line_stats.get(business_line, 0) + 1
                    affected_business_lines.add(business_line)  # 记录受影响的业务线

                    # 保存文件
                    if not dry_run:
                        # 报表的数据类型固定为"bi_report"
                        category = "bi_report"

                        # 子目录路径：path_parts从第2个元素开始（第1个是业务线）
                        # 例如：path_parts = ["cot", "A股开户2.0 --分入口"]
                        # sub_dirs = ["A股开户2.0 --分入口"]
                        sub_dirs = path_parts[1:] if len(path_parts) > 1 else []

                        # 生成文件名
                        filename = sanitize_filename(node_name)

                        # 手动构建完整路径：使用临时目录或正式目录
                        if use_atomic_replace:
                            file_path = self.file_manager.get_temp_category_path(business_line, category)
                        else:
                            file_path = self.output_dir / business_line / category

                        for sub_dir in sub_dirs:
                            file_path = file_path / sanitize_filename(sub_dir)
                        file_path = file_path / f"{filename}.yaml"

                        # 保存文件（报表使用自定义保存方法）
                        success = self._save_report_yaml_file(yaml_data, file_path)
                        if success:
                            saved_count += 1
                            saved_files.append(str(file_path))

                            if verbose:
                                logger.info(f"💾 已保存: {file_path}")

                # 如果有子节点，递归处理
                elif sub_node_list:
                    # 构建新的路径
                    new_path = path_parts + [node_name] if node_name != "REPORT" else path_parts

                    for sub_node in sub_node_list:
                        await process_node(sub_node, new_path)

            # 处理根节点下的所有业务线
            sub_nodes = root_node.get("sub_node_list", [])
            for business_line_node in sub_nodes:
                await process_node(business_line_node, [])

            # 原子性替换：将临时目录替换为正式目录
            if use_atomic_replace and not dry_run and affected_business_lines:
                logger.info("\n🔄 开始原子性替换目录...")
                replace_success_count = 0
                replace_fail_count = 0

                for business_line in sorted(affected_business_lines):
                    try:
                        success = self.file_manager.atomic_replace_category_dir(
                            business_line=business_line,
                            category="bi_report"
                        )
                        if success:
                            replace_success_count += 1
                        else:
                            replace_fail_count += 1
                    except Exception as e:
                        logger.error(f"原子性替换失败 {business_line}/bi_report: {e}")
                        replace_fail_count += 1

                logger.info(f"✅ 原子性替换完成: 成功 {replace_success_count} 个，失败 {replace_fail_count} 个")

                if replace_fail_count > 0:
                    logger.warning("部分业务线的原子性替换失败，请检查日志")

            # 显示最终统计
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            logger.info("\n" + "=" * 80)
            logger.info("✅ 报表导出完成!")
            logger.info(f"📊 处理报表: {processed_count} 个")
            logger.info(f"💾 保存文件: {saved_count} 个")
            logger.info(f"📂 输出目录: {self.output_dir}")
            logger.info(f"⏱️  耗时: {duration:.2f} 秒")

            if verbose and business_line_stats:
                logger.info("\n📁 业务线分布:")
                for bl, count in sorted(business_line_stats.items()):
                    logger.info(f"  - {bl}: {count} 个")

            logger.info("=" * 80)
            return True

        except Exception as e:
            logger.error(f"报表导出过程异常: {str(e)}", exc_info=True)
            return False

        finally:
            await self.https_client.close()

    async def _fetch_report_tree(self, query: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        获取报表目录树（通过HTTPS接口）

        Args:
            query: 查询关键字

        Returns:
            报表目录树数据
        """
        try:
            # 调用HTTPS接口获取报表列表
            result = await self.https_client.get_report_list(
                query=query or "",
                table_type="REPORT"
            )

            # 调试：打印返回结果结构
            logger.debug(f"HTTPS返回结果类型: {type(result)}")
            logger.debug(f"HTTPS返回结果keys: {result.keys() if isinstance(result, dict) else 'N/A'}")

            # 检查响应状态
            if result.get("status_code") == 0:
                return result.get("data")

            error_msg = result.get("status_msg", "Unknown error")
            logger.error(f"获取报表目录树失败: {error_msg}")
            return None

        except Exception as e:
            logger.error(f"获取报表目录树异常: {str(e)}")
            return None

    async def _fetch_report_detail(self, report_id: str) -> Optional[Dict[str, Any]]:
        """
        获取报表详情（通过HTTPS接口）

        Args:
            report_id: 报表ID

        Returns:
            报表详情数据
        """
        try:
            # 调用HTTPS接口获取报表详情
            result = await self.https_client.get_table_detail(report_id)

            # 检查响应状态
            if result.get("status_code") == 0:
                return result.get("data")

            error_msg = result.get("status_msg", "Unknown error")
            logger.error(f"获取报表详情失败 (ID: {report_id}): {error_msg}")
            return None

        except Exception as e:
            logger.error(f"获取报表详情异常 (ID: {report_id}): {str(e)}")
            return None

    def _build_report_yaml_data(self,
                               node: Dict[str, Any],
                               report_detail: Dict[str, Any],
                               path_parts: List[str],
                               export_time: str) -> Dict[str, Any]:
        """
        构建报表YAML数据

        Args:
            node: 目录树节点
            report_detail: 报表详情
            path_parts: 路径组成部分
            export_time: 导出时间

        Returns:
            YAML数据字典
        """
        # 初始化空字典
        yaml_data = {}

        # 报表详情：直接平铺，不用detail封装
        if report_detail:
            yaml_data.update(report_detail)

        # 需要移除的字段列表
        fields_to_remove = [
            "_path_info", "_metadata", "dashboard", "principal",
            "parent_unique_id", "db_name",
            "primary_column_list", "partition_column_list",
            "dir_id", "lifecycle", "create_time", "modifier",
            "creator", "update_time", "directory", "datasource_name",
            "enable_tag", "uuid", "puuid"
        ]

        # 移除不需要的字段
        for field in fields_to_remove:
            yaml_data.pop(field, None)

        # 重命名 column_list 为 columns
        if "column_list" in yaml_data:
            yaml_data["columns"] = yaml_data.pop("column_list")

        # 特殊逻辑：将 business_line 中的 "dream" 替换为 "dreamface"
        if "business_line" in yaml_data:
            business_lines = yaml_data["business_line"]
            if isinstance(business_lines, list):
                yaml_data["business_line"] = [
                    "dreamface" if bl == "dream" else bl
                    for bl in business_lines
                ]

        # 按指定顺序重新组织字段
        ordered_data = {}

        # 所有字段按顺序
        ordered_fields = ["id", "en_name", "cn_name", "standard_name", "alias",
                         "business_line", "table_type", "path"]

        for field in ordered_fields:
            if field in yaml_data:
                ordered_data[field] = yaml_data[field]

        # extra_info(倒数第二) - 转换为JSON字符串格式
        if "extra_info" in yaml_data:
            import json
            extra_info = yaml_data["extra_info"].copy()  # 复制一份，不修改原始数据
            show_type_desc = None  # 用于保存showType的中文描述

            if isinstance(extra_info, dict):
                # 移除 env 字段
                extra_info.pop("env", None)

                # showType枚举映射
                show_type_map = {
                    0: "表格", 1: "折线图", 2: "指标卡片", 3: "柱状图",
                    4: "散点图", 5: "条状图", 6: "饼图", 7: "玫瑰图",
                    8: "堆叠图", 9: "瀑布图", 10: "漏斗图", 11: "富文本",
                    12: "排行榜", 13: "面积图", 14: "桑基图", 15: "径向树状图",
                    16: "旭日图"
                }

                # 获取showType的中文描述（用于注释，不添加到数据中）
                if "showType" in extra_info:
                    show_type_value = extra_info["showType"]
                    show_type_desc = show_type_map.get(show_type_value, f"未知类型({show_type_value})")

                # 使用json.dumps格式化为多行JSON字符串
                json_str = json.dumps(extra_info, indent=2, ensure_ascii=False)
                # 使用特殊标记，后续处理时转换为literal block scalar
                ordered_data["extra_info"] = f"__LITERAL_BLOCK_START__\n{json_str}\n__LITERAL_BLOCK_END__"
                # 保存showType描述用于注释
                ordered_data["_show_type_desc"] = show_type_desc
            else:
                ordered_data["extra_info"] = extra_info

        # columns - 转换为JSON字符串格式
        if "columns" in yaml_data:
            import json
            columns = yaml_data["columns"]
            if isinstance(columns, list):
                # 格式化每个字段对象
                formatted_columns = []
                for col in columns:
                    # 只保留需要的字段（移除 order_no）
                    simplified_col = {
                        "en_name": col.get("en_name"),
                        "cn_name": col.get("cn_name"),
                        "type": col.get("type"),
                        "sample_data": col.get("sample_data")
                    }
                    formatted_columns.append(simplified_col)

                # 使用json.dumps格式化为多行JSON字符串
                json_str = json.dumps(formatted_columns, indent=2, ensure_ascii=False)
                # 使用特殊标记，后续处理时转换为literal block scalar
                ordered_data["columns"] = f"__LITERAL_BLOCK_START__\n{json_str}\n__LITERAL_BLOCK_END__"
            else:
                ordered_data["columns"] = columns

        return ordered_data

    def _save_report_yaml_file(self, yaml_data: Dict[str, Any], file_path: Path) -> bool:
        """
        保存报表YAML文件（自定义格式）

        Args:
            yaml_data: YAML数据
            file_path: 文件路径

        Returns:
            bool: 是否保存成功
        """
        try:
            import yaml
            from io import StringIO
            from ..utils.file_manager import QuotedStringDumper

            # 创建目录结构
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # 保存showType描述并从数据中移除
            show_type_desc = yaml_data.pop("_show_type_desc", None)

            # 生成YAML内容
            stream = StringIO()
            yaml.dump(yaml_data, stream,
                     Dumper=QuotedStringDumper,
                     default_flow_style=False,
                     allow_unicode=True,
                     indent=2,
                     sort_keys=False)
            yaml_content = stream.getvalue()

            # 处理特殊标记，移除标记行但保留内容
            import re

            # 移除 __LITERAL_BLOCK_START__ 和 __LITERAL_BLOCK_END__ 标记行
            lines = yaml_content.split('\n')
            cleaned_lines = []
            for line in lines:
                # 跳过包含标记的行
                if '__LITERAL_BLOCK_START__' in line or '__LITERAL_BLOCK_END__' in line:
                    continue
                cleaned_lines.append(line)

            yaml_content = '\n'.join(cleaned_lines)

            # 动态构建extra_info注释（使用之前保存的show_type_desc）
            if show_type_desc:
                extra_info_comment = f'  # 扩展信息(uv: 近3个月报表使用uv, pv: 近3个月报表使用pv, showType: 报表图表类型-{show_type_desc})'
            else:
                extra_info_comment = '  # 扩展信息(uv: 近3个月报表使用uv, pv: 近3个月报表使用pv, showType: 报表图表类型)'

            # 添加字段注释
            field_comments = {
                '"en_name":': '  # 报表英文名称',
                '"cn_name":': '  # 报表中文名称',
                '"standard_name":': '  # 报表治理后的标准名称',
                '"alias":': '  # 报表别名，多个用英文逗号分隔',
                '"business_line":': '  # 归属业务线',
                '"path":': '  # 报表路径',
                '"extra_info":': extra_info_comment,
                '"columns":': '  # 报表字段列表'
            }

            # 为每个字段添加注释（只为顶层字段添加，不为嵌套字段添加）
            lines = yaml_content.split('\n')
            commented_lines = []
            in_multiline_block = False  # 标记是否在多行块内（extra_info 或 columns）

            for line in lines:
                # 检查是否进入多行块
                if '"extra_info": |' in line or '"columns": |' in line:
                    in_multiline_block = True
                    # 为该顶层字段添加注释
                    for field, comment in field_comments.items():
                        if line.strip().startswith(field):
                            commented_lines.append(line.rstrip() + comment)
                            break
                    else:
                        commented_lines.append(line)
                    continue

                # 如果在多行块内
                if in_multiline_block:
                    # 检查是否离开多行块（下一个顶层字段出现，没有缩进）
                    if line and not line[0].isspace() and line.strip().startswith('"'):
                        in_multiline_block = False
                        # 处理这个新的顶层字段
                        comment_added = False
                        for field, comment in field_comments.items():
                            if line.strip().startswith(field):
                                commented_lines.append(line + comment)
                                comment_added = True
                                break
                        if not comment_added:
                            commented_lines.append(line)
                    else:
                        # 仍在多行块内，不添加注释
                        commented_lines.append(line)
                    continue

                # 为顶层字段添加注释
                comment_added = False
                for field, comment in field_comments.items():
                    if line.strip().startswith(field):
                        commented_lines.append(line + comment)
                        comment_added = True
                        break

                if not comment_added:
                    commented_lines.append(line)

            yaml_content = '\n'.join(commented_lines)

            # 写入文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(yaml_content)

            logger.debug(f"YAML文件已保存: {file_path}")
            return True

        except Exception as e:
            logger.error(f"保存YAML文件失败: {file_path}, 错误: {str(e)}")
            return False
