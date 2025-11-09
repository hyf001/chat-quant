"""
DataTable Exporter - 数据表导出器
先获取表列表，再获取每个表的详细字段信息
"""
import asyncio
import logging
import os
from datetime import datetime
from typing import List, Optional, Dict, Any
from pathlib import Path

from .base_exporter import BaseExporter
from ..client.easyfetch_https_client import EasyFetchHttpsClient
from ..config.config_manager import ConfigManager
from ..utils.file_manager import FileManager
from ..utils.data_processor import sanitize_filename

logger = logging.getLogger(__name__)


class DataTableExporter(BaseExporter):
    """数据表导出器"""

    def __init__(self, config: ConfigManager, agent_type: str = "data_analysis"):
        """
        初始化数据表导出器

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
                    table_type: str = "PHYSICAL",
                    query: Optional[str] = None,
                    batch_size: int = 10,
                    use_atomic_replace: bool = True) -> bool:
        """
        导出数据表schema

        Args:
            business_lines: 业务线过滤
            dry_run: 是否为预览模式
            verbose: 是否详细输出
            table_type: 表类型 (PHYSICAL/REPORT)
            query: 查询关键字
            batch_size: 批处理大小（表详情查询并发数）
            use_atomic_replace: 是否使用原子性替换（默认True）

        Returns:
            是否成功
        """
        start_time = datetime.now()

        try:
            logger.info(f"🚀 开始导出数据表schema (类型: {table_type})...")

            if dry_run:
                logger.info("📋 预览模式 - 不会实际写入文件")

            if use_atomic_replace and not dry_run:
                logger.info("🔄 使用原子性替换模式（先写入临时目录，完成后原子性替换）")

            # 第一步：获取表列表
            logger.info("📡 正在获取表列表...")
            table_list = await self._get_table_list(table_type, query)

            if not table_list:
                logger.warning("未找到任何表")
                return True

            logger.info(f"📊 找到 {len(table_list)} 个表")

            # 初始化统计信息
            processed_count = 0
            saved_count = 0
            business_line_stats = {}
            saved_files = []
            affected_business_lines = set()  # 记录受影响的业务线

            # 第二步：批量获取表详情并保存
            for i in range(0, len(table_list), batch_size):
                batch = table_list[i:i+batch_size]

                if verbose:
                    logger.info(f"📥 正在获取表详情 ({i+1}-{min(i+batch_size, len(table_list))}/{len(table_list)})...")

                # 并发获取表详情
                detail_tasks = [
                    self._get_table_detail(str(table["id"]))
                    for table in batch
                ]
                details = await asyncio.gather(*detail_tasks, return_exceptions=True)

                # 处理每个表的详情
                for table_meta, detail in zip(batch, details):
                    try:
                        if isinstance(detail, Exception):
                            logger.error(f"获取表详情失败 (ID: {table_meta.get('id')}): {str(detail)}")
                            continue

                        # 合并表元数据和详情
                        merged_data = self._merge_table_data(table_meta, detail)

                        # 过滤条件：只导出 enable_tag=true 且 datasource_name=presto-hive 的表
                        enable_tag = merged_data.get("enable_tag", False)
                        datasource_name = merged_data.get("datasource_name", "")

                        if not enable_tag or datasource_name != "presto-hive":
                            if verbose:
                                table_name = merged_data.get("en_name", "unknown")
                                logger.debug(f"跳过表 {table_name}: enable_tag={enable_tag}, datasource_name={datasource_name}")
                            continue

                        # 提取业务线（支持多个业务线）
                        business_lines_list = merged_data.get("business_line", [])
                        if not business_lines_list:
                            business_lines_list = ["unknown"]

                        # 特殊逻辑：将 "dream" 替换为 "dreamface"
                        business_lines_list = [
                            "dreamface" if bl == "dream" else bl
                            for bl in business_lines_list
                        ]

                        # 业务线过滤
                        if business_lines:
                            business_lines_list = [
                                bl for bl in business_lines_list if bl in business_lines
                            ]
                            if not business_lines_list:
                                continue

                        processed_count += 1

                        # 为每个业务线保存一份文件
                        for business_line in business_lines_list:
                            # 构建YAML数据（传入替换后的业务线）
                            yaml_data = self._build_yaml_data(merged_data, business_line)

                            # 添加文件路径信息
                            table_name = merged_data.get("en_name") or merged_data.get("name", f"table_{processed_count}")
                            filename = sanitize_filename(table_name)
                            yaml_data["_file_info"] = {
                                "filename": f"{filename}.yaml",
                                "business_line": business_line,
                                "category": "data_table",
                                "use_temp_dir": use_atomic_replace  # 标记是否使用临时目录
                            }

                            # 更新业务线统计
                            business_line_stats[business_line] = business_line_stats.get(business_line, 0) + 1
                            affected_business_lines.add(business_line)  # 记录受影响的业务线

                            # 保存文件
                            if not dry_run:
                                file_path = await self._save_single_file_async(yaml_data, use_atomic_replace)
                                if file_path:
                                    saved_files.append(file_path)
                                    saved_count += 1

                        if verbose and processed_count % 10 == 0:
                            logger.info(f"📊 已处理: {processed_count} 个表")

                    except Exception as e:
                        logger.error(f"处理表失败 (ID: {table_meta.get('id')}): {str(e)}")
                        continue

            # 原子性替换：将临时目录替换为正式目录
            if use_atomic_replace and not dry_run and affected_business_lines:
                logger.info("\n🔄 开始原子性替换目录...")
                replace_success_count = 0
                replace_fail_count = 0

                for business_line in sorted(affected_business_lines):
                    try:
                        success = self.file_manager.atomic_replace_category_dir(
                            business_line=business_line,
                            category="data_table"
                        )
                        if success:
                            replace_success_count += 1
                        else:
                            replace_fail_count += 1
                    except Exception as e:
                        logger.error(f"原子性替换失败 {business_line}/data_table: {e}")
                        replace_fail_count += 1

                logger.info(f"✅ 原子性替换完成: 成功 {replace_success_count} 个，失败 {replace_fail_count} 个")

                if replace_fail_count > 0:
                    logger.warning("部分业务线的原子性替换失败，请检查日志")

            # 显示最终统计
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            logger.info("\n" + "=" * 80)
            logger.info("✅ 数据表schema导出完成!")
            logger.info(f"📊 处理表: {processed_count} 个")
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
            logger.error(f"数据表schema导出过程异常: {str(e)}", exc_info=True)
            return False

        finally:
            await self.https_client.close()

    async def _get_table_list(self, table_type: str, query: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        获取表列表（通过HTTPS接口）

        Args:
            table_type: 表类型
            query: 查询关键字

        Returns:
            表列表
        """
        try:
            # 调用HTTPS接口获取表列表
            result = await self.https_client.get_table_list(
                query=query or "",
                table_type=table_type
            )

            # 调试:打印返回结果结构
            logger.debug(f"HTTPS返回结果类型: {type(result)}")
            logger.debug(f"HTTPS返回结果keys: {result.keys() if isinstance(result, dict) else 'N/A'}")

            # 检查响应状态
            if result.get("status_code") != 0:
                error_msg = result.get("status_msg", "Unknown error")
                logger.error(f"获取表列表失败: {error_msg}")
                return []

            # 从结果的data字段中提取表列表
            data = result.get("data", {})
            tables = self._extract_tables_from_tree(data)
            return tables

        except Exception as e:
            logger.error(f"获取表列表失败: {str(e)}")
            raise

    def _extract_tables_from_tree(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        从树结构中提取表列表

        树结构使用next字段表示子元素，通过type=table识别数据表

        Args:
            data: 树结构数据（来自HTTPS接口的data字段）

        Returns:
            表列表
        """
        tables = []

        def traverse(node: Any, path: str = "") -> None:
            """递归遍历树节点"""
            if not isinstance(node, dict):
                return

            # 判断是否为表节点
            node_type = node.get("type", "")
            if node_type == "table":
                # 提取表信息
                node_data = node.get("data", {})
                tables.append({
                    "id": node_data.get("id"),
                    "name": node_data.get("cn_name") or node_data.get("en_name") or node.get("name", ""),
                    "en_name": node_data.get("en_name", ""),
                    "cn_name": node_data.get("cn_name", ""),
                    "path": path,
                    "type": node_type,
                    "business_line": node_data.get("business_line", []),
                    "description": node_data.get("description") or node_data.get("extra_info", {}).get("description", ""),
                    # 保存表的元数据信息
                    "metadata": node_data
                })

            # 遍历子节点（next字段）
            next_nodes = node.get("next")
            if next_nodes:
                # 更新路径
                node_name = node.get("name", "")
                new_path = f"{path}/{node_name}" if path else node_name

                # next可能是列表或单个对象
                if isinstance(next_nodes, list):
                    for child in next_nodes:
                        traverse(child, new_path)
                elif isinstance(next_nodes, dict):
                    traverse(next_nodes, new_path)

        # 从root节点开始遍历
        root = data.get("root", {})
        if root:
            traverse(root)

        return tables

    async def _get_table_detail(self, table_id: str) -> Dict[str, Any]:
        """
        获取表详情（通过HTTPS接口）

        Args:
            table_id: 表ID

        Returns:
            表详情
        """
        try:
            # 调用HTTPS接口获取表详情
            result = await self.https_client.get_table_detail(table_id)

            # 检查响应状态
            if result.get("status_code") != 0:
                error_msg = result.get("status_msg", "Unknown error")
                logger.error(f"获取表详情失败 (ID: {table_id}): {error_msg}")
                return {}

            # 返回data字段
            return result.get("data", {})

        except Exception as e:
            logger.error(f"获取表详情失败 (ID: {table_id}): {str(e)}")
            raise

    def _merge_table_data(self, table_meta: Dict[str, Any], table_detail: Dict[str, Any]) -> Dict[str, Any]:
        """
        合并表元数据和详情

        Args:
            table_meta: 表元数据（从目录树获取）
            table_detail: 表详情（从HTTPS接口获取，已经是data字段）

        Returns:
            合并后的数据
        """
        # HTTPS接口直接返回的是data内容，不需要额外解析
        detail_data = table_detail

        # 合并数据，detail优先
        merged = {
            "id": detail_data.get("id") or table_meta.get("id"),
            "en_name": detail_data.get("en_name") or table_meta.get("en_name", ""),
            "cn_name": detail_data.get("cn_name") or table_meta.get("cn_name", ""),
            "standard_name": detail_data.get("standard_name", ""),
            "business_line": detail_data.get("business_line") or table_meta.get("business_line", []),
            "datasource_name": detail_data.get("datasource_name", ""),
            "db_name": detail_data.get("db_name", ""),
            "table_type": detail_data.get("table_type") or table_meta.get("type", ""),
            "lifecycle": detail_data.get("lifecycle"),
            "description": detail_data.get("extra_info", {}).get("description") or table_meta.get("description", ""),
            "path": table_meta.get("path", ""),
            "dir_id": detail_data.get("dir_id"),
            "primary_column_list": detail_data.get("primary_column_list", []),
            "partition_column_list": detail_data.get("partition_column_list", []),
            "column_list": detail_data.get("column_list", []),
            "extra_info": detail_data.get("extra_info", {}),
            "enable_tag": detail_data.get("enable_tag", True),
            "create_time": detail_data.get("create_time", ""),
            "update_time": detail_data.get("update_time"),
            "creator": detail_data.get("creator", ""),
            "modifier": detail_data.get("modifier"),
            "principal": detail_data.get("principal", ""),
            "uuid": detail_data.get("uuid", ""),
        }

        return merged

    def _build_yaml_data(self, table_data: Dict[str, Any], business_line: str) -> Dict[str, Any]:
        """
        构建YAML数据

        Args:
            table_data: 表数据
            business_line: 业务线

        Returns:
            YAML数据
        """
        import json

        # 处理 extra_info 字段：如果是字典且非空，转换为格式化的 JSON 字符串（标准格式，不含注释）
        extra_info = table_data.get("extra_info", {})
        if isinstance(extra_info, dict) and extra_info:
            # 移除 env 字段
            extra_info = extra_info.copy()
            extra_info.pop("env", None)
            # 格式化为带缩进的标准 JSON 字符串
            extra_info = json.dumps(extra_info, indent=2, ensure_ascii=False)
        elif not extra_info:
            # 如果为空，保持为空字典
            extra_info = {}

        # 处理 columns 字段：简化为只包含核心字段的列表，使用JSON格式（与bi_report保持一致）
        columns = table_data.get("column_list", [])

        if columns:
            # 简化每个字段，只保留核心信息（去掉order_no和data_format）
            simplified_columns = []
            for col in columns:
                simplified_col = {
                    "en_name": col.get("en_name", ""),
                    "cn_name": col.get("cn_name", ""),
                    "type": col.get("type", ""),
                    "sample_data": col.get("sample_data")
                }

                # 如果该列有字典信息，添加到字段中
                dict_info = col.get("dict")
                if dict_info and isinstance(dict_info, dict):
                    simplified_col["dict"] = dict_info

                simplified_columns.append(simplified_col)

            # 使用json.dumps格式化为多行JSON字符串
            json_str = json.dumps(simplified_columns, indent=2, ensure_ascii=False)
            # 使用特殊标记，后续处理时转换为literal block scalar
            columns_display = f"__LITERAL_BLOCK_START__\n{json_str}\n__LITERAL_BLOCK_END__"
        else:
            columns_display = "[]"

        # 处理 business_line：使用传入的 business_line 参数（已经过特殊逻辑处理）
        # 将单个业务线转换为列表格式
        business_line_list = [business_line] if business_line else table_data.get("business_line", [])

        # 按指定顺序返回字段
        yaml_data = {
            "id": table_data.get("id", ""),
            "en_name": table_data.get("en_name", ""),
            "cn_name": table_data.get("cn_name", ""),
            "db_name": table_data.get("db_name", ""),
            "business_line": business_line_list,
            "datasource_name": table_data.get("datasource_name", ""),
            "table_type": table_data.get("table_type", ""),
            "primary_column_list": table_data.get("primary_column_list", []),
            "partition_column_list": table_data.get("partition_column_list", []),
            "extra_info": extra_info,
            "columns": columns_display
        }

        # 添加字段注释
        yaml_data["_field_comments"] = {
            "en_name": "表名",
            "db_name": "数据库名称",
            "business_line": "归属业务线",
            "datasource_name": "表所在存储引擎",
            "primary_column_list": "主键字段",
            "partition_column_list": "分区字段",
            "extra_info": "扩展信息(description:表描述信息, foreign_condition:外表关联关系)",
            "columns": "表字段列表"
        }

        return yaml_data

    async def _save_single_file_async(self, data: Dict[str, Any], use_temp_dir: bool = False) -> Optional[str]:
        """
        异步保存单个文件

        Args:
            data: 表数据
            use_temp_dir: 是否使用临时目录（用于原子性替换）

        Returns:
            保存的文件路径，失败返回None
        """
        try:
            file_info = data.get("_file_info")
            if not file_info:
                return None

            filename = file_info["filename"]
            business_line = file_info["business_line"]
            category = file_info["category"]

            # 根据是否使用临时目录选择不同的路径生成方法
            if use_temp_dir:
                file_path = self.file_manager.generate_file_path_in_temp(filename, business_line, category)
            else:
                file_path = self.file_manager.generate_file_path(filename, business_line, category)

            # 在异步环境中保存文件
            loop = asyncio.get_event_loop()
            success = await loop.run_in_executor(
                None, self.file_manager.save_yaml_file, data, file_path
            )

            if success:
                return str(file_path)

        except Exception as e:
            logger.error(f"异步保存文件失败: {str(e)}")

        return None
