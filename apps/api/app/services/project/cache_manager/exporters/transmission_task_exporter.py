"""
TransmissionTask Exporter - 传输任务导出器
"""
import asyncio
import logging
from datetime import datetime
from typing import List, Optional, Dict, Any, Callable
from pathlib import Path

from .base_exporter import BaseExporter
from ..client.base_mcp_client import BaseMCPClient
from ..config.config_manager import ConfigManager
from ..config.constants import get_mcp_tool_config
from ..utils.file_manager import FileManager
from ..utils.data_processor import (
    build_transmission_task_yaml_data,
    sanitize_filename
)
from ..utils.business_line import extract_business_line

logger = logging.getLogger(__name__)


class TransmissionTaskExporter(BaseExporter):
    """传输任务导出器"""

    def __init__(self, config: ConfigManager, agent_type: str = "data_analysis"):
        """
        初始化传输任务导出器

        Args:
            config: 配置管理器
            agent_type: 智能体类型
        """
        super().__init__(config, agent_type)

        # 初始化文件管理器
        self.file_manager = FileManager(str(self.output_dir))

        # 获取MCP工具配置
        tool_config = get_mcp_tool_config("transmission_task_list")
        service_name = tool_config["service_name"]
        self.tool_function = tool_config["function"]  # 保存完整的工具名称

        # 初始化MCP客户端
        base_url = config.get_mcp_url(service_name)
        self.mcp_client = BaseMCPClient(
            email=config.get("default_email"),
            tenant_id=config.get("tenant_id"),
            base_url=base_url
        )

    async def export(self,
                    business_lines: Optional[List[str]] = None,
                    dry_run: bool = False,
                    verbose: bool = False,
                    batch_size: int = 50) -> bool:
        """
        导出传输任务

        Args:
            business_lines: 业务线过滤
            dry_run: 是否为预览模式
            verbose: 是否详细输出
            batch_size: 批处理大小

        Returns:
            是否成功
        """
        start_time = datetime.now()

        try:
            logger.info("🚀 开始导出传输任务...")

            if dry_run:
                logger.info("📋 预览模式 - 不会实际写入文件")

            # 初始化统计信息
            processed_count = 0
            saved_count = 0
            business_line_stats = {}
            saved_files = []
            current_batch = []

            # 进度回调
            def update_progress(count: int, name: str):
                nonlocal processed_count
                processed_count = count
                if verbose and (count % 10 == 0 or count <= 5):
                    logger.info(f"📊 已处理: {count} 个传输任务，当前: {name}")

            # 流式处理传输任务
            async for task in self._stream_transmission_task_list(update_progress):
                try:
                    # 业务线过滤
                    business_line = extract_business_line(task.get("business_segment", ""))
                    if business_lines and business_line not in business_lines:
                        continue

                    # 构建YAML数据
                    export_time = datetime.now().isoformat()
                    yaml_data = build_transmission_task_yaml_data(
                        task=task,
                        business_line=business_line,
                        export_time=export_time,
                        mcp_tool="mcp__hexin-cbas-data-transmission-mcp__transmission_task_list"
                    )

                    # 添加文件路径信息
                    filename = sanitize_filename(task.get("name", f"task_{processed_count}"))
                    yaml_data["_file_info"] = {
                        "filename": f"{filename}.yaml",
                        "business_line": business_line,
                        "category": "transmission_task"
                    }

                    # 更新业务线统计
                    business_line_stats[business_line] = business_line_stats.get(business_line, 0) + 1

                    # 添加到当前批次
                    current_batch.append(yaml_data)

                    # 批量处理
                    if len(current_batch) >= batch_size:
                        if not dry_run:
                            batch_saved = await self._save_batch_async(current_batch)
                            saved_files.extend(batch_saved)
                            saved_count += len(batch_saved)

                        current_batch.clear()

                        if verbose:
                            logger.info(f"💾 已保存批次，累计: {saved_count} 个文件")

                except Exception as e:
                    logger.error(f"处理传输任务失败: {str(e)}")
                    continue

            # 处理剩余的批次
            if current_batch:
                if not dry_run:
                    batch_saved = await self._save_batch_async(current_batch)
                    saved_files.extend(batch_saved)
                    saved_count += len(batch_saved)

            # 显示最终统计
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            logger.info("✅ 传输任务导出完成!")
            logger.info(f"📊 处理传输任务: {processed_count} 个")
            logger.info(f"💾 保存文件: {saved_count} 个")
            logger.info(f"📂 输出目录: {self.output_dir}")
            logger.info(f"⏱️  耗时: {duration:.2f} 秒")

            if verbose and business_line_stats:
                logger.info("📁 业务线分布:")
                for bl, count in sorted(business_line_stats.items()):
                    logger.info(f"  - {bl}: {count} 个")

            return True

        except Exception as e:
            logger.error(f"传输任务导出过程异常: {str(e)}")
            return False

        finally:
            await self.mcp_client.close()

    async def _stream_transmission_task_list(self,
                                           progress_callback: Optional[Callable[[int, str], None]] = None):
        """
        流式获取传输任务列表

        Args:
            progress_callback: 进度回调函数

        Yields:
            处理后的传输任务信息
        """
        # 构造传输任务列表的MCP调用参数
        arguments = {
            "CBAS_EMAIL": self.config.get("default_email"),
            "x-data-portal-tenant-id": self.config.get("tenant_id")
        }

        processed_count = 0

        def internal_progress_callback(data_item: Dict[str, Any]):
            nonlocal processed_count
            processed_count += 1

            task_name = data_item.get("name", f"task_{processed_count}")

            if progress_callback:
                progress_callback(processed_count, task_name)

        # 使用基类的流式调用方法（使用完整的工具名称）
        async for task in self.mcp_client.stream_mcp_tool(
            self.tool_function,
            arguments,
            internal_progress_callback
        ):
            yield task

    async def _save_batch_async(self, batch_data: List[Dict[str, Any]]) -> List[str]:
        """
        异步批量保存文件

        Args:
            batch_data: 批量数据

        Returns:
            保存的文件路径列表
        """
        saved_files = []

        # 使用异步任务并发保存文件
        tasks = []
        for data in batch_data:
            task = self._save_single_file_async(data)
            tasks.append(task)

        # 等待所有任务完成
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in results:
            if isinstance(result, str):  # 成功保存的文件路径
                saved_files.append(result)
            elif isinstance(result, Exception):
                logger.error(f"保存文件失败: {str(result)}")

        return saved_files

    async def _save_single_file_async(self, data: Dict[str, Any]) -> Optional[str]:
        """
        异步保存单个文件

        Args:
            data: 传输任务数据

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
