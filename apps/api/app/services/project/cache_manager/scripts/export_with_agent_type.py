#!/usr/bin/env python3
"""
智能体类型级别导出脚本

根据智能体类型自动导出该类型下所有相关的数据资源。

用法:
    apps/api/.venv/bin/python export_with_agent_type.py [--agent-type TYPE] [--business-lines BL1,BL2] [--dry-run] [--verbose]

示例:
    # 导出data_analysis智能体类型的所有数据（数据表 + BI报表）
    apps/api/.venv/bin/python export_with_agent_type.py --agent-type data_analysis

    # 导出data_develop智能体类型的所有数据（数据源 + 传输任务）
    apps/api/.venv/bin/python export_with_agent_type.py --agent-type data_develop

    # 仅导出iwc业务线的所有数据
    apps/api/.venv/bin/python export_with_agent_type.py --agent-type data_analysis --business-lines iwc

    # 预览模式（不实际写入文件）
    apps/api/.venv/bin/python export_with_agent_type.py --agent-type data_analysis --dry-run

    # 详细输出
    apps/api/.venv/bin/python export_with_agent_type.py --agent-type data_analysis --verbose
"""
import sys
import asyncio
import logging
import argparse
from pathlib import Path
from typing import List, Optional

# 动态查找并添加apps/api目录到sys.path
def find_api_root():
    """向上查找apps/api目录"""
    current = Path(__file__).resolve().parent
    while current.parent != current:  # 防止到达根目录
        # 检查是否是api目录（包含app子目录）
        if (current / "app").exists() and (current / "app").is_dir():
            # 验证这是正确的api目录（包含cache_manager）
            if (current / "app" / "services" / "project" / "cache_manager").exists():
                return current
        current = current.parent
    raise RuntimeError("无法找到apps/api目录，请确保脚本在正确的项目结构中运行")

sys.path.insert(0, str(find_api_root()))

from app.services.project.cache_manager.config.config_manager import ConfigManager
from app.services.project.cache_manager.config.constants import get_agent_type_config
from app.services.project.cache_manager.exporters.data_table_exporter import DataTableExporter
from app.services.project.cache_manager.exporters.report_exporter import ReportExporter
from app.services.project.cache_manager.exporters.datasource_exporter import DataSourceExporter
from app.services.project.cache_manager.exporters.transmission_task_exporter import TransmissionTaskExporter


