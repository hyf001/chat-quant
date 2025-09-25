"""
错误处理工具模块
"""

import logging
import traceback
from functools import wraps
from typing import Callable, Any, Dict
from langchain_core.messages import AIMessage


# 设置日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def handle_node_errors(func: Callable) -> Callable:
    """节点错误处理装饰器"""

    @wraps(func)
    def wrapper(*args, **kwargs) -> Dict[str, Any]:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Node {func.__name__} failed: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")

            # 返回错误状态
            error_message = AIMessage(
                content=f"抱歉，在执行 {func.__name__} 时遇到错误: {str(e)}\n请稍后重试或联系技术支持。"
            )

            return {
                "messages": [error_message],
                "workflow_step": "error",
                "error_info": {
                    "node": func.__name__,
                    "error": str(e),
                    "timestamp": str(logger.handlers[0].formatter.formatTime(logger.makeRecord(
                        logger.name, logging.ERROR, "", 0, "", (), None
                    )))
                }
            }

    return wrapper


def handle_agent_errors(func: Callable) -> Callable:
    """Agent错误处理装饰器"""

    @wraps(func)
    def wrapper(*args, **kwargs) -> Dict[str, Any]:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Agent {func.__name__} failed: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")

            # 返回错误状态
            error_message = AIMessage(
                content=f"Agent执行失败: {str(e)}\n正在尝试使用备用处理方式..."
            )

            return {
                "messages": [error_message],
                "workflow_step": "error_recovery",
                "error_info": {
                    "agent": func.__name__,
                    "error": str(e)
                }
            }

    return wrapper


def handle_tool_errors(func: Callable) -> Callable:
    """工具错误处理装饰器"""

    @wraps(func)
    def wrapper(*args, **kwargs) -> Dict[str, Any]:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Tool {func.__name__} failed: {str(e)}")

            return {
                "status": "error",
                "error": str(e),
                "message": f"工具 {func.__name__} 执行失败: {str(e)}"
            }

    return wrapper


class WorkflowErrorRecovery:
    """工作流错误恢复机制"""

    @staticmethod
    def create_error_recovery_node(error_info: Dict[str, Any]) -> Dict[str, Any]:
        """创建错误恢复节点"""

        error_type = error_info.get("type", "unknown")
        error_message = error_info.get("message", "未知错误")

        recovery_strategies = {
            "llm_error": "LLM服务暂时不可用，请检查网络连接或稍后重试",
            "tool_error": "工具执行失败，请检查输入参数或稍后重试",
            "data_error": "数据获取失败，请检查数据源或稍后重试",
            "strategy_error": "策略生成失败，请调整需求描述或稍后重试",
            "backtest_error": "回测执行失败，请检查策略代码或参数设置"
        }

        recovery_message = recovery_strategies.get(error_type, f"系统错误: {error_message}")

        return {
            "messages": [AIMessage(content=recovery_message)],
            "workflow_step": "error_handled",
            "needs_human_input": True
        }


def validate_state(state: Dict[str, Any]) -> bool:
    """验证状态有效性"""
    try:
        # 检查必要的字段
        required_fields = ["messages"]
        for field in required_fields:
            if field not in state:
                logger.warning(f"Missing required field: {field}")
                return False

        # 检查消息格式
        messages = state.get("messages", [])
        if not isinstance(messages, list):
            logger.warning("Messages field is not a list")
            return False

        return True

    except Exception as e:
        logger.error(f"State validation failed: {str(e)}")
        return False


def safe_workflow_execution(workflow_func: Callable) -> Callable:
    """安全的工作流执行装饰器"""

    @wraps(workflow_func)
    def wrapper(*args, **kwargs):
        try:
            # 执行前验证
            if args and isinstance(args[0], dict):
                if not validate_state(args[0]):
                    raise ValueError("Invalid state provided")

            # 执行工作流
            result = workflow_func(*args, **kwargs)

            # 执行后验证
            if isinstance(result, dict) and not validate_state(result):
                logger.warning("Workflow returned invalid state")

            return result

        except Exception as e:
            logger.error(f"Workflow execution failed: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")

            # 返回安全的错误状态
            return WorkflowErrorRecovery.create_error_recovery_node({
                "type": "workflow_error",
                "message": str(e)
            })

    return wrapper