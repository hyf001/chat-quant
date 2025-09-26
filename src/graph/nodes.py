from datetime import date, datetime
from email import message
import os
from pyexpat import model
from tabnanny import verbose
from tkinter import END
from turtle import goto, mode, update
from typing import Dict, Any
from venv import logger
from langchain_core.messages import HumanMessage, AIMessage,SystemMessage,BaseMessage
from langgraph.types import Command, interrupt
from pydantic import InstanceOf, SecretStr
from src.llms import get_llm_by_type
from src.config.agents import LLMType
from src.graph.state import State
from src.llms import llm
from src.prompt import prompt_util
from src.tools import stock_tools, system_tools
from langgraph.prebuilt import create_react_agent
from langchain_core.runnables import RunnableConfig
from langchain_tavily import TavilySearch

from src.utils import logger
import json

from src.utils.json_utils import repair_json_output
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from langgraph.prebuilt import ToolNode


log = logger.get_logger("__name__")
llm_type = "open-ai"
def intention_node(state: State) -> dict[str,Any]:
    """协调节点 - 判断接下来定哪个节点"""
    intention = "unsupported"
    # 获取最新消息内容
    modle = llm.get_llm_by_type("open-ai")
    response  = modle.invoke([
        SystemMessage(content=
                      prompt_util.getPrompt("coordination",today=datetime.now().strftime("%Y-%m-%d"))),
                    state["messages"][-1],
        ])
    
    if  isinstance (response,AIMessage):
        if isinstance(response.content,str):
            intention = response.content
        elif isinstance(response.content,list):
            intention = response.content[-1]
    log.info(f"识别到意图是{intention}")
    return {"intention":intention,"messages":[response]}


def data_query_node1(state: State,config) -> Command[str]:
    """数据查询节点"""
    model = get_llm_by_type("open-ai")
    tools = [stock_tools.stock_individual_info_em,
             stock_tools.stock_zh_a_hist,
             stock_tools.stock_zh_a_spot_em]
    model_with_tool = model.bind_tools(tools)
    inputs : list[BaseMessage] = [SystemMessage(
        content=prompt_util.getPrompt("data_query"
                                      ,today=datetime.now().strftime("%Y-%m-%d")
                                      ,work_dir="/Users/huyufei/Documents/hyf/code/github/chat-quant/workspace"))]
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


def generate_analytic_web_node(state: State) -> Command[str]:
    """生成数据分析web页面"""
    model = get_llm_by_type("open-ai")
    tools = [stock_tools.search_akshare_interfaces,
             stock_tools.invoke_akshare_interface,
             system_tools.execute_linux_command]
    agent = create_react_agent (model,tools,
                     prompt=prompt_util.getPrompt("data_query",
                                                  today=datetime.now().strftime("%Y-%m-%d"),
                                                  work_dir="/Users/huyufei/Documents/hyf/code/github/chat-quant/workspace")
    )
    messages = {"messages":state["messages"]}
    for step in agent.stream(messages,stream_mode="values"):
        step["messages"][-1].pretty_print()
    return Command(goto=END,update = {"messages":state["messages"]})



def plan_node(state: State,config: RunnableConfig):
    """计划节点 - 生成执行计划"""
    log.info("开始生成执行计划")
    system_prompt=prompt_util.getPrompt("plan",
                                                  today=datetime.now().strftime("%Y-%m-%d"),
                                                  work_dir="/Users/huyufei/Documents/hyf/code/github/chat-quant/workspace",
                                                  intension=state["intention"],
                                                  max_step_num = 5)
    
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    model = get_llm_by_type("open-ai")
    response = model.invoke(messages)
    full_response = response.model_dump_json(indent=4,exclude_none=True)
    try:
        curr_plan = json.loads(repair_json_output(full_response))
    except json.JSONDecodeError:
        log.warning("计划不是一个合法的json格式")
        return Command(goto=END)
    log.info(f"生成的plan:{full_response}")
    return Command(goto="human_feedback",update={"messages":[AIMessage(content=full_response,name="planner")]})


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

def generate_strategy_node(state: State) :
    """生成策略节点"""
    print("生成策略")
    pass


def open_answer_node(state: State) -> Dict[str, Any]:
    """开放式回答问题"""
    tavily_tool = TavilySearch( max_results=5)
    model = get_llm_by_type("open-ai")
    agent = create_react_agent (model,[tavily_tool])
    response = agent.invoke({"messages": [{"role": "user", "content": state["messages"][0].content}]},        
                            {"recursion_limit": 7},)
    return {"messages": response["messages"]}