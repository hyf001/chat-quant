from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from langgraph.checkpoint.memory import InMemorySaver
from src.graph.state import State
from src.graph.nodes import (
    coordination_node,
    plan_node,
    human_feedback_node,
    strategy_generation_handoff_node,
    unsupported_node,
    data_query_node,
    strategy_generation_node)
from src.utils.error_handler import handle_node_errors, safe_workflow_execution
from langchain_core.messages import AIMessage


def create_financial_workflow() -> CompiledStateGraph:
    """创建金融策略开发工作流"""

    # 创建状态图
    workflow = StateGraph(State)

    # 添加所有节点
    workflow.add_node("coordination", coordination_node)
    workflow.add_node("plan", plan_node)
    workflow.add_node("human_feedback", human_feedback_node)
    workflow.add_node("data_query", data_query_node)
    workflow.add_node("strategy_generation_handoff", strategy_generation_handoff_node)
    workflow.add_node("strategy_generation", strategy_generation_node)
    workflow.add_node("unsupported", unsupported_node)

    # 设置起始边 - 从START到coordination节点
    workflow.add_edge(START, "coordination")

    # 协调节点的条件边
    workflow.add_conditional_edges(
        "coordination",
        route_from_coordination,
        ["strategy_generation_handoff","data_query","unsupported"]
    )
    workflow.add_edge("strategy_generation_handoff","plan")
    workflow.add_edge("plan","human_feedback")
    workflow.add_edge("data_query",END)
    workflow.add_edge("unsupported",END)


    workflow.add_edge("strategy_generation",END)

    # 编译工作流
    memory = InMemorySaver()
    return workflow.compile(checkpointer=memory)


def route_from_coordination(state: State) -> str:
    """协调节点的路由函数"""
    if state["intention"] == 'strategy_generation':
        return  "strategy_generation_handoff"
    elif state["intention"] == "data_query":
        return "data_query"
    else :
        return "unsupported"