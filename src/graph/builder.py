import stat
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from langgraph.checkpoint.memory import InMemorySaver
from src.graph.state import State
from src.graph.nodes import (
    intention_node,
    plan_node,
    human_feedback_node,
    open_answer_node,
    generate_analytic_web_node,
    generate_strategy_node)
from src.utils.error_handler import handle_node_errors, safe_workflow_execution
from langchain_core.messages import AIMessage


def create_financial_workflow() -> CompiledStateGraph:
    """创建金融策略开发工作流
    start->意图判定->开放式回答->end
    start->意图判定->计划->人类反馈->人类反馈多次->生成数据分析页面->end
    start->意图判定->计划->人类反馈->人类反馈多次->生成策略->end
    start->意图判定->计划->人类反馈->end
    """

    # 创建状态图
    workflow = StateGraph(State)

    # 添加所有节点
    workflow.add_node("intention", intention_node)
    workflow.add_node("open_answer", open_answer_node)
    workflow.add_node("plan", plan_node)
    workflow.add_node("human_feedback", human_feedback_node)
    workflow.add_node("generate_analytic_web", generate_analytic_web_node)
    workflow.add_node("generate_strategy", generate_strategy_node)
    def _route_from_intention(state:State):
        if(state["intention"] == '都不是'):
            return "open_answer"
        else:
            return "plan"
    # 设置起始边 - 从START到intention节点
    workflow.add_edge(START, "intention")
    workflow.add_edge("plan","human_feedback")
    workflow.add_edge("human_feedback",END)
    workflow.add_edge("open_answer",END)

    workflow.add_conditional_edges("intention",_route_from_intention,["plan","open_answer"])
    
    


    # 编译工作流
    memory = InMemorySaver()
    return workflow.compile(checkpointer=memory)
