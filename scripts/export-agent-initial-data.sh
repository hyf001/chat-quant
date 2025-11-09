#!/usr/bin/env bash

# ============================================================================
# 智能体初始化数据导出脚本
#
# 说明: 从MCP服务导出智能体初始化所需的数据到本地缓存
#      使用项目虚拟环境调用 export_agent_data.py 脚本
# 作者: Auto-generated
# 日期: 2025-10-14
# ============================================================================

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Python命令（开发环境使用本地python3，Docker环境使用系统python）
# 检测是否在Docker环境中（通过检查/.dockerenv文件或DOCKER_ENV环境变量）
if [ -f "/.dockerenv" ] || [ -n "$DOCKER_ENV" ]; then
    # Docker环境使用系统Python
    PYTHON_CMD="python"
else
    # 本地开发环境使用python3
    PYTHON_CMD="python3"
fi

# 导出脚本路径
EXPORT_SCRIPT="$PROJECT_ROOT/apps/api/app/services/project/cache_manager/scripts/export_agent_data.py"

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# 显示帮助信息
show_help() {
    cat << EOF
${GREEN}智能体初始化数据导出工具${NC}

${BLUE}用法:${NC}
    $0 [OPTIONS]

${BLUE}选项:${NC}
    --agent-type TYPE          智能体类型 (必需)
                              可选值: data_analysis, fin_data_analysis
    --business-lines LINES     业务线过滤，多个用逗号分隔 (可选，仅适用于data_analysis)
                              示例: iwc,cot
    --domains DOMAINS         Domain过滤，多个用逗号分隔 (可选，仅适用于fin_data_analysis)
                              示例: stock,fund,macro
    --query KEYWORD           查询关键字 (可选，仅适用于data_analysis)
    --batch-size SIZE         批处理大小 (可选，适用于data_analysis)
    --page-size SIZE          每页大小 (可选，仅适用于fin_data_analysis，默认100)
    --dry-run                 预览模式，不实际写入文件 (可选)
    --verbose                 详细输出 (可选)
    -h, --help                显示此帮助信息

${BLUE}智能体类型说明:${NC}
    data_analysis      - 数据分析智能体 (初始化数据: 数据表、BI报表)
    fin_data_analysis  - 金融数据分析智能体 (初始化数据: 金融指标视图表)

${BLUE}示例:${NC}
    # 导出数据分析智能体的初始化数据
    $0 --agent-type data_analysis

    # 导出数据分析智能体的iwc业务线初始化数据
    $0 --agent-type data_analysis --business-lines iwc

    # 导出金融数据分析智能体的所有视图表
    $0 --agent-type fin_data_analysis

    # 导出金融数据分析智能体的指定领域视图表
    $0 --agent-type fin_data_analysis --domains stock,fund,macro

    # 预览模式（不实际写入文件）
    $0 --agent-type data_analysis --dry-run

    # 详细输出
    $0 --agent-type data_analysis --verbose

    # 查询特定关键字的表
    $0 --agent-type data_analysis --query dwd_iwc --verbose

${BLUE}注意事项:${NC}
    - 脚本会自动选择Python环境（本地开发环境使用python3，Docker中使用系统python）
    - 初始化数据保存在: data/projects/cache/<agent_type>/
    - 智能体启动时会自动加载这些缓存数据
    - 首次运行请确保已配置 .env 文件中的相关配置

EOF
}

# 检查Python环境
check_python() {
    # 检查Python命令是否可用
    if ! command -v $PYTHON_CMD &> /dev/null; then
        print_error "Python未安装或不在PATH中"
        exit 1
    fi

    # 打印Python环境信息
    if [ "$PYTHON_CMD" = "python3" ]; then
        print_info "使用本地Python3: $(which python3)"
    else
        print_info "使用系统Python (Docker环境)"
    fi
}

# 检查导出脚本
check_export_script() {
    if [ ! -f "$EXPORT_SCRIPT" ]; then
        print_error "导出脚本不存在: $EXPORT_SCRIPT"
        exit 1
    fi
}

# 主函数
main() {
    print_info "项目根目录: $PROJECT_ROOT"
    print_info "Python命令: $PYTHON_CMD"
    print_info "导出脚本: $EXPORT_SCRIPT"
    echo ""

    # 检查环境
    check_python
    check_export_script

    # 如果没有参数或者包含 -h/--help，显示帮助
    if [ $# -eq 0 ] || [[ "$*" =~ "-h" ]] || [[ "$*" =~ "--help" ]]; then
        show_help
        exit 0
    fi

    # 构建命令
    CMD="$PYTHON_CMD $EXPORT_SCRIPT"

    # 添加所有参数
    for arg in "$@"; do
        CMD="$CMD $arg"
    done

    print_info "执行命令: $CMD"
    echo ""
    echo "========================================================================"
    echo ""

    # 执行命令
    eval "$CMD"
    EXIT_CODE=$?

    echo ""
    echo "========================================================================"

    if [ $EXIT_CODE -eq 0 ]; then
        print_success "初始化数据导出完成！"
    else
        print_error "初始化数据导出失败，退出码: $EXIT_CODE"
        exit $EXIT_CODE
    fi
}

# 运行主函数
main "$@"
