#!/usr/bin/env python3
"""
金融数据策略开发工作流
主入口文件 - 演示如何使用工作流
"""

import asyncio
from json import load, tool
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file

from httpx import stream
from src.graph.state import State
from src.graph import builder
from IPython.display import display ,Image
from langchain_core.messages import HumanMessage
import time
from langgraph.types import Command, interrupt
from src.utils import logger
from src.jupyter import JupyterExecutor
import uvicorn
from src.akshare.akshare_interface import AKShareInterfaceLoader,AKShareInvoker
from src.tools import stock_tools

load_dotenv()

log = logger.get_logger(__name__)

# Environment variables are now loaded from .env file via load_dotenv()
# No need to set them manually here anymore


def show_graph():
    graph = builder.create_financial_workflow()
    png = graph.get_graph().draw_mermaid_png()
    with open("simple_test.png", "wb") as f:
        f.write(png)

def chat(input: str):
    log.info("开始聊天")
    graph = builder.create_financial_workflow()
    state = State(messages=[HumanMessage(content=input)])
    config = {"thread_id":"1"}
    for chunk in graph.stream(state,config):
        if isinstance(chunk,dict):
            for node_name, state_update in chunk.items():
                if node_name == "__interrrupt_":
                    break
                log.info(f"{node_name}==>{state_update}")

    for chunk in graph.stream(Command(resume="edit:第一步 生成文件 第二步 读取文件数据"),config):
        if isinstance(chunk,dict):
            for node_name, state_update in chunk.items():
                log.info(f"{node_name}==>{state_update}")

    asyncio.run(asyncio.sleep(1000))


def execute_code():
    jupyter_exec = JupyterExecutor()
    result = asyncio.run(jupyter_exec.execute_code("a = 10 "))
    print(result)
    result = asyncio.run(jupyter_exec.execute_code("""
print("hello world")
name="caocao0" 
name                                              
"""))
    print(result)

def ak_invoke():
    result = stock_tools.search_akshare_interfaces("300033表现如何")
    if result["status"] == "success":
        for interface in result["interfaces"]:
            print(interface['name'])
    
        




# show_graph()
# chat('300033近10天表现怎么样')
# chat('最近一个月走势比较好的股票有哪些')
# chat('601138怎么样')
chat('今天杭州天气怎么样')
# execute_code()
# ak_invoke()
#if __name__ == "__main__":
#    uvicorn.run("src.server.app:app", host="0.0.0.0", port=8000, reload=True)