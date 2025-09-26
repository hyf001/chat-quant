from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START,END
from langchain_openai import ChatOpenAI
import httpx
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.tools import tool

from basic_tool_node import BasicToolNode


class State(TypedDict):
    """
    定义state
    """
    messages: Annotated[list,add_messages]

graph_builder = StateGraph(State)


import dotenv
dotenv.load_dotenv()

llm = ChatOpenAI(model="doubao-1-5-pro-32k-250115")
memory = InMemorySaver()


proxy_client = httpx.Client(proxy="https://crs.xianyi666.top/api",verify=False)



@tool
def query_weather():
     """查询天气"""
     return {"data":"今天晴,温度35度","status":"ok"}

tools = [query_weather]
tool_node = BasicToolNode(tools)
llm_with_tools = llm.bind_tools(tools)

def chatbot(state: State):
    return {"messages":[llm_with_tools.invoke(state["messages"])]}

def route_tools(state : State):
    """工具调用条件路由"""
    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    return END

graph_builder.add_node("chatbot",chatbot)
graph_builder.add_node("tools",tool_node)
graph_builder.add_edge(START,"chatbot")
graph_builder.add_edge("chatbot",END)
graph_builder.add_conditional_edges("chatbot",route_tools,{"tools":"tools",END:END})
graph_builder.add_edge("tools","chatbot")


graph = graph_builder.compile(checkpointer=memory)



def stream_graph_updates(user_input: str,config):
      for event in graph.stream({"messages": [{"role": "user", "content": user_input}]},
                                config,):
            for value in event.values():
                  print("Assistant:", value["messages"][-1].content)

config = {'configurable':{'thread_id':"1"}}

while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break
    stream_graph_updates(user_input,config)