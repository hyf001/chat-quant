"""
FinView Exporter - 金融指标视图表导出器
"""
import asyncio
import logging
import os
from datetime import datetime
from typing import List, Optional, Dict, Any
from pathlib import Path

from .base_exporter import BaseExporter
from ..client.fin_view_https_client import FinViewHttpsClient
from ..config.config_manager import ConfigManager
from ..utils.file_manager import FileManager
from ..utils.data_processor import sanitize_filename

logger = logging.getLogger(__name__)


class FinViewExporter(BaseExporter):
    """金融指标视图表导出器"""

    # Domain映射：原始domain -> 简称
    DOMAIN_MAPPING = {
        "abs_股票领域": "stock",
        "abs_全量债券领域": "zhaiquan",
        "abs_可转债领域": "conbond",
        "abs_同花顺保险领域": "thsinsurance",
        "abs_国际美股领域": "intusstock",
        "abs_基金领域": "fund",
        "abs_基金公司领域": "fundcompany",
        "abs_基金经理领域": "fundmanager",
        "abs_宏观领域": "macro",
        "abs_宏观金融领域": "macro",
        "abs_市场环境": "marketcalendar",
        "abs_全量指数领域": "zhishu",
        "abs_新三板领域": "threeboard",
        "abs_期权领域": "options",
        "abs_期货领域": "futures",
        "abs_期货品种领域": "futures_product",
        "abs_港股领域": "hkstock",
        "abs_美股领域": "usstock",
        "abs_银行理财领域": "bwmp",
    }

    def __init__(self, config: ConfigManager, agent_type: str = "fin_data_analysis"):
        """
        初始化金融指标视图表导出器

        Args:
            config: 配置管理器
            agent_type: 智能体类型（固定为 fin_data_analysis）
        """
        super().__init__(config, agent_type)

        # 初始化文件管理器
        self.file_manager = FileManager(str(self.output_dir))

        # 初始化FinView HTTP客户端
        self.https_client = FinViewHttpsClient()

    async def export(self,
                    domains: Optional[List[str]] = None,
                    dry_run: bool = False,
                    verbose: bool = False,
                    page_size: int = 100,
                    use_atomic_replace: bool = True) -> bool:
        """
        导出金融指标视图表

        Args:
            domains: Domain过滤（简称列表，如 ["stock", "fund"]）
            dry_run: 是否为预览模式
            verbose: 是否详细输出
            page_size: 每页大小
            use_atomic_replace: 是否使用原子性替换（默认True）

        Returns:
            是否成功
        """
        start_time = datetime.now()

        try:
            logger.info("🚀 开始导出金融指标视图表...")

            if dry_run:
                logger.info("📋 预览模式 - 不会实际写入文件")

            if use_atomic_replace and not dry_run:
                logger.info("🔄 使用原子性替换模式（先写入临时目录，完成后原子性替换）")

            # 初始化统计信息
            processed_count = 0
            saved_count = 0
            domain_stats = {}
            saved_files = []
            affected_domains = set()  # 记录受影响的domain

            # 分页获取视图表列表
            page = 1
            total_items = None

            while True:
                if verbose or page == 1:
                    logger.info(f"📡 正在获取视图表列表（第{page}页）...")

                # 获取当前页数据
                result = await self._get_view_table_list(page, page_size)

                # 检查响应状态
                if result.get("status_code") == -1:
                    logger.error(f"获取视图表列表失败: {result.get('status_msg')}")
                    break

                # 提取数据
                # result结构可能是：
                # 1. list格式: {"status_code": 0, "data": [...], "total": -1}
                # 2. dict格式: {"status_code": 0, "data": {"items": [...], "total": 100}}
                data = result.get("data", {})
                result_total = result.get("total", 0)  # 获取外层的total字段

                # 调试输出：检查data类型
                if verbose:
                    logger.debug(f"data类型: {type(data)}, result.total={result_total}")

                # 处理data可能是list的情况
                if isinstance(data, list):
                    items = data
                    # 如果外层有total字段，优先使用外层的total
                    total = result_total if result_total != 0 else len(data)
                elif isinstance(data, dict):
                    items = data.get("items", [])
                    # dict格式优先使用内层的total
                    total = data.get("total", result_total)
                else:
                    logger.error(f"未知的data格式: {type(data)}")
                    break

                if total_items is None:
                    if total == -1:
                        logger.info(f"📊 API未返回总数，将持续分页直到无数据")
                        total_items = -1
                    else:
                        total_items = total
                        logger.info(f"📊 共有 {total_items} 个视图表需要处理")

                if not items:
                    logger.info(f"📄 第{page}页无数据，导出完成")
                    break

                # 处理当前页的视图表
                for item in items:
                    try:
                        # 提取domain和tableName
                        domain = item.get("domain", "")
                        table_name = item.get("tableName", "")

                        if not table_name:
                            logger.warning(f"视图表缺少tableName字段，跳过: {item}")
                            continue

                        # 映射domain到简称
                        domain_short = self.DOMAIN_MAPPING.get(domain, None)

                        if not domain_short:
                            if verbose:
                                logger.warning(f"未知的domain: {domain}，使用'unknown'")
                            domain_short = "unknown"

                        # Domain过滤
                        if domains and domain_short not in domains:
                            continue

                        processed_count += 1

                        # 构建YAML数据
                        yaml_data = self._build_yaml_data(item, domain_short)

                        # 添加文件路径信息
                        filename = sanitize_filename(table_name)
                        yaml_data["_file_info"] = {
                            "filename": f"{filename}.yaml",
                            "business_line": domain_short,  # 使用domain_short作为业务线
                            "category": None,  # fin_data_analysis类型不使用category子目录
                            "use_temp_dir": use_atomic_replace
                        }

                        # 更新domain统计
                        domain_stats[domain_short] = domain_stats.get(domain_short, 0) + 1
                        affected_domains.add(domain_short)

                        # 保存文件
                        if not dry_run:
                            file_path = await self._save_single_file_async(yaml_data, use_atomic_replace)
                            if file_path:
                                saved_files.append(file_path)
                                saved_count += 1

                        if verbose and processed_count % 50 == 0:
                            logger.info(f"📊 已处理: {processed_count} 个视图表")

                    except Exception as e:
                        logger.error(f"处理视图表失败: {item.get('tableName', 'unknown')}, 错误: {str(e)}")
                        continue

                # 检查是否还有下一页
                # 如果total=-1（未知总数），则继续请求下一页，直到返回空数组
                # 如果total已知，则检查是否已处理完所有数据
                if total_items != -1 and processed_count >= total_items:
                    logger.info(f"✅ 已处理所有 {processed_count} 个视图表")
                    break

                page += 1

            # 原子性替换：将临时目录替换为正式目录
            if use_atomic_replace and not dry_run and affected_domains:
                logger.info("\n🔄 开始原子性替换目录...")
                replace_success_count = 0
                replace_fail_count = 0

                for domain_short in sorted(affected_domains):
                    try:
                        success = self.file_manager.atomic_replace_category_dir(
                            business_line=domain_short,
                            category=None  # fin_data_analysis类型不使用category子目录
                        )
                        if success:
                            replace_success_count += 1
                        else:
                            replace_fail_count += 1
                    except Exception as e:
                        logger.error(f"原子性替换失败 {domain_short}/fin_view: {e}")
                        replace_fail_count += 1

                logger.info(f"✅ 原子性替换完成: 成功 {replace_success_count} 个，失败 {replace_fail_count} 个")

                if replace_fail_count > 0:
                    logger.warning("部分domain的原子性替换失败，请检查日志")

            # 显示最终统计
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            logger.info("\n" + "=" * 80)
            logger.info("✅ 金融指标视图表导出完成!")
            logger.info(f"📊 处理视图表: {processed_count} 个")
            logger.info(f"💾 保存文件: {saved_count} 个")
            logger.info(f"📂 输出目录: {self.output_dir}")
            logger.info(f"⏱️  耗时: {duration:.2f} 秒")

            if verbose and domain_stats:
                logger.info("\n📁 Domain分布:")
                for domain_short, count in sorted(domain_stats.items()):
                    logger.info(f"  - {domain_short}: {count} 个")

            logger.info("=" * 80)
            return True

        except Exception as e:
            logger.error(f"金融指标视图表导出过程异常: {str(e)}", exc_info=True)
            return False

        finally:
            await self.https_client.close()

    async def _get_view_table_list(self, page: int, page_size: int) -> Dict[str, Any]:
        """
        获取视图表列表

        Args:
            page: 页码
            page_size: 每页大小

        Returns:
            视图表列表
        """
        try:
            result = await self.https_client.get_view_table_list(page, page_size)
            return result
        except Exception as e:
            logger.error(f"获取视图表列表失败: {str(e)}")
            raise

    def _build_yaml_data(self, item: Dict[str, Any], domain_short: str) -> Dict[str, Any]:
        """
        构建YAML数据

        Args:
            item: 视图表数据
            domain_short: Domain简称

        Returns:
            YAML数据
        """
        import json

        # 提取基础字段
        table_name = item.get("tableName", "")
        domain = item.get("domain", "")

        # 提取字段列表（如果有）
        columns = item.get("columns", [])

        # 如果columns是字符串，尝试解析为JSON
        if isinstance(columns, str):
            try:
                columns = json.loads(columns)
            except:
                columns = []

        # 格式化columns为JSON字符串（保留原始字段，不做简化处理）
        if columns and isinstance(columns, list):
            # 使用json.dumps格式化为多行JSON字符串，保留API返回的所有字段
            json_str = json.dumps(columns, indent=2, ensure_ascii=False)
            # 使用特殊标记，后续处理时转换为literal block scalar
            columns_display = f"__LITERAL_BLOCK_START__\n{json_str}\n__LITERAL_BLOCK_END__"
        else:
            columns_display = "[]"

        # 构建YAML数据（保留API返回的所有字段）
        # 先添加tableId（如果存在）
        yaml_data = {}
        if "tableId" in item:
            yaml_data["tableId"] = item["tableId"]

        # 再添加tableName和domain
        yaml_data["tableName"] = table_name
        yaml_data["domain"] = domain

        # 添加其他字段（排除已处理的字段）
        for key, value in item.items():
            if key not in ["tableId", "tableName", "domain", "columns"]:
                yaml_data[key] = value

        # 最后添加columns字段
        yaml_data["columns"] = columns_display

        # 添加字段注释
        yaml_data["_field_comments"] = {
            "tableId": "视图表ID",
            "tableName": "视图表名称",
            "domain": "所属领域",
            "columns": "字段列表"
        }

        return yaml_data

    async def _save_single_file_async(self, data: Dict[str, Any], use_temp_dir: bool = False) -> Optional[str]:
        """
        异步保存单个文件

        Args:
            data: 视图表数据
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
