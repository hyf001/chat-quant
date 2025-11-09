#!/usr/bin/env python3
"""
金融指标视图表导出脚本

用法:
    python3 export_fin_views.py [--agent-type TYPE] [--domains D1,D2] [--page-size SIZE] [--dry-run] [--verbose]

示例:
    # 1. 导出所有金融指标视图表（默认：fin_data_analysis agent）
    python3 export_fin_views.py

    # 2. 仅导出指定domain的视图表（使用domain简称）
    python3 export_fin_views.py --domains stock,fund,macro

    # 3. 自定义每页大小（默认100）
    python3 export_fin_views.py --page-size 50

    # 4. 预览模式（不实际写入文件）
    python3 export_fin_views.py --dry-run

    # 5. 详细输出模式
    python3 export_fin_views.py --verbose

    # 6. 组合使用：导出股票和基金领域，详细输出
    python3 export_fin_views.py --domains stock,fund --verbose

支持的Domain简称:
    stock           - 股票领域
    zhaiquan        - 全量债券领域
    conbond         - 可转债领域
    thsinsurance    - 同花顺保险领域
    intusstock      - 国际美股领域
    fund            - 基金领域
    fundcompany     - 基金公司领域
    fundmanager     - 基金经理领域
    macro           - 宏观领域/宏观金融领域
    marketcalendar  - xx市场环境
    zhishu          - 全量指数领域
    threeboard      - 新三板领域
    options         - 期权领域
    futures         - 期货领域
    futures_product - 期货品种领域
    hkstock         - 港股领域
    usstock         - 美股领域
    bwmp            - 银行理财领域

环境配置:
    需要在.env文件中配置 FIN_VIEW_BASE_URL 环境变量：
    - 开发环境: FIN_VIEW_BASE_URL=https://indexmap.myhexin.com/bfe
    - 生产环境: FIN_VIEW_BASE_URL=http://cbas-babel-frontend-prod:10399/babel
    - 北美环境: FIN_VIEW_BASE_URL=http://cbas-babel-frondend-beimeipri:10399/babel

输出目录:
    ./cache/fin_data_analysis/{domain_short}/
    例如：./cache/fin_data_analysis/stock/*.yaml
"""
import sys
import asyncio
import logging
import argparse
from pathlib import Path

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
from app.services.project.cache_manager.exporters.fin_view_exporter import FinViewExporter
from app.services.project.cache_manager.config.constants import get_agent_type_config


def setup_logging(verbose: bool = False):
    """设置日志"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


async def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='导出金融指标视图表到本地YAML文件',
        epilog='更多信息请参考脚本顶部的使用示例'
    )
    parser.add_argument(
        '--agent-type',
        default='fin_data_analysis',
        help='智能体类型（默认：fin_data_analysis）'
    )
    parser.add_argument(
        '--domains',
        help='Domain过滤，多个用逗号分隔（使用简称，如：stock,fund,macro）'
    )
    parser.add_argument(
        '--page-size',
        type=int,
        default=100,
        help='每页大小（默认：100）'
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

    args = parser.parse_args()

    # 设置日志
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)

    try:
        # 验证智能体类型
        try:
            agent_type_config = get_agent_type_config(args.agent_type)
            logger.info(f"智能体类型: {args.agent_type} - {agent_type_config['description']}")
        except ValueError:
            logger.warning(f"智能体类型 {args.agent_type} 未在constants中定义，继续执行")

        # 解析domain过滤
        domains = None
        if args.domains:
            domains = [d.strip() for d in args.domains.split(',')]
            logger.info(f"Domain过滤: {domains}")

        # 初始化配置管理器
        config = ConfigManager()

        # 验证配置
        is_valid, error_msg = config.validate_config()
        if not is_valid:
            logger.error(f"配置验证失败: {error_msg}")
            sys.exit(1)

        # 验证 FIN_VIEW_BASE_URL 环境变量
        import os
        fin_view_base_url = os.getenv('FIN_VIEW_BASE_URL')
        if not fin_view_base_url:
            logger.error("环境变量 FIN_VIEW_BASE_URL 未配置，请在.env文件中配置")
            logger.error("示例：FIN_VIEW_BASE_URL=https://indexmap.myhexin.com/bfe")
            sys.exit(1)
        logger.info(f"FIN_VIEW_BASE_URL: {fin_view_base_url}")

        # 初始化金融视图表导出器
        exporter = FinViewExporter(config, args.agent_type)

        # 执行导出
        success = await exporter.export(
            domains=domains,
            dry_run=args.dry_run,
            verbose=args.verbose,
            page_size=args.page_size
        )

        if success:
            logger.info("✅ 导出任务完成")
            sys.exit(0)
        else:
            logger.error("❌ 导出任务失败")
            sys.exit(1)

    except KeyboardInterrupt:
        logger.info("用户中断导出")
        sys.exit(130)
    except Exception as e:
        logger.error(f"导出过程发生异常: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