def setup_logging(verbose: bool = False):
    """设置日志"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


async def export_data_analysis(
    config: ConfigManager,
    agent_type: str,
    business_lines: Optional[List[str]] = None,
    dry_run: bool = False,
    verbose: bool = False,
    query: Optional[str] = None,
    batch_size: int = 10
) -> bool:
    """
    导出数据分析智能体类型的所有数据

    包括：
    - 数据表（PHYSICAL）
    - BI报表（REPORT）

    Args:
        config: 配置管理器
        agent_type: 智能体类型
        business_lines: 业务线过滤
        dry_run: 是否预览模式
        verbose: 是否详细输出
        query: 查询关键字
        batch_size: 批处理大小

    Returns:
        是否全部成功
    """
    logger = logging.getLogger(__name__)
    logger.info("=" * 80)
    logger.info("开始导出数据分析智能体类型数据")
    logger.info("=" * 80)

    all_success = True

    # 1. 导出数据表（PHYSICAL）
    logger.info("\n📊 [1/2] 导出数据表...")
    logger.info("-" * 80)
    try:
        table_exporter = DataTableExporter(config, agent_type)
        success = await table_exporter.export(
            business_lines=business_lines,
            dry_run=dry_run,
            verbose=verbose,
            table_type='PHYSICAL',
            query=query,
            batch_size=batch_size
        )
        if not success:
            logger.error("❌ 数据表导出失败")
            all_success = False
        else:
            logger.info("✅ 数据表导出完成")
    except Exception as e:
        logger.error(f"❌ 数据表导出异常: {str(e)}", exc_info=True)
        all_success = False

    # 2. 导出BI报表（REPORT）
    logger.info("\n📈 [2/2] 导出BI报表...")
    logger.info("-" * 80)
    try:
        report_exporter = ReportExporter(config, agent_type)
        success = await report_exporter.export(
            business_lines=business_lines,
            dry_run=dry_run,
            verbose=verbose,
            query=query
        )
        if not success:
            logger.error("❌ BI报表导出失败")
            all_success = False
        else:
            logger.info("✅ BI报表导出完成")
    except Exception as e:
        logger.error(f"❌ BI报表导出异常: {str(e)}", exc_info=True)
        all_success = False

    return all_success


async def export_data_develop(
    config: ConfigManager,
    agent_type: str,
    business_lines: Optional[List[str]] = None,
    dry_run: bool = False,
    verbose: bool = False,
    batch_size: int = 50
) -> bool:
    """
    导出数据开发智能体类型的所有数据

    包括：
    - 数据源
    - 传输任务

    Args:
        config: 配置管理器
        agent_type: 智能体类型
        business_lines: 业务线过滤
        dry_run: 是否预览模式
        verbose: 是否详细输出
        batch_size: 批处理大小

    Returns:
        是否全部成功
    """
    logger = logging.getLogger(__name__)
    logger.info("=" * 80)
    logger.info("开始导出数据开发智能体类型数据")
    logger.info("=" * 80)

    all_success = True

    # 1. 导出数据源
    logger.info("\n🔌 [1/2] 导出数据源...")
    logger.info("-" * 80)
    try:
        datasource_exporter = DataSourceExporter(config, agent_type)
        success = await datasource_exporter.export(
            business_lines=business_lines,
            dry_run=dry_run,
            verbose=verbose,
            batch_size=batch_size
        )
        if not success:
            logger.error("❌ 数据源导出失败")
            all_success = False
        else:
            logger.info("✅ 数据源导出完成")
    except Exception as e:
        logger.error(f"❌ 数据源导出异常: {str(e)}", exc_info=True)
        all_success = False

    # 2. 导出传输任务
    logger.info("\n🔄 [2/2] 导出传输任务...")
    logger.info("-" * 80)
    try:
        task_exporter = TransmissionTaskExporter(config, agent_type)
        success = await task_exporter.export(
            business_lines=business_lines,
            dry_run=dry_run,
            verbose=verbose,
            batch_size=batch_size
        )
        if not success:
            logger.error("❌ 传输任务导出失败")
            all_success = False
        else:
            logger.info("✅ 传输任务导出完成")
    except Exception as e:
        logger.error(f"❌ 传输任务导出异常: {str(e)}", exc_info=True)
        all_success = False

    return all_success


async def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='导出指定智能体类型的所有MCP数据到本地YAML文件',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
智能体类型说明:
  data_analysis  - 数据分析智能体（包含：数据表、BI报表）
  data_develop   - 数据开发智能体（包含：数据源、传输任务）

示例:
  # 导出数据分析智能体的所有数据
  %(prog)s --agent-type data_analysis

  # 导出数据开发智能体的iwc业务线数据
  %(prog)s --agent-type data_develop --business-lines iwc

  # 预览模式
  %(prog)s --agent-type data_analysis --dry-run
        """
    )
    parser.add_argument(
        '--agent-type',
        required=True,
        choices=['data_analysis', 'data_develop'],
        help='智能体类型'
    )
    parser.add_argument(
        '--business-lines',
        help='业务线过滤，多个用逗号分隔（如：iwc,cot）'
    )
    parser.add_argument(
        '--query',
        help='查询关键字（仅适用于data_analysis智能体类型）'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='预览模式，不实际写入文件'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='详细输出'
    )
    parser.add_argument(
        '--batch-size',
        type=int,
        help='批处理大小（data_analysis默认10，data_develop默认50）'
    )

    args = parser.parse_args()

    # 设置日志
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)

    try:
        # 验证智能体类型
        agent_type_config = get_agent_type_config(args.agent_type)

        logger.info(f"\n{'=' * 80}")
        logger.info(f"智能体类型: {args.agent_type}")
        logger.info(f"描述: {agent_type_config['description']}")
        logger.info(f"包含数据类型: {', '.join(agent_type_config['data_types'])}")
        logger.info(f"{'=' * 80}\n")

        # 解析业务线过滤
        business_lines = None
        if args.business_lines:
            business_lines = [bl.strip() for bl in args.business_lines.split(',')]
            logger.info(f"业务线过滤: {', '.join(business_lines)}\n")

        # 初始化配置管理器
        config = ConfigManager()

        # 验证配置
        is_valid, error_msg = config.validate_config()
        if not is_valid:
            logger.error(f"配置验证失败: {error_msg}")
            sys.exit(1)

        # 根据智能体类型执行不同的导出逻辑
        success = False

        if args.agent_type == 'data_analysis':
            # 确定批处理大小
            batch_size = args.batch_size if args.batch_size is not None else 10

            success = await export_data_analysis(
                config=config,
                agent_type=args.agent_type,
                business_lines=business_lines,
                dry_run=args.dry_run,
                verbose=args.verbose,
                query=args.query,
                batch_size=batch_size
            )
        elif args.agent_type == 'data_develop':
            # query参数对data_develop无效
            if args.query:
                logger.warning("⚠️  --query 参数对 data_develop 智能体类型无效，将被忽略")

            # 确定批处理大小
            batch_size = args.batch_size if args.batch_size is not None else 50

            success = await export_data_develop(
                config=config,
                agent_type=args.agent_type,
                business_lines=business_lines,
                dry_run=args.dry_run,
                verbose=args.verbose,
                batch_size=batch_size
            )

        # 输出最终结果
        logger.info("\n" + "=" * 80)
        if success:
            logger.info("✅ 智能体类型数据导出任务全部完成")
            logger.info("=" * 80)
            sys.exit(0)
        else:
            logger.error("❌ 部分导出任务失败，请检查上述错误信息")
            logger.info("=" * 80)
            sys.exit(1)

    except KeyboardInterrupt:
        logger.info("\n用户中断导出")
        sys.exit(130)
    except Exception as e:
        logger.error(f"\n导出过程发生异常: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
