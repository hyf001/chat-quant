from datetime import date, datetime
from email import message
from math import log
from pyexpat import model
from tabnanny import verbose
from tkinter import END
from turtle import goto, mode, update
from typing import Dict, Any
from venv import logger
from langchain_core.messages import HumanMessage, AIMessage,SystemMessage,BaseMessage
from langgraph.types import Command, interrupt
from pydantic import InstanceOf
from src import llms
from src.config.agents import LLMType
from src.graph.state import State
from src.llms import llm
from src.prompt import prompt_util
from src.tools import stock_tools, system_tools
from langgraph.prebuilt import create_react_agent

def coordination_node(state: State) -> Command:
    """协调节点 - 判断接下来定哪个节点"""
    intension = "unsupported"
    # 获取最新消息内容
    modle = llm.get_llm_by_type("moonshot")
    response  = modle.invoke([
        SystemMessage(content=
                      prompt_util.getPromptTemplate("src/prompt/coordination.md")),
                    state["messages"][-1],
        ])
    
    if  isinstance (response,AIMessage):
        if isinstance(response.content,str):
            intension = response.content
        elif isinstance(response.content,list):
            intension = response.content[-1]

    return Command(update={"intention":intension,"messages":[response]})


def data_query_node1(state: State,config) -> Command[str]:
    """数据查询节点"""
    model = llm.get_llm_by_type("moonshot")
    tools = [stock_tools.stock_individual_info_em,
             stock_tools.stock_zh_a_hist,
             stock_tools.stock_zh_a_spot_em]
    model_with_tool = model.bind_tools(tools)
    inputs : list[BaseMessage] = [SystemMessage(
        content=prompt_util.getPromptTemplate("src/prompt/data_query.md").format(
                          today=datetime.now().strftime("%Y-%m-%d"),
                          work_dir="/Users/huyufei/Documents/hyf/code/github/chat-quant/workspace"))]
    inputs.extend(state["messages"])
    ai_message : AIMessage = model_with_tool.invoke(inputs)
    # 检查是否有工具调用
    if ai_message.tool_calls:
       tool_handler = stock_tools.ToolCall(tools)
       tool_results = tool_handler({"messages":[ai_message]},config)
       return Command(goto=END, 
        update={"messages": [ai_message] + 
        tool_results["messages"]})
    else:
       return Command(goto=END, update={"messages": [ai_message]})


def data_query_node(state: State) -> Command[str]:
    """数据查询节点"""
    model = llm.get_llm_by_type("moonshot")
    tools = [stock_tools.search_akshare_interfaces,
             stock_tools.invoke_akshare_interface,
             system_tools.execute_linux_command]
    agent = create_react_agent (model,tools,
                     prompt=prompt_util.getPromptTemplate("src/prompt/data_query.md").format(
                          today=datetime.now().strftime("%Y-%m-%d"),
                          work_dir="/Users/huyufei/Documents/hyf/code/github/chat-quant/workspace")
    )
    messages = {"messages":state["messages"]}
    for step in agent.stream(messages,stream_mode="values"):
        step["messages"][-1].pretty_print()
    return Command(goto=END,update = {"messages":state["messages"]})



def plan_node(state: State):
    """计划节点 - 生成执行计划"""

    user_request = (state["messages"][-1].content if state["messages"] else "")
    pass


def human_feedback_node(state: State) -> Command[str]:
    """人工调整计划节点 - 处理同意(accept)、中止(terminate)、重新生成(regen)、调整(edit)三种输入"""
    feedback = interrupt("Please Review the Plan.")
    if str(feedback).startswith('accept'):
        return Command(goto="strategy_generation")
    elif str(feedback).startswith('terminate'):
        return Command(goto=END)
    elif str(feedback).startswith('regen'):
        return Command(goto="plan",update={"messages":HumanMessage(content=str(feedback)[6:],name="feedback")})
    elif str(feedback).startswith('edit'):
        return Command(goto="strategy_generation",update={"current_plan":str(feedback)[6:]})
    return Command(goto="strategy_generation")

def strategy_generation_node(state: State) :
    """生成策略节点"""
    print("生成策略")
    pass

def strategy_generation_handoff_node(state: State) :
    """生成策略节点过度节点"""
    pass


def unsupported_node(state: State) -> Dict[str, Any]:
    """不支持的请求节点"""

    error_message = AIMessage(
        content="抱歉，我暂时无法处理这个请求。请尝试以下类型的请求:\n1. 金融数据查询\n2. 交易策略生成\n3. 策略回测分析"
    )

    return {
        "messages": [error_message],
        "workflow_step": "error"
    }