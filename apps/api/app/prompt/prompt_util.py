import os
from tempfile import template
from jinja2 import Environment, FileSystemLoader, select_autoescape
from app.common.types import AgentType

env = Environment(
    loader=FileSystemLoader(os.path.dirname(__file__)),
    autoescape=select_autoescape(),
    trim_blocks=True,
    lstrip_blocks=True
)

def getPrompt( agent_type : AgentType, ** args ) -> str:
    """
    根据模版获取prompt
    agent_type: 智能体类型
    args: 模版参数 要跟prompt中的模版占位符一致
    """
    template = env.get_template(f"system-prompt-{agent_type.value}.md")
    return template.render(args)