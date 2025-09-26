

import os
from jinja2 import Environment,FileSystemLoader,select_autoescape

env = Environment(
    loader=FileSystemLoader(os.path.dirname(__file__)),
    autoescape=select_autoescape(),
    trim_blocks=True,
    lstrip_blocks=True
)

def getPrompt(prompt_name,**args) -> str:
    template = env.get_template(f"{prompt_name}.md")
    return template.render(args)